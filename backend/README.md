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
2. The framework used for Python (_I am not masochistic enough to implement everything myself, from scratch_) is [Django](https://www.djangoproject.com/), extended via [Django-RestFramework](https://www.django-rest-framework.org/).
3. Long-term (_non-archival_) and operational data (_data used by the system to execute its main functions_) storage for critical tasks is done via a relational database, specifically: PostgreSQL as it is the most advanced, reliable and extensible RDBMS in the market as of writing this (c. 2023)
4. Non-structured data-warehousing and storage of non-critical data is accomplished via a noSQL database, specifically: MongoDB.
5. Task-queuing is implemented done in `Redis` via `rq` and connected to Django via `django-rq`.
6. Dependencies for Python are managed by `setup-tools` via a `requirements.in` file.

## Individual Applications

The following are the individual `django applications` created via the `python manage.py startapp <app name>` command. Non-app modules are not named here as they are only to _facilitate_ the working of these applications.

1. __[Admin](./admin_app/):__ Used to extend functionalities provided by Django to administrators via independent APIs.
2. __[Analytics](./analytics_app/):__ Used to provide analytics functionalities to moderators/analysts via APIs.
3. __[Banking](./banking_app/):__ Houses APIs to facilitate banking acitivies such as account creation/update and transaction recording.
4. __[Communications](./communications_app/):__ Used to hold communications (SMS, email, Whatsapp, _et cetera_) functionalities and APIs.
5. __[Experiments](./experiments_app/):__ Used to hold experimental APIs and functionalities for development purposes.
6. __[Know Your Customer](./kyc_app/):__ Used to hold customer data such as: personal details, addresses, ID and Address proofs, _et cetera_ and their related methods/APIs.
7. __[Ledger](./ledger_app/):__ Used to facilitate `tellers`/`accountants` in creating/maintaining their daily ledgers i.e, work diaries.
8. __[Management](./management_app/):__ Used to store custom management commands for the [backend codebase](.).
9. __[Middleware](./middleware_app/):__ Used to hold custom middleware for the [backend codebase](.), more details can be found in the [internal readme](./middleware_app/middlewares/README.MD).
10. __[User](./user_app/):__ Used to hold methods/APIs to facilitate user-management and user-authentication.

## Setup

Please make sure the pre-requisites are satisfied before proceeding with the development environment setup.

### Pre-Requisites

1. __Console:__ [Bash (_Born Again SHell_)](https://www.gnu.org/software/bash/)
   - [GitBash](https://git-scm.com/download/win) for Windows
2. __Language Compiler/Interpreter:__ [Python v3.9 (CPython)](https://www.python.org/downloads/release/python-3917/)
   - I have no idea if PyPI will work; it was created via CPython.
3. __Relational Database Management System:__ [PostgreSQL](https://www.postgresql.org/download/) and [PGAdmin4](https://www.pgadmin.org/download/)
   - While PGAdmin is not strictly necessary, it makes working with PostgreSQL a whole lot easier.
4. __noSQL Database Management System:__ [MongoDB Community](https://www.mongodb.com/try/download/community) and [MongoDB Compass](https://www.mongodb.com/products/compass)
   - Same case as PGAdmin; while compass is not strictly necessary, it makes the whole ordeal a lot simpler.
5. __In-Memory Data Structure/Store:__ [Redis](https://redis.io/)
   - Redis is used to handle queued jobs in the `backend` and caching in the `frontend`/`app`.

### Development Setup

1. Create a new virtual environment using: `python -m venv env`
2. Activate the virtual environment using: `source env/bin/activate`
    - `source env/Scripts/activate` in Windows.
3. Install the dependency management package via: `python -m pip install pip-tools`
4. Install the listed dependencies by running: `sh scripts/install_dependencies.sh`
   1. In UNIX systems, you might need to run `sudo chmod +x scripts/*.sh` before executing the script mentioned above to give it and the rest of the shell-scripts execution permission(s).
5. Create instances of a PostgreSQL database, a MongoDB cluster and a Redis server.
6. Copy the `.env` file for the backend into the folder and fill the values as per your local configuration.
7. Create any new required migrations for the RDBMS using: `python manage.py makemigrations`
8. Run said migrations for the RDBMS using: `python manage.py migrate`
   1. At this point, you can generate fake data for the database (`customers`, `accounts`, `transactions`) by running `python manage.py fakedb`.
   2. Similiarly, you can cleanse the database of all `customers`, `accounts` and `transactions` by running `python manage.py cleardb`.
   3. __NOTE:__ _These commands will only work when `DEBUG` is set to `True` and the `ENV_TYPE` is set to `DEV` in the environment variables._
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
USE_AWS_S3 = True | False
SNS_SENDER_ID = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_ARN = ""

## Redis Settings:
REDIS_HOST = "The machine where your redis server instance is hosted"
REDIS_PORT = "The post of the redis-server instance"
REDIS_DB = "Which redis instance (database) at the URI you need to access; not needed if it is the deafult db i.e, 0"
REDIS_PASSWORD = "The password (if set) of the redis server instance"
```

## Documentation

1. [Postman](https://documenter.getpostman.com/view/17779018/2s93sjT8DE)
2. [JSON](../docs/backend/backend_postman_collection.json)
