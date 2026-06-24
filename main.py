"""Demo script for PawPal+.

Builds an owner with two pets and several tasks, then prints today's plan
to the terminal. Run with:  python main.py
"""

from datetime import date

from pawpal_system import Owner, Pet, Task, Schedule, Frequency


def main() -> None:
    today = date.today()

    # 1. Owner with a daily time budget.
    owner = Owner(name="Sam", minutes_available=120, preferences="mornings")

    # 2. Two pets.
    biscuit = Pet(
        name="Biscuit",
        animal_type="Golden Retriever",
        medication="none",
        grooming_type="bath",
        grooming_frequency="monthly",
        grooming_date=date(today.year, today.month, 28),
    )
    milo = Pet(
        name="Milo",
        animal_type="Tabby Cat",
        medication="thyroid pill",
        grooming_type="brush",
        grooming_frequency="weekly",
        grooming_date=date(today.year, today.month, 28),
    )
    owner.add_pet(biscuit)
    owner.add_pet(milo)

    # 3. A schedule with several tasks across both pets (priority 1 = highest).
    schedule = Schedule(owner)
    schedule.add_task(Task("Morning walk", 30, 1, biscuit, today, Frequency.DAILY))
    schedule.add_task(Task("Feeding", 10, 1, milo, today, Frequency.DAILY))
    schedule.add_task(Task("Thyroid meds", 5, 1, milo, today, Frequency.DAILY))
    schedule.add_task(Task("Enrichment play", 20, 2, biscuit, today, Frequency.DAILY))

    # 4. Generate and print today's schedule (the planner assigns start times).
    schedule.generate_daily_plan(today)
    print("=== Today's Schedule ===")
    print(schedule.explain_plan())


if __name__ == "__main__":
    main()
