from db.dbmanager import DBManager
from utils import get_all_vacancies
from config import DB_config


if __name__ == "__main__":
    db_manager = DBManager(
        db_name=DB_config["db_name"],
        user=DB_config["user"],
        password=DB_config["password"],
        host=DB_config["host"],
        port=DB_config["port"],
    )

    db_manager.create_tables()
    vacancies = get_all_vacancies()
    db_manager.insert_data(vacancies)

    while True:
        print("Menu:")
        print("1. Вывод всех вакансий")
        print("2. Вывод вакансий по ключевому слову")
        print("3. Вывод компаний и количества вакансий")
        print("4. Вывод средней зарплаты")
        print("5. Вывод вакансий с зарплатой выше средней")
        print("6. Выход")

        choice = input("Введите номер пункта меню: ")

        if choice == "1":
            print(f">>> {db_manager.get_all_vacancies()}")
        elif choice == "2":
            keyword = input("Введите ключевое слово: ")
            print(f">>> {db_manager.get_vacancies_with_keyword(keyword)}")
        elif choice == "3":
            print(f">>> {db_manager.get_companies_and_vacancies_count()}")
        elif choice == "4":
            print(f">>> {db_manager.get_avg_salary()}")
        elif choice == "5":
            print(f">>> {db_manager.get_vacancies_with_higher_salary()}")
        elif choice == "6":
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт меню.")
