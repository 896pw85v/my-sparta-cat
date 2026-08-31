import musicbrainzngs
import json
musicbrainzngs.set_useragent('learning to use mb', '0')
# res = musicbrainzngs.search_artists('the weeknd', limit=3)

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
releases = musicbrainzngs.browse_release_groups('c8b03190-306c-4120-bb0b-6f2ebfc06ea9', limit=10)
# dict_keys(['release-group-list', 'release-group-count'])
images = []
for each in releases['release-group-list']: 
    images.append(musicbrainzngs.get_release_group_image_list(each['id']))
"""
res > Song1 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song2 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song3...
"""

def get_images(): 
    return images
# fastapi packs objects into json
# for i in images: 
#     print(type(i))