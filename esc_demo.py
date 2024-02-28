import tkinter as tk

def on_escape(event):
    root.iconify()  # 最小化窗口

root = tk.Tk()
root.title("Minimize on Esc")

# 绑定按键事件
root.bind("<Escape>", on_escape)

# # 创建一个简单的标签
# label = tk.Label(root, text="Press Esc to minimize the window.")
# label.pack(padx=20, pady=20)

root.mainloop()
