import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

root = tk.Tk()
root.title("Tic-Tac-Toe")

log_path = "oix.log"
current_player = "X"
score_x = 0
score_o = 0
history = []
board_size = 3
board = []
buttons = []

def check_winner():
    for i in range(board_size):
        if all(board[i][j] == current_player for j in range(board_size)):
            return True
        if all(board[j][i] == current_player for j in range(board_size)):
            return True
    if all(board[i][i] == current_player for i in range(board_size)):
        return True
    if all(board[i][board_size - 1 - i] == current_player for i in range(board_size)):
        return True
    return False

def is_draw():
    return all(board[i][j] != "" for i in range(board_size) for j in range(board_size))

def on_click(row, col):
    global current_player, score_x, score_o
    if board[row][col] == "":
        board[row][col] = current_player
        color = "red" if current_player == "X" else "blue"
        buttons[row][col].config(text=current_player, fg=color, state="disabled")
        if check_winner():
            if current_player == "X":
                score_x += 1
            else:
                score_o += 1
            update_score()
            zapisz_zwyciestwo(current_player)
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_board()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            zapisz_zwyciestwo("Draw")
            reset_board()
        else:
            current_player = "O" if current_player == "X" else "X"

def update_score():
    score_label.config(text=f"X: {score_x}   O: {score_o}")

def reset_board():
    global board, buttons, current_player
    current_player = "X"
    board = [["" for _ in range(board_size)] for _ in range(board_size)]
    for widget in board_frame.winfo_children():
        widget.destroy()
    buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
    for i in range(board_size):
        for j in range(board_size):
            btn = tk.Button(board_frame, text="", font=("Arial", 32), width=3, height=1,
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j, padx=2, pady=2)
            buttons[i][j] = btn

def zapisz_zwyciestwo(who):
    czas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if who in ["X", "O"]:
        imie = simpledialog.askstring("Winner Name", f"Player {who} won!\nEnter your name:")
        if imie:
            history.append(f"{czas} — Winner: {who} ({imie})")
        else:
            history.append(f"{czas} — Winner: {who}")
    else:
        history.append(f"{czas} — Result: Draw")

def show_history():
    win = tk.Toplevel(root)
    win.title("Victory History")
    win.geometry("300x300")
    text = tk.Text(win, wrap="word", font=("Arial", 12))
    text.pack(expand=True, fill="both")
    text.insert("end", "\n".join(history))
    text.config(state="disabled")

def export_history():
    try:
        with open(log_path, "w", encoding="utf-8") as file:
            file.write("Victory History:\n\n")
            file.write("\n".join(history))
        messagebox.showinfo("Export", f"History saved to:\n{log_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export history:\n{e}")

def import_history():
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                imported = [line.strip() for line in lines if "Winner:" in line or "Result:" in line]
                history.extend(imported)
            messagebox.showinfo("Import", f"History imported from:\n{log_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import history:\n{e}")
    else:
        messagebox.showwarning("Not Found", f"No oix.log file found in:\n{os.getcwd()}")

def change_board_size(size):
    global board_size
    board_size = size
    reset_board()

def show_about():
    messagebox.showinfo("About", "        polsoft.ITS  London\n\n                Tic-Tac-Toe\n\n2025© Sebastian Januchowski")

def exit_game():
    root.quit()

menu_bar = tk.Menu(root)

game_menu = tk.Menu(menu_bar, tearoff=0)
game_menu.add_command(label="New Game", command=reset_board)
game_menu.add_command(label="Victory History", command=show_history)
game_menu.add_command(label="Export History", command=export_history)
game_menu.add_command(label="Import History", command=import_history)
game_menu.add_command(label="Exit", command=exit_game)
menu_bar.add_cascade(label="Game", menu=game_menu)

board_menu = tk.Menu(menu_bar, tearoff=0)
for size in [3, 4, 6, 8, 10]:
    board_menu.add_command(label=f"{size} x {size}", command=lambda s=size: change_board_size(s))
menu_bar.add_cascade(label="Board", menu=board_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

board_frame = tk.Frame(root)
board_frame.pack(pady=10)

score_label = tk.Label(root, text="X: 0   O: 0", font=("Arial", 14))
score_label.pack(pady=(0, 10))

reset_board()
root.mainloop()