from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mb_lib
import db_conn
app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers = ['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def search_for(body: dict):
    print(body) # artist: ... , song: ...
    artist: str = body['artist'] or 'the weeknd'
    song: str = body['song']
    # if artist == '': 
    #     pass
        # just search song
        # mb_lib.get_songs_same_name()
    if song == '': 
        # just search artist
        # should do at least three
        res: dict = {}
        # should pass a name instead
        res = mb_lib.get_artist_album_covers(artist)
        return res
    # maybe pack artist portrait as well
    return {}


@app.post("/log-in")
def log_in(cre: dict):
    print(cre)
    return db_conn.sign_user(cre['u-name'])


