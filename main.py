import uuid
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import mb_lib
import db_conn
app = FastAPI()

sessions: dict[str, str] = {} # sid -> u-name
# this can change to smth like sqlite/redis

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

@app.get('/styles.css')
def give_css():
    return FileResponse('./web/styles.css')

@app.get('/scripts.js')
def give_js(): 
    return FileResponse('./web/scripts.js')

@app.get('/btools.js')
def give_tools(): 
    return FileResponse('./web/btools.js')

@app.get('/write-review')
def give_write(): 
    return FileResponse('./web/write.html')

@app.get('/write.js')
def give_write_js(): 
    return FileResponse('./web/write.js')


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

@app.post("/log-in")
def log_in(cre: dict, res: Response, req: Request):
    print(sessions)
    print(cre)
    sid_from_cookie = req.cookies.get('spc-sid', '')
    if sid_from_cookie: 
        # cookie contains sid
        sid = uuid.UUID(sid_from_cookie)
        print(sid)
        if sid in sessions:
            print('in')
            return {'success': True, 'name': sessions[sid]}
        # else: 
            # valid uuid, but not in sessions
            # 1. server fresh started
            # 2. fake sid
            # In both cases js try a normal log-in
    # else do new log-in
    try: 
        if db_conn.sign_user(cre):
            # do session id token thing
            sid: str = uuid.uuid4() # idk how uuid work
            sessions[sid] = cre['u-name']
            res.set_cookie(key='spc-sid', value=sid, httponly=True, max_age=60*60*24, samesite='lax', secure=True)
            return {'success': True, 'name': cre['u-name']}
        else:#return smth so html updates
            return {'success': False}
    except:
        return {'success': False}
# create new acountttttttttttttttttttttttttttttttttt

@app.post('/write')
def write_review(review: dict, req: Request) -> bool: 
    print(review)
    """write review into db. Returns `bool` indicating success. Recommend keeping a copy local. """
    mbid: str = review['mbid']
    uid: str = req.cookies.get('spc-sid')
    if uid is None: 
        return False
    else: 
        uid = uuid.UUID(uid)
        if  uid not in sessions: 
            return False
        uid = sessions[uid]
    content: str = review['content']
    if len(content) > 1000: 
        return False
    rating: int = review['rating']
    if rating > 5 or rating < 0: 
        return False
    return db_conn.write_into(mbid, uid, content, rating)
