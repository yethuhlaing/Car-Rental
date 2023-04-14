CREATE TABLE IF NOT EXISTS customer(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username VARCHAR(255) NOT NULL,
 password VARCHAR(255) NOT NULL,
 full_name VARCHAR(255) NOT NULL,
 date_of_birth VARCHAR(255) NOT NULL, 
 email VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS employer(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username VARCHAR(255) NOT NULL,
 password VARCHAR(255) NOT NULL,
 full_name VARCHAR(255) NOT NULL,
 position VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS car(
 registrationNum VARCHAR(255) PRIMARY KEY NOT NULL,
 model VARCHAR(255) NOT NULL,
 price_per_day INTEGER NOT NULL,
 properties VARCHAR(255) NOT NULL,
 availability  INTEGER,
 employer VARCHAR(255),
 FOREIGN KEY (employer) REFERENCES employer(full_name)
);
CREATE TABLE IF NOT EXISTS rent(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 customer VARCHAR(255) NOT NULL,
 registrationNum VARCHAR(255) NOT NULL,
 rent_date VARCHAR(255) NOT NULL,
 FOREIGN KEY (customer) REFERENCES customer(full_name),
 FOREIGN KEY (registrationNum) REFERENCES car(registrationNum)
);
CREATE TABLE IF NOT EXISTS transactions(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 customer VARCHAR(255) NOT NULL,
 payment FLOAT NOT NULL,
 payment_date TEXT(255) NOT NULL,
 FOREIGN KEY (customer) REFERENCES customer(full_name)
);
CREATE TABLE IF NOT EXISTS report(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 customer VARCHAR(255) NOT NULL,
 registrationNum VARCHAR(255) NOT NULL,
 reportDate timestamp default (strftime('%s', 'now')),
 reportIssue VARCHAR(255) NOT NULL,
 FOREIGN KEY (customer) REFERENCES customer(full_name),
 FOREIGN KEY (registrationNum) REFERENCES rent(registrationNum)
);