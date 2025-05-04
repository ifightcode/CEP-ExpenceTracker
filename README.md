# Expense Tracker

A simple desktop application for tracking personal expenses built with Python and PyQt5.

## Features

- Add expenses with date, category, amount, and description
- View all expenses in a table format
- Set and track monthly budget
- Save and load expenses from JSON file
- Export/Import expenses to/from CSV files
- Clear all expenses with confirmation

## Requirements

- Python 3.12
- uv package manager

## Installation and Running

1. Make sure you have Python 3.12 installed
2. Install uv package manager (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Run the application:
   ```bash
   uv run main.py
   ```
   This will automatically install the required dependencies (PyQt5) and run the application.

## Usage

1. **Adding an Expense**:
   - Select the date using the date picker
   - Choose a category from the dropdown
   - Enter the amount (in ₹)
   - Add a description
   - Click "Add Expense"

2. **Setting Budget**:
   - Enter the monthly budget amount
   - Click "Set Budget"
   - The application will show remaining budget and warn if exceeded

3. **Exporting/Importing**:
   - Click "Export to CSV" to save expenses to a CSV file
   - Click "Import from CSV" to load expenses from a CSV file

4. **Saving Data**:
   - Expenses are automatically saved to `expenses.json`
   - The file includes both expenses and monthly budget

5. **Clearing Data**:
   - Click "Clear All" to remove all expenses
   - A confirmation dialog will appear

## File Formats

### JSON Storage (`expenses.json`)
```json
{
    "expenses": [
        {
            "date": "YYYY-MM-DD",
            "category": "Category Name",
            "amount": 100.0,
            "description": "Expense Description"
        }
    ],
    "monthly_budget": 1000
}
```

### CSV Format
The CSV file contains the following columns:
- date (YYYY-MM-DD)
- category
- amount
- description

## Notes

- All monetary values are displayed in Indian Rupees (₹)
- The application automatically saves changes to the JSON file
- CSV import adds to existing expenses (does not replace them) 