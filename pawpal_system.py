"""PawPal+ system classes.

Skeleton generated from diagrams/uml_draft.mmd — attributes and empty
method stubs only. Implement scheduling logic in small increments.
"""

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Owner:
    name: str
    minutes_available: int
    preferences: str

    def update(self) -> None:
        ...


@dataclass
class Pet:
    name: str
    animal_type: str
    medication: str
    grooming_type: str
    grooming_frequency: str
    grooming_date: date

    def update(self) -> None:
        ...


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    start_time: time

    def update(self) -> None:
        ...


@dataclass
class Schedule:
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        ...

    def delete_task(self, task: Task) -> None:
        ...

    def show_tasks(self, on_date: date) -> list[Task]:
        ...

    def generate_daily_plan(self, on_date: date) -> list[Task]:
        ...

    def explain_plan(self) -> str:
        ...
