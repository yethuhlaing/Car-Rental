import sqlite3
from sqlite3 import Connection
import os

DB_FILEPATH = os.path.join("rentalCar.db")
DB_CONN: Connection = sqlite3.connect(DB_FILEPATH)
