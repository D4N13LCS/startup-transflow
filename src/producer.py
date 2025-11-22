import json
import os
from dotenv import load_dotenv
from faststream.rabbit import RabbitBroker

load_dotenv()

BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")

broker = RabbitBroker(BROKER_URL)

async def publicar_corrida(corrida: dict):
    async with broker:
        await broker.publish(
            message=json.dumps(corrida),
            queue="corrida_finalizada"
        )
    print(f"📤 Corrida publicada: {corrida['id_corrida']}")
