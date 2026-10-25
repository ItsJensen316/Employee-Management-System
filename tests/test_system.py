import sys
import unittest
from pathlib import Path

# Locate the restored application
ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "restored-2026"

sys.path.insert(0, str(APP_DIR))

from database import connect_db
from auth import hash_password
from employee_auth import hash_pin


class TestAuthentication(unittest.TestCase):

    def test_admin_password_hash(self):
        salt = "a1" * 16
        password = "ExampleSecurePassword123!"

        first = hash_password(password, salt)
        second = hash_password(password, salt)

        self.assertEqual(first, second)
        self.assertNotEqual(first, password)
        self.assertEqual(len(first), 64)

    def test_different_passwords(self):
        salt = "b2" * 16

        first = hash_password("PasswordOne123!", salt)
        second = hash_password("PasswordTwo123!", salt)

        self.assertNotEqual(first, second)

    def test_employee_pin_hash(self):
        salt = "c3" * 16

        first = hash_pin("123456", salt)
        second = hash_pin("654321", salt)

        self.assertNotEqual(first, second)
        self.assertEqual(len(first), 64)


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mydb = connect_db()

        if cls.mydb is None:
            raise RuntimeError(
                "Database connection failed. Check MySQL and .env."
            )

        cls.mc = cls.mydb.cursor()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "mc"):
            cls.mc.close()

        if cls.mydb is not None:
            cls.mydb.close()

    def test_database_connection(self):
        self.assertTrue(self.mydb.is_connected())

    def test_employee_table_exists(self):
        self.mc.execute("SHOW TABLES LIKE 'employee'")
        self.assertIsNotNone(self.mc.fetchone())

    def test_employee_login_table_exists(self):
        self.mc.execute("SHOW TABLES LIKE 'employee_login'")
        self.assertIsNotNone(self.mc.fetchone())

    def test_employee_columns(self):
        self.mc.execute("SHOW COLUMNS FROM employee")
        columns = {row[0] for row in self.mc.fetchall()}

        expected = {
            "empid", "empname", "department",
            "salary", "status", "bonus", "contact"
        }

        self.assertEqual(columns, expected)

    def test_employee_count(self):
        self.mc.execute("SELECT COUNT(*) FROM employee")
        result = self.mc.fetchone()[0]

        self.assertGreaterEqual(result, 0)

    def test_no_orphan_login_records(self):
        self.mc.execute(
            """
            SELECT COUNT(*)
            FROM employee_login AS login
            LEFT JOIN employee AS emp
                ON login.empid = emp.empid
            WHERE emp.empid IS NULL
            """
        )

        self.assertEqual(self.mc.fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
