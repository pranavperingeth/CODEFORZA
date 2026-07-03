# 🏆 College CP — Competitive Programming Platform

A full-featured, Codeforces-like competitive programming platform built for colleges. Write and run code directly in the browser using a VS Code-style editor, solve problems, compete with peers, and manage everything from an admin panel.

---

## 📸 What You Get

| Page | Description |
|---|---|
| **Login / Register** | Secure auth with bcrypt-hashed passwords + JWT tokens |
| **Dashboard** | Problem list with difficulty badges, search, and your submission history |
| **Problem Page** | Side-by-side problem statement + Monaco Editor (VS Code-style) with Run & Submit |
| **Admin Panel** | Add problems with test cases, manage users, promote/deactivate accounts |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | **FastAPI** (Python) |
| Database ORM | **SQLAlchemy 2.0** |
| Database | **PostgreSQL** |
| Password hashing | **bcrypt** (12 rounds, salted) |
| Authentication | **JWT** (HS256) via `python-jose` |
| Rate limiting | **slowapi** |
| Schema validation | **Pydantic v2** |
| Code execution | **subprocess** + temp directories |
| Frontend | Vanilla **HTML / CSS / JS** |
| Code editor | **Monaco Editor** (VS Code engine, via CDN) |
| Fonts | Inter (UI) + JetBrains Mono (code) via Google Fonts |

---

## 📁 Project Structure

```
college-cp/
│
├── README.md
│
├── backend/
│   ├── requirements.txt        ← all Python dependencies
│   ├── .env                    ← your secrets (DB URL, JWT key) — never commit this
│   ├── .env.example            ← template for .env
│   ├── .gitignore
│   │
│   └── app/
│       ├── __init__.py
│       │
│       ├── main.py             ← FastAPI app: middleware, routers, static serving
│       ├── database.py         ← SQLAlchemy engine + get_db() dependency
│       ├── models.py           ← ORM table definitions (users, problems, test_cases, submissions)
│       ├── schemas.py          ← Pydantic v2 request/response schemas + validation
│       ├── auth.py             ← bcrypt hashing + JWT create/decode
│       ├── dependencies.py     ← get_current_user + require_admin FastAPI deps
│       ├── executor.py         ← sandboxed code runner (Python, C++, C, Java)
│       │
│       └── routers/
│           ├── __init__.py
│           ├── auth_router.py      ← POST /api/auth/register, login, GET /me
│           ├── users_router.py     ← GET/PUT/DELETE /api/users/* (admin only)
│           ├── problems_router.py  ← GET/POST/DELETE /api/problems/*
│           └── judge_router.py     ← POST /api/judge/run, /submit, GET /submissions
│
└── frontend/
    ├── index.html       ← Login page
    ├── register.html    ← Registration page
    ├── dashboard.html   ← Problem list + submission history
    ├── problem.html     ← Problem detail + Monaco Editor
    ├── admin.html       ← Admin panel (server-side protected)
    ├── styles.css       ← Full dark-theme design system
    └── app.js           ← Shared JS: auth helpers, apiFetch, toasts, formatters
```

---

## ⚙️ Setup & Running Locally

### Step 1 — Install PostgreSQL

Make sure PostgreSQL is installed and running. Then create the database:

```bash
psql -U postgres
```
```sql
CREATE DATABASE college_cp;
\q
```

### Step 2 — Configure environment variables

```bash
cd backend
cp .env.example .env
```

Open `.env` and fill in your PostgreSQL password:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/college_cp
SECRET_KEY=bfd0f8d612a72748107d4a905e02d5b6fb6b4fe82afb0063dfe3b00c8a64a78d
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> The `SECRET_KEY` above is pre-generated. You can regenerate one any time with:
> ```bash
> python3 -c "import secrets; print(secrets.token_hex(32))"
> ```

### Step 3 — Install Python dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4 — Run the server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will:
- Automatically **create all database tables** on first startup
- Serve the **frontend** at `http://localhost:8000`
- Serve **API docs** at `http://localhost:8000/api/docs`

### Step 5 — Open in browser

```
http://localhost:8000          ← Login page
http://localhost:8000/api/docs ← Swagger UI (interactive API explorer)
```

---

## 👑 Making Yourself an Admin

All new registrations default to the `user` role. To become an admin, run this SQL after registering:

