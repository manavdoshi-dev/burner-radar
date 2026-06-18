"""MX-signature fingerprinting of disposable email services.

A "signature" is the frozenset of MX hostnames (sometimes reduced to their
registrable domain, since services often shard across mxN.example.com).
Two domains with the same signature are almost certainly served by the same
backend, which means an unknown frontend domain can be classified as a
known service if its MX signature matches.
"""

from __future__ import annotations

from collections import defaultdict

from .seeds import SEED_SERVICES


def mx_signature(mx_hosts: list[str]) -> frozenset[str]:
    """Reduce MX hostnames to their last two labels (registrable domain).

    `mail.mailinator.com` and `mail2.mailinator.com` both collapse to
    `mailinator.com`, so a rotated frontend that points to either is still
    recognised as the same service.
    """
    reduced = set()
    for host in mx_hosts:
        parts = host.strip(".").lower().split(".")
        if len(parts) >= 2:
            reduced.add(".".join(parts[-2:]))
    return frozenset(reduced)


def build_signature_index(
    domain_mx: dict[str, list[str]],
) -> dict[frozenset[str], str]:
    """Build {mx_signature: service_label} from the seed services' live MX.

    Domains in `domain_mx` that are listed under SEED_SERVICES contribute
    their MX signature to the index, tagged with their service label.
    """
    index: dict[frozenset[str], str] = {}
    for service, domains in SEED_SERVICES.items():
        for d in domains:
            mx = domain_mx.get(d) or []
            if not mx:
                continue
            sig = mx_signature(mx)
            if sig and sig not in index:
                index[sig] = service
    return index


def classify(
    domain_mx: dict[str, list[str]],
    sig_index: dict[frozenset[str], str],
) -> dict[str, str]:
    """Return {domain: service_label} for every domain whose MX matches a known signature."""
    labels: dict[str, str] = {}
    for domain, mx in domain_mx.items():
        if not mx:
            continue
        sig = mx_signature(mx)
        if sig in sig_index:
            labels[domain] = sig_index[sig]
    return labels


def group_by_service(labels: dict[str, str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for domain, service in labels.items():
        groups[service].append(domain)
    return {svc: sorted(ds) for svc, ds in sorted(groups.items())}
