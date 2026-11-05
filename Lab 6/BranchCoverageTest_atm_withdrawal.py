#PES1UG24CS144_Deeptha
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------- withdraw(): account type branch ----------
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_current_account_valid():
    assert withdraw(60000, 40000, "current", True) == 20000


def test_unknown_account_type():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "student", True)


# ---------- withdraw(): amount validation branches ----------
def test_invalid_amount_zero():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_invalid_amount_negative():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -100, "savings", True)


def test_invalid_amount_not_multiple_of_100():
    # amount > 0 but amount % 100 != 0
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


# ---------- withdraw(): daily limit branches ----------
def test_limit_exceeded_savings():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"


def test_exactly_at_savings_limit_allowed():
    assert withdraw(30000, 25000, "savings", True) == 5000


def test_limit_exceeded_current():
    assert withdraw(100000, 50100, "current", True) == "limit exceeded"


def test_exactly_at_current_limit_allowed():
    assert withdraw(60000, 50000, "current", True) == 10000


# ---------- withdraw(): fee branches ----------
def test_own_bank_no_fee_even_for_large_amount():
    assert withdraw(20000, 15000, "savings", True) == 5000


def test_other_bank_small_amount_base_fee_only():
    # 5000 + 20 = 5020
    assert withdraw(10000, 5000, "savings", False) == 4980


def test_other_bank_exactly_10000_base_fee_only():
    # boundary: amount > 10000 is False at 10000 -> fee stays 20
    assert withdraw(15000, 10000, "savings", False) == 4980


def test_other_bank_just_above_10000_extra_fee():
    # 10100 + 30 = 10130
    assert withdraw(15000, 10100, "savings", False) == 4870


def test_other_bank_large_amount_extra_fee():
    # 15000 + 30 = 15030
    assert withdraw(20000, 15000, "savings", False) == 4970


# ---------- withdraw(): balance check branches ----------
def test_insufficient_funds_own_bank():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_insufficient_funds_because_of_fee():
    # amount fits the balance, but amount + fee (1000 + 20) does not
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_exact_balance_leaves_zero():
    assert withdraw(1000, 1000, "savings", True) == 0


# ---------- pin_check() branches ----------
def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_correct_pin_on_last_allowed_attempt():
    assert pin_check(1234, 1234, 2) == "ok"


def test_card_blocked_after_three_attempts():
    assert pin_check(1234, 1111, 3) == "card blocked"


def test_card_blocked_even_with_correct_pin_after_three_attempts():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_wrong_pin_first_attempt_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_wrong_pin_second_attempt_retry():
    assert pin_check(1111, 1234, 1) == "retry"


def test_wrong_pin_third_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


# ---------- note_breakup() branches ----------
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_zero():
    assert note_breakup(0) == (0, 0, 0)


def test_note_breakup_only_100_notes():
    # remaining (100) < 200 -> else branch
    assert note_breakup(100) == (0, 0, 1)


def test_note_breakup_exactly_one_200_note():
    # remaining == 200 -> if branch boundary
    assert note_breakup(200) == (0, 1, 0)


def test_note_breakup_only_500_notes():
    assert note_breakup(1000) == (2, 0, 0)


def test_note_breakup_with_200_notes():
    # 1700 -> 3 x 500, 1 x 200, 0 x 100
    assert note_breakup(1700) == (3, 1, 0)


def test_note_breakup_mixed_all_denominations():
    # 1300 -> 2 x 500, 1 x 200, 1 x 100
    assert note_breakup(1300) == (2, 1, 1)


def test_note_breakup_without_200_notes():
    # 600 -> 1 x 500, 0 x 200, 1 x 100
    assert note_breakup(600) == (1, 0, 1)
