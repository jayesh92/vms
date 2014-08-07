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

Install Django:
  - $> sudo pip install Django==1.6.5 <br />

Also Run:
  - $> sudo pip install django-google-charts

Assuming, git is installed on your Linux or MAC OS machine, execute git clone https://github.com/jayesh92/vms-1.git <br />

  - python manage.py syncdb<br />
  - python manage.py runserver<br />

Point your browser to 127.0.0.1:8000/AdminUnit<br />

Login Details: <br />

Username : vol1 <br />
Password : vol1 <br />

Replace 1 in username, password to any digit from 1 to 6 , all have been given admin access <br />
