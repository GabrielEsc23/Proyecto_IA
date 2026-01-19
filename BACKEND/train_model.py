#Preparar el dataset para que pueda ser usado por un modelo de IA.
import numpy as np
import pandas as pd 
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer,AutoTokenizer
from sklearn.metrics import accuracy_score



#Cargar los datos
df = pd.read_csv("DATA/training.csv")
print(df.head())
print(df["label"].value_counts())

#Covertir a Datasets de HuggingFace 
dataset=Dataset.from_pandas(df)

#Separar en train y validation
split=dataset.train_test_split(test_size=0.2)
train_ds = split["train"]
val_ds = split["test"]

# 4. Cargar tokenizer base
#Convertir el texto en números para que la IA pueda aprender
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

#Funcion para tokenizar 
def tokenize(example): 
    return tokenizer(
        example["text"],
        padding="max_length",
        truncation=True, 
        max_length=128
    )
# 6. Tokenizar datasets
train_ds = train_ds.map(tokenize, batched=True)
val_ds = val_ds.map(tokenize, batched=True)


# 7. Mostrar ejemplo tokenizado
print(train_ds[0])


num_labels= 6 #Numero de emocines del dataset

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=num_labels
)

# Métrica de evaluación
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc}

# Configuración de entrenamiento
training_args = TrainingArguments(
    output_dir="./emotion_model",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# Entrenar
trainer.train()

# Guardar modelo final
trainer.save_model("./emotion_model")
tokenizer.save_pretrained("./emotion_model")

