from fastapi import FastAPI, File, UploadFile, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Variável global para armazenar o histórico de mensagens e arquivos (para fins de demonstração)
message_history = []
file_history = []

@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    
    # Armazene o arquivo em uma variável (ou faça o processamento necessário)
    file_history.append({"filename": file.filename, "content": content})
    
    # Adicione uma mensagem ao histórico informando que o PDF foi carregado
    message_history.append("PDF carregado com sucesso: " + file.filename)

    # Renderize a interface novamente com o campo de texto habilitado
    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": True, "messages": message_history})

@app.post("/send")
async def send_message(request: Request, text: str = Form(...)):
    # Adicione a mensagem ao histórico
    message_history.append(f"Você: {text}")
    
    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": True, "messages": message_history})

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": False, "messages": message_history})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
