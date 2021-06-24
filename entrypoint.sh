export FLASK_APP=app
flask db migrate
flask db upgrade
