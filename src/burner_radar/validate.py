"""MX-based liveness validation and burner-service fingerprinting."""

from __future__ import annotations

import concurrent.futures
import re
from typing import Iterable

import dns.exception
import dns.resolver

_DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")


def normalize(domain: str) -> str | None:
    d = domain.strip().lower().lstrip(".")
    if not d or d.startswith("#"):
        return None
    if "@" in d:
        d = d.rsplit("@", 1)[-1]
    if not _DOMAIN_RE.match(d):
        return None
    return d


def mx_for(domain: str, timeout: float = 4.0) -> list[str]:
    """Return MX hostnames for a domain, lowercased and dot-stripped.

    Empty list means no MX (domain cannot receive mail). Resolution errors
    return an empty list as well; callers can re-probe later.
    """
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout
    resolver.timeout = timeout
    try:
        answers = resolver.resolve(domain, "MX")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers,
            dns.exception.Timeout, dns.resolver.LifetimeTimeout):
        return []
    except Exception:
        return []
    return sorted({str(r.exchange).rstrip(".").lower() for r in answers})


def probe_many(domains: Iterable[str], workers: int = 32) -> dict[str, list[str]]:
    """Concurrent MX probe. Returns {domain: [mx_hosts]}."""
    domains = list(domains)
    result: dict[str, list[str]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(mx_for, d): d for d in domains}
        for f in concurrent.futures.as_completed(futures):
            result[futures[f]] = f.result()
    return result
