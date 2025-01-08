import tkinter as tk
import serial
from tkinter import messagebox
from PIL import Image, ImageTk

fan_state = False
light_state = False
auto_state = False
adjust_state = False
dehumidifier_state = False
default_value = "0"


def on_entry_click(event):
    widget = event.widget
    if widget.get() == default_value:
        widget.delete(0, tk.END)

def on_focus_out(event):
    widget = event.widget
    if widget.get() == "":
        widget.insert(0, default_value)


def get_input():
    global temp_input, humid_input
    temp_input = req_temp_entry.get()
    humid_input = req_humid_entry.get()

def toggle_automatic():
    global auto_state, adjust_state
    if auto_state:
        auto_state = False
        on_button.pack_forget()
        off_button.pack(padx=10)
        button_frame.pack(pady=10)
        adjust_frame.pack_forget()
        adjust_state = False
        required_frame.pack_forget()
        adjust_button.config(text="Adjustment: Off")
        home_on_button.pack_forget()
        home_off_button.pack(pady=10)
    else:
        auto_state = True
        off_button.pack_forget()
        on_button.pack(padx=10)
        button_frame.pack_forget()
        adjust_frame.pack(pady=10)
        home_on_button.pack(pady=10)
        home_off_button.pack_forget()

def toggle_fan():
    global fan_state
    if fan_state:
        fan_state = False
        fan_button.config(bg="#E90D0D", fg="white", text="Turn Off Air Conditioner")
        fan_status_label.config(text="Air Conditioner Status: Off")
        home_fan_status_label.config(text="Air Conditioner Status: Off")
    else:
        fan_state = True
        fan_button.config(bg="#54D84A", fg="white", text="Turn On Air Conditioner")
        fan_status_label.config(text="Air Conditioner Status: On")
        home_fan_status_label.config(text="Air Conditioner Status: On")

def toggle_light():
    global light_state
    if light_state:
        light_state = False
        light_button.config(bg="#E90D0D", fg="white", text="Turn Off Heater")
        light_status_label.config(text="Heater Status: Off")
        home_light_status_label.config(text="Heater Status: Off")
    else:
        light_state = True
        light_button.config(bg="#54D84A", fg="white", text="Turn On Heater")
        light_status_label.config(text="Heater Status: On")
        home_light_status_label.config(text="Heater Status: On")

def toggle_dehumidifier():
    global dehumidifier_state
    if dehumidifier_state:
        dehumidifier_state = False
        dehumidifier_button.config(bg="#E90D0D", fg="white", text="Turn Off Dehumidifier")
        dehumidifier_status_label.config(text="Dehumidifier Status: Off")
        home_dehumidifier_status_label.config(text="Dehumidifier Status: Off")
    else:
        dehumidifier_state = True
        dehumidifier_button.config(bg="#54D84A", fg="white", text="Turn On Dehumidifier")
        dehumidifier_status_label.config(text="Dehumidifier Status: On")
        home_dehumidifier_status_label.config(text="Dehumidifier Status: On")

def press_adjust_button():
    global adjust_state
    if adjust_state:
        adjust_state = False
        required_frame.pack_forget()
        adjust_button.config(text="Adjustment: Off")
    else:
        adjust_state = True
        required_frame.pack(pady=10)
        adjust_button.config(text="Adjustment: On")



def show_home_content():
    history_content_frame.pack_forget()
    setting_content_frame.pack_forget()
    home_content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    home_button.config(bg="#88D498")
    history_button.config(bg="#4CAF50")
    setting_button.config(bg="#4CAF50")

def show_history_content():
    home_content_frame.pack_forget()
    setting_content_frame.pack_forget()
    history_content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=50)
    history_button.config(bg="#88D498")
    home_button.config(bg="#4CAF50")
    setting_button.config(bg="#4CAF50")

def show_setting_content():
    home_content_frame.pack_forget()
    history_content_frame.pack_forget()
    setting_content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=50)
    setting_button.config(bg="#88D498")
    history_button.config(bg="#4CAF50")
    home_button.config(bg="#4CAF50")

