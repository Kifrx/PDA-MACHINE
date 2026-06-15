import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


def simulate_pda(input_string):
    stack = ["Z0"]

    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    opening = "([{"
    closing = ")]}"

    trace = []

    push_count = 0
    pop_count = 0
    max_depth = 1

    trace.append(
        f"{'Step':<5}{'Read':<8}{'Action':<20}{'Stack'}"
    )
    trace.append("-" * 60)

    step = 0

    for symbol in input_string:
        step += 1

        if symbol in opening:

            stack.append(symbol)
            push_count += 1

            max_depth = max(
                max_depth,
                len(stack)
            )

            trace.append(
                f"{step:<5}{symbol:<8}{'PUSH ' + symbol:<20}{str(stack)}"
            )

        elif symbol in closing:

            if len(stack) > 1 and stack[-1] == pairs[symbol]:

                stack.pop()
                pop_count += 1

                trace.append(
                    f"{step:<5}{symbol:<8}{'POP ' + pairs[symbol]:<20}{str(stack)}"
                )

            else:

                trace.append(
                    f"{step:<5}{symbol:<8}{'ERROR':<20}{str(stack)}"
                )

                stats = {
                    "push": push_count,
                    "pop": pop_count,
                    "max_depth": max_depth,
                    "final_depth": len(stack) - 1
                }

                return False, trace, stats

        else:

            trace.append(
                f"{step:<5}{symbol:<8}{'INVALID SYMBOL':<20}{str(stack)}"
            )

            stats = {
                "push": push_count,
                "pop": pop_count,
                "max_depth": max_depth,
                "final_depth": len(stack) - 1
            }

            return False, trace, stats

    accepted = (stack == ["Z0"])

    stats = {
        "push": push_count,
        "pop": pop_count,
        "max_depth": max_depth,
        "final_depth": len(stack) - 1
    }

    return accepted, trace, stats


def run_single():
    output_box.delete(1.0, tk.END)

    user_input = entry_string.get().strip()

    if not user_input:
        messagebox.showwarning(
            "Warning",
            "Masukkan string terlebih dahulu!"
        )
        return

    accepted, trace, stats = simulate_pda(user_input)

    for line in trace:
        output_box.insert(
            tk.END,
            line + "\n"
        )

    output_box.insert(
        tk.END,
        "\n" + "=" * 50 + "\n"
    )

    output_box.insert(
        tk.END,
        "STATISTICS\n"
    )

    output_box.insert(
        tk.END,
        "=" * 50 + "\n"
    )

    output_box.insert(
        tk.END,
        f"Input Length : {len(user_input)}\n"
    )

    output_box.insert(
        tk.END,
        f"Total Push   : {stats['push']}\n"
    )

    output_box.insert(
        tk.END,
        f"Total Pop    : {stats['pop']}\n"
    )

    output_box.insert(
        tk.END,
        f"Max Depth    : {stats['max_depth']}\n"
    )

    output_box.insert(
        tk.END,
        f"Final Depth  : {stats['final_depth']}\n"
    )

    output_box.insert(
        tk.END,
        f"\nRESULT : {'ACCEPT' if accepted else 'REJECT'}\n"
    )


def run_multi():
    output_box.delete(1.0, tk.END)

    data = multi_box.get(
        "1.0",
        tk.END
    ).strip()

    if not data:
        messagebox.showwarning(
            "Warning",
            "Masukkan minimal satu string!"
        )
        return

    strings = data.splitlines()

    output_box.insert(
        tk.END,
        f"{'No':<5}{'String':<25}{'Result'}\n"
    )

    output_box.insert(
        tk.END,
        "-" * 45 + "\n"
    )

    for i, s in enumerate(strings, start=1):

        accepted, _, _ = simulate_pda(s.strip())

        result = (
            "ACCEPT"
            if accepted
            else "REJECT"
        )

        output_box.insert(
            tk.END,
            f"{i:<5}{s:<25}{result}\n"
        )



# GUI

root = tk.Tk()
root.title("PDA Simulator")
root.geometry("900x650")

title = ttk.Label(
    root,
    text="Pushdown Automata Simulator",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

# Single Test

single_frame = ttk.LabelFrame(
    root,
    text="Single String Testing"
)
single_frame.pack(
    fill="x",
    padx=10,
    pady=5
)

entry_string = ttk.Entry(
    single_frame,
    width=60
)
entry_string.pack(
    side="left",
    padx=10,
    pady=10
)

run_button = ttk.Button(
    single_frame,
    text="Run PDA",
    command=run_single
)
run_button.pack(
    side="left",
    padx=5
)

# Multi Test

multi_frame = ttk.LabelFrame(
    root,
    text="Multi String Testing (1 string per line)"
)
multi_frame.pack(
    fill="x",
    padx=10,
    pady=5
)

multi_box = tk.Text(
    multi_frame,
    height=5
)
multi_box.pack(
    fill="x",
    padx=10,
    pady=10
)

multi_button = ttk.Button(
    multi_frame,
    text="Run Multi Test",
    command=run_multi
)
multi_button.pack(
    pady=5
)

# Output

output_frame = ttk.LabelFrame(
    root,
    text="Output"
)
output_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

output_box = scrolledtext.ScrolledText(
    output_frame
)
output_box.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)

root.mainloop()
