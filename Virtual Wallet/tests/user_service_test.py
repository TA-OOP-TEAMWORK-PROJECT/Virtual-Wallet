import unittest


<<<<<<< Updated upstream
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
=======

def test_create_user_success(mocker):
    mocker.patch('services.user_service.auth.get_password_hash', return_value='hashed_password')
    mocker.patch('services.user_service.insert_query', side_effect=[1, None])
    mocker.patch('services.user_service.send_registration_email')
    mocker.patch('services.user_service.check_if_unique', return_value=None)
>>>>>>> Stashed changes


if __name__ == '__main__':
    unittest.main()
