import tkinter as tk
from tkinter import ttk, messagebox
import sympy

def generate_n_digit_prime(n):
    """Generate an n-digit prime number."""
    if n >= 25:
        raise ValueError("n must be less than 25 for random generation.")
    return sympy.randprime(10**(n-1), 10**n)

def nearest_prime(num):
    """Return the nearest prime to num. If tie, pick the smaller prime."""
    if sympy.isprime(num):
        return num

    offset = 1
    while True:
        lower = num - offset
        upper = num + offset
        # Check lower first if it's >= 2
        if lower >= 2 and sympy.isprime(lower):
            return lower
        # Then check upper
        if sympy.isprime(upper):
            return upper
        offset += 1

def find_prime_pairs(p):
    """Find the first pair of distinct primes that average to p."""
    pairs = []
    for prime1 in sympy.primerange(2, 2*p):
        prime2 = 2*p - prime1
        if prime2 > prime1 and sympy.isprime(prime2):
            pairs.append((prime1, prime2))
            break
    return pairs

class PrimeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mean Relations Among Primes")
        self.master.geometry("640x480")  # Set a default window size

        # --------------------------
        #      Style Configuration
        # --------------------------
        style = ttk.Style()
        style.theme_use("clam")

        # Customize colors for frames, labels, and buttons
        style.configure("MainFrame.TFrame", background="#E6F2FF")
        style.configure("InputFrame.TFrame", background="#E6F2FF")
        style.configure("OutputFrame.TFrame", background="#E6F2FF")

        style.configure("TLabel", background="#E6F2FF", font=("Helvetica", 11))
        style.configure("TButton",
                        font=("Helvetica", 10, "bold"),
                        foreground="#333333",
                        padding=6)

        # --------------------------
        #          Main Frame
        # --------------------------
        self.main_frame = ttk.Frame(self.master, style="MainFrame.TFrame", padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --------------------------
        #       Mode Selection
        # --------------------------
        mode_frame = ttk.Frame(self.main_frame, style="InputFrame.TFrame", padding="10")
        mode_frame.pack(fill=tk.X, padx=5, pady=5)

        self.mode_var = tk.StringVar(value="random")
        self.radio_random = ttk.Radiobutton(mode_frame, text="Generate Random Prime",
                                            variable=self.mode_var, value="random",
                                            command=self.toggle_input_fields)
        self.radio_random.pack(side=tk.LEFT, padx=5)

        self.radio_user = ttk.Radiobutton(mode_frame, text="Use Provided Prime",
                                          variable=self.mode_var, value="user",
                                          command=self.toggle_input_fields)
        self.radio_user.pack(side=tk.LEFT, padx=5)

        # --------------------------
        #       Input Section
        # --------------------------
        self.input_frame = ttk.Frame(self.main_frame, style="InputFrame.TFrame", padding="10")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # 1) Entry for number of digits
        self.label_digits = ttk.Label(self.input_frame, text="Number of digits (n < 25):")
        self.label_digits.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.entry_digits = ttk.Entry(self.input_frame, width=10)
        self.entry_digits.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        # 2) Entry for user-provided prime
        self.label_user_prime = ttk.Label(self.input_frame, text="Enter a prime number:")
        self.label_user_prime.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.entry_user_prime = ttk.Entry(self.input_frame, width=15)
        self.entry_user_prime.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        # The button to process input
        self.process_button = ttk.Button(self.input_frame, text="Compute", command=self.process_input)
        self.process_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --------------------------
        #       Output Section
        # --------------------------
        self.output_frame = ttk.Frame(self.main_frame, style="OutputFrame.TFrame", padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_label = ttk.Label(self.output_frame, text="Results:")
        self.output_label.pack(anchor=tk.W, padx=5, pady=(0, 5))

        self.output_text = tk.Text(self.output_frame,
                                   wrap="word",
                                   width=60,
                                   height=14,
                                   bg="#FFFFFF",
                                   fg="#333333",
                                   font=("Helvetica", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Initialize fields
        self.toggle_input_fields()

    def toggle_input_fields(self):
        """Enable or disable entry widgets based on the selected mode."""
        mode = self.mode_var.get()
        if mode == "random":
            self.entry_digits.config(state="normal")
            self.entry_user_prime.config(state="disabled")
        else:  # user-provided prime
            self.entry_digits.config(state="disabled")
            self.entry_user_prime.config(state="normal")

    def process_input(self):
        """Handle both modes: random prime generation or user-provided prime."""
        # Clear output
        self.output_text.delete("1.0", tk.END)

        mode = self.mode_var.get()
        if mode == "random":
            self.handle_random_prime_generation()
        else:
            self.handle_user_prime()

    def handle_random_prime_generation(self):
        """Generate a random prime given the user-specified number of digits."""
        try:
            n = int(self.entry_digits.get())
            if n < 1:
                raise ValueError("Number of digits must be positive.")
            # Generate an n-digit prime
            p = generate_n_digit_prime(n)
            self.display_results(p, n)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_user_prime(self):
        """Check if user input is prime. If not, pick the nearest prime."""
        try:
            user_input = self.entry_user_prime.get().strip()
            if not user_input.isdigit():
                raise ValueError("Please enter a valid integer.")

            num = int(user_input)
            if num < 2:
                raise ValueError("Please enter an integer >= 2.")

            # Find the nearest prime if num is not prime
            p = nearest_prime(num)
            # Display results (we don't have a 'digit count' for user prime, so pass None)
            self.display_results(p, None)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_results(self, p, n):
        """Given a prime p, find the pair of primes whose average is p and display output."""
        if n is not None:
            self.output_text.insert(tk.END, f"Generated {n}-digit prime: {p}\n\n")
        else:
            self.output_text.insert(tk.END, f"Selected prime: {p}\n\n")

        # Find prime pairs that average to p
        pairs = find_prime_pairs(p)
        if pairs:
            p1, p2 = pairs[0]
            self.output_text.insert(tk.END,
                "Found a combination of distinct primes whose average equals the prime:\n\n")
            self.output_text.insert(tk.END, f"Pair: {p1} and {p2}\n\n")

            # Display the proof in the requested format
            self.output_text.insert(tk.END, "Proof:\n\n")
            self.output_text.insert(tk.END,
                f"Generated/Selected Prime times number of Discovered Primes: {p} x 2 = {2*p}\n")
            self.output_text.insert(tk.END,
                f"Sum of Discovered Primes: {p1} + {p2} = {p1 + p2}\n\n")

            # Use Unicode subscript characters for p1, p2
            self.output_text.insert(tk.END,
                "This matches the expected relation: p\u2081 + p\u2082 = n \u00D7 p,\n"
                "where p\u2081, p\u2082, ..., p\u2099 are discovered primes and p is the generated/selected prime, "
                "and n is the number of discovered primes.\n\n")
        else:
            self.output_text.insert(tk.END, "No prime pairs found.\n")


if __name__ == "__main__":
    root = tk.Tk()
    gui = PrimeGUI(root)
    root.mainloop()
