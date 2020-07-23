import os
import glob
import logging
import subprocess
import time
# from flask import flash


# ###
# Database helper functions
# ###
def db_addNewEntry(db, dbModel, Entry):
    """
    Adds a new entry to the database
    """
    NewTest = dbModel(requested_by=Entry.requested_by.data,
                      created_at=Entry.created_at,
                      env_id=Entry.env_id.data,
                      test_path=Entry.test_path.data,
                      status="RUNNING")
    db.session.add(NewTest)
    db.session.commit()


def db_getReqIdFromForm(db, dbModel, form):
    """
    Gets the request id of the form based on the time and environment number
    """
    dbEntry = db.session.query(dbModel).filter_by(
        created_at=str(form.created_at), env_id=form.env_id.data).first()
    return dbEntry.request_id


def db_getRequestIdData(db, dbModel, request_id):
    """
    Return the database row corresponding to request_id
    """
    return db.session.query(dbModel).filter_by(request_id=request_id).first()


def db_checkEnv(db, dbModel, chosenEnv):
    """
    Queries the database in search for a running instance on chosenEnv
    """
    # This querey returns a list containing all instances that match the filter
    Query = db.session.query(dbModel).filter_by(
        env_id=chosenEnv, status="RUNNING").all()

    if not Query:
        return False
    elif len(Query) == 1:
        return True
    elif len(Query) >= 1:
        logging.warning(
            "MULTIPLE RUNNING INSTANCES ON ONE ENV! Should not be possible!")
        return True


def db_updateStatusByReqId(db, dbModel, newStatus, request_id, env_id):
    """
    Updates the status and details of the entry with the given current
    request_id. The Details are read from the file
    """
    Entry = db.session.query(dbModel).filter_by(
        request_id=request_id).first()
    Entry.status = newStatus
    Entry.details = getTestDetails(env_id)
    db.session.commit()


# ###
# Test Execution helper functions
# ###
def GetTestsAsModules(test_path):
    """
    Creates a file list with all the tests from test_path. The format of the
    list entries is changed such that the files are callable as modules
    (Extensions are removed and "/" are replaced by ".")
    """
    FileList = []
    test_path = "PyTests/" + test_path

    # Single file input
    if test_path.endswith(".py"):
        # Remove extension and replace "/"
        test_path = os.path.splitext(test_path)[0]
        test_path = test_path.replace("/", ".")
        FileList.append(test_path)

    else:
        # Directory input
        if not test_path.endswith("/"):
            test_path = test_path + "/"

        for file in os.listdir("tester_webapp/" + test_path):
            if file.endswith(".py") and not file.startswith("__"):
                # Remove extension and replace "/"
                path = os.path.splitext(test_path + file)[0]
                path = path.replace("/", ".")
                FileList.append(path)

    return FileList


def getTestDetails(env_id):
    """
    Returns a string containig all logs made in the env_id folder
    """
    test_path = str(f"tester_webapp/env/{env_id}/")
    logs = ""

    for file in os.listdir(test_path):
        if file.endswith(".log"):
            with open(test_path+file, 'r') as file:
                logs += file.read()
        logs += "\n"
    return logs


def deleteLogs(env_id):
    """
    Deletes the logs created by the tests
    """
    files = glob.glob(f'tester_webapp/env/{env_id}/*')
    for file in files:
        if file.endswith(".log"):
            os.remove(file)


def callSubProcess(FileList, env_id):
    """
    Calls a subprocess to run all tests in FileList and returns
    errorFound (bool).
    """
    processpath = os.getcwd() + str(f"/tester_webapp/env/{env_id}/")
    errorFound = False
    logging.info(f"Started subprocess in environemnt {env_id} !")

    for file in FileList:
        try:
            logging.info(f"Starting Process {file} !")
            path_testRunner = str(
                f"{os.getcwd()}/tester_webapp/call_testRunner.py")
            cmd = ["python", path_testRunner, "-file", file]
            subprocess.check_output(
                cmd, cwd=processpath, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as e:
            logging.info(e)
            errorFound = True
            logging.info(f"Process {file} has failed !")

        else:
            logging.info(f"Process {file} has suceded !")

    return errorFound


def RunTest(db, dbModel, form):
    """
    Runs a test/s from all the chosen files
    """
    TestFiles = GetTestsAsModules(form.test_path.data)
    db_addNewEntry(db, dbModel, form)
    time.sleep(1)  # Wait for db to update
    # Todo: add loop unti request_id != none and remove time.sleep
    request_id = db_getReqIdFromForm(db, dbModel, form)
    logging.info(f"Added new entry with ID: {request_id} to the database")

    errorFound = callSubProcess(TestFiles, form.env_id.data)
    if errorFound:
        logging.info(f"Tests with ID: {request_id} failed")
        db_updateStatusByReqId(db, dbModel, "FAILED",
                               request_id, form.env_id.data)
        logging.info(f"Updated Status of {request_id} to \"FAILED\"")

    else:
        logging.info(f"Test with ID: {request_id} succeeded!")
        db_updateStatusByReqId(db, dbModel, "SUCCEED",
                               request_id, form.env_id.data)
        logging.info(f"updated Status of {request_id} to \"SUCCEED\"")
    deleteLogs(form.env_id.data)
