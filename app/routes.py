from datetime import date

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import auth, crud
from .database import get_db

router = APIRouter()


def get_current_user(request: Request, db: Session):
    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")

    user = db.query(crud.models.User).filter(crud.models.User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user


@router.post("/api/register")
def register(
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if crud.get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    if crud.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email уже используется")

    password_hash = auth.hash_password(password)
    user = crud.create_user(db, username, email, password_hash)

    response.set_cookie(key="user_id", value=str(user.id), httponly=True)

    return {
        "message": "Пользователь успешно зарегистрирован",
        "user_id": user.id,
        "username": user.username,
    }


@router.post("/api/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    response.set_cookie(key="user_id", value=str(user.id), httponly=True)

    return {
        "message": "Вход выполнен успешно",
        "user_id": user.id,
        "username": user.username,
    }


@router.post("/api/logout")
def logout(response: Response):
    response.delete_cookie("user_id")
    return {"message": "Выход выполнен успешно"}


@router.get("/api/me")
def me(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


@router.get("/api/workouts")
def workouts(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    data = crud.get_workouts(db, user.id)

    return [
        {
            "id": workout.id,
            "title": workout.title,
            "description": workout.description,
            "workout_date": str(workout.workout_date),
            "exercise_count": len(workout.exercises),
        }
        for workout in data
    ]


@router.post("/api/workouts")
def create_workout(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    workout_date: date = Form(...),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)

    workout = crud.create_workout(
        db=db,
        user_id=user.id,
        title=title,
        description=description,
        workout_date=workout_date,
    )

    return {
        "message": "Тренировка создана",
        "workout_id": workout.id,
    }


@router.get("/api/workouts/{workout_id}")
def workout_detail(
    workout_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    workout = crud.get_workout(db, workout_id, user.id)

    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")

    return {
            "id": workout.id,
            "title": workout.title,
            "description": workout.description,
            "workout_date": str(workout.workout_date),
            "exercises": [
                {
                    "id": exercise.id,
                    "name": exercise.name,
                    "description": exercise.description,
                    "sets": [
                        {
                            "id": workout_set.id,
                            "set_number": workout_set.set_number,
                            "reps": workout_set.reps,
                            "weight": workout_set.weight,
                        }
                        for workout_set in exercise.sets
                    ],
                }
                for exercise in workout.exercises
            ],
        }


@router.delete("/api/workouts/{workout_id}")
def delete_workout(
    workout_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    result = crud.delete_workout(db, workout_id, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")

    return {"message": "Тренировка удалена"}


@router.post("/api/workouts/{workout_id}/exercises")
def create_exercise(
    workout_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    set_number: int = Form(...),
    reps: int = Form(...),
    weight: float = Form(...),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    workout = crud.get_workout(db, workout_id, user.id)

    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")

    exercise = crud.create_exercise(
        db=db,
        workout_id=workout.id,
        name=name,
        description=description,
    )

    crud.create_set(
        db=db,
        exercise_id=exercise.id,
        set_number=set_number,
        reps=reps,
        weight=weight,
    )

    return {
        "message": "Упражнение добавлено",
        "exercise_id": exercise.id,
    }


@router.get("/api/stats")
def stats(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return crud.get_stats(db, user.id)
