from fastapi import FastAPI
import os

app = FastAPI(title="Hello FastAPI on AKS")

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/")
def root():
    pod = os.getenv("POD_NAME", "unknown")
    return {
        "message": "Hola desde FastAPI desplegado en AKS 👋",
        "pod": pod
    }
