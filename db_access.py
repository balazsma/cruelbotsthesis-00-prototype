from pathlib import Path
import mysql.connector, json

db_config = json.loads(Path("db_config.json").read_text())

db = mysql.connector.connect(
    host = db_config["db_host"],
    user = db_config["db_user"],
    password = db_config["db_pass"],
    database = db_config["db_name"],
)
cur = db.cursor()

def get_url(num):
    sql = "SELECT url FROM urls WHERE id = %s;"
    cur.execute(sql, (num,))
    return cur.fetchall()[0]

def get_max():
    sql = "SELECT COUNT(url) FROM urls"
    cur.execute(sql)
    max = 0
    for row in cur.fetchall():
        max = row[0]
    return max
