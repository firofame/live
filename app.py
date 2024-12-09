import json

# Load the input JSON
with open('input.json', 'r') as f:
    data = json.load(f)

# Create the M3U playlist content
playlist = "#EXTM3U\n"

for channel in data['channels']:
    name = channel['name']
    logo = channel['tvg-logo']
    group_title = channel['group-title']
    url = channel['url']
    
    # Add the channel to the playlist
    playlist += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group_title}", {name}\n'
    playlist += f'{url}\n'

# Write the M3U playlist to a file
with open('playlist.m3u', 'w') as f:
    f.write(playlist)

print("Playlist generated successfully as 'playlist.m3u'")
