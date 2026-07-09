# 🏆 Codeforza — Competitive Programming Platform

A full-featured, competitive programming platform built for colleges. Write and run code directly in the browser using a VS Code-style editor, solve problems, compete with peers, and manage everything from an admin panel.

---

## 📸 Platform Overview

| Page | Description |
|---|---|
| **Login / Register** | Secure auth with bcrypt-hashed passwords + JWT tokens. |
| **Dashboard** | Problem list with difficulty badges, search, and your submission history. |
| **Problem Page** | Side-by-side problem statement + Monaco Editor (VS Code-style) with Run & Submit. |
| **Leaderboard** | Global ranking of all users based on unique problems solved. |
| **Admin Panel** | Add problems with test cases, manage users, promote/deactivate accounts. |

---

## 🛠️ Architecture & Tech Stack

Codeforza is designed with a clear separation of concerns, utilizing modern technologies for both the frontend and backend.

### Frontend Design Analysis
The frontend has been overhauled to prioritize visual excellence, responsiveness, and maintainability.
- **Tailwind CSS**: The UI is powered by Tailwind CSS (via CDN), allowing for rapid prototyping and a highly consistent, utility-first design system. This eliminates massive custom CSS files and ensures a unified design language.
- **Typography & Icons**: Uses Google Fonts (`Inter` for UI readability, `Hanken Grotesk` for headings, and `JetBrains Mono` for code) alongside Material Symbols for a sleek, modern aesthetic.
- **Component Consistency**: The design emphasizes structured spacing (`gap-md`, `p-xl`), subtle micro-animations (`transition-all`, hover states), and a clean card-based layout (`bg-surface-container`, shadow depths).
- **Code Editor**: Integrated with **Monaco Editor** (the engine behind VS Code) for a professional-grade coding experience right in the browser.

### Backend Design Analysis
The backend is built for speed, security, and scalability.
- **FastAPI (Python)**: Provides extremely fast execution, automatic OpenAPI documentation, and asynchronous capabilities.
- **SQLAlchemy 2.0 & PostgreSQL**: A robust relational database setup. The ORM ensures safe parameterized queries (preventing SQL injection), while PostgreSQL handles complex joins efficiently (e.g., for calculating Leaderboard rankings on the fly).
- **Security & Authentication**:
  - Passwords are never stored in plaintext (hashed using `bcrypt` with 12 rounds).
  - Stateless authentication using `JWT` (HS256).
  - Rate limiting via `slowapi` prevents brute-force login attempts and registration spam.
- **Code Execution Engine**: Sandboxed execution using Python's `subprocess` running in isolated temporary directories. Supports Python 3, C++ 17, C, and Java.

---

## 📁 Project Structure

```
college-cp/
│
├── README.md
│
├── backend/
│   ├── requirements.txt        ← Python dependencies
│   ├── .env                    ← Secrets (DB URL, JWT key) — never commit this
│   └── app/
│       ├── main.py             ← FastAPI app: middleware, routers, static serving
│       ├── database.py         ← SQLAlchemy engine + get_db() dependency
│       ├── models.py           ← ORM tables (users, problems, test_cases, submissions)
│       ├── schemas.py          ← Pydantic validation schemas
│       ├── auth.py             ← bcrypt hashing + JWT create/decode
│       ├── dependencies.py     ← get_current_user + require_admin guards
│       ├── executor.py         ← Sandboxed code runner
│       └── routers/
│           ├── auth_router.py      ← Auth endpoints
│           ├── users_router.py     ← Admin user management
│           ├── problems_router.py  ← Problem CRUD
│           ├── judge_router.py     ← Code execution and submissions
│           └── rankings_router.py  ← Global leaderboard calculation
│
└── frontend/
    ├── index.html       ← Login page (Tailwind)
    ├── register.html    ← Registration page (Tailwind)
    ├── dashboard.html   ← Problem list (Tailwind)
    ├── problem.html     ← Problem detail + Editor (Tailwind)
    ├── admin.html       ← Admin panel (Tailwind)
    ├── leaderboard.html ← Leaderboard ranking page
    └── app.js           ← Shared JS logic (API fetching, auth state)
```

---

## ⚙️ Setup & Running Locally

### Step 1 — Install PostgreSQL

Make sure PostgreSQL is installed and running. Then create the database:

```bash
psql -U postgres -c "CREATE DATABASE college_cp;"
```

### Step 2 — Configure environment variables

```bash
cd backend
cp .env.example .env
```

Open `.env` and configure your credentials:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/college_cp
SECRET_KEY=bfd0f8d612a72748107d4a905e02d5b6fb6b4fe82afb0063dfe3b00c8a64a78d
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 3 — Install Python dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4 — Run the server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5 — Open in browser
Visit `http://localhost:8000` to see the app.
API Docs available at `http://localhost:8000/api/docs`.

---

## 👑 Making Yourself an Admin

All new registrations default to the `user` role. Run this SQL to promote yourself:

```bash
psql -U postgres -d college_cp
```
```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
\q
```
*Note: If using macOS with Homebrew Postgres, use your Mac username instead of `postgres`.*

---

## 🔐 Security Overview

- **Passwords**: Hashed with bcrypt (12 rounds).
- **JWT tokens**: Signed with HS256. Invalid/expired tokens result in 401 Unauthorized.
- **Admin API routes**: Protected server-side via FastAPI dependencies.
- **Admin page HTML**: `/admin.html` is served only if the request has a valid admin JWT.
- **Hidden test cases**: Test inputs/outputs are never sent to the browser.
- **Rate limiting**: Login (5/min), Register (10/min) per IP.

---

## 💡 What to Build Next

- [x] **Leaderboard** — Global rankings by accepted problems.
- [ ] **Contests** — Timed contests with specific problem sets.
- [ ] **Domain Restriction** — Restrict registration to `@nitc.ac.in` emails only.
- [ ] **Profiles** — User profiles with avatars and bios.
- [ ] **Posts/Announcements** — Admin-created news and problem editorials.
- [ ] **Docker Judge** — Isolated, secure code execution for production deployment.
