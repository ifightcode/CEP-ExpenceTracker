import sys
import csv
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, 
                           QMessageBox, QDateEdit, QSpinBox, QFileDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QDate

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.expenses = []
        self.monthly_budget = 0
        self.initUI()
        self.load_expenses()

    def initUI(self):
        self.setWindowTitle('Expense Tracker')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create form for adding expenses
        form_layout = QHBoxLayout()
        
        # Date input
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form_layout.addWidget(QLabel('Date:'))
        form_layout.addWidget(self.date_input)

        # Category input
        self.category_input = QComboBox()
        self.category_input.addItems(['Food', 'Travel', 'Entertainment', 'Shopping', 'Bills', 'Other'])
        form_layout.addWidget(QLabel('Category:'))
        form_layout.addWidget(self.category_input)

        # Amount input
        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setPrefix('₹')
        form_layout.addWidget(QLabel('Amount:'))
        form_layout.addWidget(self.amount_input)

        # Description input
        self.description_input = QLineEdit()
        self.description_input.setMinimumWidth(200)
        self.description_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(QLabel('Description:'))
        form_layout.addWidget(self.description_input)

        # Add expense button
        add_button = QPushButton('Add Expense')
        add_button.clicked.connect(self.add_expense)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # Create table for displaying expenses
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(['Date', 'Category', 'Amount', 'Description'])
        layout.addWidget(self.expense_table)

        # Budget section
        budget_layout = QHBoxLayout()
        self.budget_input = QSpinBox()
        self.budget_input.setRange(0, 1000000)
        self.budget_input.setPrefix('₹')
        budget_layout.addWidget(QLabel('Monthly Budget:'))
        budget_layout.addWidget(self.budget_input)
        
        set_budget_button = QPushButton('Set Budget')
        set_budget_button.clicked.connect(self.set_budget)
        budget_layout.addWidget(set_budget_button)
        
        self.budget_status = QLabel('')
        budget_layout.addWidget(self.budget_status)
        
        layout.addLayout(budget_layout)

        # Buttons for additional actions
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('Save Expenses')
        save_button.clicked.connect(self.save_expenses)
        button_layout.addWidget(save_button)

        export_csv_button = QPushButton('Export to CSV')
        export_csv_button.clicked.connect(self.export_to_csv)
        button_layout.addWidget(export_csv_button)

        import_csv_button = QPushButton('Import from CSV')
        import_csv_button.clicked.connect(self.import_from_csv)
        button_layout.addWidget(import_csv_button)

        clear_button = QPushButton('Clear All')
        clear_button.clicked.connect(self.clear_expenses)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

    def add_expense(self):
        date = self.date_input.date().toString('yyyy-MM-dd')
        category = self.category_input.currentText()
        amount = self.amount_input.value()
        description = self.description_input.text()

        if not description:
            QMessageBox.warning(self, 'Warning', 'Please enter a description')
            return

        expense = {
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        }
        self.expenses.append(expense)
        self.update_expense_table()
        self.check_budget()
        self.save_expenses()  # Auto-save after adding expense

    def update_expense_table(self):
        self.expense_table.setRowCount(len(self.expenses))
        for row, expense in enumerate(self.expenses):
            self.expense_table.setItem(row, 0, QTableWidgetItem(expense['date']))
            self.expense_table.setItem(row, 1, QTableWidgetItem(expense['category']))
            self.expense_table.setItem(row, 2, QTableWidgetItem(f"₹{expense['amount']}"))
            self.expense_table.setItem(row, 3, QTableWidgetItem(expense['description']))

    def set_budget(self):
        self.monthly_budget = self.budget_input.value()
        self.check_budget()
        self.save_expenses()  # Auto-save after setting budget

    def check_budget(self):
        if self.monthly_budget == 0:
            return

        total_expenses = sum(expense['amount'] for expense in self.expenses)
        remaining = self.monthly_budget - total_expenses

        if remaining < 0:
            self.budget_status.setText(f'Warning: You have exceeded your budget by ₹{abs(remaining)}!')
            self.budget_status.setStyleSheet('color: red')
        else:
            self.budget_status.setText(f'Remaining budget: ₹{remaining}')
            self.budget_status.setStyleSheet('color: green')

    def save_expenses(self):
        try:
            data = {
                'expenses': self.expenses,
                'monthly_budget': self.monthly_budget
            }
            with open('expenses.json', 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save expenses: {str(e)}')

    def load_expenses(self):
        try:
            with open('expenses.json', 'r') as file:
                data = json.load(file)
                self.expenses = data.get('expenses', [])
                self.monthly_budget = data.get('monthly_budget', 0)
                self.budget_input.setValue(self.monthly_budget)
            self.update_expense_table()
            self.check_budget()
        except FileNotFoundError:
            pass
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load expenses: {str(e)}')

    def export_to_csv(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export to CSV", "", "CSV Files (*.csv)"
            )
            if file_path:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                    writer.writeheader()
                    writer.writerows(self.expenses)
                QMessageBox.information(self, 'Success', 'Expenses exported to CSV successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to export expenses: {str(e)}')

    def import_from_csv(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import from CSV", "", "CSV Files (*.csv)"
            )
            if file_path:
                with open(file_path, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    imported_expenses = list(reader)
                    for expense in imported_expenses:
                        expense['amount'] = float(expense['amount'])
                    self.expenses.extend(imported_expenses)
                self.update_expense_table()
                self.check_budget()
                self.save_expenses()  # Auto-save after importing
                QMessageBox.information(self, 'Success', 'Expenses imported from CSV successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to import expenses: {str(e)}')

    def clear_expenses(self):
        reply = QMessageBox.question(self, 'Confirm Clear',
                                   'Are you sure you want to clear all expenses?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.expenses = []
            self.update_expense_table()
            self.check_budget()
            self.save_expenses()  # Auto-save after clearing

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExpenseTracker()
    ex.show()
    sys.exit(app.exec_())
