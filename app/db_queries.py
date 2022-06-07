import psycopg2
import dotenv
import os
from pathlib import Path
from os.path import join, dirname


CONNECTION = None
CURSOR = None
def init_database():
    dotenv_path = join(dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)
    global CONNECTION
    global CURSOR
    print(os.getenv("HOST"))
    CONNECTION = psycopg2.connect(host=os.getenv("HOST"),port=5432,user=os.getenv("DBUSERNAME"),dbname="postgres",password=os.getenv("PASSWORD"),sslmode="require")
    print("connection established")

    CURSOR=CONNECTION.cursor()

def get_leaderboard():
    try:
        dotenv.load_dotenv()
        CURSOR.execute(
            """
            select *
            from leaderboard
            """
        )
        results = CURSOR.fetchall()
        return results
    except Exception as ex:
        return "Failed to connect" + str(ex)


def write_leaderboard(name:str,enemies_killed:int,time_completed:int):
    try:
        CURSOR.execute(
            """
            insert into leaderboard(name,enemies_killed,time_completed)
            values(
                '{name}','{enemies_killed}','{time_completed}'
            );
            """
        )
        CURSOR.commit()
        return "Wrote to db succesfully"
    except:
        return "Failed to wrtie to db"

