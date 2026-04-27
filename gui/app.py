import sys
from core.timer import ShutdownTimer
from core.platform import PLATFORM
from utils.history import load_history

DARK = "#0D0D0D"
PANEL = "#161616"
CARD = "#1E1E1E"
BORDER = "#2A2A2A"
ACCENT = "#00E5A0"
WARN = "#FF6B35"
TEXT = "#F0F0F0"
MUTED = "#6B6B6B"
FONT_MONO = ("Courier New", 10)


def run_gui():
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        print("ERROR: Tkinter not available. Run with --cli flag.")
        sys.exit(1)

    root = tk.Tk()
    root.title("Shutdown Timer Pro")
    root.geometry("520x640")
    root.resizable(False, False)
    root.configure(bg=DARK)

    timer_ref = [None]

    hours_var = tk.StringVar(value="0")
    minutes_var = tk.StringVar(value="60")
    seconds_var = tk.StringVar(value="0")
    action_var = tk.StringVar(value="shutdown")
    status_var = tk.StringVar(value="READY")
    countdown_var = tk.StringVar(value="00:00:00")
    progress_var = tk.DoubleVar(value=0.0)

    def make_card(parent, title):
        outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        outer.pack(fill="x", padx=20, pady=(0, 12))
        inner = tk.Frame(outer, bg=CARD, padx=16, pady=12)
        inner.pack(fill="both")
        tk.Label(inner, text=title, font=("Courier New", 9),
                 fg=MUTED, bg=CARD).pack(anchor="w")
        return inner

    header = tk.Frame(root, bg=DARK, pady=24)
    header.pack(fill="x")
    tk.Label(header, text="SHUTDOWN TIMER", font=("Courier New", 18, "bold"), fg=ACCENT, bg=DARK).pack()
    tk.Label(header, text=f"v2.0  ·  {PLATFORM.upper()}", font=FONT_MONO, fg=MUTED, bg=DARK).pack()

    time_card = make_card(root, "SET DURATION")
    time_row  = tk.Frame(time_card, bg=CARD)
    time_row.pack(fill="x", pady=(8, 0))

    entry_style = dict(
        font=("Courier New", 26, "bold"), fg=TEXT, bg=PANEL,
        width=3, justify="center", relief="flat", bd=0,
        insertbackground=ACCENT,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
    )

    for var, label, col in [
        (hours_var, "HH", 0),
        (minutes_var, "MM", 2),
        (seconds_var, "SS", 4),
    ]:
        tk.Entry(time_row, textvariable=var, **entry_style).grid(row=0, column=col, padx=4)
        tk.Label(time_row, text=label, font=("Courier New", 9),
                 fg=MUTED, bg=CARD).grid(row=1, column=col, pady=(2, 0))
        if col < 4:
            tk.Label(time_row, text=":", font=("Courier New", 26, "bold"),
                     fg=MUTED, bg=CARD).grid(row=0, column=col + 1)

    presets_row = tk.Frame(time_card, bg=CARD)
    presets_row.pack(fill="x", pady=(12, 0))
    tk.Label(presets_row, text="PRESETS:", font=("Courier New", 9),
             fg=MUTED, bg=CARD).pack(side="left", padx=(0, 8))

    def set_preset(m):
        hours_var.set("0")
        minutes_var.set(str(m))
        seconds_var.set("0")

    for mins in [15, 30, 60, 90, 120]:
        tk.Button(
            presets_row, text=f"{mins}m",
            font=("Courier New", 9), fg=MUTED, bg=PANEL,
            relief="flat", bd=0, padx=8, pady=2, cursor="hand2",
            activeforeground=ACCENT, activebackground=PANEL,
            command=lambda m=mins: set_preset(m),
        ).pack(side="left", padx=2)

    action_card = make_card(root, "ACTION")
    action_row  = tk.Frame(action_card, bg=CARD)
    action_row.pack(fill="x", pady=(8, 0))

    for val, lbl in [
        ("shutdown",  "⏻ Shutdown"),
        ("restart",   "↺ Restart"),
        ("sleep",     "☽ Sleep"),
        ("hibernate", "❄ Hibernate"),
    ]:
        tk.Radiobutton(
            action_row, text=lbl, variable=action_var, value=val,
            font=("Courier New", 10), fg=TEXT, bg=CARD,
            selectcolor=PANEL, activeforeground=ACCENT,
            activebackground=CARD, relief="flat", cursor="hand2",
        ).pack(side="left", padx=(0, 16))

    prog_card = make_card(root, "PROGRESS")
    tk.Label(prog_card, textvariable=countdown_var,
             font=("Courier New", 36, "bold"), fg=ACCENT, bg=CARD).pack(pady=(8, 4))
    tk.Label(prog_card, textvariable=status_var,
             font=("Courier New", 10), fg=MUTED, bg=CARD).pack(pady=(0, 8))

    prog_canvas = tk.Canvas(prog_card, height=6, bg=PANEL, highlightthickness=0)
    prog_canvas.pack(fill="x", pady=(0, 4))

    def draw_progress(pct):
        prog_canvas.delete("bar")
        w = prog_canvas.winfo_width()
        if w < 2:
            return
        fill_w = int(w * pct)
        color = ACCENT if pct < 0.75 else (WARN if pct < 0.9 else "#FF2D55")
        if fill_w > 0:
            prog_canvas.create_rectangle(0, 0, fill_w, 6,
                                         fill=color, outline="", tags="bar")

    btn_frame = tk.Frame(root, bg=DARK)
    btn_frame.pack(fill="x", padx=20, pady=12)

    btn_cfg = dict(
        font=("Courier New", 11, "bold"),
        relief="flat", bd=0, padx=20, pady=10,
        cursor="hand2", width=10,
    )

    start_btn = tk.Button(
        btn_frame, text="▶  START",
        fg=DARK, bg=ACCENT,
        activeforeground=DARK, activebackground="#00CC8E",
        **btn_cfg,
    )
    cancel_btn = tk.Button(
        btn_frame, text="✕  CANCEL",
        fg=WARN, bg=PANEL,
        activeforeground=WARN, activebackground=CARD,
        state="disabled",
        **btn_cfg,
    )
    start_btn.pack(side="left", padx=(0, 8))
    cancel_btn.pack(side="left")

    hist_card = make_card(root, "RECENT HISTORY")
    hist_text = tk.Text(
        hist_card, height=5, font=("Courier New", 9),
        fg=MUTED, bg=CARD, relief="flat", bd=0, state="disabled",
    )
    hist_text.pack(fill="x", pady=(6, 0))

    def refresh_history():
        hist_text.config(state="normal")
        hist_text.delete("1.0", "end")
        for h in reversed(load_history()[-5:]):
            status = "✓" if h.get("completed") else "✗"
            mins = h["duration_seconds"] // 60
            ts   = h["started_at"][:16] if h.get("started_at") else "—"
            hist_text.insert("end", f"  {status}  {ts}  {mins}min  {h['action']}\n")
        hist_text.config(state="disabled")

    refresh_history()

    total_ref = [0]

    def on_tick(remaining):
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        countdown_var.set(f"{h:02d}:{m:02d}:{s:02d}")
        elapsed = total_ref[0] - remaining
        pct = elapsed / total_ref[0] if total_ref[0] > 0 else 0
        progress_var.set(pct)
        root.after(0, draw_progress, pct)
        status_var.set(f"RUNNING  —  {int(pct * 100)}% elapsed")

    def on_done():
        root.after(0, lambda: [
            status_var.set("EXECUTING ACTION..."),
            start_btn.config(state="normal"),
            cancel_btn.config(state="disabled"),
            refresh_history(),
        ])

    def on_cancel():
        root.after(0, lambda: [
            status_var.set("CANCELLED"),
            countdown_var.set("00:00:00"),
            draw_progress(0),
            start_btn.config(state="normal"),
            cancel_btn.config(state="disabled"),
            refresh_history(),
        ])

    def start_timer():
        try:
            h = int(hours_var.get() or 0)
            m = int(minutes_var.get() or 0)
            s = int(seconds_var.get() or 0)
            total = h * 3600 + m * 60 + s
            if total <= 0:
                messagebox.showerror("Invalid", "Please enter a duration > 0.")
                return
        except ValueError:
            messagebox.showerror("Invalid", "Hours/Minutes/Seconds must be numbers.")
            return

        total_ref[0] = total
        t = ShutdownTimer(
            seconds=total,
            action=action_var.get(),
            on_tick=on_tick,
            on_done=on_done,
            on_cancel=on_cancel,
        )
        timer_ref[0] = t
        t.start()
        start_btn.config(state="disabled")
        cancel_btn.config(state="normal")
        status_var.set("RUNNING...")

    def cancel_timer():
        if timer_ref[0]:
            timer_ref[0].cancel()

    start_btn.config(command=start_timer)
    cancel_btn.config(command=cancel_timer)

    def on_close():
        if timer_ref[0] and not timer_ref[0].cancelled:
            if messagebox.askyesno("Timer Running",
                                   "A timer is active. Cancel it and exit?"):
                timer_ref[0].cancel()
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    prog_canvas.bind("<Configure>", lambda e: draw_progress(progress_var.get()))
    root.mainloop()