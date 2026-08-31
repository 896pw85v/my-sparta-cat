"""
Note on musicbrainz: 
SEARCH matches anything related to the provided string, have to restrict with Luscene 
LOOKUP returns detailed info about a singular entity, and 25< of related info. Must have ?inc=
BROWSE searches related entities with a MBID. page offset by returned amounts

The DB is fk broken the columns doesn't align. Only good thing is not require account
"""

import requests
import json
# artist = input('Search for artist: ')
respond = requests.get('https://musicbrainz.org/ws/2/artist/?query=artist:"The Weeknd"&fmt=json')

answer = json.loads(respond.text)['artists']

def get_response(url: str):
    """
    Returns a parsed json object from the url query\n
    Only work with json"""
    response = requests.get(url)
    return json.loads(response.text)

# exit()
count = 0
for artist in answer: 
    count = count + 1
    print(count, artist['name']), f'({artist['type']})'

num = 1 # int(input(f'Select the artist you want (1-{count}): '))

mbid = answer[num - 1]['id']
# print(answer[num - 1]['id'])
# print(len(answer[num - 1]['id']))

song = 'after hour'

respond = get_response(f'https://musicbrainz.org/ws/2/recording/?query={song} AND arid:{mbid}&fmt=json&offset=0')
print(respond['recordings'][0])
for rec in respond['recordings']:
    print(rec['title'])
