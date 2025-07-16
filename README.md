### Part 1: Theoretical Deep Dive

Study this in `deep_error.py`:

```python
def fetch_records():
    # Simulates fetching raw text entries
    return [
        "user:1|score:100",
        "user:2|score:abc",
        "bad_format_record",
        "user:3|score:50"
    ]

def parse_record(record):
    # Expect format "user:<id>|score:<number>"
    parts = record.split("|")
    if len(parts) != 2:
        raise ValueError(f"Format error in '{record}'")
    u_part = parts[0].split(":")
    s_part = parts[1].split(":")
    if len(u_part) != 2 or len(s_part) != 2:
        raise ValueError(f"Parsing error in '{record}'")
    return u_part[1], s_part[1]

def process_records():
    users = []
    scores = []
    for rec in fetch_records():
        try:
            uid, raw_score = parse_record(rec)
            score = int(raw_score)            # may raise ValueError
        except ValueError as e:
            print(f"[Warning] Skipping record: {e}")
        else:
            users.append(uid)
            scores.append(score)
        finally:
            print(f"Finished processing: {rec}")
    # Compute total without returning anything
    total = 0
    for i in range(len(scores)):
        total += scores[i]
    print("Total score:", total)
```

**Your tasks (write up in `Part1_deepdive.md`):**

1. **Trace**

   * Run just the call to `parse_record("bad_format_record")`.
   * Capture the full traceback: which line, what exception type, what message?
2. **Explain**

   * For a **valid** record (e.g. `"user:1|score:100"`), in what order do `try`, `else`, and `finally` execute?
   * For a **malformed** record, how does that order change?
   * Why does `finally` always run, even on exceptions?
   * Contrast what happens when `parse_record` fails vs. when `int(raw_score)` fails.
3. **Modify**

   * In `process_records`, catch the `ValueError` from `int(raw_score)` and **re‑raise** it as

     ```python
     raise RuntimeError("Conversion error") from e
     ```
   * Then wrap your call to `process_records()` in a `try`/`except RuntimeError as e:` that prints

     ```python
     print("Processing failed, root cause:", e.__cause__)
     ```
   * Show your updated code and a sample run in your write‑up.
4. **Discuss** (short bullet points)

   * What pitfalls come from using a bare `except:`?
   * How do specific exceptions plus `else`/`finally` improve robustness and maintainability?

---

### Part 2: Practical Exercises (≈ 35 min)

*(No changes; still no dicts, tuples, comprehensions or classes.)*

#### 1. `safe_sum(str_list)`

```python
def safe_sum(str_list):
    """
    - For each entry in str_list, try to convert it to int.
    - On ValueError, append the error message to errors.
    - On success (else), add to total.
    - In finally for each entry, print "Processed entry: <entry>".
    - Return a list [total, errors], where errors is itself a list of strings.
    """
```

* **Sample**

  ```python
  result = safe_sum(["4", "x", "10", ""])
  # result == [14, [
  #   "invalid literal for int() with base 10: 'x'",
  #   "invalid literal for int() with base 10: ''"
  # ]]
  ```

#### 2. `bulk_divide(num_strs, den_strs)`

```python
def bulk_divide(num_strs, den_strs):
    """
    - Iterate by index over both lists.
    - try: convert num_strs[i] and den_strs[i] to int and divide.
    - except ValueError: append "Error at idx i: invalid literal '<val>'" to errors.
    - except ZeroDivisionError: append "Error at idx i: division by zero" to errors.
    - except Exception: append any other error string.
    - else: append str(result) to results.
    - finally: append "Index i processed" to logs.
    - Return a list [results, errors, logs], each being a list of strings.
    """
```

* **Sample**

  ```python
  output = bulk_divide(["8","a","6"], ["2","2","0"])
  # output == [
  #   ["4.0"],    # results
  #   [
  #     "Error at idx 1: invalid literal 'a'",
  #     "Error at idx 2: division by zero"
  #   ],
  #   [
  #     "Index 0 processed",
  #     "Index 1 processed",
  #     "Index 2 processed"
  #   ]
  # ]
  ```


Good luck!
