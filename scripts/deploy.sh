#!/usr/bin/env bash
# Pull-based deploy. The server asks github what is new instead of github
# reaching in: nothing has to be exposed, no runner executes foreign code on a
# machine that also holds the production database.
#
# Deploys only a commit whose CI is green, checks the bot afterwards, and rolls
# back to the previous commit if it is not.
#
# Usage: deploy.sh [--force]   (--force skips the CI check, for a manual fix)
set -uo pipefail

PROJECT="${PROJECT:-$HOME/projects/music-ocean-bot}"
NOTIFY="${NOTIFY:-$HOME/.claude/notify-telegram.sh}"
REPO="${REPO:-shinzo13/music-ocean-bot}"
BRANCH="${BRANCH:-main}"
CONTAINER="${CONTAINER:-music-ocean-bot-bot-1}"
STATE_DIR="${STATE_DIR:-$HOME/.local/state/koshke-deploy}"
HEALTH_WAIT="${HEALTH_WAIT:-25}"

force=0
[ "${1:-}" = "--force" ] && force=1

mkdir -p "$STATE_DIR"
exec 9>"$STATE_DIR/lock"
# A deploy started while the previous one is still building would fight it over
# the same container.
flock -n 9 || { echo "another deploy is running"; exit 0; }

log() { printf '%s %s\n' "$(date -u '+%F %T')" "$*"; }
notify() { [ -x "$NOTIFY" ] && "$NOTIFY" "$1" >/dev/null 2>&1 || true; }

cd "$PROJECT" || { notify "🔴 кошке: не найден каталог $PROJECT"; exit 1; }

git fetch --quiet origin "$BRANCH" || { log "fetch failed"; exit 1; }

current=$(git rev-parse HEAD)
target=$(git rev-parse "origin/$BRANCH")
[ "$current" = "$target" ] && { log "already at ${target:0:7}"; exit 0; }

# This script resets the checkout it runs in, so it must not run in the one
# where work happens: an uncommitted edit would be gone without a word. The
# deploy directory is a separate clone that nobody types in.
if [ -n "$(git status --porcelain)" ]; then
    log "working copy is dirty, refusing to reset it"
    notify "🔴 кошке: в $PROJECT есть несохранённые изменения, деплой не трогаю"
    exit 1
fi

log "new commit ${target:0:7} (at ${current:0:7})"

if [ "$force" -eq 0 ]; then
    # Deploying a commit whose tests never ran is how a red build reaches
    # production while everyone believes CI is protecting them.
    status=$(curl -s -m 20 "https://api.github.com/repos/$REPO/commits/$target/check-runs" \
        | python3 -c "
import json, sys
try:
    runs = json.load(sys.stdin).get('check_runs', [])
except Exception:
    print('unknown'); raise SystemExit
if not runs:
    print('pending'); raise SystemExit
if any(r['status'] != 'completed' for r in runs):
    print('pending')
elif all(r['conclusion'] in ('success', 'neutral', 'skipped') for r in runs):
    print('success')
else:
    print('failure')
")
    case "$status" in
        success) log "ci is green" ;;
        pending) log "ci still running, waiting for the next round"; exit 0 ;;
        failure)
            log "ci failed for ${target:0:7}"
            marker="$STATE_DIR/failed-$target"
            [ -f "$marker" ] || { touch "$marker"; notify "🔴 кошке: CI красный на ${target:0:7}, деплой не поеду делать"; }
            exit 1
            ;;
        *) log "could not read ci status, skipping this round"; exit 0 ;;
    esac
fi

subject=$(git log -1 --format=%s "$target")

git reset --hard --quiet "$target" || { notify "🔴 кошке: не смог перейти на ${target:0:7}"; exit 1; }

log "building"
if ! docker compose up -d --build >"$STATE_DIR/last-build.log" 2>&1; then
    log "build failed, rolling back"
    git reset --hard --quiet "$current"
    docker compose up -d --build >/dev/null 2>&1
    notify "🔴 кошке: сборка ${target:0:7} упала, откатился на ${current:0:7}
$(tail -5 "$STATE_DIR/last-build.log")"
    exit 1
fi

sleep "$HEALTH_WAIT"

healthy=1
state=$(docker inspect -f '{{.State.Status}}' "$CONTAINER" 2>/dev/null)
[ "$state" = "running" ] || healthy=0
# A container that starts and dies on the first update looks "running" for a
# few seconds, so the log has to be clean too.
if docker logs --since "${HEALTH_WAIT}s" "$CONTAINER" 2>&1 | grep -qE ' - (ERROR|CRITICAL) - |^Traceback'; then
    healthy=0
fi

if [ "$healthy" -eq 0 ]; then
    log "unhealthy after deploy, rolling back to ${current:0:7}"
    git reset --hard --quiet "$current"
    docker compose up -d --build >/dev/null 2>&1
    notify "🔴 кошке: ${target:0:7} не поднялся (status=${state:-нет}), откатился на ${current:0:7}
$(docker logs --since 60s "$CONTAINER" 2>&1 | grep -E ' - (ERROR|CRITICAL) - ' | head -3)"
    exit 1
fi

echo "$target" > "$STATE_DIR/last-deployed"
log "deployed ${target:0:7}"
notify "🟢 кошке: выкатил ${target:0:7} — $subject"
