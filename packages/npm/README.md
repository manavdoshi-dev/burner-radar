# burner-radar-data

Disposable email domain blocklist with a tiny API. Bundled, offline, zero runtime dependencies.

The dataset is rebuilt daily by the [burner-radar](https://github.com/manavdoshi-dev/burner-radar) pipeline from multiple community lists, MX-validated, and classified by parent service via MX fingerprinting.

## Install

```bash
npm install burner-radar-data
```

## Use

```ts
import { isDisposable, getService } from "burner-radar-data";

isDisposable("foo@mailinator.com");          // true
isDisposable("user@gmail.com");              // false

getService("foo@mailinator.com");            // "mailinator"
getService("xyz@somerotateddomain.com");     // "tempmail"  (matched via MX fingerprint)
getService("user@gmail.com");                // null
```

Bulk access:

```ts
import { domains, services, dataGeneratedAt } from "burner-radar-data";

domains().size;                          // ~17,000+
services()["mailinator"];                // [list of all known Mailinator frontends]
dataGeneratedAt();                       // "2026-06-18T..."
```

## Notes

- `getService` returns `null` for any domain not classified into a known service. That is not the same as "this domain is legit": always use `isDisposable` for the blocklist check.
- The dataset is bundled with each release. To get a fresher list, upgrade the package or pull `data/domains.txt` directly from the [GitHub repo](https://github.com/manavdoshi-dev/burner-radar/blob/main/data/domains.txt).

## License

MIT.
