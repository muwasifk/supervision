# Supervisor
The Supervisor is a web application running with a Django backend that allows administrators of high schools to generate a supervision schedule for their teachers easily. It reduces 30+ hours of manual work to just a few minutes. 

## Features
Through its easy-to-use platform, The Supervisor can:
* Parse teacher information either through manual input or CSV upload
* Generate valid calendar in milliseconds and view year-long calendar on the web app
* Export the calendar to CSV or ICS for easy editing

## Installation
Clone the repository to your local machine
```bash
git clone https://github.com/muwasifk/supervision/
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the root directory and place the following variables. For the values, use your own configuration of Supabase. 
```
SECRET_KEY=
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
DATABASE_HOST=
DATABASE_NAME=postgres
DATABASE_USER=
DATABASE_PORT=5432
DATABASE_PASSWORD=
```
To run the web application and to view it in your browser, run 
```bash
python manage.py runserver
```

## Known Bugs
At times, the sign in with google feature will not work on the log in page. If this happens, please use the sign in with google button in the home screen on the website OR type into the password box, delete it, and then try the button.

## Support
Please contact kchaw1@ocdsb.ca, mkamr4@ocdsb.ca, or esui1@ocdsb.ca for support or feature requests.
## Sources

**General Usage**
| [Flowbite](https://flowbite.com/docs/getting-started/introduction/) | | Used for tailwind documentation |
| [Supabase](https://supabase.com/docs) | | Used for connecting database to the Postgre frontend |
| [Adobe Express](https://www.adobe.com/express/create/logo) | | Used for logo and design creating |
| [Django Docs](https://docs.djangoproject.com/en/5.0/) | | Used for Django documentation |
| [Python hashlib](https://docs.python.org/3/library/hashlib.html) | | Used for Securing hashes and message digests |


**Features**
| [Google OAuth Tutorial #1](https://medium.com/@infowithkiiru/django-user-registration-with-google-67524cce5ab7) | | Used for creating a sign-in-with-google |
| [Google OAuth Tutorial #2](https://pylessons.com/django-google-oauth) | | Used for creating a sign-in-with-google |
| [Chat GPT](https://chat.openai.com/) | | Prompt: “I'd like to create a python code that creates a new csv, writes to it with specific data in the python file and has an export feature to download the new csv file” |
| [Ics.py](https://icspy.readthedocs.io/en/stable/) | | Used for creating ics calendar |

**Developer Side**
| [Environment Keys](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f) | | Used for protecting secret keys |
