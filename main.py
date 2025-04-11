from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parsers.ufsm_parser import parse_ufsm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/editais/ufsm")
def get_editais_ufsm():
    return parse_ufsm()