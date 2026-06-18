"""Public community-maintained lists of disposable email domains.

Each source is treated as a low-weight signal. A domain that appears in
multiple sources gets a higher confidence score.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    fmt: str  # "lines" or "json_list"


SOURCES: list[Source] = [
    Source(
        name="disposable-email-domains/blocklist",
        url="https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/disposable_email_blocklist.conf",
        fmt="lines",
    ),
    Source(
        name="7c/fakefilter",
        url="https://raw.githubusercontent.com/7c/fakefilter/main/txt/data.txt",
        fmt="lines",
    ),
    Source(
        name="ivolo/disposable-email-domains",
        url="https://raw.githubusercontent.com/ivolo/disposable-email-domains/master/index.json",
        fmt="json_list",
    ),
]
