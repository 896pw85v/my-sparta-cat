import uuid
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import mb_lib
import db_conn
app = FastAPI()

sessions: dict[str, str] = {} # sid -> u-name
# db stores a permanent copy with expiration time
# keep this one as a cache as well, memory cache + permanent storage

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
    
"""
log-in and sign-up take the same data and does the same thing except one 
tiny difference - the db part. May do a function"""

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
        else: 
            # valid uuid, but not in sessions
            # 1. server fresh started
            # 2. fake sid (what?)
            # find session in db 
            user_name = db_conn.find_and_renew_session(sid)
            if user_name: 
                # user session is valid
                res.set_cookie(key='spc-sid', value=sid, httponly=True, max_age=60*60*24, samesite='lax', secure=True)
                return {'success': True, 'name': user_name}
            else: 
                # session expires / simply doesn't exist
                # delete cookie, make user manually sign-in
                res.set_cookie(key='spc-sid', value=sid, httponly=True, max_age=0, samesite='lax', secure=True)
                return {'success': False}
    # else do new log-in
    try: 
        if not (cre['u-name'] and cre['password']): 
            return {'success': False}
        new_sid = db_conn.sign_user(cre)
        if new_sid:
            # do session id token thing
            # sid: str = uuid.uuid4() # idk how uuid work
            sessions[new_sid] = cre['u-name']
            res.set_cookie(key='spc-sid', value=new_sid, httponly=True, max_age=60*60*24, samesite='lax', secure=True)
            return {'success': True, 'name': cre['u-name']}
        else:#return smth so html updates
            return {'success': False}
    except:
        return {'success': False}
# create new acountttttttttttttttttttttttttttttttttt
@app.post('/sign-up')
def sign_up(user: dict, res: Response):
    if 'u-name' in user and 'password' in user: 
        uname = user['u-name']
        password = user['password']
    else: 
        print(user, 'bad user profile')
        return {'success': False}
    if not (uname or password): 
        return {'success': False}
    sid: uuid.UUID = db_conn.create_account(uname, password)
    if sid: 
        sessions[sid] = uname
        res.set_cookie(key='spc-sid', value=sid, httponly=True, max_age=60*60*24, samesite='lax', secure=True)
        return {'success': True, 'name': uname}
    else: 
        return {'success': False}

@app.post('/write')
def write_review(review: dict, req: Request) -> bool: 
    print(review)
    """write review into db. Returns `bool` indicating success. Recommend keeping a copy local. """
    mbid: str = review['mbid']
    sid: str = req.cookies.get('spc-sid')
    user_name = None
    if sid is None: 
        return False
    else: 
        user_name = db_conn.find_and_renew_session(sid)
        if  uuid.UUID(sid) not in sessions or user_name is None: 
            return False
    content: str = review['content']
    if len(content) > 1000: 
        return False
    rating: int = review['rating']
    if rating > 5 or rating < 0: 
        return False
    return db_conn.write_into(mbid, user_name, content, rating)
