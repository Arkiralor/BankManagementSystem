# Bank Management System Backend API

A demonstrative management system for a single bank, written in Python/Django.

This is not the software that a bank's customer might use to manage their account(s) rather, this is the software that would be used by the employees of the bank to manage day-to-day activities of the bank, such as:

1. Registering new customers
   1. Recording their KYC details
2. Creating/Requisitioning accounts for customers.
3. Recording transactions to and from bank accounts.
   - _For simplicity's sake, we have envisioned a world/reality in which the bank using this system is the only bank in the world so we do not need to manage branches or external bank transfers._

## Stack

The sub-techstack for the backend, specifically is as follows:

1. The core language in which it is written in, is Python, specifically the `CPython` variant.
2. The framework used for Python (_I am not masochistic enough to implement everything myself, from scratch_) is [Django](https://some-domain.com), extended via [Django-RestFramework](https://some-domain.com).
3. Long-term (_non-archival_) and operational data (_data used by the system to execute its main functions_) storage for critical tasks is done via a relational database, specifically: PostgreSQL as it is the most advanced, reliable and extensible RDBMS in the market as of writing this (c. 2023)
4. Non-structured data-warehousing and storage of non-critical data is accomplished via a noSQL database, specifically: MongoDB.
5. Dependencies for Python are managed by `setup-tools` via a `requirements.in` file.

## Setup

Please make sure the pre-requisites are satisfied before proceeding with the development environment setup.

### Pre-Requisites

1. __Console:__ [Bash](https://some-domain.com)
   - [GitBash](https://some-domain.com) for Windows
2. __Language Compiler/Interpreter:__ [Python v3.9 (CPython)](https://some-domain.com)
   - I have no idea if PyPI will work; it was created via CPython.
3. __Relational Database Management System:__ [PostgreSQL](https://some-domain.com) and [PGAdmin4](https://some-domain.com)
   - While PGAdmin is not strictly necessary, it makes working with PostgreSQL a whole lot easier.
4. __noSQL Database Management System:__ [MongoDB Community](https://some-domain.com) and [MongoDB Compass](https://some-domain.com)
   - Same case as PGAdmin; while compass is not strictly necessary, it makes the whole ordeal a lot simpler.

### Development Setup

1. Create a new virtual environment using: `python -m venv env`
2. Activate the virtual environment using: `source env/bin/activate`
    - `source env/Scripts/activate` in Windows.
3. Install the dependency management package via: `python -m pip install pip-tools`
4. Install the listed dependencies by running: `sh scripts/install_dependencies.sh`
   1. In UNIX systems, you might need to run `sudo chmod +x scripts/*.sh` before executing the script mentioned above to give it and the rest of the shell-scripts execution permission(s).
5. Create instances of a PostgreSQL database and a MongoDB cluster.
6. Copy the `.env` file for the backend into the folder and fill the values as per your local configuration.
7. Create any new required migrations for the RDBMS using: `python manage.py makemigrations`
8. Run said migrations for the RDBMS using: `python manage.py migrate`
9. Create a new Superuser or Administrator using: `python manage.py createsuperuser`

    ___FOR LOCAL DEV MACHINE ONLY___

    ```sh
    USERNAME: admin
    EMAIL: admin@admin.com
    PASSWORD: password
    ```

10. If they do not exist; create the `static` and `media` directories by running the following commands.

    ```sh
    mkdir static
    mkdir media
    ```

11. Run `python manage.py collectstatic --no-input` to collate the necessary `static` files.

12. Run `sh scripts/run_server.sh` to start the development server.

### .ENV File Format

The following is the format used by the `.env` file mentioned above.

```env
## General Settings:
APP_NAME = "The name of your application"
DOMAIN_URL = "The domain of your application"
OWNER_EMAIL = "Your official email address"
CONTACT_EMAIL = "Contact email for your application"


## System Settings:
SECRET_KEY = "Secret key for site encryption (one-way)"
DEBUG = True | False
ENV_TYPE = "DEV" | "PROD" | "TEST" | "QA"
ALLOWED_HOSTS = "host 1, host 2, host 3, host 4, ..."
JWT_ALGORITHM = "HS256"
CORS_ORIGIN_WHITELIST = "origin 1, origin 2, origin 3, origin 4, ..."

## Database Settings:
DB_NAME = "Name of SQL database"
DB_HOST = "Host for SQL database"
DB_PORT = "Posrt for SQL database"
DB_USER = "Username for SQL database"
DB_PASSWORD = "Password for SQL database"

## MongoDB Settings:
MONGO_URI = "URI for MongoDB"
MONGO_NAME = "Name of MongoDB cluster"
MONGO_HOST = "Host for MongoDB cluster"
MONGO_PORT = "Port for MongoDB cluster"
MONGO_USER = "Username for MongoDB cluster"
MONGO_PASSWORD = "Password for MongoDB cluster"

## Internationalization Settings:
LANGUAGE_CODE = " "
TIME_ZONE = " "
USE_I18N = True | False
USE_TZ = True | False

## Authentication Settings:
OTP_ATTEMPT_LIMIT = How many login attempts before being blocked
OTP_ATTEMPT_TIMEOUT = How long to block for

## Amazon Web Services Settings:
SNS_SENDER_ID = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_ARN = ""
```

## Documentation

1. [Postman](https://documenter.getpostman.com/view/17779018/2s93sjT8DE)
2. [JSON](../docs/backend/backend_postman_collection.json)
