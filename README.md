# uptobox-tools

## uptobox_files.py
Permet d'avoir la liste des fichiers de son compte UpToBox.com, triés par date de dernier téléchargement croissante. 

### Utilisation
```
usage: uptobox_files.py [-h] [--token TOKEN] [--sort {name,created,size,downloads,last_download,folder}]
                        [--fields FIELDS] [--output OUTPUT]
                        [FOLDER ...]

Script to list files in your UpToBox account.

positional arguments:
  FOLDER                Folders(s) to explore (default="//").

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        API token.
  --fields FIELDS, -f FIELDS
                        Fields to display separated by coma without spaces (available: 'name', 'created', 'size',
                        'downloads', 'last_download', 'folder', 'url') (default="last_download,url,folder,name").
  --sort {name,created,size,downloads,last_download,folder}, -s {name,created,size,downloads,last_download,folder}
                        Sort list by... (default="last_download")
  --output OUTPUT, -o OUTPUT
                        Output to file.
```

Si le token n'est pas renseigné, il est lu du fichier de config `uptobox_files.cfg`. 
Si le token n'est pas disponible dans ce fichier de config, il est demandé et sera sauvegardé dans `uptobox_files.cfg`. 


#### Exemples 
##### Lister les fichiers à la racine : 
```
python uptobox_files.py
```
qui est l'équivalent de 
```
python uptobox_files.py --fields "last_download,url,folder,name" --sort "last_download" //
```

##### Enregistrer les noms des fichiers des répertoires "Folder 1" et "Folder 2" dans un fichier "out.txt" : 
```
python uptobox_files.py --fields "name" --sort "name" --output "out.txt" "//Folder 1" "//Folder 2"
```
