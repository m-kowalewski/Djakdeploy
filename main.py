from fastapi import FastAPI 

from pydantic import BaseModel

app = FastAPI()
@app.get('/')
def Hello():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def method():
	return {"method":"GET"}

@app.post("/method")
def method():
	return {"method":"POST"}

@app.put("/method")
def method():
	return {"method":"PUT"}

@app.delete("/method")
def method():
	return {"method":"DELETE"}
