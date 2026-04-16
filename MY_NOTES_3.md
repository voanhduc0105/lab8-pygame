# Plans
    - Use time based instead of frame based, with time library and delta-time (scheduled on a later date)
    - Remove kill property. Replace that by the property of: Whenever a square hits another, the life span reduces. Depending on the size it will either be a drastic or minor reduction
    - Recycle squares to prevent memo overflow
    - Bonus: Pause menu to implement options to:
        + Disable ROE / AOE
        + View stats (This will be done on a later date? Maybe?)
        + Access pause menu with p or esc button.
        + When in pause menu, the bg will be darkened / lightened

# How to go about this
    - Aging:
        + Set up a health property for each square, and a max health for easier access, and a damage. both health and dmg scales with box size
        + Change the kill property so that when colided, each square will take damage.
        + Squares will also slowly take damage when alive.
    - Recycle:
        + To prevent the wrong square being popped, we add an id property so each square has a unique id that increments every time a new one is made.
        + Also make a new list called disabled squares that fetches that pop value
        + When creating new square, it checks if disabled squares is empty. If yes, create a new one, if not, edit the properties.
    - Pause menu:
        + Had to use tutorial for this: https://youtu.be/AIamQfL9d1I?si=y93HzbIpWQ3bqOkr

# Why delay implementation
    - Breaks the whole system of movement


