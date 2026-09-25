from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import mb_lib
import db_conn
app = FastAPI()

sessions: dict[str, str] = {} # sid -> u-name

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers = ['*']
)

# index = Path('./web/index.html')
@app.get("/")
def read_root():
    # return {"Hello": "World"}
    return FileResponse('./web/index.html')


@app.post("/")
def search_for(body: dict):
    print(body) # artist: ... , song: ...
    artist: str = body['artist'] or 'the weeknd'
    song: str = body['song']
    if song == '': 
        # just search artist
        res: dict = {}
        # should pass a name instead
        res = mb_lib.get_artist_album_covers(artist)
        return res
    else: 
        res:list = mb_lib.get_songs_same_name(name=song, artist=artist)
        return res
    # maybe pack artist portrait as well
    return {}

import uuid
@app.post("/log-in")
def log_in(cre: dict, res: Response):
    print(cre)
    try: 
        if db_conn.sign_user(cre):
            # do session id token thing
            sid: str = uuid.uuid4() # idk how uuid work
            sessions[sid] = cre['u-name']
            res.set_cookie(key='sid', value=sid, httponly=True, max_age=60*60*24, samesite='lax', secure=True)
            return sid # This attempt to set a cookie via a Set-Cookie header was blocked due to user preference
        else:
            return ''
    except:
        return ''


@app.post('/write')
def write_review(review: dict) -> bool: 
    """write review into db. Returns `bool` indicating success. Recommend keeping a copy local. """
    mbid: str = review['mbid']
    uid: str = None # get id from token
    content: str = review['content']
    if len(content) > 1000: 
        return False
    rating: int = review['rating']
    if rating > 5 or rating < 0: 
        return False
    return db_conn.write_into(mbid, uid, content, rating)