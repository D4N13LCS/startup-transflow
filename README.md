# TransFlow — Sistema de Processamento de Corridas

Sistema assíncrono baseado em microsserviços utilizando **FastAPI**, **RabbitMQ**, **Redis** e **MongoDB** para processar corridas, atualizar saldos de motoristas e armazenar histórico de viagens.

---

## 🚀 Instalação e Execução

### **1. Clonar o repositório**

```bash
git clone http://github.com/D4N13LCS/startup-transflow
cd transflow
```

### **2. Criar arquivo `.env`**

Crie um arquivo `.env` na raiz com:

```
MONGO_URI=mongodb://mongo:27017
REDIS_URL=redis://redis:6379
BROKER_URL=amqp://guest:guest@rabbitmq:5672/
```

### **3. Subir os containers**

```bash
docker compose up --build
```

Serviços iniciados:

* `app` — API FastAPI
* `consumer` — worker de processamento
* `rabbitmq` — broker de mensagens
* `redis` — cache e armazenamento de saldo
* `mongo` — banco principal

Acesse:

* **API:** [http://localhost:8000](http://localhost:8000)
* **Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **RabbitMQ:** [http://localhost:15672](http://localhost:15672) (guest / guest)

---

## 🔐 Variáveis de Ambiente

Essenciais para execução local ou em containers:

```
MONGO_URI=mongodb://mongo:27017
REDIS_URL=redis://redis:6379
BROKER_URL=amqp://guest:guest@rabbitmq:5672/
```

Essas variáveis também são definidas no `docker-compose.yml` para garantir comunicação entre serviços.

---

## 🧪 Como Usar e Testar

### **1. Enviar uma corrida (publica mensagem na fila)**

**POST /corridas**

```json
{
  "id_corrida": "12345",
  "passageiro": { "nome": "Carlos", "telefone": "99999-0000" },
  "motorista": { "nome": "João", "nota": 4.8 },
  "origem": "Centro",
  "destino": "Aeroporto",
  "valor_corrida": 32.50,
  "forma_pagamento": "pix"
}
```

O sistema irá:

1. Publicar no RabbitMQ
2. Consumer irá processar
3. Redis será atualizado com saldo atômico
4. Mongo receberá o documento persistido

### **2. Listar corridas**

```
GET /corridas
```

### **3. Filtrar por forma de pagamento**

```
GET /corridas/pix
```

### **4. Consultar saldo do motorista**

```
GET /saldo/João
```

O Redis retorna o saldo atualizado pela fila.

---

## 📚 Swagger — Documentação Interativa

Acesse:

```
http://localhost:8000/docs
```

Permite:

* testar endpoints
* visualizar schemas
* entender modelos
* enviar requisições sem Postman

---

## 🖼 Capturas de Tela

### **Swagger — Endpoints**

* GET /corridas
  ![alt text](image.png)

* Response
  ![alt text](image-1.png)

* POST /corridas
  ![alt text](image-2.png)

* Response
  ![alt text](image-3.png)

* GET /corridas/{forma_pagamento}
  ![alt text](image-4.png)

* Response
  ![alt text](image-5.png)

* GET /saldo/{motorista}
  ![alt text](image-6.png)

* Response
  ![alt text](image-7.png)

---

## 🛠 Logs de Execução

### **API (app)**

Use:

```
docker logs app
```

![alt text](image-8.png)

### **Consumer**

Use:

```
docker logs -f consumer
```

![alt text](image-9.png)

### **RabbitMQ (fila ativa)**

![alt text](image-10.png)

### **MongoDB (corridas)**

Comandos:

```
docker exec -it mongo mongosh
use transflow
db.corridas.find().pretty()
```

Exemplo:
![alt text](image-11.png)

### **Redis (saldos)**

1. Acesse o container do Redis

```bash
docker exec -it redis redis-cli
```

2. Liste todas as chaves existentes

```bash
KEYS *
```

3. Consulte um saldo salvo como string

```bash
GET saldo:Fabricio
```

4. Verificar se o Redis está persistindo corretamente

```bash
INFO persistence
```

<img width="788" height="210" alt="image" src="https://github.com/user-attachments/assets/d38e673e-5f8c-489a-ae4b-694823bfd585" />


---
