
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import font  
import threading
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
# from base import Base
import time
import ast


STATUS_FIELDS = ["status", "update_time", "apk_type", "app_name", "app_type", "version", "environment"]

# 更新 appids.py 文件
def update_appids_file(side, appid):
    pass

# 保存选择到 selections.txt
def save_selection(selected, side):
    pass

# 加载用户选择的应用
def load_selections():
    selections = {'left': '', 'right': ''}
    try:
        with open('selections.txt', 'r', encoding='utf-8') as file:
            for line in file:
                side, value = line.strip().split('=')
                selections[side] = value
    except FileNotFoundError:
        pass  # File not found, will use default values
    return selections

# 更新下拉选项
def update_dropdown_options(event, selected_dropdown_var, other_dropdown, all_options, side):
    selected_value = selected_dropdown_var.get()
    if selected_value == "清除已选":
        selected_dropdown_var.set('')
        update_appids_file(side, '')
        other_dropdown["values"] = ["清除已选"] + all_options
        save_selection('', side)
        event.widget.master.focus()  # 移除焦点
    else:
        other_dropdown['values'] = ["清除已选"] + [option for option in all_options if option != selected_value]
        event.widget.master.focus()  # 移除焦点
        appid = app_ids.get(selected_value, '')
        update_appids_file(side, appid)
        save_selection(selected_value, side)


# 创建下拉列表的函数
def create_dropdown(root, var, values, column, row, side):
    dropdown = ttk.Combobox(root, textvariable=var, values=["清除已选"] + values, postcommand=lambda: var.set('') if var.get() == "请选择您的应用" else None, state='readonly')
    dropdown.bind('<<ComboboxSelected>>', lambda event: update_dropdown_options(event, var, right_dropdown if side == 'left' else left_dropdown, options, side))
    dropdown.grid(column=column, row=row, padx=10, pady=10)
    return dropdown


def simulate_long_process():
    pass


def on_run_click():
    """run按钮点击事件"""
    def get_app_ids():
        try:
            with open("appids.py", "r") as file:
                content = file.read()
                app_ids_dict = ast.literal_eval(content)
                return app_ids_dict.get("LEFT_APPID", ""), app_ids_dict.get("RIGHT_APPID", "")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{e}")
            return "", ""

    def check_appids():
        """校验appids"""
        left_app_id, right_app_id = get_app_ids()

        if not left_app_id and not right_app_id:
            messagebox.showinfo("提示", "请至少选择一个应用")
            return None
        elif left_app_id == right_app_id:
            messagebox.showinfo("提示", "请重新选择应用") 
            return None 

    if check_appids():
        return
    
    # 清空当前显示的数据和图片
    update_ui(upper_left_frame, None, {field: "" for field in STATUS_FIELDS})
    update_ui(upper_right_frame, None, {field: "" for field in STATUS_FIELDS})
    
    # 禁用run按钮
    run_button.config(state='disabled')
    # 开始模拟长时间运行的过程
    threading.Thread(target=simulate_long_process).start()


# 主程序开始
root = tk.Tk()
root.title("test_APP打包助手V23.9.1")
root.geometry("1150x600")

# Define a standard font
standard_font = font.Font(size=12)

# 使用单个Frame使用grid放置所有widget
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)
# main_frame.grid(fill="both", expand=True)

# 在main_frame中配置grid布局
main_frame.columnconfigure([0, 1], weight=1)
main_frame.rowconfigure([0, 1], weight=1)

# 创建上半部分的左侧和右侧区域
upper_left_frame = tk.Frame(main_frame)
upper_left_frame.grid(row=0, column=0, sticky="nsew")
upper_right_frame = tk.Frame(main_frame)
upper_right_frame.grid(row=0, column=1, sticky="nsew")

# 创建下半部分区域
lower_frame = tk.Frame(main_frame)
lower_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Configure rows and columns inside upper frames
for upper_frame in (upper_left_frame, upper_right_frame):
    upper_frame.columnconfigure(0, weight=1)
    for i in range(7):  # For the number of status fields
        upper_frame.rowconfigure(i, weight=1)

