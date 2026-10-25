import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print("MySQL connection successful!")

    mc = connection.cursor()
    mc.execute("SELECT COUNT(*) FROM employee")

    print("Employee count:", mc.fetchone()[0])

except mysql.connector.Error as error:
    print("Connection failed:", error)

finally:
    if "mc" in locals():
        mc.close()
    if "connection" in locals() and connection.is_connected():
        connection.close()