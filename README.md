- minimum required .env file
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```
- create tables in database
```
python -m parser.migration_utils upgrade head
```
- start parser
```
python -m parser
```