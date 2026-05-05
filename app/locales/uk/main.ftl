# shared
btn-back = Назад
btn-yes = Так
btn-no = Ні
btn-cancel = Скасувати

## main menu
welcome = Ласкаво просимо до <b>Music Ocean!</b> 🌊
btn-how-to-use = Як користуватись?
btn-profile = Профіль
btn-settings = Налаштування
btn-admin-panel = Адмін-панель
usage-guide-text = ькцлдцкпл

## profile
profile-text =
    <b>👤 {$user}</b>

    <b>• Зареєстрований</b>: <code>{$registered}</code>
    <b>• Завантажено треків</b>: <code>{$tracks_downloaded}</code>

## settings
settings-text = Налаштування
option-already-selected = Цей варіант вже вибрано.

btn-language = Мова
choose-language = Оберіть мову:
language-changed = 🇺🇦 Мову змінено!

btn-music-engine = Музичний рушій
choose-engine = Оберіть рушій за замовчуванням:
engine-changed = ✅ Рушій за замовчуванням змінено
btn-scrobbling = Скроблінг

btn-track-previews = Превʼю треку
choose-previews = Оберіть вигляд превʼю треку:
previews-changed = ✅ Превʼю треку змінено

btn-show-covers = Показувати обкладинки
btn-show-mp3-previews = Показувати MP3-фрагменти

feature-not-available = 🔒 Ця функція поки недоступна.

## scrobbling
scrobbling-description = <b>Скроблінг</b>

    Увійдіть у свій акаунт Last.fm і отримайте можливість швидко завантажувати треки прослухані в інших плеєрах.
scrobbling-already-setup = Скроблінг вже налаштовано!
scrobbling-enter-username = Введіть ваш юзернейм на Last.fm:
scrobbling-invalid-username = Невірний юзернейм, спробуйте ще раз.
scrobbling-no-data = Немає даних про прослуховування.
scrobbling-is-that-right = Останній трек: <i>{ $artist } - { $title }</i>

    Все вірно?
scrobbling-success = ✅ Скроблінг Last.fm налаштовано.
btn-setup-scrobbling = Налаштувати скроблінг
btn-setup-scrobbling-again = Змінити юзернейм

## admin panel
admin-panel-text = Програ́мний руші́й
btn-export-users = Експорт користувачів
btn-mailing = Розсилка
btn-mailing-send = Надіслати
mailing-enter-message = Введіть повідомлення для розсилки:
mailing-canceled = Скасовано.
mailing-sending = Надсилаю всім користувачам...
mailing-finished = Розсилку завершено ({ $succeed }/{ $all } успішно).

## track info
track-info =
    <blockquote><b><i>{ $artist_name } - { $title }</i></b></blockquote>

    • <b>Рушій</b>: {$engine_emoji}  <code>{$engine_name}</code>
track-info-admin =
    • <b>ID треку</b>: <code>{ $track_id }</code>
    • <b>Завантажив</b>: { $downloaded_by }
track-not-found = Цей трек не завантажувався через Music Ocean.
btn-album = Альбом
btn-artist = Виконавець

## inline search
usage-guide-title = Як користуватись розширеним пошуком?
usage-guide-description = Натисніть, щоб відкрити інструкцію.
usage-guide-message = <b>Як користуватись розширеним пошуком?</b>

    i dont know
feature-soundcloud-link-search = Пошук за посиланням SoundCloud
not-supported-title = { $feature } поки не підтримується.
not-supported-description = :(
not-supported-message = Ця функція поки недоступна.
setup-scrobbling-title = Скроблінг
setup-scrobbling-description = Налаштуйте скроблінг, щоб миттєво завантажувати те, що слухаєте!
setup-scrobbling-message = <b>Скроблінг Spotify</b>

    Налаштуйте ьлициштзцкитзц ТУДУ швидко завантажувати треки з плеєра.

## downloading
invalid-link = Невірне посилання.
downloading = Завантажую...
downloaded = Завантажено!
btn-search-for-track = Знайти трек
btn-download-all = Завантажити всі треки
btn-downloading = Завантажую...

## entities
entity-album =
    <b>{$title}</b>
    <i>{$artist_name}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-playlist =
    <b>{$title}</b>
    <i>{$track_count}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
