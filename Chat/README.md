# 🔐 API de Mensageria Segura com WebSocket

Projeto back-end focado em **segurança, autenticação e tempo real**, simulando um sistema de troca de mensagens privadas entre usuários, com **criptografia de conteúdo**, **WebSocket** e **controle de acesso**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **Django 5.0+**
- **Django REST Framework (DRF)**
- **Django Channels** (WebSocket)
- **JWT (JSON Web Token)**
- **PostgreSQL**
- **Redis** (Channel Layer)
- **Docker / Docker Compose**
- **Criptografia (Fernet / cryptography)**
- **Daphne** (ASGI Server)

---

## 📌 Funcionalidades

- ✅ Cadastro e autenticação de usuários
- ✅ Autenticação via JWT
- ✅ Envio de mensagens privadas em tempo real (WebSocket)
- ✅ Mensagens **criptografadas antes de serem salvas no banco**
- ✅ Listagem de mensagens do usuário autenticado
- ✅ Verificação de usuário em tempo real (✅ / ❌)
- ✅ Controle de permissões (acesso apenas às próprias mensagens)
- ✅ Validação de dados e tratamento de erros
- ✅ Dockerizado com PostgreSQL e Redis

---

## 🔐 Segurança Implementada

- Autenticação stateless com JWT
- Proteção de rotas sensíveis
- Criptografia do conteúdo das mensagens em repouso
- Isolamento de dados por usuário
- Validação de payloads da API
- WebSocket autenticado via token JWT na query string

---

## 🗂️ Estrutura do Projeto
Chat/
├── app/
│ ├── accounts/ # Autenticação e usuários
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ └── urls.py
│ │
│ ├── messaging/ # Mensagens e WebSocket
│ │ ├── consumers.py # Lógica do WebSocket
│ │ ├── middleware.py # Autenticação JWT no WebSocket
│ │ ├── routing.py # Rotas WebSocket
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── static/ # Frontend do chat
│ │ └── messaging/
│ │ ├── css/
│ │ │ └── chat.css
│ │ └── js/
│ │ └── chat.js
│ │
│ └── core/ # Configurações centrais
│ ├── asgi.py # Configuração ASGI com Channels
│ ├── settings.py
│ └── urls.py
│
├── staticfiles/ # Arquivos estáticos coletados
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── requirements.txt
└── README.md

text

---

## 🔑 Autenticação

A API utiliza **JWT** para autenticação REST e **WebSocket**.

### Login
POST /api/auth/login/

text

**Resposta:**
```json
{
  "access": "jwt_token",
  "refresh": "jwt_refresh_token"
}
O token deve ser enviado no header:

text
Authorization: Bearer <token>
Para WebSocket, o token é passado na query string:

text
ws://localhost:8000/ws/chat/?token=<jwt_token>
🔌 WebSocket - Chat em Tempo Real
Conectar ao WebSocket
javascript
const socket = new WebSocket(`ws://localhost:8000/ws/chat/?token=${ACCESS_TOKEN}`);
Enviar mensagem
javascript
socket.send(JSON.stringify({
    recipient: "username_destino",
    content: "Mensagem secreta"
}));
Receber mensagem
javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("De:", data.sender, "Mensagem:", data.message);
};
📡 Endpoints da API
Autenticação
Método	Rota	Descrição
POST	/api/auth/register/	Registrar novo usuário
POST	/api/auth/login/	Login (retorna JWT)
POST	/api/auth/refresh/	Refresh do token
GET	/api/auth/check-username/?username=<user>	Verifica se usuário existe
Mensagens
Método	Rota	Descrição
GET	/api/auth/messages/	Lista mensagens do usuário
POST	/api/auth/send/	Envia mensagem via REST
🐳 Executando com Docker
bash
# Construir e subir os containers
docker-compose up --build

# Aplicação disponível em:
http://localhost:8000

# Chat WebSocket disponível em:
ws://localhost:8000/ws/chat/
Serviços
Django + Daphne: Porta 8000

PostgreSQL: Porta 5432

Redis: Porta 6379

Comandos úteis
bash
# Ver logs
docker logs django_app

# Executar comandos no container
docker exec -it django_app bash

# Coletar arquivos estáticos
docker exec django_app python manage.py collectstatic --noinput

# Parar containers
docker-compose down

# Parar e remover volumes (limpar banco)
docker-compose down -v
🧪 Testes
bash
# Executar testes
docker exec django_app python manage.py test

# Ou localmente (com venv ativado)
python manage.py test
⚠️ Problemas Comuns e Soluções
WebSocket não conecta (404)
Verifique se o Redis está rodando: docker ps | grep redis

Confira se o token JWT é válido e não expirou

Verifique os logs: docker logs django_app

Arquivos estáticos não carregam
bash
docker exec django_app python manage.py collectstatic --noinput
Erro "Apps aren't loaded yet"
Certifique-se de que o asgi.py está configurado corretamente (imports após get_asgi_application())

📈 Possíveis Evoluções
✅ WebSocket para mensagens em tempo real (implementado)

⬜ Rate limiting (proteção contra spam)

⬜ Confirmação de leitura de mensagens

⬜ Criptografia ponta a ponta (E2EE)

⬜ Autenticação em dois fatores (2FA)

⬜ Logs e auditoria de segurança

⬜ Notificações push

🎯 Objetivo do Projeto
Este projeto foi desenvolvido para demonstrar:

Domínio de APIs REST e WebSockets

Aplicação prática de segurança

Organização de código e boas práticas

Integração com Docker e serviços (PostgreSQL, Redis)

Capacidade de construir soluções reais e escaláveis

👤 Autor
José Peixoto de Almeida Neto

Estudante de Análise e Desenvolvimento de Sistemas
Foco em Back-End, Segurança da Informação e Tempo Real

📄 Licença
Este projeto é de código aberto e está licenciado sob a MIT License.

📌 Projeto com fins educacionais e profissionais.