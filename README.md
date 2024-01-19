

# CINEMASH SERVER


# Usage Instructions


Install the local dependencies, run migrations, and start the server.


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/romanmay7/cinemash-server.git
    $ cd {{ cinemash-server }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    	
    $ python manage.py migrate
	
Create Super User:

    $ python manage.py createsuperuser 

You can now run the development server:

    $ python manage.py runserver
