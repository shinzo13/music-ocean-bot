# shared
btn-back = Back
btn-yes = Yes
btn-no = No
btn-cancel = Cancel

## main menu
welcome = Welcome to <b>Music Ocean!</b> 🌊
btn-how-to-use = How to use?
btn-profile = Profile
btn-settings = Settings
btn-admin-panel = Admin panel
usage-guide-text = Usage guide is available via <a href='{$guide_url}'>this link</a>.

## profile
profile-text =
    <b>👤 {$user}</b>

    <b>• Registered</b>: <code>{$registered}</code>
    <b>• Tracks downloaded</b>: <code>{$tracks_downloaded}</code>

## settings
settings-text = Settings
option-already-selected = This option is already selected.


btn-language = Language
choose-language = Choose language:
language-changed = 🇬🇧 Language changed!

btn-music-engine = Music engine
choose-engine = Choose a default engine to use:
engine-changed = ✅ Engine changed successfully
btn-scrobbling = Scrobbling

btn-track-previews = Track previews
choose-previews = Choose track preview appearance:
previews-changed = ✅ Track preview options changed successfully

btn-show-covers = Show covers
btn-show-mp3-previews = Show MP3 previews

feature-not-available = 🔒 This feature is not available at the moment.

## scrobbling
scrobbling-description =
    <b>Scrobbling</b>

    Log in into your Last.fm account and get ability to quickly download tracks you have listened to in other players.
scrobbling-already-setup = Scrobbling is already configured!
scrobbling-enter-username = Enter your Last.fm username:
scrobbling-invalid-username = Invalid username, try again.
scrobbling-no-data = No listening data available.
scrobbling-is-that-right =
    Last track: <i>{ $artist } - { $title }</i>

    Is that right?
scrobbling-success = ✅ Last.fm scrobbling successfully set up.
btn-setup-scrobbling = Setup scrobbling
btn-setup-scrobbling-again = Edit username

## admin panel
admin-panel-text = Admin panel
btn-export-users = Export users
btn-mailing = Mailing
btn-mailing-send = Send
mailing-enter-message = Send a message for mailing:
mailing-canceled = Canceled.
mailing-sending = Sending to all users...
mailing-finished = Mailing finished ({ $succeed }/{ $all } succeeded).

## track info
track-info =
    <blockquote><b><i>{ $artist_name } - { $title }</i></b></blockquote>

    • <b>Engine</b>: {$engine_emoji}  <code>{$engine_name}</code>
track-info-admin =
    • <b>Track ID</b>: <code>{ $track_id }</code>
    • <b>Downloaded by</b>: { $downloaded_by }
track-not-found = This track was not downloaded via Music Ocean.
btn-album = Album
btn-artist = Artist

## inline search
usage-guide-title = How to use advanced search?
usage-guide-description = Click here to see the usage guide.
usage-guide-message =
    <b>How to use advanced search?</b>

    i dont know
feature-soundcloud-link-search = SoundCloud link search
feature-youtube-advanced-search = YouTube-based advanced search
not-supported-title = { $feature } is not supported at the moment.
not-supported-description = :(
not-supported-message = This feature is not supported yet.
setup-scrobbling-title = Spotify scrobbling
setup-scrobbling-description = Set up scrobbling to instantly download tracks you're listening to!
setup-scrobbling-message =
    <b>Spotify scrobbling</b>

    Log in into your Spotify account and get ability to quickly download tracks from your player.

## downloading
invalid-link = Invalid link.
downloading = Downloading...
downloaded = Downloaded!
btn-search-for-track = Search for track
btn-download-all = Download all tracks
btn-downloading = Downloading...

## entities
entity-album =
    <b>{$title}</b>
    <i>{$artist_name}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-playlist =
    <b>{$title}</b>
    <i>{$track_count}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-artist =
    <b>{$name}</b>
    <i>{$listeners} listeners</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>

# other
recognizing = <i>Recognizing...</i>
not-recognized = <i>Not recognized!</i>