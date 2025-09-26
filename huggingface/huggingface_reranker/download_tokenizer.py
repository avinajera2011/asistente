from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "BAAI/bge-reranker-base"

print(f"Descargando modelo y tokenizador: {MODEL_NAME}")
AutoTokenizer.from_pretrained(MODEL_NAME)
AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
print("Descarga completa.")
