# Patient List Comparison Tool

A desktop app for reconciling patient rosters across practices. Import two Excel spreadsheets and the tool normalizes and compares them to surface who was added, removed, or changed, then exports the differences back to Excel.

Built at Trusted Doctors to reconcile patient lists across pediatric practices.

## Features
- Import lists from Excel (`.xlsx`) via a file picker
- Normalizes names and dates of birth for reliable matching
- Persists imported lists in a local SQLite database (SQLAlchemy)
- Compares two lists and reports additions, removals, and mismatches
- Exports the comparison result back to Excel

## Tech
Python · Tkinter (GUI) · pandas · SQLAlchemy / SQLite · PyInstaller (packaged as a Windows executable)

## Structure
```
src/
  ListApplication.py   Tkinter entry point + UI
  FileHelper.py        Excel import/export (pandas) + file dialogs
  DatabaseDriver.py    SQLite persistence via SQLAlchemy
  Spreadsheet.py       list model + comparison logic
testing/testing.py     comparison tests
```

## Run
```bash
pip install pandas openpyxl sqlalchemy
python src/ListApplication.py
```

## Note
Imported data is stored in a local `database.db` (gitignored). No patient data is included in this repository.
