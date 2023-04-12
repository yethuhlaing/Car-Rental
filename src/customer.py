from menu import Menu
from db_query import Query
import datetime as dt
from colorama import init, Fore, Style
from fetchAPI import FetchAPI
COMMISSION_RATE = {
        "Nordea" : 0.15,
        "OP" : 0.14,
        "Spankki" : 0.11,
        "Handelsbanken" : 0.20,
        "PayPal" : 0.03
}
UNAVAILABILITY =  0
AVAILABILITY = 1
# --------------------------------Menu for Customer--------------------------------#
class CustomerMenu(Menu):
        def __init__(self) -> None:
                super().__init__(options=[
                        {"description": "Register", "action": self.registerCustomer},
                        {"description": "Login", "action": self.loginCustomer},
                ], title="If you are already our Customer, you can login to our Rental App.\nIf not, please register first.")
                return None
        def registerCustomer(self) -> None:
                username = input("username: ")
                password = input("password: ")
                full_name = input("full_name: ")
                date_of_birth = input("date_of_birth(dd/mm/yyyy): ")
                email = input("email: ")
                customer = (username, password, full_name, date_of_birth, email)
                list = Query.selectCustomer((username, password))
                if len(list) == 0: #finding the unique customer
                        if '.' in email and '@' in email: #check validity of email
                                Query.insertCustomer(customer)
                                print("You have successfully registered in our Rental Car System")
                                print("Do you want to login?")
                                self.loginCustomer()
                        else:
                                print("Invalid email address.")
                else:
                        print("Try another username! The username is already taken.")
                        self.loginCustomer()
                return None
        def loginCustomer(self) -> None:
                while True:
                        username = input("Enter your Username: ")
                        password = input("Enter your Password: ")
                        identity = (username, password)
                        result = Query.selectCustomer(identity)
                        if len(result) == 0:
                                print("Incorrect Username or Password")
                        else:
                                break
                (_, _, _, fname, date_of_birth, _) = result[0]
                print("You have been logged in to the Car Rental Application.")
                Customer(fname, date_of_birth).start()
                return None
