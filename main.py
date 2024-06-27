import requests


from db.dbmanager import DBManager
from config import DB_config


companies = [
    "1740",  # Яндекс
    "87021",  # WB
    "2180",  # ozon
    "2748",
    "907345",  # lukiol
    "633069",
    "3529",  # sber
    "78638",  # tbank
    "15478",  # vk
    "668019",
]


def get_vacancies(company_name):
    url = f"https://api.hh.ru/vacancies?employer_id={company_name}"
    response = requests.get(url, params={"per_page": 10})
    return response.json()


def get_all_vacancies():
    all_vacancies = []
    for company in companies:
        vacancies = get_vacancies(company)
        all_vacancies.extend(vacancies["items"])
    return all_vacancies


if __name__ == "__main__":
    db_manager = DBManager(
        db_name=DB_config["db_name"],
        user=DB_config["user"],
        password=DB_config["password"],
        host=DB_config["host"],
        port=DB_config["port"],
    )
    # db_manager.create_tables()

    # vacancies = get_all_vacancies()

    # db_manager.insert_data(vacancies)
    print(db_manager.get_companies_and_vacancies_count())
    # print(db_manager.get_all_vacancies())
    # print(db_manager.get_avg_salary())
    # print(db_manager.get_vacancies_with_higher_salary())
    # print(db_manager.get_vacancies_with_keyword("Python"))
