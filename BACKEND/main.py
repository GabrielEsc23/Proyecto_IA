
#Se crea un servidor WEB CON FASTAPI(API)
from fastapi import FastAPI,UploadFile,File
import pdfplumber
import pandas as pd
from docx import Document
from io import BytesIO
from transformers import pipeline
from collections import Counter


LABEL_MAP = {
    "LABEL_0": "Tristeza",
    "LABEL_1": "Alegría",
    "LABEL_2": "Amor",
    "LABEL_3": "Enojo",
    "LABEL_4": "Miedo",
    "LABEL_5": "Sorpresa"
}

translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-es-en"
)
#Esto carga un modelo que reconoce emociones en español.
emotion_analyzer = pipeline(
    "text-classification",
    model="./emotion_model",  # o el nombre que elegiste
    return_all_scores=True
)

app=FastAPI()
@app.get("/")
def root(): 
    return {"status":"ok"}

@app.post("/analyze-text")
async def analyze_text(data: dict):
    text = data.get("text", "")
    if not text.strip():
        return {"error": "Texto vacío"}

    snippet = text[:512]

    # Traducir a inglés
    translated = translator(snippet)[0]["translation_text"]

    # Analizar una sola vez todo el texto
    results = emotion_analyzer(translated)[0]

    # Convertir etiquetas a nombres humanos
    emotions = {
        LABEL_MAP.get(r["label"], r["label"]): round(r["score"] * 100, 2)
        for r in results
    }

    dominant = max(emotions, key=emotions.get)

    return {
        "chars": len(text),
        "dominant_emotion": dominant,
        "percentages": emotions,
        "summary": build_summary(dominant, emotions)
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
    
    blocks= smart_split(text)
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
        "summary": build_summary(dominant,porcentages)
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

import re

def smart_split(text: str, max_words: int = 120):
    import re
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)

    blocks = []
    current = []

    for s in sentences:
        words = s.split()
        if len(current) + len(words) <= max_words:
            current.extend(words)
        else:
            blocks.append(" ".join(current))
            current = words

    if current:
        blocks.append(" ".join(current))

    return blocks



def analyze_block(text: str):
    snippet = text[:512]

    # Traducir a inglés
    translated = translator(snippet)[0]["translation_text"]

    # Analizar con tu modelo entrenado en inglés
    result = emotion_analyzer(translated)[0]
    label = result["label"]

    human = LABEL_MAP.get(label, label)

    return {
        "emotion": human,
        "score": float(result["score"])
    }

    
def build_summary(dominant,percentages):
    parts=[f"{k} ({v}%)" for k, v in percentages.items()]
    return(
        f"El texto tiene un tono principalmente {dominant.lower()}. "
        f"Las emociones más presentes son: " + ", ".join(parts)
    )
    