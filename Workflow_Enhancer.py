# To run the app locally, flet & psycopg2 to be installed in your virtual environment 
# Run pip install flet from terminal
# Run pip install psycopgp2 in terminal
# Run pip install email validator in terminal
from flet import* 
import flet as ft
import datetime
import psycopg2
from email_validator import validate_email, EmailNotValidError 
import math


def Heading(page, value): #A Heading function for the pages headings
    # page.fonts = {
        # "CustomFont": r"C:\Users\AppData\Local\Microsoft\Windows\Fonts\The Friday St
        return ft.Text(
            value=value, 
            color=ft.colors.BROWN_200, 
            text_align=ft.TextAlign.CENTER,
            # font_family="CustomFont",
            size=40, 
            weight=ft.FontWeight.BOLD, 
            italic=False
        )

def Gradient_Background(): # A Function to add similar gradient background to all the pages
    AccentColour = ["#0582f0","#2509b0","#4c09b0","#8a05f0","#8309b0","#551d80","#2c0f42"]
    AccentColour1=["#0582f0","#2509b0","#4c09b0","#8a05f0","#8309b0",]
    return ft.Container(
            gradient=ft.RadialGradient(
                center=ft.Alignment(0, -1.25),
                radius=1.4,
                colors= AccentColour1
            ),
            padding=10,
            margin=0,
            expand=True
        )

def InputField(hint_text, IsPassword=False, width=None): # A Function to create custom text widget
    text_field = ft.TextField(
        hint_text=hint_text,
        text_style=ft.TextStyle(color="a0cafd"),
        text_align="Left",
        color="a0cafd",
        border_color=ft.colors.TRANSPARENT,
        width=width,
        password=IsPassword
    )
    container = ft.Container(
        content=text_field,
        border=ft.Border(bottom=ft.BorderSide(1, ft.colors.WHITE)),
        border_radius=ft.border_radius.all(0),
        padding=ft.padding.only(bottom=2), expand= False
    )
    return container, text_field

def DateSelector(page, text, elevation=None): # A Function to create custom date selector widget
    def Date_Select(e):
            DateSelect.value = e.control.value.strftime('%Y-%m-%d')
            DateSelect.text = DateSelect.value
            DateSelect.update()

    def open_date_picker(e):
        date_picker = ft.DatePicker(value=datetime.datetime.now(), 
                                    on_change=Date_Select)
        page.dialog = date_picker
        page.dialog.open = True
        page.update()
        
    DateSelect=ft.ElevatedButton(text=text, 
                                icon=ft.icons.CALENDAR_MONTH, 
                                on_click=open_date_picker, 
                                bgcolor=ft.colors.TRANSPARENT, 
                                elevation=elevation)    
    return DateSelect

def DropDown(hint, width=None, icon=None, Option1=None, Option2=None, Option3=None): # A Function to create custom Dropdown widget
    return ft.Dropdown(hint_text=hint, width=width, prefix_icon=icon,
            options=[
                ft.dropdown.Option(Option1),
                ft.dropdown.Option(Option2),
                ft.dropdown.Option(Option3),
            ],
            filled=None,
                border_color=ft.colors.TRANSPARENT,
                hint_style=ft.TextStyle(color="a0cafd"),
                text_style=ft.TextStyle(color=ft.colors.BROWN_200, weight=ft.FontWeight.BOLD), 
        )

def PopUp(page, title, message): # A Function to create custom pop up message
    def ClosePopUp(e):
        if page is not None:  # Checking if page exists before using it
            page.dialog.open = False
            page.update()
    if page is not None:  # Checking if page exists before creating the dialog
        Dialogue = ft.AlertDialog( 
        title=ft.Text(title), 
        content=ft.Text(message), 
        actions=[ft.TextButton("Ok", on_click=ClosePopUp)])
        page.dialog = Dialogue
        page.dialog.open = True
        page.update()

def Database_Connection(): # A Function to declare Databse Connection Parameters
    return psycopg2.connect(
        dbname="Yourdb", 
        user="Yourdb_owner", 
        password="Your Password",
        host="your Host", 
        port="5432"
    )
#I have used Neondb

