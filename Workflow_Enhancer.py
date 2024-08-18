#project management app
import tkinter as tk
from tkinter import Label, LabelFrame, Entry, Button, Listbox, Scrollbar, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import re
import pymysql


class App:
    def __init__(self, login_root):
        # login_root= tk.Tk()
        self.root=login_root
        self.root.title("Project Mangement App")
        self.root.geometry("480x480")
        self.root.configure(bg="#21c476")
        tk.Label(text="Login Screen", bg="#21c476",fg="Black", font=("Arial",14,"bold", "italic")).grid(row=1,column=1, padx=10, pady=10)
        Email_id= tk.Label(self.root, text="Email id", bg="#21c476", width=12).grid(row=2,column=1, padx=20, pady=10)
        Password= tk.Label(self.root, text="Password", width=12).grid(row=3,column=1, padx=20, pady=10)
        self.Entry_Email_id= tk.Entry(self.root, bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Email_id.grid(row=2, column=3, padx=20, pady=10)
        self.Entry_Email_id.insert(0, "Enter email")
        self.Entry_Email_id.bind("<FocusIn>", self.on_Focus_In)
        self.Entry_Email_id.bind("<FocusOut>", self.on_Focus_Out)
        self.Entry_Password= tk.Entry(self.root, show="*")
        self.Entry_Password.grid(row=3, column=3, padx=20, pady=10)
        forgot_button=tk.Button(self.root,text="Forgot Password or Username?", bd=0, bg="#21c476", command=self.forgot_window).grid(row=4, column=3, padx=20, pady=10)
        signup_button=tk.Button(self.root,text="Dont have an account?", bd=0, command=self.signup_window).grid(row=5, column=3, padx=20, pady=10)
        Submit_button=tk.Button(self.root,text="Login", command=self.Login).grid(row=6, column=3, padx=20, pady=10)

    def on_Focus_In(self, event):
        if self.Entry_Email_id.get()!="":
            self.Entry_Email_id.delete(0, "end")
    def on_Focus_Out(self, event):
        if not self.Entry_Email_id.get():
            self.Entry_Email_id.insert(0, "Enter Email")

    def signup_window(self):
        self.root.destroy()
        signup_root=tk.Tk()
        signup_root.title("Project Management App")
        signup_root.geometry("580x480")
        tk.Label(text="Signup Screen", font=("calibre",14,"bold", "italic")).grid(row=1,column=1)
        Name= tk.Label(signup_root, text="Name", width=12).grid(row=2,column=1, padx=20, pady=10)
        self.Entry_Name= tk.Entry(signup_root,)
        self.Entry_Name.grid(row=2, column=2, padx=20, pady=10)
        Email_id= tk.Label(signup_root, text="Email id").grid(row=3,column=1, padx=20, pady=10)
        self.Entry_Email_id= tk.Entry(signup_root, bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Email_id.grid(row=3, column=2, padx=20, pady=10)
        Password= tk.Label(signup_root, text="Password", width=12).grid(row=4,column=1, padx=20, pady=10)
        self.Entry_Password= tk.Entry(signup_root, show="*")
        self.Entry_Password.grid(row=4, column=2, padx=20, pady=10)
        Confirm_Password= tk.Label(signup_root, text="Confirm Password").grid(row=5,column=1, padx=20, pady=10)
        self.Entry_Confirm_Password= tk.Entry(signup_root, show="*", bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Confirm_Password.grid(row=5, column=2, padx=20, pady=10)
        dob_label = tk.Label(signup_root, text="D.O.B").grid(row=6, column=1, padx=20, pady=10)
        self.dob_entry = DateEntry(signup_root, width=12, background='darkblue', foreground='white', borderwidth=2, year=2000, month=1, day=1, date_pattern='y-mm-dd')
        self.dob_entry.grid(row=6, column=2, padx=20, pady=10)
        self.dob_entry.bind("<<DateEntrySelected>>", lambda event: self.calculate_age())

        Age_section=tk.Label(signup_root, text="Your age is").grid(row=7, column=1, padx=20, pady=10)
        self.age_point = tk.Label(signup_root, text="")
        self.age_point.grid(row=7, column=2, padx=20, pady=10)

        ttk.Label(signup_root, text="Gender").grid(row=8,column=1, padx=20, pady=10)
        m= tk.StringVar()
        self.Gender= ttk.Combobox(signup_root, textvariable=m)
        self.Gender['values'] = ("Select",'Male','Female')
        self.Gender.grid(row=8,column=2, padx=20, pady=10)
        self.Gender.current(0)
        ttk.Label(signup_root, text="Security Question").grid(row=9,column=1, padx=20, pady=10)
        n= tk.StringVar()
        self.Security_QS= ttk.Combobox(signup_root, textvariable=n)
        self.Security_QS['values'] = ("Select","Your First Mobile Brand","Your First School Name","Your Favourite Pet Name")
        self.Security_QS.grid(row=9,column=2, padx=20, pady=10)
        self.Security_QS.current(0)
        Answer= tk.Label(signup_root, text="Answer").grid(row=10,column=1, padx=20, pady=10)
        self.Entry_Answer= tk.Entry(signup_root, bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Answer.grid(row=10, column=2, padx=20, pady=10)
        Submit_button=tk.Button(signup_root,text="Sign Up", command= self.connect_database)
        Submit_button.grid(row=11, column=2, padx=20, pady=10)
        back_button=tk.Button(signup_root,text="Already have an account?", bd=0, command=lambda:self.back_to_login(signup_root))
        back_button.grid(row=12, column=2, padx=20, pady=10)
        
        signup_root.mainloop()

    def forgot_window(self):
        self.root.destroy()
        forgot_root=tk.Tk()
        forgot_root.title("Project Management App")
        forgot_root.geometry("720x480")
        tk.Label(text="Forgot Screen", font=("calibre",14,"bold", "italic")).grid(row=1,column=1, padx=10, pady=10)
        Name= tk.Label(forgot_root, text="Name", width=12).grid(row=2,column=1, padx=20, pady=10)
        self.Entry_Name= tk.Entry(forgot_root,)
        self.Entry_Name.grid(row=2, column=2, padx=20, pady=10)
        Email_id= tk.Label(forgot_root, text="Email id").grid(row=3,column=1, padx=20, pady=10)
        self.Entry_Email_id= tk.Entry(forgot_root, bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Email_id.grid(row=3, column=2, padx=20, pady=10)
        Password= tk.Label(forgot_root, text="New Password").grid(row=4,column=1, padx=20, pady=10)
        self.Entry_Password= tk.Entry(forgot_root, show="*")
        self.Entry_Password.grid(row=4, column=2, padx=20, pady=10)
        Confirm_Password= tk.Label(forgot_root, text="Confirm New Password").grid(row=5,column=1, padx=20, pady=10)
        self.Entry_Confirm_Password= tk.Entry(forgot_root, show="*", bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Confirm_Password.grid(row=5, column=2, padx=20, pady=10)
        dob_label = tk.Label(forgot_root, text="D.O.B").grid(row=6, column=1, padx=20, pady=10)
        self.dob_entry = DateEntry(forgot_root, width=12, background='darkblue', foreground='white', borderwidth=2, year=2000, month=1, day=1, date_pattern='y-mm-dd')
        self.dob_entry.grid(row=6, column=2, padx=20, pady=10)
        self.dob_entry.bind("<<DateEntrySelected>>", lambda event: self.calculate_age())
        
        Age_section=tk.Label(forgot_root, text="Your age is").grid(row=7, column=1, padx=20, pady=10)
        self.age_point = tk.Label(forgot_root, text="")
        self.age_point.grid(row=7, column=2, padx=20, pady=10)

        ttk.Label(forgot_root, text="Security Question").grid(row=9,column=1, padx=20, pady=10)
        n= tk.StringVar()
        self.Security_QS= ttk.Combobox(forgot_root, textvariable=n)
        self.Security_QS['values'] = ("Select","Your First Mobile Brand","Your First School Name","Your Favourite Pet Name")
        self.Security_QS.grid(row=9,column=2, padx=20, pady=10)
        self.Security_QS.current(0)
        Answer= tk.Label(forgot_root, text="Answer").grid(row=10,column=1, padx=20, pady=10)
        self.Entry_Answer= tk.Entry(forgot_root, bg="lime", fg="blue", font=("calibre",10,"bold", "italic"))
        self.Entry_Answer.grid(row=10, column=2, padx=20, pady=10)
        Submit_button=tk.Button(forgot_root,text="Reset Password", command=self.forgot)
        Submit_button.grid(row=11, column=2, padx=20, pady=10)
        back_button=tk.Button(forgot_root,text="Go Back to login", command=lambda:self.back_to_login(forgot_root)).grid(row=12, column=2, padx=20, pady=10)
        forgot_root.mainloop()

    def back_to_login(self,current_root):
        current_root.destroy() #This destroys the signup_root as here current_root=signup_root
        main_root = tk.Tk()
        app = App(main_root)
        main_root.mainloop()

    def Entry_clear(self):
        self.Entry_Name.delete(0,tk.END)
        self.Entry_Email_id.delete(0,tk.END)
        self.Entry_Password.delete(0,tk.END)
        self.Entry_Confirm_Password.delete(0,tk.END)
        self.dob_entry.delete(0,tk.END)
        self.age_point.config(text="")
        self.Gender.set("Select")
        self.Security_QS.set("Select")
        self.Entry_Answer.delete(0,tk.END)

<<<<<<< HEAD
=======
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
>>>>>>> origin/main

    def calculate_age(self):
        dob = self.dob_entry.get_date()
        # print(f"Selected DOB: {dob}")  # Debugging line to check DOB
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age>=18:
            self.age_point.config(text=f"{age} years")
        else:
            self.age_point.config(text=str(age))
        self.user_age = age
        # print(f"Calculated Age: {age}")  # Debugging line to check age calculation

    def Name_varify(self, Name):
        if not Name.strip():
            return False
        # return count
        for j in Name:
            if not(j.isalpha() or j.isspace()):
                return False
        return True
    
    def Email_varify(self, Email_id):
        # P1=r'^[a-zA-Z0-9.!#$%&*+-/=?^_{|}~]+$'
        # P2=r'^[a-zA-Z0-9._%+-]+$'
        # P3=r'^[a-zA-Z0-9._%+-]+$'
        # pattern=re.compile
        try:
        # Validate.
            valid = validate_email(Email_id)
            # Update with the normalized form.
            email = valid.email
            return True
        except EmailNotValidError as e:
            # Email is not valid, exception message is human-readable.
            return False
        
    def Password_verify(self, Password):
        has_upper=False
        has_lower=False
        has_digit=False
        has_special=False

        if 12>=len(Password)>=8:
            for i in Password:
                if i.isupper():
                    has_upper = True
                elif i.islower():
                    has_lower = True
                elif i.isdigit():
                    has_digit = True
                else:
                    has_special = True

        if has_upper and has_lower and has_digit and has_special:
            return True
        else:
            return False
        
    def CPassword_verify(self, CPassword, Password):
        if CPassword==Password:
            return True

    
    
    def connect_database(self):
    # print("Working")
        if (self.Entry_Name.get()=="" or self.Entry_Email_id.get()=="" 
            or self.Entry_Password.get()=="" or self.Entry_Confirm_Password.get()=="" or self.Entry_Answer.get()==""):
            messagebox.showerror("Error", "Fill All the fields correctly")
            # print(self.Entry_Name.get())
        elif not (self.Name_varify(self.Entry_Name.get())):
            messagebox.showerror("Error", "Name Field should only have Alphabatical Char")
        elif not (self.Email_varify(self.Entry_Email_id.get())):
            messagebox.showerror("Error", "Enter Valid Email Adress")
        elif not (self.Password_verify(self.Entry_Password.get())):
            messagebox.showerror("Error", "1.Password Length Must have between 8-12 charaters 2.Password must have atleast 1 Capital, 1 Small, 1 Digit & 1 Special Character ")
        elif not (self.CPassword_verify(self.Entry_Confirm_Password.get(),self.Entry_Password.get())):
            messagebox.showerror("Error", "Password & Confirm Password doesn't match")
        elif self.user_age<18:
            messagebox.showerror("Error", "You must be at least 18 years old to register")

        else:
            try:
<<<<<<< HEAD
                Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi")
=======
                Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi", database="todo_list")
                #Use Your LocalDB Login credentials
>>>>>>> origin/main
                MyCursor=Connection_var.cursor()
            except: 
                messagebox.showerror("Error", "Some Error Occured")
                return
            try:
                query="create database userdata"
                MyCursor.execute(query)
                query="use userdata"
                MyCursor.execute(query)
                query="create table data(id int auto_increment primary key not null, Name varchar(50), Email varchar(50), Password varchar (12), DOB varchar(10), Gender varchar(10), Security_Qs varchar (100), Answer varchar(30))"
                MyCursor.execute(query)
            except:
                MyCursor.execute("use userdata")

            query="insert into data(Name, Email, Password, DOB, Gender, Security_Qs, Answer) values(%s, %s, %s, %s, %s, %s, %s)"
            MyCursor.execute(query,(self.Entry_Name.get(), self.Entry_Email_id.get(), self.Entry_Password.get(), self.dob_entry.get_date().strftime('%Y-%m-%d'), self.Gender.get(), self.Security_QS.get(), self.Entry_Answer.get()))
            Connection_var.commit()
            Connection_var.close()
            messagebox.showinfo("Success", "Signup Successful!!")
            self.Entry_clear()
        
    def Login(self):
        # print("working")
        if (self.Entry_Email_id.get()=="" or self.Entry_Password.get()==""): messagebox.showerror("Error", "Fill All the fields correctly")
        else:
            try:
                Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi")
                MyCursor=Connection_var.cursor()
            except: 
                messagebox.showerror("Error", "Some Error Occured")
                return
            query="use userdata"
            MyCursor.execute(query)
            query= "select * from data where Email=%s and Password=%s"
            MyCursor.execute(query,(self.Entry_Email_id.get(), self.Entry_Password.get()))
            row= MyCursor.fetchone()
            if row==None: messagebox.showerror("Error", "Invalid Email or Password")
            else: 
                messagebox.showinfo("Welcome", "Login Successful!!")
                self.root.destroy()

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
                                cursor = connection.cursor()
                                cursor.execute("DELETE FROM data WHERE id = %s", (task_id,))
                                connection.commit()
                                connection.close()
                                self.populate_listbox()
                            else:
                                connection = pymysql.connect(host="localhost", user="root", password="SQL@2022bibhi", database="todo_list")
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

    def forgot(self):
        if (
            self.Entry_Name.get()=="" 
            or self.Entry_Email_id.get()=="" 
            or self.Entry_Password.get()=="" 
            or self.Entry_Confirm_Password.get()=="" 
            or self.dob_entry.get()=="" 
            or self.Security_QS.get()=="" 
            or self.Entry_Answer.get()==""): messagebox.showerror("Error", "Fill All the fields correctly")
        elif not (self.Password_verify(self.Entry_Password.get())):
            messagebox.showerror("Error", "1.Password Length Must have between 8-12 charaters 2.Password must have atleast 1 Capital, 1 Small, 1 Digit & 1 Special Character ")
        elif not (self.CPassword_verify(self.Entry_Confirm_Password.get(),self.Entry_Password.get())):
            messagebox.showerror("Error", "New Password & Confirm New Password doesn't match")
        else:
            try:
                Connection_var=pymysql.connect(host="localhost", user= "root", password= "SQL@2022bibhi")
                MyCursor=Connection_var.cursor()
            except: 
                messagebox.showerror("Error", "Some Error Occured")
                return
            query="use userdata"
            MyCursor.execute(query)
            query= "select * from data where Name=%s and Email=%s and DOB=%s and Security_Qs=%s and Answer=%s"
            MyCursor.execute(query, (self.Entry_Name.get(), self.Entry_Email_id.get(), self.dob_entry.get_date().strftime('%Y-%m-%d'), self.Security_QS.get(), self.Entry_Answer.get()))
            row= MyCursor.fetchone()
            if row==None: messagebox.showerror("Error", "User Doesn't Exist in databse")
            else: 
                query= "update data set Password=%s where Name=%s and Email=%s and DOB=%s and Security_Qs=%s and Answer=%s"
                MyCursor.execute(query, (self.Entry_Password.get(), self.Entry_Name.get(), self.Entry_Email_id.get(), self.dob_entry.get_date().strftime('%Y-%m-%d'), self.Security_QS.get(), self.Entry_Answer.get()))
                Connection_var.commit()
                Connection_var.close()
<<<<<<< HEAD
                messagebox.showinfo("Welcome", "Password reset Successful, please login with new password")
                self.window.destroy()
=======
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
>>>>>>> origin/main


if __name__ == "__main__":
    login_root = tk.Tk()
    app = App(login_root)
    login_root.mainloop()