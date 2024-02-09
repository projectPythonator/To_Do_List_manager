import to_do_app_backend as backend_file
import unittest


"""Known bugs to fix
Technically right now the backend isn't fully connected to the front end exception wise
need to bridge this gap via model and controller
Example would be you can add a new user that already exists so it just loads the user instead
SHOULD DO IS FOLLOWING: put up text box notifying user already exists explicitly
Fix would be checking for exceptions during is_valid_input functions

When we update instead of using a DB update command we just delete then create.
it's the same operation but we should sometime put in fix that uses the proper command
Fix would be just add an update function to the back end 
"""


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

    def test_delete_one(self):
        db_name = 'agis.db'
        table_name = "test_delete_one_table"
        expected = [("test task 1", "content here 1"), ("test task 2", "content here 2")]
        conn = backend_file.connect_to_db(db_name)
        backend_file.drop_table(conn, table_name)
        backend_file.create_table(conn, table_name)
        for key, value in expected:
            backend_file.insert_one(conn, key, value, table_name)
        backend_file.delete_one(conn, "test task 1", table_name)
        test_contents = backend_file.select_all(conn, table_name)
        self.assertEqual(len(test_contents), len(expected)-1)
        for i, row_values in enumerate(test_contents[1:]):
            self.assertEqual(row_values[1], expected[i][0])
            self.assertEqual(row_values[2], expected[i][1])
        backend_file.delete_one(conn, "test task 2", table_name)
        test_contents = backend_file.select_all(conn, table_name)
        self.assertEqual(len(test_contents), len(expected)-2)


if __name__ == "__main__":
    unittest.main()