```bash
psql -U postgres -d college_cp
```
```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';

-- Verify it worked:
SELECT username, email, role FROM users;

\q
```

Once you're an admin:
- The **Admin** link appears in the navbar automatically
- You can promote other users to admin from the Admin Panel UI
- No more SQL needed after that

---

## 🧑‍💻 Online Judge — Supported Languages

The judge runs code using system-installed compilers in isolated temp directories.

| Language | Command used | Install on macOS |
|---|---|---|
| **Python 3** | `python3` | Pre-installed |
| **C++ 17** | `g++ -O2 -std=c++17` | `xcode-select --install` or `brew install gcc` |
| **C** | `gcc -O2` | Same as C++ |
| **Java** | `javac` + `java` | Download JDK from [adoptium.net](https://adoptium.net) |

**Verdicts:**

| Verdict | Meaning |
|---|---|
| `AC` | Accepted — all test cases passed ✅ |
| `WA` | Wrong Answer — output didn't match |
| `TLE` | Time Limit Exceeded |
| `RE` | Runtime Error — program crashed |
| `CE` | Compilation Error — code didn't compile |

**Run vs Submit:**
- **Run** (▶ button) — runs your code with your own custom input. No test cases. Good for testing logic.
- **Submit** (⬆ button) — runs your code against all hidden test cases. Returns verdict only — test case inputs/outputs are never revealed.

---

## 🔌 API Reference

All API routes are prefixed with `/api/`. Protected routes require `Authorization: Bearer <token>` header.

### Auth — `/api/auth/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/register` | None | Create new account (rate limited: 10/min) |
| `POST` | `/api/auth/login` | None | Login, get JWT token (rate limited: 5/min) |
| `GET` | `/api/auth/me` | User | Get your own profile |

**Login response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "username": "pranav",
    "email": "pranav@college.edu",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-07-03T..."
  }
}
```

### Problems — `/api/problems/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/problems/` | User | List all problems (sorted by difficulty) |
| `POST` | `/api/problems/` | **Admin** | Create a problem with test cases |
| `GET` | `/api/problems/{id}` | User | Problem detail + sample test cases only |
| `DELETE` | `/api/problems/{id}` | **Admin** | Delete problem + all its test cases |
| `POST` | `/api/problems/{id}/test-cases` | **Admin** | Add a test case to existing problem |

### Judge — `/api/judge/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/judge/run` | User | Run code with custom stdin (playground) |
| `POST` | `/api/judge/submit` | User | Submit code against all test cases |
| `GET` | `/api/judge/submissions` | User | Your last 50 submissions |
| `GET` | `/api/judge/submissions/{id}` | User | Single submission detail |

### Users — `/api/users/` (Admin only)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/users/` | **Admin** | List all users |
| `GET` | `/api/users/{id}` | **Admin** | Get single user |
| `PUT` | `/api/users/{id}/role` | **Admin** | Change user role (`user` or `admin`) |
| `DELETE` | `/api/users/{id}` | **Admin** | Deactivate a user (soft delete) |

---

## 🔐 Security Overview

### What's protected and how

| Concern | How it's handled |
|---|---|
| **Passwords** | Hashed with **bcrypt (12 rounds)** — never stored plaintext. Even if the DB is stolen, hashes can't be reversed quickly |
| **JWT tokens** | Signed with HS256. Contain user ID, username, role, and expiry. Invalid/expired tokens → 401 |
| **Admin API routes** | `require_admin` dependency runs **server-side** — even a forged client-side token can't bypass the server check |
| **Admin page HTML** | `/admin.html` is served **only if the request has a valid admin JWT** — the HTML never reaches non-admins |
| **SQL injection** | SQLAlchemy ORM uses **parameterized queries** everywhere — no raw SQL |
| **Hidden test cases** | Test case inputs/outputs are **never sent to the browser** — only the verdict |
| **Username enumeration** | Login returns the same error whether the username exists or not |
| **Rate limiting** | Login: **5/min** per IP. Register: **10/min** per IP |
| **Self-protection** | Admins cannot demote or deactivate their own account |
| **CORS** | Locked to `localhost:8000` in dev |

### What passwords look like in the database

```
User types: "MyPassword123"
Stored in DB: "$2b$12$K8HKnZ7y3YyTqNzXmP8..."   ← bcrypt hash, irreversible
```

