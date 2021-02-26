# -*- coding: utf-8 -*-
__version__ = "0.02.00"


import configparser
import argparse
import re
import sys
import os
from uptobox_class import UpToBox


if __name__ == "__main__":
    # Parse des arguments passés en ligne de commande.
    parser = argparse.ArgumentParser(
        description="""Script to list files in your UpToBox account."""
    )
    parser.add_argument(
        "folders",
        type=str,
        metavar='N', 
        nargs='*',
        default=["//"],
        help="Folders(s) to explore.",
    )
    parser.add_argument(
        "--token", "-t", type=str, default="", help="API token."
    )
    parser.add_argument(
        "--sort", "-s", type=str, choices=['name', 'created', 'size', 'downloads', 'last_download', 'folder'], default="last_download", help="Sort list by..."
    )
    parser.add_argument(
        "--fields", "-f", type=str, default="last_download,url,folder,name", help="Fields to display."
    )
    parser.add_argument(
        "--output", "-o", type=str, default="", help="Output to file."
    )

    args = parser.parse_args()
    

    folders = ['//' + str(f) if f[0:2] != '//' else f for f in args.folders]
    token = args.token
    sort_by = args.sort
    fields_to_display = args.fields
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
            # Ecriture de la config.
            config["DEFAULT"]["token"] = token
            with open(config_file, "w") as configfile:
                config.write(configfile)

    utb = UpToBox(token)

    # Récupération de la liste des fichiers.
    all_files = []
    for f in folders:
        files = utb.uptobox_files(path=f)
        for file in files:
            file['file_folder'] = f
            file['file_url'] = f"{utb.url_base}{file['file_code']}"
            all_files.append(file)

    if not all_files:
        sys.exit()
    all_files.sort(key=lambda x: x['file_' + sort_by])

    header = "\t".join(['file_' + fld.strip() for fld in fields_to_display.split(',')])

    fo = None
    if output_file:
        fo = open(output_file, "w")
    print(header, file=fo)
    for f in all_files:
        to_display = "\t".join([f['file_' + fld.strip()] for fld in fields_to_display.split(',')])
        print(to_display, file=fo)

    if output_file:
        fo.close()
    else:
        print(f"{len(all_files)} elements")
