# Finalytics.AI 💰 — Smart Financial Analytics & Budget Intelligence

A production-ready full-stack web application designed for comprehensive personal finance management, budget planning, and algorithmic spending intelligence. Built with **Python Flask**, **PostgreSQL / SQLite**, **Bootstrap 5**, **Chart.js**, and **Gunicorn**.

---

## ✨ Features & Capabilities

- **🔐 User Authentication**: Secure registration and session authentication with hashed passwords via `Werkzeug` & `Flask-Login`.
- **📊 Real-Time Analytics Dashboard**:
  - Live Net Balance, Total Monthly Inflows, and Categorized Outflows.
  - **Financial Health Score (0–100)** and Savings Rate tracking.
  - **6-Month Cashflow Trajectory**: Dual-line area chart tracking income vs expenses across cycles.
  - **Expense Allocation Donut Chart**: Interactive visualization of spending distribution.
- **💡 Algorithmic AI Insights**: Real-time evaluation of burn rate, category concentration, and savings benchmarks with classified pill badges.
- **🎯 Dynamic Budgeting**: Define monthly spending ceilings per category with visual progress bars, remaining allowances, and budget breach warnings.
- **📋 Transaction Ledger**: Filter by income/expense type, category, or note search queries; record new transactions with an integrated modal.
- **📥 Native CSV Export**: Download transaction history directly to formatted `.csv`.
- **🚀 Production Deployment Ready**: Includes `Procfile`, `runtime.txt`, `Dockerfile`, `.env.example`, and automatic PostgreSQL URL normalization for platforms like Render, Railway, and Fly.io.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask 3.0, Flask-SQLAlchemy, Flask-Login, Pandas, Gunicorn
- **Database**: SQLite (default local) / PostgreSQL (production)
- **Frontend**: HTML5, Vanilla CSS Design System, Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4, Plus Jakarta Sans

---

## 🚀 Local Development Setup

### 1. Clone & Enter Repository
```bash
git clone https://github.com/Athish-Raj-Tadakanahalli/<your-repo-name>.git
cd Finalytics-AI-master
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your web browser. Database tables are initialized automatically on startup!

---

## 🌐 Production Deployment Guide

### Option 1: Deploy on Render (Recommended)
1. Push your repository to GitHub.
2. Log into [Render.com](https://render.com) and click **New > Web Service**.
3. Select your repository.
4. Set the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()"`
5. (Optional) Create a **PostgreSQL** database on Render and paste the `Internal Database URL` into your Web Service environment variables as `DATABASE_URL`.
6. Add `SECRET_KEY` in environment variables:
   Generate one via: `python -c "import secrets; print(secrets.token_hex(32))"`
7. Click **Deploy**!

### Option 2: Deploy on Railway
1. Click **New Project > Deploy from GitHub repo**.
2. Railway will automatically detect the `Procfile` and `requirements.txt`.
3. Add a PostgreSQL plugin on Railway if persistent storage is desired; Railway will automatically set `DATABASE_URL`.
4. Add `SECRET_KEY` in the project variables.

### Option 3: Deploy with Docker
Build and run the containerized application anywhere:
```bash
docker build -t finalytics-ai .
docker run -p 5000:5000 -e SECRET_KEY="your-secret-key" finalytics-ai
```

---

## 👤 Author
Developed by **Athish Raj Tadakanahalli** (@Athish-Raj-Tadakanahalli)
