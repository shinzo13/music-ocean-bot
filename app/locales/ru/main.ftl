# shared
btn-back = Назад
btn-yes = Да
btn-no = Нет
btn-cancel = Отмена

## main menu
welcome = Добро пожаловать в <b>Music Ocean!</b> 🌊
btn-how-to-use = Как пользоваться?
btn-profile = Профиль
btn-settings = Настройки
btn-admin-panel = Админ-панель
usage-guide-text = Гайд доступен по <a href='{$guide_url}'>этой ссылке</a>.

## profile
profile-text =
    <b>👤 {$user}</b>

    <b>• Зарегистрирован</b>: <code>{$registered}</code>
    <b>• Скачано треков</b>: <code>{$tracks_downloaded}</code>

## settings
settings-text = Настройки
option-already-selected = Эта опция уже выбрана.

btn-language = Язык
choose-language = Выберите язык:
language-changed = 🇷🇺 Язык изменён!

btn-music-engine = Музыкальная платформа
choose-engine = Выберите платформу по умолчанию:
engine-changed = ✅ Движок по умолчанию изменен
btn-scrobbling = Скробблинг

btn-track-previews = Превью треков
choose-previews = Выберите вид превью треков:
previews-changed = ✅ Превью треков изменено

btn-show-covers = Показывать обложки
btn-show-mp3-previews = Показывать MP3-фрагменты

feature-not-available = 🔒 Эта функция пока недоступна.

## scrobbling
scrobbling-description =
    <b>Скробблинг</b>

    Войдите в свой аккаунт Last.fm и получите возможность быстро скачивать треки прослушанные в других плеерах.
scrobbling-already-setup = Скробблинг уже настроен!
scrobbling-enter-username = Введите ваш юзернейм на Last.fm:
scrobbling-invalid-username = Неверный юзернейм, попробуйте ещё раз.
scrobbling-no-data = Нет данных о прослушиваниях.
scrobbling-is-that-right =
    Последний трек: <i>{ $artist } - { $title }</i>

    Всё верно?
scrobbling-success = ✅ Скробблинг Last.fm настроен.
btn-setup-scrobbling = Настроить скробблинг
btn-setup-scrobbling-again = Изменить юзернейм

## admin panel
admin-panel-text = Админ-панель
btn-export-users = Экспорт пользователей
btn-mailing = Рассылка
btn-mailing-send = Отправить
mailing-enter-message = Введите сообщение для рассылки:
mailing-canceled = Отменено.
mailing-sending = Отправляю всем пользователям...
mailing-finished = Рассылка завершена ({ $succeed }/{ $all } успешно).

## track info
track-info =
    <blockquote><b><i>{ $artist_name } - { $title }</i></b></blockquote>

    • <b>Движок</b>: {$engine_emoji}  <code>{$engine_name}</code>
track-info-admin =
    • <b>ID трека</b>: <code>{ $track_id }</code>
    • <b>Скачал</b>: { $downloaded_by }
track-not-found = Этот трек не скачивался через Music Ocean.
btn-album = Альбом
btn-artist = Исполнитель

## inline search
usage-guide-title = Как пользоваться расширенным поиском?
usage-guide-description = Нажмите, чтобы открыть руководство.
usage-guide-message = <b>Как пользоваться расширенным поиском?</b>

    i dont know
feature-soundcloud-link-search = Поиск по ссылке SoundCloud
feature-youtube-advanced-search = Расширенный поиск по YouTube
not-supported-title = { $feature } пока не поддерживается.
not-supported-description = :(
not-supported-message = Эта функция пока недоступна.
setup-scrobbling-title = Скробблинг Spotify
setup-scrobbling-description = Настройте скробблинг, чтобы мгновенно скачивать то, что слушаете!
setup-scrobbling-message = <b>Скробблинг Spotify</b>

    Настройте скробблинг чтобы быстро скачивать треки которые вы слушаете! мямямямя

## downloading
invalid-link = Неверная ссылка.
downloading = Скачиваю...
downloaded = Скачано!
btn-search-for-track = Найти трек
btn-download-all = Скачать все треки
btn-downloading = Скачиваю...

## entities
entity-album =
    <b>{$title}</b>
    <i>{$artist_name}</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-playlist =
    <b>{$title}</b>
    <i>{$track_count} треков</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>
entity-artist =
    <b>{$name}</b>
    <i>{$listeners} слушателей</i>
    <a href="{$cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>

# other
recognizing = <i>Распознаю...</i>
not-recognized = <i>Не распознано!</i>