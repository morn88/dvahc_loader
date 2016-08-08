import urllib.parse
import urllib.request
import re
import os
import tqdm
import sys


def check_folder():
    folder = 'done_webm'
    try:
        os.mkdir(folder)
        print('Папка созданна')
    except FileExistsError:
        print('Папка готова')


def connect(url):
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        respData = resp.read()

        with open('links.txt', 'w') as saveFile:
            saveFile.write(str(respData))
        return 'OK'

    except Exception as e:
        print(str(e))
        return str(e)


def download(url):
    url = url[0:-5].replace('res', 'src') + '/'
    url_path = url.split('/')

    with open('links.txt') as file:
        string = file.read()

    match = r'href="(.*?)"'
    need = re.findall(match, string)
    st_list = []
    for st in need:
        if st.endswith('.webm'):
            st = st.replace('..', '/'.join(url_path[0:-3]))
            st_list.append(st)

    st_set = set(st_list)
    file_list = os.listdir('./done_webm')
    done_list = [url + i for i in file_list]

    done_set = set(done_list)
    downl_set = st_set.difference(done_set)
    if len(downl_set) != 0:
        return downl_set
        os.chdir('./done_webm')
        for i in tqdm.tqdm(downl_set):
            fileName = i.split('/')
            urllib.request.urlretrieve(i, fileName[-1])
    else:
        print('Нет новых файлов')
if __name__ == '__main__':

    check_folder()

    if len(sys.argv) > 1:
        url = sys.argv[1]
        connect(url)
        download(url)
    else:
        print('Укажите ссылку на тред')