def update_temperature_bar(temp):
    temp = max(0, min(55, temp))
    bar_width = int((temp / 55) * 380)
    temperature_canvas.coords(temperature_bar, 10, 22, bar_width, 38)
    if temp >= 37:
        color = "#EA1B24"
        temperature_status_label.config(text="Temperature Too High", fg="red")
    elif temp > 25:
        color = "#FFFF55"
        temperature_status_label.config(text="High Temperature", fg="orange")
    elif temp >= 15:
        color = "#68DC4B"
        temperature_status_label.config(text="Normal Temperature", fg="green")
    else:
        color = "#1DB4D4"
        temperature_status_label.config(text="Temperature Too Low", fg="blue")

    temperature_canvas.itemconfig(temperature_bar, fill=color)
    temperature_label.config(text=f"Temperature: {temp}°C")
    temperature_canvas.create_line(103.6363, 20, 103.6363, 40, fill="black", width=1)  ## 15
    temperature_canvas.create_line(172.7272, 20, 172.7272, 40, fill="black", width=1)  ## 25
    temperature_canvas.create_line(193.4545, 20, 193.4545, 40, fill="black", width=1)  ## 28
    temperature_canvas.create_line(255.6363, 20, 255.6363, 40, fill="black", width=1)  ## 37


def update_humidity_bar(humidity):
    humidity = max(0, min(100, humidity))
    bar_width = int((humidity / 100) * 380)
    humidity_canvas.coords(humidity_bar, 10, 22, bar_width, 38)

    if humidity <= 40:
        color = "#FFFF55"
        humidity_status_label.config(text="Low Humidity", fg="orange")
    elif humidity <= 70:
        color = "#68DC4B"
        humidity_status_label.config(text="Normal Humidity", fg="green")
    else:
        color = "#EA1B24"
        humidity_status_label.config(text="Humidity Too High", fg="red")

    humidity_canvas.itemconfig(humidity_bar, fill=color)
    humidity_label.config(text=f"Humidity: {humidity}%")
    humidity_canvas.create_line(152, 20, 152, 40, fill="black", width=1)  ## 40
    humidity_canvas.create_line(266, 20, 266, 40, fill="black", width=1)  ## 70

def update_gas_bar(gas):
    gas = max(0, min(1000, gas))
    bar_width = int((gas / 1000) * 380)
    gas_canvas.coords(gas_bar, 10, 22, bar_width, 38)

    if gas <= 300:
        color = "#68DC4B"
        gas_status_label.config(text="Normal Gas Concentration", fg="green")
    elif gas <= 600:
        color = "#FFFF55"
        gas_status_label.config(text="High Gas Concentration", fg="orange")
    else:
        color = "#EA1B24"
        gas_status_label.config(text="Gas Concentration Too High!", fg="red")

    gas_canvas.itemconfig(gas_bar, fill=color)
    gas_label.config(text=f"Gas Concentration: {gas} PPM")
    gas_canvas.create_line(114, 20, 114, 40, fill="black", width=1)
    gas_canvas.create_line(228, 20, 228, 40, fill="black", width=1)

    if gas > 600:
        messagebox.showerror("Smoke/Gas Warning", "SOS: Gas or Smoke Level Exceeded!")


########################################################################################################################
# Menu

root = tk.Tk()
root.title("MexTech")
root.geometry("900x550")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 900
window_height = 550
position_top = int(screen_height / 2 - window_height / 2 - 30)
position_left = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


menu_frame = tk.Frame(root, bg="#4CAF50", width=150, height=400)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

button_style = {
    "font": ("Arial", 14),
    "compound": tk.LEFT,
    "bg": "#4CAF50",
    "fg": "white",
    "bd": 0,
    "activebackground": "#3E8E41",
    "activeforeground": "white",
    "height": 70,
    "width": 200
}

# Thêm icon cho Dashboard
home_icon = Image.open("icons/home.png")
home_icon = home_icon.resize((70, 70), Image.Resampling.LANCZOS)
home_icon_tk = ImageTk.PhotoImage(home_icon)

home_button = tk.Button(menu_frame, text="  Dashboard", image=home_icon_tk, command=show_home_content, **button_style)
home_button.pack(pady=20)

# Thêm icon cho Setting
setting_icon = Image.open("icons/setting.png")
setting_icon = setting_icon.resize((50, 50), Image.Resampling.LANCZOS)
setting_icon_tk = ImageTk.PhotoImage(setting_icon)

setting_button = tk.Button(menu_frame, text="    Setting", image=setting_icon_tk, command=show_setting_content, **button_style)
setting_button.pack(fill=tk.X, pady=20)

