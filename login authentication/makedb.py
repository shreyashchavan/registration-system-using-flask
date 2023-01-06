import sqlite3

conn = sqlite3.connect('mydatabase.db')

c = conn.cursor()

c.execute('''CREATE TABLE users (
    id  PRIMARY KEY autoincrement,
    fname text not null,
    lname text not null,
    date timestamp,
    is_active boolean default 0,
    email text not null,
    password text not null CHECK(LENGTH(password) >7)
);''')

conn.commit()
conn.close()