The original password is discarded immediately. No page, no API, no admin view ever exposes passwords.

### Known risks for local/college use (acceptable for now)

| Risk | Impact | Production fix |
|---|---|---|
| JWT in `localStorage` | XSS could steal token | Use `httpOnly` cookies |
| Code executor on host machine | Malicious code runs on your laptop | Wrap each run in a Docker container |
| No HTTPS | Token visible on network | Put nginx/Caddy with TLS in front |

> **For a college LAN with trusted users, the current setup is solid.** These risks become critical only if you open it to the public internet.

---

## 🗃️ Database Schema

### `users`
| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `username` | VARCHAR(50) | Unique, indexed |
| `email` | VARCHAR(255) | Unique, indexed |
| `hashed_password` | TEXT | bcrypt hash only |
| `role` | ENUM | `user` or `admin` |
| `is_active` | BOOLEAN | Soft-delete flag |
| `created_at` | TIMESTAMP | Auto set by DB |

### `problems`
| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `title` | VARCHAR(200) | |
| `statement` | TEXT | Problem description |
| `input_format` | TEXT | Optional |
| `output_format` | TEXT | Optional |
| `constraints` | TEXT | Optional |
| `difficulty` | INTEGER | 800–3500 (Codeforces scale) |
| `time_limit` | FLOAT | Seconds (default 2.0) |
| `memory_limit` | INTEGER | MB (default 256) |
| `created_by` | UUID (FK) | References `users.id` |

### `test_cases`
| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `problem_id` | UUID (FK) | CASCADE delete |
| `input_data` | TEXT | Input for the test |
| `expected_output` | TEXT | Expected stdout |
| `is_sample` | BOOLEAN | `true` = shown to users |

### `submissions`
| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID (FK) | |
| `problem_id` | UUID (FK) | Nullable (playground runs) |
| `language` | VARCHAR(20) | `python`, `cpp`, `c`, `java` |
| `code` | TEXT | Submitted code |
| `status` | VARCHAR(50) | `AC`, `WA`, `TLE`, `RE`, `CE` |
| `stderr` | TEXT | Compiler/runtime errors |
| `execution_time` | FLOAT | Wall-clock seconds |
| `created_at` | TIMESTAMP | |

---

## 🚀 Production Checklist

Before exposing this to the internet:

- [ ] **Change `SECRET_KEY`** — generate a fresh one: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- [ ] **Set `ACCESS_TOKEN_EXPIRE_MINUTES`** to 15–30 (shorter = safer)
- [ ] **HTTPS** — put nginx or Caddy in front with a TLS certificate
- [ ] **Update CORS** — change `allow_origins` in `main.py` to your actual domain
- [ ] **Docker the executor** — wrap each code execution in an isolated container
- [ ] **Set up Alembic** — for safe database schema migrations
- [ ] **Use gunicorn** — `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
- [ ] **Secure your `.env`** — use environment secrets (Railway, Render, etc.) instead of a file
- [ ] **Backup the database** — set up regular PostgreSQL dumps

---

## 🐛 Common Issues

**`password authentication failed for user "postgres"`**
→ Wrong password in `DATABASE_URL` in your `.env` file.

**`database "college_cp" does not exist`**
→ Run: `psql -U postgres -c "CREATE DATABASE college_cp;"`

**`command not found: g++` when running C++ code**
→ Install Xcode tools: `xcode-select --install`

**Monaco Editor not loading**
→ You need an internet connection — it loads from a CDN. Check your network.

**Admin link not showing in navbar**
→ You haven't been promoted to admin yet. Run the SQL UPDATE shown above.

**`RateLimitExceeded` on login**
→ You hit 5 login attempts/minute. Wait 60 seconds and try again.

---

## 💡 What to Build Next

- [ ] **Contests** — timed contests with scoreboards
- [ ] **Leaderboard** — global rankings by accepted problems
- [ ] **Problem tags** — filter by topic (graphs, dp, greedy, etc.)
- [ ] **Editorial** — admin can attach a solution explanation per problem
- [ ] **Multiple test file upload** — bulk import test cases via `.zip`
- [ ] **Checker support** — for problems with multiple valid outputs
- [ ] **Email verification** — on registration
- [ ] **Docker judge** — isolated, secure code execution for production
