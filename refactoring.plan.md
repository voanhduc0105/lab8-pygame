# Refactoring Plan

## 1. Overview
This project is a single-file Pygame simulation in [main.py](/home/moonimochacat/Desktop/EPITA%20(Linux)/AI%20for%20Software%20Engineering/Github/lab8-pygame/main.py) where colorful squares move, collide, chase, flee, and sometimes get reused from a disabled pool. The code works as a small game prototype, but it is harder than necessary for beginners to read because important logic is repeated, the main loop is long, and several values are still written as raw numbers instead of named constants.

The best light refactoring is to keep the behavior the same while making the code easier to follow step by step. The goal is not to redesign the game, but to make the current structure clearer for first-year students.

## 2. Refactoring Goals
- Improve readability by giving repeated values and repeated logic clearer names.
- Reduce duplication in square creation, reset, and reuse logic.
- Make the main game loop easier to understand by separating input, update, and drawing steps.
- Add small safety checks for edge cases without changing the intended behavior.
- Keep the code beginner-friendly and avoid advanced abstractions.

## 3. Step-by-Step Refactoring Plan

### Step 1: Replace magic numbers with named constants
What to do:
- Move repeated numbers such as `10`, `40`, `60`, `0.3`, and the hard-coded reset count `15` into descriptive constants near the top of the file.
- Use names that describe their role, such as `MIN_SQUARE_SIZE`, `MAX_SQUARE_CAP`, `BASE_LIFE_SECONDS`, or `PAUSE_BUTTON_COUNT`.

Why this helps:
- Beginners can understand what each number means without searching through the file.
- If one of these values changes later, it only needs to be updated in one place.

Add inline comments in the final code:
- Explain that the new constants make the simulation easier to tune.
- Mention that named values improve readability and reduce mistakes.

Short example:
```python
# before
self.square_size = random.randint(10, WINDOW_WIDTH // 30)

# after
self.square_size = random.randint(MIN_SQUARE_SIZE, WINDOW_WIDTH // 30)
```

### Step 2: Extract repeated square setup into one helper method
What to do:
- Create one small method inside `Square` that randomizes all square properties, such as size, position, velocity, color, pulse, tired, life, and damage.
- Use that helper both in `__init__` and in `squarecreation` when reusing an object from `disabledsquares`.

Why this helps:
- The same initialization logic currently appears twice.
- A shared helper makes the code shorter and makes it easier to see which properties define a square.

Add inline comments in the final code:
- Explain that the helper keeps new and reused squares consistent.
- Mention that this avoids copy-paste mistakes.

Short example:
```python
# before
# repeated random setup in __init__
# repeated random setup again in squarecreation

# after
self._randomize_state()
```

### Step 3: Separate collision response from damage logic
What to do:
- Keep `squarecollision` doing the overlap check, but move the repeated horizontal and vertical bounce adjustments into small helper methods.
- Keep the health reduction in one clearly named method so it is obvious that collisions also cause damage.

Why this helps:
- `squarecollision` is currently long and deeply nested.
- Smaller helpers make it easier to understand which part handles movement and which part handles damage.

Add inline comments in the final code:
- Explain that the helpers separate motion handling from health handling.
- Mention that smaller functions are easier to test and read.

Short example:
```python
# before
if a.x < b.x:
    if self.vx - other.vx > 0:
        ...
    self.i_want_to_KILL_you(other)

# after
self._bounce_x(other, a, b)
self._apply_collision_damage(other)
```

### Step 4: Make the main loop read like phases
What to do:
- Split the large `while running:` loop in `main()` into a few small helper functions, such as:
  - one for event handling,
  - one for updating squares,
  - one for drawing the frame,
  - one for pause-screen actions.
- Keep the order the same so the game behaves the same.

Why this helps:
- Beginners can understand the loop faster when each phase has one job.
- The current loop mixes input, simulation, and rendering in one place, which makes it hard to scan.

Add inline comments in the final code:
- Explain what each phase does.
- Mention that separating phases matches the usual game-loop structure.

Short example:
```python
# before
while running:
    # events, updates, collision checks, drawing all together

# after
while running:
    handle_events(...)
    update_squares(...)
    draw_frame(...)
```

### Step 5: Add small safety checks for edge cases
What to do:
- Guard the distance-based math in `flee` and `chase` so the code does not divide by zero if two squares share the exact same center.
- Review any index-based reset logic in the pause menu so it does not rely on a hard-coded index that could become confusing.

Why this helps:
- These checks improve correctness without changing the intended simulation rules.
- Beginners learn that even small visual simulations need defensive programming.

Add inline comments in the final code:
- Explain why the zero-distance guard exists.
- Mention that edge cases are important because real gameplay can produce overlapping positions.

Short example:
```python
# before
away_x = (selfcenter[0] - othercenter[0]) / dist

# after
if dist == 0:
    return
away_x = (selfcenter[0] - othercenter[0]) / dist
```

### Step 6: Improve names only where the meaning is unclear
What to do:
- Rename a few unclear names if needed, but keep the total number of renames small.
- Focus on names that directly affect readability, such as `topspd`, `minspd`, or the pause-toggle flags.
- Do not rename everything at once.

Why this helps:
- Very small renames can make the code much easier to read without creating a large patch.
- Beginners benefit most from names that describe behavior in plain language.

Add inline comments in the final code:
- Explain the meaning of the new names.
- Mention that readable names help future readers understand the code faster.

## 4. Final Output Requirements (Mandatory)
When this plan is executed, the output MUST:
- Contain only the refactored code.
- Include inline comments explaining what changed.
- Include inline comments explaining why the change improves readability, maintainability, or correctness.
- Include inline comments that highlight important programming concepts such as constants, helpers, game-loop phases, and edge-case checks.
- Keep all explanations concise and beginner-friendly.

## 5. Key Concepts for Students
- Constants: named values that replace magic numbers and make code easier to tune.
- Helper functions: small functions that reduce duplication and explain one job at a time.
- Game loop phases: input, update, and render are common parts of interactive programs.
- Object reuse: reinitializing an old object can be simpler than creating a brand-new one.
- Defensive programming: small checks prevent crashes when unusual input or positions occur.

## 6. Safety Notes
- Test the game after each small step so behavior stays the same.
- Preserve the current collision and pause behavior unless a change is clearly a bug fix.
- Keep the refactor small enough that students can compare the before and after version easily.
- If a rename makes the code less obvious, prefer the simpler name even if it is not perfect.
