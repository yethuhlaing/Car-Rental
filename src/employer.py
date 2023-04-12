from menu import Menu
from db_query import Query
from menu import Menu
from colorama import init, Fore, Back, Style
init(convert=True)
# --------------------------------Menu for Employer--------------------------------#
class EmployerMenu(Menu):
        def __init__(self) -> None:
                super().__init__(options=[
                        {"description": "Login", "action": self.loginEmployer},
                ], title="Login to our Rental App.")
        def loginEmployer(self) -> None:
                while True:
                        username = input("Enter your Username: ")
                        password = input("Enter your Password: ")
                        identity = (username, password)
                        result = Query.selectEmployer(identity)
                        if len(result) == 0:
                                print("Incorrect Username or Password")
                        else:
                                break
                (_, _, _, fname, _) = result[0]
                print("You have been logged in to the Car Rental Application.")
                Employer(fname).start()
                return None
# --------------------------------Employer--------------------------------#
class Employer(Menu):
        full_name: str
        def __init__(self, full_name: str) -> None:
                self.full_name = full_name
                super().__init__(options=[
                        {"description": "Add the Car", "action": self.addCar},
                        {"description": "List the Available Car","action": self.listAvailableCar},
                        {"description": "List the Rented Car", "action": self.listRentedCar},
                        {"description": "List the Transactions", "action": self.listTransactions},
                        {"description": "Calculate the Transactions", "action": self.calculateTransactions},
                ])
                return None
        def addCar(self)-> None:
                try:
                        registrationNum = input("Enter the registrationNum: ")
                        model = input("Enter the Model: ")
                        price_per_day = int(input("Enter the  Price per day: "))
                        properties = input("Enter the Properties: ")
                        result = (registrationNum, model, price_per_day, properties, 1, self.full_name)
                        Query("car", columns= self.car_cols, parameters=result).insertQuery()
                        print("\nYou have successfully added the follwing car available car in Rental Car System")
                        print(f"Registration Number: {registrationNum}", f"Model: {model}", f"Price per day: {price_per_day}", f'Properties: {properties}', sep='\n')
                        Employer(self.full_name).start()
                except Exception as err:
                        print(err)
                return None

        def listAvailableCar(self)-> None:
                result = Query.selectAvailableCar()
                if len(result) != 0:
                        for car_turple in result:
                                print("*" * 50)
                                print(Fore.CYAN + f"Registration Number: {car_turple[0]}", f"Model: {car_turple[1]}",
                                f"Price per day: {car_turple[2]}", f'Properties: {car_turple[3]}' + Style.RESET_ALL, sep='\n')
                else:
                        print("There is no available cars!")
                Employer(self.full_name).start()
                return None

        def listRentedCar(self)-> None:
                result = Query.selectAllRentedCar()
                if len(result) != 0:
                        for car_turple in result:
                                print("*" * 50)
                                print(Fore.CYAN + f"Registration Number: {car_turple[1]}", f"customer: {car_turple[2]}",
                                f"rent_date: {car_turple[3]}" + Style.RESET_ALL, sep='\n')
                else:
                        print("There is no rented cars!")
                Employer(self.full_name).start()
                return None

        def listTransactions(self)-> None:
                result = Query.selectTransaction()
                if len(result) != 0:
                        for transaction in result:
                                print(Fore.CYAN + f"Customer Name: {transaction[1]}", f"Net Payment: {transaction[2]}", f"Payment date: {transaction[3]}" + Style.RESET_ALL, sep='\n')                      
                else:
                        print("There is no transactions!")
                Employer(self.full_name).start()
                return None

        def calculateTransactions(self)-> None:
                result = Query.countTransaction()
                if len(result) != 0:
                        for transaction in result:
                                print(Fore.CYAN + f"Customer: {transaction[0]}", f"Total Net Payment: {transaction[1]}" + Style.RESET_ALL, sep='\n')
                else:
                        print("There is no transaction!")
                Employer(self.full_name).start()
                return None

                
        