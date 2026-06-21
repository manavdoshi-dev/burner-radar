# burner-radar-data

Disposable email domain blocklist with a tiny API. Bundled, offline, zero dependencies.

The dataset is rebuilt daily by the [burner-radar](https://github.com/manavdoshi-dev/burner-radar) pipeline from multiple community lists, MX-validated, and classified by parent service via MX fingerprinting.

## Install

```bash
pip install burner-radar-data
```

## Use

```python
from burner_radar_data import is_disposable, get_service

is_disposable("foo@mailinator.com")          # True
is_disposable("user@gmail.com")              # False

get_service("foo@mailinator.com")            # "mailinator"
get_service("xyz@somerotateddomain.com")     # "tempmail"  (matched via MX fingerprint)
get_service("user@gmail.com")                # None
```

Bulk access:

```python
from burner_radar_data import domains, services, data_generated_at

len(domains())                # ~17,000+
services()["mailinator"]      # [list of all known Mailinator frontends]
data_generated_at()           # "2026-06-18T..."
```

## Notes

- `get_service` returns `None` for any domain not classified into a known service. That is not the same as "this domain is legit": always use `is_disposable` for the blocklist check.
- The dataset is bundled with each release. To get a fresher list, upgrade the package or pull `data/domains.txt` directly from the [GitHub repo](https://github.com/manavdoshi-dev/burner-radar/blob/main/data/domains.txt).

## License

MIT.
