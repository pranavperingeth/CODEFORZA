# 🏆 Codeforza — Elevating Competitive Programming 🚀

Welcome to **Codeforza**, a full-featured, blazing-fast competitive programming platform built specifically for colleges and developer communities! 

Imagine having your own private Codeforces—where you can write, run, and submit code directly in the browser via a **VS Code-style editor**, climb the global **Leaderboard**, and manage everything through a sleek **Admin Panel**. That's Codeforza! ✨

---

## 📸 Platform Overview

| 🌟 Feature | 📝 What it does |
|---|---|
| **🔒 Secure Auth** | Bulletproof login/register with bcrypt-hashed passwords + JWT tokens. |
| **📊 Dashboard** | Browse problems, check out difficulty badges, search instantly, and track your submission history! |
| **💻 The Arena** | Side-by-side problem statements and a **Monaco Editor** (VS Code's engine). Run custom tests or submit for judgment! |
| **🏆 Leaderboard** | Climb the ranks! Global standings based on unique problems solved. Who is the undisputed champion? |
| **⚙️ Admin Panel** | The command center. Add new problems, inject secret test cases, and manage user roles with ease. |

---

## 🛠️ Architecture & Tech Stack

Codeforza isn't just a toy—it's built with a clean separation of concerns, utilizing a modern and scalable stack.

### 🎨 Frontend: Beautiful by Default
The frontend was completely overhauled to prioritize visual excellence and a buttery-smooth user experience.
- **Tailwind CSS 🌊**: Powered by Tailwind via CDN. It enables rapid prototyping and a beautiful, consistent, utility-first design system without the bloat of massive CSS files.
- **Typography & Aesthetics ✨**: Beautifully crafted with Google Fonts (`Inter` for readability, `Hanken Grotesk` for punchy headings, and `JetBrains Mono` for the code editor).
- **Sleek UI Components 🧩**: Enjoy structured spacing, subtle micro-animations on hover, and a premium card-based layout featuring gorgeous shadow depths.
- **Monaco Editor ⌨️**: A professional-grade coding experience baked right into your browser.

### ⚡ Backend: Built for Speed & Security
- **FastAPI (Python) 🚀**: Extremely fast execution, asynchronous capabilities, and automatic OpenAPI documentation out of the box.
- **SQLAlchemy 2.0 & PostgreSQL 🐘**: A rock-solid database setup. Parameterized queries prevent SQL injection, while Postgres effortlessly handles the complex on-the-fly math required for the live Leaderboard.
- **Ironclad Security 🛡️**: 
  - Passwords? Never in plaintext (hashed via `bcrypt`, 12 rounds).
  - Authentication? Completely stateless via `JWT` (HS256).
  - Spam protection? Handled gracefully by `slowapi` rate limiting.
- **The Judge Engine ⚖️**: Secure, sandboxed code execution using Python's `subprocess` in isolated temp directories. (Supports Python 3, C++ 17, C, and Java).

---

## 📁 Project Structure

```text
college-cp/
│
├── README.md
│
├── backend/                  🔥 The FastAPI Engine
│   ├── requirements.txt
│   ├── .env                  ← Top secret config goes here
│   └── app/
│       ├── main.py           ← The brain (middlewares, routers)
│       ├── database.py       ← DB Connection
│       ├── models.py         ← SQLAlchemy ORM models
│       ├── schemas.py        ← Pydantic validation magic
│       ├── auth.py           ← Hashing & JWT logic
│       ├── executor.py       ← The Code Judge
│       └── routers/          ← API Endpoints (Auth, Problems, Judge, Rankings)
│
└── frontend/                 ✨ The Tailwind UI
    ├── index.html            ← Login (Entry Point)
    ├── register.html         
    ├── dashboard.html        ← Problem List
    ├── problem.html          ← The Coding Arena
    ├── admin.html            ← Command Center
    ├── leaderboard.html      ← The Hall of Fame
    └── app.js                ← Shared JS superpowers
```

---

## 🚀 Setup & Running Locally

Ready to launch Codeforza on your machine? Let's go!

### Step 1 — Spin up PostgreSQL 🐘
Ensure Postgres is installed and running. Jump into your terminal:
```bash
psql -U postgres -c "CREATE DATABASE college_cp;"
```

### Step 2 — Configure Secrets 🤫
```bash
cd backend
cp .env.example .env
```
Open `.env` and plug in your database credentials and secret keys!

### Step 3 — Install Dependencies 📦
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4 — Ignite the Server 🔥
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Boom! 💥 The server will auto-create all database tables and serve the frontend at `http://localhost:8000`. API Docs are waiting for you at `http://localhost:8000/api/docs`.

---

## 👑 Claiming Your Admin Crown
All new users start as standard players. Want the keys to the kingdom? Run this quick SQL command:

```bash
psql -U postgres -d college_cp
```
```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
\q
```
*(Mac/Homebrew users: use your Mac username instead of `postgres`!)*

---

## 🔐 Security Overview
Codeforza takes security seriously:
- **No Plaintext**: Passwords are mathematically crushed by `bcrypt`.
- **JWT Protection**: Invalid tokens are instantly rejected (401 Unauthorized).
- **Backend Guards**: The Admin API routes are protected *server-side* by FastAPI dependencies. You can't fake being an admin.
- **Hidden Tests**: Test cases are judged in the dark. Inputs/outputs are *never* leaked to the browser.
- **Rate Limiting**: Brute-force attacks are stopped in their tracks.

---

## 🔮 What's Next on the Roadmap?
- [x] **Leaderboard** — Global rankings are LIVE! 🏆
- [ ] **Contests** — High-stakes, timed coding battles. ⏱️
- [ ] **Domain Restriction** — Exclusive access (e.g., `@nitc.ac.in` only). 🎓
- [ ] **Player Profiles** — Show off your avatar, bio, and stats! 🧑‍💻
- [ ] **Announcements** — Admin-curated news and problem editorials. 📰
- [ ] **Dockerized Judge** — Containerized, ultra-secure code execution for the big leagues. 🐳

---
*Built for the competitive spirit. Happy Coding!* 🎉
