# burner-radar

A continuously-updated database of disposable / temporary / burner email domains, with a collection pipeline that actually keeps itself fresh.

Existing community lists rot. Mailinator alone rotates through hundreds of frontend domains, Temp-Mail and DropMail publish new ones weekly, and the popular `disposable-email-domains` GitHub lists rely on manual PRs that fall months behind. `burner-radar` rebuilds its list on a schedule from public signals (community lists, MX-record fingerprinting of known burner services, liveness probes) and ships a clean dataset every day.

## What you get

- `data/domains.txt`: one domain per line, sorted, ready to drop into any signup-form blocklist
- `data/domains.json`: same domains with metadata (first seen, last seen alive, sources, parent service, confidence)
- `data/services.json`: each known burner service grouped with every frontend domain we have linked to it via MX fingerprinting
- A GitHub Actions workflow that rebuilds all three daily

## Why it exists

Every product with a signup form fights the same battle: free-trial abuse, fake accounts, skewed activation funnels, and forum spam, all riding on disposable email addresses. Paid services (Kickbox, ZeroBounce) charge per check. Free lists are stale. This project sits in the middle: a free, automated, transparent dataset that anyone can vendor or query.

## Use it

Drop the list into your signup validation:

```python
disposable = set(open("data/domains.txt").read().splitlines())

def is_disposable(email: str) -> bool:
    domain = email.rsplit("@", 1)[-1].lower().strip()
    return domain in disposable
```

Or pull it straight from GitHub:

```bash
curl -sSL https://raw.githubusercontent.com/manavdoshi-dev/burner-radar/main/data/domains.txt
```

## How it works

The collector runs three passes:

1. **Community ingest.** Pulls from a curated set of existing disposable-email lists on GitHub, merges them, and treats each list as a low-weight signal.
2. **Seed expansion.** A hand-maintained list of known burner services (Mailinator, Guerrilla Mail, Temp-Mail, YOPmail, and so on) anchors the dataset. Their MX records are recorded and used as fingerprints.
3. **Liveness check.** Every candidate domain gets an MX lookup. Domains with no MX are dropped.
4. **MX fingerprinting.** Each seed service contributes an MX signature (the registrable domain of its mail servers). Any candidate whose MX signature matches a known service is labelled as a frontend for that service. The current build links over 2,000 community-listed domains to a parent service this way, including 1,249 Temp-Mail rotations and 225 Mailinator frontends that the upstream community lists do not tag.

Each domain ends up with a confidence score based on how many independent signals agreed (sources, live MX, fingerprint match).

## Roadmap

- Passive-DNS-based discovery of new domains sharing MX records with known burner services
- Certificate Transparency log monitoring for new domains matching burner naming patterns
- A free public API with rate limiting
- A tiny npm and pip package wrapping the data with a local cache

## License

MIT. The data is gathered from public sources and is provided as-is.
