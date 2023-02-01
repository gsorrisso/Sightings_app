from flask_app.controllers import users, sightings
# this is pulling from users

from flask_app import app
#we  still need to import app because we are running the server as if it is the main entry point


if __name__ == "__main__":
    app.run(debug=True, port=5001)