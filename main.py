
import tkinter as tk
from tkinter import ttk, messagebox
import random
from algorithms.bubble_sort import bubble_sort_steps
from algorithms.selection_sort import selection_sort_steps
from algorithms.insertion_sort import insertion_sort_steps


# ============================================================
# COLORS
# ============================================================

BG = "#0f172a"
PANEL = "#1e293b"
PANEL_2 = "#111827"
PANEL_3 = "#172033"

TEXT = "#f8fafc"
MUTED = "#94a3b8"

ACCENT = "#38bdf8"
GREEN = "#22c55e"
RED = "#ef4444"
YELLOW = "#facc15"
PURPLE = "#a78bfa"

BORDER = "#334155"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("AlgoVision — Algorithm Visualization & Performance Analysis")
root.geometry("1280x820")
root.minsize(1150, 720)
root.configure(bg=BG)


# ============================================================
# GLOBAL VARIABLES
# ============================================================

numbers = []

sorting = False
paused = False
callback_id = None

comparisons = 0
swaps = 0
operations = 0

bubble_i = 0
bubble_j = 0

selection_i = 0
selection_j = 1
min_index = 0

insertion_i = 1
insertion_j = 0
insertion_key = 0
insertion_initialized = False


# ============================================================
# ALGORITHM COMPLEXITY
# ============================================================

complexity_info = {
    "Bubble Sort": {
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    },

    "Selection Sort": {
        "best": "O(n²)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    },

    "Insertion Sort": {
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    }
}


# ============================================================
# ALGORITHM CODE
# ============================================================

algorithm_code = {

    "Bubble Sort": [
        "for i in range(n):",
        "    for j in range(0, n-i-1):",
        "        if arr[j] > arr[j+1]:",
        "            swap(arr[j], arr[j+1])"
    ],

    "Selection Sort": [
        "for i in range(n):",
        "    min_index = i",
        "    for j in range(i+1, n):",
        "        if arr[j] < arr[min_index]:",
        "            min_index = j",
        "    swap(arr[i], arr[min_index])"
    ],

    "Insertion Sort": [
        "for i in range(1, n):",
        "    key = arr[i]",
        "    j = i - 1",
        "    while j >= 0 and arr[j] > key:",
        "        arr[j+1] = arr[j]",
        "        j -= 1",
        "    arr[j+1] = key"
    ]
}


# ============================================================
# VARIABLES
# ============================================================

algorithm_var = tk.StringVar(value="Bubble Sort")
dataset_var = tk.StringVar()
speed_var = tk.IntVar(value=50)

comparison_var = tk.StringVar(value="0")
swap_var = tk.StringVar(value="0")
operation_var = tk.StringVar(value="Ready")

status_var = tk.StringVar(value="READY")
size_var = tk.StringVar(value="0 elements")

best_var = tk.StringVar(value="O(n)")
average_var = tk.StringVar(value="O(n²)")
worst_var = tk.StringVar(value="O(n²)")
space_var = tk.StringVar(value="O(1)")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def update_status(status):
    status_var.set(status)


def update_metrics():
    comparison_var.set(str(comparisons))
    swap_var.set(str(swaps))
    operation_var.set(str(operations))


def update_size():
    size_var.set(f"{len(numbers)} elements")


def cancel_pending_callback():
    global callback_id

    if callback_id is not None:
        try:
            root.after_cancel(callback_id)
        except tk.TclError:
            pass

        callback_id = None


def schedule_next(callback):
    global callback_id

    cancel_pending_callback()

    if sorting and not paused:
        callback_id = root.after(
            get_animation_speed(),
            callback
        )


def get_animation_speed():
    speed = speed_var.get()

    delay = int(800 - (speed * 7))

    if delay < 50:
        delay = 50

    return delay


# ============================================================
# DATASET
# ============================================================

def parse_dataset():

    text = dataset_var.get().strip()

    if not text:
        messagebox.showwarning(
            "Dataset Required",
            "Please enter some numbers."
        )
        return None

    try:
        values = [
            int(x.strip())
            for x in text.split(",")
            if x.strip()
        ]

        if len(values) < 2:
            messagebox.showwarning(
                "Dataset Too Small",
                "Enter at least 2 numbers."
            )
            return None

        if len(values) > 30:
            messagebox.showwarning(
                "Dataset Too Large",
                "Please enter maximum 30 numbers."
            )
            return None

        return values

    except ValueError:

        messagebox.showerror(
            "Invalid Dataset",
            "Use numbers separated by commas.\n\nExample:\n64, 25, 12, 22, 11"
        )

        return None


def load_dataset():

    global numbers

    if sorting:
        return

    values = parse_dataset()

    if values is None:
        return

    numbers = values

    reset_metrics()
    draw_bars()

    update_status("READY")
    operation_var.set("Dataset loaded successfully.")

    update_size()
    update_buttons()


def generate_random():

    global numbers

    if sorting:
        return

    numbers = [
        random.randint(10, 100)
        for _ in range(random.randint(6, 12))
    ]

    dataset_var.set(", ".join(map(str, numbers)))

    reset_metrics()
    draw_bars()

    update_status("READY")
    operation_var.set("Random dataset generated.")

    update_size()
    update_buttons()


# ============================================================
# METRICS
# ============================================================

def reset_metrics():

    global comparisons
    global swaps
    global operations

    comparisons = 0
    swaps = 0
    operations = 0

    comparison_var.set("0")
    swap_var.set("0")


# ============================================================
# DRAW VISUALIZATION
# ============================================================

def draw_bars(highlight=None):

    canvas.delete("all")

    if not numbers:
        canvas.create_text(
            430,
            210,
            text="Enter a dataset to begin visualization",
            fill=MUTED,
            font=("Segoe UI", 16)
        )
        return

    width = 820
    height = 400

    margin_left = 45
    margin_right = 25
    margin_top = 30
    margin_bottom = 55

    usable_width = width - margin_left - margin_right
    usable_height = height - margin_top - margin_bottom

    bar_width = usable_width / len(numbers)

    max_value = max(numbers)

    for i, value in enumerate(numbers):

        x1 = margin_left + i * bar_width + 5
        x2 = margin_left + (i + 1) * bar_width - 5

        bar_height = (
            value / max_value
        ) * usable_height

        y2 = height - margin_bottom
        y1 = y2 - bar_height

        fill = ACCENT

        if highlight and i in highlight:
            fill = YELLOW

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=fill,
            outline=""
        )

        canvas.create_text(
            (x1 + x2) / 2,
            y1 - 12,
            text=str(value),
            fill=TEXT,
            font=("Segoe UI", 9, "bold")
        )

        canvas.create_text(
            (x1 + x2) / 2,
            y2 + 18,
            text=str(i),
            fill=MUTED,
            font=("Segoe UI", 9)
        )


