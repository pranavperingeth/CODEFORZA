"""
schemas.py — Pydantic v2 request/response schemas.

Organized by domain:
  - Auth      : UserCreate, Token, TokenData
  - Users     : UserOut, RoleUpdate
  - Problems  : ProblemCreate, ProblemListOut, ProblemDetailOut, TestCaseCreate/Out
  - Judge     : RunRequest, SubmitRequest, RunResult, SubmissionOut
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


# ── Enums ────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


# ── Auth / User schemas ───────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be 3–50 characters")
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not all(c in allowed for c in v):
            raise ValueError("Username may only contain letters, digits, or underscores")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenData(BaseModel):
    user_id: str
    username: str
    role: str


class RoleUpdate(BaseModel):
    role: UserRole


# ── Problem / TestCase schemas ────────────────────────────────────────────────

class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    is_sample: bool = False


class TestCaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    input_data: str
    expected_output: str
    is_sample: bool


class ProblemCreate(BaseModel):
    title: str
    statement: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    difficulty: int = 800
    time_limit: float = 2.0
    memory_limit: int = 256
    test_cases: List[TestCaseCreate] = []

    @field_validator("difficulty")
    @classmethod
    def difficulty_range(cls, v: int) -> int:
        if not (800 <= v <= 3500):
            raise ValueError("Difficulty must be between 800 and 3500")
        return v

    @field_validator("time_limit")
    @classmethod
    def time_limit_range(cls, v: float) -> float:
        if not (0.5 <= v <= 10.0):
            raise ValueError("Time limit must be between 0.5 and 10 seconds")
        return v


class ProblemListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    difficulty: int
    time_limit: float
    memory_limit: int
    created_at: datetime


class ProblemDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    statement: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    difficulty: int
    time_limit: float
    memory_limit: int
    created_at: datetime
    # Populated manually in the router — only sample test cases exposed
    sample_test_cases: List[TestCaseOut] = []


# ── Judge schemas ─────────────────────────────────────────────────────────────

class RunRequest(BaseModel):
    """Run code without test cases (playground mode)."""
    language: str
    code: str
    stdin: str = ""

    @field_validator("language")
    @classmethod
    def lang_supported(cls, v: str) -> str:
        supported = {"python", "cpp", "c", "java"}
        if v not in supported:
            raise ValueError(f"Language must be one of: {', '.join(supported)}")
        return v

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Code cannot be empty")
        if len(v) > 65536:
            raise ValueError("Code exceeds 64 KB limit")
        return v


class SubmitRequest(BaseModel):
    """Submit code for judging against a problem's test cases."""
    problem_id: UUID
    language: str
    code: str

    @field_validator("language")
    @classmethod
    def lang_supported(cls, v: str) -> str:
        supported = {"python", "cpp", "c", "java"}
        if v not in supported:
            raise ValueError(f"Language must be one of: {', '.join(supported)}")
        return v


class RunResult(BaseModel):
    status: str           # OK | TLE | RE | CE
    stdout: str
    stderr: str
    execution_time: float


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    language: str
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    execution_time: Optional[float] = None
    created_at: datetime
    problem_id: Optional[UUID] = None


# ── Rankings schemas ──────────────────────────────────────────────────────────

class LeaderboardEntry(BaseModel):
    """One row on the leaderboard."""
    rank: int
    user_id: UUID
    username: str
    problems_solved: int          # number of unique problems with AC
    total_score: int              # sum of difficulty of each uniquely solved problem
    last_ac_at: Optional[datetime] = None  # tie-break: earlier = better
