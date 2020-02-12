# 036. sqlite3
#
# In-process SQL. Placeholders, joins, and Row factory.
#
# Run: python 036_sqlite3/main.py

# --- sqlite3 ---
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("create table users (id integer, name text)")
con.execute("insert into users values (?, ?)", (1, "Ada"))
row = con.execute("select name from users where id = ?", (1,)).fetchone()
print(row[0])
con.close()

# --- sqlite join ---
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
con.executescript("""
create table t (id integer, name text);
create table u (user_id integer, city text);
insert into t values (1, 'Ada');
insert into u values (1, 'London');
""")
row = con.execute("select t.name, u.city from t join u on t.id = u.user_id").fetchone()
print(row["name"], row["city"])