# Thêm icon cho History
history_icon = Image.open("icons/history.png")
history_icon = history_icon.resize((60, 60), Image.Resampling.LANCZOS)
history_icon_tk = ImageTk.PhotoImage(history_icon)

history_button = tk.Button(menu_frame, text="    History", image=history_icon_tk, command=show_history_content, **button_style)
history_button.pack(fill=tk.X, pady=20)

########################################################################################################################
# content

home_content_frame = tk.Frame(root)
home_content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

temperature_frame = tk.Frame(home_content_frame)
temperature_frame.pack(pady=20)

temperature_canvas = tk.Canvas(temperature_frame, width=380, height=70, bg="#F0F0F0")
temperature_canvas.pack()

temperature_canvas.create_rectangle(10, 20, 380, 40, outline="black", width=2)
temperature_canvas.create_line(103.6363, 20, 103.6363, 40, fill="black", width=1) ## 15
temperature_canvas.create_line(172.7272, 20, 172.7272, 40, fill="black", width=1) ## 25
temperature_canvas.create_line(193.4545, 20, 193.4545, 40, fill="black", width=1) ## 28
temperature_canvas.create_line(255.6363, 20, 255.6363, 40, fill="black", width=1) ## 37
temperature_canvas.create_text(15, 50, text="0°C", font=("Arial", 10))
temperature_canvas.create_text(103.7, 50, text="15°C", font=("Arial", 10))
temperature_canvas.create_text(172.7272, 50, text="25°C", font=("Arial", 10))
temperature_canvas.create_text(193.4545, 50, text="28°C", font=("Arial", 10))
temperature_canvas.create_text(255.6363, 50, text="37°C", font=("Arial", 10))
temperature_canvas.create_text(360, 50, text="55°C", font=("Arial", 10))

temperature_bar = temperature_canvas.create_rectangle(10, 20, 10, 40, fill="#00BFFF", outline="")

temperature_label = tk.Label(temperature_frame, text="Temperature: 0°C", font=("Arial", 14))
temperature_label.pack(side=tk.LEFT, padx=20)

temperature_status_label = tk.Label(temperature_frame, text="Normal Temperature", font=("Arial", 12))
temperature_status_label.pack(side=tk.LEFT, padx=0)


humidity_frame = tk.Frame(home_content_frame)
humidity_frame.pack()

humidity_canvas = tk.Canvas(humidity_frame, width=380, height=70, bg="#F0F0F0")
humidity_canvas.pack()

humidity_canvas.create_rectangle(10, 20, 380, 40, outline="black", width=2)
humidity_canvas.create_line(152, 20, 152, 40, fill="black", width=1) ## 40
humidity_canvas.create_line(266, 20, 266, 40, fill="black", width=1) ## 70
humidity_canvas.create_text(15, 50, text="0%", font=("Arial", 10))
humidity_canvas.create_text(152, 50, text="40%", font=("Arial", 10))
humidity_canvas.create_text(266, 50, text="70%", font=("Arial", 10))
humidity_canvas.create_text(360, 50, text="100%", font=("Arial", 10))

humidity_bar = humidity_canvas.create_rectangle(10, 20, 10, 40, fill="#00BFFF", outline="")

humidity_label = tk.Label(humidity_frame, text="Humidity: 0%", font=("Arial", 14))
humidity_label.pack(side=tk.LEFT, padx=20)

humidity_status_label = tk.Label(humidity_frame, text="Normal Humidity", font=("Arial", 12))
humidity_status_label.pack(side=tk.LEFT, padx=0)

gas_frame = tk.Frame(home_content_frame)
gas_frame.pack(pady=20)

gas_canvas = tk.Canvas(gas_frame, width=380, height=70, bg="#F0F0F0")
gas_canvas.pack()

gas_canvas.create_rectangle(10, 20, 380, 40, outline="black", width=2)
gas_canvas.create_line(114, 20, 114, 40, fill="black", width=1)
gas_canvas.create_line(228, 20, 228, 40, fill="black", width=1)
gas_canvas.create_text(25, 50, text="0 PPM", font=("Arial", 10))
gas_canvas.create_text(114, 50, text="300 PPM", font=("Arial", 10))
gas_canvas.create_text(228, 50, text="600 PPM", font=("Arial", 10))
gas_canvas.create_text(352, 50, text="1000 PPM", font=("Arial", 10))

