import os
import time
import threading
import random
from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI

_ui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui")
ui = WebUI(assets_dir_path=_ui_dir)

boot_time = time.time()
last_click = 0.0

# ── Questions Database ────────────────────────
questions = [
    # --- Calculus 1 ---
    {"q": "What is the derivative of x^2?", "options": ["x", "2x", "x^3/3"], "correct": 1},
    {"q": "What is the integral of cos(x)?", "options": ["sin(x) + c", "-sin(x) + c", "-cos(x) + c"], "correct": 0},
    {"q": "Limit of sin(x)/x as x approaches 0 is:", "options": ["0", "Infinity", "1"], "correct": 2},
    {"q": "What is the derivative of e^x?", "options": ["x*e^(x-1)", "e^x", "ln(x)"], "correct": 1},
    {"q": "The domain of ln(x) is:", "options": ["x > 0", "x >= 0", "All real numbers"], "correct": 0},
    {"q": "What is the derivative of a constant?", "options": ["1", "0", "Undefined"], "correct": 1},
    {"q": "What is the integral of e^x?", "options": ["e^x + c", "x*e^x + c", "ln(x) + c"], "correct": 0},
    {"q": "If f'(x) = 0 for all x, then f(x) is:", "options": ["Linear", "Constant", "Exponential"], "correct": 1},

    # --- Algebra and Geometry ---
    {"q": "Determinant of an identity matrix is:", "options": ["0", "1", "Depends on size"], "correct": 1},
    {"q": "Dot product of two orthogonal vectors is:", "options": ["0", "1", "-1"], "correct": 0},
    {"q": "What is the dimension of R^3?", "options": ["1", "2", "3"], "correct": 2},
    {"q": "Cross product of two parallel vectors is:", "options": ["Zero vector", "Identity vector", "1"], "correct": 0},
    {"q": "The trace of a matrix is the sum of its:", "options": ["Rows", "Columns", "Diagonal elements"], "correct": 2},
    {"q": "A matrix multiplied by its inverse yields:", "options": ["Zero matrix", "Identity matrix", "Diagonal matrix"], "correct": 1},

    # --- C ---
    {"q": "Which library contains printf() in C?", "options": ["<stdlib.h>", "<stdio.h>", "<math.h>"], "correct": 1},
    {"q": "Array indices in C always start at:", "options": ["0", "1", "-1"], "correct": 0},
    {"q": "What is the standard size of a char in C?", "options": ["1 byte", "2 bytes", "4 bytes"], "correct": 0},
    {"q": "A pointer is a variable that stores a:", "options": ["Floating value", "Memory address", "String"], "correct": 1},
    {"q": "The logical AND operator in C is:", "options": ["&", "&&", "AND"], "correct": 1},
    {"q": "Which of the following is not a valid C variable name?", "options": ["int n", "int $main", "float j"], "correct": 1},
    {"q": "Which loop guarantees at least one execution?", "options": ["for", "while", "do-while"], "correct": 2},
    {"q": "Which of the following cannot be a variable name in C?", "options": ["class", "friend", "volatile"], "correct": 2},

    # --- C++ ---
    {"q": "Which of these is an OOP principle?", "options": ["Encapsulation", "Compilation", "Iteration"], "correct": 0},
    {"q": "Standard output stream in C++ is:", "options": ["cin", "cout", "printf"], "correct": 1},
    {"q": "The symbol used for a destructor is:", "options": ["*", "&", "~"], "correct": 2},
    {"q": "Default access specifier for a class is:", "options": ["Public", "Protected", "Private"], "correct": 2},
    {"q": "The 'new' keyword allocates memory on the:", "options": ["Stack", "Heap", "Registers"], "correct": 1},
    {"q": "Multiple functions with the same name is:", "options": ["Overloading", "Overriding", "Inheritance"], "correct": 0},
    {"q": "A virtual function allows for:", "options": ["Polymorphism", "Encapsulation", "Fast execution"], "correct": 0},
    {"q": "Which operator accesses a class member via pointer?", "options": [".", "->", "::"], "correct": 1},

    # --- Physics 1 ---
    {"q": "Newton's Second Law is expressed as:", "options": ["F = ma", "E = mc^2", "v = d/t"], "correct": 0},
    {"q": "The standard unit of Force is:", "options": ["Joule", "Watt", "Newton"], "correct": 2},
    {"q": "Kinetic energy formula is:", "options": ["mgh", "1/2 mv^2", "Fd"], "correct": 1},
    {"q": "Acceleration due to gravity on Earth is roughly:", "options": ["9.8 m/s^2", "10.5 m/s^2", "8.2 m/s^2"], "correct": 0},
    {"q": "Momentum is the product of mass and:", "options": ["Force", "Acceleration", "Velocity"], "correct": 2},
    {"q": "In an isolated system, energy is always:", "options": ["Created", "Destroyed", "Conserved"], "correct": 2},
    {"q": "The unit of Work is:", "options": ["Newton", "Joule", "Pascal"], "correct": 1},

    # --- Electrical Engineering ---
    {"q": "First Ohm's Law is stated as:", "options": ["P = VI", "V = IR", "I = VR"], "correct": 1},
    {"q": "The standard unit of resistance is:", "options": ["Ohm", "Farad", "Henry"], "correct": 0},
    {"q": "Kirchhoff's Current Law implies conservation of:", "options": ["Charge", "Energy", "Power"], "correct": 0},
    {"q": "Electric power formula is:", "options": ["P = VI", "P = V/R", "P = I^2/V"], "correct": 0},
    {"q": "Internal resistance of an ideal voltage source:", "options": ["Zero Ohms", "100 Ohms", "1 Ohm"], "correct": 0},
    {"q": "An inductor stores energy in a:", "options": ["Electric field", "Magnetic field", "Dielectric"], "correct": 1},

    # --- Calculus 2 and Probabilities ---
    {"q": "Partial derivative of x^2*y with respect to x:", "options": ["x^2", "2xy", "2x"], "correct": 1},
    {"q": "The gradient vector points in the direction of:", "options": ["Max increase", "Max decrease", "Zero change"], "correct": 0},
    {"q": "The probability of a certain/sure event is:", "options": ["0", "0.5", "1"], "correct": 2},
    {"q": "What's the sum of all probabilities in a distribution?", "options": ["0", "1", "100"], "correct": 1},
    {"q": "Expected value of a fair 6-sided dice:", "options": ["3", "3.5", "4"], "correct": 1},
    {"q": "The gradient of a scalar field is a:", "options": ["Scalar", "Vector", "Matrix"], "correct": 1},
    {"q": "If A and B are independent, P(A and B) = ", "options": ["P(A)+P(B)", "P(A)*P(B)", "P(A)-P(B)"], "correct": 1},
    {"q": "P(A|B)=(P(B|A)*P(A))/(P(B)). What's the name of this theorem?", "options": ["Levin", "Volt", "Bayes"], "correct": 2},

    # --- Physics 2 ---
    {"q": "The standard unit of electrical charge is:", "options": ["Coulomb", "Ampere", "Volt"], "correct": 0},
    {"q": "Coulomb's Law calculates:", "options": ["Magnetic flux", "Electrostatic force", "Resistance"], "correct": 1},
    {"q": "The standard unit of magnetic field is:", "options": ["Tesla", "Weber", "Henry"], "correct": 0},
    {"q": "Speed of light in vacuum is approx:", "options": ["3x10^6 m/s", "3x10^8 m/s", "3x10^10 m/s"], "correct": 1},
    {"q": "Capacitance formula is:", "options": ["C = Q/V", "C = QV", "C = V/Q"], "correct": 0},
    {"q": "Gauss's Law relates electric flux to:", "options": ["Mass", "Distance", "Enclosed charge"], "correct": 2},
    {"q": "Faraday's Law states changing magnetic flux induces:", "options": ["Resistance", "EMF", "Capacitance"], "correct": 1},

    # --- Communication Networks ---
    {"q": "How many layers are in the OSI Model?", "options": ["5", "7", "4"], "correct": 1},
    {"q": "Length of an IPv4 address is:", "options": ["32 bits", "64 bits", "128 bits"], "correct": 0},
    {"q": "Which protocol is at the Transport layer?", "options": ["HTTP", "TCP", "IP"], "correct": 1},
    {"q": "Default port for HTTP is:", "options": ["21", "80", "443"], "correct": 1},
    {"q": "The Ping command uses which protocol?", "options": ["TCP", "UDP", "ICMP"], "correct": 2},
    {"q": "A MAC address consists of how many bits?", "options": ["32", "48", "64"], "correct": 1},
    {"q": "DNS translates domain names into:", "options": ["MAC addresses", "IP addresses", "URLs"], "correct": 1},

    # --- Algorithms and Data Structures ---
    {"q": "Time complexity of binary search is:", "options": ["O(n)", "O(log n)", "O(n^2)"], "correct": 1},
    {"q": "Which structure follows LIFO?", "options": ["Queue", "Stack", "Tree"], "correct": 1},
    {"q": "Which structure follows FIFO?", "options": ["Stack", "Queue", "Heap"], "correct": 1},
    {"q": "Average case time complexity of QuickSort:", "options": ["O(n log n)", "O(n^2)", "O(n)"], "correct": 0},
    {"q": "A tree node with no children is a:", "options": ["Root", "Branch", "Leaf"], "correct": 2},
    {"q": "Edges in a tree with n nodes:", "options": ["n", "n-1", "n/2"], "correct": 1},
    {"q": "Resolving hash table collisions by storing multiple items in the same bucket is called:", "options": ["Open addressing", "Chaining", "Rehashing"], "correct": 1},

    # --- Operating Systems ---
    {"q": "Unlike processes, threads share:", "options": ["Registers", "Virtual Memory", "Program Counter"], "correct": 1},
    {"q": "How many conditions are required for a deadlock?", "options": ["2", "3", "4"], "correct": 2},
    {"q": "Semaphore P (wait) operation:", "options": ["Increments", "Decrements", "Resets"], "correct": 1},
    {"q": "Java keyword for mutual exclusion:", "options": ["synchronized", "volatile", "transient"], "correct": 0},
    {"q": "Virtual memory relies on:", "options": ["Paging", "Polling", "Spooling"], "correct": 0},
    {"q": "A Context Switch saves the state of the:", "options": ["RAM", "Hard Drive", "CPU"], "correct": 2},
    {"q": "A terminated process still in the process table:", "options": ["Orphan", "Zombie", "Daemon"], "correct": 1},

    # --- Databases and SQL ---
    {"q": "SQL command to retrieve data:", "options": ["GET", "FETCH", "SELECT"], "correct": 2},
    {"q": "A Primary Key must be unique and:", "options": ["Integer", "NOT NULL", "String"], "correct": 1},
    {"q": "When I speak of an ER model, ER stands for:", "options": ["Entity-Relationship", "Exact-Row", "Entity-Record"], "correct": 0},
    {"q": "A Foreign Key maintains:", "options": ["Referential integrity", "Performance", "Security"], "correct": 0},
    {"q": "SQL command to completely remove a table:", "options": ["DELETE", "DROP TABLE", "REMOVE"], "correct": 1},
    {"q": "The 'A' in ACID properties stands for:", "options": ["Accuracy", "Atomicity", "Availability"], "correct": 1},
    {"q": "A Join returning only matching rows is:", "options": ["INNER JOIN", "OUTER JOIN", "LEFT JOIN"], "correct": 0},

    # --- Software Engineering ---
    {"q": "UML Use Case diagrams show system functionality from:", "options": ["User perspective", "Code perspective", "Hardware level"], "correct": 0},
    {"q": "Which of these is an Agile framework?", "options": ["Waterfall", "Scrum", "Spiral"], "correct": 1},
    {"q": "The Singleton pattern ensures a class has:", "options": ["No instances", "Multiple instances", "One instance"], "correct": 2},
    {"q": "Design patterns are:", "options": ["Reusable solutions", "Code libraries", "Compilers"], "correct": 0},
    {"q": "A UML Class diagram represents the system's:", "options": ["Dynamic behavior", "Static structure", "Execution flow"], "correct": 1},
    {"q": "Encapsulation aims to hide:", "options": ["Internal state", "Public methods", "Inheritance"], "correct": 0},
    {"q": "The Waterfall model is characterized by:", "options": ["Iterative loops", "Sequential phases", "Daily standups"], "correct": 1},

    # --- PPM ---
    {"q": "The term 'Pixel' stands for:", "options": ["Picture Element", "Point Cell", "Pic-Scale"], "correct": 0},
    {"q": "The RGB color model is used primarily for:", "options": ["Printing", "Screens", "Painting"], "correct": 1},
    {"q": "Raster graphics are composed of:", "options": ["Mathematical formulas", "Pixels", "Vectors"], "correct": 1},
    {"q": "Vector graphics scale without losing quality because they use:", "options": ["Math formulas", "More pixels", "Compression"], "correct": 0},
    {"q": "Which is an example of lossy image compression?", "options": ["PNG", "BMP", "JPEG"], "correct": 2},
    {"q": "The Alpha channel in an image controls:", "options": ["Brightness", "Transparency", "Contrast"], "correct": 1},
    {"q": "Standard cinematic framerate is:", "options": ["24 fps", "60 fps", "120 fps"], "correct": 0}
]

