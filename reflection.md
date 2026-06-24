# PawPal+ Project Reflection

## 1. System Design

The goal of this app is to help a busy pet owner stay consistent with pet care. This app should be able to add a pet, schedule a walk, see today's tasks, track tasks (walks, feedings, meds, enrichment, grooming).

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I chose to create four classes - Pet, Tasks,Schedule, and Owner. A pet is what this app centers around and contains information regarding its needs and care. This information can be updated via the Update() method. The tasks associated with this pet are outlined in the Task class with attributes regarding its duration, time, and priority. There is the owner class which has  a "Has-a" relationship with the Pet class (1 -> n). The owner has pets, preferences, availbility, and also an Update() method. Lastly, the schedule ties all of these classes together, generates a plan for an owner based on tasks associated with the pets they own. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, Task has no date attribute which makes it difficult to show show_tasks() and generate_daily_plan() based on the date. There is no recurrence attribute in Task which may make users create extra task objects for the same task (ie two task objects to give medication if a pet needs meds twice daily). There should a completed bool for each task and a tie between  task.pet and owner.pet. Both are important when generating schedules and for overall clarity. Also, adding a task_id helps when deleting a task that is seperate from another task for another pet with the same name (ie walk for PetA AND walk for PetB, but you want to delete the walk for PetA only).
---

## Sample Output

=== Today's Schedule ===
Plan for 2026-06-23 (65/120 min used):
  08:00 — Thyroid meds for Milo (5 min) [priority 1]
  08:05 — Feeding for Milo (10 min) [priority 1]
  08:15 — Morning walk for Biscuit (30 min) [priority 1]
  08:45 — Enrichment play for Biscuit (20 min) [priority 2]
  
## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
