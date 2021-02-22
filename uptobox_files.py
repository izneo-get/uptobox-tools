# -*- coding: utf-8 -*-
__version__ = "0.01.01"


import requests
import json
import configparser
import re
import sys
import os

base_url = 'https://uptobox.com/'

def uptobox_files(path='//'):
    url = f'https://uptobox.com/api/user/files'

    page_size = 100
    page = 0

    all_files = []

    there_is_more = True

    while there_is_more:
        params = {
            'token': token,
            'path': path,
            'limit': page_size,
            'offset': page * page_size,
            # 'orderBy': '',
            # 'dir': 'DESC'
        }

        response = requests.get(
            url,
            params=params,
        )

        res = json.loads(response.text)

        if res['statusCode'] == 1:
            print(f"[ERROR] {res['message']}: {res['data']}")
            return

        for f in res['data']['files']:
            all_files.append(f)

        there_is_more = len(res['data']['files']) == page_size
        page += 1

    return all_files


if __name__ == "__main__":
    root_dir = "//"
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
        if root_dir[0:2] != '//':
            root_dir = '//' + root_dir


    token = ''
    # Lecture de la config.
    config = configparser.RawConfigParser()
    config_file = re.sub(r"\.py$", ".cfg", os.path.abspath(sys.argv[0]))
    config_file = re.sub(r"\.exe$", ".cfg", config_file)
    if os.path.isfile(config_file):
        config.read(config_file, encoding="utf-8")
        token = config.get(
            "DEFAULT", "token", fallback=token
        )
    if not token:
        token = input("Uptobox token: ")

    # Ecriture de la config.
    config["DEFAULT"]["token"] = token
    with open(config_file, "w") as configfile:
        config.write(configfile)

    # Récupération de la liste des fichiers.
    files = uptobox_files(path=root_dir)
    if not files:
        sys.exit()
    files.sort(key=lambda x: x['file_last_download'])
    print(f"file_last_download\tfile_code\tfile_name")
    for f in files:
        print(f"{f['file_last_download']}\t{base_url}{f['file_code']}\t{f['file_name']}")
    print(f"{len(files)} elements")
