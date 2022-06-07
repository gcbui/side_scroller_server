"""fast api routing tool for api"""
from re import L
from unicodedata import name
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


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


app = FastAPI(title = "cmd_adventures")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)


@app.get("/")
async def root():
    """home page"""
    return {"message": "Welcome to Side Scroller Server"}


@app.get("/leaderboard",response_class=HTMLResponse)
async def leaderboard():
    """home page"""
    
    converted_html = '''<!DOCTYPE html>
    
    <html>
    <body>

    <h2 title="LEADERBOARD">LEADERBOARD</h2>

    <p title="I'm a tooltip">HERE ARE THE STATS: </p>'''
    converted_html += convert_leaderboard_to_string()
    return converted_html + """ </body> </html>""" 

def compare(a:LeaderboardUpdateRequest,b:LeaderboardUpdateRequest):
    return a.enemies_killed-b.enemies_killed

@app.post("/update-leaderboard")
async def update_leaderboard(leaderboard_update_request:LeaderboardUpdateRequest):
    """home page"""
    global LEADERBOARD
    LEADERBOARD.append(leaderboard_update_request)
    #highest_kills = sorted(LEADERBOARD,cmp=compare)
    highest_kills = LEADERBOARD.sort(key=lambda x: x.enemies_killed,reverse=True)
    return {"message": "Welcome to Side Scroller Server"}
