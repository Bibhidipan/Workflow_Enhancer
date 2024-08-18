import flet as ft
import datetime
import psycopg2
from psycopg2 import sql
import math

def PopUp(page, title, message):
    def ClosePopUp(e):
        page.dialog.open = False
        page.update()
    Dialogue = ft.AlertDialog(
        title=ft.Text(title), 
        content=ft.Text(message), 
        actions=[ft.TextButton("Ok", on_click=ClosePopUp)])
    page.dialog = Dialogue
    page.dialog.open = True
    page.update()

def Databse_Connection():
    return psycopg2.connect(
            dbname="YourDBName", 
            user= "Yourdb_owner", 
            password= "Your Password", 
            host="Your host", 
            port="5432")
#I have used Neondb

def Create_Database():
    try:
        connection = psycopg2.connect(
            dbname="YourDBName", 
            user= "Yourdb_owner", 
            password= "Your Password", 
            host="Your host", 
            port="5432")
        
        cursor = connection.cursor()
        cursor.execute("create table if not exists data(id SERIAL PRIMARY KEY, Task TEXT, Priority TEXT, Target_Date DATE, Status TEXT)")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Database creation failed: {e}")

class ToDo_APP:
    def __init__(self, page):
        self.page = page
        self.page.title = "The Workflow Enhancer"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_height = 800
        self.page.window_width = 400
        self.page.window_resizable = False
        self.page.theme_mode = "dark"
        # background_image = ft.Image(
        #     src="C:/Users/bibhi/Desktop/Project_Venv/Project_management_app/APPBG.jpg", 
        #     width=400, 
        #     height=800, 
        #     fit=ft.ImageFit.COVER
        # )   
        
        self.Task = ft.TextField(hint_text="Enter The Task", text_align="Left", width=380)
        self.Priority = ft.Dropdown(hint_text="Priority", 
                                    width=100, 
                                    options=[ft.dropdown.Option("High"), 
                                    ft.dropdown.Option("Medium"), 
                                    ft.dropdown.Option("Low")])

        def Date_Select(e):
            self.DateSelect.value = e.control.value.strftime('%Y-%m-%d')
            self.DateSelect.text = self.DateSelect.value
            self.DateSelect.update()

        def open_date_picker(e):
            date_picker = ft.DatePicker(value=datetime.datetime.now(),on_change=Date_Select)
            self.page.dialog = date_picker
            self.page.dialog.open = True
            self.page.update()

        self.DateSelect = ft.ElevatedButton(text="Target Date", icon=ft.icons.CALENDAR_MONTH, on_click=open_date_picker)

        page.add(self.Task, 
                ft.Row([
                    self.Priority, 
                    self.DateSelect, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.Add_Task)]))

        self.TabProperties = ft.Tabs(selected_index=0, animation_duration=300, divider_height=0, indicator_padding=0, scrollable=True,
            tabs=[
                ft.Tab(text="Pending", icon=ft.icons.DENSITY_SMALL, content=ft.ListView(expand=True, spacing=10, padding=10)),
                ft.Tab(text="Ongoing", icon=ft.icons.PENDING_ACTIONS, content=ft.ListView(expand=True, spacing=10, padding=10)),
                ft.Tab(text="Completed", icon=ft.icons.DONE_ALL, content=ft.ListView(expand=True, spacing=10, padding=10))
            ], expand=1
        )

        self.page.add(self.TabProperties)
        self.load_tasks()

    def Add_Task(self, e):
        if not self.Task.value or not self.Priority.value or self.DateSelect.value == "Target Date":
            PopUp(self.page, "Error", "Please Fill All the fields Correctly")
            return
        try:
            Connection_Var = Databse_Connection()
            MyCursor = Connection_Var.cursor()
            MyCursor.execute("INSERT INTO data (Task, Priority, Target_Date, Status) VALUES (%s, %s, %s, %s)",
                            (self.Task.value, self.Priority.value, self.DateSelect.value, "Pending"))
            Connection_Var.commit()
            MyCursor.close()
            Connection_Var.close()
            PopUp(self.page, "Success", "Task Added Successfully")
            self.clear_inputs()
            self.load_tasks()
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to add Task {e}")

    def clear_inputs(self):
        self.Task.value = ""
        self.Priority.value = None
        self.DateSelect.text = "Target Date"
        self.Task.focus()
        self.Task.update()
        self.DateSelect.update()
        self.page.update()

    def load_tasks(self):
        tasks = self.fetch_data()
        pending_tasks = [task for task in tasks if task[4] == "Pending"]
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
                gradient_colors = ["0xff1f005c", "0xff5b0060", "0xff870160", "0xffac255e", "0xffca485c", "0xffe16b5c", "0xfff39060", "0xffffb56b"]
            elif Status == "Ongoing":
                gradient_colors = ["#2707f5", "#2f17cf", "#3422a8", "#332687", "#261e57", "#1a1533", "#0a0912"]
            elif Status == "Completed":
                gradient_colors = ["#02f775", "#13d16c", "#1ab060", "#1f9456", "#1f7346", "#1d5738", "#163826", "#0c1a12", "#050a07"]
            else:  # Default gradient if Status is unknown or "Delete"
                gradient_colors = ["#808080", "#a9a9a9"]

            if Status == "Pending":
                card_opacity = 1.0  # Fully opaque
            elif Status == "Ongoing":
                card_opacity = 0.8  # Slightly transparent
            elif Status == "Completed":
                card_opacity = 0.6  
            
            # Create a card for each task
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
                    padding=10,  # Apply padding here
                    width=380,
                    border_radius=10  # Slightly less than the card's width to accommodate padding
                ),
                elevation=2,
                width=400,
                opacity=card_opacity
            )

            tab_content.controls.append(task_card)

        tab_content.update()


    def Update_Task_Status(self, task_id, new_Status):
        try:
            if new_Status == "Delete":
                connection = Databse_Connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM data WHERE id = %s", (task_id,))
                connection.commit()
                connection.close()
                self.load_tasks()
            else:
                Connection_var = Databse_Connection()
                MyCursor = Connection_var.cursor()
                MyCursor.execute("UPDATE data SET Status = %s WHERE id = %s", (new_Status, task_id))
                Connection_var.commit()
                MyCursor.close()
                Connection_var.close()
                self.load_tasks()
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to update task Status: {e}")

    def fetch_task_id(self, task_label):
        try:
            Connection_var = Databse_Connection()
            MyCursor = Connection_var.cursor()
            MyCursor.execute("SELECT id FROM data WHERE Task = %s", (task_label,))
            task_id = MyCursor.fetchone()
            MyCursor.close()
            Connection_var.close()
            return task_id[0] if task_id else None
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to fetch task ID: {e}")
            return None

    def fetch_data(self):
        try:
            Connection_Var = Databse_Connection()
            MyCursor = Connection_Var.cursor()
            MyCursor.execute("SELECT id, Task, Priority, Target_Date, Status from data")
            Rows = MyCursor.fetchall()
            Priority_Level = {"High": 1, "Medium": 2, "Low": 3}
            Sorted_Rows = sorted(Rows, key=lambda DBColumn: (DBColumn[3], Priority_Level.get(DBColumn[2], 4)))
            MyCursor.close()
            Connection_Var.close()
            return Sorted_Rows
        except Exception as e:
            PopUp(self.page, "Error", f"Failed to fetch Tasks {e}")

    def Create_data(self):
        try:
            Connection_Var = Databse_Connection()
            MyCursor = Connection_Var.cursor()
            MyCursor.execute("create table if not exists data(id SERIAL PRIMARY KEY, Task TEXT, Priority TEXT, Target_Date DATE, status TEXT)")
            Connection_Var.close()
        except Exception as e:
            PopUp(self.page, "Error", f"Database Creation Failed {e}")

def main(page: ft.Page):
    Create_Database()
    app = ToDo_APP(page)
    app.Create_data()

ft.app(target=main)
