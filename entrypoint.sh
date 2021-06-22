export FLASK_APP=app
flask db migrate
flask db upgrade
gunicorn -b :8080 main:app