
# PayBridge – FastAPI Payment Middleware

PayBridge is a stateless HTTP middleware built using FastAPI and PostgreSQL that acts as an integration layer between business services and an external payment provider.

## 🚀 Features

- Make a payment for a sales transaction
- Revert a single payment
- List all payments for a transaction
- Revert all payments for a transaction
- Stateless architecture with PostgreSQL persistence
- Dockerized and ready with docker-compose
- External unreliable provider handled gracefully

---

## 📦 Requirements

- Docker
- Docker Compose
- Python 3.11+ (for local development)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Mkamal88/PayBridge.git
cd PayBridge
```

### 2. Install the `.whl` file

The external provider is provided as a Python wheel.

Place the file `technical_exercise-1.0.0-py3-none-any.whl` in the root directory.

### 3. Start the project

```bash
docker-compose up --build
```

Access the API at: [http://localhost:8888/docs](http://localhost:8000/docs)

---

## 📌 Endpoints Summary

### `POST /transactions`
Create a new sales transaction.

### `POST /payment`
Make a payment for a transaction using the external provider.

### `GET /transactions/{id}/payments`
List all payments associated with a transaction.

### `POST /revert`
Revert a specific payment by request_id.

### `POST /transactions/{id}/revert_all`
Revert all payments associated with a transaction.

---

## ⚙️ Design Notes

- `SalesTransaction` and `Payment` are SQLAlchemy ORM models.
- All interactions with the external provider are JSON-based.
- The `request_id` is UUID-based and generated internally.
- Error responses are handled and exposed with meaningful messages.

---

## 🧪 Testing

```bash
docker-compose exec api pytest
```

Tests are located in the `/tests` directory.

---

## 🐳 Docker Notes

- App runs on port `8000` internally. You can map it externally as needed in `docker-compose.yml`.

---

## 🧑‍💻 Author

Built by Mohamed Kamal.
