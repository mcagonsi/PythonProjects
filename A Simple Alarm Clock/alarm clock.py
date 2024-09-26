from datetime import datetime,time,timedelta
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import winsound  # For Windows system

class Alarm(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Alarm Clock')
        self.geometry('300x140')

        def reset():
            self.destroy()

        def start():
            time = alarm_time.get()
            try:
                time = time.split(":")
                hour = int(time[0])
                minute = int(time[1])
                if hour < 24 and minute < 60:


                    now = datetime.datetime.now()
                    while True:

                        if now.hour == hour and now.minute == minute:
                            winsound.Beep(1000, 3000)
                            messagebox.showinfo('Ringing','Wake up')

                            break
                        else:
                            now = datetime.datetime.now()
                            continue

                else:


                    invalid = ttk.Label(frame,text='Invalid Time')
                    invalid.grid(column=0,row=3)
            except Exception:
                invalid = ttk.Label(frame,text='Invalid Format')
                invalid.grid(column=0,row=4)

        frame = ttk.Frame(self,padding ='10 10 10 10')
        frame.pack(fill='both',expand=True)

        alarm_time_label = ttk.Label(frame,text='Set Alarm Time HH:MM')
        alarm_time_label.grid(column=0,row=0)

        alarm_time=tk.StringVar()
        alarm_time_entry = ttk.Entry(frame,textvariable=alarm_time)
        alarm_time_entry.grid(column=1,row=0)

        start_alarm =ttk.Button(frame,text='Start Alarm',command=start)
        start_alarm.grid(column=0,row=2)

        reset_alarm =ttk.Button(frame,text='Reset Alarm',command=reset)
        reset_alarm.grid(column=1,row=2)

        for child in frame.winfo_children():
            child.grid_configure(padx=5,pady=5)

def main():
    AlarmClock = Alarm()
    AlarmClock.mainloop()


if __name__ =='__main__':
    main()

