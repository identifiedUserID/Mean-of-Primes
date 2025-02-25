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
        master.title("Mean Relations Among Primes")

        # Create a frame for input
        input_frame = ttk.Frame(master, padding="10")
        input_frame.grid(row=0, column=0, sticky="W")

        # Label and Entry for number of digits
        self.label = ttk.Label(input_frame, text="Enter number of digits (n < 25):")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.entry = ttk.Entry(input_frame, width=10)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # Button to generate prime and find pairs
        self.generate_button = ttk.Button(input_frame, text="Generate Prime", command=self.generate_prime)
        self.generate_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Text widget to display output
        self.output_text = tk.Text(master, wrap="word", width=60, height=15, padx=10, pady=10)
        self.output_text.grid(row=1, column=0)

    def generate_prime(self):
        # Clear the output area
        self.output_text.delete("1.0", tk.END)
        try:
            n = int(self.entry.get())
            if n < 1:
                raise ValueError("Number of digits must be positive.")
            # Generate an n-digit prime number
            p = generate_n_digit_prime(n)
            self.output_text.insert(tk.END, f"Generated {n}-digit prime: {p}\n\n")

            # Find prime pairs that average to p
            pairs = find_prime_pairs(p)
            if pairs:
                self.output_text.insert(tk.END,
                                        "Found pairs of distinct primes whose average equals the generated prime:\n")
                for (p1, p2) in pairs:
                    self.output_text.insert(tk.END, f"{p1} and {p2}\n")
            else:
                self.output_text.insert(tk.END, "No prime pairs found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    gui = PrimeGUI(root)
    root.mainloop()
