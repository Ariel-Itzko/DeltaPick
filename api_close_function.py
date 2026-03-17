from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_connection():
    return psycopg2.connect(
        host=_required_env("DB_HOST"),
        database=_required_env("DB_NAME"),
        user=_required_env("DB_USER"),
        password=_required_env("DB_PASSWORD"),
        port=_required_env("DB_PORT")
    )

class Item(BaseModel):
    a: int
    b: str
    c: float
    d: int


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/close")
def run_close(item: Item):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM close(%s, %s, %s, %s);"
        cursor.execute(query, (item.a, item.b, item.c, item.d))

        rows = cursor.fetchall()

        colnames = [desc[0] for desc in cursor.description]

        result = [dict(zip(colnames, row)) for row in rows]

        return {
            "status": "success",
            "rows": result
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
