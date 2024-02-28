import ast
from tkinter import messagebox
from appids import appids as app_ids

def get_app_ids():
        """获取app id"""
        try:
            with open("selected_appids.py", "r") as file:
                content = file.read()
                app_ids_dict = ast.literal_eval(content)
                return app_ids_dict.get("LEFT_APPID", ""), app_ids_dict.get("RIGHT_APPID", "")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{e}")
            return "", ""
    
    
def get_app_ids1():
    """读取app id"""
    with open('selections.txt', 'r') as file:
        content = file.read()

    lines = content.split('\n')

    for line in lines:
        if line.startswith('left='):
            left_value = line.split('=')[1] 
        elif line.startswith('right='):
            right_value = line.split('=')[1]
    if left_value:
        left_appid = app_ids.get(f"{left_value}", '')
    else:
        left_appid = None
    if right_value:
        right_appid = app_ids.get(f"{right_value}", '')
    else:
        right_appid = None
    return left_appid, right_appid 



def get_app_ids2():
    """读取app id"""
    app_ids_dict = {}

    with open('selections.txt', 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split('=')
            app_ids_dict[key] = app_ids.get(value, None)
    
    print(app_ids_dict)
    return app_ids_dict.get('left'), app_ids_dict.get('right')

get_app_ids2()