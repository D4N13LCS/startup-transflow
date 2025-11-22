import os
import json
import asyncio
import time
from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from src.database.redis_client import r
from src.database.mongo_client import corridas_collection
import redis.asyncio as redis

load_dotenv()

BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")


broker = RabbitBroker(BROKER_URL)
app = FastStream(broker)


@broker.subscriber("corrida_finalizada")
async def processar_corrida(msg: str):
    corrida = json.loads(msg)

    motorista = corrida["motorista"]["nome"]
    valor = corrida["valor_corrida"]

    saldo_key = f"saldo:{motorista}"

    async with r.pipeline(transaction=True) as pipe:
        while True:
            try:
                await pipe.watch(saldo_key)
                current = await pipe.get(saldo_key)
                current = float(current) if current else 0.0

                pipe.multi()
                pipe.set(saldo_key, current + valor)
                await pipe.execute()
                break

            except redis.WatchError:
                continue

    await corridas_collection.update_one(
        {"id_corrida": corrida["id_corrida"]},
        {"$set": corrida},
        upsert=True
    )

    print(f"✔ Corrida processada: {corrida['id_corrida']}")


if __name__ == "__main__":
    while True:
        try:
            print("Tentando conectar no RabbitMQ...")
            asyncio.run(app.run())
            break
        except Exception as e:
            print(f"RabbitMQ ainda não disponível, tentando novamente em 5s: {e}")
            time.sleep(5)
