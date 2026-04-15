from flask import Flask, make_response
from flask_migrate import Migrate

from server.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route('/')
def index():
    body = {
        'message': 'Welcome to the Workout Tracker App'
    }
    return make_response(body, 200)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    data = Workout.query.all()
    for workout in data:  
        return make_response(workout.to_dict(), 200)
    
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    ...
    
@app.route('/workouts', methods=['POST'])
def create_workout():
    ...
    
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    ...
    
@app.route('/exercises', methods=['GET'])
def get_exercises():
    ...
    
@app.route('/exercises/<int:id>')
def get_exercise(id):
    ...
    
@app.route('/exercises', methods=['POST'])
def create_exercise():
    ...
    
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    ...
    
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout():
    ...

if __name__ == '__main__':
    app.run(port=5555, debug=True)