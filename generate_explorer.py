import json
import os

with open('.github/agents/code-explorer-template.html', 'r', encoding='utf-8') as f:
    template = f.read()

tabs = """
<button class="tab-btn active" onclick="switchTab('arch', this)">Architecture</button>
<button class="tab-btn" onclick="switchTab('patterns', this)">Patterns</button>
<button class="tab-btn" onclick="switchTab('typehints', this)">Type Hints</button>
<button class="tab-btn" onclick="switchTab('perf', this)">Performance</button>
<button class="tab-btn" onclick="switchTab('codereview', this)">Code Review</button>
<button class="tab-btn" onclick="switchTab('nextsteps', this)">Resources</button>
"""

panels = """
<div id="tab-arch" class="tab-panel active">
    <div class="arch-subnav">
        <button class="arch-btn active" onclick="switchArch('deps', this)">Dependencies</button>
        <button class="arch-btn" onclick="switchArch('calls', this)">Call Graph</button>
        <button class="arch-btn" onclick="switchArch('seq', this)">Runtime Sequence</button>
        <button class="arch-btn" onclick="switchArch('dflow', this)">Data Flow</button>
    </div>
    
    <div id="arch-deps" class="arch-panel active">
        <div class="diag-title">Project Dependencies</div>
        <div class="diag-container" id="diag-deps1"></div>
        <div class="diag-caption">External modules and library imports used in the application.</div>
    </div>
    <div id="arch-calls" class="arch-panel">
        <div class="diag-title">Function Call Graph</div>
        <div class="diag-container" id="diag-calls1"></div>
        <div class="diag-caption">Relationships between Pygame setup, the main loop, and Square class methods.</div>
    </div>
    <div id="arch-seq" class="arch-panel">
        <div class="diag-title">Game Loop Sequence</div>
        <div class="diag-container" id="diag-seq1"></div>
        <div class="diag-caption">Step-by-step frame execution including physical logic and collision.</div>
    </div>
    <div id="arch-dflow" class="arch-panel">
        <div class="diag-title">Squares List Flow</div>
        <div class="diag-container" id="diag-dflow1"></div>
        <div class="diag-caption">How the simulated objects trace through creation, iteration, object pooling and rendering.</div>
    </div>
</div>

<div id="tab-patterns" class="tab-panel">
    <div class="two-col">
        <div>
            <h3 class="section-head green">Good Patterns</h3>
            
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">♻️</span>
                    <span class="pattern-title">Object Pooling</span>
                </div>
                <div class="pattern-desc">Recycling objects using disabled_squares to minimize garbage collection.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>Preserves instances instead of destroying and instantiating memory.</span>
                    <span class="layer layer-eng"><span class="layer-label">Insights</span>Greatly helps Python maintain a consistent FPS.</span>
                    <span class="layer layer-arch"><span class="layer-label">Arch</span>Reduces the memory usage and GC latency spikes.</span>
                </div>
            </div>
            
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">📦</span>
                    <span class="pattern-title">Encapsulation</span>
                </div>
                <div class="pattern-desc">The Square class binds its own state and behavior.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>Groups related properties (x, y, speed) together.</span>
                    <span class="layer layer-eng"><span class="layer-label">Insights</span>Ensures that rendering logic does not have to recalculate object bounding boxes manually.</span>
                    <span class="layer layer-arch"><span class="layer-label">Arch</span>Creates an object-oriented domain model independent of the Pygame view.</span>
                </div>
            </div>
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">📐</span>
                    <span class="pattern-title">Consistent Constants</span>
                </div>
                <div class="pattern-desc">Using global constants for window boundaries and logic caps.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>`WINDOW_WIDTH`, `FPS`, `SUBSTEP` replace hardcoded numbers.</span>
                    <span class="layer layer-eng"><span class="layer-label">Insights</span>Prevents scaling bugs if dimensions suddenly expand.</span>
                    <span class="layer layer-arch"><span class="layer-label">Arch</span>Decouples configuration from operational structure.</span>
                </div>
            </div>
        </div>
        <div>
            <h3 class="section-head yellow">Potential Issues</h3>
            
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">⚠️</span>
                    <span class="pattern-title">Nested O(N^2) Checks</span>
                </div>
                <div class="pattern-desc">Cartesian product of physics tests scales terribly.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>Every square queries every other square for collisions.</span>
                    <span class="layer layer-eng"><span class="layer-label">Insights</span>As entities grow, calculation time explodes exponentially.</span>
                    <span class="layer layer-arch"><span class="layer-label">Arch</span>Monolithic looping prevents easy multi-threading optimizations later.</span>
                </div>
            </div>
        </div>
    </div>
</div>

<div id="tab-typehints" class="tab-panel">
    <div class="type-banner">
        <div class="score-big">3.5/5</div>
        <div class="score-verdict">Intermediate adoption: Signatures exist, specific instances like drawing use type hints, but container generics and deep methods run untyped.</div>
    </div>
    <div class="two-col">
        <div>
            <h3 class="section-head green">Strengths</h3>
            <ul>
                <li style="margin-bottom: 0.5rem"><strong>Explicit Object Types:</strong> Properly uses `pygame.Surface` on rendering interfaces natively resolving IDE checks.</li>
                <li><strong>Consistent Basics:</strong> The core init and primary lifecycle endpoints correctly declare `-> None`.</li>
            </ul>
        </div>
        <div>
            <h3 class="section-head red">Gaps</h3>
            <ul>
                <li style="margin-bottom: 0.5rem"><strong>Missing Container Generics:</strong> `disabledsquares: list` instead of `list[Square]`.</li>
                <li><strong>Omitted Key Returns:</strong> `squarecollision` returns boolean signals but isn't explicitly typed `-> bool`.</li>
            </ul>
        </div>
    </div>
</div>

<div id="tab-perf" class="tab-panel">
    <div class="card" style="margin-bottom: 1rem; text-align: center">
        <span class="badge-score">4.5 / 6</span><br><br>
        <span style="color:var(--muted)">Object pooling integration heavily optimized garbage collection, but mathematical overhead continues to limit entity scale.</span>
    </div>
    <div class="two-col">
        <div>
            <h3 class="section-head green">Wins</h3>
            <div class="perf-card">
                <div class="perf-title">Substepping Precision</div>
                <div class="perf-desc">Slicing updates (`self.vx / steps`) stops fast objects from skipping collision checks entirely.</div>
            </div>
            <div class="perf-card">
                <div class="perf-title">Object Pooling</div>
                <div class="perf-desc">Reassigning parameters to an existing cached object significantly saves instantiation performance overhead.</div>
            </div>
        </div>
        <div>
            <h3 class="section-head red">Risks</h3>
            <div class="perf-card">
                <div class="perf-title">Pygame Math Avoidance</div>
                <div class="perf-desc">Instead of `pygame.math.Vector2`, custom tuple allocations and explicit `math.hypot()` are executed in O(N^2) inner loops, thrashing CPU caches.</div>
            </div>
        </div>
    </div>
</div>

<div id="tab-codereview" class="tab-panel">
    <div class="review-layout">
        <div class="review-left">
            <div class="review-item selected" id="ri-0" onclick="selectReview(0)">
                <div class="ri-titlerow">
                    <span class="ri-title">List Iteration Defensive Copies</span>
                    <span class="badge badge-low">low</span>
                </div>
                <div class="ri-note">Using list(squares).</div>
            </div>
            <div class="review-item" id="ri-1" onclick="selectReview(1)">
                <div class="ri-titlerow">
                    <span class="ri-title">Nested O(N^2) Distance Math</span>
                    <span class="badge badge-medium">medium</span>
                </div>
                <div class="ri-note">Scalability limits frame delivery.</div>
            </div>
            <div class="review-item" id="ri-2" onclick="selectReview(2)">
                <div class="ri-titlerow">
                    <span class="ri-title">Magic Numbers in Random Distributions</span>
                    <span class="badge badge-low">low</span>
                </div>
                <div class="ri-note">Unclear constant thresholds.</div>
            </div>
            <div class="review-item" id="ri-3" onclick="selectReview(3)">
                <div class="ri-titlerow">
                    <span class="ri-title">Incomplete Return Annotations</span>
                    <span class="badge badge-low">low</span>
                </div>
                <div class="ri-note">Missing -> bool on conditional returns.</div>
            </div>
        </div>
        <div class="review-right" id="review-detail-panel">
        </div>
    </div>
</div>

<div id="tab-nextsteps" class="tab-panel">
    <div class="card">
        <h3>Further Reading</h3>
        <div class="ns-item">
            <div class="ns-num">1</div>
            <div class="ns-text">
                <a href="https://gameprogrammingpatterns.com/object-pool.html">Object Pool Pattern</a>
                <div class="ns-desc">Learn more deeply about the Object Pooling mechanism now used to cache your dead squares!</div>
            </div>
        </div>
        <div class="ns-item">
            <div class="ns-num">2</div>
            <div class="ns-text">
                <a href="https://refactoring.guru/design-patterns/state">The State Design Pattern</a>
                <div class="ns-desc">Encapsulate square "tired", "moving", and "fleeing" routines directly as independent states on Refactoring.Guru.</div>
            </div>
        </div>
        <div class="ns-item">
            <div class="ns-num">3</div>
            <div class="ns-text">
                <a href="https://www.pygame.org/docs/ref/math.html">Pygame Vector2 Mechanics</a>
                <div class="ns-desc">Utilize hardware-accelerated vector properties provided seamlessly inside the Pygame suite.</div>
            </div>
        </div>
    </div>
</div>
"""

