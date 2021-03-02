# -*- coding: utf-8 -*-
__version__ = "02.05"

"""
Source : https://github.com/izneo-get/uptobox-tools
"""

import configparser
import argparse
import re
import sys
import os
from uptobox_class import UpToBox
import csv
import requests


def check_version():
    latest_version_url = 'https://raw.githubusercontent.com/izneo-get/uptobox-tools/master/VERSION'
    res = requests.get(latest_version_url)
    if res.status_code != 200:
        print(f"Version {__version__} (impossible to check official version)")
    else:
        latest_version = res.text.strip()
        if latest_version == __version__:
            print(f"Version {__version__} (official version)")
        else:
            print(f"Version {__version__} (official version is different: {latest_version})")
            print("Please check https://github.com/izneo-get/uptobox-tools/releases/latest")
    print()


if __name__ == "__main__":
    check_version()

    # Parse des arguments passés en ligne de commande.
    parser = argparse.ArgumentParser(
        description="""Script to list files in your UpToBox account."""
    )
    parser.add_argument(
        "folders",
        type=str,
        metavar='FOLDER', 
        nargs='*',
        default=["//"],
        help="Folders(s) to explore (default=\"//\").",
    )
    parser.add_argument(
        "--token", "-t", type=str, default="", help="API token."
    )
    parser.add_argument(
        "--fields", "-f", type=str, default="", help="Fields to display separated by coma without spaces (available: 'name', 'created', 'size', 'downloads', 'last_download', 'folder', 'url') (default=\"last_download,url,folder,name\")."
    )
    parser.add_argument(
        "--sort", "-s", type=str, choices=['name', 'created', 'size', 'downloads', 'last_download', 'folder'], default="", help="Sort list by... (default=\"last_download\")"
    )
    parser.add_argument(
        "--recursive", "-r", default=False, action="store_true", help="Explore folders recursively."
    )
    parser.add_argument(
        "--find-missing", "-m", type=str, metavar="REFERENCE_FILE", default="", help="Find missing distant files compared to a reference list of files."
    )
    parser.add_argument(
        "--output", "-o", type=str, metavar="OUTPUT_FILE", default="", help="Output to a file."
    )

    args = parser.parse_args()
    

    folders = ['//' + str(f) if f[0:2] != '//' else f for f in args.folders]
    token = args.token
    sort_by = args.sort
    fields_to_display = args.fields
    recursive = args.recursive
    find_missing = args.find_missing
    output_file = args.output

    if not token:
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
            utb = UpToBox(token)
            user = utb.uptobox_user()
            if user['statusCode'] == 0:
                # Ecriture de la config.
                config["DEFAULT"]["token"] = token
                with open(config_file, "w") as configfile:
                    config.write(configfile)

    utb = UpToBox(token)
    user = utb.uptobox_user()
    if user['statusCode'] != 0:
        print("[ERROR] Invalid token.")
        sys.exit()

    # Find-missing
    files_to_search = {}
    if find_missing:
        if fields_to_display:
            print("[WARNING] While \"--find-missing\", \"--fields\" will be ignored...")
        if sort_by:
            print("[WARNING] While \"--find-missing\", \"--sort\" will be ignored...")
        if not os.path.isfile(find_missing):
            print(f"[ERROR] File \"{find_missing}\" doesn't exist.")
            sys.exit()
        input_file = csv.DictReader(open(find_missing, "r", encoding="utf-8"), delimiter='\t')
        if 'file_name' in input_file.fieldnames:
            # Fichier au format attendu.
            for line in input_file:
                files_to_search[line['file_name']] = line
        else:
            # Fichier plat.
            files_to_search = {l: l for l in list(map(lambda s: s.strip(), open(find_missing, "r", encoding="utf-8").readlines()))}

        if not files_to_search:
            print("[ERROR] Can't find a list of file names in \"{find_missing}\"...")
            sys.exit()


    # Default values
    if not fields_to_display:
        fields_to_display = "last_download,url,folder,name"
    if not sort_by:
        sort_by = "last_download"
    
    # Récupération de la liste des fichiers.
    all_files = {}
    all_names = []
    for f in folders:
        files = utb.uptobox_files(path=f, recursive=recursive)
        all_files.update(files)
        for file in files:
            all_names.append(files[file]['file_name'])
    
    fo = None
    if output_file:
        fo = open(output_file, "w", encoding="utf-8")

    if files_to_search:
        # On veut juste voir les fichiers qui manquent.
        missing = list(set(files_to_search) - set(all_names))
        print("Missing files:", file=fo)
        if len(missing) > 0 and 'file_name' in input_file.fieldnames:
            print("\t".join(input_file.fieldnames), file=fo)
        for m in missing:
            line = m
            if 'file_name' in input_file.fieldnames:
                line = "\t".join([files_to_search[m][k] for k in input_file.fieldnames])
            print(line, file=fo)
        print(f"Total: {len(missing)}", file=fo)
        sys.exit()

    if not all_files:
        sys.exit()

    header = "\t".join(['file_' + fld.strip() for fld in fields_to_display.split(',')])

    
    print(header, file=fo)
    for _, f in sorted(all_files.items(), key=lambda item: item[1]['file_' + sort_by]):
        to_display = "\t".join([str(f['file_' + fld.strip()]) for fld in fields_to_display.split(',')])
        print(to_display, file=fo)

    if output_file:
        fo.close()
    else:
        print(f"{len(all_files)} elements")
