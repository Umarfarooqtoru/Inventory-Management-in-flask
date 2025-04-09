# Inventory Management System

This is a Flask-based Inventory Management System designed for a store. It allows users to manage categories, items, departments, and transactions, as well as issue items to departments and generate reports.

## Features

- **User Authentication**: Login and registration functionality with hashed passwords.
- **Dashboard**: Overview of total categories, items, departments, and low stock items.
- **Category Management**: Add, edit, and delete categories.
- **Item Management**: Add, edit, and delete items, with transaction logging.
- **Department Management**: Add, edit, and delete departments.
- **Issue Items**: Issue items to departments and track usage.
- **Reports**: Generate detailed reports of inventory transactions.
- **Low Stock Printing**: Print a list of low stock items.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd STORE
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. **Login**: Use the default admin credentials or register a new user.
2. **Dashboard**: Access the dashboard to view an overview of the inventory system.
3. **Manage Categories**: Add, edit, or delete categories.
4. **Manage Items**: Add, edit, or delete items, and log transactions.
5. **Manage Departments**: Add, edit, or delete departments.
6. **Issue Items**: Issue items to departments and track their usage.
7. **Generate Reports**: Generate detailed reports of inventory transactions.
8. **Print Low Stock**: Print a list of low stock items.

## Project Structure

- `app.py`: Main application file.
- `models.py`: Database models.
- `templates/`: HTML templates for the application.
- `instance/inventory.db`: SQLite database file.

## Dependencies

- Flask
- Flask-SQLAlchemy
- Werkzeug
