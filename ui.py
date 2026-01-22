from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import sys

root = Tk()
root.withdraw()

def show_loading(message="Generating plan..."):
    window = Toplevel()
    window.title("Please wait")
    window.geometry("300x100")
    window.resizable(False, False)

    label = Label(window, text=message, padx=20, pady=20)
    label.pack(expand=True)

    window.update()
    return window


def show_plan_and_confirm(plan_text):
    result = {"choice": None}

    window = Toplevel()
    window.title("Confirm Organization Plan")
    window.geometry("550x420")

    frame = Frame(window)
    frame.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    text.insert(END, plan_text)
    text.config(state="disabled")
    text.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=text.yview)

    def apply():
        result["choice"] = "apply"
        window.destroy()

    def refine():
        result["choice"] = "refine"
        window.destroy()

    def cancel():
        result["choice"] = "cancel"
        window.destroy()

    btn_frame = Frame(window)
    btn_frame.pack(pady=10)

    Button(btn_frame, text="Apply", width=12, command=apply).pack(side=LEFT, padx=10)
    Button(btn_frame, text="Refine", width=12, command=refine).pack(side=LEFT, padx=10)
    Button(btn_frame, text="Cancel", width=12, command=cancel).pack(side=LEFT, padx=10)

    window.wait_window()

    return result["choice"]


def select_folder():
    root = Tk()
    root.withdraw()  # Hide main window
    folder_path = filedialog.askdirectory(title="Select folder to organize")
    return folder_path


def ask_user_input(title, prompt):
    result = {"text": None}

    window = Toplevel()
    window.title(title)
    window.geometry("500x350")

    Label(window, text=prompt, wraplength=480, justify="left").pack(pady=10)

    text = Text(window, height=10, wrap="word")
    text.pack(fill=BOTH, expand=True, padx=10)

    def submit():
        result["text"] = text.get("1.0", END).strip()
        window.destroy()

    def cancel():
        window.destroy()

    btn_frame = Frame(window)
    btn_frame.pack(pady=10)

    Button(btn_frame, text="OK", width=10, command=submit).pack(side=LEFT, padx=10)
    Button(btn_frame, text="Cancel", width=10, command=cancel).pack(side=LEFT)

    window.wait_window()
    return result["text"]

def ask_yes_no(title, message):
    root = Tk()
    root.withdraw()
    return messagebox.askyesno(title, message)

def show_info(title, message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo(title, message)

def fatal_error(message):
    messagebox.showerror("Fatal Error", message)
    sys.exit(1)