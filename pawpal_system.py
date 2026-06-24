"""PawPal+ system classes.

Skeleton generated from diagrams/uml_draft.mmd — attributes and empty
method stubs only. Implement scheduling logic in small increments.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from uuid import uuid4


class Frequency(Enum):
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Owner:
    name: str
    minutes_available: int
    preferences: str
    pets: list["Pet"] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the owner immediately after construction."""
        self._validate()

    def _validate(self) -> None:
        """Reject an empty name or negative time budget."""
        if not self.name or not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if self.minutes_available < 0:
            raise ValueError(
                f"minutes_available cannot be negative, got {self.minutes_available}."
            )

    def update(self, **changes: object) -> None:
        """Update one or more attributes by keyword, then re-validate."""
        for attr, value in changes.items():
            if not hasattr(self, attr):
                raise AttributeError(f"Owner has no attribute {attr!r}.")
            setattr(self, attr, value)
        self._validate()

    def add_pet(self, pet: "Pet") -> None:
        """Register a pet to this owner (no duplicates by identity)."""
        if any(pet is existing for existing in self.pets):
            raise ValueError(f"{pet.name!r} is already registered to {self.name}.")
        self.pets.append(pet)


@dataclass
class Pet:
    name: str
    animal_type: str
    medication: str
    grooming_type: str
    grooming_frequency: str
    grooming_date: date

    def __post_init__(self) -> None:
        """Validate the pet immediately after construction."""
        self._validate()

    def _validate(self) -> None:
        """Reject an empty name or animal type."""
        if not self.name or not self.name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not self.animal_type or not self.animal_type.strip():
            raise ValueError("Pet animal_type cannot be empty.")

    def update(self, **changes: object) -> None:
        """Update one or more attributes by keyword, then re-validate."""
        for attr, value in changes.items():
            if not hasattr(self, attr):
                raise AttributeError(f"Pet has no attribute {attr!r}.")
            setattr(self, attr, value)
        self._validate()


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    pet: "Pet"
    due_date: date
    frequency: Frequency = Frequency.DAILY
    start_time: time | None = None  # assigned by the planner
    completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Validate the task immediately after construction."""
        self._validate()

    def _validate(self) -> None:
        """Reject states that would break scheduling."""
        if not self.name or not self.name.strip():
            raise ValueError("Task name cannot be empty.")
        if self.duration <= 0:
            raise ValueError(f"duration must be positive, got {self.duration}.")
        if self.priority < 1:
            raise ValueError(f"priority must be >= 1, got {self.priority}.")
        if not isinstance(self.frequency, Frequency):
            raise TypeError(f"frequency must be a Frequency, got {self.frequency!r}.")

    def update(self, **changes: object) -> None:
        """Update one or more attributes by keyword, then re-validate.

        Example: task.update(duration=45, priority=1)
        """
        for attr, value in changes.items():
            if not hasattr(self, attr):
                raise AttributeError(f"Task has no attribute {attr!r}.")
            setattr(self, attr, value)
        self._validate()

    def mark_complete(self) -> None:
        """Mark this task complete for adherence tracking."""
        self.completed = True

    def occurs_on(self, on_date: date) -> bool:
        """Return True if this task should appear on ``on_date``.

        Recurrence is anchored to ``due_date``: a task never occurs before it.
        """
        if on_date < self.due_date:
            return False
        if self.frequency is Frequency.ONE_TIME:
            return on_date == self.due_date
        if self.frequency is Frequency.DAILY:
            return True
        if self.frequency is Frequency.WEEKLY:
            return (on_date - self.due_date).days % 7 == 0
        return False


DAY_START = time(8, 0)  # plans lay tasks out starting at 8:00 AM


@dataclass
class Schedule:
    owner: Owner
    # Flat list for now; consider indexing by date if history grows large.
    tasks: list[Task] = field(default_factory=list)

    # Reasoning captured by the last generate_daily_plan() call, for explain_plan().
    _last_date: date | None = field(default=None, init=False, repr=False)
    _last_planned: list[Task] = field(default_factory=list, init=False, repr=False)
    _last_skipped: list[Task] = field(default_factory=list, init=False, repr=False)
    _last_used: int = field(default=0, init=False, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a task, ensuring it belongs to one of the owner's pets."""
        if not any(task.pet is pet for pet in self.owner.pets):
            raise ValueError(
                f"Task pet {task.pet.name!r} is not one of "
                f"{self.owner.name}'s pets."
            )
        if any(existing.task_id == task.task_id for existing in self.tasks):
            raise ValueError(f"Task {task.task_id!r} is already scheduled.")
        self.tasks.append(task)

    def delete_task(self, task_id: str) -> None:
        """Remove a task by id; raise if no such task exists."""
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                return
        raise KeyError(f"No task with id {task_id!r}.")

    def show_tasks(self, on_date: date) -> list[Task]:
        """All tasks occurring on ``on_date``, highest priority first."""
        due = [task for task in self.tasks if task.occurs_on(on_date)]
        return sorted(due, key=lambda task: (task.priority, task.name))

    def tasks_for(self, pet: Pet) -> list[Task]:
        """All scheduled tasks belonging to ``pet``."""
        return [task for task in self.tasks if task.pet is pet]

    def generate_daily_plan(self, on_date: date) -> list[Task]:
        """Fit the day's tasks into the owner's available minutes.

        Tasks are taken highest-priority first (shorter tasks break ties so
        more can fit). Each planned task is assigned a sequential start_time;
        tasks that don't fit the time budget are skipped. Returns the planned
        tasks in chronological order.
        """
        candidates = sorted(
            (task for task in self.tasks if task.occurs_on(on_date)),
            key=lambda task: (task.priority, task.duration, task.name),
        )

        planned: list[Task] = []
        skipped: list[Task] = []
        used = 0
        cursor = datetime.combine(on_date, DAY_START)

        for task in candidates:
            if used + task.duration <= self.owner.minutes_available:
                task.start_time = cursor.time()
                cursor += timedelta(minutes=task.duration)
                used += task.duration
                planned.append(task)
            else:
                task.start_time = None
                skipped.append(task)

        self._last_date = on_date
        self._last_planned = planned
        self._last_skipped = skipped
        self._last_used = used
        return planned

    def explain_plan(self) -> str:
        """Explain the most recently generated plan in plain language."""
        if self._last_date is None:
            return "No plan generated yet. Call generate_daily_plan() first."

        budget = self.owner.minutes_available
        lines = [
            f"Plan for {self._last_date.isoformat()} "
            f"({self._last_used}/{budget} min used):",
        ]
        for task in self._last_planned:
            start = task.start_time.strftime("%H:%M") if task.start_time else "--:--"
            lines.append(
                f"  {start} — {task.name} for {task.pet.name} "
                f"({task.duration} min) [priority {task.priority}]"
            )
        if self._last_skipped:
            lines.append(
                f"Skipped {len(self._last_skipped)} task(s) — not enough time:"
            )
            for task in self._last_skipped:
                lines.append(
                    f"  {task.name} for {task.pet.name} "
                    f"({task.duration} min) [priority {task.priority}]"
                )
        return "\n".join(lines)
