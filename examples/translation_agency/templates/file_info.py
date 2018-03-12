import os

file_size = os.stat('./translate.html').st_size
with open('./file_info.txt', 'w+') as f:
    f.write(f'file size: {file_size}')
