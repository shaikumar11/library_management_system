# Library Management System

A desktop Library Management System (Python, Tkinter, SQLite) for adding,
viewing, updating, issuing/returning, and deleting book records.

## Design

The project follows the **Repository pattern**: all database access is
isolated inside `LibraryRepository` (`repository.py`). `main.py` contains
only UI and application logic and never touches SQL directly — it calls
methods like `repo.add_book()`, `repo.get_all_books()`, `repo.update_status()`.

This separation means:
- The data layer can be unit-tested without launching the GUI (`test_repository.py` uses an in-memory SQLite DB).
- The database engine or schema can change without touching UI code.
- Business/UI logic stays readable, since it isn't mixed with raw SQL.

## Structure

```
main.py              # Tkinter UI, calls into the repository
repository.py         # LibraryRepository — owns all DB reads/writes
test_repository.py    # unittest suite for the repository (7 tests)
```

## Run it

```bash
python main.py
```

## Run the tests

```bash
python -m unittest test_repository.py -v
```
