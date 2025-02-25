import tkinter as tk
from tkinter import ttk, messagebox
import sympy


### Core Functions ###

def generate_n_digit_prime(n):
    """Generate an n-digit prime number."""
    if n >= 25:
        raise ValueError("n must be less than 25 for random generation.")
    return sympy.randprime(10 ** (n - 1), 10 ** n)


def nearest_prime(num):
    """Return the nearest prime to num. If tie, pick the smaller prime."""
    if sympy.isprime(num):
        return num
    offset = 1
    while True:
        lower = num - offset
        upper = num + offset
        if lower >= 2 and sympy.isprime(lower):
            return lower
        if sympy.isprime(upper):
            return upper
        offset += 1


def find_prime_pairs(p):
    """Find a pair of distinct primes that average to p.
       That is, find p₁ and p₂ with p₁ + p₂ = 2*p."""
    for prime1 in sympy.primerange(2, 2 * p):
        prime2 = 2 * p - prime1
        if prime2 > prime1 and sympy.isprime(prime2):
            return [prime1, prime2]
    return []


def find_prime_combination(p, m):
    """
    Find a list of m (not necessarily distinct) primes that sum to m*p.
    That is, find primes p₁, p₂, ..., pₘ such that p₁+p₂+...+pₘ = m * p.
    This uses a simple backtracking search and allows repeated primes.
    """
    target = m * p
    # For candidate range, we generate all primes from 2 up to m*p.
    # (For small p and moderate m this works; for huge numbers this search may be expensive.)
    candidates = list(sympy.primerange(2, m * p + 1))
    candidates.sort()

    found = [None]  # will hold the first valid combination

    def backtrack(start_index, current_list, current_sum, count):
        if count == m:
            if current_sum == target:
                found[0] = list(current_list)
                return True
            return False

        # Pruning: if even the smallest possible sum from here exceeds target,
        # or the largest possible sum is less than target, abandon this branch.
        if candidates:
            min_possible = current_sum + (m - count) * candidates[0]
            max_possible = current_sum + (m - count) * candidates[-1]
            if min_possible > target or max_possible < target:
                return False

        for i in range(start_index, len(candidates)):
            candidate = candidates[i]
            if current_sum + candidate > target:
                # Because candidates are sorted, no later candidate will work.
                break
            current_list.append(candidate)
            # Allow repetition by not incrementing the index.
            if backtrack(i, current_list, current_sum + candidate, count + 1):
                return True
            current_list.pop()
        return False

    if backtrack(0, [], 0, 0):
        return found[0]
    return []


### GUI Class ###

class PrimeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mean Relations Among Primes")
        self.master.geometry("680x550")  # Adjust window size as needed

        # --------------------------
        #      Style Configuration
        # --------------------------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MainFrame.TFrame", background="#E6F2FF")
        style.configure("InputFrame.TFrame", background="#E6F2FF")
        style.configure("OutputFrame.TFrame", background="#E6F2FF")
        style.configure("TLabel", background="#E6F2FF", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="#333333", padding=6)

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
        self.radio_random = ttk.Radiobutton(
            mode_frame, text="Generate Random Prime",
            variable=self.mode_var, value="random",
            command=self.toggle_input_fields
        )
        self.radio_random.pack(side=tk.LEFT, padx=5)

        self.radio_user = ttk.Radiobutton(
            mode_frame, text="Use Provided Prime",
            variable=self.mode_var, value="user",
            command=self.toggle_input_fields
        )
        self.radio_user.pack(side=tk.LEFT, padx=5)

        # --------------------------
        #       Input Section
        # --------------------------
        self.input_frame = ttk.Frame(self.main_frame, style="InputFrame.TFrame", padding="10")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Row 0: For random prime: "Number of digits" field.
        self.label_digits = ttk.Label(self.input_frame, text="Number of digits (n < 25):")
        self.label_digits.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.entry_digits = ttk.Entry(self.input_frame, width=10)
        self.entry_digits.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        # Row 1: For provided prime: "Enter a prime number:" field.
        self.label_user_prime = ttk.Label(self.input_frame, text="Enter a prime number:")
        self.label_user_prime.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.entry_user_prime = ttk.Entry(self.input_frame, width=15)
        self.entry_user_prime.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        # Row 2: Custom discovered prime count checkbutton.
        self.custom_count_enabled = tk.BooleanVar(value=False)
        self.custom_count_check = ttk.Checkbutton(
            self.input_frame,
            text="Custom Number",
            variable=self.custom_count_enabled,
            command=self.toggle_custom_count
        )
        self.custom_count_check.grid(row=2, column=0, columnspan=2, pady=5, sticky="W")

        # Row 3: Custom discovered prime count entry (hidden by default).
        self.label_custom_count = ttk.Label(self.input_frame, text="Enter number of discovered primes ( > 2 ):")
        self.entry_custom_count = ttk.Entry(self.input_frame, width=10)
        # Hide initially
        self.label_custom_count.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.entry_custom_count.grid(row=3, column=1, padx=5, pady=5, sticky="W")
        self.label_custom_count.grid_remove()
        self.entry_custom_count.grid_remove()

        # Row 4: Process Button
        self.process_button = ttk.Button(self.input_frame, text="Compute", command=self.process_input)
        self.process_button.grid(row=4, column=0, columnspan=2, pady=10)

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
                                   height=20,
                                   bg="#FFFFFF",
                                   fg="#333333",
                                   font=("Helvetica", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Configure a text tag for bold text.
        self.output_text.tag_config("bold", font=("Helvetica", 10, "bold"))

        # Initialize the fields for the chosen mode.
        self.toggle_input_fields()

    def toggle_input_fields(self):
        """Show the appropriate input field (and hide the other) based on the selected mode."""
        mode = self.mode_var.get()
        if mode == "random":
            # Show digits row; hide provided prime row.
            self.label_digits.grid()
            self.entry_digits.grid()
            self.label_user_prime.grid_remove()
            self.entry_user_prime.grid_remove()
        else:
            # Hide digits row; show provided prime row.
            self.label_digits.grid_remove()
            self.entry_digits.grid_remove()
            self.label_user_prime.grid()
            self.entry_user_prime.grid()

    def toggle_custom_count(self):
        """Show or hide the custom discovered primes count entry."""
        if self.custom_count_enabled.get():
            self.label_custom_count.grid()
            self.entry_custom_count.grid()
        else:
            self.label_custom_count.grid_remove()
            self.entry_custom_count.grid_remove()

    def process_input(self):
        """Process input in the chosen mode and also get the desired discovered prime count."""
        self.output_text.delete("1.0", tk.END)
        # Determine discovered prime count.
        if self.custom_count_enabled.get():
            try:
                custom_count = int(self.entry_custom_count.get())
                if custom_count <= 2:
                    raise ValueError("Custom discovered prime count must be greater than 2.")
            except ValueError as ve:
                messagebox.showerror("Input Error", f"Custom count error: {ve}")
                return
        else:
            custom_count = 2  # default

        mode = self.mode_var.get()
        if mode == "random":
            self.handle_random_prime_generation(custom_count)
        else:
            self.handle_user_prime(custom_count)

    def handle_random_prime_generation(self, discovered_count):
        """Generate a random prime given the number of digits, then find discovered primes."""
        try:
            n = int(self.entry_digits.get())
            if n < 1:
                raise ValueError("Number of digits must be positive.")
            p = generate_n_digit_prime(n)
            self.display_results(p, n, discovered_count)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_user_prime(self, discovered_count):
        """Use a provided prime (or nearest prime if necessary) and then find discovered primes."""
        try:
            user_input = self.entry_user_prime.get().strip()
            if not user_input.isdigit():
                raise ValueError("Please enter a valid integer for the prime.")
            num = int(user_input)
            if num < 2:
                raise ValueError("Please enter an integer greater than or equal to 2.")
            p = nearest_prime(num)
            self.display_results(p, None, discovered_count)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_results(self, p, digit_count, discovered_count):
        """
        Given a prime p, find discovered primes (using discovered_count) such that their sum equals discovered_count * p.
        Then display the results and a proof.
        """
        # Format the prime using commas.
        p_formatted = format(p, ",")
        if digit_count is not None:
            self.output_text.insert(tk.END, f"Generated {digit_count}-digit prime: {p_formatted}\n\n", "bold")
        else:
            self.output_text.insert(tk.END, f"Selected prime: {p_formatted}\n\n", "bold")

        # Find a combination of discovered primes.
        if discovered_count == 2:
            discovered = find_prime_pairs(p)
        else:
            discovered = find_prime_combination(p, discovered_count)
        if not discovered:
            self.output_text.insert(tk.END, f"No combination of {discovered_count} discovered primes found.\n")
            return

        # Format each discovered prime with commas.
        discovered_formatted = [format(x, ",") for x in discovered]
        sum_discovered = sum(discovered)
        sum_discovered_formatted = format(sum_discovered, ",")

        # Bold output for the discovered primes.
        self.output_text.insert(
            tk.END,
            f"Found a combination of {discovered_count} discovered primes whose average equals the prime:\n\n"
            f"Pair: {', '.join(discovered_formatted)}\n\n",
            "bold"
        )

        # Display the proof.
        target_sum = p * discovered_count
        target_sum_formatted = format(target_sum, ",")
        self.output_text.insert(
            tk.END,
            "Proof:\n\n"
            f"Generated/Selected Prime times number of Discovered Primes: {p_formatted} x {discovered_count} = {target_sum_formatted}\n"
            f"Sum of Discovered Primes: {' + '.join(discovered_formatted)} = {sum_discovered_formatted}\n\n"
            "This matches the expected relation: p\u2081 + p\u2082 + ... + p\u2099 = n \u00D7 p,\n"
            "where p\u2081, p\u2082, ..., p\u2099 are the discovered primes, p is the generated/selected prime,\n"
            "and n is the number of discovered primes.\n\n"
        )


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    gui = PrimeGUI(root)
    root.mainloop()
