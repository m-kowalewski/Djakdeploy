from fastapi import FastAPI, HTTPException, Response, Request, Depends, Cookie, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
import secrets

app = FastAPI()
security = HTTPBasic()
app.counter = 0
app.next_patient_id=0
app.patients = {}
app.uzytkownik = {"trudnY": "PaC13Nt"}
app.secret_key ="abc"
app.tokens = {}
templates = Jinja2Templates(directory="templates")

def check_cookie(session_token: str = Cookie(None)):
    if session_token not in app.tokens:
        session_token = None
    return session_token

def login_check_cred(credentials: HTTPBasicCredentials = Depends(security)):
    correct = False
    for username, password in app.uzytkownik.items():
        correct_username = secrets.compare_digest(credentials.username, username)
        correct_password = secrets.compare_digest(credentials.password, password)
        if (correct_username and correct_password):
            correct = True
    if not correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens[session_token]=credentials.username
    return session_token

@app.get('/')
def Hello():#response: Response, session_token: str = Depends(check_cookie)):
	#response.status_code = status.HTTP_302_FOUND
	return {"message": "Hello!"}

#@app.post('/')
#def Hello(response: Response, session_token: str = Depends(check_cookie)):
#	response.status_code = status.HTTP_302_FOUND
#	return {"message": "Hello!"}

@app.get('/welcome')
def Hello(request: Request, response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		#response.status_code = status.HTTP_401_UNAUTHORIZED
		#return "log in to get access"
		raise HTTPException(status_code=401, detail="Unathorised")
	#response.status_code = status.HTTP_302_FOUND
	username = app.tokens[session_token]
	#return {"message": "Hello World during the coronavirus pandemic!"}
	return templates.TemplateResponse("item.html", {"request": request, "user":username})

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
	surname: str

class DajMiCosResp(BaseModel):
	id: int
	patient: DajMiCosRq

@app.get("/patient")
def patientfun(response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	if len(app.patients) != 0:
		return app.patients
	#resp = {}
	#for x in app.pacjenci.values():
	#	resp[x.id] = { 'name': x.name, 'surname': x.surname}
	#if resp:
	#	return JSONResponse(resp)
	response.status_code = status.HTTP_204_NO_CONTENT

@app.post("/patient")#, response_model=DajMiCosResp)
def patientfun(Rq: DajMiCosRq,response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	pk=f"id_{app.next_patient_id}"
	app.patients[pk]=Rq.dict()
	response.status_code = status.HTTP_302_FOUND
	response.headers["Location"] = f"/patient/{pk}"
	app.next_patient_id+=1
	#app.pacjenci.append(patient)
	#app.counter += 1
	###pacjent = DajMiCosResp(id = app.counter, patient = patient)
	#return patient


@app.get("/patient/{pk}")
def pacjenci(pk: str, response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	#response.status_code = status.HTTP_302_FOUND
	if pk in app.patients:
		return app.patients[pk]
	response.status_code = status.HTTP_204_NO_CONTENT

@app.delete("/patient/{pk}")
def delete_pacjent(pk: str, response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	app.patients.pop(pk, None)
	response.status_code = status.HTTP_204_NO_CONTENT
	#response.status_code = status.HTTP_302_FOUND

@app.post("/login")
def login(response: Response, session_token: str = Depends(login_check_cred)):
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=session_token)
    #return response

@app.post("/logout")
def logout(response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	#response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
	response.status_code = status.HTTP_302_FOUND
	response.headers["Location"] = "/"
	app.tokens.pop(session_token)
	#return response
	#return RedirectResponse("/")