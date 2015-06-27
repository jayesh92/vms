# Automated Testing for VMS

The QA process is divided as follows:

- Continuous Intergation: Used travis to setup CI for VMS Project
- Functional Testing: Used Selnium to write UI tests from an end-users perspective.(black-box tests)
- Unit Testing: Valeria is writing unit-tests for the codebase.(white-box tests)

## Few important points regarding CI:

- `.travis.yml` is the config file to run the travis build
- Build can be viewed at `http://travis.org/jayesh92/vms`
- Status would be reflected in the badge in `README.md`

## Few important points regarding Functional Testing:

- Selenium, a browser automation tool is used to simulate the functionality.
  python APIs for selnium are used in the tests.

- Django provides a class `LiveServerTestCase`. What this does is that, It
  setups a Virtual Django Sever in the background which can be used by 
  selenium to run tests.

- So, each testcase Class inherits `LiveServerTestCase`, Contains a `setUp`
  and `tearDown` method to instantiate and end live-server respectively.
  Each testcase in the class begins with `test`.

- Each Test Class covers a view. Class name represents the name of the view
  in nav-bar. Test suite for a view is contained in `tests` folder of the app
  containing the view. For Ex: `Volunteer Search` tab in the nav-bar of an
  admin user redirects to `http://127.0.0.1:8000/volunteer/search/`, so 
  the corresponding tests for this view would be in `VolunteerSearch` class
  in `tests` folder of `volunteer` app.

- Each app contains a `tests` folder containing the unit-tests and functional
  tests and an `__init__.py` to let django consider it as a package.

- Currently, only functional tests for admin views have been written.

## Steps to run tests:

- Currently, used `python 2.7`
- Clone project: `git clone https://github.com/jayesh92/vms.git`
- In the root folder of the project, startup a new virtual environment
  `virtualenv -p /usr/bin/python2.7 venv`
- Activate virtualenv, `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- `cd vms`
- To run, `python manage.py runserver`. Browse 
  `http://127.0.0.1:8000/home`
- To execute tests `python manage.py test`. This will run all unit-tests and
  all functional-tests across all apps. To execute tests of only a particular
  app, run `python manage.py test <app_name>`
- If all tests pass, `OK` will be received at the end.
- For functional tests, a firefox window for each test will open up
  automatically and close after simulation of tests.