# ============================================================
# COMPLEXITY PANEL
# ============================================================

def update_complexity():

    algorithm = algorithm_var.get()

    info = complexity_info[algorithm]

    best_var.set(info["best"])
    average_var.set(info["average"])
    worst_var.set(info["worst"])
    space_var.set(info["space"])

    update_code_panel()


# ============================================================
# LIVE CODE PANEL
# ============================================================

def update_code_panel(highlight_line=None):

    for widget in code_inner.winfo_children():
        widget.destroy()

    algorithm = algorithm_var.get()

    code_lines = algorithm_code[algorithm]

    for index, line in enumerate(code_lines):

        line_number = index + 1

        if highlight_line == line_number:

            frame = tk.Frame(
                code_inner,
                bg="#243b53"
            )

            frame.pack(
                fill="x",
                padx=5,
                pady=1
            )

            number_label = tk.Label(
                frame,
                text=f"{line_number:>2}",
                width=3,
                bg="#243b53",
                fg=ACCENT,
                font=("Consolas", 10, "bold")
            )

            number_label.pack(
                side="left"
            )

            code_label = tk.Label(
                frame,
                text=line,
                anchor="w",
                bg="#243b53",
                fg=TEXT,
                font=("Consolas", 10)
            )

            code_label.pack(
                side="left",
                fill="x"
            )

        else:

            frame = tk.Frame(
                code_inner,
                bg=PANEL_2
            )

            frame.pack(
                fill="x",
                padx=5,
                pady=1
            )

            number_label = tk.Label(
                frame,
                text=f"{line_number:>2}",
                width=3,
                bg=PANEL_2,
                fg=MUTED,
                font=("Consolas", 10)
            )

            number_label.pack(
                side="left"
            )

            code_label = tk.Label(
                frame,
                text=line,
                anchor="w",
                bg=PANEL_2,
                fg="#cbd5e1",
                font=("Consolas", 10)
            )

            code_label.pack(
                side="left",
                fill="x"
            )


