# Database Migration

### DB migration:

Alembic is used for database migrations.

To change any database model, follow these steps.

- Make sure that you have an up-to-date squeaknode with a sqlite database.
- Make a note of the path to the ".db" sqlite database file. (Usually `~/.sqk/data/testnet/data.db` by default). If this is an initial migration, then create an empty file at this location.
- Make the changes to database models in `squeaknode/db/models.py`
- Update the `alembic.ini` file to point to the sqlite file from before:
	```
	sqlalchemy.url = sqlite://///home/<USER>/.sqk/data/testnet/data.db
	```
- Run the command to generate a new alembic migration:
	```
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	pip install -e .
	alembic -c squeaknode/db/alembic.ini revision --autogenerate -m "<YOUR_MESSAGE>"
	```
- To generate a new initial version revision, follow the same steps as above, but the `/home/<USER>/.sqk/data/testnet/data.db` file should be an empty file.
