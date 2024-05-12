from statement import *
import pytest


def test_invoice_1():
    plays = read_json_file(PLAYS_DB_FPATH)
    invoice = read_json_file(INVOICES_DB_FPATH)[0]
    expected = """Statement for BigCo
  Hamlet: $650.00 (55 seats)
  As You Like It: $580.00 (35 seats)
  Othello: $500.00 (40 seats)
Amount owed is $1,730.00
You earned 47 credits"""
    assert statement(invoice, plays) == expected


def test_invoice_2():
    plays = read_json_file(PLAYS_DB_FPATH)
    invoice = read_json_file(INVOICES_DB_FPATH)[1]
    expected = """Statement for SmallCo
  Hamlet: $400.00 (5 seats)
  As You Like It: $327.00 (9 seats)
Amount owed is $727.00
You earned 1 credits"""
    assert statement(invoice, plays) == expected