# ============================================================
# BUBBLE SORT
# ============================================================

def start_bubble_sort():

    global bubble_i
    global bubble_j
    global sorting

    bubble_i = 0
    bubble_j = 0
    sorting = True

    update_status("RUNNING")
    update_buttons()

    bubble_sort_step()


def bubble_sort_step():

    global bubble_i
    global bubble_j
    global comparisons
    global swaps
    global operations
    global sorting

    if not sorting or paused:
        return

    n = len(numbers)

    if bubble_i >= n - 1:

        sorting = False

        draw_bars()

        update_status("COMPLETED")
        operation_var.set("Bubble Sort completed successfully.")

        update_code_panel()

        update_buttons()

        return

    if bubble_j >= n - bubble_i - 1:

        bubble_i += 1
        bubble_j = 0

        schedule_next(bubble_sort_step)
        return

    comparisons += 1
    operations += 1

    comparison_var.set(str(comparisons))

    operation_var.set(
        f"Comparing index {bubble_j} and {bubble_j + 1}"
    )

    draw_bars(
        [bubble_j, bubble_j + 1]
    )

    update_code_panel(3)

    if numbers[bubble_j] > numbers[bubble_j + 1]:

        numbers[bubble_j], numbers[bubble_j + 1] = (
            numbers[bubble_j + 1],
            numbers[bubble_j]
        )

        swaps += 1
        operations += 1

        swap_var.set(str(swaps))

        operation_var.set(
            f"Swapped index {bubble_j} and {bubble_j + 1}"
        )

        draw_bars(
            [bubble_j, bubble_j + 1]
        )

        update_code_panel(4)

    bubble_j += 1

    schedule_next(bubble_sort_step)


# ============================================================
# SELECTION SORT
# ============================================================

def start_selection_sort():

    global selection_i
    global selection_j
    global min_index
    global sorting

    selection_i = 0
    selection_j = 1
    min_index = 0

    sorting = True

    update_status("RUNNING")
    update_buttons()

    selection_sort_step()


def selection_sort_step():

    global selection_i
    global selection_j
    global min_index
    global comparisons
    global swaps
    global operations
    global sorting

    if not sorting or paused:
        return

    n = len(numbers)

    if selection_i >= n - 1:

        sorting = False

        draw_bars()

        update_status("COMPLETED")
        operation_var.set(
            "Selection Sort completed successfully."
        )

        update_code_panel()
        update_buttons()

        return

    if selection_j >= n:

        if min_index != selection_i:

            numbers[selection_i], numbers[min_index] = (
                numbers[min_index],
                numbers[selection_i]
            )

            swaps += 1
            operations += 1

            swap_var.set(str(swaps))

            operation_var.set(
                f"Placed minimum value at index {selection_i}"
            )

            draw_bars(
                [selection_i, min_index]
            )

            update_code_panel(6)

        selection_i += 1
        selection_j = selection_i + 1
        min_index = selection_i

        schedule_next(selection_sort_step)

        return

    comparisons += 1
    operations += 1

    comparison_var.set(str(comparisons))

    operation_var.set(
        f"Comparing index {selection_j} with current minimum"
    )

    draw_bars(
        [min_index, selection_j]
    )

    update_code_panel(4)

    if numbers[selection_j] < numbers[min_index]:

        min_index = selection_j

        operation_var.set(
            f"New minimum found at index {min_index}"
        )

        update_code_panel(5)

    selection_j += 1

    schedule_next(selection_sort_step)


# ============================================================
# INSERTION SORT
# ============================================================

def start_insertion_sort():

    global insertion_i
    global insertion_j
    global insertion_key
    global insertion_initialized
    global sorting

    insertion_i = 1
    insertion_j = 0
    insertion_key = 0
    insertion_initialized = False

    sorting = True

    update_status("RUNNING")
    update_buttons()

    insertion_sort_step()


