import os
import shutil

def log_that_line(logWhat):
    try:
        file = open('github.csv', "a")  # Open the file in append mode
        file.write(logWhat)             # Write each item to the file
        file.close()
    except:
        log_that_line(logWhat)

# This function finds the last comma character index number within a text
def LastCommaPosition(text):
    CommaCount = text.count(',')
    RepNum = 0
    for i in range(CommaCount):
        RepNum = text.find(',', RepNum)
        RepNum += 1
    return RepNum - 1

x = 0
row_complete = True
channel_name = ''
channel_url = ''
channel_directory = 'streams'

log_that_line('channel_name,channel_url\n')
print('Collecting channels......')
for y, filename in enumerate(os.listdir(channel_directory)):
    f = os.path.join(channel_directory, filename)
    with open(f, 'r') as source_file:
        for i, line in enumerate(source_file):
            if line.find('#EXTM3U') != -1 or line.find('#EXTVLCOPT') != -1:
                continue
            elif line.find('tvg-id') != -1 and row_complete == True:
                line = line[LastCommaPosition(line) + 1:]
                channel_name = line.replace('\n', '')
                row_complete = False
            else:
                channel_url = line.replace('\n', '')
                row_complete = True
                channel_name = channel_name.replace(',','')
                channel_url = channel_url.replace(',','')
                log_that_line(f'"{channel_name}", "{channel_url}"'  + '\n')
    # print(filename)
    x += 1
print(x, 'files completed')



import pandas as pd
df = pd.read_csv('github.csv', sep=',')
df['channel_url'] = df['channel_url'].str.replace('"','')
df['channel_url'] = df['channel_url'].str.strip()
df['channel_name'] = df['channel_name'].str.replace('"','')

channels = set()
with open('channels.m3u','r') as live_channels:
    for i, channel in enumerate(live_channels.readlines()):
        if i % 2 != 0:
            channel = channel.replace('\n','')
            channel = channel[channel.find(',') + 1:]
            channels.add(channel)
live_channels.close()

new_channels_list = df[df['channel_name'].isin(channels)].sort_values(by='channel_name', ascending=True)

import os
os.remove('channels.m3u')

def log_that_line(logWhat):
    try:
        file = open('channels.m3u', "a")  # Open the file in append mode
        file.write(logWhat)               # Write each item to the file
        file.close()
    except:
        log_that_line(logWhat)

log_that_line('#EXTM3U\n')
for i, row in new_channels_list.iterrows():
    name = row.iloc[0]
    url = row.iloc[1]
    # print(f'{name},{url}')
    line1 = '#EXTINF:-1 tvg-id="",' + name
    line2 = url
    log_that_line(line1 + '\n' + line2 + '\n')

os.remove('github.csv')
shutil.rmtree('streams')
print('Channels urls updated!')