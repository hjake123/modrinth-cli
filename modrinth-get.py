import requests
import json
import urllib
import sys

def choose_primary_file(version):
    for file in version['files']:
        if file['primary']:
            return file
    return version['files'][0]

headers = {'User-Agent': 'hyperlynx/modrinth-cli (hjake123@gmail.com)'}

slug = sys.argv[1]
game_version_specified = False
if len(sys.argv) > 2:
    game_version = sys.argv[2]
    game_version_specified = True

responce = requests.get('https://api.modrinth.com/v2/project/' + slug + '/version', headers=headers).content
object = json.loads(responce.decode('utf-8'))

for version in object:
    if not game_version_specified or game_version in version['game_versions'] :
        urllib.request.urlretrieve(choose_primary_file(version)['url'], choose_primary_file(version)['filename'])
        break