import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc
import model_view_controller as mvc_file
import unittest


class TestBackEnd(unittest.TestCase):
    def test_scrub(self):
        test_str = 'QWERTY123456!@#$%{}{}{}'
        expected = 'QWERTY123456'
        self.assertEqual(backend_file.scrub(test_str), expected)

    def test_connect_to_db(self):
        expected_local = ':memory:'
        expected_named = 'agis.db'
        backend_file.connect_to_db()
        self.assertEqual(backend_file.DB_name, expected_local)
        backend_file.connect_to_db('agis')
        self.assertEqual(backend_file.DB_name, expected_named)

    def test_select_all(self):
        """Depends on insert one working"""
        db_name = 'agis.db'
        table_name = "test_select_all_table"
        expected = [("test task 1", "content here 1"), ("test task 2", "content here 2")]
        backend_file.connect_to_db(db_name)
        conn = backend_file.connect_to_db(db_name)
        backend_file.drop_table(conn, table_name)
        backend_file.create_table(conn, table_name)
        for key, value in expected:
            backend_file.insert_one(conn, key, value, table_name)
        test_contents = backend_file.select_all(conn, table_name)

        self.assertEqual(len(test_contents), len(expected))
        for i, row_values in enumerate(test_contents):
            self.assertEqual(row_values[1], expected[i][0])
            self.assertEqual(row_values[2], expected[i][1])

    def test_insert_one(self):
        """Depends on insert one working"""
        db_name = 'agis.db'
        table_name = "test_insert_one_table"
        expected = [("test name 1", "content here 1")]
        backend_file.connect_to_db(db_name)
        conn = backend_file.connect_to_db(db_name)
        backend_file.drop_table(conn, table_name)
        backend_file.create_table(conn, table_name)
        for key, value in expected:
            backend_file.insert_one(conn, key, value, table_name)
        test_contents = backend_file.select_all(conn, table_name)

        self.assertEqual(len(test_contents), len(expected))
        for i, row_values in enumerate(test_contents):
            self.assertEqual(row_values[1], expected[i][0])
            self.assertEqual(row_values[2], expected[i][1])


if __name__ == "__main__":
    unittest.main()