def insertion_sort_step():

    global insertion_i
    global insertion_j
    global insertion_key
    global insertion_initialized

    global comparisons
    global swaps
    global operations
    global sorting

    if not sorting or paused:
        return

    n = len(numbers)

    if insertion_i >= n:

        sorting = False

        draw_bars()

        update_status("COMPLETED")

        operation_var.set(
            "Insertion Sort completed successfully."
        )

        update_code_panel()
        update_buttons()

        return

    if not insertion_initialized:

        insertion_key = numbers[insertion_i]
        insertion_j = insertion_i - 1
        insertion_initialized = True

        operation_var.set(
            f"Selected {insertion_key} as current key"
        )

        draw_bars([insertion_i])

        update_code_panel(2)

        schedule_next(insertion_sort_step)

        return

    if insertion_j >= 0:

        comparisons += 1
        operations += 1

        comparison_var.set(str(comparisons))

        operation_var.set(
            f"Comparing {numbers[insertion_j]} with {insertion_key}"
        )

        draw_bars(
            [insertion_j, insertion_j + 1]
        )

        update_code_panel(4)

        if numbers[insertion_j] > insertion_key:

            numbers[insertion_j + 1] = numbers[insertion_j]

            swaps += 1
            operations += 1

            swap_var.set(str(swaps))

            operation_var.set(
                f"Moved {numbers[insertion_j]} one position right"
            )

            draw_bars(
                [insertion_j, insertion_j + 1]
            )

            update_code_panel(5)

            insertion_j -= 1

            schedule_next(insertion_sort_step)

            return

    numbers[insertion_j + 1] = insertion_key

    operations += 1

    operation_var.set(
        f"Inserted {insertion_key} at index {insertion_j + 1}"
    )

    draw_bars(
        [insertion_j + 1]
    )

    update_code_panel(6)

    insertion_i += 1
    insertion_initialized = False

    schedule_next(insertion_sort_step)


# ============================================================
# START SORT
# ============================================================

def start_sort():

    global numbers

    if sorting:
        return

    if len(numbers) < 2:

        values = parse_dataset()

        if values is None:
            return

        numbers = values

    reset_metrics()

    global paused
    paused = False

    algorithm = algorithm_var.get()

    if algorithm == "Bubble Sort":
        start_bubble_sort()

    elif algorithm == "Selection Sort":
        start_selection_sort()

    elif algorithm == "Insertion Sort":
        start_insertion_sort()


# ============================================================
# PAUSE
# ============================================================

def pause_sort():

    global paused

    if sorting and not paused:

        paused = True

        cancel_pending_callback()

        update_status("PAUSED")

        operation_var.set(
            "Visualization paused — state preserved."
        )

        update_buttons()


# ============================================================
# RESUME
# ============================================================

def resume_sort():

    global paused

    if sorting and paused:

        paused = False

        update_status("RUNNING")

        operation_var.set(
            "Visualization resumed — continuing from paused state."
        )

        update_buttons()

        algorithm = algorithm_var.get()

        if algorithm == "Bubble Sort":
            bubble_sort_step()

        elif algorithm == "Selection Sort":
            selection_sort_step()

        elif algorithm == "Insertion Sort":
            insertion_sort_step()


# ============================================================
# RESET
# ============================================================

def reset_visualization():

    global sorting
    global paused

    sorting = False
    paused = False

    cancel_pending_callback()

    reset_metrics()

    update_status("READY")

    operation_var.set(
        "Visualization reset."
    )

    draw_bars()

    update_buttons()


# ============================================================
# BUTTON STATE
# ============================================================

def update_buttons():

    if sorting and not paused:

        start_button.config(state="disabled")
        load_button.config(state="disabled")
        random_button.config(state="disabled")

        pause_button.config(state="normal")
        resume_button.config(state="disabled")

        algorithm_menu.config(state="disabled")

    elif sorting and paused:

        start_button.config(state="disabled")
        load_button.config(state="disabled")
        random_button.config(state="disabled")

        pause_button.config(state="disabled")
        resume_button.config(state="normal")

        algorithm_menu.config(state="disabled")

    else:

        start_button.config(state="normal")
        load_button.config(state="normal")
        random_button.config(state="normal")

        pause_button.config(state="disabled")
        resume_button.config(state="disabled")

        algorithm_menu.config(state="readonly")


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x",
    padx=25,
    pady=(18, 8)
)


title = tk.Label(
    header,
    text="AlgoVision",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 25, "bold")
)

title.pack(
    side="left"
)


subtitle = tk.Label(
    header,
    text="Interactive Algorithm Visualization & Performance Analysis",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
)

subtitle.pack(
    side="left",
    padx=18,
    pady=(7, 0)
)


