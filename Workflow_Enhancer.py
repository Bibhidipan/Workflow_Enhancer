import tkinter as tk
from tkinter import*
from tkinter import Label, LabelFrame, Entry, Button, Listbox, Scrollbar, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import pymysql

class Todo:
    def __init__(self, todo_root):
        self.root=todo_root
        self.root.title("To Do App")
        self.root.geometry("820x520")
        self.root.configure(bg="#171315")
        Label(self.root, text="The Todo App", bg="#171315", fg="#0b9e81", font=("Calibri", 20, "bold", "italic")).grid(row=0, column=0, padx=10, pady=10)
        
        self.frame = LabelFrame(self.root, text="Task adding section", bg="#0b9e81", fg="#333333")
        self.frame.grid(row=1, column=0, padx=15, pady=10, columnspan=3, sticky="nw")
        self.Task_entry= Entry(self.frame, bd=1, relief="flat", width=40, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"))
        self.Task_entry.grid(row=1, column= 0, padx=5, sticky="nsew")
        self.Task_entry.insert(0, "Enter The Task")
        self.Task_entry.bind("<FocusIn>", self.on_entry_click)
        self.Task_entry.bind("<FocusOut>", self.on_focus_out)
        self.Priority= ttk.Combobox(self.frame, values=["--Set Priority--","High", "Medium", "Low"], state="readonly", width=13)
        self.Priority.grid(row=1, column=1,padx=5, sticky="nsew")
        self.Priority.current(0)
        self.Target_Date= DateEntry(self.frame, width=10, background='Green', foreground='white', borderwidth=2, year=2024, month=1, day=1, date_pattern='y-mm-dd')
        self.Target_Date.grid(row=1, column=3, padx=5, sticky="nsew")
        Button(self.frame, text="Add Task",bd=0, bg="#0b9e81", fg="#333333", font=("Calibri", 12, "bold", "italic"), command=self.Add).grid(row=1, column=4,padx=10)
        
        self.frame2= LabelFrame(self.root, text="Pending Task List", bg="#0b9e81", fg="#333333", padx=5, pady=5)
        self.frame2.grid(row=2, column=0, padx=15, pady=10)
        self.Task_List= Listbox(self.frame2, bd=1, relief="flat", height=15, width=45, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"))
        self.Task_List.grid(row= 0, column= 0, padx=5, pady=5, sticky="nsew")
        self.Vscrollbar=Scrollbar(self.frame2, orient="vertical", command=self.Task_List.yview)
        self.Vscrollbar.grid(row=0, column=1, sticky="ns")
        self.Task_List.config(yscrollcommand=self.Vscrollbar.set)
        self.Vscrollbar.config(command=Listbox.yview)

        self.frame3= LabelFrame(self.root, text="Ongoing Task List", bg="#0b9e81", fg="#333333", padx=5, pady=5)
        self.frame3.grid(row=3, column=0, pady=10)
        self.Ongoing_Task_List= Listbox(self.frame3, bd=1, relief="flat", height=15, width=45, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"))
        self.Ongoing_Task_List.grid(row= 0, column= 0, padx=5, pady=5, sticky="nsew")
        self.Vscrollbar2=Scrollbar(self.frame3, orient="vertical", command=self.Task_List.yview)
        self.Vscrollbar2.grid(row=0, column=1, sticky="ns")
        self.Task_List.config(yscrollcommand=self.Vscrollbar2.set)
        self.Vscrollbar2.config(command=Listbox.yview)

        self.frame4= LabelFrame(self.root, text="Completed Task List", bg="#0b9e81", fg="#333333", padx=5, pady=5)
        self.frame4.grid(row=4, column=0, padx=15, pady=10)
        self.Completed_Task_List= Listbox(self.frame4, bd=1, relief="flat", height=15, width=45, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"))
        self.Completed_Task_List.grid(row= 0, column= 0, padx=5, pady=5, sticky="nsew")
        self.Vscrollbar3=Scrollbar(self.frame4, orient="vertical", command=self.Task_List.yview)
        self.Vscrollbar3.grid(row=0, column=1, sticky="ns")
        self.Task_List.config(yscrollcommand=self.Vscrollbar3.set)
        self.Vscrollbar3.config(command=Listbox.yview)

        self.Create_Data()
        self.populate_listbox()

    def on_entry_click(self, event):
        """Function to handle placeholder removal on focus in."""
        if self.Task_entry.get() == "Enter The Task":
            self.Task_entry.delete(0, "end")

    def on_focus_out(self, event):
        """Function to handle placeholder restoration on focus out."""
        if not self.Task_entry.get():
            self.Task_entry.insert(0, "Enter The Task")

    def Entry_clear(self):
        self.Task_entry.delete(0,tk.END)

    def Create_Data(self):  
                try:
                    Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi")
                    #Use Your LocalDB Login credentials
                    MyCursor=Connection_var.cursor()
                    MyCursor.execute("CREATE DATABASE IF NOT EXISTS todo_list")
                    MyCursor.execute("use todo_list")
                    MyCursor.execute("create table if not exists data(id int auto_increment primary key not null, Task varchar(1000), Priority varchar(10), Target_Date varchar(20), status varchar(10))")
                    Connection_var.close()
                except Exception as e:
                    messagebox.showerror("Error", f"There is no task to add the task{e}")

    def Add(self):
        if self.Task_entry.get()=="" or self.Task_entry.get()=="Enter The Task" : messagebox.showerror("Error", "There is no task to add")
        elif self.Priority.get()=="--Set Priority--": messagebox.showerror("Error", "Set the priority for task")
        else:
            try:
                Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi", database="todo_list")
                #Use Your LocalDB Login credentials
                MyCursor=Connection_var.cursor()
                MyCursor.execute("use todo_list")
                MyCursor.execute("insert into data (Task, Priority, Target_Date, Status) values(%s, %s, %s, %s)", (self.Task_entry.get(), self.Priority.get(), self.Target_Date.get(), "Pending"))
                Connection_var.commit()
                Connection_var.close()
                messagebox.showinfo("Success", "Task Added")
                self.Entry_clear()
                self.populate_listbox()
            except Exception as e: 
                messagebox.showerror("Error", f"failed to add task {e}")


    def fetch_data(self):
        try:
            Connection_var = pymysql.connect(host="localhost", user="root", password="SQL@2022bibhi", database="todo_list")
            #Use Your LocalDB Login credentials
            cursor = Connection_var.cursor()
            cursor.execute("SELECT id, Task, Priority, Target_Date, Status FROM data")
            rows = cursor.fetchall()
            Priority_Level={"High":1, "Medium":2, "Low":3}
            Sorted_rows=sorted(rows, key=lambda x:(x[3], Priority_Level.get(x[2],4)))
            cursor.close()
            Connection_var.close()
            return Sorted_rows
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")
            return []

    def populate_listbox(self):
        for frame in [self.frame2, self.frame3, self.frame4]:
            for widget in frame.winfo_children():
                widget.destroy()

        self.add_listbox_headers()
        rows = self.fetch_data()
        for row in rows:
            task_id, task, priority, target_date, status = row
            self.create_task_widget(task_id, task, priority, target_date, status)

    def add_listbox_headers(self):
        for frame in [self.frame2, self.frame3, self.frame4]:
            self.task_frame1 = tk.Frame(frame, bg="#171315")
            self.task_frame1.grid(sticky="nsew")

            t_Label = tk.Label(self.task_frame1, text="Tasks", bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=60, anchor="center")
            t_Label.grid(row=0, column=1)

            p_label = tk.Label(self.task_frame1, text="Priority", bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=10, anchor="center")
            p_label.grid(row=0, column=2)

            td_label = tk.Label(self.task_frame1, text="Target Date", bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=10, anchor="center")
            td_label.grid(row=0, column=3)

            Status_label = tk.Label(self.task_frame1, text="Status", bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=13, anchor="center")
            Status_label.grid(row=0, column=4)


    def create_task_widget(self, task_id, task, priority, target_date, status):
            
        if status == 'Pending':
            listbox = self.Task_List
            frame = self.frame2
        elif status == 'Ongoing':
            listbox = self.Ongoing_Task_List
            frame = self.frame3
        elif status == 'Completed':
            listbox = self.Completed_Task_List
            frame = self.frame4
        else:
            listbox = self.Task_List  # Default to pending tasks list
            frame = self.frame2

        task_frame = tk.Frame(frame, bg="#171315")
        task_frame.grid(sticky="nsew")

        task_label = tk.Label(task_frame, text=task, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=60, anchor="w")
        task_label.grid(row=1, column=1, padx=10)

        priority_label = tk.Label(task_frame, text=priority, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=6, anchor="center")
        priority_label.grid(row=1, column=2)

        target_date_label = tk.Label(task_frame, text=target_date, bg="#171315", fg="#0b9e81", font=("Calibri", 12, "bold", "italic"), width=10, anchor="center")
        target_date_label.grid(row=1, column=3, padx=15)

        status_menu = ttk.Combobox(task_frame, values=["Pending", "Ongoing", "Completed", "Delete"], state="readonly", width=8)
        status_menu.set(status)
        status_menu.grid(row=1, column=4)
        status_menu.bind("<<ComboboxSelected>>", lambda event, tid=task_id, sm=status_menu: self.update_status(tid, sm))

    def update_status(self, task_id, status_menu):
        new_status = status_menu.get()
        try:
            if new_status == "Delete":
                connection = pymysql.connect(host="localhost", user="root", password="SQL@2022bibhi", database="todo_list")
                #Use Your LocalDB Login credentials
                cursor = connection.cursor()
                cursor.execute("DELETE FROM data WHERE id = %s", (task_id,))
                connection.commit()
                connection.close()
                self.populate_listbox()
            else:
                connection = pymysql.connect(host="localhost", user="root", password="SQL@2022bibhi", database="todo_list")
                #Use Your LocalDB Login credentials
                cursor = connection.cursor()
                cursor.execute("UPDATE data SET Status = %s WHERE id = %s", (new_status, task_id))
                connection.commit()
                connection.close()
                self.populate_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")


if __name__ == "__main__":
    todo_root = tk.Tk()
    app = Todo(todo_root)
    todo_root.mainloop()

