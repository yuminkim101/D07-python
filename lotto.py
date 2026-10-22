import random
import tkinter as tk
from datetime import datetime

SETS = 5
PICKS = 6
BG = "#FFF0F5"
BALL_COLORS = ["#FFD166", "#74C0FC", "#FF8FA3", "#B8B8B8", "#8CE99A"]
FONT = "AppleGothic"


def ball_color(n):
    # 1~10 노랑, 11~20 파랑, 21~30 분홍, 31~40 회색, 41~45 초록
    return BALL_COLORS[min((n - 1) // 10, 4)]


def draw_sets():
    return [sorted(random.sample(range(1, 46), PICKS)) for _ in range(SETS)]


def show_numbers():
    for widget in result_frame.winfo_children():
        widget.destroy()

    for i, numbers in enumerate(draw_sets(), start=1):
        row = tk.Frame(result_frame, bg=BG)
        row.pack(pady=6)
        tk.Label(row, text=f"{i}세트", font=(FONT, 14, "bold"), bg=BG, fg="#C2255C").pack(side="left", padx=(0, 10))
        for n in numbers:
            tk.Label(
                row, text=str(n), width=3, font=(FONT, 16, "bold"),
                bg=ball_color(n), fg="white", relief="flat", pady=4,
            ).pack(side="left", padx=3)

    date_label.config(text=f"🗓 {datetime.now():%Y년 %m월 %d일 %H:%M} 뽑기")


root = tk.Tk()
root.title("🍀 귀여운 로또 🍀")
root.configure(bg=BG)
root.geometry("520x530")

tk.Label(root, text="🍀 행운의 로또 번호 🍀", font=(FONT, 22, "bold"), bg=BG, fg="#E64980").pack(pady=(20, 4))
date_label = tk.Label(root, text=f"🗓 오늘은 {datetime.now():%Y년 %m월 %d일}", font=(FONT, 12), bg=BG, fg="#868E96")
date_label.pack(pady=(0, 10))

result_frame = tk.Frame(root, bg=BG)
result_frame.pack(pady=6)

tk.Button(
    root, text="✨ 번호 뽑기 ✨", font=(FONT, 16, "bold"),
    fg="#C2255C", highlightbackground=BG, command=show_numbers,
).pack(pady=18)

tk.Label(root, text="대박 나세요! 🐰💖", font=(FONT, 12), bg=BG, fg="#E64980").pack()

root.mainloop()
