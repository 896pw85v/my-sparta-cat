import musicbrainzngs

musicbrainzngs.set_useragent('learning to use api', '0')
artist_album_cache: dict[str, dict] = {} # id -> list_of_album_covers
# returned: 
# artists -+ ...
#         |+ ...
#         |+ ...

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
    except: 
        print('hmm')
        print(res)
        return {}
    artists = res['artist-list']
    # return artists
    id_name = {}
    for artist in artists:
        id_name[artist['id']] = artist['name']
        # res = artist['name']
        # if 'disambiguation' in artist.keys(): 
        #     res +=  ' (' + artist['disambiguation'] + ')'
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
    if artist_id in artist_album_cache: 
        return artist_album_cache[artist_id]
    images = []
    releases = musicbrainzngs.browse_release_groups(artist_id, limit=10)
    # dict_keys(['release-group-list', 'release-group-count'])
    for release in releases['release-group-list']: 
        print(release['id'])
        try: 
            image: dict = musicbrainzngs.get_release_group_image_list(release['id'])
            image['title'] = release['title']
            images.append(image) # maybe just return a subset of api response
        except: 
            pass # or continue
    # cache to db
    artist_album_cache[artist_id] = images
    print(len(images))
    return images

"""
[x] front and back talks!!
[x] Third party api 
[ ] db to back
[ ] account
[ ] writing review
[ ] logged in with session and cookie
"""
# {'id': 'fc5ecd80-3961-4036-ae95-1e629428562f', 'type': 'Album', 'title': 'Greatest Hits', 'first-release-date': '2026-01-31', 'primary-type': 'Album'}
# the greatest hit. not gonna report cuz need account. keep here as a note for future