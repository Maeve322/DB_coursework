import requests

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


def get_vacancies(company_name) -> dict:
    """
    Retrieves vacancies for a given company from the HeadHunter API.

    Args:
        company_name (str): The name of the company.

    Returns:
        dict: A dictionary containing the vacancy data.
    """
    url = f"https://api.hh.ru/vacancies?employer_id={company_name}"
    response = requests.get(url, params={"per_page": 10})
    return response.json()


def get_all_vacancies() -> list[dict]:
    """
    Retrieves all vacancies for a list of companies from the HeadHunter API.

    Args:
        companies (list[str]): A list of company names.

    Returns:
        list[dict]: A list of dictionaries containing the vacancy data.
    """
    all_vacancies = []
    for company in companies:
        vacancies = get_vacancies(company)
        all_vacancies.extend(vacancies["items"])
    return all_vacancies
