# Architecture Documentation

## Scope
This document describes the concrete architecture implemented in [main.py](main.py) and the documentation generator utility in [generate_explorer.py](generate_explorer.py).

## 1) Module Dependency Graph
```mermaid
graph LR
    MAIN["main.py"] --> PYG["pygame"]
    MAIN --> RNG["random"]
    MAIN --> MATH["math"]
    MAIN --> TIME["time"]
    EXPL["generate_explorer.py"] --> JSON["json"]
    EXPL --> OS["os"]
```

Notes:
- The simulation runtime is centered in [main.py](main.py).
- The docs utility in [generate_explorer.py](generate_explorer.py) is separate from runtime execution.

## 2) High-Level Runtime Flow
```mermaid
flowchart TD
    START["Program Start"] --> INIT["main(): pygame init and window setup"]
    INIT --> SEED["Create initial squares list"]
    SEED --> LOOP{"running flag true?"}
    LOOP -- "Yes" --> TICK["Frame tick: dt = clock.tick(FPS) / 1000"]
    TICK --> EVENTS["Process pygame events"]
    EVENTS --> PAUSE{"pause active?"}
    PAUSE -- "No" --> UPDATE["SUBSTEP movement and border collisions"]
    UPDATE --> PAIRS["Pairwise collision/flee/chase checks"]
    PAIRS --> RENDER["Draw overlays, squares, HUD"]
    PAUSE -- "Yes" --> MENU["Draw pause overlay and buttons"]
    MENU --> RENDER
    RENDER --> FLIP["pygame.display.flip()"]
    FLIP --> LOOP
    LOOP -- "No" --> QUIT["pygame.quit() and exit"]
```

Notes:
- The pause branch gates simulation updates while still rendering UI.
- The simulation can terminate when no active squares remain.

## 3) Function-Level Call Graph
```mermaid
graph TD
    ENTRY["__main__ entry"] --> MAINFN["main()"]

    MAINFN --> SQINIT["Square() constructor"]
    MAINFN --> EVTS["pygame.event.get()"]
    MAINFN --> MOVE["Square.move(dt, steps, squares, disabled_squares)"]
    MAINFN --> BORD["Square.bordercollision(squares, disabled_squares)"]
    MAINFN --> COLL["Square.squarecollision(other, squares, disabled_squares)"]
    MAINFN --> FLEE["Square.flee(other)"]
    MAINFN --> CHASE["Square.chase(other)"]
    MAINFN --> DRAW["Square.draw(screen)"]
    MAINFN --> DPAUSE["draw_pause(screen, surface, font, flags)"]

    MOVE --> BYE["Square.bidfarewell(squares, disabled_squares)"]
    BORD --> CREATE["Square.squarecreation(squares, disabled_squares)"]
    COLL --> GETA["Square.getrect()"]
    COLL --> KILL["Square.i_want_to_KILL_you(other)"]
    COLL --> CREATE
```

Notes:
- Call edges reflect direct method/function invocations present in [main.py](main.py).
- [draw_pause](main.py#L314) is used only in paused rendering.

## 4) Primary Execution Sequence (Full Frame Path)
```mermaid
sequenceDiagram
    participant BOOT as "Python Runtime"
    participant APP as "main()"
    participant PG as "Pygame"
    participant SQ as "Square Instances"
    participant UI as "Pause UI"

    BOOT->>APP: "Call main() from __main__"
    APP->>PG: "init(), set_mode(), Clock(), SysFont()"
    APP->>SQ: "Create initial list with Square()"

    loop "Per-frame while running"
        APP->>PG: "clock.tick(FPS) -> dt"
        APP->>PG: "poll events"

        alt "Quit event or no squares"
            APP->>APP: "set running = False"
        else "Continue running"
            alt "pause == False"
                loop "SUBSTEP updates"
                    APP->>SQ: "move(dt, SUBSTEP, squares, disabled_squares)"
                    APP->>SQ: "bordercollision(squares, disabled_squares)"
                end
                loop "Pairwise square interactions"
                    APP->>SQ: "squarecollision(other, squares, disabled_squares)"
                    APP->>SQ: "flee(other)"
                    APP->>SQ: "chase(other)"
                end
            else "pause == True"
                APP->>UI: "draw_pause(...)"
                UI-->>APP: "return reset/toggle button rects"
                APP->>APP: "handle pause-button clicks"
            end

            APP->>SQ: "draw(screen) for each active square"
            APP->>PG: "display.flip()"
        end
    end

    APP->>PG: "quit()"
```

## 5) Utility Script Flow ([generate_explorer.py](generate_explorer.py))
```mermaid
flowchart LR
    START["Script Start"] --> READTPL["Read HTML template file"]
    READTPL --> BUILD["Build tabs, panels, reviews, diagrams strings"]
    BUILD --> REPL["Apply placeholder replacements"]
    REPL --> WRITE["Write docs/code_explorer.html"]
    WRITE --> END["Script End"]
```

Notes:
- This path is file-generation logic and does not participate in the Pygame runtime loop.
