import tkinter as tk
from tkinter import messagebox
import random
import os
from auth import register, login, create_tables
from export import export_to_pdf

# Зчитування слів з файлів у папці "słowa"
WORDS = []
CATEGORY_WORDS = {}

slowa_dir = "słowa"
if os.path.isdir(slowa_dir):
    for filename in os.listdir(slowa_dir):
        if filename.endswith(".txt"):
            category = filename[:-4].capitalize()
            with open(os.path.join(slowa_dir, filename), "r", encoding="utf-8") as f:
                words = [line.strip().lower() for line in f if line.strip()]
                CATEGORY_WORDS[category] = words
                WORDS.extend([(w, category) for w in words])
else:
    print("Folder 'słowa' nie istnieje. Utwórz go i dodaj pliki kategorii.")

MAX_ERRORS = 6

class HangmanGame:
    def __init__(self, root, username, mode):
        self.root = root
        self.username = username
        self.mode = mode
        self.word = ""
        self.display_word = []
        self.errors = 0
        self.guessed_letters = []
        self.correct_count = 0
        self.incorrect_count = 0

        if self.mode == "czasowy":
            self.time_left = 180

        self.build_ui()
        if self.mode == "czasowy":
            self.start_timer()
        self.new_game()

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white", highlightthickness=2)
        self.canvas.pack(pady=10)

        self.category_var = tk.StringVar()
        self.word_var = tk.StringVar()

        tk.Label(self.root, textvariable=self.category_var, font=("Arial", 14, "bold")).pack(pady=5)
        self.word_label = tk.Label(self.root, textvariable=self.word_var, font=("Courier", 30, "bold"))
        self.word_label.pack(pady=10)

        if self.mode == "czasowy":
            self.timer_var = tk.StringVar()
            self.timer_label = tk.Label(self.root, textvariable=self.timer_var, font=("Arial", 14), fg="red")
            self.timer_label.pack()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.entry = tk.Entry(input_frame, font=("Arial", 22), width=2, justify='center', fg="blue", bg="white", bd=3)
        self.entry.grid(row=0, column=0, padx=10)
        self.entry.bind("<Return>", lambda event: self.guess())

        self.guess_btn = tk.Button(input_frame, text="Zgadnij", font=("Arial", 14), command=self.guess)
        self.guess_btn.grid(row=0, column=1, padx=10)

        self.new_btn = tk.Button(input_frame, text="Nowa gra", font=("Arial", 14), command=self.new_game)
        self.new_btn.grid(row=0, column=2, padx=10)

        self.menu_btn = tk.Button(self.root, text="Wróć do menu", font=("Arial", 12), command=self.back_to_menu)
        self.menu_btn.pack(pady=10)

    def new_game(self):
        if "_" in self.display_word and self.errors < MAX_ERRORS:
            self.update_stats(False)
            self.incorrect_count += 1

        self.word, self.category = random.choice(WORDS)
        self.display_word = ["_" for _ in self.word]
        self.errors = 0
        self.guessed_letters = []
        self.category_var.set(f"Kategoria: {self.category}")
        self.update_display()
        self.canvas.delete("all")
        self.draw_base()

    def update_display(self):
        self.word_var.set(" ".join(self.display_word))

    def guess(self):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Błąd", "Wpisz jedną literę.")
            return

        if letter in self.guessed_letters:
            messagebox.showinfo("Uwaga", "Już próbowałeś tej litery.")
            return

        self.guessed_letters.append(letter)

        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.display_word[i] = letter
            self.update_display()
            if "_" not in self.display_word:
                self.update_stats(True)
                self.correct_count += 1
                messagebox.showinfo("Wygrana!", f"Gratulacje! Odgadłeś słowo: {self.word}")
                self.new_game()
        else:
            self.errors += 1
            self.draw_next()
            if self.errors >= MAX_ERRORS:
                self.update_stats(False)
                self.incorrect_count += 1
                messagebox.showerror("Przegrana", f"Słowo to: {self.word}")
                self.new_game()

    def start_timer(self):
        if self.time_left > 0:
            self.timer_var.set(f"Pozostało: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Czas minął!",
                                f"Koniec gry! Odgadnięte: {self.correct_count}, Błędy: {self.incorrect_count}")
            self.back_to_menu()

    def update_stats(self, win):
        from auth import Player, Session
        session = Session()
        user = session.query(Player).filter_by(username=self.username).first()
        if user:
            if win:
                user.wins += 1
            else:
                user.losses += 1
            session.commit()
        session.close()

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MenuWindow(self.root, self.username)

    def draw_base(self):
        c = self.canvas
        c.create_line(50, 280, 250, 280, width=2)
        c.create_line(100, 280, 100, 50, width=2)
        c.create_line(100, 50, 200, 50, width=2)
        c.create_line(200, 50, 200, 80, width=2)

    def draw_next(self):
        c = self.canvas
        if self.errors == 1:
            c.create_oval(180, 80, 220, 120, width=2)
        elif self.errors == 2:
            c.create_line(200, 120, 200, 190, width=2)
        elif self.errors == 3:
            c.create_line(200, 140, 170, 170, width=2)
        elif self.errors == 4:
            c.create_line(200, 140, 230, 170, width=2)
        elif self.errors == 5:
            c.create_line(200, 190, 170, 240, width=2)
        elif self.errors == 6:
            c.create_line(200, 190, 230, 240, width=2)

class MenuWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.frame = tk.Frame(root)
        self.frame.pack(pady=100, fill="both", expand=True)

        tk.Label(self.frame, text=f"Zalogowano jako: {username}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.frame, text="Wybierz tryb gry:", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.frame, text="Klasyczny", font=("Arial", 14), width=25,
                  command=lambda: self.start_game("klasyczny")).pack(pady=5, fill="x", padx=50)

        tk.Button(self.frame, text="Na czas (3 minuty)", font=("Arial", 14), width=25,
                  command=lambda: self.start_game("czasowy")).pack(pady=5, fill="x", padx=50)

        tk.Button(self.frame, text="Statystyki", font=("Arial", 14), width=25,
                  command=self.show_stats).pack(pady=5, fill="x", padx=50)

        tk.Button(self.frame, text="Wyloguj", font=("Arial", 14), width=25,
                  command=self.logout).pack(pady=20, fill="x", padx=50)

    def start_game(self, mode):
        self.frame.destroy()
        HangmanGame(self.root, self.username, mode)

    def logout(self):
        self.root.destroy()
        main()

    def show_stats(self):
        from auth import Session, Player
        session = Session()
        players = session.query(Player).all()
        session.close()

        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statystyki graczy")

        tk.Label(stats_window, text="Nick", font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(stats_window, text="Wygrane", font=("Arial", 12, "bold")).grid(row=0, column=1)
        tk.Label(stats_window, text="Przegrane", font=("Arial", 12, "bold")).grid(row=0, column=2)

        for i, p in enumerate(players, start=1):
            tk.Label(stats_window, text=p.username).grid(row=i, column=0)
            tk.Label(stats_window, text=p.wins).grid(row=i, column=1)
            tk.Label(stats_window, text=p.losses).grid(row=i, column=2)

        tk.Button(stats_window, text="Export to PDF", font=("Arial", 12),
                      command=lambda: self.export_stats_pdf()).grid(row=i + 1, column=0, columnspan=3, pady=15)

    def export_stats_pdf(self):
        export_to_pdf()
        messagebox.showinfo("Eksport zakończony", "Plik został zapisany pomyślnie.")


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(pady=100)

        tk.Label(self.frame, text="Nazwa użytkownika:", font=("Arial", 14)).grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Hasło:", font=("Arial", 14)).grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 14), show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Zaloguj", command=self.handle_login, font=("Arial", 12)).grid(row=2, column=0, pady=10)
        tk.Button(self.frame, text="Zarejestruj", command=self.handle_register, font=("Arial", 12)).grid(row=2, column=1, pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, msg = login(username, password)
        if success:
            self.frame.destroy()
            MenuWindow(self.root, username)
        else:
            messagebox.showerror("Błąd logowania", msg)

    def handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, msg = register(username, password)
        if success:
            messagebox.showinfo("Sukces", msg)
        else:
            messagebox.showerror("Błąd rejestracji", msg)

def main():
    create_tables()
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