# 创建dropdowns并放置在顶部，居中
options = ['以色列 IOS', '以色列 Android', '阿联酋 IOS', '阿联酋 Android', 'EU IOS', 'EU Android']
app_ids = {'以色列 IOS': '1', '以色列 Android': '2', '阿联酋 IOS': '3', '阿联酋 Android': '4', 'EU IOS': '5', 'EU Android': '6'}

left_var = tk.StringVar(value="请选择应用")
right_var = tk.StringVar(value="请选择应用")

# 加载用户选择的应用并设置下拉列表的初始值
selections = load_selections()
left_initial_selection = selections['left'] if selections['left'] in app_ids else "请选择您的应用"
right_initial_selection = selections['right'] if selections['right'] in app_ids else "请选择您的应用"

left_var.set(left_initial_selection)
right_var.set(right_initial_selection)

# # 创建并放置左侧的下拉菜单
# left_dropdown = ttk.Combobox(upper_left_frame, textvariable=left_var, values=options, state='readonly')
# left_dropdown.pack(pady=10, expand=True)

# # 创建并放置右侧的下拉菜单
# right_dropdown = ttk.Combobox(upper_right_frame, textvariable=right_var, values=options, state='readonly')
# right_dropdown.pack(pady=10, expand=True)


# 创建下拉列表并放置到左右部分
left_dropdown = create_dropdown(upper_left_frame, left_var, options, 0, 0, 'left')
right_dropdown = create_dropdown(upper_right_frame, right_var, options, 1, 0, 'right')


# Function to initialize UI with image placeholders and default status info
def initialize_ui(frame, status_info):
    # Create a canvas for image placement
    canvas = tk.Canvas(frame, width=256, height=256, bg='white')
    canvas.create_rectangle(2, 2, 254, 254, outline="black", fill="white")
    canvas.create_text(128, 128, text="No Image Available")
    # canvas.pack(pady=20)  # run to center the canvas
    canvas.grid(pady=20)  # run to center the canvas
    frame.canvas = canvas  # Save canvas reference

    # Create status fields
    status_fields_frame = tk.Frame(frame)
    # status_fields_frame.pack()
    status_fields_frame.grid()
    frame.status_fields = {}  # Save labels reference

    for field in status_info:
        field_frame = tk.Frame(status_fields_frame)
        field_frame.pack(fill='x', expand=True)
        label = tk.Label(field_frame, text=f"{field}: ", width=12, anchor="e")
        label.pack(side="left")
        value_label = tk.Label(field_frame, text="N/A", width=12, anchor="w")
        value_label.pack(side="left")
        frame.status_fields[field] = value_label  # Save label reference for updates


# Function to update the image and status information
def update_ui(frame, img_path, status_info):
    pass

# Initialize UI for left and right frames
initialize_ui(upper_left_frame, STATUS_FIELDS)
initialize_ui(upper_right_frame, STATUS_FIELDS)

default_value_for_gui = "None"
original_status_info = {key: default_value_for_gui for key in STATUS_FIELDS}

# 在左右侧区域添加图片和状态信息
update_ui(upper_left_frame, r"", original_status_info)
update_ui(upper_right_frame, r"", original_status_info)

# Function to handle dropdown selection
def handle_dropdown_selection(event):
    # Set focus to another widget to simulate clearing the selection highlight
    left_dropdown.selection_clear()  # Clear the selection highlight
    right_dropdown.selection_clear()

    # Set focus to another widget to simulate clearing the selection highlight
    root.focus_set()

# Function to handle clicking on the root window
def handle_click(event):
    left_dropdown.selection_clear()  # Clear the selection highlight
    right_dropdown.selection_clear()
    root.focus_set()

# Bind the <Button-1> (left mouse button click) event on the root window
root.bind("<Button-1>", handle_click)

# 绑定下拉菜单的<<ComboboxSelected>>事件到处理函数
left_dropdown.bind("<<ComboboxSelected>>", handle_dropdown_selection)
right_dropdown.bind("<<ComboboxSelected>>", handle_dropdown_selection)

run_button = tk.Button(lower_frame, text="run", command=on_run_click)
run_button.pack(pady=30, ipadx=30, ipady=10)

# 修改关闭窗口的行为
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