# --------------------------------Customer--------------------------------#
class Customer(Menu):
        init(autoreset=True)
        full_name: str
        date_of_birth: str
        due_payment: float
        starting_customer_amount: float
        current_time: object

        def __init__(self, full_name: str, date_of_birth: str, due_payment: float = 0) -> None:
                super().__init__(options=[
                        {"description": "Available Car list","action": self.listAvailableCar},
                        {"description": "Rent Car", "action": self.rentCar},
                        {"description": "Report Issues", "action": self.report},
                        {"description": "Return Car", "action": self.returnCar},
                        {"description": "Payment","action": self.payment},
                        {"description": "Car Gallery", "action": self.gallery},
                        {"description": "Rental History", "action": self.rentalHistory},
                        {"description": "Report History", "action": self.reportHistory},
                ])
                self.full_name = full_name
                self.date_of_birth = date_of_birth
                self.due_payment = due_payment
                self.starting_customer_amount = 2000
                self.current_time = dt.datetime.now().date

        def listAvailableCar(self) -> None:
                try:
                        for car_turple in Query.selectAvailableCar():
                                print("*" * 50)
                                print(Fore.CYAN + f"Registration Number: {car_turple[0]}", f"Model: {car_turple[1]}", f"Price per month: {car_turple[2]}", f'Properties: {car_turple[3]}' + Style.RESET_ALL, sep='\n')
                        Customer(self.full_name, self.date_of_birth, self.due_payment).start()
                except Exception as err:
                       print(err)
                
        def rentCar(self) -> None:
                if self.customer_check(self.date_of_birth):
                        self.car_reg = input('Please input the car registration number you want to rent: ')   
                        result = Query.selectCar(self.car_reg)
                        if len(result) == 0:
                                print("The Registration Number is incorrect!")
                        else:
                                renting_car = result[0]
                                #Checking Availiability
                                if renting_car[4] == 1: 
                                        self.rent_date = str(self.current_time())
                                        Query.updateCar(UNAVAILABILITY, self.car_reg)
                                        print("You have successfully rented the following car")
                                        print(Fore.LIGHTGREEN_EX + f"Registration Number: {self.car_reg}",f'Rented Date: {self.rent_date}' + Style.RESET_ALL, sep='\n')
                                        car = (self.full_name, self.car_reg, self.rent_date)
                                        Query.insertRent(car)
                                else:
                                        print('Car already rented')                                         
                        Customer(self.full_name, self.date_of_birth, self.due_payment).start()
                return None

        def report(self)-> None:
                self.car_reg = input("Please input the registration number of your rented car: ")
                rented_car = Query.selectRentedCar(self.full_name, self.car_reg)
                #Check whether the customer rented or not
                if len(rented_car) > 0: 
                        self.report_issue = input("What issue would you like to report?\n")
                        #Insert into Database
                        report = (self.full_name, self.car_reg,self.report_issue)
                        Query.insertReport(report)
                        #Loop the program
                        Customer(self.full_name, self.due_payment).start()
                else:
                        print("Please enter the correct registration number!")
                return None

        def customer_check(self,b_day)-> bool:
                try:
                        day, month, year = b_day.split('/')
                        bday = dt.date(int(year), int(month), int(day))
                        age = dt.datetime.now().year - int(bday.year)
                        if age > 100:
                                print('Age limit exceeded')
                                return False
                        elif age < 18:
                                print('You must be 18 years and above to rent a car')
                                return False
                        else:
                                return True
                except ValueError:
                        print('Incorrect date format')

        def returnCar(self)-> None:
                self.return_reg = str(input('Please input the car registration number: '))
                self.looping = False
                self.rented_cars = Query.selectRentedCar(self.full_name, self.return_reg)
                for car in self.rented_cars:
                        if car[2] == self.return_reg:
                                rented_date = dt.datetime.strptime(car[3], '%Y-%m-%d')
                                due_date = dt.datetime.strptime(str(self.current_time()), '%Y-%m-%d') 
                                duration = due_date - rented_date
                                price_per_month = Query.selectPrice(self.return_reg)[0][0]
                                print(Query.selectPrice(self.return_reg)[0])
                                self.due_payment = price_per_month * abs(duration.days)                                   
                                print(Fore.LIGHTBLACK_EX + f"\nHello {self.full_name}.\nYou return this car ({self.return_reg}) in {due_date}.\nYour Rental Period is {abs(duration)}" + Style.RESET_ALL)
                                Query.updateCar(AVAILABILITY, self.return_reg)
                                Query.deleteRentedCar(self.full_name, self.return_reg)
                                self.looping = True
                                break
                if self.looping == False:
                        print('Incorrect Input')
                Customer(self.full_name, self.date_of_birth, self.due_payment).start()
                return None
        def payment(self)-> None:
                customer_amount = float(input("Please enter your credit amount in your card: "))
                if customer_amount > self.starting_customer_amount:
                        print("The available bank service for our Applications are following")
                        for i in COMMISSION_RATE.keys():    
                                print(" -", i, end="")                                  
                        bank_name = input("\nPlease enter your bank name: ")
                        self.processPayment(bank_name, customer_amount)
                else:
                        print(f"Our Rental Application set the starting amount from {self.starting_customer_amount}$\nPlease make sure you have that amount to continue.\nSorry to feel bother you.")
                Customer(self.full_name, self.date_of_birth, self.due_payment).start()
                return None
        def processPayment(self, bank_name, customer_amount) -> None:    
                if bank_name in COMMISSION_RATE.keys():
                        self.rate = COMMISSION_RATE[bank_name]
                        self.commission = self.due_payment * self.rate
                        self.net_payment = self.commission + self.due_payment
                        self.remaining = customer_amount - self.net_payment       
                        print(f"The due payment is {self.due_payment}\nThe commission rate is {self.rate}\nThe Net amount remain in your account is {self.remaining:.2f}")
                        transaction = (self.full_name, self.net_payment, str(self.current_time()))
                        Query.insertTransactions(transaction)
                else:   
                        print("The bank name is incorrect!")
                return None

        def gallery(self)-> None:
                try:
                        while True:
                                query = input("What Car image would you like to see: ")
                                quantity = int(input("How many images would you like to see: "))                      
                                FetchAPI(query, str(quantity)).DisplayPhotos()
                                choice = int(input("Do you still want to continue or exist: (0 -exit , 1 = continue): "))
                                if choice == 0:
                                        break
                                elif type(choice) != int:
                                        print("Please enter the value 1 or 0")
                        Customer(self.full_name,self.due_payment).start()
                except Exception as error:
                        raise error
                return None

        def rentalHistory(self)-> None:
                result = Query.selectRentedHistory(self.full_name)
                if len(result) != 0:
                        for car in result:
                                print(f"Customer : {car[1]}\nRegistration Number: {car[2]}\nRented Date: {car[3]}")
                else:
                        print("There is no Rental History.")
                Customer(self.full_name, self.due_payment).start()
                return None

        def reportHistory(self) -> None:
                result = Query.selectReport(self.full_name)
                for i in result:
                        print(f"The Regestration No. of your rented car is {i[1]}.\nYou reported the following statement at {i[2]}\n{i[3]}")
                Customer(self.full_name, self.due_payment).start()
                return None




