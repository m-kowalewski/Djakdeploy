from fastapi import FastAPI 

from pydantic import BaseModel

app = FastAPI()
@app.get('/')
def Hello():
	return {"message": "Hello World during the coronavirus pandemic!"}
