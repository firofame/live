import json
import re
import requests

# Read the handles from a file
with open('handles.txt', 'r') as f:
    handles = [tuple(line.strip().split(',')) for line in f]

# Write the playlist file
with open('playlist.m3u8', 'w') as f:
    f.write('#EXTM3U\n\n')
    for i, (handle, group) in enumerate(handles, start=1):
        # Construct the URL for the channel's live stream
        url = f'https://www.youtube.com/@{handle}/live'

        # Send a GET request to the URL
        response = requests.get(url)

        # Search for the ytInitialData variable in the page source
        match = re.search(r'var ytInitialData = ({.*?});', response.text)

        # Extract the JSON data from the match
        json_data = match.group(1)

        # Parse the JSON data
        data = json.loads(json_data)

        # Extract the channel name and image URL
        channel_name = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
        image_url = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][-1]['url']

        # Construct the M3U8 URL for the channel's live stream
        m3u8_url = f'https://live.firofame.workers.dev/?@={handle}'

        # Write the metadata and URL to the playlist file
        f.write(f'#EXTINF:-1 tvg-logo="{image_url}" group-title="{group}", {channel_name}\n{m3u8_url}\n\n')
