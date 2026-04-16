import wx
import wx.lib.buttons as buttons
from datetime import datetime

# --- CONFIGURATION (THEME) ---
THEME = {
    'bg_dark': '#1E1E1E',       
    'bg_panel': '#2D2D30',      
    'text': '#FFFFFF',          
    'accent': '#4EC9B0',        
    'accent_secondary': '#D16D9E', 
    'button_bg': '#007ACC',     
    'button_fg': '#FFFFFF',     
    'timer_text': '#FFD700',    
    'input_bg': '#3E3E42',      
    'input_fg': '#FFFFFF'       
}

class StyledFrame(wx.Frame):
    """A base frame that sets up the dark theme automatically"""
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        self.SetBackgroundColour(THEME['bg_dark'])
        
    def setup_panel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(THEME['bg_panel'])
        return panel

    def create_header(self, parent, text, size=14, color=THEME['accent']):
        lbl = wx.StaticText(parent, label=text)
        font = lbl.GetFont()
        font.PointSize = size
        font.MakeBold()
        lbl.SetFont(font)
        lbl.SetForegroundColour(color)
        return lbl

    def create_text(self, parent, text):
        lbl = wx.StaticText(parent, label=text)
        lbl.SetForegroundColour(THEME['text'])
        return lbl
    
    def create_input(self, parent, value=""):
        txt = wx.TextCtrl(parent, value=value)
        txt.SetBackgroundColour(THEME['input_bg'])
        txt.SetForegroundColour(THEME['input_fg'])
        return txt
    
    def create_button(self, parent, label, func, bg_color=THEME['button_bg']):
        btn = wx.Button(parent, label=label)
        btn.SetBackgroundColour(bg_color)
        btn.SetForegroundColour(THEME['button_fg'])
        btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.Bind(wx.EVT_BUTTON, func)
        return btn

