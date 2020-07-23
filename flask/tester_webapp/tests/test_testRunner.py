# Tests the routes and database connection of the flask application
# NOTE: app, db, dbData import MUST BE UNDER sys.path.append. Relative import
# is still buggy at the moment. -> To fix <-
import unittest
import sys
sys.path.append(".")
from tester_webapp.TestRunner import *
from tester_webapp.forms import New_Request
from tester_webapp import app, db, dbData


class FlaskFormSubclass():
    def __init__(self, data):
        self.data = data


class FlaskFormSim():
    """
    FlaskForm Simulation
    """

    def __init__(self, requested_by, created_at, env_id, test_path, details):
        self.requested_by = FlaskFormSubclass(requested_by)
        self.created_at = created_at
        self.env_id = FlaskFormSubclass(env_id)
        self.test_path = FlaskFormSubclass(test_path)
        self.details = FlaskFormSubclass(details)


class testRunnerTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # db.session.close()
        # db.drop_all()
        # db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_db_helpers(self):
        """
        Test all database helper functions
        """
        created_at = "8888-88-88 00:00:00"
        form = FlaskFormSim("Mock", created_at, 101, "MockPath", None)

        # Test db_addNewEntry
        db_addNewEntry(db, dbData, form)
        db_entry = dbData.query.filter_by(created_at=created_at).first()
        self.assertEqual(form.requested_by.data, db_entry.requested_by)
        self.assertEqual(form.created_at, db_entry.created_at)
        self.assertEqual(form.env_id.data, db_entry.env_id)
        self.assertEqual(form.test_path.data, db_entry.test_path)
        self.assertEqual(form.details.data, db_entry.details)

        # Test db_getReqIdFromForm
        req_id = db_getReqIdFromForm(db, dbData, form)
        db_query = db.session.query(dbData).filter_by(
            created_at=created_at, env_id=101).first()
        db_query = db_query.request_id
        self.assertEqual(req_id, db_query)

        # Test db_getRequestIdData
        request_id_data = db_getRequestIdData(db, dbData, req_id)
        db_query = db.session.query(dbData).filter_by(
            request_id=req_id).first()
        self.assertEqual(request_id_data, db_query)

        # Test db_checkEnv
        status = db_checkEnv(db, dbData, 101)
        self.assertTrue(status)
        status = db_checkEnv(db, dbData, 102)
        self.assertFalse(status)

        # Test db_updateStatusByReqId
        db_updateStatusByReqId(db, dbData, "MockStatus",
                               req_id, form.env_id.data)
        db_query = db.session.query(dbData).filter_by(
            request_id=req_id).first()
        self.assertEqual(str(db_query.status), "MockStatus")

        # Test GetTestsAsModules(test_path) - a TrueTest and FalseTest file
        # must be under PyTests/MockTests/
        # test Folder input
        List = GetTestsAsModules("MockTests")
        expected = ['PyTests.MockTests.TrueTest']
        expected.append('PyTests.MockTests.FalseTest')
        self.assertListEqual(List, expected)
        # test single file input
        file = GetTestsAsModules("MockTests/TrueTest.py")
        self.assertListEqual(["PyTests.MockTests.TrueTest"], file)

        # Test getTestDetails
        # Note: Environment 101 is used for Testing. There are 2 Mock Logfiles
        details = getTestDetails(101)
        self.assertIn("MOCK LOG 1", details)
        self.assertIn("MOCK LOG 2", details)

        # Test callSubProcess
        File = "PyTests.MockTests."
        errorFound = callSubProcess([File + "TrueTest"], 100)
        self.assertEqual(errorFound, False)
        errorFound = callSubProcess([File + "FalseTest"], 100)
        self.assertEqual(errorFound, True)

        # Clean-up: Remove old form from database
        db.session.delete(db_entry)
        db.session.commit()

        # Test RunTest - chosen test fails
        form = FlaskFormSim("Mock", created_at, 100,
                            "MockTests/FalseTest.py", None)
        RunTest(db, dbData, form)
        db_query = db.session.query(dbData).filter_by(
            created_at=created_at).first()
        self.assertEqual(form.requested_by.data, db_query.requested_by)
        self.assertEqual(form.created_at, db_query.created_at)
        self.assertEqual(form.env_id.data, db_query.env_id)
        self.assertEqual(form.test_path.data, db_query.test_path)
        db.session.delete(db_query)
        db.session.commit()

        # Test RunTest - chosen test works
        form.test_path.data = "MockTests/TrueTest.py"
        RunTest(db, dbData, form)
        db_query = db.session.query(dbData).filter_by(
            created_at=created_at).first()
        self.assertEqual(form.requested_by.data, db_query.requested_by)
        self.assertEqual(form.created_at, db_query.created_at)
        self.assertEqual(form.env_id.data, db_query.env_id)
        self.assertEqual(form.test_path.data, db_query.test_path)
        db.session.delete(db_query)
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
