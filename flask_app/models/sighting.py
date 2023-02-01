from flask_app.config.mysqlconnection import connectToMySQL
#in the class apps you need this ^ written from folder to file 
from flask import flash
from flask_app.models import user

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.num_of_sas = data['num_of_sas']
        self.user_id = data['user_id']
        self.current_sasquatch_user = None

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data['location']) < 3:
            flash("Location at least 3 characters long.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description at least 3 characters long.")
            is_valid = False
        if data['date'] == '':
            flash("Input date!")
            is_valid = False
        if 'num_of_sas' not in data:
            flash("How many sasquatch?")
            is_valid = False

        return is_valid

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM sasquatch.sightings JOIN users on sightings.user_id = users.id;"
        results = connectToMySQL("sasquatch").query_db(query)

        sightings=[]

        for row in results:
            sighting = cls(row)
            user_information = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
            }
            sighting.current_sasquatch_user = user.User(user_information)
            sightings.append(sighting)

        return sightings
# --------------------------


    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM sasquatch.sightings JOIN users on sightings.user_id = users.id WHERE sightings.id = %(id)s;"

        result = connectToMySQL("sasquatch").query_db(query, data)
        if not result:
            return False
        
        result = result[0]
        sighting = cls(result)

        user_information = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password']
            }
        sighting.current_sasquatch_user = user.User(user_information)
        return sighting
    @classmethod
    def delete_sighting(cls,data):
        query = "DELETE FROM `sasquatch`.`sightings` WHERE id =%(id)s"
        return connectToMySQL('sasquatch').query_db(query, data)
# ------------------------------
    @classmethod
    def update_sighting(cls,data):
        query = 'UPDATE sasquatch.sightings SET location = %(location)s, description = %(description)s, date = %(date)s, num_of_sas = %(num_of_sas)s WHERE id = %(id)s;'
        return connectToMySQL('sasquatch').query_db(query,data)

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO sasquatch.sightings (location,description,date,num_of_sas,user_id) VALUES (%(location)s,%(description)s,%(date)s,%(num_of_sas)s,%(user_id)s);'
        return connectToMySQL('sasquatch').query_db(query,data)