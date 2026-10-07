import musicbrainzngs

musicbrainzngs.set_useragent('learning to use api', '0')
# artist_album_cache: dict[str, dict] = {} # id -> list_of_album_covers
# this cache is not in use for now
def get_artist_album_covers(name: str) -> dict[str, list]: 
    """{artist_name -> list_of_covers}"""
    artist_cover = {}
    artists: dict = search_artists(name)
    print(type(artists))
    for id, name in artists.items(): 
        artist_cover[name] = fetch_artist_album_with_cover(id)
    return artist_cover

def search_artists(name = 'the weeknd') -> dict[str, str]:
    """receive a name, return a `dict` of {id: name} of matched artists"""
    res = {}
    print('name: ',name)
    try: 
        res = musicbrainzngs.search_artists(name, limit=1)
        # returned: 
        # artist-list -+ ...
        #         |+ ...
        #         |+ ...
    except: 
        print('hmm... Failed to search artist - ', name)
        print(res)
        return {}
    artists = res['artist-list']
    # return artists
    id_name = {}
    for artist in artists:
        res = artist['name']
        if 'disambiguation' in artist.keys(): 
            res +=  ' (' + artist['disambiguation'] + ')'
        id_name[artist['id']] = res
        # print(res)
    return id_name


"""
res > Song1 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song2 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song3...
"""

# should receive an id, called by another func
def fetch_artist_album_with_cover(artist_id: str) -> list[dict]: 
    print(artist_id)
    # if artist_id in artist_album_cache: 
    #     return artist_album_cache[artist_id]
    images = []
    releases = musicbrainzngs.browse_release_groups(artist_id, limit=10)
    # dict_keys(['release-group-list', 'release-group-count'])
    for release in releases['release-group-list']: 
        print(release['id'])
        try: 
            image: dict = musicbrainzngs.get_release_group_image_list(release['id'])
            image['title'] = release['title']
            images.append(image) # maybe just return a subset of api response
            # try do same site by sending html pages from back end
        except: 
            continue
    # cache to db
    # artist_album_cache[artist_id] = images
    print(len(images))
    return images

def get_songs_same_name(name: str, artist: str, offset: int = 0) -> list[dict]:
    """Must have song `name` and artist. Return list of `dict`s containing: 
    title, id, artist-credit-phrase, and images (list)""" 
    # I can't imagine how this would throw error, nor what to do if it did
    res: dict = musicbrainzngs.search_recordings(recording=name, limit = 10, offset=offset, artist=artist) # recording aka songs?
    # print(res.keys())
    rec_list = res['recording-list']
    songs: list = []
    phrases = []
    for recording in rec_list:
        try: 
            song: dict = {}
            song['title'] = recording['title']
            song['id'] = recording['id']
            song['artist-credit-phrase'] = recording['artist-credit-phrase']
            images = musicbrainzngs.get_release_group_image_list(recording['release-list'][0]['release-group']['id']) # hard coded yes
            song['images'] = images['images']
            songs.append(song)
            phrases.append(recording['artist-credit-phrase'])
        except: 
            continue
    return songs
"""
list: 
    {
    id -> id string, 
    title -> title string
    artist-credit-phrase -> artist-credit-phrase (artists), 
    images -> [{
        thumbnails -> {
            size -> url, 
            ..., 
            ...
            }
        },
        ...
        ]
    },
    ...
"""

"""
[x] front and back talks!!
[x] Third party api 
[x] db to back
[x] account
[x] writing review
[x] logged in with session and cookie
[x] create new account
[ ] https (live server, SSL...), hashing password
[ ] public access to db (get rid of local)
[x] displaying my reviews
[ ] improve search by weighing popular artists
[ ] small local storage
[ ] dark mode
[ ] multi lang? (these are mostly frontend stuff)
[ ] better js
[ ] OR, rebuild with more modern stack first
"""
# {'id': 'fc5ecd80-3961-4036-ae95-1e629428562f', 'type': 'Album', 'title': 'Greatest Hits', 'first-release-date': '2026-01-31', 'primary-type': 'Album'}
# the greatest hit. not gonna report cuz need account. keep here as a note for future

