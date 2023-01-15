import sqlite3
import os
from source.settings import DATABASE_NAME

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, DATABASE_NAME)


class Handler:
    def __init__(self):
        db = db_path
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def get_score(self, level_id):
        score = self.cur.execute('''SELECT max_score FROM level_max_score''').fetchall()
        return score[level_id][0]

    def save_result(self, level_id, result):
        prev_result = self.get_score(level_id)
        if result > prev_result:
            self.cur.execute(f'''UPDATE level_max_score SET max_score={result} WHERE max_score={prev_result} ''')
            self.con.commit()