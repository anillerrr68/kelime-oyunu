import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random

# --- RENKLER ---
BG_COLOR = "#2c3e50"
FRAME_COLOR = "#34495e"
BUTTON_COLOR = "#ecf0f1"
TEXT_COLOR = "#ecf0f1"
CORRECT_COLOR = "#2ecc71"
WRONG_COLOR = "#e74c3c"

# --- ANA PENCERE ---
root = tk.Tk()
root.title("Kelime Oyunu")
root.geometry("700x600")
root.configure(bg=BG_COLOR)

# --- STİL ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Calibri",16,"bold"), padding=10)
style.configure("TLabel", font=("Calibri",18), foreground=TEXT_COLOR, background=BG_COLOR)

# --- DURUM DEĞİŞKENLERİ ---
hangman_word = ""
display_word = ""
wrong_guesses = 0
max_wrong = 6
scramble_word = ""
score = 0
time_limit = 30  # saniye
hangman_time_left = 0
scramble_time_left = 0
timer_id = None

# --- MENÜ ---
def show_menu():
    hangman_frame.grid_forget()
    scramble_frame.grid_forget()
    menu_frame.grid(row=0, column=0, sticky="nsew")
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

# --- ZAMANLAYICI FONKSİYONU ---
def update_timer(frame_type):
    global hangman_time_left, scramble_time_left, timer_id
    if frame_type == "hangman":
        if hangman_time_left > 0:
            hangman_time_left -= 1
            hangman_timer.config(text=f"Süre: {hangman_time_left}s")
            timer_id = root.after(1000, lambda: update_timer("hangman"))
        else:
            messagebox.showinfo("Süre Bitti!", f"Kelimeyi bulamadınız! Kelime: {hangman_word}")
            start_hangman()
    elif frame_type == "scramble":
        if scramble_time_left > 0:
            scramble_time_left -= 1
            scramble_timer.config(text=f"Süre: {scramble_time_left}s")
            timer_id = root.after(1000, lambda: update_timer("scramble"))
        else:
            score -= 2
            scramble_score.config(text=f"Puan: {score}")
            messagebox.showinfo("Süre Bitti!", f"Kelimeyi çözemediniz! Kelime: {scramble_word}")
            start_scramble()

# --- HANGMAN ---
def start_hangman():
    global hangman_word, display_word, wrong_guesses, hangman_time_left, timer_id
    hangman_word = simpledialog.askstring("Kelime Girin", "Oynanacak kelimeyi girin:").upper()
    display_word = "_" * len(hangman_word)
    wrong_guesses = 0
    hangman_time_left = time_limit
    hangman_label.config(text=" ".join(display_word), font=("Calibri",36,"bold"))
    hangman_status.config(text=f"Hatalı Tahmin: {wrong_guesses}/{max_wrong}")
    hangman_score.config(text=f"Puan: {score}")
    hangman_timer.config(text=f"Süre: {hangman_time_left}s")
    hangman_frame.grid(row=0, column=0, sticky="nsew")
    menu_frame.grid_forget()
    letter_entry.delete(0, tk.END)
    letter_entry.focus()
    if timer_id:
        root.after_cancel(timer_id)
    update_timer("hangman")

def guess_letter():
    global display_word, wrong_guesses, score
    letter = letter_entry.get().upper()
    letter_entry.delete(0, tk.END)
    if len(letter) !=1 or not letter.isalpha():
        messagebox.showwarning("Uyarı","Lütfen tek bir harf girin!")
        return
    if letter in hangman_word:
        new_display = ""
        for i,c in enumerate(hangman_word):
            new_display += c if c == letter or display_word[i] != "_" else "_"
        display_word = new_display
        hangman_label.config(text=" ".join(display_word))
        score += 5
    else:
        wrong_guesses += 1
        score -= 2
        hangman_status.config(text=f"Hatalı Tahmin: {wrong_guesses}/{max_wrong}")
    hangman_score.config(text=f"Puan: {score}")
    if display_word == hangman_word:
        messagebox.showinfo("Tebrikler!", f"Kelimeyi buldunuz: {hangman_word}")
        start_hangman()
    elif wrong_guesses >= max_wrong:
        messagebox.showinfo("Oyun Bitti", f"Kaybettiniz! Kelime: {hangman_word}")
        start_hangman()

