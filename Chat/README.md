# 🔐 API de Mensageria Segura

Projeto back-end focado em **segurança, autenticação e boas práticas**, simulando um sistema de troca de mensagens privadas entre usuários, com **criptografia de conteúdo** e **controle de acesso**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **Django**
- **Django REST Framework (DRF)**
- **JWT (JSON Web Token)**
- **PostgreSQL**
- **Docker / Docker Compose**
- **Criptografia (Fernet / cryptography)**

---

## 📌 Funcionalidades

- Cadastro de usuários
- Autenticação via JWT
- Envio de mensagens privadas entre usuários
- Mensagens **criptografadas antes de serem salvas no banco**
- Listagem de mensagens do usuário autenticado
- Controle de permissões (acesso apenas às próprias mensagens)
- Validação de dados e tratamento de erros

---

## 🔐 Segurança Implementada

- Autenticação stateless com JWT
- Proteção de rotas sensíveis
- Criptografia do conteúdo das mensagens em repouso
- Isolamento de dados por usuário
- Validação de payloads da API

---

## 🗂️ Estrutura final sugerida

Chat/
├── app/                     ← código da aplicação
│   ├── accounts/            ← autenticação e usuários
│   │   ├── migrations/
│   │   ├── **init**.py
│   │   ├── [admin.py](http://admin.py/)
│   │   ├── [apps.py](http://apps.py/)
│   │   ├── [models.py](http://models.py/)
│   │   ├── [serializers.py](http://serializers.py/)
│   │   ├── [views.py](http://views.py/)
│   │   ├── [urls.py](http://urls.py/)
│   │   └── [tests.py](http://tests.py/)
│   │
│   ├── messaging/           ← mensagens seguras
│   │   ├── migrations/
│   │   ├── **init**.py
│   │   ├── [admin.py](http://admin.py/)
│   │   ├── [apps.py](http://apps.py/)
│   │   ├── [models.py](http://models.py/)
│   │   ├── [serializers.py](http://serializers.py/)
│   │   ├── [views.py](http://views.py/)
│   │   ├── [urls.py](http://urls.py/)
│   │   └── [tests.py](http://tests.py/)
│   │
│   └── core/                ← settings centrais
│       ├── **init**.py
│       ├── [asgi.py](http://asgi.py/)
│       ├── [settings.py](http://settings.py/)
│       ├── [urls.py](http://urls.py/)
│       └── [wsgi.py](http://wsgi.py/)
│
├── venv/                    ← ambiente virtual (não sobe pro git)
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── [entrypoint.sh](http://entrypoint.sh/)
├── [manage.py](http://manage.py/)
├── requirements.txt
└── [README.md](http://readme.md/)

---

## 🔑 Autenticação

A API utiliza **JWT** para autenticação.

### Login

```
POST /api/auth/login/

```

**Resposta:**

```json
{
  "access": "jwt_token",
  "refresh": "jwt_refresh_token"
}

```

O token deve ser enviado no header:

```
Authorization: Bearer <token>

```

---

## ✉️ Endpoints Principais

### Enviar mensagem

```
POST /api/messages/send/

```

```json
{
  "receiver": "username_destino",
  "content": "Mensagem secreta"
}

```

### Listar mensagens

```
GET /api/messages/

```

---

## 🐳 Executando com Docker

```bash
docker-compose build5
docker-compose up

```

A aplicação estará disponível em:

```
http://localhost:8000

```

---

## 🧪 Testes

Os testes podem ser executados com:

```bash
python manage.py test

```

---

## 📈 Possíveis Evoluções

- WebSocket para mensagens em tempo real
- Rate limiting (proteção contra spam)
- Confirmação de leitura de mensagens
- Criptografia ponta a ponta (E2EE)
- Autenticação em dois fatores (2FA)
- Logs e auditoria de segurança

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido para demonstrar:

- Domínio de APIs REST
- Aplicação prática de segurança
- Organização de código
- Boas práticas de back-end
- Capacidade de construir soluções reais

---

## 👤 Autor

**José Peixoto de Almeida Neto**

Estudante de Análise e Desenvolvimento de Sistemas

Foco em Back-End e Segurança da Informação

---

📌 *Projeto com fins educacionais e profissionais.*