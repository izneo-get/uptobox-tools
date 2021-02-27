# uptobox-tools

## uptobox_files.py
Permet d'avoir la liste des fichiers de son compte UpToBox.com, triés par date de dernier téléchargement croissante. 

### Utilisation
```
usage: uptobox_files.py [-h] [--token TOKEN] [--fields FIELDS]
                        [--sort {name,created,size,downloads,last_download,folder}] [--find-missing REFERENCE_FILE]
                        [--output OUTPUT]
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
  --find-missing REFERENCE_FILE
                        Find missing distant files compared to a reference list of files.
  --output OUTPUT_FILE, -o OUTPUT_FILE
                        Output to a file.
```

L'option `--token` (optionnelle) permet de préciser le token d'API du compte UpToBox. 
Si le token n'est pas renseigné, il est lu du fichier de config `uptobox_files.cfg`. 
Si le token n'est pas disponible dans ce fichier de config, il est demandé et sera sauvegardé dans `uptobox_files.cfg`. 

L'option `--fields` (optionnelle) permet de donner la liste des champs que l'on souhaite voir en sortie. Ils doivent être séparés par une virgule, sans espace. 
Les champs disponibles sont : `name`, `created`, `size`, `downloads`, `last_download`, `folder`, `url`.
Si l'option n'est pas renseignée, les champs utilisés seront : `"last_download,url,folder,name"` 

L'option `--sort` (optionnelle) permet de définir dans quel ordre les fichiers doivent être triés. 
La valeur doit être parmi : `name`, `created`, `size`, `downloads`, `last_download`, `folder`. 
Si l'option n'est pas renseignée, le champ utilisé sera : `last_download` (les fichiers dont la date de dernier téléchargement est la plus ancienne seront affichés en premier). 

L'option `--find-missing` (optionnelle) permet de prendre en entrée un fichier contenant une liste de noms de fichiers. Le script listera tous les fichiers de cette liste qui ne sont pas présents sur le compte UpToBox dans les répertoires requêtés. 
Le fichier peut soit être une liste simple de noms, soit une liste générée avec l'option `--output OUTPUT_FILE`. 
Cette option est incompatible avec les options `--fields` et `--sort`. 

L'option `--output` (optionnelle) permet d'enregistrer le résultat dans un fichier, au lieu de la sortie standard. 



#### Exemples 
##### Lister les fichiers à la racine du compte : 
```
python uptobox_files.py
```
qui est l'équivalent de 
```
python uptobox_files.py --fields "last_download,url,folder,name" --sort "last_download" //
```

##### Enregistrer uniquement les noms des fichiers des répertoires "Folder 1" et "Folder 2" dans un fichier "out.txt" : 
```
python uptobox_files.py --fields "name" --sort "name" --output "out.txt" "//Folder 1" "//Folder 2"
```

##### Trouver les fichiers qui sont sur un compte A mais pas sur un compte B : 
```
python uptobox_files.py --token TOKEN_DU_COMPTE_A --output "compte_A.txt" "//"
python uptobox_files.py --token TOKEN_DU_COMPTE_B --find-missing "compte_A.txt" "//"
```
Le script va d'abord interroger le compte A pour connaitre la liste des fichiers présents à la racine. Le résultat sera écrit dans le fichier `compte_A.txt`. 
Le script va ensuite interroger le compte B. Tous les fichiers listés dans A qui ne sont pas à la racine de B seront alors affichés. 

