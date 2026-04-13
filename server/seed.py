#!/usr/bin/env python3
from app import app
from models import *
from datetime import date, timedelta

def seed_data():
    with app.app_context():
        Exercise.query.delete()
        Workout.query.delete()
        WorkoutExercises.query.delete()
        db.session.commit()
    
        # Exercise Table
        exercises = [
            Exercise(name='Push-up', category='bodyweight training', equipment_needed=False), 
            Exercise(name='Squat', category='Legs', equipment_needed=True),
            Exercise(name='Dumbell Row', category='Back', equipment_needed=True)
        ]
        db.session.add_all(exercises)
        db.session.commit()
    
        # Workout table
        base_date = date.today() - timedelta(days=30)
        workouts = [
            Workout(date=base_date, duration_minutes=60, notes='Morning chest workout'),
            Workout(date=base_date + timedelta(days=2), duration_minutes=75, notes='Leg day with heavy squats'),
            Workout(date=base_date + timedelta(days=5), duration_minutes=45, notes='Quick upper body session')
        ]
        db.session.add_all(workouts)
        db.session.commit()
    
        # WorkoutExercises table
        workout_exercises = [
            WorkoutExercises(workout_id=1, exercise_id=1, reps=10, sets=4, duration_seconds=None),
            WorkoutExercises(workout_id=1, exercise_id=5, reps=15, sets=3, duration_seconds=None),
            WorkoutExercises(workout_id=1, exercise_id=8, reps=12, sets=3, duration_seconds=None),
            
            WorkoutExercises(workout_id=2, exercise_id=2, reps=8, sets=5, duration_seconds=None),
            WorkoutExercises(workout_id=2, exercise_id=6, reps=12, sets=3, duration_seconds=None),
            WorkoutExercises(workout_id=2, exercise_id=7, reps=None, sets=3, duration_seconds=60),
            
            WorkoutExercises(workout_id=3, exercise_id=4, reps=8, sets=4, duration_seconds=None),
            WorkoutExercises(workout_id=3, exercise_id=9, reps=10, sets=3, duration_seconds=None),
            WorkoutExercises(workout_id=3, exercise_id=10, reps=12, sets=3, duration_seconds=None)
        ]
        db.session.add_all(workout_exercises)
        db.session.commit()
    
        print("Databases seeded successfully!")
    
# reset data and add new example data, committing to db
seed_data()