import os

def get_file_lines(txtFile):
    with open(txtFile) as file:
        contents = file.readlines()
        contents.remove('#EXTM3U\n')
        return contents

def add_file_lines(target_file, file_contents):
    for line in file_contents:
        with open(target_file, 'a') as file:
            file.write(line)

def run():
    folder_name = 'streams'
    file_names = os.listdir(folder_name)

    for file_name in file_names:
        print(folder_name+'/'+file_name)
        contents = get_file_lines(folder_name+'/'+file_name)
        add_file_lines('channels.txt', contents)
    
if __name__ == '__main__':
    run()