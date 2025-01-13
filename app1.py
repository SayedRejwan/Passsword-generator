import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Web Password Generator")
        self.root.configure(bg="#121212")  # Dark background
        self.password = ""
        self.password_history = []  # To store generated passwords

        # GUI Layout
        self.setup_gui()

    def setup_gui(self):
        # Title Label
        tk.Label(self.root, text="Dark Web Password Generator", font=("Helvetica", 16, "bold"), fg="#FF4500", bg="#121212").grid(row=0, column=0, columnspan=3, pady=10)

        # Length Input
        tk.Label(self.root, text="Password Length:", font=("Helvetica", 12), fg="#FFFFFF", bg="#121212").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.length_var = tk.IntVar(value=12)
        tk.Entry(self.root, textvariable=self.length_var, width=10, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Helvetica", 12)).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Checkboxes for Character Types
        self.include_lower = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.include_lower, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=2, column=0, sticky="w", padx=5)

        self.include_upper = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.include_upper, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=3, column=0, sticky="w", padx=5)

        self.include_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.include_digits, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=4, column=0, sticky="w", padx=5)

        self.include_special = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Special Characters", variable=self.include_special, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=5, column=0, sticky="w", padx=5)

        # Avoid Ambiguous Characters Checkbox
        self.avoid_ambiguous = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Avoid Ambiguous Characters", variable=self.avoid_ambiguous, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=6, column=0, sticky="w", padx=5)

        # Save Password to History Checkbox
        self.save_to_history = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Save to History", variable=self.save_to_history, fg="#FFFFFF", bg="#121212", selectcolor="#1E1E1E").grid(row=7, column=0, sticky="w", padx=5)

        # Buttons
        tk.Button(self.root, text="Generate Password", command=self.generate_password, font=("Helvetica", 12), bg="#FF4500", fg="#FFFFFF", activebackground="#FF6347", activeforeground="#FFFFFF").grid(row=8, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, font=("Helvetica", 12), bg="#FF4500", fg="#FFFFFF", activebackground="#FF6347", activeforeground="#FFFFFF").grid(row=9, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="View History", command=self.view_history, font=("Helvetica", 12), bg="#FF4500", fg="#FFFFFF", activebackground="#FF6347", activeforeground="#FFFFFF").grid(row=10, column=0, columnspan=3, pady=10)

        # Output Display
        self.password_display = tk.Entry(self.root, font=("Courier", 14), width=30, state="readonly", bg="#1E1E1E", fg="#000000", insertbackground="#FFFFFF")
        self.password_display.grid(row=11, column=0, columnspan=3, pady=10)

        # Strength Indicator
        self.strength_label = tk.Label(self.root, text="Strength: Unknown", font=("Helvetica", 12), fg="#FF0000", bg="#121212")
        self.strength_label.grid(row=12, column=0, columnspan=3, pady=5)

    def generate_password(self):
        try:
            length = self.length_var.get()
            if length < 8:
                raise ValueError("Password length should be at least 8 characters.")

            # Character Pools
            pools = ""
            if self.include_lower.get():
                pools += string.ascii_lowercase
            if self.include_upper.get():
                pools += string.ascii_uppercase
            if self.include_digits.get():
                pools += string.digits
            if self.include_special.get():
                pools += "!@#$%^&*()_+-=[]{}|;:,.<>?/"

            if self.avoid_ambiguous.get():
                pools = pools.translate(str.maketrans('', '', 'O0Il1'))

            if not pools:
                raise ValueError("At least one character type must be selected.")

            # Generate Password
            self.password = ''.join(random.choices(pools, k=length))

            # Display Password
            self.password_display.config(state="normal")
            self.password_display.delete(0, tk.END)
            self.password_display.insert(0, self.password)
            self.password_display.config(state="readonly")

            # Save to History
            if self.save_to_history.get():
                self.password_history.append(self.password)

            # Update Strength Indicator
            self.update_strength_indicator()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_strength_indicator(self):
        length = len(self.password)
        pools_count = sum([self.include_lower.get(), self.include_upper.get(), self.include_digits.get(), self.include_special.get()])

        if length >= 12 and pools_count >= 3:
            strength = "Strong"
        elif length >= 8 and pools_count >= 2:
            strength = "Medium"
        else:
            strength = "Weak"

        self.strength_label.config(text=f"Strength: {strength}")

    def copy_to_clipboard(self):
        if self.password:
            pyperclip.copy(self.password)
            messagebox.showinfo("Copied", f"Password copied to clipboard and saved in history!\nPassword: {self.password}")
            if self.password not in self.password_history:
                self.password_history.append(self.password)
        else:
            messagebox.showerror("Error", "No password to copy.")

    def view_history(self):
        if not self.password_history:
            messagebox.showinfo("History", "No passwords generated yet.")
        else:
            history_window = tk.Toplevel(self.root)
            history_window.title("Password History")
            history_window.configure(bg="#121212")
            tk.Label(history_window, text="Generated Passwords:", font=("Helvetica", 14), fg="#FFFFFF", bg="#121212").pack(pady=10)

            history_text = tk.Text(history_window, font=("Courier", 12), width=40, height=10, bg="#1E1E1E", fg="#000000", insertbackground="#FFFFFF")
            history_text.pack(padx=10, pady=10)
            history_text.insert(tk.END, '\n'.join(self.password_history))
            history_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
