from app.modules.musicocean.engines.youtube.utils.parsers.parse_track_info import parse_track_info


def parse_search_response(raw_data: dict):
    tracks = []
    try:
        tabs = raw_data['contents']['tabbedSearchResultsRenderer']['tabs']
        for tab in tabs:
            if 'tabRenderer' in tab and tab['tabRenderer'].get('selected', False):
                sections = tab['tabRenderer']['content']['sectionListRenderer']['contents']
                for section in sections:
                    if 'musicShelfRenderer' in section:
                        shelf = section['musicShelfRenderer']
                        if 'title' in shelf and shelf['title']['runs'][0]['text'] == 'Songs':
                            contents = shelf['contents']
                            for item in contents:
                                if 'musicResponsiveListItemRenderer' in item:
                                    track_info = parse_track_info(
                                        item['musicResponsiveListItemRenderer']
                                    )
                                    tracks.append(track_info)

    except (KeyError, IndexError):
        raise RuntimeError("idk how to parse it")

    return tracks