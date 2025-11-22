from fastapi import FastAPI
from src.models.corrida_model import Corrida
from src.database.mongo_client import corridas_collection
from src.database.redis_client import r
from src.producer import publicar_corrida
import asyncio

app = FastAPI(title="TransFlow API")


# POST — publica evento no broker
@app.post("/corridas")
async def cadastrar_corrida(corrida: Corrida):
    asyncio.create_task(publicar_corrida(corrida.dict()))
    return {"message": "Corrida publicada para processamento"}


# GET — todas corridas
@app.get("/corridas")
async def listar_corridas():
    dados = []
    cursor = corridas_collection.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        dados.append(doc)
    return dados


# GET — filtrar por tipo de pagamento
@app.get("/corridas/{forma_pagamento}")
async def corridas_por_pagamento(forma_pagamento: str):
    dados = []
    cursor = corridas_collection.find({"forma_pagamento": forma_pagamento})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        dados.append(doc)
    return dados


# GET — saldo do motorista
@app.get("/saldo/{motorista}")
async def saldo_motorista(motorista: str):
    saldo = await r.get(f"saldo:{motorista}")
    return {"motorista": motorista, "saldo": float(saldo) if saldo else 0.0}
