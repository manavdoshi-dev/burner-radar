import { DOMAINS, SERVICE_BY_DOMAIN, SERVICES, GENERATED_AT, VERSION } from "./data.js";

function extractDomain(emailOrDomain: string): string {
  let s = emailOrDomain.trim().toLowerCase();
  const at = s.lastIndexOf("@");
  if (at >= 0) s = s.slice(at + 1);
  return s.replace(/^\.+|\.+$/g, "");
}

/** True if the domain part is a known disposable email domain. */
export function isDisposable(emailOrDomain: string): boolean {
  return DOMAINS.has(extractDomain(emailOrDomain));
}

/**
 * Parent burner service for this domain, or null if unknown.
 *
 * A null return does NOT mean the domain is legit. It only means we have no
 * MX-fingerprint match for a known service. Use isDisposable for the
 * blocklist check.
 */
export function getService(emailOrDomain: string): string | null {
  return SERVICE_BY_DOMAIN.get(extractDomain(emailOrDomain)) ?? null;
}

/** Full set of disposable domains in this release. */
export function domains(): ReadonlySet<string> {
  return DOMAINS;
}

/** {service_name: [frontend_domains]} for all classified services. */
export function services(): Readonly<Record<string, readonly string[]>> {
  return SERVICES;
}

/** ISO-8601 timestamp of when the bundled dataset was generated. */
export function dataGeneratedAt(): string {
  return GENERATED_AT;
}

export { VERSION as version };
