# 🧠 Sistema de Análisis de Emociones en Texto
**Proyecto Final – Fundamentos de Inteligencia Artificial**

Sistema basado en Procesamiento de Lenguaje Natural (NLP) para detectar y clasificar emociones presentes en textos escritos en español, utilizando modelos transformer y una arquitectura cliente-servidor.

---

## 👥 Integrantes
- Gabriel Escobar  
- Xavier Ochoa  
- Wilmer Ramos  

---

## 📖 Descripción del Proyecto
Este proyecto implementa un sistema de análisis emocional de texto que permite identificar la emoción dominante y la distribución porcentual de emociones en textos y documentos.  
Utiliza modelos de **Deep Learning** basados en **Transformers**, combinados con traducción automática para lograr una alta precisión en textos en español.

El sistema puede procesar texto directo o archivos en formatos como **TXT, PDF, DOCX, CSV y XLSX**, mostrando resultados de forma clara mediante una interfaz gráfica.

---

## 🎯 Objetivos
- Detectar y clasificar emociones en textos en español  
- Analizar documentos de diferentes formatos  
- Mostrar distribución porcentual de emociones  
- Proporcionar una interfaz gráfica fácil de usar  
- Aplicar conceptos fundamentales de Inteligencia Artificial y NLP  

---

## ❤️ Emociones Detectadas
El sistema identifica las siguientes emociones:
- Tristeza  
- Alegría  
- Amor  
- Enojo  
- Miedo  
- Sorpresa  

---

## 🏗️ Arquitectura del Sistema
El proyecto sigue una arquitectura **cliente-servidor**:

- **Backend**: API desarrollada con **FastAPI**
- **Frontend**: Interfaz gráfica desarrollada con **Tkinter**
- **Modelo IA**: DistilBERT fine-tuned para clasificación emocional
- **Traducción**: Pipeline `Helsinki-NLP/opus-mt-es-en`

---

## 🔄 Flujo de Funcionamiento
1. El usuario ingresa texto o carga un archivo  
2. El frontend envía la solicitud al backend  
3. El backend preprocesa y segmenta el texto  
4. El texto se traduce de español a inglés  
5. El modelo analiza las emociones  
6. Se agregan los resultados  
7. El frontend muestra la emoción dominante y porcentajes  

---

## ⚙️ Requisitos del Sistema

### Hardware
- Procesador: Intel Core i5 o equivalente (mínimo)
- RAM: 8 GB (16 GB recomendado)
- GPU: Opcional (mejora rendimiento)

### Software
- Python 3.8 o superior
- Sistemas compatibles: Windows, Linux, macOS

---

## 📦 Tecnologías Utilizadas
- Python
- FastAPI
- Transformers (Hugging Face)
- DistilBERT
- Tkinter
- Pandas
- pdfplumber
- python-docx
- Requests

---

## 📂 Estructura del Proyecto
```text
├── BACKEND/
│   ├── main.py
│   ├── train_model.py
│   ├── emotion_model/
│   └── requirements.txt
├── Frontend/
│   └── frontend.py
└── README.md

```
---

## 🚀 Instalación
- Instalar dependencias
pip install fastapi uvicorn transformers torch
pip install pdfplumber python-docx pandas openpyxl
pip install requests

- Ejecutar Backend
cd BACKEND
uvicorn main:app --reload

- Ejecutar Frontend
cd Frontend
python frontend.py

---


## 🔌 Endpoints de la API
Endpoint         Método        Descripción
/                GET           Verificar estado del servidor
/analyze-text    POST          Analiza texto directo
/upload          POST          Analiza archivos


---


## 📊 Ejemplo de Respuesta
{
  "dominant_emotion": "Alegría",
  "percentages": {
    "Alegría": 78.45,
    "Amor": 8.12,
    "Tristeza": 5.23
  }
}


---


## ⚠️ Limitaciones
	•	Optimizado para español
	•	Puede perder matices en la traducción
	•	No detecta sarcasmo con alta precisión
	•	Textos muy largos incrementan el tiempo de análisis


---


## 🔮 Mejoras Futuras
	•	Modelo entrenado directamente en español
	•	Más emociones detectables
	•	Visualización temporal de emociones
	•	Interfaz web (React / Vue)
	•	Exportación de resultados


---


## 📌 Conclusión
Este proyecto demuestra la aplicación práctica de la Inteligencia Artificial y el Procesamiento de Lenguaje Natural en el análisis emocional de textos, integrando modelos modernos, traducción automática y una arquitectura modular que permite escalabilidad y mejoras futuras.
