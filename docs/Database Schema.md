# Database Schema

The following include the models that define the database schema, its purpose, an explanation of non-trivial fields and a description of model relationships.

## Administrator Model

```
class Volunteer(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    country = models.CharField()
    phone_number = models.CharField()
    unlisted_organization = models.CharField()
    organization = models.ForeignKey(Organization)
    email = models.EmailField(max_length=20)
    user = models.OneToOneField(User)
```
### Purpose

The Administrator model is used to represent an administrator.

### Explanation of non-trivial fields

`Organization` - The organization that an administrator is associated with.

`unlisted_organization` - If the administrator is not associated with an organization in the Organization table in the database, then this field is filled in instead.

### Relationships

1) One-to-One between Administrator and Django auth_user.

2) One-to-Many from Organization to Administrator.

## Volunteer Model

```
class Volunteer(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    country = models.CharField()
    phone_number = models.CharField()
    unlisted_organization = models.CharField()
    organization = models.ForeignKey(Organization)
    email = models.EmailField(max_length=20)
    websites = models.TextField()
    description = models.TextField()
    resume = models.TextField()
    resume_file = models.FileField()
    user = models.OneToOneField(User)
```
### Purpose
The Volunteer model is used to represent a volunteer.

### Explanation of non-trivial fields

`Organization` - The organization that a volunteer is associated with.

`unlisted_organization` - If the volunteer is not associated with an organization in the Organization table in the database, then this field is filled in instead.

`websites` - Contains URLs to a volunteer's online profiles (such as GitHub or a personal website).

`description` - Contains a volunteer's biography.

`resume` - Holds the file name of an uploaded resume.

`resume_file` - Holds the path name to the resume stored in the file system of the server.

### Relationships

1) One-to-One between Volunteer and Django auth_user.

2) One-to-Many from Organization to Volunteer.

## Organization Model

```
class Organization(models.Model):
    organization_name = models.CharField(max_length=45)
```
### Purpose

The Organization table contains Anita Borg Institute partners which can be viewed [here](http://anitaborg.org/partner-with-us/our-partners/).

An Organization may make matching monetary donations to the Anita Borg Institute according to their employee's volunteer hours. Please see the Requirements document for more details.

### Relationships

1) One-to-Many from Organization to Administrator.

2) One-to-Many from Organization to Volunteer.

## Event, Job, Shift, VolunteerShift Example

The following example may assist in understanding the Event, Job, Shift and VolunteerShift models described below:

```
Event Name: Open Source Conference
Date Range of Reception Job: October 15th to October 31st

    Jobs for Open Source Conference Event:

    Job 1 Name: Reception
    Date Range of Reception Job: October 15th to October 25th

        Shifts for Reception Job:

        Shift 1 is on October 15th from 3:00pm to 4:00pm
        Shift 2 is on October 15th from 3:30pm to 5:00pm
        Shift 3 is on October 17th from 9:00am to 10:00am
        Shift 4 is on October 25th from 10:00am to 1:00pm

    Job 2 Name: Greeter
    Date Range of Greeter Job: October 8th to October 31st

        Shifts for Greeter Job:

        Shift 1 is on October 9th from 1:00pm to 3:00pm
        Shift 2 is on October 11th from 5:00pm to 4:00pm
        Shift 3 is on October 12th from 10:00am to 11:00am

Event Name: Python Conference
Date Range of Python Conference: April 12th to April 14th

    Jobs for Python Conference Event:

    Job 1 Name: Registration
    Date Range of Registration Job: April 12th to April 14th

        Shifts for Registration Job:

        Shift 1 is on April 12th from 8:00pm to 9:00pm
        Shift 2 is on April 12th from 8:30pm to 10:00pm
        Shift 3 is on April 13th from 7:00am to 11:00am
        Shift 4 is on April 24th from 11:00am to 2:00pm

    Job 2 Name: Organizer
    Date Range of Organizer Job: April 12th to April 13th

        Shifts for Organizer Job:

        Shift 1 is on April 12th from 3:00pm to 5:00pm
        Shift 2 is on April 13th from 2:00pm to 3:00pm
        Shift 3 is on April 13th from 11:00am to 11:30am
```
## Event Model

```
class Event(models.Model):
    name = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
````

### Purpose

The Event model is used to represent an event.

### Relationships

1) One-to-Many from Event to Job (an Event can contain many Jobs).

## Job Model

```
class Job(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
````

### Purpose

The Job model is used to represent a job.

### Explanation of non-trivial fields

`start_date` - Indicates the start date of a job that has been **scheduled** by the administrator.

`end_date` - Indicates the end date of a job that has been **scheduled** by the administrator.

Jobs occur within a `start_date` and `end_date` date range.

### Relationships

1) One-to-Many from Job to Shift (a Job can contain many Shifts).

2) One-to-Many from Event to Job (an Event can contain many Jobs).

## Shift Model

```
class Shift(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_volunteers = models.PositiveSmallIntegerField()
    job = models.ForeignKey(Job)
    #VolunteerShift is the intermediary model for the many-to-many relationship between Volunteer and Shift
    volunteers = models.ManyToManyField(Volunteer, through=’VolunteerShift’)
```
### Purpose

The Shift model is used to represent a shift.

### Explanation of non-trivial fields

`start_time` - Indicates the start time of a shift that has been **scheduled** by the administrator.

`end_time` - Indicates the end time of a shift that has been **scheduled** by the administrator.

Shifts occur within a `start_time` and `end_time` time range. These are scheduled times that give the volunteer that has signed up for a shift an indication of the time they need to start and end their shift.

`max_volunteers` - Indicates the maximum number of volunteers that can be signed up for a particular shift (since multiple volunteers can sign up for the same shift).

### Relationships

1) One-to-Many from Shift to VolunteerShift.

2) One-to-Many from Job to Shift (a Job can contain many Shifts).

## VolunteerShift Model

```
class VolunteerShift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    volunteer = models.ForeignKey(Volunteer)
    shift = models.ForeignKey(Shift)
```

### Purpose

The VolunteerShift model is required since there is a Many-to-Many relationship between Volunteer and Shift. There is a Many-to-Many relationship between Volunteer and Shift because Volunteers can be signed up for multiple Shifts and Shifts may include (be served by) multiple Volunteers.

**The VolunteerShift model is used to keep track of the Shifts a Volunteer is signed up for.**

When a Volunteer signs up for a Shift, a new record/row is added to the VolunteerShift table in the database that associates the Volunteer with the Shifts that they signed up for via the primary key of the VolunteerShift table which is `(volunteer_id, shift_id)`.

### Explanation of non-trivial fields

`start_time` - Indicates the start time **logged** by the volunteer. It is the time that the volunteer actually started their shift.

`end_time` - Indicates the end time **logged** by the volunteer. It is the time that the volunteer actually ended their shift.

`start_time` and `end_time` are logged by the volunteer after they have completed their Shift. `start_time` and `end_time` can be thought of as **logged** times (similar to a punch card). Volunteer hours are calculated based on the difference between the `end_time` and the `start_time`.

### Relationships

1) One-to-Many from Volunteer to VolunteerShift (since a Volunteer can be signed up for multiple Shifts).

2) One-to-Many from Shift to VolunteerShift (a Shift can be served by multiple Volunteers).