# --- SCRAMBLE ---
def start_scramble():
    global scramble_word, scramble_time_left, timer_id
    scramble_word = simpledialog.askstring("Kelime Girin", "Oynanacak kelimeyi girin:").upper()
    letters = list(scramble_word)
    random.shuffle(letters)
    scramble_time_left = time_limit
    scramble_label.config(text=" ".join(letters), font=("Calibri",36,"bold"))
    scramble_score.config(text=f"Puan: {score}")
    scramble_timer.config(text=f"Süre: {scramble_time_left}s")
    scramble_frame.grid(row=0, column=0, sticky="nsew")
    menu_frame.grid_forget()
    word_entry.delete(0, tk.END)
    word_entry.focus()
    if timer_id:
        root.after_cancel(timer_id)
    update_timer("scramble")

def check_scramble():
    global score
    guess = word_entry.get().upper()
    word_entry.delete(0, tk.END)
    if guess == scramble_word:
        score += 10
        scramble_score.config(text=f"Puan: {score}")
        messagebox.showinfo("Tebrikler!", f"Doğru! Kelime: {scramble_word}")
        start_scramble()
    else:
        score -= 2
        scramble_score.config(text=f"Puan: {score}")

# --- MENÜ ---
menu_frame = ttk.Frame(root, style="TFrame")
menu_frame.grid_rowconfigure([0,1,2], weight=1)
menu_frame.grid_columnconfigure(0, weight=1)
ttk.Label(menu_frame,text="Kelime Oyunu", font=("Calibri",36,"bold")).grid(row=0,column=0,pady=30)
ttk.Button(menu_frame,text="Hangman Oyunu", command=start_hangman).grid(row=1,column=0,pady=20)
ttk.Button(menu_frame,text="Scramble Oyunu", command=start_scramble).grid(row=2,column=0,pady=20)
menu_frame.grid(row=0, column=0, sticky="nsew")

# --- HANGMAN FRAME ---
hangman_frame = ttk.Frame(root, style="TFrame")
hangman_label = ttk.Label(hangman_frame,text="", font=("Calibri",36,"bold"))
hangman_label.pack(pady=20)
hangman_status = ttk.Label(hangman_frame,text="", font=("Calibri",20))
hangman_status.pack()
hangman_score = ttk.Label(hangman_frame,text=f"Puan: {score}", font=("Calibri",20))
hangman_score.pack()
hangman_timer = ttk.Label(hangman_frame,text="", font=("Calibri",20))
hangman_timer.pack(pady=5)
letter_entry = tk.Entry(hangman_frame,font=("Calibri",24))
letter_entry.pack(pady=10)
ttk.Button(hangman_frame,text="Tahmin Et", command=guess_letter).pack(pady=10)
ttk.Button(hangman_frame,text="Yeni Oyun", command=start_hangman).pack(pady=10)
ttk.Button(hangman_frame,text="Menüye Dön", command=show_menu).pack(pady=10)

# --- SCRAMBLE FRAME ---
scramble_frame = ttk.Frame(root, style="TFrame")
scramble_label = ttk.Label(scramble_frame,text="", font=("Calibri",36,"bold"))
scramble_label.pack(pady=20)
scramble_score = ttk.Label(scramble_frame,text=f"Puan: {score}", font=("Calibri",20))
scramble_score.pack()
scramble_timer = ttk.Label(scramble_frame,text="", font=("Calibri",20))
scramble_timer.pack(pady=5)
word_entry = tk.Entry(scramble_frame,font=("Calibri",24))
word_entry.pack(pady=10)
ttk.Button(scramble_frame,text="Kontrol Et", command=check_scramble).pack(pady=10)
ttk.Button(scramble_frame,text="Yeni Oyun", command=start_scramble).pack(pady=10)
ttk.Button(scramble_frame,text="Menüye Dön", command=show_menu).pack(pady=10)

# --- UYGULAMA ---
root.mainloop()
