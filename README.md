# The Quiz Show

An interactive Computer Engineering quiz game physically controlled via Arduino hardware, featuring a synthwave/neon-style web interface. 
Players answer questions by pressing the physical A, B, and C buttons on the **Modulino Buttons** module, 
while questions and options are displayed in real-time in the browser.

---

## Overview

The app consists of three communicating layers:

```
[Arduino physical buttons] ──► [Python Server] ──► [Web Interface in browser]
```

- The **Arduino hardware** detects button presses and displays visual feedback on the LED matrix.
- The **Python server** manages all quiz logic: questions, scoring, and match state.
- The **web interface** displays questions, options, and scores, while playing background music and sound effects.

---

## Game Flow

### 1. Start Screen
Opening the app in the browser shows a black screen displaying "Click here to start the game." — required to unlock browser audio. Once clicked, the waiting music begins and the game is ready to start.

### 2. Match Start
Press **any** of the three physical buttons (A, B, or C). The server randomly selects **10 questions** from the database (which contains 100) and the match begins. The music switches to the quiz theme.

### 3. Answering Questions
For each question, three options labeled A, B, and C are displayed. Press the physical button corresponding to the chosen answer:
- If the answer is **correct**: the LED matrix displays a circle (○), the correct answer sound plays, and the score increases.
- If the answer is **incorrect**: the LED matrix displays an X, the wrong answer sound plays, and the correct letter is revealed.

### 4. Final Suspense
After the tenth question, the screen displays "That's all! Press any button to find out your result." — a suspenseful transition before revealing the final score.

### 5. Results Screen
Pressing a button reveals the final grade, accompanied by dedicated audio followed by the end-game music theme. The outcome depends on the score:

| Score | Title | Tier |
|---|---|---|
| 0 | Damn. | Red |
| 1 – 5 | Eh… | Orange |
| 6 – 9 | Good job! | Green |
| 10 | PERFECT! | Gold |

Beating the personal session record displays the **"New Record!"** badge.

### 6. Return to Start
Pressing any button on the results screen returns to the start screen, ready for a new match. The session's highest score remains visible in the top left corner.

---

## Included Questions

The database contains **100 university-level questions** from Computer Engineering Bachelor's degree courses.
Each match randomly selects 10 unique questions with no repeats during the current game.

---

## Web Interface

The interface features a **synthwave/neon** theme with a dark background and an animated grid. The top section includes:
- **"Highest Score" badge** in the top left, displaying the session's peak score.
- **Connection indicator** in the top right (green = connected, red = disconnected).
- **Quiz logo** centered in the header.
- **Current score** (`SCORE: X/10`).
- **Volume controls**: two independent sliders for background music (BGM) and sound effects (SFX).

---

## Project Structure


```

interactive-quiz-unilab/
├── app.yaml              App configuration (name, icon, dependencies)
├── python/
│   └── main.py           Quiz logic and hardware communication
├── sketch/
│   └── sketch.ino        Arduino firmware (button handling and LED matrix)
└── ui/
├── index.html            Page structure
├── app.js                Interface logic and Socket.IO communication
├── styles.css            Styling (synthwave theme)
├── logo.png              Quiz logo
├── favicon.png           Browser tab icon
└── audio/                Audio files (.ogg)

```

---

## Hardware Requirements

- Compatible **Arduino** board (e.g., Arduino UNO R4 WiFi)
- **Modulino Buttons**: module equipped with three physical buttons and RGB LEDs
- Arduino **LED Matrix** (built into supported boards)

---

## Adding or Modifying Questions

Questions are stored in the `questions` list inside `python/main.py`. Each entry follows this format:

```python
{"q": "Question text?", "options": ["Option A", "Option B", "Option C"], "correct": 1}

```

The `correct` field represents the zero-based **index** (0, 1, or 2) of the valid option. Questions can be added, modified, or removed freely; the app will always randomly pick 10 questions per match.