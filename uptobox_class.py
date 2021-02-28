# -*- coding: utf-8 -*-
import requests
import json


class UpToBox:
    token: str = ""
    url_base = "https://uptobox.com/"
    url_files = "https://uptobox.com/api/user/files"
    url_user = "https://uptobox.com/api/user/me"

    def __init__(self, token: str):
        self.token = token

    def uptobox_user(self):
        params = {
            "token": self.token,
        }
        response = requests.get(
            self.url_user,
            params=params,
        )
        res = json.loads(response.text)
        return res


    def uptobox_files(self, path="//", recursive=False):
        page_size = 100
        page = 0

        all_files = {}
        all_folders = {}
        there_is_more = True
        while there_is_more:
            params = {
                "token": self.token,
                "path": path,
                "limit": page_size,
                "offset": page * page_size,
                # 'orderBy': '',
                # 'dir': 'DESC'
            }

            response = requests.get(
                self.url_files,
                params=params,
            )

            res = json.loads(response.text)

            if res["statusCode"] == 1:
                print(f"[ERROR] {path} {res['message']}: {res['data']}")
                return []

            for f in res["data"]["files"]:
                f['file_folder'] = path
                f['file_path'] = path + f['file_name']
                f['file_url'] = f"{self.url_base}{f['file_code']}"

                all_files[f['file_code']] = f

            for f in res["data"]["folders"]:
                all_folders[f['fullPath']] = f['fullPath']

            there_is_more = len(res["data"]["files"]) == page_size
            page += 1

        # Sort by filename.
        all_files = {k: v for k, v in sorted(all_files.items(), key=lambda item: item[1]['file_name'])}

        if recursive:
            for folder in all_folders:
                all_files.update(self.uptobox_files(folder, recursive=True))

        return all_files