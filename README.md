# Job Vacancies Database Manager

This Python class, `DBManager`, provides a simple interface for managing a PostgreSQL database to store and retrieve job vacancy data. The class uses the `psycopg2` library to interact with the database.

## Installation

Before using this class, make sure you have installed the `psycopg2` library. You can install it using pip:

```bash
pip install psycopg2
```

## Usage

To use the `DBManager` class, create an instance with the appropriate database connection details:
Edit your configuration in `config.py` file
```python
DB_config = {
    "db_name": "your_database_name",
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "your_port",
}
```

Then, you can use the following methods to interact with the database:

- `create_tables()`: Creates the necessary tables (`companies` and `vacancies`) in the database.
- `insert_data(vacancies)`: Inserts job vacancy data into the database. The `vacancies` parameter should be a list of dictionaries, where each dictionary represents a vacancy with the following keys: `employer`, `name`, `salary`, and `url`.
- `get_companies_and_vacancies_count()`: Returns a list of dictionaries, where each dictionary represents a company and its associated vacancies count.
- `get_all_vacancies()`: Returns a list of dictionaries, where each dictionary represents a vacancy with the following keys: `company_name`, `vacancy_name`, `salary`, and `link`.
- `get_avg_salary()`: Returns the average salary of all vacancies in the database.
- `get_vacancies_with_higher_salary()`: Returns a list of dictionaries, where each dictionary represents a vacancy with a salary higher than the average salary.
- `get_vacancies_with_keyword(keyword)`: Returns a list of dictionaries, where each dictionary represents a vacancy with the specified keyword in its name.

## Example

```python
db_manager = DBManager(db_name="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")

db_manager.create_tables()

vacancies = [
    {
        "employer": {"name": "Company A"},
        "name": "Software Engineer",
        "salary": {"from": 80000},
        "url": "https://example.com/vacancy1"
    },
    {
        "employer": {"name": "Company B"},
        "name": "Data Scientist",
        "salary": {"from": 90000},
        "url": "https://example.com/vacancy2"
    },
    {
        "employer": {"name": "Company A"},
        "name": "Frontend Developer",
        "salary": {"from": 70000},
        "url": "https://example.com/vacancy3"
    }
]

db_manager.insert_data(vacancies)

companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
print(companies_and_vacancies_count)
# Output: [{'name': 'Company A', 'vacancies_count': 2}, {'name': 'Company B', 'vacancies_count': 1}]

all_vacancies = db_manager.get_all_vacancies()
print(all_vacancies)
# Output: [{'company_name': 'Company A', 'vacancy_name': 'Software Engineer', 'salary': 80000, 'link': 'https://example.com/vacancy1'}, ...]

avg_salary = db_manager.get_avg_salary()
print(avg_salary)
# Output: 80000.0

higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
print(higher_salary_vacancies)
# Output: [{'company_name': 'Company B', 'vacancy_name': 'Data Scientist', 'salary': 90000, 'link': 'https://example.com/vacancy2'}, ...]

keyword_vacancies = db_manager.get_vacancies_with_keyword("Software")
print(keyword_vacancies)
# Output: [{'company_name': 'Company A', 'vacancy_name': 'Software Engineer', 'salary': 80000, 'link': 'https://example.com/vacancy1'}, ...]
```

Note: Replace the connection details (`db_name`, `user`, `password`, `host`, `port`) with your actual PostgreSQL database credentials.