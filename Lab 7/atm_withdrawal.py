#PES1UG24CS144_Deeptha
# Hardened ATM helpers.
# Every function validates its input and returns None for anything invalid,
# instead of crashing with ValueError / IndexError / AttributeError.


def _parse_amount(text):
    """Convert text such as '2,500' to a non-negative int.

    Returns None if text is not a str, is empty, or contains anything other
    than ASCII digits (and commas, which are removed). That rejects signs,
    decimals, spaces inside the number, '1_000' (int() would accept it),
    and non-ASCII digits.
    """
    #PES1UG24CS144_Deeptha
    if not isinstance(text, str):
        return None
    cleaned = text.strip().replace(',', '')
    if not cleaned or not (cleaned.isascii() and cleaned.isdigit()):
        return None
    try:
        return int(cleaned)
    except ValueError:  # e.g. more digits than Python's int-conversion limit
        return None


def notes_needed(amount):
    #PES1UG24CS144_Deeptha
    value = _parse_amount(amount)
    if value is None:
        return None
    return value // 100


def mask_card(card_number):
    #PES1UG24CS144_Deeptha
    if not isinstance(card_number, str):
        return None
    groups = card_number.split()
    if len(groups) != 4:
        return None
    for g in groups:
        if len(g) != 4 or not (g.isascii() and g.isdigit()):
            return None
    return "XXXX XXXX XXXX " + groups[3]


def average_withdrawal(amounts_csv):
    #PES1UG24CS144_Deeptha
    if not isinstance(amounts_csv, str):
        return None
    amounts = []
    for part in amounts_csv.split(','):
        value = _parse_amount(part)
        if value is None:  # empty entry, text, negative, decimal, ...
            return None
        amounts.append(value)
    return sum(amounts) // len(amounts)  # amounts is never empty here


def main():
    #PES1UG24CS144_Deeptha
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result if result is not None else "Invalid amount")

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result if result is not None else "Invalid card number")

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result if result is not None else "Invalid withdrawals list")


if __name__ == "__main__":
    main()
