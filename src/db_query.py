from db_config import DB_CONN
class Query:
        @staticmethod
        def insertCar(car):
                cursor = DB_CONN.cursor()
                sql_statement = "INSERT INTO car(registrationNum, model, price_per_day, properties, availability, employer) VALUES (?,?,?,?,?,?)"
                cursor.execute(sql_statement, car)
                DB_CONN.commit()
                cursor.close()
        @staticmethod
        def insertCustomer(customer):
                cursor = DB_CONN.cursor()
                sql_statement = "INSERT INTO customer(username, password, full_name, date_of_birth, email) VALUES (?,?,?,?,?)"
                cursor.execute(sql_statement, customer)
                DB_CONN.commit()
                cursor.close()
        @staticmethod
        def insertReport(report):
                cursor = DB_CONN.cursor()
                sql_statement = "INSERT INTO report(customer, registrationNum, reportIssue) VALUES (?,?,?)"
                cursor.execute(sql_statement, report)
                DB_CONN.commit()
                cursor.close()
        @staticmethod
        def insertTransactions(transaction):
                cursor = DB_CONN.cursor()
                sql_statement = "INSERT INTO transactions(customer, payment, payment_date) VALUES (?,?,?)"
                cursor.execute(sql_statement, transaction)
                DB_CONN.commit()
                cursor.close()
        @staticmethod
        def insertRent(rentCar):
                cursor = DB_CONN.cursor()
                sql_statement = "INSERT INTO rent(customer, registrationNum, rent_date) VALUES (?,?,?)"
                cursor.execute(sql_statement, rentCar)
                DB_CONN.commit()
                cursor.close()
        @staticmethod
        def selectCustomer(identity):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM customer WHERE username = ? AND password = ?"
                cursor.execute(sql_statement, identity)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results
        @staticmethod
        def selectEmployer(identity):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM employer WHERE username = ? AND password = ?"
                cursor.execute(sql_statement, identity)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectAvailableCar():
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM car WHERE availability = 1"
                cursor.execute(sql_statement)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectCar(carReg):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM car WHERE registrationNum = ?"
                cursor.execute(sql_statement, (carReg,))
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def updateCar(availability, car_reg):
                cursor = DB_CONN.cursor()
                sql_statement = "UPDATE car SET availability = ? WHERE registrationNum = ?"
                cursor.execute(sql_statement, (availability, car_reg,))
                DB_CONN.commit()
                cursor.close()
                return None
      
        @staticmethod
        def deleteRentedCar(customer, car_reg):
                cursor = DB_CONN.cursor()
                sql_statement = "DELETE FROM rent WHERE customer = ? AND registrationNum = ?"
                cursor.execute(sql_statement, (customer, car_reg,))
                DB_CONN.commit()
                cursor.close()
                return None
                
        @staticmethod
        def selectRentedCar(customer, car_reg):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM rent WHERE customer = ? AND registrationNum= ?"
                cursor.execute(sql_statement, (customer, car_reg,))
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results
        @staticmethod
        def selectRentedHistory(customer):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM rent WHERE customer = ?"
                cursor.execute(sql_statement, (customer,))
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectAllRentedCar():
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM rent"
                cursor.execute(sql_statement)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectPrice(carReg):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT price_per_day FROM car WHERE registrationNum = ?"
                cursor.execute(sql_statement, (carReg,))
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectTransaction():
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT * FROM transactions"
                cursor.execute(sql_statement)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def countTransaction():
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT customer, SUM(payment) FROM transactions GROUP BY customer ORDER BY payment_date"
                cursor.execute(sql_statement)
                results = cursor.fetchall()
                DB_CONN.commit()
                cursor.close()
                return results

        @staticmethod
        def selectReport(customer):
                cursor = DB_CONN.cursor()
                sql_statement = "SELECT customer, registrationNum, datetime(reportDate, 'unixepoch') AS reportDate, reportIssue FROM report WHERE customer = ?"
                cursor.execute(sql_statement, (customer,))
                results = cursor.fetchall()
                DB_CONN.commit()
                return results
