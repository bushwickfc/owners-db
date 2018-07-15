# Owners-DB

In the spring of 2018, the Bushwick Food Co-op transitioned from a member/dues-based model to an owner/equity-based model, and all existing members had to effectively terminate their memberships and re-register as owners. These registration records were initially stored in a Google Sheet...

The main function of this script is to fetch the new ownership data (as well as some historic membership data), sort through it, and insert it into our new Postgres database. Running the script will also output a file named 'no_old_member_id.csv' to the root directory, which contains a list of owners who, for one reason or another, could not be associated by email address with a matching record in the old Members DB (additional action may need to be taken for these owners - see the comments in `import/report.py` for more info).

## Setup

#### Install Dependencies

This script requires two dependencies - `pygsheets` and `psycopg2` (psycopg2-binary, actually). They can be installed by running:

```bash
pip3 install -r import/requirements.txt
```

See the important notes below on using both of these dependencies...

Separately, you'll need to install Flyway to handle the database migration - https://flywaydb.org/download/

#### Run Migration

This script uses a local installation of Flyway to handle migrating the schema.

Run the Flyway migration script from the root of your local Flyway directory:

```bash
flyway -user=root -url="jdbc:postgresql://localhost/owners_db" -locations="filesystem:/path-to-this-app/owners-db/sql" migrate
```

in my case, this script needed to be prefixed with `./` and the `user` needed to be set as `postgres` :

```bash
./flyway -user=postgres -url="jdbc:postgresql://localhost/owners_db" -locations="filesystem:/Users/darrenklein/desktop/darren/development/bushwickfc/owners-db/sql" migrate
```

(can rollback using the `clean` command, instead of `migrate` - find the full list of commands at https://flywaydb.org/documentation/commandline/)

#### Run the Seedfile

Finally, load the seed data by running the following script from the root of the owners-db directory:

```bash
psql -U postgres -d owners_db -f seed/seed.sql
```

(Again, I needed to set the `-U` as 'postgres' here instead of 'root' to match my local config.)

## Use

To run this script, run the command

```bash
python3 import/run.py
```

This will pull data from the Google Sheet, format it, and insert it into a database. It will also produce a .csv file named 'no_old_member_id.csv' in this script's root directory. After the inserts have been run, a list of successful/failed inserts will be printed to the console.

#### Idempotency

Across tables, an owner is identified by their email address. When this script runs, the function `exists/3` in `insert.py` will check before each insert to see if a record for that owner already exists on that table. If so, it will quietly skip the insert; otherwise, it will go ahead and attempt the insert.

It should be safe to run this script repeatedly against the same database instance.

## pygsheets

I used pygsheets[https://github.com/nithinmurali/pygsheets] to access Google sheets. Two top-level gitignored files are required to run this library:

- `client_secret.json`
- `sheets.googleapis.com-python.json`

Following the pygsheets instruction to set up an OAuth Google API key will produce the `client_secret.json` file; when you put that in your project and run the script for the first time, you'll be prompted to visit an authorization web page and enter a secret key from that page - this will create the `sheets.googleapis.com-python.json` file automatically.

## psycopg2

This script uses psycopg2 to insert the data into Postgres. psycopg2, of course, requires databse credentials, which are gitignored. To run this script, you'll need a local copy of the file `import/credentials.py`, formatted like so:

```python
user = 'postgres'
password = 'password'
dbname = 'owners_db'
host = 'localhost'
```

Initially, I had used the 'standard' version of psycopg2, but it produced a warning that I should install psycopg2-binary instead... so I did.

## Ingest steps
`cd import`
Import owners:
`python3 run.py owner-import --new-owner {new_owner.csv} --master-sheet {members_db.csv`}
Import equity payments + payment plans:
`python3 run.py equity-import --equity-payments {equity_export.csv} --payment-agreement {payment_plan.csv}`
Import 7shifts:
`python3 run.py seven-shifts --end-date {1st of current month, ex 2018-06-01}`
Import meeting hours:
`python3 run.py meeting-attendance {meeting_attendance.csv}`