def Create_User_Table(): # A Function to create the Users Details Table
    try:
        connection = Database_Connection()
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL, 
                        password VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        dob DATE,
                        security_qs VARCHAR(255),
                        answer VARCHAR(255),
                        designation VARCHAR(100))""")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        PopUp(page=None, title="Error", message="Database creation failed due to: {e}")

def Create_Task_Table(): # A Function to create the Tasks Details Table
    try:
        connection = Database_Connection()
        cursor = connection.cursor()
        cursor.execute("""create table if not exists tasks_list(
            id SERIAL PRIMARY KEY, 
            Task TEXT, Priority TEXT, 
            Target_Date DATE, Status TEXT, 
            user_id INTEGER REFERENCES users(id))""")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        PopUp(page=None, title="Error", message="Database creation failed due to: {e}") 



class Workflow_Enhancer_APP:
    def __init__(self, page, user_id):
        self.page = page
        self.user_id = user_id
        self.search_query="" #Initial Query for search tab is null
        Create_Task_Table() #Initiating table creation to store the tasks
        self.page.title = "The Workflow Enhancer"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_height = 712
        self.page.window_width = 400
        self.page.window_resizable = True #allows to resize the app as per user prference
        self.page.padding = 0 #to ensure the background container fits the total avalable space for the app
        self.page.theme_mode = "dark"

        Background = Gradient_Background()

        Task_container, self.Task = InputField("Enter The Task...")

        self.Priority= DropDown(hint="Priority", 
                                Option1="High", 
                                Option2="Medium", 
                                Option3="Low", 
                                icon=ft.icons.PRIORITY_HIGH , 
                                width=150)

        self.TabProperties = ft.Tabs(
            selected_index=0, #The first Tab stays selected
            animation_duration=300, 
            divider_height=0, 
            indicator_padding=0, 
            scrollable=True,
            tabs=[
                ft.Tab(text="Pending", icon=ft.icons.DENSITY_SMALL, content=ft.ListView(expand=True, spacing=10, padding=10)),
                ft.Tab(text="Ongoing", icon=ft.icons.PENDING_ACTIONS, content=ft.ListView(expand=True, spacing=10, padding=10)),
                ft.Tab(text="Completed", icon=ft.icons.DONE_ALL, content=ft.ListView(expand=True, spacing=10, padding=10))
            ], 
            expand=True
        )
        
        self.DateSelect= DateSelector(self.page, text="Target Date", elevation=0)

        self.Back_Button= ft.IconButton(icon=ft.icons.LOGOUT, on_click= self.Back_To_Login, bgcolor=ft.colors.TRANSPARENT)

        self.search_input = ft.TextField(
            hint_text="Search Tasks...",
            on_change=self.update_search_query,
            width=200,
            prefix_icon=ft.icons.SEARCH,
            border_color=ft.colors.TRANSPARENT,
        )

        page.add(ft.Stack(controls=[ #Stack is used to put items into layers
            Background,
            ft.Column(controls=[ #Controls added into colums to set there positions or display properties togather
                ft.Container(content=ft.Column(controls=[
                    ft.Row(controls=[
                        Task_container,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, 
                            on_click=self.Add_Task, 
                            bgcolor=ft.colors.TRANSPARENT, 
                            elevation=0)], 
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ft.Row(controls=[self.Priority, self.DateSelect],alignment=ft.MainAxisAlignment.CENTER)],
                alignment=ft.MainAxisAlignment.START,
                spacing=10),
                padding=ft.padding.all(10),
                margin=0,
                alignment=ft.alignment.top_center),
                ft.Container(content=self.TabProperties, expand=True, padding=ft.padding.all(10), margin=0),
                ft.Container(content=ft.Column(controls=[
                    ft.Row(controls=[self.search_input, self.Back_Button], alignment=ft.MainAxisAlignment.CENTER, spacing= 100)])),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=0)
        ],
        expand=True)
        )
        self.load_tasks() #Ffter adding elements to the page the already existing tasks to be loaded in the User Interface

    def clear_inputs(self): #Inputs to be cleared after each task addition and the page to be updated
        self.Task.value = ""
        self.Priority.value = None
        self.DateSelect.text = "Target Date"
        self.Task.focus()
        self.Task.update()
        self.DateSelect.update()
        self.page.update()

    def update_search_query(self, e):
        self.search_query = e.control.value.lower()  # Update the search query with the user's input
        self.load_tasks()

    def Add_Task(self, e):  #Function to add tasks into the Tasks table 
        task_value = self.Task.value if self.Task.value else ""
        priority_value = self.Priority.value
        date_value = self.DateSelect.text if self.DateSelect.text != "Target Date" else ""

        if task_value=="" or priority_value=="" or date_value=="":
            PopUp(self.page, "Error", "Please Fill All the fields Correctly")
            return
        try:
            Connection_Var = Database_Connection()
            Cursor = Connection_Var.cursor()
            Cursor.execute("INSERT INTO tasks_list(task, priority, target_date, status, user_id) VALUES (%s, %s, %s, %s, %s)",
                        (task_value, priority_value, date_value, "Pending", self.user_id)) #user_id to be fetched during login
            Connection_Var.commit()
            Cursor.close()
            Connection_Var.close()
            PopUp(self.page, "Success", "Task Added Successfully")
            self.clear_inputs()
            self.load_tasks()
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to add Task {e}")

    def fetch_data(self):
        try:
            Connection_Var = Database_Connection()
            Cursor = Connection_Var.cursor()
            Cursor.execute("SELECT id, task, priority, target_date, status FROM tasks_list WHERE user_id = %s", (self.user_id,))
            Rows = Cursor.fetchall()
            Priority_Level = {"High": 1, "Medium": 2, "Low": 3}
            Sorted_Rows = sorted(Rows, key=lambda DBColumn: (DBColumn[3], Priority_Level.get(DBColumn[2], 4))) 
            #First the tasks to to be fetched as per the sequence of its Target Date, then Priority for the same to be checked for tasks stacking sorting
            # The task which has the earliest target date will be stacked at the top
            # Then priorirty of it to be chcked to  
            Cursor.close()
            Connection_Var.close()
            if self.search_query:  # If there is a search query, filter the tasks
                Sorted_Rows = [row for row in Sorted_Rows if self.search_query in row[1].lower()]
            return Sorted_Rows
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to fetch the Tasks {e}")

    def Update_Task_Status(self, task_id, new_Status):
        try:
            if new_Status == "Delete":
                connection = Database_Connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tasks_list WHERE id = %s", (task_id,))
                connection.commit()
                connection.close()
                self.load_tasks()
            else:
                Connection_var = Database_Connection()
                Cursor = Connection_var.cursor()
                Cursor.execute("UPDATE tasks_list SET Status = %s WHERE id = %s", (new_Status, task_id))
                Connection_var.commit()
                Cursor.close()
                Connection_var.close()
                self.load_tasks()
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to update task Status: {e}")

    def load_tasks(self):
        tasks = self.fetch_data()
        pending_tasks = [task for task in tasks if task[4] == "Pending"] #task[4]=Status which is the primary condition to store the the different type of tasks
        ongoing_tasks = [task for task in tasks if task[4] == "Ongoing"]
        completed_tasks = [task for task in tasks if task[4] == "Completed"]
        self.update_tab_content(0, pending_tasks)
        self.update_tab_content(1, ongoing_tasks)
        self.update_tab_content(2, completed_tasks)

    def update_tab_content(self, tab_index, tasks):
        tab_content = self.TabProperties.tabs[tab_index].content

        tab_content.controls.clear()
        for task in tasks:
            task_id, Task, Priority, DateSelect, Status = task

            if Status == "Pending":
                gradient_colors = ["0xff1f005c", "0xff5b0060", "0xff870160", "0xffac255e", "0xffca485c", "0xffe16b5c", "0xfff39060", "#f79f5c"]
            elif Status == "Ongoing":
                gradient_colors = ["#2707f5", "#2f17cf", "#3422a8", "#332687", "#261e57", "#1a1533", "#0a0912"]
            elif Status == "Completed":
                gradient_colors = ["#04662e", "#1f9456", "#1f7346", "#1d5738", "#163826"]

            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Task: {Task}", size=16, weight="bold", text_align="start"),
                            ft.Row([
                                ft.Text(f"Priority: {Priority}", size=14, text_align="start"),
                                ft.Dropdown(
                                    width=120,
                                    value=Status,
                                    options=[
                                        ft.dropdown.Option("Pending"),
                                        ft.dropdown.Option("Ongoing"),
                                        ft.dropdown.Option("Completed"),
                                        ft.dropdown.Option("Delete")
                                    ], border_radius=30, filled=False, border_color=ft.colors.TRANSPARENT, 
                                    on_change=lambda e, task_id=task_id: self.Update_Task_Status(task_id, e.control.value)
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.MainAxisAlignment.CENTER),
                            ft.Text(f"Target Date: {DateSelect}", text_align="start"),
                        ],
                        spacing=2
                    ), 
                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.Alignment(0.8, 1),
                    colors=gradient_colors,
                    tile_mode=ft.GradientTileMode.MIRROR,rotation=math.pi / 3,),
                    padding=10, 
                    width=380,
                    border_radius=10  # Slightly less than the card's width to accommodate padding
                ),
                elevation=2,
                width=400,
            )
            tab_content.controls.append(task_card)
        tab_content.update()

    def Back_To_Login(self, e):
        self.page.clean() 
        Authentication_Page(self.page)

def main(page: ft.Page):
    Create_Task_Table()
    app = Workflow_Enhancer_APP(page)


class Authentication_Page: # A class which includes all the USer Registration, Authentication, Data_Modification  Pages and relevent functions to them
    def __init__(self, page):
        self.page = page
        Create_User_Table() # User Details Table Initiated
        page.window.height = 667
        page.window.width = 375
        self.Login_Page(page)
        self.page.window_resizable = True
        self.page.padding=0
        self.page.theme_mode = "dark"

    def Login_Page(self, page):
        self.page.title= "The Workflow Enhancer"
        self.Page_Heading = Heading(self.page,"Welcome!!")
        self.page.padding=0
        self.page.theme_mode = "dark"

        Background= Gradient_Background()
        Email_container, self.Email = InputField("Email", width=290)
        Password_container, self.Password = InputField("Password", width=290, IsPassword=True)
        self.Login_Button = ft.ElevatedButton("Login", on_click=self.Login, icon=ft.icons.LOGIN, bgcolor=ft.colors.TRANSPARENT)
        self.Forgot_Password_Button = ft.TextButton("Forgot Password?", on_click=self.ToForgotPassword)
        self.SignUp_Button = ft.TextButton("Don't have an account?", on_click=self.ToSignUp)
        
        Main_Container=ft.Container(content=ft.Stack(controls=[
            Background,
            ft.Container(content=ft.Column(controls=[
            ft.Row([self.Page_Heading], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([Email_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([Password_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.Login_Button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.Forgot_Password_Button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.SignUp_Button], alignment=ft.MainAxisAlignment.CENTER)]), 
                                padding=ft.padding.all(35),
                                margin=0,
                                alignment=ft.alignment.top_center,)]), expand=True)
        page.add(Main_Container)

    def ForgotPassWordPage(self, page):
        self.page.title= "The Workflow Enhancer"
        self.Page_Heading = Heading(self.page,"Reset Password")
        self.page.padding=0
        self.page.theme_mode = "dark"

        Background= Gradient_Background()

        Username_container, self.Username =  InputField("Username/Name", width=290)
        Email_container, self.Email = InputField("Email", width=290)
        Password_container, self.Password = InputField("Password", width=290, IsPassword=True)
        ConfirmPassword_container, self.ConfirmPassword = InputField("Confirm Password", width=290, IsPassword=True)

        self.DateSelect= DateSelector(page, "D.O.B")

        self.SecurityQS = DropDown(hint="Choose The Security Question", 
                                    width=270, Option1="Your First Mobile Brand", 
                                    Option2="Your First School Name", 
                                    Option3= "Your Favourite Pet Name")

        Answer_container, self.Answer = InputField("Answer", width=290)

        self.Reset_Password_Button = ft.ElevatedButton("Reset Password", on_click=self.Reset_Password, bgcolor=ft.colors.TRANSPARENT)
        self.BackToLogin_Button = ft.ElevatedButton("Back To Login", on_click=self.BackToLogin, bgcolor=ft.colors.TRANSPARENT)

        Main_Container=ft.Container(content=ft.Stack(controls=[
            Background,
            ft.Container(content=ft.Column(controls=[
            ft.Row([self.Page_Heading], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([Username_container], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([Email_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([Password_container], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([ConfirmPassword_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.DateSelect], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.SecurityQS], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([Answer_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.Reset_Password_Button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.BackToLogin_Button], alignment=ft.MainAxisAlignment.CENTER)
            ]), padding=ft.padding.all(30),
                margin=0,
                alignment=ft.alignment.top_center,)]), expand=True)
        page.add(Main_Container)

    def SignUpPage(self, page):
        self.page.title= "The Workflow Enhancer"
        self.Page_Heading = Heading(self.page,"Sign Up!")
        self.page.padding=0
        self.page.theme_mode = "dark"

        Background= Gradient_Background()

        Username_container, self.Username =  InputField("Username/Name", width=290)
        Email_container, self.Email = InputField("Email", width=290)
        Password_container, self.Password = InputField("Password", width=290, IsPassword=True)
        ConfirmPassword_container, self.ConfirmPassword = InputField("Confirm Password", width=290, IsPassword=True)

        self.DateSelect= DateSelector(page, "D.O.B")

        self.SecurityQS = DropDown(hint="Choose The Security Question", 
                                    width=270, Option1="Your First Mobile Brand", 
                                    Option2="Your First School Name", 
                                    Option3= "Your Favourite Pet Name")

        Answer_container, self.Answer = InputField("Answer", width=290)
        
        self.Designation = ft.Dropdown(hint_text="Choose Your Position",
            options=[
                ft.dropdown.Option("Cheif"),
                ft.dropdown.Option("Head"),
                ft.dropdown.Option("Senior Manager"),
                ft.dropdown.Option("Manager"),
                ft.dropdown.Option("Asst. Manager"),
            ],
            filled=None,
                    border_color=ft.colors.TRANSPARENT,
                    hint_style=ft.TextStyle(color="a0cafd"),
                    text_style=ft.TextStyle(color=ft.colors.BROWN_200, weight=ft.FontWeight.BOLD),
        )

        self.SignUp_Button = ft.ElevatedButton("SignUp", on_click=self.SignUp, bgcolor=ft.colors.TRANSPARENT)
        self.BackToLogin_Button = ft.ElevatedButton("Back To Login", on_click=self.BackToLogin, bgcolor=ft.colors.TRANSPARENT)

        Main_Container=ft.Container(content=ft.Stack(controls=[
            Background,
            ft.Container(content=ft.Column(controls=[
            ft.Row([self.Page_Heading], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([Username_container], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([Email_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([Password_container], alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row([ConfirmPassword_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.DateSelect], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.SecurityQS], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([Answer_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.Designation], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.SignUp_Button, self.BackToLogin_Button],alignment=ft.MainAxisAlignment.CENTER)
            ]), 
            padding=ft.padding.all(30),
            margin=0,
            alignment=ft.alignment.top_center
            )
            ]),expand=True)
        page.add(Main_Container)

    def ToForgotPassword(self, e):
        self.page.clean()
        self.ForgotPassWordPage(self.page)

    def ToSignUp(self, e):
        self.page.clean()
        self.SignUpPage(self.page)

    def BackToLogin(self, e):
        self.page.clean()
        self.Login_Page(self.page)

    def calculate_age(self, dob_str):
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age >= 18:
            return True
        return False

    def Name_verify(self, Username):
        if not Username.strip():
            return False
        for j in Username:
            if not (j.isalpha() or j.isalnum() or j.isspace()):
                return False
        return True

    def Email_verify(self, Email):
        try:
            valid = validate_email(Email)
            email = valid.email
            return True
        except EmailNotValidError as e:
            return False

    def Password_verify(self, Password):
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        if 12 >= len(Password) >= 8:
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
        return False

    def CPassword_verify(self, ConfirmPassword, Password):
        if ConfirmPassword == Password:
            return True
        return False

    def Entry_clear(self):
        self.Username.value = ""
        self.Email.value = ""
        self.Password.value = ""
        self.ConfirmPassword.value = ""
        self.DateSelect.text = "D.O.B"
        self.SecurityQS.value = ""
        self.Answer.value = ""
        self.Username.update()
        self.Email.update()
        self.Password.update()
        self.ConfirmPassword.update()
        self.DateSelect.update()
        self.SecurityQS.update()
        self.Answer.update()

    def SignUp(self, e):    
        if (self.Username.value == "" 
            or self.Email.value == "" 
            or self.Password.value == "" 
            or self.ConfirmPassword.value == "" 
            or self.DateSelect.value == ""
            or self.SecurityQS.value == ""
            or self.Answer.value == ""
            or self.Designation.value == ""
        ):
            PopUp(self.page, "Error", "Fill All the fields correctly")

        elif not self.Name_verify(self.Username.value):
            PopUp(self.page, "Error","Username/Name Field should only have Alphanumerical Characters")
        elif not self.Email_verify(self.Email.value):
            PopUp(self.page,"Error","Enter Valid Email Address")
        elif not self.Password_verify(self.Password.value):
            PopUp(self.page, "Error",
                """1.Password Length Must be between 8-12 characters, 
                2.Password must have at least 1 Capital, 1 Small, 1 Digit & 1 Special Character""")
        elif not self.CPassword_verify(self.ConfirmPassword.value, self.Password.value):
            PopUp(self.page,"Error","Password & Confirm Password don't match")
        elif not self.calculate_age(self.DateSelect.text):
            PopUp(self.page, "Error", "You must be at least 18 years old to register")
        else:
            try:
                Connection_var = Database_Connection()
                Cursor = Connection_var.cursor()

            except Exception as e:
                PopUp(self.page, "Error", "Some Error Occurred")
                return
            try:
                query="INSERT INTO users(username, password, email, dob, security_qs, answer, designation) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                Parameters=(
                    self.Username.value,
                    self.Password.value,
                    self.Email.value, 
                    self.DateSelect.text, 
                    self.SecurityQS.value, 
                    self.Answer.value,
                    self.Designation.value
                    )
                Cursor.execute(query, Parameters)
                Connection_var.commit()
                Cursor.close()
                Connection_var.close()
                PopUp(self.page, "Success", "Signup Successful!!")
                self.Entry_clear()
            except Exception as e:
                PopUp(self.page, "Error", f"Error {e} Occurred During Data Insertion")

    def Reset_Password(self, e):
        if (self.Username.value == "" 
            or self.Email.value == "" 
            or self.Password.value == "" 
            or self.ConfirmPassword.value == "" 
            or self.DateSelect.value == ""
            or self.Answer.value == ""
        ):PopUp(self.page, "Error", "Fill All the fields correctly")

        elif not self.Name_verify(self.Username.value):
            PopUp(self.page, "Error", "Username/Name Field should only have Alphanumerical Characters")
        elif not self.Email_verify(self.Email.value):
            PopUp(self.page, "Error", "Enter Valid Email Address")
        elif not self.Password_verify(self.Password.value):
            PopUp(self.page, "Error",
                "1. Password Length Must be between 8-12 characters, 2. Password must have at least 1 Capital, 1 Small, 1 Digit & 1 Special Character")
        elif not self.CPassword_verify(self.ConfirmPassword.value, self.Password.value):
            PopUp(self.page, "Error", "Password & Confirm Password don't match")
        elif not self.calculate_age(self.DateSelect.text):
            PopUp(self.page, "Error", "Userdata not registered")
        else:
            try:
                Connection_var = Database_Connection()
                Cursor = Connection_var.cursor()
            except Exception as e:
                PopUp(self.page, "Error", "Some Error Occurred during Database connection")
                return

            query = """
                SELECT * FROM users
                WHERE username = %s 
                AND email = %s 
                AND dob = %s 
                AND security_qs = %s 
                AND answer = %s
            """
            Cursor.execute(query, (
                self.Username.value, 
                self.Email.value, 
                self.DateSelect.text, 
                self.SecurityQS.value,
                self. Answer.value
            ))
            row = Cursor.fetchone()
            if row is None:
                PopUp(self.page, "Error", "User Doesn't Exist in database")
            else:
                query = """
                    UPDATE users
                    SET password = %s 
                    WHERE username = %s 
                    AND email = %s 
                    AND dob = %s 
                    AND security_qs = %s 
                    AND answer = %s
                """ #Updates the password if all other fields match with the database
                Cursor.execute(query, (
                    self.Password.value,
                    self.Username.value, 
                    self.Email.value, 
                    self.DateSelect.text, 
                    self.SecurityQS.value, 
                    self.Answer.value,
                ))
                Connection_var.commit()
                Connection_var.close()
                PopUp(self.page, "Welcome", "Password reset Successful, please login with new password")
                self.Entry_clear()

    def Login(self, e):
        if (self.Email.value=="" or self.Password.value==""): PopUp(self.page, "Error", "Fill All the fields correctly")
        else:
            try:
                Connection_var=Database_Connection()
                Cursor= Connection_var.cursor()
            except: 
                PopUp(self.page, "Error", "Some Error Occured")
                return
            query="SELECT id FROM users WHERE Email = %s AND Password = %s" #selecting id to fetch data relevenet to the specific id only
            Parameter=(self.Email.value, self.Password.value)
            Cursor.execute(query, Parameter)
            user_id= Cursor.fetchone()
            Cursor.close()
            Connection_var.close()
            if user_id==None: PopUp(self.page, "Error", "Invalid Email or Password")
            else: 
                PopUp(self.page,"Welcome!", "Login Successful!!")
                self.page.clean()
                Workflow_Enhancer_APP(self.page, user_id)

def main(page: ft.Page):
    Create_Task_Table()
    Authentication_Page(page)

ft.app(target=main)