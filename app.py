import json
import re
import requests

def read_handles(file_path):
    with open(file_path, 'r') as f:
        return [tuple(line.strip().split(',')) for line in f]

def fetch_channel_data(handle):
    url = f'https://www.youtube.com/@{handle}/live'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for handle {handle}: {e}")
        return None

    match = re.search(r'var ytInitialData = ({.*?});', response.text)
    if not match:
        print(f"No ytInitialData found for handle {handle}")
        return None

    try:
        json_data = match.group(1)
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data for handle {handle}: {e}")
        return None

    try:
        channel_name = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
        image_url = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][-1]['url']
        channel_id = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['title']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
    except (KeyError, IndexError) as e:
        print(f"Error extracting channel data for handle {handle}: {e}")
        return None

    return {
        'channel_name': channel_name,
        'image_url': image_url,
        'channel_id': channel_id
    }

def write_playlist(file_path, handles):
    with open(file_path, 'w') as f:
        f.write('#EXTM3U\n')
        for handle, group in handles:
            channel_data = fetch_channel_data(handle)
            if channel_data:
                m3u8_url = f'https://ythls.armelin.one/channel/{channel_data["channel_id"]}.m3u8'
                f.write(f'#EXTINF:-1 tvg-logo="{channel_data["image_url"]}" group-title="{group}", {channel_data["channel_name"]}\n{m3u8_url}\n')

def write_channel_data(file_path, handles):
    channel_data = []
    for handle, group in handles:
        data = fetch_channel_data(handle)
        if data:
            channel_data.append({
                'channel_name': data['channel_name'],
                'channel_id': data['channel_id']
            })
    with open(file_path, 'w') as f:
        json.dump(channel_data, f)

handles = read_handles('handles.txt')
write_playlist('playlist.m3u', handles)
write_channel_data('playlist.json', handles)
