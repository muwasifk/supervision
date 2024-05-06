# Supervisor
Supervisor is a jumpstart software platform for teacher supervision-scheduling ease.

## Features
Through its easy-to-use platform, supervisor can:
 - Import teacher data through CSV, or manual input as well.
 - Generate a UI Calendar for supervision schedules throughout the school year.
 - Allow for exporting the schedule into a CSV or ICS file (connected to Google Calendar).
 - Store old schedules for simple and easy access.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages:
```bash
pip install -r requirements.txt
```
Use the pip "install -r requirements.txt" command to install all of the Python modules and packages listed in the requirements.txt file. This saves time and effort.
## Known Bugs
At times, the sign in with google feature will not work on the log in page. If this happens, please use the sign in with google button in the home screen on the website OR type into the password box, delete it, and then try the button.

## Support
Please contact kchaw1@ocdsb.ca, mkamr4@ocdsb.ca, or esui1@ocdsb.ca for support or feature requests.
## Sources

**General Usage**
| [Flowbite](https://flowbite.com/docs/getting-started/introduction/) | | Used for tailwind documentation |
| [Supabase](https://supabase.com/docs) | | Used for connecting database to the Postgre frontend |
| [Adobe Express](https://www.adobe.com/express/create/logo) | | Used for logo and design creating |

**Features**
| [Google OAuth Tutorial #1](https://medium.com/@infowithkiiru/django-user-registration-with-google-67524cce5ab7) | | Used for creating a sign-in-with-google |
| [Google OAuth Tutorial #2](https://pylessons.com/django-google-oauth) | | Used for creating a sign-in-with-google |
| [Chat GPT](https://chat.openai.com/) | | Prompt: “I'd like to create a python code that creates a new csv, writes to it with specific data in the python file and has an export feature to download the new csv file” |

**Developer Side**
| [Environment Keys](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f) | | Used for protecting secret keys |
