"""burner-radar-data: a disposable email domain blocklist with a tiny API.

    >>> from burner_radar_data import is_disposable, get_service
    >>> is_disposable("foo@mailinator.com")
    True
    >>> get_service("foo@mailinator.com")
    'mailinator'
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources

__version__ = "0.1.0"

__all__ = [
    "is_disposable",
    "get_service",
    "domains",
    "services",
    "data_generated_at",
    "__version__",
]


def _extract_domain(email_or_domain: str) -> str:
    s = email_or_domain.strip().lower()
    if "@" in s:
        s = s.rsplit("@", 1)[-1]
    return s.lstrip(".").rstrip(".")


@lru_cache(maxsize=1)
def _domains() -> frozenset[str]:
    text = resources.files(__name__).joinpath("data/domains.txt").read_text(encoding="utf-8")
    return frozenset(line for line in text.splitlines() if line)


@lru_cache(maxsize=1)
def _services_payload() -> dict:
    text = resources.files(__name__).joinpath("data/services.json").read_text(encoding="utf-8")
    return json.loads(text)


@lru_cache(maxsize=1)
def _domain_to_service() -> dict[str, str]:
    payload = _services_payload()
    mapping: dict[str, str] = {}
    for entry in payload.get("services", []):
        svc = entry["service"]
        for d in entry.get("domains", []):
            mapping[d] = svc
    return mapping


def is_disposable(email_or_domain: str) -> bool:
    """Return True if the domain part is a known disposable email domain."""
    return _extract_domain(email_or_domain) in _domains()


def get_service(email_or_domain: str) -> str | None:
    """Return the parent burner service for this domain, or None if unknown.

    A return of None does NOT mean the domain is legit. It only means we have
    no MX-fingerprint match for a known service. Use is_disposable for the
    blocklist check.
    """
    return _domain_to_service().get(_extract_domain(email_or_domain))


def domains() -> frozenset[str]:
    """The full set of disposable domains in this release."""
    return _domains()


def services() -> dict[str, list[str]]:
    """{service_name: [frontend_domains]} for all classified services."""
    return {
        entry["service"]: list(entry["domains"])
        for entry in _services_payload().get("services", [])
    }


def data_generated_at() -> str:
    """ISO-8601 timestamp of when the bundled dataset was generated."""
    return _services_payload().get("generated_at", "")
