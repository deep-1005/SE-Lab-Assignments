#PES1UG24CS144_Deeptha
from hypothesis import given, example, strategies as st
from atm_withdrawal import notes_needed, mask_card, average_withdrawal


# ---------------------------------------------------------------------------
# Part 1: "no crash" fuzz tests (random text and None thrown at every function)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
@example(None)
@example("")
@example("abc")
@example("-500")
@example("2500.50")
@example("1_000")
def test_notes_needed_no_crash(s):
    #PES1UG24CS144_Deeptha
    try:
        notes_needed(s)
    except Exception as e:
        assert False, f"notes_needed crashed with: {e!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example("1234")
@example("1234 5678 9012")
@example("1234567890123456")
def test_mask_card_no_crash(s):
    #PES1UG24CS144_Deeptha
    try:
        mask_card(s)
    except Exception as e:
        assert False, f"mask_card crashed with: {e!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example("1,,3")
@example("one,two")
@example(",")
@example("-100,200")
def test_average_withdrawal_no_crash(s):
    #PES1UG24CS144_Deeptha
    try:
        average_withdrawal(s)
    except Exception as e:
        assert False, f"average_withdrawal crashed with: {e!r}"


# ---------------------------------------------------------------------------
# Part 2: property tests (valid input must still give the right answer,
# invalid input must be rejected with None instead of a wrong answer)
# ---------------------------------------------------------------------------

@given(st.integers(min_value=0, max_value=10**12))
def test_notes_needed_valid_amount(n):
    #PES1UG24CS144_Deeptha
    assert notes_needed(f"{n:,}") == n // 100
    assert notes_needed(str(n)) == n // 100


@given(st.integers(min_value=1, max_value=10**12))
def test_notes_needed_rejects_negative(n):
    #PES1UG24CS144_Deeptha
    assert notes_needed(f"-{n}") is None


@given(st.text() | st.none())
def test_notes_needed_result_is_none_or_non_negative_int(s):
    #PES1UG24CS144_Deeptha
    result = notes_needed(s)
    assert result is None or (isinstance(result, int) and result >= 0)


group = st.text(alphabet="0123456789", min_size=4, max_size=4)


@given(st.tuples(group, group, group, group))
def test_mask_card_valid_card(groups):
    #PES1UG24CS144_Deeptha
    masked = mask_card(" ".join(groups))
    assert masked == "XXXX XXXX XXXX " + groups[3]
    assert len(masked) == 19


@given(st.text() | st.none())
def test_mask_card_never_leaks_more_than_last_four_digits(s):
    #PES1UG24CS144_Deeptha
    masked = mask_card(s)
    if masked is not None:
        assert masked.startswith("XXXX XXXX XXXX ")
        assert len(masked) == 19
        assert masked[-4:].isdigit()


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=50))
def test_average_withdrawal_valid_list(values):
    #PES1UG24CS144_Deeptha
    result = average_withdrawal(",".join(str(v) for v in values))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1, max_size=10),
       st.integers(min_value=1, max_value=10**6))
def test_average_withdrawal_rejects_negative_entry(values, bad):
    #PES1UG24CS144_Deeptha
    assert average_withdrawal(",".join(str(v) for v in values + [-bad])) is None


@given(st.text() | st.none())
def test_average_withdrawal_result_is_none_or_non_negative_int(s):
    #PES1UG24CS144_Deeptha
    result = average_withdrawal(s)
    assert result is None or (isinstance(result, int) and result >= 0)
