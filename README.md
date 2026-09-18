<div align="center">

# 📚 Library Management System

A desktop Library Management System built with **Python**, **Tkinter**, and **SQLite** — add, view, update, issue/return, and delete book records through a simple GUI, backed by a clean, testable data layer.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-07405E?logo=sqlite&logoColor=white)
![Tests](https://github.com/shaikumar11/library_management_system/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</div>

---

## ✨ Features

- ➕ Add new book records with duplicate Book ID protection
- 👀 View and select records from a live table
- ✏️ Update book details
- 🔄 Issue / return books with card-ID tracking
- 🗑️ Delete a single record or wipe the full inventory
- ✅ Fully unit-tested data layer (7 tests, no GUI required to run them)

---

## 🏗️ Design — Repository Pattern

The project separates **data access** from **UI/application logic**:

```
┌─────────────────┐       calls        ┌──────────────────────┐       reads/writes      ┌──────────────┐
│     main.py       │  ───────────────▶  │  LibraryRepository    │  ─────────────────────▶  │  library.db   │
│  (Tkinter UI)      │                    │   (repository.py)      │                          │   (SQLite)     │
└─────────────────┘                     └──────────────────────┘                          └──────────────┘
```

All SQL lives in **one place** — `LibraryRepository`. `main.py` never touches SQL directly; it calls methods like `repo.add_book()`, `repo.get_all_books()`, `repo.update_status()`.

**Why it matters:**

| Without Repository | With Repository |
|---|---|
| SQL scattered across every UI function | SQL centralized in one class |
| Can't test data logic without launching the GUI | Data layer tested independently (`test_repository.py`) |
| Swapping the DB engine means editing UI code | UI code never changes if the storage layer changes |

---

## 📁 Project Structure

```
library_management_system/
├── main.py                      # Tkinter UI — calls into the repository, no SQL here
├── repository.py                # LibraryRepository — owns all DB reads/writes
├── test_repository.py           # unittest suite for the repository (7 tests)
├── .github/workflows/tests.yml  # CI — runs the test suite on every push
└── README.md
```

---

## 🚀 Getting Started

**Requirements:** Python 3.8+ (Tkinter ships with the standard library on most installs)

```bash
git clone https://github.com/shaikumar11/library_management_system.git
cd library_management_system
python main.py
```

## 🧪 Running Tests

```bash
python -m unittest test_repository.py -v
```

Tests run against an **in-memory SQLite database**, so they're fast and leave no files behind.

---

## 🗺️ Roadmap

- [ ] Add search/filter by book name or author
- [ ] Export inventory to CSV
- [ ] Add a `Member` table for library membership tracking

---

<div align="center">

Built by [Shaik Mohammed Umar](https://github.com/shaikumar11)

</div>
