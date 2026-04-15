from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from datetime import date
from schema import (
    ExerciseSchema,
    ExerciseCreateSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
    WorkoutCreateSchema,
    WorkoutExerciseCreateSchema
)
from server.models import Exercise, Workout, WorkoutExercises, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_create_schema = ExerciseCreateSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()
workout_create_schema = WorkoutCreateSchema()

# Define Routes here
@app.route('/')
def index():
    body = {
        'message': 'Welcome to the Workout Tracker App'
    }
    return make_response(body, 200)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200
    
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200
    
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    errors = workout_create_schema.validate(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'errors': errors}), 400

    try:
        date_str = data.get('date')
        if isinstance(date_str, str):
            workout_date = date.fromisoformat(date_str)
        else:
            workout_date = date_str
            
        workout = Workout(
            date=workout_date,
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    try:
        for we in workout.exercises:
            db.session.delete(we)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'message': 'Workout deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200
    
@app.route('/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200

    
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    errors = exercise_create_schema.validate(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'errors': errors}), 400

    try:
        exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed')
        )
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    try:
        # Delete associated workout_exercises first
        for we in exercise.workouts:
            db.session.delete(we)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({'message': 'Exercise deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    data = request.get_json()
    if not data:
        data = {}

    errors = workout_exercise_create_schema.validate(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'errors': errors}), 400

    try:
        workout_exercise = WorkoutExercises(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)