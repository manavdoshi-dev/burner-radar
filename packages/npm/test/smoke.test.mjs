import { test } from "node:test";
import assert from "node:assert/strict";

import {
  isDisposable,
  getService,
  domains,
  services,
  dataGeneratedAt,
} from "../dist/index.js";

test("known disposable", () => {
  assert.equal(isDisposable("foo@mailinator.com"), true);
  assert.equal(isDisposable("MAILINATOR.COM"), true);
  assert.equal(isDisposable("bar@yopmail.com"), true);
});

test("known legit", () => {
  assert.equal(isDisposable("user@gmail.com"), false);
  assert.equal(isDisposable("user@protonmail.com"), false);
  assert.equal(isDisposable("user@example.com"), false);
});

test("service lookup", () => {
  assert.equal(getService("foo@mailinator.com"), "mailinator");
  assert.equal(getService("bar@yopmail.com"), "yopmail");
  assert.equal(getService("user@gmail.com"), null);
});

test("dataset size", () => {
  assert.ok(domains().size > 10_000);
});

test("services present", () => {
  const s = services();
  assert.ok(s.mailinator);
  assert.ok(s.yopmail);
});

test("generated at", () => {
  assert.ok(dataGeneratedAt().length > 0);
});
