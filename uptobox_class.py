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

    def uptobox_files(self, path="//"):
        page_size = 100
        page = 0

        all_files = []
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
                all_files.append(f)

            there_is_more = len(res["data"]["files"]) == page_size
            page += 1

        return all_files