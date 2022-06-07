"""fast api routing tool for api"""
from re import L
from unicodedata import name
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
#from db_queries import *


import psycopg2
import dotenv
import os

CONNECTION = None
CURSOR = None
def init_database():
    dotenv.load_dotenv()
    global CONNECTION
    global CURSOR
    #CONNECTION = psycopg2.connect(host=os.getenv("HOST"),port=5432,user=os.getenv("USERNAME"),dbname="postgres",password=os.getenv("PASSWORD"),sslmode="require")
    CONNECTION = psycopg2.connect(host="side-scroller-server.postgres.database.azure.com",port=5432,user="gcbui",dbname="postgres",password="GBDiddy111",sslmode="require")
    print("connection established")
    print("connection established")
    CURSOR=CONNECTION.cursor()

def get_leaderboard():
    try:
        CURSOR.execute(
            f"""
            select *
            from leaderboard
            """
        )
        results = CURSOR.fetchall()
        return results
    except:
        return "Failed to connect"

def write_leaderboard(name:str,enemies_killed:int,time_completed:int):
    try:
        CURSOR.execute(
            f"""
            insert into leaderboard(name,enemies_killed,time_completed)
            values(
                '{name}','{enemies_killed}','{time_completed}'
            );
            """
        )
        CONNECTION.commit()
        return "Wrote to db succesfully"
    except Exception as ex:
        return "Failed to wrtie to db" + str(ex)


LEADERBOARD = []

class LeaderboardUpdateRequest(BaseModel):
    name:str
    enemies_killed:int
    time_completed:int

    '''def __init__(self,name,enemies_killed,time_completed):
        self.name = name
        self.enemies_killed = enemies_killed
        self.time_completed = time_completed'''

    def __repr__(self) -> str:
        return "NAME: " +self.name + " ENEMIES KILLED: " + str(self.enemies_killed) + " TIME COMPLETE: " + str(self.time_completed)

    def __str__(self) -> str:
        return "NAME: " +self.name + " ENEMIES KILLED: " + str(self.enemies_killed) + " TIME COMPLETE: " + str(self.time_completed)

def convert_leaderboard_to_string():
    leaderboard_str = ""
    print("ENTERED FUNC")
    for leaderboard_entry in LEADERBOARD:
        leaderboard_str += "<p>" + str(leaderboard_entry) + "</p>"
        print(leaderboard_str+"ENTERED HERE")
    return leaderboard_str

init_database()
app = FastAPI()


@app.get("/")
async def root():
    """home page"""
    return {"message": "Welcome to Side Scroller Server"}


@app.get("/leaderboard",response_class=HTMLResponse)
async def leaderboard():
    """home page"""
    #leaderboard_data = get_leaderboard()
    #leaderboard_table = LeaderboardUpdateRequest()
    converted_html = '''<!DOCTYPE html>
    
    <html>
    <body>

    <h2 title="LEADERBOARD">LEADERBOARD</h2>

    <p title="I'm a tooltip">HERE ARE THE STATS: </p>'''
    #converted_html += convert_leaderboard_to_string()
    converted_html += str(get_leaderboard())
    return converted_html + """ </body> </html>""" 

def compare(a:LeaderboardUpdateRequest,b:LeaderboardUpdateRequest):
    return a.enemies_killed-b.enemies_killed

@app.post("/update-leaderboard")
async def update_leaderboard(leaderboard_update_request:LeaderboardUpdateRequest):
    """home page"""
    #global LEADERBOARD
    #LEADERBOARD.append(leaderboard_update_request)
    #highest_kills = LEADERBOARD.sort(key=lambda x: x.enemies_killed,reverse=True)
    
    message = write_leaderboard(leaderboard_update_request.name,leaderboard_update_request.enemies_killed,leaderboard_update_request.time_completed)
    return {message}

