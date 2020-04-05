from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.pacjenci = []

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
	app.pacjenci.append(patient)
	app.counter += 1
	pacjent = DajMiCosResp(id = app.counter, patient = patient)

	return pacjent
	#return DajMiCosResp(patient=rq.dict())

@app.get("/patient/{pk}")
def pacjenci(pk: int):
	if pk < len(app.pacjenci[pk-1]):
		return app.pacjenci[pk-1]
	else:
		raise HTTPException(status_code = 204, detail = "Index not found")






