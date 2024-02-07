import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc
import model_view_controller as mvc_file
import unittest


class TestBackEnd(unittest.TestCase):
    def test_scrub(self):
        test_str = 'QWERTY123456!@#$%{}{}{}'
        expected = 'QWERTY123456'
        self.assertEqual(backend_file.scrub(test_str), expected)



if __name__ == "__main__":
    unittest.main()
