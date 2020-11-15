# development

### DB migration:

Alembic is used for database migrations.

To change any database model, follow these steps.

- Make sure that you have an up-to-date squeaknode with a sqlite database.
- Make a note of the path to the ".db" sqlite database file. (Usually `~/.sqk/data/testnet/data.db` by default)
- Make the changes to database models in `squeaknode/db/models.py`
- Update the `alembic.ini` file to point to the sqlite file from before:
	```
	sqlalchemy.url = sqlite://///home/<USER>/.sqk/data/testnet/data.db
	```
- Run the command to generate a new alembic migration:
	```
	$ virtuelenv venv
	$ pip install -r requirements.txt
	$ pip install -e .
	$ alembic revision --autogenerate -m "<YOUR_MESSAGE>"
	```
