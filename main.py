import os
import tkinter as tk
from tkinter import ttk, filedialog
from FilesFoldersStructureMaker import FilesFoldersStructureMaker as ffsm
import platform
import subprocess
import configparser

class FileStructureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File/Folder Structure Maker")

        # Menu bar
        # Create a style for the menu buttons
        self.style = ttk.Style(self.root)

        # Custom menu bar using ttk.Menubutton
        self.menu_frame = tk.Frame(self.root, bg="#ffffff", height=25)  # This is the container for our menus
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # File menu button
        self.file_menu_btn = ttk.Menubutton(self.menu_frame, text="File", direction="below")
        self.file_menu_btn.pack(side=tk.LEFT, padx=10)
        self.file_menu = tk.Menu(self.file_menu_btn, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_config)
        self.file_menu_btn["menu"] = self.file_menu

        # Help menu button
        self.help_menu_btn = ttk.Menubutton(self.menu_frame, text="Help", direction="below")
        self.help_menu_btn.pack(side=tk.LEFT, padx=10)
        self.help_menu = tk.Menu(self.help_menu_btn, tearoff=0)
        self.help_menu.add_command(label="Demo", command=self.load_demo)
        self.help_menu_btn["menu"] = self.help_menu

        # Settings menu button
        self.settings_menu_btn = ttk.Menubutton(self.menu_frame, text="Settings", direction="below")
        self.settings_menu_btn.pack(side=tk.LEFT, padx=10)
        self.settings_menu = tk.Menu(self.settings_menu_btn, tearoff=0)

        # Theme selection submenu
        self.theme_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.theme_menu.add_radiobutton(label="Light", command=lambda: self.set_theme("light"))
        self.theme_menu.add_radiobutton(label="Dark", command=lambda: self.set_theme("dark"))
        self.settings_menu.add_cascade(label="Theme", menu=self.theme_menu)
        self.settings_menu_btn["menu"] = self.settings_menu

        # Input label
        self.label = tk.Label(root, text="Enter the folder structure:")
        self.label.pack()

        # Text box for input
        self.text_box = tk.Text(root, height=15, width=50)
        self.text_box.pack()

        # Button to create folder structure
        self.create_button = tk.Button(root, text="Create Structure", command=self.create_structure)
        self.create_button.pack()

        # Base repository
        self.base_directory = None

        self.base_path = tk.Text(root, height=1, width=50)
        self.base_path.pack()
        self.set_base_path('')

        # Select folder to create the structure in
        self.select_button = tk.Button(root, text="Select Base Directory", command=self.select_directory)
        self.select_button.pack()

        # Default theme
        self.set_theme("light")  # Set default to light theme

        # Load settings at startup
        self.load_config()
        

    def set_base_path(self, path):
        """Set the base path in the text widget."""
        self.base_path.delete(1.0, tk.END)   # Clear the current content
        self.base_path.insert(tk.END, path)  # Insert the selected path

    def get_base_path(self):
        return self.base_path.get("1.0", tk.END).strip()

    def select_directory(self):
        """Select the base directory to create the folder structure."""
        self.base_directory = filedialog.askdirectory()
        if self.base_directory:
            self.custom_messagebox("info", "Directory Selected", f"Base Directory: {self.base_directory}")
            self.set_base_path(self.base_directory)
        else:
            self.custom_messagebox("warning", "No Directory Selected", "Please select a valid directory.")

    def open_file_explorer(self, path):
        """Open the file explorer at the given path."""
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux and other Unix-like OS
            subprocess.run(["xdg-open", path])

    def create_structure(self):
        """Create the folder structure based on the input."""
        if self.get_base_path() == '' and not self.base_directory:
            self.custom_messagebox("error", "Error", "Please select a base directory first.")
            return

        if self.get_base_path() != '':
            base_dir = self.get_base_path()
        else:
            base_dir = self.base_directory
            self.set_base_path(base_dir)
        structure_text = self.text_box.get("1.0", tk.END).strip()

        if not structure_text:
            self.custom_messagebox("warning", "Warning", "Please enter a valid folder structure.")
            return

        # Create the folder structure
        exception = ffsm.make(base_dir, structure_text)
        if isinstance(exception, Exception):
            self.custom_messagebox("error", "Error", f"File structure not created! Error:\n{exception}")
        else:
            self.custom_messagebox("info", "Success", "File structure created successfully!")

            # Open the file explorer at the base directory after creation
            self.open_file_explorer(base_dir)

    def set_theme(self, theme):
        """Set the application's theme."""
        if theme == "light":
            self.bg_color = "#ffffff"
            self.fg_color = "#000000"
            menu_bg = "#f0f0f0"
            menu_fg = "#000000"
        elif theme == "dark":
            self.bg_color = "#2e2e2e"
            self.fg_color = "#ffffff"
            menu_bg = "#3c3f41"
            menu_fg = "#ffffff"

        # Apply theme to widgets
        self.root.config(bg=self.bg_color)
        self.label.config(bg=self.bg_color, fg=self.fg_color)
        self.text_box.config(bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.create_button.config(bg=self.bg_color, fg=self.fg_color)
        self.base_path.config(bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.select_button.config(bg=self.bg_color, fg=self.fg_color)

        # Apply theme to the custom menu buttons
        self.menu_frame.config(bg=self.bg_color)
        self.style.configure("TMenubutton", background=menu_bg, foreground=menu_fg)
        self.file_menu_btn.config(style="TMenubutton")
        self.help_menu_btn.config(style="TMenubutton")
        self.settings_menu_btn.config(style="TMenubutton")

    def load_demo(self):
        """Load the demo base path and folder structure."""
        demo_base_path = "/home/me/test"
        demo_structure = """    folders_and_files_structure_demo/
    ├── static/
    │   ├── css/
    │   │   ├── base/
    │   │   │   ├── reset.css
    │   │   │   ├── styles.css
    │   │   ├── theme/
    │   │   │   ├── dark.css
    │   │   │   ├── light.css
    │   ├── js/
    │   │   ├── modules/
    │   │   │   ├── app.js
    │   │   │   ├── service.js
    │   │   ├── vendor/
    │   │   │   ├── jquery.js
    │   │   │   ├── bootstrap.js
    ├── templates/
    │   ├── layouts/
    │   │   ├── header.html
    │   │   ├── footer.html
    │   ├── includes/
    │   │   ├── navbar.html
    │   │   ├── sidebar.html
    │   ├── pages/
    │   │   ├── home.html
    │   │   ├── about.html
    ├── app.py
    ├── models.py
    └── database.db
        """
        self.set_base_path(demo_base_path)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, demo_structure)

        self.custom_messagebox("info", "Next Steps", "1. Adapt the base directory path.\n2. Click 'Create Structure' button.")

    def custom_messagebox(self, box_type, title, message):
        """Create a custom messagebox with the current theme and center it."""
        top = tk.Toplevel(self.root)
        top.title(title)

        # Set the size of the messagebox window
        top.geometry("300x150")

        # Calculate the position to center the messagebox on the root window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Messagebox dimensions
        msgbox_width = 300
        msgbox_height = 150

        # Center position
        center_x = root_x + (root_width // 2) - (msgbox_width // 2)
        center_y = root_y + (root_height // 2) - (msgbox_height // 2)

        # Set the geometry to position the window in the center of the root window
        top.geometry(f"{msgbox_width}x{msgbox_height}+{center_x}+{center_y}")

        # Set background and foreground colors based on the theme
        top.config(bg=self.bg_color)

        # Message label
        msg = tk.Label(top, text=message, bg=self.bg_color, fg=self.fg_color)
        msg.pack(pady=20)

        # OK button
        ok_button = tk.Button(top, text="OK", command=top.destroy, bg=self.bg_color, fg=self.fg_color)
        ok_button.pack(pady=10)

        # Make sure the dialog is modal (prevents interaction with main window until closed)
        top.grab_set()
        top.transient(self.root)
        top.focus_force()

    # def save_config(self):
    #     """Save the current theme, input structure text, and base folder to a config file."""
    #     config = configparser.ConfigParser()
    #     config['Settings'] = {
    #         'Theme': 'light' if self.bg_color == "#ffffff" else 'dark',
    #         'BaseFolder': self.get_base_path(),
    #         'StructureText': self.text_box.get("1.0", tk.END).strip()
    #     }

    #     config_file = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("Config files", "*.ini")])
    #     if config_file:
    #         with open(config_file, 'w') as configfile:
    #             config.write(configfile)
    #         self.custom_messagebox("info", "Success", "Configuration saved successfully!")

    def save_config(self):
        """Save the current theme, input structure text, and base folder to a config file."""
        config = configparser.ConfigParser()
        config['Settings'] = {
            'Theme': 'light' if self.bg_color == "#ffffff" else 'dark',
            'BaseFolder': self.get_base_path(),
            'StructureText': self.text_box.get("1.0", tk.END).strip()
        }

        config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        self.custom_messagebox("info", "Success", "Configuration saved successfully!")

    def load_config(self):
        """Load the settings from the config file at startup."""
        config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            if 'Settings' in config:
                theme = config['Settings'].get('Theme', 'light')
                base_folder = config['Settings'].get('BaseFolder', '')
                structure_text = config['Settings'].get('StructureText', '')

                self.set_theme(theme)
                self.set_base_path(base_folder)
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, structure_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStructureApp(root)
    root.mainloop()
