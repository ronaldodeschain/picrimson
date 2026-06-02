from datetime import datetime, timezone
from fastapi import Request


class LoginAttemptService:
    """Gerencia tentativas de login em sessão para limitar ataques de força bruta."""

    MAX_ATTEMPTS = 5
    BLOCK_SECONDS = 300
    SESSION_KEY = "login_attempts"

    def __init__(self, request: Request):
        self.request = request

    def _now_timestamp(self) -> int:
        return int(datetime.now(timezone.utc).timestamp())

    def _load_attempts(self) -> dict:
        attempts = self.request.session.get(self.SESSION_KEY, {})
        if not isinstance(attempts, dict):
            attempts = {}
        return attempts

    def _save_attempts(self, attempts: dict) -> None:
        self.request.session[self.SESSION_KEY] = attempts

    def get_attempt_info(self, email: str) -> dict:
        attempts = self._load_attempts()
        return attempts.get(email, {"count": 0, "blocked_until": 0})

    def is_blocked(self, email: str) -> bool:
        info = self.get_attempt_info(email)
        return info.get("blocked_until", 0) > self._now_timestamp()

    def blocked_seconds_left(self, email: str) -> int:
        info = self.get_attempt_info(email)
        blocked_until = info.get("blocked_until", 0)
        now = self._now_timestamp()
        return max(0, blocked_until - now)

    def remaining_attempts(self, email: str) -> int:
        info = self.get_attempt_info(email)
        if info.get("blocked_until", 0) > self._now_timestamp():
            return 0
        count = info.get("count", 0)
        return max(0, self.MAX_ATTEMPTS - count)

    def register_failure(self, email: str) -> None:
        attempts = self._load_attempts()
        info = attempts.get(email, {"count": 0, "blocked_until": 0})
        now = self._now_timestamp()

        if info.get("blocked_until", 0) > now:
            # Already blocked, keep the block in place.
            attempts[email] = info
            self._save_attempts(attempts)
            return

        count = info.get("count", 0) + 1
        blocked_until = info.get("blocked_until", 0)

        if count >= self.MAX_ATTEMPTS:
            blocked_until = now + self.BLOCK_SECONDS

        attempts[email] = {"count": count, "blocked_until": blocked_until}
        self._save_attempts(attempts)

    def reset_attempts(self, email: str) -> None:
        attempts = self._load_attempts()
        if email in attempts:
            del attempts[email]
            self._save_attempts(attempts)