status_frame = tk.Frame(
    header,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

status_frame.pack(
    side="right"
)


status_dot = tk.Label(
    status_frame,
    text="●",
    bg=PANEL,
    fg=GREEN,
    font=("Segoe UI", 10)
)

status_dot.pack(
    side="left",
    padx=(10, 4),
    pady=7
)


status_label = tk.Label(
    status_frame,
    textvariable=status_var,
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
)

status_label.pack(
    side="left",
    padx=(0, 10)
)


# ============================================================
# CONTROL PANEL
# ============================================================

control_frame = tk.Frame(
    root,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

control_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


# Algorithm

tk.Label(
    control_frame,
    text="ALGORITHM",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8, "bold")
).grid(
    row=0,
    column=0,
    padx=(15, 5),
    pady=(10, 2),
    sticky="w"
)


algorithm_menu = ttk.Combobox(
    control_frame,
    textvariable=algorithm_var,
    values=[
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort"
    ],
    state="readonly",
    width=18
)

algorithm_menu.grid(
    row=1,
    column=0,
    padx=(15, 8),
    pady=(0, 12)
)


algorithm_menu.bind(
    "<<ComboboxSelected>>",
    lambda event: update_complexity()
)


# Dataset

tk.Label(
    control_frame,
    text="DATASET",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8, "bold")
).grid(
    row=0,
    column=1,
    padx=5,
    pady=(10, 2),
    sticky="w"
)


dataset_entry = tk.Entry(
    control_frame,
    textvariable=dataset_var,
    width=34,
    bg=PANEL_2,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    font=("Segoe UI", 10)
)

dataset_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=(0, 12)
)


# Load

load_button = tk.Button(
    control_frame,
    text="Load",
    command=load_dataset,
    bg=PANEL_3,
    fg=TEXT,
    activebackground="#26364d",
    activeforeground=TEXT,
    relief="flat",
    padx=15,
    cursor="hand2"
)

load_button.grid(
    row=1,
    column=2,
    padx=4,
    pady=(0, 12)
)


# Random

random_button = tk.Button(
    control_frame,
    text="Random",
    command=generate_random,
    bg=PANEL_3,
    fg=TEXT,
    activebackground="#26364d",
    activeforeground=TEXT,
    relief="flat",
    padx=15,
    cursor="hand2"
)

random_button.grid(
    row=1,
    column=3,
    padx=4,
    pady=(0, 12)
)


# Start

start_button = tk.Button(
    control_frame,
    text="▶  Start",
    command=start_sort,
    bg=ACCENT,
    fg="#082f49",
    activebackground="#7dd3fc",
    activeforeground="#082f49",
    relief="flat",
    font=("Segoe UI", 9, "bold"),
    padx=18,
    cursor="hand2"
)

start_button.grid(
    row=1,
    column=4,
    padx=8,
    pady=(0, 12)
)


# Pause

pause_button = tk.Button(
    control_frame,
    text="Ⅱ  Pause",
    command=pause_sort,
    bg=PANEL_3,
    fg=TEXT,
    activebackground="#26364d",
    activeforeground=TEXT,
    relief="flat",
    padx=15,
    state="disabled",
    cursor="hand2"
)

pause_button.grid(
    row=1,
    column=5,
    padx=4,
    pady=(0, 12)
)


# Resume

resume_button = tk.Button(
    control_frame,
    text="▶  Resume",
    command=resume_sort,
    bg=PANEL_3,
    fg=TEXT,
    activebackground="#26364d",
    activeforeground=TEXT,
    relief="flat",
    padx=15,
    state="disabled",
    cursor="hand2"
)

resume_button.grid(
    row=1,
    column=6,
    padx=4,
    pady=(0, 12)
)


# Reset

reset_button = tk.Button(
    control_frame,
    text="Reset",
    command=reset_visualization,
    bg=PANEL_3,
    fg=TEXT,
    activebackground="#26364d",
    activeforeground=TEXT,
    relief="flat",
    padx=15,
    cursor="hand2"
)

reset_button.grid(
    row=1,
    column=7,
    padx=(4, 15),
    pady=(0, 12)
)


# Speed

tk.Label(
    control_frame,
    text="SPEED",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8, "bold")
).grid(
    row=0,
    column=8,
    padx=(12, 4),
    pady=(10, 2),
    sticky="w"
)


speed_scale = tk.Scale(
    control_frame,
    from_=1,
    to=100,
    orient="horizontal",
    variable=speed_var,
    bg=PANEL,
    fg=TEXT,
    troughcolor=PANEL_2,
    highlightthickness=0,
    showvalue=True,
    width=12,
    length=120
)

speed_scale.grid(
    row=1,
    column=8,
    padx=(8, 15),
    pady=(0, 12)
)