# ── Game Starting State ───────────────────────────────────────────────────────────
state = {
    "start_screen":  True,
    "wait_result":   False,
    "game_over":     False,
    "current_q":     0,
    "score":         0,
    "question_text": "Press any button to start.",
    "options":       ["-", "-", "-"],
    "last_result": None,
    "last_correct_letter": "",
    "highest_score": 0,
    "new_record":    False,
    "result_title":  "",
    "result_desc":   "",
    "result_tier":   0
}

current_game_questions = []

def _broadcast(room=None):
    ui.send_message("state_update", state, room=room)

def manda_feedback(tipo):
    def _fire():
        try:
            Bridge.call("show_feedback", tipo, 0)
        except Exception as e:
            print(f"Ignored LED feedback: {e}")
    threading.Thread(target=_fire, daemon=True).start()

# ── Button Input Section ───────────────────────────────────────────────
def on_button_event(index: int, event_type: str):
    global last_click
    global current_game_questions

    if event_type != "press":
        return

    now = time.time()
    if now - boot_time < 2.0: return
    if now - last_click < 0.5: return
    last_click = now

    if state["start_screen"]:
        current_game_questions = random.sample(questions, 10)

        state["start_screen"]  = False
        state["wait_result"]   = False
        state["game_over"]     = False
        state["current_q"]     = 0
        state["score"]         = 0
        
        state["last_result"] = None
        state["last_correct_letter"] = ""
        state["result_title"]  = ""
        state["result_desc"]   = ""
        
        state["question_text"] = current_game_questions[0]["q"]
        state["options"]       = current_game_questions[0]["options"]
        
        _broadcast()           
        manda_feedback(2)      
        ui.send_message("play_bgm", "quiz")

    elif state["wait_result"]:
        state["wait_result"] = False
        state["game_over"]   = True
        state["question_text"] = "Press any button to return to the start screen."
        state["options"]       = ["-", "-", "-"]
        
        score = state["score"]
        if score == 0:
            state["result_title"] = "Damn."
            state["result_desc"]  = "Better luck next time.. This wasn't it. :("
            state["result_tier"]  = 0
        elif 1 <= score <= 5:
            state["result_title"] = "Eh…"
            state["result_desc"]  = "Practice makes perfect. Keep going and you will make it!"
            state["result_tier"]  = 1
        elif 6 <= score <= 9:
            state["result_title"] = "Good job!"
            state["result_desc"]  = "Not perfect, but still well done! You almost got it!"
            state["result_tier"]  = 2
        elif score == 10:
            state["result_title"] = "PERFECT!"
            state["result_desc"]  = "Either you are very well prepared.. or you tried again and again until you got down all the answers by memory.\nNo matter! Congratulations!"
            state["result_tier"]  = 3
        
        if score > state["highest_score"] and score > 0:
            state["highest_score"] = score
            state["new_record"]    = True

        _broadcast()
        manda_feedback(2)
        ui.send_message("play_result_audio", state["result_tier"])

    elif state["game_over"]:
        state["start_screen"]  = True
        state["game_over"]     = False
        state["wait_result"]   = False
        state["question_text"] = "Press any button to start."
        state["options"]       = ["-", "-", "-"]
        state["new_record"]    = False 
        
        _broadcast()
        manda_feedback(2)
        ui.send_message("play_bgm", "start")

    else:
        q = current_game_questions[state["current_q"]]
        correct = index == q["correct"]
        
        lettere = ["A", "B", "C"]
        state["last_result"] = correct
        state["last_correct_letter"] = lettere[q["correct"]]

        state["score"] += int(correct)
        state["current_q"] += 1

        if state["current_q"] < len(current_game_questions):
            nq = current_game_questions[state["current_q"]]
            state["question_text"] = nq["q"]
            state["options"]       = nq["options"]
        else:
            state["wait_result"]   = True
            state["question_text"] = "That's all! Press any button to find out your result."
            state["options"]       = ["-", "-", "-"]

        _broadcast()                        
        manda_feedback(1 if correct else 0) 
        ui.send_message("play_sound", "correct" if correct else "wrong")

Bridge.provide("button_event", on_button_event)

def on_connect(sid):
    global state
    
    state["start_screen"]  = True
    state["wait_result"]   = False
    state["game_over"]     = False
    state["current_q"]     = 0
    state["score"]         = 0
    state["question_text"] = "Press any button to start."
    state["options"]       = ["-", "-", "-"]
    state["last_result"]   = None
    state["last_correct_letter"] = ""
    state["new_record"]    = False
    state["result_title"]  = ""
    state["result_desc"]   = ""
    state["result_tier"]   = 0
    
    _broadcast(room=sid)
    ui.send_message("play_bgm", "start", room=sid)
    manda_feedback(2) 

ui.on_connect(on_connect)

App.run()