class MenuFrame(StyledFrame):
    def __init__(self):
        super().__init__(None, title="UNIMATE - Dashboard", size=(420, 600)) 
        panel = self.setup_panel()
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- DASHBOARD HEADER ---
        header = self.create_header(panel, "UNIMATE", size=24)
        sub_header = self.create_text(panel, "Integrated Productivity Environment")
        
        sizer.Add(header, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        sizer.Add(sub_header, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        # --- INTERACTIVE GOAL MANAGER ---
        box = wx.StaticBox(panel, label="  My Goals  ")
        box.SetForegroundColour(THEME['accent'])
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # List of goals
        self.goal_list = wx.ListBox(panel, size=(-1, 80)) 
        self.goal_list.SetBackgroundColour(THEME['input_bg'])
        self.goal_list.SetForegroundColour(THEME['text'])
        self.goal_list.Append("Finish Semester 1 with > 8.5 CGPA") 
        
        box_sizer.Add(self.goal_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Input row
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.goal_input = self.create_input(panel, "New Goal...")
        
        # Small buttons for Add/Remove
        add_btn = wx.Button(panel, label="+", size=(30, -1))
        add_btn.Bind(wx.EVT_BUTTON, self.add_goal)
        
        rem_btn = wx.Button(panel, label="-", size=(30, -1))
        rem_btn.Bind(wx.EVT_BUTTON, self.remove_goal)
        
        input_sizer.Add(self.goal_input, 1, wx.RIGHT, 5)
        input_sizer.Add(add_btn, 0, wx.RIGHT, 2)
        input_sizer.Add(rem_btn, 0)
        
        box_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer.Add(box_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        # --- NAVIGATION BUTTONS ---
        grid = wx.GridSizer(rows=3, cols=1, vgap=15, hgap=15)
        
        # CHANGED TO YELLOW
        btn_timer = self.create_button(panel, "  1. Focus Hub (Timer)  ", self.open_study_timer, bg_color='#FFD700')
        # Manually set text to black so it is readable on yellow
        btn_timer.SetForegroundColour('#000000') 
        
        btn_tasks = self.create_button(panel, "  2. Task Manager (To-Do)  ", self.open_task_manager)
        btn_events = self.create_button(panel, "  3. Event Manager (Deadlines)  ", self.open_event_manager, bg_color=THEME['accent_secondary'])
        
        grid.Add(btn_timer, 0, wx.EXPAND)
        grid.Add(btn_tasks, 0, wx.EXPAND)
        grid.Add(btn_events, 0, wx.EXPAND)
        
        sizer.Add(grid, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 40)
        
        panel.SetSizer(sizer)
        self.Centre()

        # --- INITIALIZE SUB-WINDOWS ONCE (Prevent Data Loss) ---
        self.timer_window = StudyTimer(parent=self)
        self.task_window = SimpleTaskManager(parent=self)
        self.event_window = EventManager(parent=self)
        
        # Hide them initially
        self.timer_window.Hide()
        self.task_window.Hide()
        self.event_window.Hide()

    # --- GOAL FUNCTIONS ---
    def add_goal(self, event):
        g = self.goal_input.GetValue()
        if g and g != "New Goal...":
            self.goal_list.Append(g)
            self.goal_input.SetValue("")

    def remove_goal(self, event):
        sel = self.goal_list.GetSelection()
        if sel != wx.NOT_FOUND:
            self.goal_list.Delete(sel)

    # --- NAVIGATION FUNCTIONS ---
    def open_study_timer(self, event):
        self.timer_window.Show()
        self.Hide()
    
    def open_task_manager(self, event):
        self.task_window.Show()
        self.Hide()

    def open_event_manager(self, event):
        self.event_window.Show()
        self.Hide()

class StudyTimer(StyledFrame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Focus Hub", size=(450, 420))
        self.parent_menu = parent
        panel = self.setup_panel()
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        quote = self.create_text(panel, "Focus on the process, not the outcome.")
        sizer.Add(quote, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        
        self.time_display = wx.StaticText(panel, label="00:00:00")
        font = self.time_display.GetFont()
        font.PointSize = 48
        font.MakeBold()
        self.time_display.SetFont(font)
        self.time_display.SetForegroundColour(THEME['timer_text'])
        
        sizer.Add(self.time_display, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.start_btn = self.create_button(panel, "Start", self.start_timer)
        self.pause_btn = self.create_button(panel, "Pause", self.pause_timer)
        self.stop_btn = self.create_button(panel, "Stop", self.stop_timer)
        
        btn_sizer.Add(self.start_btn, 1, wx.ALL, 5)
        btn_sizer.Add(self.pause_btn, 1, wx.ALL, 5)
        btn_sizer.Add(self.stop_btn, 1, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        
        # Presets
        sizer.Add(self.create_text(panel, "Quick Presets:"), 0, wx.LEFT | wx.TOP, 20)
        preset_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pomo_btn = wx.Button(panel, label="Pomodoro (25m)")
        short_btn = wx.Button(panel, label="Short Break (5m)")
        preset_sizer.Add(pomo_btn, 1, wx.ALL, 5)
        preset_sizer.Add(short_btn, 1, wx.ALL, 5)
        sizer.Add(preset_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        
        pomo_btn.Bind(wx.EVT_BUTTON, lambda e: self.set_timer(25))
        short_btn.Bind(wx.EVT_BUTTON, lambda e: self.set_timer(5))

        back_btn = wx.Button(panel, label="< Dashboard")
        back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        sizer.Add(back_btn, 0, wx.ALIGN_LEFT | wx.ALL, 20)
        
        panel.SetSizer(sizer)
        
        self.timer = wx.Timer(self)
        self.elapsed = 0
        self.running = False
        self.target_time = None
        self.Bind(wx.EVT_TIMER, self.update_timer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()
    
    def on_back(self, event): 
        self.Hide() 
        if self.parent_menu: self.parent_menu.Show()

    def on_close(self, event):
        if self.timer.IsRunning(): self.timer.Stop()
        self.Hide() 
        if self.parent_menu: self.parent_menu.Show()

    def update_timer(self, event):
        if self.running:
            self.elapsed += 1
            self.display_time(self.elapsed)
            if self.target_time and self.elapsed >= self.target_time:
                self.timer.Stop()
                self.running = False
                wx.MessageBox("Time's up! Great work.", "Timer")
    def display_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        self.time_display.SetLabel(f"{h:02d}:{m:02d}:{s:02d}")
        self.time_display.GetParent().Layout()
    def set_timer(self, minutes):
        self.stop_timer(None)
        self.target_time = minutes * 60
        self.start_timer(None)
    def start_timer(self, event):
        if not self.running:
            self.running = True
            self.timer.Start(1000)
    def pause_timer(self, event):
        if self.running:
            self.timer.Stop()
            self.running = False
    def stop_timer(self, event):
        if self.running: self.timer.Stop()
        self.running = False
        self.elapsed = 0
        self.display_time(0)

class SimpleTaskManager(StyledFrame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Task Manager", size=(500, 500))
        self.parent_menu = parent
        self.tasks = []
        panel = self.setup_panel()
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        main_sizer.Add(self.create_header(panel, "Quick To-Do List"), 0, wx.ALL | wx.CENTER, 15)
        
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.title_input = self.create_input(panel, "New Task...")
        self.add_btn = self.create_button(panel, "+ Add", self.add_task)
        input_sizer.Add(self.title_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        input_sizer.Add(self.add_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        self.task_list = wx.ListBox(panel)
        self.task_list.SetBackgroundColour("#333333")
        self.task_list.SetForegroundColour("#FFFFFF")
        main_sizer.Add(self.task_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mark_btn = self.create_button(panel, "Mark Done", self.mark_complete)
        self.clear_btn = wx.Button(panel, label="Clear All")
        btn_sizer.Add(self.mark_btn, 1, wx.RIGHT, 10)
        btn_sizer.Add(self.clear_btn, 1)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        back_btn = wx.Button(panel, label="< Dashboard")
        back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        main_sizer.Add(back_btn, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 20)
        
        panel.SetSizer(main_sizer)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.clear_tasks)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()

    def on_back(self, event): 
        self.Hide()
        if self.parent_menu: self.parent_menu.Show()

    def on_close(self, event):
        self.Hide()
        if self.parent_menu: self.parent_menu.Show()

    def add_task(self, event):
        t = self.title_input.GetValue()
        if t and t != "New Task...":
            self.tasks.append({'title': t, 'completed': False})
            self.refresh_list()
            self.title_input.SetValue("")
            
    def refresh_list(self):
        self.task_list.Clear()
        for task in self.tasks:
            status = "✔" if task['completed'] else "☐"
            self.task_list.Append(f"{status}  {task['title']}")
            
    def mark_complete(self, event):
        selection = self.task_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.tasks[selection]['completed'] = True
            self.refresh_list()
            
    def clear_tasks(self, event):
        self.tasks = []
        self.refresh_list()

class EventManager(StyledFrame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Event Manager", size=(500, 500))
        self.parent_menu = parent
        self.events = []
        panel = self.setup_panel()
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        main_sizer.Add(self.create_header(panel, "Deadlines & Events", color=THEME['accent_secondary']), 0, wx.ALL | wx.CENTER, 15)
        
        # Two Inputs
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(self.create_text(panel, "Event Name:"), 0, wx.RIGHT, 5)
        self.title_input = self.create_input(panel, "")
        row1.Add(self.title_input, 1, wx.EXPAND)
        
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(self.create_text(panel, "Due Date:   "), 0, wx.RIGHT, 5) 
        self.date_input = self.create_input(panel, "12 Dec")
        row2.Add(self.date_input, 1, wx.EXPAND)
        
        input_sizer.Add(row1, 0, wx.EXPAND | wx.BOTTOM, 10)
        input_sizer.Add(row2, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.add_btn = self.create_button(panel, "+ Add Event", self.add_event, bg_color=THEME['accent_secondary'])
        input_sizer.Add(self.add_btn, 0, wx.ALIGN_RIGHT)
        
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        self.event_list = wx.ListBox(panel)
        self.event_list.SetBackgroundColour("#333333")
        self.event_list.SetForegroundColour("#FFFFFF")
        main_sizer.Add(self.event_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.remove_btn = wx.Button(panel, label="Remove Selected")
        btn_sizer.Add(self.remove_btn, 1)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        back_btn = wx.Button(panel, label="< Dashboard")
        back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        main_sizer.Add(back_btn, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 20)
        
        panel.SetSizer(main_sizer)
        
        self.remove_btn.Bind(wx.EVT_BUTTON, self.remove_event)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()

    def on_back(self, event): 
        self.Hide()
        if self.parent_menu: self.parent_menu.Show()

    def on_close(self, event):
        self.Hide()
        if self.parent_menu: self.parent_menu.Show()
        
    def add_event(self, event):
        title = self.title_input.GetValue()
        date = self.date_input.GetValue()
        
        if title and date:
            entry = f"[{date}]  {title}"
            self.events.append(entry)
            self.refresh_list()
            self.title_input.SetValue("")
    
    def refresh_list(self):
        self.event_list.Clear()
        for e in self.events:
            self.event_list.Append(e)
            
    def remove_event(self, event):
        selection = self.event_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.events.pop(selection)
            self.refresh_list()

if __name__ == "__main__":
    app = wx.App()
    frame = MenuFrame()
    frame.Show()
    app.MainLoop()