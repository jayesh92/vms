# Software Design

## Django Apps

**administrator** - Contains functionality associated with administrators (such as functionality to view settings and generate reports).

**authentication** - A module for basic authentication. Enables a user to log in, log out and register. This app is acting as a stub/mock app for authentication functionality. VMS will be integrated with the Systers Portal application in the future and will use the authentication app of Portal instead (since the authentication app of Portal is more complete in development).

**event** - Contains functionality associated with events (such as functionality to create, edit and delete events).

**home** - Contains code that implements the VMS homepage.

**job** - Contains functionality associated with jobs (such as functionality to create, edit and delete jobs).

**organization** - Contains functionality associated with organizations (such as functionality to create, edit and delete organizations).

**registration** - A module for registration functionality. Enables the creation of administrator and volunteer accounts.

**shift** - Contains functionality associated with shifts (such as functionality to sign up, add hours and cancel shifts).

**vms** - Contains a base template and project settings. **base.html** contains template elements that are present across all templates. **settings.py** specifies project wide settings.

**volunteer** - Contains functionality associated with volunteers (such as functionality to edit and view volunteer profiles).

## Application Architecture

Each app contains a template layer, a view layer (sometimes called a "controller" in other frameworks) and an additional services layer for business logic.

In particular, each Django app described above contains the following files:

**forms.py** - Contains Django Form classes. Using Django Form classes automates many aspects of developing forms. Developers can specify form fields and their types as well as regular expressions for server-side validation. These forms are automatically rendered as HTML by the Django framework. Forms can be easily processed and validated by the Django framework.

**models.py** - Contains Django Models that correspond to database tables. The command `python manage.py syncdb` will create database tables for a database (such as a PostgreSQL or MySQL database) that correspond to these models.

**services.py** - Contains business logic code.

A services layer was introduced in order to separate out the view (controller) code and the business logic code, making it easier to write integration/regression tests for the view layer and unit tests for the business logic layer.

Introducing a services layer also ensures that the Django app has proper separation of concerns, making the application more modular and easier to maintain.

**templates** directory - Contains template (HTML) code.

**tests.py** - Contains unit tests for each function in **services.py** using the Python [unittest](https://docs.python.org/3/library/unittest.html) unit testing framework.

**urls.py** - Specifies the URLs for the Django app.

**views.py** - Contains the view (controller) code of the Django app. It is responsible for processing a user's request and returning an appropriate response.
