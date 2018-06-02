flyway -user=admin -password=admin -url="jdbc:postgresql://localhost/owners_db" -locations="filesystem:sql" info

##Setup

First, run the Flyway migration script from the root of your local Flyway directory:

```bash
flyway -user=root -url="jdbc:postgresql://localhost/owners_db" -locations="filesystem:/path-to-this-app/owners-db/sql" migrate
```

in my case, this script needed to be prefixed with `./` and the `user` needed to be set as `postgres` :

```bash
./flyway -user=postgres -url="jdbc:postgresql://localhost/owners_db" -locations="filesystem:/Users/darrenklein/desktop/darren/development/bushwickfc/owners-db/sql" migrate
```

then, load the seed data:

```bash
psql -U postgres -d owners_db -f seed/seed.sql
```

##Use

To run this script, run the command

```bash
python3 import/run.py
```

This will pull data from the Google Sheet, format it, and insert it into a database.

##Notes (by @darrenklein)

I'm running MySQL version 8.0.11, and had an issue running the `V1_initial_schema.sql` script due to a collation issue. I had to change line 131 to read:

```sql
concat(o.display_name, s.pos_display, CONVERT(pp.pos_display USING latin1)) as pos_display,
```

in order to get it to run correctly.

##pygsheets

I used pygsheets[https://github.com/nithinmurali/pygsheets] to access Google sheets. Two top-level gitignored files are required to run this library:

- `client_secret.json`
- `sheets.googleapis.com-python.json`

Following the pygsheets instruction to set up an OAuth Google API key will produce the `client_secret.json` file; when you put that in your project and run the script for the first time, you'll be prompted to visit an authorization web page and enter a secret key from that page - this will create the `sheets.googleapis.com-python.json` file automatically.

##psycopg2

This script uses psycopg2 to insert the data into Postgres. psycopg2, of course, requires databse credentials, which are gitignored. To run this script, you'll need a local copy of the file `import/credentials.py`, formatted like so:

```python
user = 'postgres'
password = 'password'
dbname = 'owners_db'
host = 'localhost'
```
