from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="aws-1-ap-northeast-1.pooler.supabase.com",
    database="postgres",
    user="postgres.pvqkfmfpwybhfebnxebl",
    password="!xnW+_YzMkk7am2",
    port="5432"
)

class Item(BaseModel):
    a: int
    b: str
    c: float
    d: int

@app.post("/close")
def run_close(item: Item):
    try:
        cursor = conn.cursor()

        query = "SELECT * FROM close(%s, %s, %s, %s);"
        cursor.execute(query, (item.a, item.b, item.c, item.d))

        rows = cursor.fetchall()  # 🔥 כל התוצאות

        # 🔹 שמות העמודות
        colnames = [desc[0] for desc in cursor.description]

        cursor.close()

        # 🔹 הפיכה ל-JSON נורמלי
        result = [dict(zip(colnames, row)) for row in rows]

        return {
            "status": "success",
            "rows": result
        }

    except Exception as e:
        return {"error": str(e)}