# ============================================================
# MAIN CONTENT
# ============================================================

main_frame = tk.Frame(
    root,
    bg=BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(5, 20)
)


# ============================================================
# LEFT SIDE
# ============================================================

left_frame = tk.Frame(
    main_frame,
    bg=BG
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


# Visualization header

visual_header = tk.Frame(
    left_frame,
    bg=BG
)

visual_header.pack(
    fill="x",
    pady=(0, 6)
)


tk.Label(
    visual_header,
    text="VISUALIZATION",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(
    side="left"
)


tk.Label(
    visual_header,
    textvariable=size_var,
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(
    side="right"
)


# Canvas

canvas_frame = tk.Frame(
    left_frame,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

canvas_frame.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    canvas_frame,
    bg=PANEL,
    highlightthickness=0
)

canvas.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


# Operation panel

operation_frame = tk.Frame(
    left_frame,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

operation_frame.pack(
    fill="x",
    pady=(10, 0)
)


tk.Label(
    operation_frame,
    text="CURRENT OPERATION",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8, "bold")
).pack(
    anchor="w",
    padx=14,
    pady=(10, 2)
)


tk.Label(
    operation_frame,
    textvariable=operation_var,
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    padx=14,
    pady=(0, 10)
)


# ============================================================
# METRICS
# ============================================================

metrics_frame = tk.Frame(
    left_frame,
    bg=BG
)

metrics_frame.pack(
    fill="x",
    pady=(10, 0)
)


def create_metric(parent, title, variable):

    frame = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 6)
    )

    tk.Label(
        frame,
        text=title,
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        pady=(9, 2)
    )

    tk.Label(
        frame,
        textvariable=variable,
        bg=PANEL,
        fg=TEXT,
        font=("Segoe UI", 17, "bold")
    ).pack(
        pady=(0, 9)
    )


create_metric(
    metrics_frame,
    "COMPARISONS",
    comparison_var
)

create_metric(
    metrics_frame,
    "SWAPS",
    swap_var
)

create_metric(
    metrics_frame,
    "OPERATIONS",
    operation_var
)


# ============================================================
# RIGHT SIDE
# ============================================================

right_frame = tk.Frame(
    main_frame,
    bg=BG,
    width=315
)

right_frame.pack(
    side="right",
    fill="y",
    padx=(10, 0)
)

right_frame.pack_propagate(False)


# ============================================================
# COMPLEXITY PANEL
# ============================================================

complexity_frame = tk.Frame(
    right_frame,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

complexity_frame.pack(
    fill="x",
    pady=(0, 10)
)


tk.Label(
    complexity_frame,
    text="COMPLEXITY ANALYSIS",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(
    anchor="w",
    padx=14,
    pady=(12, 10)
)


complexity_rows = [
    ("Best Case", best_var),
    ("Average Case", average_var),
    ("Worst Case", worst_var),
    ("Space", space_var)
]


for label_text, variable in complexity_rows:

    row = tk.Frame(
        complexity_frame,
        bg=PANEL
    )

    row.pack(
        fill="x",
        padx=14,
        pady=4
    )

    tk.Label(
        row,
        text=label_text,
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(
        side="left"
    )

    tk.Label(
        row,
        textvariable=variable,
        bg=PANEL,
        fg=ACCENT,
        font=("Segoe UI", 9, "bold")
    ).pack(
        side="right"
    )


# ============================================================
# LIVE CODE PANEL
# ============================================================

code_frame = tk.Frame(
    right_frame,
    bg=PANEL_2,
    highlightbackground=BORDER,
    highlightthickness=1
)

code_frame.pack(
    fill="both",
    expand=True
)


code_header = tk.Frame(
    code_frame,
    bg=PANEL_2
)

code_header.pack(
    fill="x"
)


tk.Label(
    code_header,
    text="ALGORITHM LOGIC",
    bg=PANEL_2,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(
    side="left",
    padx=14,
    pady=12
)


tk.Label(
    code_header,
    text="LIVE",
    bg=PANEL_2,
    fg=GREEN,
    font=("Segoe UI", 8, "bold")
).pack(
    side="right",
    padx=14
)


code_inner = tk.Frame(
    code_frame,
    bg=PANEL_2
)

code_inner.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


# ============================================================
# INITIAL SETUP
# ============================================================

update_complexity()

draw_bars()

update_buttons()


# ============================================================
# RUN APPLICATION
# ============================================================

root.mainloop()