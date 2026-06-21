from burner_radar_data import (
    domains,
    get_service,
    is_disposable,
    services,
    data_generated_at,
)


def test_known_disposable():
    assert is_disposable("foo@mailinator.com")
    assert is_disposable("MAILINATOR.COM")
    assert is_disposable("bar@yopmail.com")


def test_known_legit():
    assert not is_disposable("user@gmail.com")
    assert not is_disposable("user@protonmail.com")
    assert not is_disposable("user@example.com")


def test_service_lookup():
    assert get_service("foo@mailinator.com") == "mailinator"
    assert get_service("bar@yopmail.com") == "yopmail"
    assert get_service("user@gmail.com") is None


def test_dataset_size():
    assert len(domains()) > 10_000


def test_services_present():
    s = services()
    assert "mailinator" in s
    assert "yopmail" in s


def test_generated_at():
    assert data_generated_at()
