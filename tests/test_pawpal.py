"""Tests for core PawPal+ behaviors."""

from datetime import date

from pawpal_system import Owner, Pet, Task, Schedule


def make_pet(name: str = "Biscuit") -> Pet:
    return Pet(
        name=name,
        animal_type="dog",
        medication="none",
        grooming_type="bath",
        grooming_frequency="monthly",
        grooming_date=date(2026, 7, 1),
    )


def test_mark_complete_changes_status():
    """Calling mark_complete() flips the task from incomplete to complete."""
    pet = make_pet()
    task = Task("Walk", duration=30, priority=1, pet=pet, due_date=date(2026, 6, 23))

    assert task.completed is False  # starts incomplete

    task.mark_complete()

    assert task.completed is True  # status actually changed


def test_adding_task_increases_pet_task_count():
    """Adding a task for a pet increases that pet's task count by one."""
    pet = make_pet()
    owner = Owner("Sam", minutes_available=60, preferences="mornings")
    owner.add_pet(pet)
    schedule = Schedule(owner)

    before = len(schedule.tasks_for(pet))
    assert before == 0

    schedule.add_task(
        Task("Feed", duration=10, priority=1, pet=pet, due_date=date(2026, 6, 23))
    )

    after = len(schedule.tasks_for(pet))
    assert after == before + 1
