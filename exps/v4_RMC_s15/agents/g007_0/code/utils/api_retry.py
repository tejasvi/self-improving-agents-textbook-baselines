"""Retry helpers with exponential backoff for transient LLM API failures."""
import functools
import random
import time

import anthropic
import openai

# Exceptions that are always considered transient.
_TRANSIENT_EXC_TYPES = (
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.APIConnectionError,
    openai.InternalServerError,
    anthropic.RateLimitError,
    anthropic.APITimeoutError,
    anthropic.APIConnectionError,
    anthropic.InternalServerError,
    anthropic.OverloadedError,
)

# HTTP status codes that indicate a transient condition.
_TRANSIENT_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504, 529}


def is_transient_error(exc):
    """Return True if the exception looks like a transient API failure."""
    if isinstance(exc, _TRANSIENT_EXC_TYPES):
        return True
    status = getattr(exc, "status_code", None)
    return isinstance(status, int) and status in _TRANSIENT_STATUS_CODES


def compute_backoff(attempt, base_delay, max_delay):
    """Exponential backoff delay (attempt is 0-based) with +/-25% jitter."""
    delay = min(max_delay, base_delay * (2 ** attempt))
    return delay * random.uniform(0.75, 1.25)


def retry_api_call(max_retries=5, base_delay=2.0, max_delay=60.0, logging=print):
    """Decorator retrying the wrapped LLM call on transient errors only.

    Makes at most `max_retries + 1` attempts using a bounded loop; non-transient
    errors are raised immediately.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if not is_transient_error(e) or attempt == max_retries:
                        raise
                    last_exc = e
                    delay = compute_backoff(attempt, base_delay, max_delay)
                    logging(
                        f"Transient API error in {fn.__name__} "
                        f"(attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {delay:.1f}s."
                    )
                    time.sleep(delay)
            raise last_exc  # pragma: no cover - loop always returns or raises
        return wrapper
    return decorator
