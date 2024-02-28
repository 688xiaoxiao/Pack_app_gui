
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import font  
import threading
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from base import Base
import time
import ast
from cfg import CHROME_DRIVER_PATH
from appids import appids as app_ids

"""已解决dropdown 动态更新问题"""
"""appids.txt 配置为外部文件""" # 更新图片的逻辑，需确认，看是删除还是更新

STATUS_FIELDS = ["Status", "Update_time", "Apk_type", "App_name", "App_type", "Version", "Environment", "Remark"]

# 更新 selected_appids.py 文件
def update_appids_file(side, appid):
    with open('selected_appids.py', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    new_line = f'{side.upper()}_APPID = "{appid}"\n'
    for i, line in enumerate(lines):
        if line.startswith(f'{side.upper()}_APPID'):
            lines[i] = new_line
            break
    
    with open('selected_appids.py', 'w', encoding='utf-8') as file:
        file.writelines(lines)

# 保存选择到 selections.txt
def save_selection(selected, side):
    try:
        with open('selections.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    new_line = f'{side}={selected}\n'
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(side):
            lines[i] = new_line
            updated = True
            break

    if not updated:
        lines.append(new_line)

    with open('selections.txt', 'w', encoding='utf-8') as file:
        file.writelines(lines)

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
        # update_appids_file(side, '')
        other_dropdown["values"] = ["清除已选"] + all_options
        save_selection(None, side)
        event.widget.master.focus()  # 移除焦点
    else:
        other_dropdown['values'] = ["清除已选"] + [option for option in all_options if option != selected_value]
        event.widget.master.focus()  # 移除焦点
        # 更新 selected_appids.py 文件中的 appid
        # appid = app_ids.get(selected_value, '')
        # update_appids_file(side, appid)
        save_selection(selected_value, side)


# 创建下拉列表的函数
def create_dropdown(root, var, values, column, row, side):
    dropdown = ttk.Combobox(root, textvariable=var, values=["清除已选"] + values, postcommand=lambda: var.set('') if var.get() == "请选择您的应用" else None, state='readonly')
    dropdown.bind('<<ComboboxSelected>>', lambda event: update_dropdown_options(event, var, right_dropdown if side == 'left' else left_dropdown, options, side))
    dropdown.grid(column=column, row=row, padx=10, pady=10)
    return dropdown


# 读取app id
def get_appids():
    """读取app id"""
    app_ids_dict = {}

    with open('selections.txt', 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split('=')
            app_ids_dict[key] = app_ids.get(value, None)
    
    print(app_ids_dict)
    return app_ids_dict.get('left'), app_ids_dict.get('right')

#  执行子进程 
def exe_sub_process():
    root.iconify()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    options.page_load_strategy = 'eager' 
    options.add_argument("--headless")   # default as non visualizd mode
    d = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    # d = webdriver.Chrome(options=options)  # 若webdriver已加入系统环境变量
    # 从 selections.txt 中读取用户选择的应用
    left_appid, right_appid = get_appids()
    
    left_status_info, right_status_info = Base(d).pack_app_for_gui(left_appid, right_appid) 
    
    # Check if left_status_info is not None before creating the dictionary
    left_status_info = {key: value for key, value in zip(STATUS_FIELDS, left_status_info)} if left_status_info is not None else None

    right_status_info = {key: value for key, value in zip(STATUS_FIELDS, right_status_info)} if right_status_info is not None else None

    # update the gui after the "long running process"
    if left_status_info:
        if left_status_info["Status"] == "成功":
            root.after(0, update_ui, upper_left_frame, r"qr_code_img\Android.png", left_status_info)
    else:
        root.after(0, update_ui, upper_left_frame, r"", left_status_info)  # 失败后 传入有意义的字段值
        
    if right_status_info:
        if right_status_info["Status"] == "成功":
            root.after(0, update_ui, upper_right_frame, r"qr_code_img\IOS.png", right_status_info)
    else:
        root.after(0, update_ui, upper_right_frame, r"", right_status_info)

    messagebox.showinfo("Notification", "Check it out!")
    # 重新启用run按钮
    root.after(0, run_button.config, {'state': 'normal'})

#  run按钮点击事件
def on_run_click():
    """run按钮点击事件"""
    left_appid, right_appid = get_appids()
    # 校验appids
    if left_appid is None and right_appid is None:
        messagebox.showinfo("提示", "请至少选择一个应用")
        return 
    elif left_appid == right_appid:
        messagebox.showinfo("提示", "请重新选择应用") 
        return  

    # 清空当前显示的数据和图片
    # update_ui(upper_left_frame, None, {field: "" for field in STATUS_FIELDS})
    # update_ui(upper_right_frame, None, {field: "" for field in STATUS_FIELDS})
    for frame in (upper_left_frame, upper_right_frame):
        update_ui(frame, None, {field: "" for field in STATUS_FIELDS})
    
    # 禁用run按钮
    run_button.config(state='disabled')
    # 开始长时间运行的子进程
    threading.Thread(target=exe_sub_process).start()


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
    # Update image if provided
    if img_path:
        img = PhotoImage(file=img_path)
        frame.canvas.create_image(128, 128, image=img)
        frame.canvas.image = img  # Keep a reference!
    else:
        frame.canvas.delete("all")  # Clear canvas
        frame.canvas.create_rectangle(2, 2, 254, 254, outline="black", fill="white")
        frame.canvas.create_text(128, 128, text="No Image Available")

    # Update status fields
    for field, value in status_info.items():
        frame.status_fields[field].config(text=value)

# 修改关闭窗口的行为
def on_closing():
    if messagebox.askokcancel("关闭", "确定关闭?"):
        root.destroy()

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

def on_escape(event):
    root.iconify()  # 最小化窗口
    
    
# 主程序开始
root = tk.Tk()
root.title("APP打包助手V23.7.1")
root.geometry("1150x630")

standard_font = font.Font(size=12)

# 使用单个Frame使用grid放置所有widget
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

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
# options = ['EU Android', 'EU IOS', '以色列 Android', '以色列 IOS', '阿联酋 Android', '阿联酋 IOS']
options = [key for key in app_ids]
# app_ids = {'以色列 IOS': '1', '以色列 Android': '2', '阿联酋 IOS': '3', '阿联酋 Android': '4', 'EU IOS': '5', 'EU Android': '6'}

left_var = tk.StringVar(value="请选择应用")
right_var = tk.StringVar(value="请选择应用")

# 加载用户选择的应用并设置下拉列表的初始值
selections = load_selections()
left_initial_selection = selections['left'] if selections['left'] in app_ids else "请选择您的应用"
right_initial_selection = selections['right'] if selections['right'] in app_ids else "请选择您的应用"

left_var.set(left_initial_selection)
right_var.set(right_initial_selection)

# 创建下拉列表并放置到左右部分
left_dropdown = create_dropdown(upper_left_frame, left_var, options, 0, 0, 'left')
right_dropdown = create_dropdown(upper_right_frame, right_var, options, 0, 0, 'right')

# Initialize UI for left and right frames
initialize_ui(upper_left_frame, STATUS_FIELDS)
initialize_ui(upper_right_frame, STATUS_FIELDS)

default_value_for_gui = "--"
original_status_info = {key: default_value_for_gui for key in STATUS_FIELDS}

# 在左右侧区域添加图片和状态信息
update_ui(upper_left_frame, r"", original_status_info)
update_ui(upper_right_frame, r"", original_status_info)

# Bind the <Button-1> (left mouse button click) event on the root window
root.bind("<Button-1>", handle_click)

# Pass 'options' as an argument when binding the event
left_dropdown.bind('<<ComboboxSelected>>', lambda event: update_dropdown_options(event, left_var, right_dropdown, options, 'left'))
right_dropdown.bind('<<ComboboxSelected>>', lambda event: update_dropdown_options(event, right_var, left_dropdown, options, 'right'))

run_button = tk.Button(lower_frame, text="Run", command=on_run_click)
run_button.pack(pady=30, ipadx=30, ipady=10)

# 绑定按键事件
root.bind("<Escape>", on_escape)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
