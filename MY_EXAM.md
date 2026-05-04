# Ex 7
    - Best way to go about this is to make an empty list for each square
    - They will have max size of 30 (can be adjusted in trails_length)
    - Repeatedly draw from one to another point on the list.
    - Oh and remember to start from center as well
    - Oh and its an first in last out order, meaning when it reaches max of 30, it will remove the 0'th item
# ex 7 weird behaviors:
    - When passing border, since its a wrapping border, it uhm, create funny lines across the screens. I know why this happens, but explain it will cost a lot of time so sorry
    - We tackle this by empty-ing the list
    - Also, newly created squares should have their records empty
    - Also, position records in accordance to the top left of squares (because that is how pygame works)
    - Also because the game runs in steps, the length of the list should be trail_elngth*steps
# Another visual bug for ex 7
    - The trail seems to be a funny ring instead.