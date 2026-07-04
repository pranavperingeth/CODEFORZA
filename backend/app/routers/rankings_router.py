"""
routers/rankings_router.py — Global leaderboard / ranking endpoint.

Ranking formula:
  total_score = sum(difficulty) of each uniquely solved problem (status = 'AC')
  Tie-break: user whose latest AC was earlier ranks higher.

All endpoints require a valid JWT (any role — user or admin).
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, case, distinct
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import LeaderboardEntry

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get(
    "/",
    response_model=List[LeaderboardEntry],
    summary="Get the global leaderboard",
)
def get_leaderboard(
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),  # JWT auth required
):
    """
    Compute the global leaderboard.

    For every active user, count the number of unique problems they've solved
    (status = 'AC') and sum the difficulty of those problems.

    Sorted by:
      1. total_score DESC  (higher score = higher rank)
      2. last_ac_at ASC    (earlier last solve = higher rank on tie)

    Users with zero solves are included at the bottom so everyone sees
    themselves on the board.
    """

    # ── Subquery: for each user, get the set of problem_ids with at least one AC ─
    # We join submissions → problems to grab the difficulty column.
    ac_sub = (
        db.query(
            models.Submission.user_id,
            models.Problem.id.label("problem_id"),
            models.Problem.difficulty.label("difficulty"),
            func.min(models.Submission.created_at).label("first_ac_at"),
        )
        .join(models.Problem, models.Submission.problem_id == models.Problem.id)
        .filter(
            models.Submission.status == "AC",
            models.Submission.problem_id.isnot(None),
        )
        .group_by(
            models.Submission.user_id,
            models.Problem.id,
            models.Problem.difficulty,
        )
        .subquery("ac_problems")
    )

    # ── Main query: aggregate per user ────────────────────────────────────────
    rankings_q = (
        db.query(
            models.User.id.label("user_id"),
            models.User.username.label("username"),
            func.coalesce(func.count(ac_sub.c.problem_id), 0).label("problems_solved"),
            func.coalesce(func.sum(ac_sub.c.difficulty), 0).label("total_score"),
            func.max(ac_sub.c.first_ac_at).label("last_ac_at"),
        )
        .outerjoin(ac_sub, models.User.id == ac_sub.c.user_id)
        .filter(models.User.is_active == True)  # noqa: E712 — SQLAlchemy needs ==
        .group_by(models.User.id, models.User.username)
        .order_by(
            func.coalesce(func.sum(ac_sub.c.difficulty), 0).desc(),  # highest score first
            func.max(ac_sub.c.first_ac_at).asc().nullslast(),        # earlier AC wins ties
        )
        .all()
    )

    # ── Build response with rank numbers ─────────────────────────────────────
    entries: List[LeaderboardEntry] = []
    for idx, row in enumerate(rankings_q, start=1):
        entries.append(
            LeaderboardEntry(
                rank=idx,
                user_id=row.user_id,
                username=row.username,
                problems_solved=row.problems_solved,
                total_score=row.total_score,
                last_ac_at=row.last_ac_at,
            )
        )

    return entries
