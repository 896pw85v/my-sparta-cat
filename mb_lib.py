import musicbrainzngs

musicbrainzngs.set_useragent('learning to use api', '0')
# res = musicbrainzngs.search_artists('the weeknd', limit=3)
artist_album_cache: dict = {}
# returned: 
# artists -+ ...
#         |+ ...
#         |+ ...

# artists = res['artist-list']
# for each in artists: 
#     res = each['name']
#     if 'disambiguation' in each.keys(): 
#         res +=  ' (' + each['disambiguation'] + ')'
#     print(res)

# twk: dict = artists[0]
# print(twk['id'])
# artist=twk['id']
# dict_keys(['release-group-list', 'release-group-count'])


"""
res > Song1 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song2 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song3...
"""

# should receive an id, called by another func
def get_artist_album_with_cover(artist_id: str): 
    print(artist_id)
    if artist_id in artist_album_cache: 
        return artist_album_cache[artist_id]
    images = []
    releases = musicbrainzngs.browse_release_groups(artist_id, limit=10)
    for release in releases['release-group-list']: 
        print(release['id'])
        try: 
            image: dict = musicbrainzngs.get_release_group_image_list(release['id'])
            image['title'] = release['title']
            images.append(image)
        except: 
            pass
        # cache to db
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