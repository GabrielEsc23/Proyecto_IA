
#Se crea un servidor WEB CON FASTAPI(API)
from fastapi import FastAPI,UploadFile,File
import pdfplumber
import pandas as pd
from docx import Document
from io import BytesIO
from transformers import pipeline
from collections import Counter

EMOTION_MAP = {
    "joy": "Alegría",
    "sadness": "Tristeza",
    "fear": "Miedo",
    "anger": "Enojo",
    "surprise": "Sorpresa",
    "love": "Afecto",
    "others": "Neutral"
}


#Esto carga un modelo que reconoce emociones en español.
emotion_analyzer=pipeline(
    "text-classification",
    model="finiteautomata/beto-emotion-analysis",
    
)

app=FastAPI()
@app.get("/")
def root(): 
    return {"status":"ok"}

@app.post("/analyze-text")
async def analyze_text(data:dict):
    text=data.get("text","")
    if not text.strip():
        return {"error":"Texto vacío"}
    blocks=split_text(text)
    results=[]
    for block in blocks:
        analysis=analyze_block(block)
        results.append(analysis)
        
    emotions=[r["emotion"] for r in results]
    count=Counter(emotions)
    total=len(emotions)
    
    percentages = {
        emotion: round((qty / total) * 100, 2)
        for emotion, qty in count.items()
    }
    dominant=count.most_common(1)[0][0]
    
    return{
         "chars": len(text),
        "blocks": len(blocks),
        "dominant_emotion": dominant,
        "percentages": percentages,
        "timeline": results,
        "summary": build_summary(dominant, percentages)
    }
    
# Aqui se hace que la API pueda recibir archivos
#UploadFile representa el archivo que sube el usuario
#File(...) le dice a FastAPI que esto viene en un formulario
@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    file_bytes=await file.read()
    filename=file.filename.lower()
    
    if filename.endswith(".txt"):
        text=read_txt(file_bytes)
    elif filename.endswith(".pdf"):
        text=read_pdf(file_bytes)
    elif filename.endswith(".docx"):
        text=read_docx(file_bytes)
    elif filename.endswith(".xlsx"):
        text=read_excel(file_bytes)
    else:
        return {"error":"Formato no soportado"}
    
    blocks= split_text(text)
    results= []
    for block in blocks:
        analysis=analyze_block(block)
        results.append(analysis)
    emotions=[r["emotion"] for r in results]
    count=Counter(emotions)
    total=len(emotions)
    
    porcentages={
        emotion:round((qty/total)*100,2)
        for emotion,qty in count.items()
    }
    dominant=count.most_common(1)[0][0]
    return{
        "chars":len(text),
        "blocks":len(blocks),
        "dominant_emotion":dominant,
        "percentages":porcentages,
        "timeline":results,
        "preview":text[:300],
        "sumary": build_summary(dominant,porcentages)
    }
    
#Se van a leer los archivos que se reciben desde el cliente
def read_txt(file_bytes:bytes)-> str:
    return file_bytes.decode("utf-8",errors="ignore")

def read_pdf(file_bytes:bytes)-> str:
    text=""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text +=page_text + "\n"
    return text

def read_docx(file_bytes)-> str:
    doc=Document(BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)

def read_excel(file_bytes:bytes)-> str: 
    df=pd.read_excel(BytesIO(file_bytes))
    #Covertir todo el contenido a texto 
    return "\n".join(
        
        " ".join(str(cell) for cell in row)
        for row in df.values
    )
    
#Esta función:
#Toma todo el texto
#Lo separa en bloques de ~200 palabras
#Devuelve una lista de strings """

def split_text(text:str,max_words: int =200):
    words=text.split()
    blocks=[]
    current=[]
    
    for word in words:
        current.append(word)
        if len(current)>=max_words:
            blocks.append(" ".join(current))
            current=[]
    if current:
        blocks.append(" ".join(current))
    return blocks


def analyze_block(text:str):
    snippet=text[:512]
    result=emotion_analyzer(snippet)[0]
    label=result["label"]
    return{
        "emotion":EMOTION_MAP.get(label,label),
        "score":float(result["score"])
    }
    
def build_summary(dominant,percentages):
    parts=[f"{k} ({v}%)" for k, v in percentages.items()]
    return(
        f"El texto tiene un tono principalmente {dominant.lower()}. "
        f"Las emociones más presentes son: " + ", ".join(parts)
    )
    