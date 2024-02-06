import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc
import unittest


class TestBackEnd(unittest.TestCase):
    def test_create_tasks(self):
        test_data = {"task_1": "test the back end", "hello task": "hello world"}
        backend_file.create_tasks(test_data)

    def test_create_task_by_name_and_description(self):
        test_task_name = "test_2"
        test_task_description = "testing this task now"
        backend_file.create_task_by_name_and_description(test_task_name, test_task_description)
        self.assertEqual(test_task_name in backend_file.to_do_tasks, True)
        self.assertEqual(backend_file.to_do_tasks[test_task_name], test_task_description)
        self.assertEqual(len(backend_file.to_do_tasks), 1)
        self.assertRaises(mvc_exc.TaskNameOnCreationAlreadyExists,
                          backend_file.create_task_by_name_and_description,
                          test_task_name, test_task_description)

    def test_read_task_by_named_key(self):
        test_data = {"task_1": "test the back end", "hello task": "hello world"}
        backend_file.create_tasks(test_data)
        test_task_name_should_fail = "task_2"
        test_task_name = "task_1"
        test_task_description = "test the back end"
        self.assertEqual(backend_file.read_task_by_named_key(test_task_name), test_task_description)
        self.assertRaises(mvc_exc.TaskNameOnReadDoesNotExist,
                          backend_file.read_task_by_named_key,
                          test_task_name_should_fail)

    def test_read_all_tasks(self):
        test_data = {"task_1": "test the back end", "hello task": "hello world"}
        expected_test_list = [("task_1", "test the back end"), ("hello task", "hello world")]
        backend_file.create_tasks(test_data)
        self.assertEqual(backend_file.read_all_tasks(), expected_test_list)

    def test_update_task_given_keyed_name(self):
        test_data = {"task_1": "test the back end", "hello task": "hello world"}
        backend_file.create_tasks(test_data)
        test_task_name_should_fail = "task_2"
        test_task_name = "task_1"
        test_task_description = "test the back end"
        backend_file.update_task_given_keyed_name(test_task_name, test_task_description)
        self.assertEqual(backend_file.to_do_tasks[test_task_name],
                         test_task_description)
        self.assertRaises(mvc_exc.TaskNameOnUpdateDoesNotExist,
                          backend_file.update_task_given_keyed_name,
                          test_task_name_should_fail,
                          test_task_description)

    def test_delete_task_given_keyed_name(self):
        test_data = {"task_1": "test the back end", "hello task": "hello world"}
        backend_file.create_tasks(test_data)
        test_task_name_should_fail = "task_2"
        test_task_name = "task_1"
        self.assertRaises(mvc_exc.TaskNameOnDeleteDoesNotExist,
                          backend_file.delete_task_given_keyed_name,
                          test_task_name_should_fail)
        backend_file.delete_task_given_keyed_name(test_task_name)
        self.assertTrue(test_task_name not in backend_file.to_do_tasks)


if __name__ == "__main__":
    unittest.main()