gas_bar = gas_canvas.create_rectangle(10, 20, 10, 40, fill="#00BFFF", outline="")

gas_label = tk.Label(gas_frame, text="Gas Concentration: 0 PPM", font=("Arial", 14))
gas_label.pack(side=tk.LEFT, padx=20)

gas_status_label = tk.Label(gas_frame, text="Normal Gas Concentration", font=("Arial", 12))
gas_status_label.pack(side=tk.LEFT, padx=0)

home_status_frame = tk.Frame(home_content_frame)
home_status_frame.pack(pady = 5)

home_fan_status_label = tk.Label(home_status_frame, text="Air Conditioner Status: Off", font=("Arial", 12))
home_fan_status_label.pack(side=tk.LEFT, padx=10)

home_light_status_label = tk.Label(home_status_frame, text="Heater Status: Off", font=("Arial", 12))
home_light_status_label.pack(side=tk.LEFT, padx=10)

home_dehumidifier_status_label = tk.Label(home_status_frame, text="Dehumidifier Status: Off", font=("Arial", 12))
home_dehumidifier_status_label.pack(pady=10)


##Mode
home_auto_frame = tk.Frame(home_content_frame)
home_auto_frame.pack(pady = 10)

home_auto_label = tk.Label(home_auto_frame, text="Automatic Mode:", font=("Arial", 14))
home_auto_label.pack(side=tk.LEFT, padx=10)

home_on_icon = Image.open("icons/on_button.png")
home_on_icon = home_on_icon.resize((120, 60), Image.Resampling.LANCZOS)
home_on_icon_tk = ImageTk.PhotoImage(home_on_icon)
home_on_button = tk.Label(home_auto_frame, image=home_on_icon_tk, compound=tk.LEFT, bd=0)
home_on_button.pack(padx = 10)

home_off_icon = Image.open("icons/off_button.png")
home_off_icon = home_off_icon.resize((120, 60), Image.Resampling.LANCZOS)
home_off_icon_tk = ImageTk.PhotoImage(home_off_icon)
home_off_button = tk.Label(home_auto_frame, image=home_off_icon_tk, compound=tk.LEFT, bd = 0)

########################################################################################################################
setting_content_frame = tk.Frame(root)
status_frame = tk.Frame(setting_content_frame)
status_frame.pack(pady = 30)

fan_status_label = tk.Label(status_frame, text="Air Conditioner Status: Off", font=("Arial", 15, "bold"), fg="red")
fan_status_label.pack(side=tk.LEFT, padx=10)

light_status_label = tk.Label(status_frame, text="Heater Status: Off", font=("Arial", 15, "bold"), fg="red")
light_status_label.pack(side=tk.LEFT, padx=10)

dehumidifier_frame = tk.Frame(setting_content_frame)
dehumidifier_frame.pack()

dehumidifier_status_label = tk.Label(dehumidifier_frame, text="Dehumidifier Status: Off", font=("Arial", 15, "bold"), fg="red")
dehumidifier_status_label.pack()

###################################################################

auto_frame = tk.Frame(setting_content_frame)
auto_frame.pack(pady = 10)

auto_label = tk.Label(auto_frame, text="Automatic Mode:", font=("Arial", 14))
auto_label.pack(side=tk.LEFT, padx=10)

on_icon = Image.open("icons/on_button.png")
on_icon = on_icon.resize((120, 60), Image.Resampling.LANCZOS)
on_icon_tk = ImageTk.PhotoImage(on_icon)
on_button = tk.Button(auto_frame, image=on_icon_tk, compound=tk.LEFT, bd=0, command=toggle_automatic)
on_button.pack(padx = 10)

off_icon = Image.open("icons/off_button.png")
off_icon = off_icon.resize((120, 60), Image.Resampling.LANCZOS)
off_icon_tk = ImageTk.PhotoImage(off_icon)
off_button = tk.Button(auto_frame, image=off_icon_tk, compound=tk.LEFT, bd = 0, command=toggle_automatic)

## Button fan + light
button_frame = tk.Frame(setting_content_frame)
button_frame.pack(pady = 10)

fan_button = tk.Button(button_frame, text="Turn On Air Conditioner", font=("Arial", 12), width=20, height=2, command=toggle_fan)
fan_button.pack(side = tk.LEFT)

