from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parsers_html.ufsm_parser import parse_ufsm
from parsers_pdf.ufsm_pdf_parser import extrair_competencias

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

@app.get("/ler-pdf/")
def extrair_competencias_ufsm(url:str):
    try:
        conteudo = extrair_competencias(url)
        return {"Conteudo: ": conteudo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
