from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import schemas
import crud
from database import SessionLocal
from uuid import uuid4

# Necessary imports for langchain summarization
# Para modelos de linguagem e cadeias
#####from langchain.llms import OpenAI  # Na v0.1.1, OpenAI pode estar diretamente em llms
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate  # PromptTemplate geralmente está em prompts
from langchain.chains import LLMChain  # LLMChain deve estar disponível diretamente em chains

# Para interagir com PDFs
#####from langchain.document_loaders import PyPDFLoader  # Carrega PDFs
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Divide texto
####from langchain.embeddings import OpenAIEmbeddings  # Embeddings da OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
####from langchain.vectorstores import FAISS  # Banco de vetores FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA  # Cadeia de recuperação de perguntas e respostas

# Import personalizado (não mexo nisso, presumo que seja seu)
from schemas import QuestionRequest
llm = OpenAI()

router = APIRouter(prefix="/pdfs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.PDFResponse, status_code=status.HTTP_201_CREATED)
def create_pdf(pdf: schemas.PDFRequest, db: Session = Depends(get_db)):
    return crud.create_pdf(db, pdf)

@router.post("/upload", response_model=schemas.PDFResponse, status_code=status.HTTP_201_CREATED)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_name = f"{uuid4()}-{file.filename}"
    return crud.upload_pdf(db, file, file_name)

@router.get("", response_model=List[schemas.PDFResponse])
def get_pdfs(selected: bool = None, db: Session = Depends(get_db)):
    return crud.read_pdfs(db, selected)

@router.get("/{id}", response_model=schemas.PDFResponse)
def get_pdf_by_id(id: int, db: Session = Depends(get_db)):
    pdf = crud.read_pdf(db, id)
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf

@router.put("/{id}", response_model=schemas.PDFResponse)
def update_pdf(id: int, pdf: schemas.PDFRequest, db: Session = Depends(get_db)):
    updated_pdf = crud.update_pdf(db, id, pdf)
    if updated_pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return updated_pdf

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_pdf(id: int, db: Session = Depends(get_db)):
    if not crud.delete_pdf(db, id):
        raise HTTPException(status_code=404, detail="PDF not found")
    return {"message": "PDF successfully deleted"}

print ("%%%% ÁREA LANGCHAIN #####")
# LANGCHAIN
langchain_llm = OpenAI(temperature=0)

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

@router.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {'summary': summary}

print ("%%%%% INÍCIO Ask a question about one PDF file %%%%%")
# Ask a question about one PDF file
@router.post("/qa-pdf/{id}")
def qa_pdf_by_id(id: int, question_request: QuestionRequest,db: Session = Depends(get_db)):
    pdf = crud.read_pdf(db, id)
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    print(pdf.file)
    loader = PyPDFLoader(pdf.file)
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000,chunk_overlap=400)
    document_chunks = text_splitter.split_documents(document)
    embeddings = OpenAIEmbeddings()
    stored_embeddings = FAISS.from_documents(document_chunks, embeddings)
    QA_chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=stored_embeddings.as_retriever())
    question = question_request.question
    answer = QA_chain.run(question)
    return answer

print ("%%%%% FIM Ask a question about one PDF file %%%%%")

#Incluído por Paul Moniz
###write_poem_template_string = """
write_sumar_template_string = """
        Write a short poem with the following text:
        {text}
"""

###write_poem_prompt = PromptTemplate(
write_sumar_prompt = PromptTemplate(
    template=write_sumar_template_string,
    input_variables=['text'],
)

###write_poem_chain = LLMChain(
write_sumar_chain = LLMChain(
    llm=langchain_llm,
    prompt=write_sumar_prompt,
)

###@router.post("/write-poem/{id}")
###async def write_poem_by_id(id: int, db: Session = Depends(get_db)):
@router.post("/write-sumar/{id}")
###async def write_poem_by_id(id: int, db: Session = Depends(get_db)):
async def write_sumar_by_id(id: int, db: Session = Depends(get_db)):
    pdf = crud.read_pdf(db, id)
    if pdf  is None:
        raise HTTPException(status_code=404, detail="pdf do not found")
    sumar = write_sumar_chain.run(text=pdf.name)
    print ("%%%%%%%%%% sumar em write_sumar_by_id %%%%%%%%% = ", sumar)
    return {'sumar': sumar}