from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, CheckConstraint

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)
    
    # Establish the r/ship to WorkoutExercise
    workoutExercise = db.relationship('WorkoutExercises', back_populates='exercise')
    
    # Many-to-many with Workout through WorkoutExercise
    workout = db.relationship('Workout', secondary='workoutExercises')
    
    __table_args__ = (
        CheckConstraint("LENGTH(name) > 3", name='exercise_name_length_check'),
    )
    
    def __repr__(self):
        return f"Exercise(name={self.name}, category={self.category}, equipment_needed={self.equipment_needed})"
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    # Establish the r/ship to WorkoutExercise
    workoutExercise = db.relationship('WorkoutExercises', back_populates='workout')
    
    # Many-to-many with Exercise through WorkoutExercise
    exercise = db.relationship('Exercise', secondary='workoutExercises')
    
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name='workout_duration'),
    )
    
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if not duration_minutes and duration_minutes < 0:
            raise ValueError("Duration minutes cannot be empty and less than 0.")
        return duration_minutes

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
    
    # Establish the r/ship to Workout and Exercise
    workout = db.relationship('Workout', back_populates='workoutExercise')
    exercise = db.relationship('Exercise', back_populates='workoutExercise')
    
    @validates('duration_seconds')
    def validate_duration_seconds(self, key, duration_seconds):
        if duration_seconds is not None and duration_seconds < 0:
            raise ValueError("Duration seconds cannot be empty and less than 0.")
    
    def __repr__(self):
        return f"WorkoutExercise(workout_id={self.workout_id}, exercise_id={self.exercise_id}, reps={self.reps}, sets={self.reps}, duration_seconds={self.duration_seconds})"