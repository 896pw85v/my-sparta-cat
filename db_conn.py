import psycopg2
import uuid

# I have no idea there is a psycopg3
# Every connection creates a new connection object 
# because service might die at anytime
# TODO: this wastes time and network, need better pattern or another deployment

# pg Admin
# py -> pg, then do logging in

def create_conn(): 
    return psycopg2.connect(database="postgres", 
                        user="kitty",
                        password="P@ssw0rd",
                        host="localhost",
                        port="5432")

def sign_user(user: dict):
    """Sign in user by checking if the corresponding row exists. 
    Return `True` on success, `Fail` on else. """
    # no commit/rollback since only select
    if user['u-name'] == "" or user['password'] == '': 
        return False
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET search_path = sparta_cat')
    cur.execute('SELECT user_name FROM users WHERE user_name = %s AND pass_hash = %s', (user['u-name'], user['password']))
    matched_users: list = cur.fetchall()
    print('users that matched: ', matched_users)
    if len(matched_users) == 0: 
        conn.close()
        return None
    elif len(matched_users) > 1: 
        print(matched_users)
        conn.close()
        raise Exception('user conflict/clash. (this is probably a db issue)')
    else: 
        # user verified, shouldn't have fk violation
        new_sid = new_session(cur, user['u-name'])
        conn.commit()
        conn.close()
        print(new_sid)
        return new_sid
    

def create_account(user_name: str, pass_hash: str): 
    """
    adds user information to database. """
    print(user_name, pass_hash)
    sql = """INSERT INTO users (user_name, pass_hash) VALUES (%s, %s);"""
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET search_path = sparta_cat;')
    try:
        cur.execute(sql, (user_name, pass_hash))
        sid = new_session(cur, user_name)
        conn.commit()
        conn.close()
        return sid
    except psycopg2.errors.UniqueViolation:
        print("Unique violation haha for: ", user_name)
        conn.rollback()
        conn.close()
        return None

def find_and_renew_session(sid: uuid.UUID): 
    """
    Find existing, unexpired session id, returns user name if success. """
    print(sid)
    sid = str(sid)
    # psycopg2.extras.register_uuid()
    # sid = psycopg2.extensions.adapt(sid)#.getquoted()
    # sid = psycopg2.extras.UUID_adapter(sid)
    print(sid, type(sid))
    sql = """SELECT user_name FROM sessions WHERE sid = %s::UUID AND expire_by > CURRENT_DATE;"""
    try: 
        conn = create_conn()
        cur = conn.cursor()
        cur.execute('SET search_path = sparta_cat;')
        cur.execute(sql, (sid,))
        user_name = cur.fetchone()
        print(user_name)
        # here renews expire date. Maybe generate a new one for security
        if user_name: 
            renew = """UPDATE sessions SET expire_by = CURRENT_DATE + 30 WHERE user_name = %s;"""
            cur.execute(renew, (user_name,))
            conn.commit()
            conn.close()
            return user_name[0]
        # None, no valid session
        conn.close()
        return user_name
    except: 
        print(cur.fetchone())
        conn.rollback()
        conn.close()
        return None # sounds good
    
def new_session(cur, uname: str): 
    """
    This function should be used with other functions, therefore expects a prepared cursor. 
    In addition, this function does not handle transaction, any exception will be raised. 
    Return new sid, either brand new or renewed. """
    print(type(cur))
    sql = """SELECT expire_by > current_date, expire_by FROM sessions WHERE user_name = %s;"""
    cur.execute(sql, (uname,)) # i dont think expire_by is needed
    res = cur.fetchone()
    print(res)
    if res and res[0]: 
        # user exists and not expired
        # if res[0]: 
            # not expired
        update = """update sessions set sid = gen_random_uuid(), expire_by = current_date + 30 where user_name = %s RETURNING sid;"""
        cur.execute(update, (uname,))
        new_sid = cur.fetchone()[0]
        print("Generated new sid", new_sid, " for ", uname)
        return new_sid
    else: 
        # new user or expired session
        insert = """insert into sessions (user_name) values (%s) RETURNING sid; """
        cur.execute(insert, (uname,)) # uuid collide? 
        sid = cur.fetchone()
        print(sid)
        return sid[0]

def write_into(mbid: str, user_name: str, content: str, rating: int) -> bool: 
    """
    Here should do validation again!!!!!!!!!!!!!
    Write or update a user's review and rating. 
    Return a `bool` indicating completion. """
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET search_path = sparta_cat')
    sql = """INSERT INTO song_rating AS ss (song_mbid, user_name, review, rating) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (song_mbid, user_name) DO UPDATE 
    SET review = (%s), rating = (%s) 
    WHERE ss.song_mbid = %s AND ss.user_name = %s;"""
    try:
        # insert. insert don't return anything, therefore can't know result 
        cur.execute(sql, (mbid, user_name, content, rating, content, rating, mbid, user_name))
    except: 
        conn.rollback()
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

def read_review(user_name: str, mbid: uuid.UUID = None, limit: int = 10, offset: int = 0): 
    """Fetch this user's rating/reviews on this song, or all of his reviews. 
    Return text/json. """
    # my brain is a mesh now im js doing whatever comes in mind
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET SEARCH_PATH TO sparta_cat;')
    if not user_name: 
        # empty string 
        return None
    if not "valid session": 
        return None # js means - idk how to do thissssss
    sql = """?"""
    if not mbid: 
        sql = """SELECT song_mbid, rating, review FROM song_rating 
                WHERE user_name = %s
                ORDER BY last_updated
                LIMIT %s
                OFFSET %s;"""
        cur.execute(sql, (user_name, limit, offset))
        res = cur.fetchall() # should be <= 10 entries
        print(res)
        conn.close()
        return res
    else: 
        sql = """SELECT song_mbid, rating, review FROM song_rating 
                WHERE song_mbid = %s::uuid AND user_name = %s
                ORDER BY last_updated
                LIMIT %s
                OFFSET %s;"""
        cur.execute(sql, (str(mbid), user_name, limit, offset))
        res = cur.fetchall()
        print(res)
        conn.close()
        return res
        

