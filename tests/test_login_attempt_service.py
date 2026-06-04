"""Testes do serviço de tentativa de login.

Cobertura:
    - registra falhas de login e incrementa contagem
    - bloqueia após número máximo de tentativas
    - zera contador após login bem-sucedido
    - calcula corretamente tentativas restantes
"""

import time
from typing import Any, cast

from app.services.login_attempt_service import LoginAttemptService


class DummyRequest:
    def __init__(self):
        self.session = {}


def test_login_attempts_increment_and_block_after_maximum():
    """CT-007: bloqueio deve ocorrer depois de várias tentativas falhas."""
    request = cast(Any, DummyRequest())
    service = LoginAttemptService(request)
    email = "usuario@example.com"

    # Simula falhas de login até a última tentativa permitida
    for attempt in range(LoginAttemptService.MAX_ATTEMPTS - 1):
        assert not service.is_blocked(email)
        service.register_failure(email)
        info = service.get_attempt_info(email)
        assert info["count"] == attempt + 1
        assert info["blocked_until"] == 0

    service.register_failure(email)
    assert service.is_blocked(email)
    info = service.get_attempt_info(email)
    assert info["count"] == LoginAttemptService.MAX_ATTEMPTS
    assert info["blocked_until"] > 0


def test_login_attempts_reset_on_successful_login():
    """Após login bem-sucedido, as tentativas devem ser zeradas."""
    request = cast(Any, DummyRequest())
    service = LoginAttemptService(request)
    email = "usuario@example.com"

    service.register_failure(email)
    service.register_failure(email)
    assert service.get_attempt_info(email)["count"] == 2

    service.reset_attempts(email)
    assert service.get_attempt_info(email)["count"] == 0
    assert service.get_attempt_info(email)["blocked_until"] == 0


def test_block_duration_is_applied_and_expires():
    """O bloqueio temporário deve expirar ao passar o intervalo definido."""
    request = cast(Any, DummyRequest())
    service = LoginAttemptService(request)
    email = "usuario@example.com"

    for _ in range(LoginAttemptService.MAX_ATTEMPTS):
        service.register_failure(email)

    assert service.is_blocked(email)
    remaining = service.blocked_seconds_left(email)
    assert remaining > 0

    # Simula a passagem do tempo para liberar o bloqueio.
    service.request.session[LoginAttemptService.SESSION_KEY][email]["blocked_until"] = int(time.time()) - 1
    assert not service.is_blocked(email)
    assert service.blocked_seconds_left(email) == 0


def test_remaining_attempts_decreases_with_failures():
    """A contagem de tentativas restantes deve diminuir após cada falha."""
    request = cast(Any, DummyRequest())
    service = LoginAttemptService(request)
    email = "usuario@example.com"

    assert service.remaining_attempts(email) == LoginAttemptService.MAX_ATTEMPTS
    service.register_failure(email)
    assert service.remaining_attempts(email) == LoginAttemptService.MAX_ATTEMPTS - 1
    for _ in range(LoginAttemptService.MAX_ATTEMPTS - 1):
        service.register_failure(email)
    assert service.remaining_attempts(email) == 0
    assert service.is_blocked(email)
