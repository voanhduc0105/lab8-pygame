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
    <!-- Existing arch panels -->
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
        <div class="diag-caption">Relationships between Pygame setup, the main loop, and Square class methods (including chase and flee).</div>
    </div>
    <div id="arch-seq" class="arch-panel">
        <div class="diag-title">Game Loop Sequence (with dt)</div>
        <div class="diag-container" id="diag-seq1"></div>
        <div class="diag-caption">Step-by-step frame execution utilizing delta time (dt) across updates.</div>
    </div>
    <div id="arch-dflow" class="arch-panel">
        <div class="diag-title">Squares List Flow</div>
        <div class="diag-container" id="diag-dflow1"></div>
        <div class="diag-caption">How the simulated objects trace through creation, iteration, object pooling, and rendering.</div>
    </div>
</div>

<div id="tab-patterns" class="tab-panel">
    <div class="two-col">
        <div>
            <h3 class="section-head green">Good Patterns</h3>
            
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">⏱️</span>
                    <span class="pattern-title">Delta Time (dt) Integration</span>
                </div>
                <div class="pattern-desc">Movement and logic now use delta time from the clock beautifully.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>`dt` normalizes logic updates independent of FPS.</span>
                </div>
            </div>

            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">🔘</span>
                    <span class="pattern-title">Debug GUI Flags</span>
                </div>
                <div class="pattern-desc">Using toggle_roe_flag & toggle_vector_flag to show invisible logic natively.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>Enables dynamic testing of variables.</span>
                </div>
            </div>
        </div>
        <div>
            <h3 class="section-head yellow">Potential Issues</h3>
            <div class="pattern-card">
                <div class="pattern-header">
                    <span class="pattern-icon">⚠️</span>
                    <span class="pattern-title">Global State Sprawl</span>
                </div>
                <div class="pattern-desc">Using `global pause` and global flag tracking within `main()`.</div>
                <div class="pattern-layers">
                    <span class="layer layer-basics"><span class="layer-label">Basics</span>Can make refactoring and multithreading difficult in the future.</span>
                </div>
            </div>
        </div>
    </div>
</div>

<div id="tab-typehints" class="tab-panel">
    <div class="type-banner">
        <div class="score-big">4.8/5</div>
        <div class="score-verdict">Excellent adoption: Just added forward references like `list['Square']` which formally defines object schemas. A massive improvement!</div>
    </div>
    <div class="two-col">
        <div>
            <h3 class="section-head green">Strengths</h3>
            <ul>
                <li style="margin-bottom: 0.5rem"><strong>Forward Referencing:</strong> Uses `list['Square']` to avoid circular import issues while still getting strong IDE typing.</li>
                <li><strong>Primitive Annotations:</strong> `dt: float`, `steps: int` properly specify explicit variables.</li>
            </ul>
        </div>
        <div>
            <h3 class="section-head red">Gaps</h3>
            <ul>
                <li><strong>Omitted Key Returns:</strong> `squarecollision` returns boolean signals but still lacks the explicit `-> bool` return hint.</li>
            </ul>
        </div>
    </div>
</div>

<div id="tab-perf" class="tab-panel">
    <div class="card" style="margin-bottom: 1rem; text-align: center">
        <span class="badge-score">4.5 / 6</span><br><br>
        <span style="color:var(--muted)">Delta time integration is a big win for frame pacing, but O(N^2) Math ops continue limiting scale.</span>
    </div>
    <div class="two-col">
        <div>
            <h3 class="section-head green">Wins</h3>
            <div class="perf-card">
                <div class="perf-title">Delta Time Framing</div>
                <div class="perf-desc">Slicing updates (`dt / steps`) bounds logic accurately even in slowdowns.</div>
            </div>
        </div>
        <div>
            <h3 class="section-head red">Risks</h3>
            <div class="perf-card">
                <div class="perf-title">Pygame Math Avoidance</div>
                <div class="perf-desc">Explicit `math.hypot()` executed in O(N^2) loops instead of fast Vector2 ops.</div>
            </div>
        </div>
    </div>
