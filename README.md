#Wheezy Teaser

Which we are creating at Ninjaas. This is written on `wheezy.web`

Installation:

+ Install the python `requirement.pip` with pip on virtualwrapper.
+ As this is a simple application we are using `SQLAlchemy` for storing the emails.

Emails:

+ CSS in the emails should be inline. They shouldn't be internal or external so we are using `premailer`

Running It:

1. Init the database. We are using SQLite. `python init_db.py`
2. Create a new file called the `local_setting` from `settings.py` to get your own email settings.
3. To run just use `python run.py`