from db_config import DB_CONN
from menu import Menu
from customer import CustomerMenu
from employer import EmployerMenu

class Main:
	def __init__(self) -> None:
		self.initDB()
		main_menu = MainMenu()
		main_menu.start()
		DB_CONN.close()
	def initDB(self) -> None:
		with open("init.sql", 'r', encoding="UTF-8") as file_handle:
			cursor = DB_CONN.cursor()
			sql_script = file_handle.read()
			cursor.executescript(sql_script)
			DB_CONN.commit()
		return None

class MainMenu(Menu): 
        def __init__(self) -> None:
                super().__init__(options=[
                        {"description": "Are you a Customer", "action": self.customerAction},
                        {"description": "Are you an Employer", "action": self.employerAction},
                ], title="Welcome to our Car Rental Application.")
                return None
        def customerAction(self):
                menuCustomer = CustomerMenu()
                menuCustomer.start()
        def employerAction(self):
                menuEmployer = EmployerMenu()
                menuEmployer.start()
		
if __name__ == "__main__":
        app = Main()