# Tests the routes and database connection of the flask application
# NOTE: app, db, dbData import MUST BE UNDER sys.path.append. Relative import
# is still buggy at the moment. -> To fix <-
import unittest
import sys
import time
sys.path.append(".")
from tester_webapp import app, db, dbData


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        db.session.close()
        db.drop_all()
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def create_request_flask(self, requested_by, env_id, test_path):
        """
        Creates a request based on the database model
        """
        request = dict(request_id=1,
                       requested_by=requested_by,
                       created_at='---',
                       env_id=env_id,
                       test_path=test_path,
                       status="status",
                       details="details")
        return request

    def create_dbEntry(self, requested_by, created_at, env_id):
        NewTest = dbData(requested_by=requested_by,
                         created_at=created_at,
                         env_id=env_id,
                         test_path="Tests",
                         status="MockStatus",
                         details="MockDetails")
        return NewTest

    # Tests:

    def test_database(self):
        """
        Test database copy, read, update, delete
        """
        # Test Adding an entry to the database
        Entry1 = self.create_dbEntry("Mock1", "9999-99-99 00:00:00", 101)
        db.session.add(Entry1)
        db.session.commit()
        TestList = dbData.query.all()
        self.assertIn(Entry1, TestList)

        # Test Updating an entry in the database
        get_NewTest = dbData.query.filter_by(
            created_at="9999-99-99 00:00:00").first()
        get_NewTest.status = "Testing"
        db.session.commit()
        get_NewTest = dbData.query.filter_by(
            created_at="9999-99-99 00:00:00").first()
        self.assertEqual("Testing", get_NewTest.status)

        # Test Removing an entry from the database
        get_NewTest = dbData.query.filter_by(
            created_at="9999-99-99 00:00:00").first()
        db.session.delete(get_NewTest)
        db.session.commit()
        TestList = dbData.query.all()
        self.assertNotIn(Entry1, TestList)

    def test_run_list(self):
        """
        Test main page
        """
        # Test basic response
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/test-run-list.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Test correct form post - test runs
        form_correct = self.create_request_flask(
            "MockPost", 99, "Tests/TrueTest.py")
        response = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_correct)
        time.sleep(0.5)
        # refresh page
        response = self.app.get('/test-run-list.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MockPost", response.data)
        self.assertIn(99, response.data)
        self.assertIn(b"Tests/TrueTest.py", response.data)
        # Cleanup
        get_NewTest = dbData.query.filter_by(requested_by="MockPost").first()
        db.session.delete(get_NewTest)
        db.session.commit()

        # Test correct form post - environment blocked (99)
        Entry1 = self.create_dbEntry("MockPost", "9999-99-99 00:00:00", 99)
        Entry1.status = "RUNNING"
        db.session.add(Entry1)
        db.session.commit()
        form_correct = self.create_request_flask(
            "MockPost2", 99, "Tests/TrueTest.py")
        response = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_correct)
        # # refresh page
        # response = self.app.get('/test-run-list.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"MockPost2", response.data)
        msg = "Test Environment 99 is currently busy! "\
              "Please choose a different one."
        self.assertIn(bytearray(msg, 'utf-8'), response.data)
        # Cleanup
        db.session.delete(Entry1)
        db.session.commit()

        # Test incorrect form post
        # Wrong EnvID, name too short, test does not exist
        form_false = self.create_request_flask("a", 101, "does-not-exist")
        response_false = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_false)
        self.assertEqual(response_false.status_code, 200)
        self.assertIn(b'Field must be between 2 and 20 characters long.',
                      response_false.data)
        self.assertIn(b'Number must be between 1 and 100.',
                      response_false.data)
        msg = 'Test does not exist! Please choose an'\
              'existing test file or directory!'
        self.assertIn(bytearray(msg, 'utf-8'), response_false.data)

        # Test partly empty post : NOTHING, correct, correct
        form_correct = self.create_request_flask([], 1, "Tests")
        response_false = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_correct)
        self.assertNotIn(b'Field must be between 2 and 20 characters long.',
                         response_false.data)
        self.assertNotIn(b'Number must be between 1 and 100.',
                         response_false.data)
        msg = 'Test does not exist! Please choose an'\
              'existing test file or directory!'
        self.assertNotIn(bytearray(msg, 'utf-8'), response_false.data)
        self.assertIn(b'This field is required.', response_false.data)

        # Test partly empty post : correct, NOTHING, correct
        form_correct = self.create_request_flask("Someone", [], "Tests")
        response_false = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_correct)

        self.assertNotIn(b'Field must be between 2 and 20 characters long.',
                         response_false.data)
        self.assertNotIn(b'Number must be between 1 and 100.',
                         response_false.data)
        self.assertNotIn(bytearray(msg, 'utf-8'), response_false.data)
        self.assertIn(b'This field is required.', response_false.data)

        # Test partly empty post : correct, correct, NOTHING
        form_correct = self.create_request_flask("Someone", 1, [])
        response_false = self.app.post(
            '/test-run-list.html', follow_redirects=True, data=form_correct)
        self.assertNotIn(b'Field must be between 2 and 20 characters long.',
                         response_false.data)
        self.assertNotIn(b'Number must be between 1 and 100.',
                         response_false.data)
        self.assertNotIn(bytearray(msg, 'utf-8'), response_false.data)
        self.assertIn(b'This field is required.', response_false.data)

        # Test Reading rows
        Entry1 = self.create_dbEntry("Mock1", "9999-99-99 11:11:11", 101)
        Entry2 = self.create_dbEntry("Mock2", "9999-99-99 22:22:22", 102)
        Entry3 = self.create_dbEntry("Mock3", "9999-99-99 33:33:33", 103)
        db.session.add_all([Entry1, Entry2, Entry3])
        db.session.commit()
        response = self.app.get('/test-run-list.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mock1", response.data)
        self.assertIn(b"Mock2", response.data)
        self.assertIn(b"Mock3", response.data)
        self.assertIn(b"9999-99-99 11:11:11", response.data)
        self.assertIn(b"9999-99-99 22:22:22", response.data)
        self.assertIn(b"9999-99-99 33:33:33", response.data)
        self.assertIn(b"101", response.data)
        self.assertIn(b"102", response.data)
        self.assertIn(b"103", response.data)
        for i in range(3):
            date = str(f"9999-99-99 {i+1}{i+1}:{i+1}{i+1}:{i+1}{i+1}")
            get_NewTest = dbData.query.filter_by(created_at=date).first()
            db.session.delete(get_NewTest)
        db.session.commit()
        response = self.app.get('/test-run-list.html', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Mock1", response.data)
        self.assertNotIn(b"Mock2", response.data)
        self.assertNotIn(b"Mock3", response.data)

    def test_list_details(self):
        """
        Test Show Details page
        """
        Entry1 = self.create_dbEntry("Mock4", "9999-99-99 44:44:44", 101)
        Entry1.request_id = 999999
        db.session.add(Entry1)
        db.session.commit()
        data = {"requested_by": "999999"}
        response = self.app.post('/test-run-detail.html',
                                 follow_redirects=True, data=data)
        self.assertIn(b"Test details", response.data)
        self.assertIn(b"Mock4", response.data)
        self.assertIn(b"101", response.data)
        self.assertIn(b"MockStatus", response.data)
        self.assertIn(b"MockDetails", response.data)
        db.session.delete(Entry1)
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
