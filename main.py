from fastapi import FastAPI, HTTPException, Response, Request, Depends, Cookie, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
import secrets

app = FastAPI()
security = HTTPBasic()
app.counter = 0
app.pacjenci = []
app.uzytkownik = {"trudnY": "PaC13Nt"}
app.secret_key ="abc"
app.tokens = {}

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
def Hello():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def Hello(response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	response.status_code = status.HTTP_302_FOUND
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
def patientfun(patient: DajMiCosRq,response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	response.status_code = status.HTTP_302_FOUND
	app.pacjenci.append(patient)
	app.counter += 1
	#pacjent = DajMiCosResp(id = app.counter, patient = patient)
	return patient


@app.get("/patient/{pk}")
def pacjenci(pk: int,response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	response.status_code = status.HTTP_302_FOUND
	if pk < len(app.pacjenci):
		return app.pacjenci[pk-1]
	else:
		raise HTTPException(status_code = 204, detail = "Index not found")


@app.post("/login")
def login(response: Response, session_token: str = Depends(login_check_cred)):
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=session_token)
    return response

@app.post("/logout")
def logout(response: Response, session_token: str = Depends(check_cookie)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "log in to get access"
	response.status_code = status.HTTP_302_FOUND
	response.headers["Location"] = "/"
	app.tokens.pop(session_token)
