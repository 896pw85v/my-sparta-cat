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

def sign_user(u_name: str):
    # TODO: SQL injection
    if u_name == "": 
        return False
    cur.execute('SELECT user_name FROM users WHERE user_name = %s', [u_name])
    matched_users: list = cur.fetchall()
    # query only no commit?
    if len(matched_users) == 0: 
        return False
    elif len(matched_users) > 1: 
        raise Exception('user conflict/clash')
    else: 
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