</div>

<div id="tab-codereview" class="tab-panel">
    <div class="review-layout">
        <div class="review-left">
            <div class="review-item selected" id="ri-0" onclick="selectReview(0)">
                <div class="ri-titlerow">
                    <span class="ri-title">Excellent Type Hint Advancements</span>
                    <span class="badge badge-low">low</span>
                </div>
                <div class="ri-note">Safely typed lists with 'Square'.</div>
            </div>
            <div class="review-item" id="ri-1" onclick="selectReview(1)">
                <div class="ri-titlerow">
                    <span class="ri-title">Repetitive Flee vs Chase Math</span>
                    <span class="badge badge-medium">medium</span>
                </div>
                <div class="ri-note">chase() and flee() duplicate logic.</div>
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
                <a href="https://refactoring.guru/design-patterns/state">The State Design Pattern</a>
                <div class="ns-desc">Encapsulate square "tired", "moving", "chasing", and "fleeing" routines.</div>
            </div>
        </div>
    </div>
</div>
"""

reviews = [
    {
        "id": 0,
        "title": "Type Hint Forward References",
        "severity": "low",
        "fullExplanation": "You correctly updated the typing gaps by using string-forward references for the Square class (`list['Square']`), solving the prior typing deficiency and improving intellisense enormously. Good job!",
        "snippet": "def squarecreation(listofsquares: list['Square'], disabledsquares: list['Square']):",
        "improvementHint": "Make sure you also add return hints for methods that return True/False or integers."
    },
    {
        "id": 1,
        "title": "Duplicated AI Logic",
        "severity": "medium",
        "fullExplanation": "The newly added `chase` and `flee` methods repeat almost all the same calculations and vector alignments only with flipped signs.",
        "snippet": "def flee(self, other...)\n    # math\ndef chase(self, other...)\n    # math",
        "improvementHint": "Refactor into a single method or utility that returns the vector between two points with a scalar modifier."
    }
]

diagrams = {
    "deps1": r"""graph LR
    n1[main.py] --> p1[pygame]
    n1 --> p2[random]
    n1 --> p3[math]
    n1 --> p4[time]
    """,
    "calls1": r"""graph TD
    c1[main loop] --> c2[Square.move]
    c1 --> c3[Square.bordercollision]
    c1 --> c4[Square.squarecollision]
    c1 --> c5[Square.flee]
    c1 --> c6[Square.chase]
    c1 --> c7[Square.draw]
    """,
    "seq1": r"""sequenceDiagram
    participant p1 as main
    participant p2 as pygame
    participant p3 as "Square obj"
    
    p1->>p2: clock.tick(FPS)
    p1->>p3: move(dt)
    p1->>p3: bordercollision()
    p1->>p3: squarecollision()
    p1->>p3: flee() 
    p1->>p3: chase()
    p1->>p3: draw()
    """,
    "dflow1": r"""graph TD
    d1[squarecreation] --> d2[squares list]
    d3[disabled squares pool] -->|Reuse/Reset Life| d1
    d2 --> d4[apply dt Updates]
    """
}

out = template.replace('<!-- SLOT:TITLE -->', 'main.py (Typing Update)')
out = out.replace('<!-- SLOT:FILE_BADGE -->', 'main.py')
out = out.replace('<!-- SLOT:HEADER_META -->', 'Pygame Logic Analysis - Latest Types & DT Update')
out = out.replace('<!-- SLOT:TAB_BUTTONS -->', tabs)
out = out.replace('<!-- SLOT:TAB_PANELS -->', panels)

review_str = ",\n".join([json.dumps(r) for r in reviews])
out = out.replace('/* SLOT:REVIEW_ITEMS */', review_str)

diagrams_str = ",\n".join([f'"{k}": String.raw`{v}`' for k, v in diagrams.items()])
out = out.replace('/* SLOT:DIAGRAMS_MAP */', diagrams_str)

with open('docs/code_explorer.html', 'w', encoding='utf-8') as f:
    f.write(out)