reviews = [
    {
        "id": 0,
        "title": "Good Job: List Iteration Defensive Copies",
        "severity": "low",
        "fullExplanation": "You solved the iterator modification issue by explicitly copying the list `list(squares)` before the inner loops. This correctly safeguards from runtime bounds errors, although it introduces minor memory overhead.",
        "snippet": "for squarea in list(squares):\n    for squareb in list(squares):\n        # check interactions",
        "improvementHint": "Now you are safely bypassing modifying loops while iterating. Keep an eye on memory if the list grows considerably, but for now this fixes the previous high bug."
    },
    {
        "id": 1,
        "title": "Nested O(N^2) Distance Math",
        "severity": "medium",
        "fullExplanation": "The `squarecollision` and `flee` logic relies on cartesian interaction maps: evaluating everything against everything else continuously. Combining this with intense math ops limits entity counts severely.",
        "snippet": "for squarea in list(squares):\n    for squareb in list(squares):\n        if squarea != squareb:\n            squarea.squarecollision(squareb, squares, disabled_squares)",
        "improvementHint": "Adopt spatial partitioning mechanisms like a QuadTree or Grid bucket approach. If sticking to vanilla arrays, at least use `pygame.math.Vector2.distance_to()`."
    },
    {
        "id": 2,
        "title": "Magic Numbers in Random Distributions",
        "severity": "low",
        "fullExplanation": "Literals like `random.randint(1, 25-Square.pity) == 1` or `flee_strength = 0.3` restrict dynamic balancing and confuse configuration purposes.",
        "snippet": "if random.randint(1, 25-Square.pity) == 1:\n    #...",
        "improvementHint": "Replace literal integers with properly named module-level configuration variables like `SPAWN_CHANCE_INVERSE = 25`."
    },
    {
        "id": 3,
        "title": "Incomplete Return Annotations",
        "severity": "low",
        "fullExplanation": "Some functions return distinct signals out of deep conditional nesting without clearly conveying their contract to the IDE interface, forcing manual inspections.",
        "snippet": "def squarecollision(self, other, listofsquares, disabledsquares):\n    # ...\n    return True",
        "improvementHint": "Provide definitive `-> bool:` annotations and ensure a fallback `return False` is provided universally at the bottom of the structure."
    }
]

