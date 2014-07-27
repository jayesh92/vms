VMS
===

Volunteer Management System, Django Project.<br />
This contains Admin functionality for:<br />
  - Registering Users as Admin<br />
  - Login/Logout<br />
  - Create Events<br />
  - Create Jobs inside each event<br />
  - Assign Jobs to Volunteers in forms of shifts<br />
  - Search jobs by event OR time for volunteers and ablility to volunteer<br />
  - Generation of reports by various parameters<br />

Future Work:<br />
  - Enhance Reporting in terms of more data<br />
  - Add PDF export option to reports<br />
  - Error Reporting on forms for adding multiple shifts for same volunteer<br />
  - Error Reporting on forms for adding same job multiple times for an event<br />
  - Add client tests in test.py for forms<br />

To Run: <br />

Install Django: pip install Django==1.6.5 <br />

Assuming, git is installed on your Linux or MAC OS machine, execute git clone https://github.com/jayesh92/vms-1.git <br />

cd vms-1 <br />

cd VMS/templates<br />

pwd<br />
Copy output of previous command

cd .. <br />

vim settings.py <br />
Replace path on line number 34 to path copied from previously<br />

cd ..<br />
python manage.py runserver<br />

Point your browser to 127.0.0.1:8000/AdminUnit<br />

If you have Django installed, clone this repo and run the following commands: <br/>
 - python manage.py syncdb<br />
 - python manage.py runserver<br />
 
If prompted for admin id/password during first command, enter yes and enter any credentials whom you want to be the super admin <br/>
After second step, point your browser to 127.0.0.1:8000/admin or 127.0.0.1:8000/AdminUnit
