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
    if artist == '': 
        # just search song
        
        mb_lib.get_songs_same_name(song)
    if song == '': 
        # just search artist
        res: dict = {}
        # should pass a name instead
        res = mb_lib.get_artist_album_covers(artist)
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







































@app.get('/styles.css')
def give_css():
    return FileResponse('./web/styles.css')

@app.get('/scripts.js')
def give_js(): 
    return FileResponse('./web/scripts.js')

@app.get('/btools.js')
def give_tools(): 
    return FileResponse('./web/btools.js')