diagrams = {
    "deps1": r"""graph LR
    n1[main.py] --> p1[pygame]
    n1 --> p2[random]
    n1 --> p3[math]
    n1 --> p4[time]
    click p1 href "https://www.pygame.org/docs/" "Open docs"
    click p2 href "https://docs.python.org/3/library/random.html" "Open docs"
    click p3 href "https://docs.python.org/3/library/math.html" "Open docs"
    click p4 href "https://docs.python.org/3/library/time.html" "Open docs"
    """,
    "calls1": r"""graph TD
    c1[main module] --> c2[main loop]
    c2 --> c4[move]
    c2 --> c5[bordercollision]
    c2 --> c6[squarecollision]
    c2 --> c7[flee]
    c2 --> c8[draw]
    c2 --> c10[draw pause]
    c4 --> c11[bidfarewell]
    c6 --> c9[i want to KILL you]
    c5 --> c12[squarecreation]
    """,
    "seq1": r"""sequenceDiagram
    participant p1 as main
    participant p2 as pygame
    participant p3 as "Square obj"
    
    p1->>p2: init
    p1->>p2: get events
    
    p1->>p3: move units
    p1->>p3: bordercollision step
    
    p1->>p3: squarecollision query
    p1->>p3: flee logic
    
    p1->>p3: draw layer
    p1->>p2: flip display
    """,
    "dflow1": r"""graph TD
    d1[squarecreation method] --> d2[squares list]
    d3[disabled squares cache] -->|Object Pooling| d1
    d2 --> d4[Motion Updates]
    d4 --> d5[Collision Filter]
    d5 -->|bidfarewell| d3
    d5 --> d6[Screen Render]
    """
}

out = template.replace('<!-- SLOT:TITLE -->', 'main.py')
out = out.replace('<!-- SLOT:FILE_BADGE -->', 'main.py')
out = out.replace('<!-- SLOT:HEADER_META -->', '1st-year CS Pygame Logic & Architecture Analysis')
out = out.replace('<!-- SLOT:TAB_BUTTONS -->', tabs)
out = out.replace('<!-- SLOT:TAB_PANELS -->', panels)

review_str = ",\n".join([json.dumps(r) for r in reviews])
out = out.replace('/* SLOT:REVIEW_ITEMS */', review_str)

diagrams_str = ",\n".join([f'"{k}": String.raw`{v}`' for k, v in diagrams.items()])
out = out.replace('/* SLOT:DIAGRAMS_MAP */', diagrams_str)

with open('docs/code_explorer.html', 'w', encoding='utf-8') as f:
    f.write(out)

