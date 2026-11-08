import builtins
from io import StringIO

import pytest

from animacy.utils import logging as catalog_logging


def test_log_skips_catalog_when_level_is_disabled(monkeypatch):
    def fail_open(*args, **kwargs):
        raise AssertionError("disabled log message opened the catalog")

    monkeypatch.setattr(catalog_logging, "LOG_LEVEL", catalog_logging.WARNING)
    monkeypatch.setattr(builtins, "open", fail_open)

    catalog_logging.log(3, catalog_logging.DEBUG, "unused")


def test_log_uses_id_formats_and_prints_catalog_message(monkeypatch, capsys):
    monkeypatch.setattr(catalog_logging, "LOG_LEVEL", catalog_logging.INFO)
    monkeypatch.setattr(
        catalog_logging,
        "_LOG_STRINGS_PATH",
        "unused",
    )
    monkeypatch.setattr(
        builtins,
        "open",
        lambda *_args, **_kwargs: StringIO(
            "# comment\n\n001|First entry\n003|Hello {}!\n"
        ),
    )

    catalog_logging.log(3, catalog_logging.INFO, "world")

    assert capsys.readouterr().out == "Hello world!\n"


def test_log_reads_package_catalog(monkeypatch, capsys):
    monkeypatch.setattr(catalog_logging, "LOG_LEVEL", catalog_logging.INFO)

    catalog_logging.log(1, catalog_logging.INFO, 42, "00:01")

    assert capsys.readouterr().out == "Process performance message 42@00:01\n"


def test_log_raises_when_id_is_missing(monkeypatch):
    monkeypatch.setattr(catalog_logging, "LOG_LEVEL", catalog_logging.INFO)
    monkeypatch.setattr(
        builtins,
        "open",
        lambda *_args, **_kwargs: StringIO("001|Only entry\n"),
    )

    with pytest.raises(KeyError, match="Log message ID not found: 3"):
        catalog_logging.log(3, catalog_logging.INFO)


def test_log_rejects_malformed_catalog_entry(monkeypatch):
    monkeypatch.setattr(catalog_logging, "LOG_LEVEL", catalog_logging.INFO)
    monkeypatch.setattr(
        builtins,
        "open",
        lambda *_args, **_kwargs: StringIO("not a record\n"),
    )

    with pytest.raises(ValueError, match="Malformed log catalog entry"):
        catalog_logging.log(3, catalog_logging.INFO)
