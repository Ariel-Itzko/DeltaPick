from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello {name}"}
