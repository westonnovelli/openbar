#OpenBAR
###Breakthrough Academic Resources

##App Description
The application is broken down into three 'apps' (that's Django's name for it), think of them as modules:
* openbar - main module that contains the settings and configurations
* openbar_search - secondary module that encapsulates the search feature
* openbar_users - secondary module that encapsulates the user management feature

The top level of the application has these three module directories and one extra one: templates/ This directory holds
all of the front end templates

#####How to run the app
Django provides a built-in webserver. A browser makes requests to this server which routes the calls into the
application code (the stuff we are writing) which then responds back and (often) returns a template to render in the
browser.

To start the application you have to start the server locally on your machine.
```bash
python manage.py runserver
```
The manage.py file is the interface for talking to the application. If you run
```bash
python manage.py help
```
You will see all that it can do.

#####How to develop in the app
Most of the application is written in Python, so you need to know your way around that. Templates use a composite
between django's python based templating language and html.

The main module has a settings.py file that defines the configuration for the entire application, for example, the
INSTALLED_APPS variable defines the apps (modules) that are used in the whole application. If you were to make
openbar_newFeature you would add it to this list.

Also within the main modules is the urls.py file. This is what routes the http requests from the browser to the
controller objects (referred to as views in Django). The controllers then interact with the models and respond with
templates. Django models an MVC (model, view, controller paradigm); this is confusing, however, because of naming
conventions, in Django terms it would be a MTV (model, template, view). Nevertheless the paradigm stays the same:
templates talk to views which talk to models; models should never talk to templates directly.

#####Working with a Database
Django defaults to a sqlite3 database. This works perfect for us, its simple, yet powerful. It store the data in a
single files which is compact and easy to manage.

When working with databases, you define a schema or blueprints of what the data will look like. These blueprints are
based on the models (which is the data being stored in the db). When changes are made to the models, you must change
the database schema. When you have a database that is running in production, you have to be careful not to lose data
that is already in the database. To handle this, we have database migrations. These are instructions for the database
to update it's schema. So if you make changes to the models, you have to make and run the migrations to keep the
database up to date.

To make migrations, run:
```bash
python manage.py makemigrations
```

To then run those migrations, run:
```bash
python manage.py migrate
```

Be sure to do this every time you make a model change, or the application will break.
