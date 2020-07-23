from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
import concurrent.futures as threads
from tester_webapp import app, db, dbData
from tester_webapp.forms import New_Request
from tester_webapp.TestRunner import db_checkEnv, db_getRequestIdData,\
    RunTest

# Used to run the tests in the background of the app
backgroundTask = threads.ThreadPoolExecutor()


@app.route("/", methods=['GET', 'POST'])
@app.route('/test-run-list.html', methods=['GET', 'POST'])
def test_run_list():
    form = New_Request()
    TableRows = dbData.query.order_by(dbData.request_id.desc()).all()

    if form.validate_on_submit():
        if db_checkEnv(db, dbData, form.env_id.data):
            flash(f'Test Environment {form.env_id.data} is currently busy! '
                  'Please choose a different one.', 'danger')

        else:
            form.created_at = datetime.today()
            flash(
                f'Test on Environment {form.env_id.data} started !', 'success')
            backgroundTask.submit(RunTest, db, dbData, form)
            # use RunTest for debugging. backgroundTask doesnt show errors or
            # flash messages
            # RunTest(db, dbData, form)
        return redirect(url_for("test_run_list"))

    print("Rediecting...")
    return render_template('test-run-list.html', title='Test Overview',
                           form=form, TableRows=TableRows)


@app.route("/test-run-detail.html", methods=['GET', 'POST'])
def test_run_detail():
    if request.method == 'POST':
        request_id = request.form['requested_by']
        test_data = db_getRequestIdData(db, dbData, request_id)

    return render_template('test-run-detail.html', test_data=test_data)
