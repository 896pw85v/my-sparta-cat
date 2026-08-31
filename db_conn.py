import psycopg2
import requests

conn = psycopg2.connect(database="postgres", 
                        user="kitty",
                        password="P@ssw0rd",
                        host="localhost",
                        port="5432")

print(conn)
cursor = conn.cursor()
cursor.execute('SET search_path = sparta_cat')
cursor.execute('SELECT * FROM sparta_cat.users;')
print('currente users')
for each in cursor.fetchall():
    print(each)

sql = """INSERT INTO users (user_name) values ('I-am-the-first-user') ON CONFLICT (user_name) DO NOTHING"""
cursor.execute(sql)
print('current users')
cursor.execute('SELECT * FROM sparta_cat.users;')
print(cursor.fetchone())
conn.commit()

requests.get('https://musicbrainz.org/w/2/search/artists/?query=artists:"The Weekend"&fmt=json&limit=1')

conn.close()