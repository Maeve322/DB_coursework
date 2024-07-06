import psycopg2
from psycopg2.extras import DictCursor


class DBManager:
    def __init__(
        self, db_name: str, user: str, password: str, host: str, port: int
    ):
        """
        Initializes a new instance of the DBManager class.

        Args:
            db_name (str): The name of the database.
            user (str): The username to use for the connection.
            password (str): The password to use for the connection.
            host (str): The host address of the database server.
            port (int): The port number to use for the connection.
        """
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port,
            cursor_factory=DictCursor,
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Creates the necessary tables in the database if they do not exist.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                company_id INTEGER NOT NULL REFERENCES companies(id),
                name VARCHAR(255) NOT NULL,
                salary INTEGER,
                link VARCHAR(255) NOT NULL
            );
        """
        )
        self.conn.commit()

    def insert_data(self, vacancies: list[dict]):
        """
        Inserts data into the database.
        Args:
            vacancies (list[dict]): A list of vacancy dictionaries.
        """
        company_names = set()
        for vacancy in vacancies:
            company_name = vacancy["employer"]["name"]
            if company_name not in company_names:
                company_names.add(company_name)
                self.cursor.execute(
                    "INSERT INTO companies (name) VALUES (%s) RETURNING id",
                    (company_name,),
                )
                company_id = self.cursor.fetchone()["id"]
            else:
                self.cursor.execute(
                    "SELECT id FROM companies WHERE name = %s", (company_name,)
                )
                company_id = self.cursor.fetchone()["id"]
            salary = vacancy["salary"]["from"] if vacancy["salary"] else None
            self.cursor.execute(
                """
                INSERT INTO vacancies (company_id, name, salary, link)
                VALUES (%s, %s, %s, %s)
            """,
                (company_id, vacancy["name"], salary, vacancy["url"]),
            )
        self.conn.commit()

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """
        Returns a list of companies with their corresponding vacancy counts.

        Returns:
            list[dict]: A list of dictionaries containing company names
                and vacancy counts.
        """
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> list[dict]:
        """
        Returns a list of all vacancies.

        Returns:
            list[dict]: A list of dictionaries containing vacancy information.
        """
        self.cursor.execute(
            """
            SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """
        Returns the average salary of all vacancies.

        Returns:
            float: The average salary.
        """
        self.cursor.execute("SELECT AVG(salary) FROM vacancies")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """
        Returns a list of vacancies with salaries higher
            than the average salary.

        Returns:
            list[dict]: A list of dictionaries containing vacancy information.
        """
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
            WHERE v.salary > %s
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> list[dict]:
        """
        Returns a list of vacancies with names containing
            the specified keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list[dict]: A list of dictionaries containing vacancy information.
        """
        self.cursor.execute(
            """
            SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
            WHERE v.name ILIKE %s
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()
