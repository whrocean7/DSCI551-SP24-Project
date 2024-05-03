First,
RateMyBeer.py is backend file of flask
config.txt is the configuration information of database connection
static folder contains .css file and .js files for frontend
templates folder contains .html files for frontend
data preparation.sql is for inserting data for test

If you want to use this RateMyBeer.py, first install these libraries
pip install Flask
pip install flask_cors
pip install pymysql

this backend service will run on http://localhost:8091/
so make sure the 8091 port is available

to implement the project, 3 steps are needed

1. data preparation
create database using data and command in .sql file

2. config data connection in config.txt
config data connection information in config.txt in this form
[database name]
host=localhost
user=root
password=your password
database=database name

3. run the project with command
export FLASK_APP=RateMyBeer.py
export FLASK_RUN_PORT=8091
export FLASK_DEBUG=1
flask run --port=8091 --debug






