# Lab 6 - Code and Branch Coverage (ATM Withdrawal)

Coverage analysis of the assigned `atm_withdrawal.py` module (repo L6_L7_18_atm_withdrawal) using `coverage` and `pytest`.

## Files

| File | Description |
|------|-------------|
| `atm_withdrawal.py` | Module under test (withdraw, pin_check, note_breakup) |
| `test_atm_withdrawal.py` | Original starter test file |
| `CodeCoverageTest_atm_withdrawal.py` | Test cases for code (line) coverage |
| `BranchCoverageTest_atm_withdrawal.py` | Test cases for branch coverage |
| `screenshots/` | Terminal output of the coverage reports |

## Results

| Test file | Line coverage | Branch coverage |
|-----------|---------------|-----------------|
| CodeCoverageTest_atm_withdrawal.py | 100% | 98% |
| BranchCoverageTest_atm_withdrawal.py | 100% | 100% |

## Commands

    coverage run -m pytest <test_file>
    coverage report -m
    coverage run --branch -m pytest <test_file>
    coverage report -m
