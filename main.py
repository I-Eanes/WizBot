from fastapi import FastAPI
import sqlite3

# SQLITE Db Connection Stuff
con = sqlite3.connect("Data/WizBase.db", isolation_level=None)
cur = con.cursor()

# FASTAPI Initialization Stuff
app = FastAPI()

# Root of API
@app.get("/")
async def root():
    return {"message" : "WELCOME TO WIZAPI"}

# Spell Calls for the API
@app.get("/spells")
async def spells():
    results = cur.execute(f"SELECT * FROM Spells;")
    return results.fetchall()

@app.get("/spells/{spell_id}")
async def spells(spell_id):
    results = cur.execute(f"SELECT * FROM Spells WHERE spellID = {spell_id};")
    return results.fetchall()

@app.get("/user/{user_id}")
async def user(user_id):
    results = cur.execute(f"SELECT * FROM users WHERE ID = '{user_id}';")
    return results.fetchall()

@app.post("/user/new/{user_id}")
async def user(user_id):
    cur.execute(f"INSERT INTO users (ID) VALUES ({user_id});")

@app.patch("/user/lvl/{user_id}")
async def user(user_id):
    cur.execute(f"UPDATE Users SET (LVL = LVL + 1) WHERE ID = {user_id};")

@app.patch("/user/spells/{user_id}/{slot}/{spell}")
async def user(user_id, slot, spell):
    cur.execute("UPDATE Users SET ({slot} = {spell}) WHERE ID = {user_id};")

