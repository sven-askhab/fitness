from datetime import date

from sqlalchemy.orm import Session

from . import models


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, username: str, email: str, password_hash: str):
    user = models.User(
        username=username,
        email=email,
        password_hash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_workouts(db: Session, user_id: int):
    return (
        db.query(models.Workout)
        .filter(models.Workout.user_id == user_id)
        .order_by(models.Workout.workout_date.desc())
        .all()
    )


def get_workout(db: Session, workout_id: int, user_id: int):
    return (
        db.query(models.Workout)
        .filter(
            models.Workout.id == workout_id,
            models.Workout.user_id == user_id,
        )
        .first()
    )


def create_workout(
    db: Session,
    user_id: int,
    title: str,
    description: str,
    workout_date: date,
):
    workout = models.Workout(
        user_id=user_id,
        title=title,
        description=description,
        workout_date=workout_date,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def delete_workout(db: Session, workout_id: int, user_id: int):
    workout = get_workout(db, workout_id, user_id)
    if not workout:
        return False

    db.delete(workout)
    db.commit()
    return True


def create_exercise(
    db: Session,
    workout_id: int,
    name: str,
    description: str,
    order_index: int = 0,
):
    exercise = models.Exercise(
        workout_id=workout_id,
        name=name,
        description=description,
        order_index=order_index,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def create_set(
    db: Session,
    exercise_id: int,
    set_number: int,
    reps: int,
    weight: float,
):
    workout_set = models.Set(
        exercise_id=exercise_id,
        set_number=set_number,
        reps=reps,
        weight=weight,
    )
    db.add(workout_set)
    db.commit()
    db.refresh(workout_set)
    return workout_set


def get_stats(db: Session, user_id: int):
    workouts = get_workouts(db, user_id)

    total_workouts = len(workouts)
    total_exercises = 0
    total_sets = 0
    total_reps = 0
    total_volume = 0.0

    for workout in workouts:
        total_exercises += len(workout.exercises)

        for exercise in workout.exercises:
            total_sets += len(exercise.sets)

            for workout_set in exercise.sets:
                total_reps += workout_set.reps
                total_volume += workout_set.reps * workout_set.weight

    return {
        "total_workouts": total_workouts,
        "total_exercises": total_exercises,
        "total_sets": total_sets,
        "total_reps": total_reps,
        "total_volume": round(total_volume, 2),
    }
