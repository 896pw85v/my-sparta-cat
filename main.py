from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mb_lib
import db_conn
app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers = ['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def read_item(body: dict):
    print(body)
    return mb_lib.get_images()
# simply return objects. FastAPI packs it into json

@app.post("/log-in")
def log_in(cre: dict):
    print(cre)
    return db_conn.sign_user(cre['u-name'])