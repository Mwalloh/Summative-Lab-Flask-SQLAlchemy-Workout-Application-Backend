from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"Exercise(name={self.name}, category={self.category}, equipment_needed={self.equipment_needed})"
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f"Workout(date={self.date}, duration_minutes={self.duration_minutes}, notes={self.notes})"
class WorkoutExercises(db.Model):
    __tablename__= 'workoutExercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    def __repr__(self):
        return f"WorkoutExercise(workout_id={self.workout_id}, exercise_id={self.exercise_id}, reps={self.reps}, sets={self.reps}, duration_seconds={self.duration_seconds})"