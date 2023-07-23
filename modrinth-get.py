import requests
import json
import urllib
import sys
import os
import zipfile

def choose_primary_file(version):
    for file in version['files']:
        if file['primary']:
            return file
    return version['files'][0]

def remove_existing_mod(slug):
    for file in os.listdir():
        if file.endswith('.jar'):
            modstoml = zipfile.ZipFile(file, mode='r').read("META-INF/mods.toml").decode('utf-8')
            if 'modId="'+slug+'"' in modstoml:
                print('Found existing mod with slug "'+slug+'", updating...')
                os.remove(file)

def get_modrinth_mod(slug, game_version, game_version_specified=False):
    headers = {'User-Agent': 'hyperlynx/modrinth-cli (discord: hyperlynx)'}
    responce = requests.get('https://api.modrinth.com/v2/project/' + slug + '/version', headers=headers).content
    object = json.loads(responce.decode('utf-8'))

    for version in object:
        if not game_version_specified or game_version in version['game_versions'] :
            if choose_primary_file(version)['filename'] in os.listdir():
                print('Already have latest version of mod "'+slug+'"')
                sys.exit(0)

            remove_existing_mod(slug)
            urllib.request.urlretrieve(choose_primary_file(version)['url'], choose_primary_file(version)['filename'])
            break

# Script start!
if len(sys.argv) == 1:
    print('Usage: python modrinth-get.py <slug> <game_version (optional)>\nOr: python modrinth-get.py -update <game_version>')
    sys.exit(1)

slug = sys.argv[1]
game_version_specified = False
if len(sys.argv) > 2:
    game_version = sys.argv[2]
    game_version_specified = True

if slug == '-update' or slug == '-u':
    if not game_version_specified:
        print('Usage: python modrinth-get.py -update <game_version>')
        sys.exit(1)
    for file in os.listdir():
        if file.endswith('.jar'):
            modstoml = zipfile.ZipFile(file, mode='r').read("META-INF/mods.toml").decode('utf-8')
            slug = modstoml.split('modId="')[1].split('"')[0]
            get_modrinth_mod(slug, game_version, True)
    sys.exit(0)

get_modrinth_mod(slug, game_version, game_version_specified)