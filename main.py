from fastapi import FastAPI 

from pydantic import BaseModel

app = FastAPI()
app.counter = 0

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

class DajMiCosRq(BaseModel):
	name: str
	surename: str

class DajMiCosResp(BaseModel):
	id: int
	patient: DajMiCosRq

@app.post("/patient")#, response_model=DajMiCosResp)
def patientfun(patient: DajMiCosRq):
	#global counter
	app.counter += 1
	pacjent = DajMiCosResp(id = app.counter, patient = patient)
	#app.counter += 1
	return pacjent
	#return DajMiCosResp(patient=rq.dict())




