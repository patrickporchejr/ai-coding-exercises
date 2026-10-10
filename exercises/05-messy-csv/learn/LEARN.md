# Phase 1: Learn (cleaning messy data in Python)

**Goal:** learn the Python tools and habits this exercise needs, so that in the Phase 2 mock interview you're thinking about the data, not the syntax.

**Mode:** untimed. Docs and AI help are allowed. Ask for hints rather than answers.

**Data:** `members_raw.csv`, a gym-membership export. It's a different dataset from the interview one (`../orders_raw.csv`), so practising here doesn't spoil the mock. **Don't open `orders_raw.csv` or `../mock/interviewer.md` until Phase 2.**

**Where to work:** `../answers/learn/`, for example one file per drill or a single notebook-style script.

**Setup:** `uv pip install pandas` (or `uv pip install -r requirements.txt` from the repo root).

---

## 1. Core ideas

- **Two ways to do it.** You can clean a CSV with **pandas** (a table you transform a column at a time) or with **plain Python** (`csv.DictReader` gives you one dict per row, and you loop). Both are fine in an interview. pandas is shorter for whole-column operations; plain Python makes a per-row audit log very natural. Pick one and be able to say why.
- **DataFrame and Series.** In pandas the table is a `DataFrame` and each column is a `Series`. Get a column with `df["col"]`. (`df.col` also works, but breaks on names with spaces or names that clash with methods.)
- **Whole-column vs. per-value.** Simple string work has vectorised methods: `df["name"].str.strip()`. Anything that needs `if` or `try` goes in a normal Python function that you apply to each value with `df["col"].map(my_function)`.
- **Missing values.** pandas uses `NaN` (sometimes `None` or `pd.NA`). Test with `pd.isna(v)` or `df["col"].isna()`. **Never `v == NaN`**: it's always False.
- **Indexing is 0-based.** `df.iloc[0]` is the first row. Keep the original file row number in its own column if you want to report on it.
- **Clean values, then log them.** Every function you write should give back the clean value *and* tell you whether it changed or failed. The report is a deliverable.

## 2. Toolkit for this exercise

