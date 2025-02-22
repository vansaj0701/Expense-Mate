# Expense Mate

The Expense Mate is a web-based application that allows users to manage their income and expenses efficiently. Built with Flask and SQLite, it provides a user-friendly platform for tracking financial data. Users can register, log in, and input their expenses under different categories. The app calculates total income, total expenses, and current balance, helping users maintain better control over their finances.


## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Security](#security)
- [Prerequisites](#prerequisites)
- [Contributing](#contributing)


## Features

- **User Registration**: Users can create an account by providing their name, email, total income, and password.
- **User Login**: Users can log in using their email and password.
- **Track Income & Expenses**: Users can view their total income, categorized expenses, and the current balance.
- **Add Expenses**: Users can add expenses, categorized by type (e.g., travel, food, other) with a date.
- **Edit Income**: Users can change their total income after authenticating with their password.
- **History**: View a history of recent expenses with their category, amount, and date.


## Tech Stack

- **Flask**: A micro web framework for Python.
- **SQLite**: A lightweight relational database used to store user and expense data.
- **Werkzeug**: A WSGI utility library for password hashing.


## Installation

Follow the steps below to get the application running on your local machine:

1. Clone this repository:

    ```bash
    git clone https://github.com/vansaj0701/Expense-Mate.git
    cd expense-tracker
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database:

    The database (`expense.db`) will be automatically created when you first run the app.

6. Run the application:

    ```bash
    flask run
    ```

7. Open the app in your browser at:

    ```
    http://127.0.0.1:5000/
    ```


## Usage

1. **Register**: Go to `/register` and create an account by filling out your name, email, total income, and password.
2. **Login**: After registration, log in using your email and password at `/login`.
3. **Add Expenses**: Once logged in, navigate to `/new` to add an expense.
4. **View Dashboard**: The main page (`/`) displays your total income, expenses by category, and balance.
5. **Edit Income**: To update your income, go to `/edit_amount` and provide your new income along with your password for authentication.


## Database Schema

The app uses an SQLite database with the following tables:

- **users**: Stores user information.
  - `user_id`: Primary key, auto-incremented.
  - `name`: User's full name.
  - `email`: User's email (unique).
  - `amount`: Total income.
  - `password`: Hashed password.

- **expenses**: Stores expenses for each user.
  - `expense_id`: Primary key, auto-incremented.
  - `user_id`: Foreign key referencing `users.user_id`.
  - `category`: Category of the expense (e.g., "travel", "food", etc.).
  - `amount`: Amount spent.
  - `date_added`: Date when the expense was added.


## Security

- Passwords are securely stored using hashing via `werkzeug.security`.
- Sessions are managed using Flask's session system with server-side storage (via Flask-Session).


## Prerequisites

- Python 3.x
- Flask
- Flask-Session
- SQLite (default database, no installation needed)


## Contributing

This project is a personal submission for CS50, and I’m currently not accepting external contributions. However, feel free to fork the repository and make improvements for your own learning.
