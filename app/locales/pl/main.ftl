# shared
btn-back = Wróć
btn-yes = Tak
btn-no = Nie
btn-cancel = Odrzuć

## main menu
welcome = Witamy w <b>{ $brand }!</b>
btn-how-to-use = Jak używać?
btn-profile = Konto
btn-settings = Ustawienia
btn-admin-panel = Panel administratora
usage-guide-text = Tutorial jest dostępny poprzez <a href='{$guide_url}'>ten link</a>.

## profile
profile-text =
    <b>👤 {$user}</b>

    <b>• Zarejestrowany</b>: <code>{$registered}</code>
    <b>• Pobrano utworów</b>: <code>{$tracks_downloaded}</code>

## settings
settings-text = Ustawienia
option-already-selected = Ta opcja jest już wybrana.

btn-language = Język
choose-language = Wybierz język:
language-changed = 🇬🇧 Język został zmieniony!

btn-music-engine = Platforma muzyczna
choose-engine = Wybierz domyślną platformę muzyczną:
engine-changed = ✅ Zmieniono domyślną platformę muzyczną
btn-scrobbling = Scrobbling

btn-track-previews = Podgląd utworu
choose-previews = Wybierz wygląd podglądu utworu:
previews-changed = ✅ Zmieniono podgląd utworu
previews-already-selected = ☑️ Ta opcja jest już wybrana

btn-show-covers = Pokazuj okładki
btn-show-mp3-previews = Pokazuj fragmenty MP3

feature-not-available = 🔒 Ta opcja jest chwilowo niedostępna.

## scrobbling
scrobbling-description = <b>Scrobbling</b>

    Zaloguj się na swoje konto Last.fm i zyskaj możliwość szybkiego pobierania utworów przesłuchanych w innych odtwarzaczach.
scrobbling-already-setup = Scrobbling jest już skonfigurowany!
scrobbling-enter-username = Podaj swój username Last.fm:
scrobbling-invalid-username = Nieprawidłowy username, spróbuj ponownie.
scrobbling-no-data = Brak informacji o odsłuchach.
scrobbling-is-that-right =
    Ostatni utwór: <i>{ $artist } - { $title }</i>

    Zgadza się?
scrobbling-success = ✅ Scrobbling Last.fm został skonfigurowany.
btn-setup-scrobbling = Skonfiguruj scrobbling
btn-setup-scrobbling-again = Zmień username

## admin panel
admin-panel-text = Panel administratora
btn-export-users = Eksportuj użytkowników
btn-mailing = Mailing
btn-mailing-send = Wyślij
mailing-enter-message = <i>Wpisz wiadomość do wysłania:</i>
mailing-enter-buttons =
    <i>Wpisz przyciski w takim formacie:</i>

    <code>
    przycisk1 - link1
    przycisk2 - link2
    { "[...]" }
    </code>

mailing-restricted-content-type = <i>Tego typu treści nie można wysłać, wyślij inną wiadomość.</i>
mailing-approve-message = <i>Wysłać to do wszystkich użytkowników?</i>
mailing-invalid-format = <i>Nieprawidłowy format, spróbuj ponownie.</i>
mailing-canceled = <i>Odrzucono.</i>
mailing-sending = <i>Wysyłam do wszystkich użytkowników...</i>
mailing-finished = <i>Mailing zakończony ({ $succeed }/{ $all } pomyślnie).</i>

## track info
track-info =
    <blockquote><b><i>{ $artist_name } - { $title }</i></b></blockquote>

    • <b>Platforma</b>: {$engine_emoji}  <code>{$engine_name}</code>
track-info-admin =
    • <b>ID utworu</b>: <code>{ $track_id }</code>
    • <b>Pobrano przez</b>: { $downloaded_by }
track-not-found = Ten utwór nie był pobierany przez { $brand }.
btn-album = Album
btn-artist = Wykonawca

## inline search
usage-guide-title = Jak używać zaawansowanego wyszukiwania?
usage-guide-description = Kliknij tutaj, aby zobaczyć instrukcję.
usage-guide-message =
    <b>Jak używać zaawansowanego wyszukiwania?</b>

    i dont know
feature-soundcloud-link-search = Wyszukiwanie po linku SoundCloud
feature-spotify-link-search = Wyszukiwanie po linku Spotify (playlista/artysta)
feature-youtube-advanced-search = Zaansowane wyszukiwanie przez YT
not-supported-title = { $feature } nie jest aktualnie obsługiwane.
not-supported-description = :(
not-supported-message = Ta funkcja nie jest jeszcze dostępna.
setup-scrobbling-title = Scrobbling Spotify
setup-scrobbling-description = Skonfiguruj scrobbling, aby natychmiast pobierać słuchane utwory!
setup-scrobbling-message =
    <b>Scrobbling Spotify</b>

    Zaloguj się na swoje konto Spotify i zyskaj możliwość szybkiego pobierania utworów z odtwarzacza.

## downloading
invalid-link = Nieprawidłowy link.
downloading = Pobieranie...
downloaded = Pobrano!
btn-search-for-track = Szukaj utworu
btn-download-all = Pobierz wszystkie utwory
btn-downloading = Pobieranie...

## entities
entity-album =
    <b>{$title}</b>
    <i>{$artist_name}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-playlist =
    <b>{$title}</b>
    <i>{$track_count} utworów</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-artist =
    <b>{$name}</b>
    <i>{$listeners} słuchaczy</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>

# other
recognizing = <i>Rozpoznuję...</i>
not-recognized = <i>Nie rozpoznano!</i>

## support / errors
error-track-unavailable = Ten utwór jest niedostępny do pobrania.
support-hint = Jeśli problem nadal występuje — napisz do wsparcia @koshkesupportbot

## support menu
btn-support = Wsparcie
btn-write-support = Contact support
support-text =
    <b>Wsparcie</b>

    Masz pytanie, błąd lub utwór się nie pobiera? Napisz do nas — odpowiemy tutaj, na Telegramie.

## top
top-title = 🏆 <b>Top wg pobrań</b>
top-empty = Nikt jeszcze niczego nie pobrał.

## moderation
unban-notice = 🔓 <b>Blokada zdjęta.</b> Możesz znowu korzystać z bota — witamy z powrotem!
