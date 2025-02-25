import tkinter as tk
from tkinter import ttk, messagebox
import sympy


def generate_n_digit_prime(n):
    """Generate an n-digit prime number."""
    if n >= 25:
        raise ValueError("n must be less than 25")
    return sympy.randprime(10 ** (n - 1), 10 ** n)


def find_prime_pairs(p):
    """Find the first pair of distinct primes that average to p."""
    pairs = []
    for prime1 in sympy.primerange(2, 2 * p):
        prime2 = 2 * p - prime1
        if prime2 > prime1 and sympy.isprime(prime2):
            pairs.append((prime1, prime2))
            break
    return pairs


class PrimeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mean Relations Among Primes")
        self.master.geometry("600x400")  # Set a default window size

        # --------------------------
        #      Style Configuration
        # --------------------------
        style = ttk.Style()
        style.theme_use("clam")

        # Customize colors for frames, labels, and buttons
        style.configure("MainFrame.TFrame", background="#E6F2FF")  # Light bluish background
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
        #       Input Section
        # --------------------------
        self.input_frame = ttk.Frame(self.main_frame, style="InputFrame.TFrame", padding="10")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.label = ttk.Label(self.input_frame, text="Enter number of digits (n < 25):")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = ttk.Entry(self.input_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.generate_button = ttk.Button(self.input_frame, text="Generate Prime", command=self.generate_prime)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        # --------------------------
        #       Output Section
        # --------------------------
        self.output_frame = ttk.Frame(self.main_frame, style="OutputFrame.TFrame", padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        # Label for the output area
        self.output_label = ttk.Label(self.output_frame, text="Results:")
        self.output_label.pack(anchor=tk.W, padx=5, pady=(0, 5))

        # Text widget for displaying results
        self.output_text = tk.Text(self.output_frame,
                                   wrap="word",
                                   width=60,
                                   height=12,
                                   bg="#FFFFFF",
                                   fg="#333333",
                                   font=("Helvetica", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def generate_prime(self):
        """Generates an n-digit prime and finds pairs whose average is that prime."""
        # Clear the output area first
        self.output_text.delete("1.0", tk.END)

        try:
            n = int(self.entry.get())
            if n < 1:
                raise ValueError("Number of digits must be positive.")

            # Generate an n-digit prime number
            p = generate_n_digit_prime(n)

            # Display the generated prime
            self.output_text.insert(tk.END, f"Generated {n}-digit prime: {p}\n\n")

            # Find prime pairs that average to p
            pairs = find_prime_pairs(p)
            if pairs:
                # For this demo, we only display the first pair found
                p1, p2 = pairs[0]

                self.output_text.insert(tk.END,
                                        "Found a combination of distinct primes whose average equals the generated prime:\n\n")

                self.output_text.insert(tk.END, f"Pair: {p1} and {p2}\n\n")

                # Display the proof in your requested format
                self.output_text.insert(tk.END, "Proof:\n\n")
                self.output_text.insert(tk.END,
                                        f"Generated Prime times number of Discovered Primes: {p} x 2 = {2 * p}\n")
                self.output_text.insert(tk.END,
                                        f"Sum of Discovered Primes: {p1} + {p2} = {p1 + p2}\n\n")

                # Use Unicode subscript characters for p1, p2, ..., pₙ
                self.output_text.insert(tk.END,
                                        "This matches the expected relation: p\u2081 + p\u2082 = n \u00D7 p,\n"
                                        "where p\u2081, p\u2082, ..., p\u2099 are discovered primes and p is the generated prime, "
                                        "and n is the number of discovered primes.\n\n")
            else:
                self.output_text.insert(tk.END, "No prime pairs found.\n")

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    gui = PrimeGUI(root)
    root.mainloop()
