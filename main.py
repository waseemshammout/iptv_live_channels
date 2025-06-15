import requests
from datetime import datetime
import pandas as pd

def get_streams(url):
    
    """
    Purpose: Gets individual url for all files
    Input  : str presents the API endpoint of streams
    Output : A dictionary where k = file name and v = URL
    """
    
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        names = list()
        urls = list()
        for file in files:
            names.append(file['name'])
            urls.append(file['download_url'])
    return dict(zip(names, urls))

dict_files = get_streams('https://api.github.com/repos/iptv-org/iptv/contents/streams')

def get_url_content(url):
    
    """
    Purpose: Getting the contents of m3u file using a supplied URL
    Input  : str presents an single url
    Output : A list of m3u file content
    """
    
    lines = list()
    response = requests.get(url=url)
    if response.status_code == 200:
        for line in response.text.splitlines():
            if line.find('#EXTM3U') == -1 and line.find('EXTVLCOPT') == -1:
                line = line.strip()
            lines.append(line)
    return lines

# urls = dict_files.values()

# for i, url in enumerate(urls):
#     content = get_url_content(url)
#     contents_clean = content[1:]
#     with open('t.txt', 'a', encoding='utf-8') as txtFile:
#         txtFile.write('\n'.join(contents_clean) + '\n')
#         txtFile.close()
#         print(i + 1, 'is done!')

def parse_channels(fileName):
    line_open = False
    channels_dict = dict()
    channel_url, channel_name = "", ""
    with open(fileName, "r", encoding='utf-8') as tFile:
        for i, line in enumerate(tFile.readlines()):
            line = line.replace("\n", "")
            if line.find('#EXTVLCOPT:') != -1:
                line_open = True
                continue
            elif line.find('#EXTINF:-1 tvg-id="') != -1:
                line_open = True
                channel_name = line[line.find(",") + 1 :]
                if channel_name.find('like Gecko') != -1:
                    channel_name = channel_name[channel_name.find(',')+1:]
            elif line_open and line.find("http") != -1:
                channel_url = line
                line_open = False
                if not (channel_name in channels_dict.keys()):
                    channels_dict[channel_name] = channel_url
    df = pd.DataFrame({
        'channel_name':channels_dict.keys(),
        'channel_url':channels_dict.values()
    })
    return df

df = parse_channels('t.txt')
df.to_csv('channels.csv', index=False)
print('End Time:', datetime.now())

def get_channels(fileName):
    channels = set()
    with open(fileName, 'r') as f:
        for l in f.readlines():
            l = l.replace('\n','')
            channels.add(l)
    return channels
fav_channels = get_channels('channels.txt')

def add_line(text):
    try:
        file = open('channels.m3u', "a")
        file.write(text)             
        file.close()
    except:
        add_line(text)
        
def fill_channels_file(channels_urls: pd.DataFrame):
    add_line('#EXTM3U\n')
    for _, row in channels_urls.iterrows():
        name = row.iloc[0]
        if name in fav_channels:
            url = row.iloc[1]
            line1 = f'#EXTINF:-1 tvg-id="{name}",{name}'
            line2 = url
            add_line(line1 + '\n' + line2 + '\n')
    
fill_channels_file(df)