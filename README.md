# API Automation Framework - E-commerce
A scalable API automation framework built using Python and Pytest for testing real-world e-commerce workflows like authentication, cart, and order management.

## Tech Stack
- Python
- Pytest
- Requests
- Allure Reports

## Features
- Modular API automation framework
- Reusable request handling
- Pytest-based test execution
- Response validation
- Reporting support (Allure)
- Scalable folder structure

## Project Structure
project/
│── tests/
│── utils/
│── pages/
│── config.py
│── .env
│── conftest.py

## How to Run

1. Clone the repo:
git clone https://github.com/your-username/api-automation-ecommerce.git

2. Install dependencies:
pip install -r requirements.txt

3. Run tests:
pytest

4.Allure Reporting

1. Run tests and generate Allure results:
pytest --alluredir=allure-results

2. Generate and open the report:
allure serve allure-results
