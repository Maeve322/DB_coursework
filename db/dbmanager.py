import psycopg2
from psycopg2.extras import DictCursor


class DBManager:
    def __init__(self, db_name, user, password, host, port):
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

    def insert_data(self, vacancies):
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

    def get_companies_and_vacancies_count(self):
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute(
            """
            SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("SELECT AVG(salary) FROM vacancies")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
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

    def get_vacancies_with_keyword(self, keyword):
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
