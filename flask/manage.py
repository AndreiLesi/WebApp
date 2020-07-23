from flask.cli import FlaskGroup
from tester_webapp import app, db, dbData

cli = FlaskGroup(app)

@cli.command("createDB")
def createDB():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("createSampleDB")
def createSampleDB():
    """
    Creates a Database and fills it with sample entries
    """
    db.drop_all()
    db.create_all()

    Test1 = dbData(requested_by="SampleRequest",
                   created_at="1234-56-78 99:99:99",
                   env_id=1,
                   test_path="SampleTestPath",
                   details = "SampleDetails...",
                   status="SUCCEED")
    Test2 = dbData(requested_by="SampleRequest",
                   created_at="1234-56-78 99:99:99",
                   env_id=2,
                   test_path="SampleTestPath",
                   details = "SampleDetails...",
                   status="FAILED")
    Test3 = dbData(requested_by="SampleRequest",
                   created_at="1234-56-78 99:99:99",
                   env_id=3,
                   test_path="SampleTestPath",
                   details = "SampleDetails...",
                   status="SUCCEED")
    Test4 = dbData(requested_by="SampleRequest",
                   created_at="1234-56-78 99:99:99",
                   env_id=4,
                   test_path="SampleTestPath",
                   details = "SampleDetails...",
                   status="FAILED")
    Test5 = dbData(requested_by="SampleRequest",
                   created_at="1234-56-78 99:99:99",
                   env_id=5,
                   test_path="SampleTestPath",
                   details = "SampleDetails...",
                   status="SUCCEED")
    db.session.add_all([Test1, Test2, Test3, Test4, Test5])
    db.session.commit()

if __name__ == "__main__":
    cli()