light_button = tk.Button(button_frame, text="Turn On Heater", font=("Arial", 12), width=20, height=2, command=toggle_light)
light_button.pack(side = tk.LEFT, padx = 10)

dehumidifier_button = tk.Button(button_frame, text="Turn On Dehumidifier", font=("Arial", 12), width=20, height=2, command=toggle_dehumidifier)
dehumidifier_button.pack(pady = 10)

## Data yêu cầu - Frame
required_frame = tk.Frame(setting_content_frame)
required_data_frame = tk.Frame(required_frame)
required_data_frame.pack(side=tk.LEFT)
required_temp = tk.Frame(required_data_frame)
required_temp.pack(pady=2)
required_humid = tk.Frame(required_data_frame)
required_humid.pack(pady=2)

##Adjust_button
adjust_frame = tk.Frame(setting_content_frame)
adjust_button = tk.Button(adjust_frame, text="Adjustment: Off", font=("Arial", 14), command=press_adjust_button)
adjust_button.pack()

## Label & Entry
req_temp_label = tk.Label(required_temp, text="Required Tempurature", font=("Arial", 14), width=17)
req_temp_label.pack(side=tk.LEFT)
req_temp_entry = tk.Entry(required_temp, font=("Arial", 12), width=6, justify="center")
req_temp_entry.insert(0, default_value)
req_temp_entry.pack(pady = 4, padx=10)

req_humid_label = tk.Label(required_humid, text="Required Humidity", font=("Arial", 14), width=17)
req_humid_label.pack(side=tk.LEFT)
req_humid_entry = tk.Entry(required_humid, font=("Arial", 12), width=6, justify="center")
req_humid_entry.insert(0, default_value)
req_humid_entry.pack(pady = 4, padx=10)

req_humid_entry.bind("<FocusIn>", on_entry_click)
req_humid_entry.bind("<FocusOut>", on_focus_out)
req_temp_entry.bind("<FocusIn>", on_entry_click)
req_temp_entry.bind("<FocusOut>", on_focus_out)

## Send button
send_icon = Image.open("icons/send_button.png")
send_icon = send_icon.resize((150, 100), Image.Resampling.LANCZOS)
send_icon_tk = ImageTk.PhotoImage(send_icon)
send_button = tk.Button(required_frame, image=send_icon_tk, compound=tk.LEFT, bd = 0, command=get_input)
send_button.pack(side=tk.LEFT, padx=20)

########################################################################################################################
history_content_frame = tk.Frame(root)
history_label = tk.Label(history_content_frame, text="Warning History", font=("Arial", 16))
history_label.pack(pady=20)

history_list = tk.Listbox(history_content_frame, font=("Arial", 12), width=60, height=15, justify="center")
history_list.pack(pady=10)

show_home_content()
toggle_automatic()
update_temperature_bar(25)
update_humidity_bar(40)
update_gas_bar(89)
gas = 305
if gas > 3022:
    messagebox.showerror("Smoke/Gas Warning", "SOS: Gas or Smoke Level Exceeded!")

# List of danger messages
danger_logs = [
    'DANGER: Temp=40.28°C, Gas=435 (Time: 2024-12-08 10:10:16)',
    'DANGER: Temp=44.30°C, Gas=476 (Time: 2024-12-08 17:49:16)',
    'DANGER: Temp=39.95°C, Gas=472 (Time: 2024-12-08 13:15:16)',
    'DANGER: Temp=44.27°C, Gas=445 (Time: 2024-12-09 04:22:16)',
    'DANGER: Temp=40.59°C, Gas=465 (Time: 2024-12-08 15:39:16)',
    'DANGER: Temp=38.79°C, Gas=454 (Time: 2024-12-08 18:26:16)',
    'DANGER: Temp=49.47°C, Gas=305 (Time: 2024-12-08 10:23:16)',
    'DANGER: Temp=45.76°C, Gas=424 (Time: 2024-12-09 09:41:16)',
    'DANGER: Temp=37.93°C, Gas=461 (Time: 2024-12-09 04:58:16)',
    'DANGER: Temp=48.18°C, Gas=492 (Time: 2024-12-08 15:10:16)'
]

# Insert danger messages into the Listbox
for log in danger_logs:
    history_list.insert(tk.END, log)

root.mainloop()
