def parse_track_info(music_responsive_item):
    track_info = {}

    if 'playlistItemData' in music_responsive_item:
        track_info['video_id'] = music_responsive_item['playlistItemData']['videoId']

    if 'thumbnail' in music_responsive_item:
        thumbnails = music_responsive_item['thumbnail']['musicThumbnailRenderer']['thumbnail']['thumbnails']
        track_info['thumbnail'] = thumbnails[-1]['url']

    if 'flexColumns' in music_responsive_item:
        flex_columns = music_responsive_item['flexColumns']
        if len(flex_columns) > 0:
            first_column = flex_columns[0]['musicResponsiveListItemFlexColumnRenderer']
            if 'text' in first_column and 'runs' in first_column['text']:
                track_info['title'] = first_column['text']['runs'][0]['text']
        if len(flex_columns) > 1:
            second_column = flex_columns[1]['musicResponsiveListItemFlexColumnRenderer']
            if 'text' in second_column and 'runs' in second_column['text']:
                runs = second_column['text']['runs']
                if len(runs) > 0 and 'navigationEndpoint' in runs[0]:
                    track_info['artist'] = runs[0]['text']
                    if 'browseEndpoint' in runs[0]['navigationEndpoint']:
                        track_info['artist_id'] = runs[0]['navigationEndpoint']['browseEndpoint']['browseId']
                if len(runs) > 2 and 'navigationEndpoint' in runs[2]:
                    track_info['album'] = runs[2]['text']
                    if 'browseEndpoint' in runs[2]['navigationEndpoint']:
                        track_info['album_id'] = runs[2]['navigationEndpoint']['browseEndpoint']['browseId']
                if len(runs) > 4:
                    track_info['duration'] = runs[-1]['text']
        if len(flex_columns) > 2:
            third_column = flex_columns[2]['musicResponsiveListItemFlexColumnRenderer']
            if 'text' in third_column and 'runs' in third_column['text']:
                track_info['plays'] = third_column['text']['runs'][0]['text']

    return track_info
