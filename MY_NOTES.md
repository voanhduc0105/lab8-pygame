

# Ideas
    - Different square size should have different speed. The smaller the squares, the higher the speed and vice versa
    - When the square touches another square, have them bounce like the border bounce.
    - After each bounce, the squares can either lose energy, or have more energy.
    - Squares should pulse a bit after being hit, either corner hit or square hits
    - Slightly change the angle of the square upon each hit. We have already implemented that in the 3rd method, where squares can lose or have more energy.
    - Create a random new square with a low chance upon collision. Cap the max square that can appear on screen to prevent crashing
    - Add a label that updates the amount of squares.
    - Create a pity system where if there are no squares created, increase the create chance until one is made, then reset the pity counter. This guarantees a square to spawn. Display chance for square spawn too.


# Thought process

## Square touching another
    - Theres a method in pygame called rect, which contains the method colliderect, checking if two objects overlap each other
    - However, it only checks for overlap, does not specify which way of overlapping
    - Since rect is a class that wants x, y, length, width, we can store the x and y of our squares.
    - Then when checking, we fetch said variables and check if theyre colliding horizontally or vertically, and whether one square is to the right of the other and more

## Energy loss
    - After every wall bounce, it will not lose energy
    - After each cube bounce, it will either lose energy or have more energy. It will be random for chaos measures

## Pulsing

### AI's response
    To implement a “pulse” effect (brightness increase) when a square bounces off a wall or collides with another square, you’ll need to:

    Track a “pulse” state for each square (e.g., a timer or intensity value).
    When a collision or wall bounce happens, set the pulse state to a max value.
    In the draw method, if pulse is active, draw the square with a brighter color (e.g., add to RGB, clamp to 255).
    Each frame, decrease the pulse state so the brightness returns to normal.
    Would you like a step-by-step breakdown for each of these, or do you want to try implementing the “pulse” state variable and triggering it first?

### My thoughts
    - At each hitting cases, I will put the pulse at max (fps / 4 since it will only happen for 1/3 of a second). While pulse is max, if it is hit by another object, reset pulse.
    - Change the square color in the draw line in the move function and decrease the pulse by 1.

# Bugs
    - Sometimes after collision (esp between big and small squares), the big square will have its direction to be the same as the smaller one.
    - Because small squares move so fast, it can sometimes pass the check.
    - RGB only takes int, so sometimes color fails due to the input in the color field being a float instead.
    - Because max of each item in RGB is 255 (basic color thing), we should do set the items in the RGB tuple to be the min value of 255 or the brightness color
    - Because 5 checks are done in each frame, the chance is amplified by a lot.

# Bug tackle
    - Sol to bug 1: Check if vx and vy are negative or positive to set values appropriately
    - Sol to bug 2: Do 5 checks instead of 1
    - Sol to bug 3: Wrap around int
    - sol to bug 4: Already mentioned
    - sol to bug 5: Create a flag. If we have already check the collision (and the collision is true), set the flag to True. That way when the loop runs again, if it is already checked, we dont have to check again. also move the loop to being the innermost loop instead of the outtermost
    