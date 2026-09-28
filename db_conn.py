import psycopg2

# pg Admin
# py -> pg, then do logging in
# On every function, creates new connection and close 
# TODO: this wastes time and network, need better pattern

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
    cur.execute('SELECT user_name FROM users WHERE user_name = %s AND  pass_hash = %s', (user['u-name'], user['password']))
    matched_users: list = cur.fetchall()
    print('users that matched: ', matched_users)
    if len(matched_users) == 0: 
        conn.close()
        return False
    elif len(matched_users) > 1: 
        print(matched_users)
        conn.close()
        raise Exception('user conflict/clash. (this is probably a db issue)')
    else: 
        conn.close()
        return True
    
def write_into(mbid: str, uid: str, content: str, rating: int) -> bool: 
    """
    Here should do validation again!!!!!!!!!!!!!
    Write or update a user's review and rating. 
    Return a `bool` indicating completion. """
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET search_path = sparta_cat')
    sql = """INSERT INTO song_rating AS ss (song_mbid, user_id, review, rating) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (song_mbid, user_id) DO UPDATE 
    SET review = (%s), rating = (%s) 
    WHERE ss.song_mbid = %s AND ss.user_id = %s;"""
    try:
        # insert. insert don't return anything, therefore can't know result 
        cur.execute(sql, (mbid, uid, content, rating, content, rating, mbid, uid))
    except: 
        conn.rollback()
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

def create_account(user_name: str, pass_hash: str): 
    """
    adds user information to database. """
    sql = """INSERT INTO users (user_name, pass_hash) VALUES (%s, %s);"""
    conn = create_conn()
    cur = conn.cursor()
    cur.execute('SET search_path = sparta_cat')
    try:
        cur.execute(sql, (user_name, pass_hash))
        conn.commit()
        conn.close()
        return True
    except psycopg2.errors.UniqueViolation:
        print("Unique violation haha for: ", user_name)
        conn.rollback()
        conn.close()
        return False