| Task | pandas | Plain Python |
|---|---|---|
| Read everything as text | `pd.read_csv(f, dtype=str, keep_default_na=False)` | `rows = list(csv.DictReader(open(f, newline="")))` |
| Peek | `df.info()`, `df.head()`, `df.dtypes` | `rows[:3]` |
| Count rows | `len(df)` | `len(rows)` |
| Trim whitespace | `df["x"].str.strip()` | `v.strip()` |
| Case | `.str.lower()`, `.str.upper()`, `.str.title()` | `v.lower()`, `v.upper()`, `v.title()` |
| Regex replace | `df["x"].str.replace(r"[^0-9]", "", regex=True)` | `re.sub(r"[^0-9]", "", v)` |
| Regex check | `df["x"].str.match(r"^\d+$")` | `re.fullmatch(r"\d+", v)` |
| Recode with a lookup | `df["x"].map({"prem": "premium", ...})` (anything not in the dict becomes NaN) | `lookup.get(v.lower())` (returns `None` if missing) |
| Logic with many branches | A function with `if/elif/else`, applied with `.map(f)` | The same function, called in your loop |
| Filter rows | `df[(df["plan"] == "basic") & (df["fee"] > 10)]`. Use `&` and `\|`, not `and`/`or`, and **wrap each condition in parentheses**. | `[r for r in rows if r["plan"] == "basic"]` |
| Select columns | `df[["a", "b"]]` | `{k: r[k] for k in ("a", "b")}` |
| Exact duplicates | `df.duplicated()`, `df.drop_duplicates()` | Track a `set` of `tuple(r.values())` you've already seen |
| Duplicates on a key | `df[df["id"].duplicated(keep=False)]` | `collections.Counter(r["id"] for r in rows)` |
| Count values | `df["plan"].value_counts(dropna=False)` | `Counter(r["plan"] for r in rows)` |
| Group summary | `df.groupby("g").size()` or `.agg(...)` | `Counter` or a `dict` of lists |
| Parse a number | No built-in for `"$1,049.00"`. Strip what you don't want with `re.sub`, then `float(...)` (or `Decimal(...)` for money). | Same |
| Parse dates, several formats | Try `datetime.strptime(v, fmt)` for each format in a list, catching `ValueError`. (`pd.to_datetime` guesses formats for you, which is exactly what you *don't* want with messy data.) | Same |
| Build a log table | Append dicts to a list, then `pd.DataFrame(log)` at the end | Append dicts to a list |
| Write | `df.to_csv(f, index=False)` (forget `index=False` and you get an extra column) | `csv.DictWriter` |

## 3. Python syntax you'll need

```python
import re
from datetime import datetime

def parse_thing(raw):            # functions; indentation is the block
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:            # float("abc") raises ValueError
        return None

issues = []                       # an empty list
issues.append({"row": 3, "column": "fee", "raw": "free", "action": "set to 0"})

for i, row in df.iterrows():      # row-by-row loop (slow, but fine for small files)
    print(f"row {i}: {row['name']!r}")   # f-strings; !r shows quotes and stray spaces
```

## 4. Gotchas

1. **pandas guesses types and silently changes values.** Default `read_csv` turns `0012` into `12.0` (a blank in the column makes it float), and turns `"N/A"`, `"NA"`, `""` and `"null"` into NaN, so you lose the evidence of what was there. Read as `dtype=str, keep_default_na=False` first, then convert on purpose.
2. **Missing values in a string column are `NaN`, a float.** In pandas 3 an empty cell in a text column comes back as `NaN`, not `None`. So `v.lower()` crashes with `'float' object has no attribute 'lower'`. Check `pd.isna(v)` before calling string methods in your own functions.
3. **`.map(dict)` turns unmapped values into NaN.** If you map plan names and forget a spelling, that value quietly becomes missing. Check what didn't map before you trust the result.
4. **Chained assignment.** `df[df.x > 1]["y"] = 0` may do nothing (and warns). Use `df.loc[df["x"] > 1, "y"] = 0`.
5. **Integer columns with missing values.** A plain int column can't hold NaN, so pandas turns it into float. Use `astype("Int64")` (capital I) if you need nullable integers.
6. **Floats and money.** `0.1 + 0.2 != 0.3`. For an interview, `round(x, 2)` plus saying "in production I'd use `Decimal` or integer cents" is a good answer.

## 5. Drills on `members_raw.csv`

Do these in order. Each has a self-check so you know you're on track. Write the code yourself. If you're stuck, ask for a hint, not the answer.

**Drill 1: Load it two ways.**
Load the file with plain `pd.read_csv` and look at `dtypes` and the first rows. Then load it as all-strings with no NA conversion.
- *Check:* the default load shows `member_id` as `float64` with values like `12.0`, and reports 1 missing `member_id`. The all-strings load has 14 rows and keeps `0012`.
- *Say out loud:* what information did the default load destroy?

**Drill 2: Whitespace and casing.**
Strip every column. Normalise names to title case.
- *Check:* `"  tom okafor"` → `"Tom Okafor"`, `"LENA BERG"` → `"Lena Berg"`.
- *Think:* what would title case do to `"mcdonald"` or `"de la cruz"`? Is that your problem today?

**Drill 3: Missing-value tokens.**
Decide which strings mean "missing" (`""`, `"N/A"`, `"-"`, ...). Turn them into real missing values.
- *Check:* after this, missing counts per column are `member_id 1, name 1, phone 2, plan 1, signup_date 1, monthly_fee 2, active 2`.

**Drill 4: Categories.**
Normalise `plan` to exactly `basic`, `premium` or `family` using a lookup dict.
- *Check (before deduplication):* basic 6, premium 3, family 3, and exactly one non-missing value that doesn't map. Find it with code, not by eye.
- *Decide:* what do you do with the unknown plan? Drop the row, keep it as-is, or keep it and flag it?

**Drill 5: Booleans.**
Turn `active` into `True` / `False` / missing.
- *Check:* there are 7 distinct non-missing spellings in the raw data.

**Drill 6: Money.**
Write `parse_fee(raw)` that handles `$49.99`, `79.00 USD`, `"$1,049.00"`, `$79` and `free`.
- *Check:* 12 rows end up with a number, 2 are missing.
- *Decide:* is `free` 0 or missing? Is `$1,049.00` a real fee for a gym membership? You can't know, but you can flag it. What rule would you use to flag outliers?

**Drill 7: Dates.**
Write `parse_signup(raw)` that tries a list of formats.
- *Check:* with formats for `2024-01-15`, `15 Jan 2024` and `2024/02/03`, exactly 2 non-missing values fail to parse. Look at why each one fails. They fail for different reasons.
- *Gotcha:* one of the dates that *does* parse looks wrong but is correct. Which one, and why?
- *Decide:* `03/04/2024` could be 3 April or 4 March. What do you do when nothing in the row tells you?

**Drill 8: Phones.**
Keep digits only and check the length.
- *Check:* exactly one phone has the wrong number of digits after cleaning.

**Drill 9: Duplicates.**
Find exact duplicate rows, then rows that share a `member_id` but aren't exact copies.
- *Check:* 1 exact duplicate (`0013`). One `member_id` (`0020`) appears twice with different raw text.
- *Think:* run the duplicate check before and after normalising. Why does the answer change, and which order is right?

**Drill 10: The audit log and output.**
Rework your cleaning so that every change and every drop appends a dict to an `issues` list: row number, column, raw value, new value (or "dropped"), and a reason. Write `members_clean.csv` and print a summary of issues by reason.
- *Check:* if you drop exact duplicates, the all-missing row, the row with no `member_id`, and collapse the `0020` pair, you end up with 10 rows. Your number may differ if you made different decisions. That's fine if your log explains every one.

## 6. Structure to aim for

When you redo it as one script, aim for something an interviewer can follow at a glance:

1. **Load** as raw strings, and keep the original row number.
2. **One small function per column type**: missing tokens, text, category, number, date, boolean. Each returns the clean value *and* a reason when it changed or failed.
3. **Normalise first, deduplicate second.**
4. **Decide drop vs. keep-and-flag** with a rule you can say in one sentence.
5. **Write the clean file and the report.** The report is a deliverable, not an afterthought.

## 7. Ready for Phase 2?

You're ready for the mock when you can do these **without looking anything up**:
- [ ] Read a CSV as all-strings and say why
- [ ] Strip, lowercase and regex-replace a column
- [ ] Recode with a dict and find the values that didn't map
- [ ] Write a parse function with `try/except` that tries several date formats
- [ ] Find exact duplicates and duplicates on a key
- [ ] Build a list of dicts and turn it into a DataFrame
- [ ] Write a CSV without the index column

Then go to [`../mock/MOCK.md`](../mock/MOCK.md).
