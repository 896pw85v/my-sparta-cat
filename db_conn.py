import psycopg2

# pg Admin
# py -> pg, then do logging in

conn = psycopg2.connect(database="postgres", 
                        user="kitty",
                        password="P@ssw0rd",
                        host="localhost",
                        port="5432")
cur = conn.cursor()
cur.execute('SET search_path = sparta_cat')

def sign_user(user: dict):
    # TODO: SQL injection
    if user['u-name'] == "" or user['password'] == '': 
        return False
    cur.execute('SELECT user_name FROM users WHERE user_name = %s AND  pass_hash = %s', (user['u-name'], user['password']))
    matched_users: list = cur.fetchall()
    print(matched_users)
    # query only no commit?
    if len(matched_users) == 0: 
        return False
    elif len(matched_users) > 1: 
        print(matched_users)
        raise Exception('user conflict/clash. (this is probably a db issue)')
    else: 
        return True
    
def write_into(mbid: str, uid: str, content: str, rating: int) -> bool: 
    """
    Here should do validation again!!!!!!!!!!!!!
    Write or update a user's review and rating. 
    Return a `bool` indicating completion. """
    sql = """INSERT INTO song_rating AS ss (song_mbid, user_id, review, rating) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (song_mbid, user_id) DO UPDATE 
    SET review = (%s), rating = (%s) 
    WHERE ss.song_mbid = %s AND ss.user_id = %s;"""
    try:
        # insert. insert don't return anything, therefore can't know result 
        cur.execute(sql, (mbid, uid, content, rating, content, rating, mbid, uid))
    except: 
        return False
    conn.commit()
    return True
# print(conn)
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM sparta_cat.users;')
# print('currente users')
# for each in cursor.fetchall():
#     print(each)

# sql = """INSERT INTO users (user_name) values ('I-am-the-first-user') ON CONFLICT (user_name) DO NOTHING"""
# cursor.execute(sql)
# print('current users')
# cursor.execute('SELECT * FROM sparta_cat.users;')
# print(cursor.fetchone())

# conn.commit()

# requests.get('https://musicbrainz.org/w/2/search/artists/?query=artists:"The Weekend"&fmt=json&limit=1')

# conn.close()