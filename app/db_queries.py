import psycopg2
import dotenv
import os

CONNECTION = None
CURSOR = None
def init_database():
    dotenv.load_dotenv()
    global CONNECTION
    global CURSOR
    CONNECTION = psycopg2.connect(host=os.getenv(HOST),port=5432,user=os.getenv(DBUSERNAME),dbname="postgres",password=os.getenv(PASSWORD),sslmode="require")
    print("connection established")

    CURSOR=CONNECTION.cursor()

def get_leaderboard():
    try:
        CURSOR.execute(
            """
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

