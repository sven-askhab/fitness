from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # связи
    workouts = relationship(
        "Workout",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(150), nullable=False)
    description = Column(Text)
    workout_date = Column(Date, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # связи
    user = relationship("User", back_populates="workouts")
    exercises = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    name = Column(String(150), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    # связи
    workout = relationship("Workout", back_populates="exercises")
    sets = relationship(
        "Set",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # связи
    exercise = relationship("Exercise", back_populates="sets")
