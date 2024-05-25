from fastapi import FastAPI, File, UploadFile, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.logging_config import logger
from utils import get_text_content_from_pdf_content
from langchain_utils import chunck_text_content_and_embedding_and_responde_user_input
from models import PDFContent
from database import engine, get_db
from database import Base
from dotenv import load_dotenv

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

message_history = list()

@app.on_event("startup")
async def startup():
    load_dotenv()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = UploadFile(...), db: AsyncSession = Depends(get_db)):
    if ".pdf" not in file.filename:
        message_history.append(f"Please provide an .PDF file")
        return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": False, "messages": message_history})

    message_history.append("Loading the PDF file. It may take some seconds" + file.filename)
    content = await file.read()
    pdf_text_content = get_text_content_from_pdf_content(content)

    new_pdf = PDFContent(filename=file.filename, content=pdf_text_content)
    db.add(new_pdf)
    await db.commit()

    message_history.append("PDF loaded with success: " + file.filename)
    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": True, "messages": message_history})

@app.post("/send")
async def send_message(request: Request, text: str = Form(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PDFContent).order_by(PDFContent.id.desc()).limit(1))
    pdf_content = result.scalar_one_or_none()

    if not pdf_content:
        message_history.append("No PDF content found. Please upload a PDF first.")
        return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": False, "messages": message_history})

    logger.info(f"PDF Content, {pdf_content.content}")
    response = chunck_text_content_and_embedding_and_responde_user_input(pdf_content.content, text)
    message_history.append(f"You: {text} Assistent: {response}")

    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": True, "messages": message_history})

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "pdf_uploaded": False, "messages": message_history})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
