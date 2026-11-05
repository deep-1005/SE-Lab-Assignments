#PES1UG24CS144_Deeptha
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------- withdraw() ----------
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account_type():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "student", True)


def test_invalid_amount_zero():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_limit_exceeded():
    assert withdraw(100000, 30000, "savings", True) == "limit exceeded"


def test_other_bank_large_amount_fee():
    # 15000 + fee (20 + 10) = 15030
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------- pin_check() ----------
def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_card_blocked_after_three_attempts():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_wrong_pin_third_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


# ---------- note_breakup() ----------
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_with_200_notes():
    # 1700 -> 3 x 500, 1 x 200, 0 x 100
    assert note_breakup(1700) == (3, 1, 0)


def test_note_breakup_without_200_notes():
    # 600 -> 1 x 500, 0 x 200, 1 x 100
    assert note_breakup(600) == (1, 0, 1)
