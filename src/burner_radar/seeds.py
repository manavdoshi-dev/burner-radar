"""Hand-maintained seed list of known disposable email services.

Each service maps to a list of its canonical primary domains. These anchor
MX-based fingerprinting: any other domain whose MX records match a service's
signature is treated as a frontend for that service.
"""

SEED_SERVICES: dict[str, list[str]] = {
    "mailinator": ["mailinator.com"],
    "guerrillamail": [
        "guerrillamail.com",
        "sharklasers.com",
        "grr.la",
        "guerrillamailblock.com",
        "spam4.me",
        "pokemail.net",
    ],
    "yopmail": ["yopmail.com", "yopmail.fr", "yopmail.net"],
    "tempmail": ["tempmail.com", "temp-mail.org", "temp-mail.io"],
    "10minutemail": ["10minutemail.com", "10minutemail.net", "10minutemail.org"],
    "dispostable": ["dispostable.com"],
    "dropmail": ["dropmail.me", "10mail.org"],
    "maildrop": ["maildrop.cc"],
    "mintemail": ["mintemail.com"],
    "mohmal": ["mohmal.com"],
    "fakemailgenerator": ["fakemailgenerator.com"],
    "throwawaymail": ["throwawaymail.com"],
    "trashmail": ["trashmail.com", "trashmail.de"],
    "tempmailaddress": ["tempmailaddress.com"],
    "tempinbox": ["tempinbox.com"],
    "tempr": ["tempr.email"],
    "fakeinbox": ["fakeinbox.com"],
    "getairmail": ["getairmail.com"],
    "mailcatch": ["mailcatch.com"],
    "mailnesia": ["mailnesia.com"],
    "spambog": ["spambog.com"],
    "spamgourmet": ["spamgourmet.com"],
    "spamex": ["spamex.com"],
    "owlymail": ["owlymail.com"],
    "minuteinbox": ["minuteinbox.com"],
    "moakt": ["moakt.com"],
    "anonbox": ["anonbox.net"],
    "deadaddress": ["deadaddress.com"],
    "mytrashmail": ["mytrashmail.com"],
    "incognitomail": ["incognitomail.org"],
    "jetable": ["jetable.org"],
    "mailexpire": ["mailexpire.com"],
    "meltmail": ["meltmail.com"],
    "tempemail": ["tempemail.net", "tempemail.co"],
    "throwam": ["throwam.com"],
    "wegwerfmail": ["wegwerfmail.de"],
    "anonymbox": ["anonymbox.com"],
}


SEED_DOMAINS: list[str] = sorted({d for ds in SEED_SERVICES.values() for d in ds})
