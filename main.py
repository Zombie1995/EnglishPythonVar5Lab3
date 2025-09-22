import random
import string
import tkinter as tk
from tkinter import messagebox

# Character tape: A-Z then 0-9
TAPE = string.ascii_uppercase + "0123456789"
TAPE_LEN = len(TAPE)

SHIFT_BLOCK2 = 3   # Right shift
SHIFT_BLOCK3 = -5  # Left shift


def shift_char(c: str, offset: int) -> str:
    idx = TAPE.index(c)
    return TAPE[(idx + offset) % TAPE_LEN]


def generate_from_block1(block1: str) -> str:
    block2 = ''.join(shift_char(c, SHIFT_BLOCK2) for c in block1)
    block3 = ''.join(shift_char(c, SHIFT_BLOCK3) for c in block1)
    return f"{block1}-{block2}-{block3}"


def random_block(length: int = 5) -> str:
    return ''.join(random.choice(TAPE) for _ in range(length))


def main():
    root = tk.Tk()
    root.title("Game Key Generator")
    root.resizable(False, False)

    # Try to load background image (place a PNG named background.png in the same directory)
    bg_label = None
    try:
        bg_image = tk.PhotoImage(file="background.png")
        bg_label = tk.Label(root, image=bg_image)
        bg_label.image = bg_image  # keep reference
        bg_label.pack(fill="both", expand=True)
    except Exception:
        # Fallback solid color
        root.configure(bg="#1e1e1e")

    overlay = tk.Frame(root, bg="#000000", bd=0, highlightthickness=0)
    overlay.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(overlay, text="Key Generator", font=("Segoe UI", 18, "bold"), fg="#ffffff", bg="#000000")
    title.grid(row=0, column=0, columnspan=4, pady=(10, 15))

    # Block1 input
    tk.Label(overlay, text="Enter Block 1 (5 chars A-Z0-9):", fg="#dddddd", bg="#000000", font=("Segoe UI", 10)).grid(row=1, column=0, columnspan=4, sticky="w", padx=12)

    block1_var = tk.StringVar()

    def on_block1_change(*_):
        value = block1_var.get().upper()
        # Filter invalid chars
        filtered = ''.join(ch for ch in value if ch in TAPE)
        if len(filtered) > 5:
            filtered = filtered[:5]
        if filtered != value:
            block1_var.set(filtered)

    block1_var.trace_add('write', on_block1_change)

    entry_block1 = tk.Entry(overlay, textvariable=block1_var, font=("Consolas", 14), width=8, justify='center')
    entry_block1.grid(row=2, column=0, padx=12, pady=5, sticky='w')

    def set_random_block1():
        block1_var.set(random_block())

    tk.Button(overlay, text="Random", command=set_random_block1, bg="#333333", fg="#ffffff", activebackground="#555555").grid(row=2, column=1, padx=(0, 12), pady=5)

    # Generated key output
    tk.Label(overlay, text="Generated Key:", fg="#dddddd", bg="#000000", font=("Segoe UI", 10)).grid(row=3, column=0, columnspan=4, sticky="w", padx=12, pady=(10, 0))
    key_var = tk.StringVar()
    entry_key = tk.Entry(overlay, textvariable=key_var, font=("Consolas", 16), width=20, justify='center', state='readonly')
    entry_key.grid(row=4, column=0, columnspan=3, padx=12, pady=5)

    def copy_key():
        k = key_var.get()
        if not k:
            return
        root.clipboard_clear()
        root.clipboard_append(k)
        messagebox.showinfo("Copied", "Key copied to clipboard.")

    tk.Button(overlay, text="Copy", command=copy_key, bg="#333333", fg="#ffffff", activebackground="#555555").grid(row=4, column=3, padx=(0, 12), pady=5)

    def generate_key():
        b1 = block1_var.get().upper()
        if len(b1) != 5:
            messagebox.showerror("Error", "Block 1 must be exactly 5 valid characters.")
            return
        try:
            key = generate_from_block1(b1)
        except ValueError:
            messagebox.showerror("Error", "Invalid characters in Block 1.")
            return
        key_var.set(key)

    btn_generate = tk.Button(overlay, text="Generate Key", command=generate_key, font=("Segoe UI", 11, "bold"), bg="#0078d4", fg="#ffffff", activebackground="#0a84ff", padx=10, pady=6)
    btn_generate.grid(row=5, column=0, columnspan=4, pady=(15, 15))

    # Minimum window size if no image
    if not bg_label:
        root.geometry("480x300")
    else:
        # Resize overlay relative to image size
        w = bg_label.image.width()
        h = bg_label.image.height()
        overlay.configure(padx=20, pady=10)
        root.geometry(f"{w}x{h}")

    root.mainloop()


if __name__ == "__main__":
    main()