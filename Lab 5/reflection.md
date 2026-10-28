\# Lab 5 – Reflection



\*\*Student:\*\* Deeptha S (PES1UG24CS144)



\### 1. Which issues were the easiest to fix, and which were the hardest? Why?



The easiest were the Flake8 style issues (E501 line too long, E225 missing whitespace) and the Pylint naming and docstring messages. They were mechanical: each message pointed to an exact line and the fix did not change behaviour.



The hardest were the ones that needed a design change. Removing the `global order\_total` (W0603) and the shadowed `conn` (W0621) could not be done by editing one line. The connection and running total had to move into a `SupplierOrderTracker` class, which meant rewriting `main()` and checking the output was still `1 540`. The unused `remarks` argument was also a judgement call: I could delete the parameter or make it useful. I chose to store it in a new column, because a caller passing remarks expects them to be saved.



\### 2. Did the static analysis tools report any false positives? If so, describe one example.



Nothing was completely wrong, but some messages were misleading. Pylint C0103 asked for `order\_total` to be renamed to UPPER\_CASE because it sits at module level and looks like a constant. It is actually a running counter, so renaming it to `ORDER\_TOTAL` would have silenced the warning while making the code more confusing. The real fix was removing the global altogether.



Bandit B110 (try/except/pass) is also sometimes a false positive in real projects, where ignoring a specific expected error is intended. Here it was a real problem because it caught every `Exception`.



Bandit only flagged the SQL with Medium confidence. If the values had been hard-coded constants it would have been a false positive, but here they come from function arguments, so it was a real injection risk.



\### 3. How would you integrate static analysis tools into your actual software development workflow?



\- \*\*Locally:\*\* run Flake8 and Pylint in the editor (VS Code Python extension) so problems show up while typing, and add a `pre-commit` hook that runs Flake8, Pylint and Bandit before each commit.

\- \*\*In CI:\*\* add a GitHub Actions workflow that runs all three on every push and pull request. Bandit High/Medium findings and Flake8 errors fail the build. Pylint has a minimum score with `--fail-under=9.5`.

\- \*\*Configuration:\*\* keep shared settings (line length, disabled checks) in `pyproject.toml` / `.flake8` / `.pylintrc` so everyone gets the same results, and only use `# nosec` or `# pylint: disable` with a comment explaining why.



\### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?



\- \*\*Security:\*\* both injection paths are gone. Shell commands are no longer built from input, and SQL uses parameterised queries, so names like `O'Brien` now work. Bandit went from 3 issues (1 High) to 0.

\- \*\*Robustness:\*\* database errors are logged instead of silently swallowed. Invalid quantities are rejected. `mark\_received` reports whether the order existed and keeps the remarks. Importing the module no longer runs the demo.

\- \*\*Readability and maintainability:\*\* snake\_case names, docstrings and a single class that owns the connection and total make the code easier to read, test and reuse. Pylint improved from 2.41/10 to 10.00/10 and Flake8 is clean.

