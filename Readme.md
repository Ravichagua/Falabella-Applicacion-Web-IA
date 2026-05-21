## Python Virtual Enviroment
```
python -m venv .venv
```
Install pip libraries
```
source .venv/bin/activate
pip install -r requirements.txt
```
Run flask
`python app.py`


## DB Enviroment
```
DATABASE_URL=postgresql://user:password@localhost:5432/falabella
```

## Postgres user
```
sudo -u postgres psql -c "REVOKE ALL PRIVILEGES ON SCHEMA public FROM user;" || true
sudo -u postgres psql -c "DROP DATABASE IF EXISTS falabella;"
sudo -u postgres psql -c "DROP USER IF EXISTS user;"
sudo -u postgres psql -c "CREATE USER user WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE user WITH CREATEDB;"
sudo -u postgres psql -c "CREATE DATABASE falabella OWNER user;"
sudo -u postgres psql -d falabella -c "GRANT ALL PRIVILEGES ON SCHEMA public TO user;"
```
