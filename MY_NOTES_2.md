# Requirements
    - Make the smaller squares flee away from the bigger ones
    - All squares tend to keep a certain randomness to their behavior / trajectory

# Though process

## Flee mechanic
    - If the square is near the proximity of a bigger square (should set the criteria to be 2 times big, perhaps), then it has a chance to run away instead. If it constantly runs away then all small squares would just ignore the big squares, making the "game" not fun.
    - When it is near the big square, invert movement. First, "define" the center of the square, and "map out" a circle as a radius. The circle's radius should be approx 2x the radius. If the mini square's center is in the proximity of that radius, it has a chance to flee. This happens every frame so it can either flee early or flee late, or not flee at all.
    - How to define center of square: Since the top left is the drawing point, we mark the center as x + size / 2 and y + size / 2. In pygame, the higher the y, the lower the position is. It is basically inverted
    - Just inverting the movement is lame. We can do this:
        + Calculate the movement vector pointing away from the square
        + Normalize it by dividing by the distance, so that it is limited in the range of -1 to 1
        + Add by the numbers from above, and flee strength, making it look like theres a forcefield in the big square that pushes the small ones away
    - Bonus: If user hover over a square, it shows the area of effect

## Certain randomness to behavior
    - Every square spawned will have the property:
        + Kill chance: A chance to kill other squares.
        + Im tired: Squares sometimes stops to rest at random times
        + Why am i here: Suddenly reverts movement

# Known issues (previoysly)
    - Squares are too big -> should reduce size
    - Move too fast -> Lower speed limit
    - Sometimes squares move very very slow after spd jitter -> Add lower speed limit