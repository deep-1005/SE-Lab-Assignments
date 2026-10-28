\# Lab 5 – Static Code Analysis: Issue Table



\*\*Student:\*\* Deeptha S (PES1UG24CS144)

\*\*File analysed:\*\* `supplier\_orders.py` (repo `L5\_18\_supplier\_orders`)

\*\*Tools:\*\* Pylint, Bandit, Flake8



\## Before vs after



| Tool | Before | After |

|------|--------|-------|

| Pylint | 2.41/10 (22 messages) | 10.00/10 (0 messages) |

| Bandit | 3 issues (1 High, 1 Medium, 1 Low) | 0 issues |

| Flake8 | 4 violations | 0 violations |



\## Issues found and fixed (high and medium severity first)



Line numbers refer to the original `supplier\_orders.py`.



| # | Issue | Type | Line(s) | Description | Fix Approach |

|---|-------|------|---------|-------------|--------------|

| 1 | OS command injection – Bandit B605 (High / High) | Security | 21 | `os.system("echo notifying warehouse about " + supplier)` builds a shell command from input. A supplier name such as `Acme \& del \*.\*` would run an extra command. | Removed the shell call and `import os`; the notification is now printed directly with `print()`, so no shell is started. |

| 2 | SQL injection – Bandit B608 (Medium / Medium), Pylint C0209 | Security | 11 | The INSERT query was built with `%` string formatting, so a value like `O'Brien` breaks the query and crafted input can change the SQL. | Switched to a parameterised query with `?` placeholders and passed the values as a tuple to `execute()`. |

| 3 | Silently swallowed errors – Bandit B110 (Low), Pylint W0718 broad-exception-caught | Bug / Security | 25–28 | `except Exception: pass` hides every failure, including database errors, so cleanup could fail with no trace. | Catch only `sqlite3.Error`, log it with `logging.error(...)` and return 0 so the caller knows nothing was deleted. |

| 4 | Global mutable state – Pylint W0603 global-statement, C0103 invalid-name | Design | 6, 10 | `order\_total` was a module global changed with `global`, which makes the code hard to test and reuse. | Moved the connection and the running total into a `SupplierOrderTracker` class (`self.order\_total`). |

| 5 | Shadowed module connection – Pylint W0621 redefined-outer-name | Bug risk | 4, 9, 16, 24, 31 | A module-level `conn` was created on import and every function parameter called `conn` shadowed it, making it easy to use the wrong one. | The connection is created in `SupplierOrderTracker.\_\_init\_\_` and used as `self.conn`; no module-level connection remains. |

| 6 | Unused argument `remarks` – Pylint W0613 | Bug | 16 | `markReceived()` accepted `remarks` but threw it away, so the caller's data was silently lost. | Added a `remarks` column and store it in the UPDATE; the method also returns `True`/`False` depending on whether the order existed. |

| 7 | Code runs on import | Bug (found in review) | 44 | `main()` was called at module level, so importing the file ran the demo. | Wrapped the call in `if \_\_name\_\_ == "\_\_main\_\_":`. |

| 8 | No input validation | Bug (found in review) | 9–13 | A negative or non-integer quantity was accepted and corrupted the running total. | `place\_order()` raises `ValueError` unless quantity is a positive integer. |

| 9 | camelCase function names – Pylint C0103 | Style | 9, 16, 20, 31 | `placeOrder`, `markReceived`, `notifyWarehouse`, `pendingCount` break the PEP 8 snake\_case convention. | Renamed to `place\_order`, `mark\_received`, `notify\_warehouse`, `pending\_count`. |

| 10 | Missing docstrings – Pylint C0114, C0116 | Style | 1, 9, 16, 20, 24, 31, 35 | No module or function docstrings. | Added a module docstring and a docstring for the class and every method/function. |

| 11 | Line too long – Flake8 E501, Pylint C0301 | Style | 5, 11, 32 | Lines of 122, 131 and 87 characters exceed the 79 (Flake8) / 100 (Pylint) limit. | Split SQL strings using implicit string concatenation inside brackets. |

| 12 | Missing whitespace around operator – Flake8 E225 | Style | 12 | `order\_total+=quantity` | Changed to `self.order\_total += quantity`. |

| 13 | Final newline missing – Pylint C0304 | Style | last line | Found when re-running Pylint after the Pylint commit (score 9.74/10): the file did not end with a newline. | Added a newline at the end of the file in the Flake8 commit; Pylint then rated it 10.00/10. |



\## Commits



1\. \*\*Bandit fixes\*\* – issues 1, 2, 3 (Bandit: 0 issues)

2\. \*\*Pylint fixes\*\* – issues 4–10 (Pylint: 9.74/10)

3\. \*\*Flake8 fixes\*\* – issues 11, 12, 13 (Flake8: 0 violations, Pylint: 10.00/10)



The program output is unchanged (`notifying warehouse about Acme` then `1 540`).

