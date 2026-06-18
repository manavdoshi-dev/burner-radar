"""Top-level collection pipeline.

build() does, in order:
  1. Pull each community source, normalize each line/entry to a domain.
  2. Merge with the hardcoded seed list.
  3. MX-probe every candidate. Drop domains with no MX (cannot receive mail).
  4. Build an MX-signature index from seed services and classify every
     domain whose MX signature matches a known service.
  5. Score each domain by number of independent sources that agreed.
  6. Write data/domains.txt, data/domains.json, data/services.json.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import requests

from .fingerprint import build_signature_index, classify, group_by_service
from .seeds import SEED_DOMAINS
from .sources import SOURCES, Source
from .validate import normalize, probe_many


@dataclass
class DomainRecord:
    domain: str
    sources: set[str] = field(default_factory=set)
    mx: list[str] = field(default_factory=list)
    service: str | None = None
    first_seen: str = ""
    last_seen_alive: str = ""

    @property
    def confidence(self) -> float:
        # 0.5 floor for any single source. Each additional source adds 0.1.
        # Live MX adds 0.2. Service fingerprint match adds 0.2.
        score = 0.5 + 0.1 * max(0, len(self.sources) - 1)
        if self.mx:
            score += 0.2
        if self.service:
            score += 0.2
        return round(min(score, 1.0), 2)

    def to_json(self) -> dict:
        return {
            "domain": self.domain,
            "sources": sorted(self.sources),
            "mx": self.mx,
            "service": self.service,
            "first_seen": self.first_seen,
            "last_seen_alive": self.last_seen_alive,
            "confidence": self.confidence,
        }


def _fetch(source: Source, timeout: float = 30.0) -> list[str]:
    resp = requests.get(source.url, timeout=timeout, headers={"User-Agent": "burner-radar/0.1"})
    resp.raise_for_status()
    if source.fmt == "json_list":
        data = resp.json()
        if not isinstance(data, list):
            return []
        return [str(x) for x in data]
    return resp.text.splitlines()


def _load_existing(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {entry["domain"]: entry for entry in payload.get("domains", [])}


def build(data_dir: Path) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    json_path = data_dir / "domains.json"
    txt_path = data_dir / "domains.txt"
    services_path = data_dir / "services.json"

    previous = _load_existing(json_path)
    records: dict[str, DomainRecord] = {}

    def record_for(domain: str) -> DomainRecord:
        if domain not in records:
            prev = previous.get(domain, {})
            records[domain] = DomainRecord(
                domain=domain,
                first_seen=prev.get("first_seen", now),
                last_seen_alive=prev.get("last_seen_alive", ""),
            )
        return records[domain]

    source_counts: dict[str, int] = defaultdict(int)

    for src in SOURCES:
        try:
            raw_entries = _fetch(src)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] source {src.name} failed: {exc}")
            continue
        added = 0
        for raw in raw_entries:
            d = normalize(raw)
            if d is None:
                continue
            record_for(d).sources.add(src.name)
            added += 1
        source_counts[src.name] = added
        print(f"[ok]   {src.name}: {added} entries")

    for raw in SEED_DOMAINS:
        d = normalize(raw)
        if d is None:
            continue
        record_for(d).sources.add("burner-radar/seeds")

    print(f"[info] {len(records)} unique candidates before MX probe")

    mx_results = probe_many(records.keys())
    alive = 0
    for domain, mx in mx_results.items():
        rec = records[domain]
        rec.mx = mx
        if mx:
            rec.last_seen_alive = now
            alive += 1

    sig_index = build_signature_index(mx_results)
    print(f"[info] built signature index from {len(sig_index)} known services")
    labels = classify(mx_results, sig_index)
    for domain, service in labels.items():
        records[domain].service = service
    print(f"[info] classified {len(labels)} domains via MX fingerprinting")

    final = {d: r for d, r in records.items() if r.mx or "burner-radar/seeds" in r.sources}
    print(f"[info] keeping {len(final)} domains after liveness filter ({alive} with live MX)")

    sorted_domains = sorted(final.keys())
    txt_path.write_text("\n".join(sorted_domains) + "\n", encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(sorted_domains),
        "source_counts": dict(source_counts),
        "classified_count": len(labels),
        "domains": [final[d].to_json() for d in sorted_domains],
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=False), encoding="utf-8")

    groups = group_by_service({d: r.service for d, r in final.items() if r.service})
    services_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "services": [
            {"service": svc, "domain_count": len(domains), "domains": domains}
            for svc, domains in groups.items()
        ],
    }
    services_path.write_text(json.dumps(services_payload, indent=2), encoding="utf-8")

    return {"count": len(sorted_domains), "alive": alive, "classified": len(labels)}
