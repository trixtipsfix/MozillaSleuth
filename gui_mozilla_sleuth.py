import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess

__version__ = 1.0
contributors = "whoamirza x 0xd4"

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mozilla Sleuth")
        
        ascii_banner = """
███╗   ███╗ ██████╗ ███████╗██╗██╗     ██╗      █████╗     ███████╗██╗     ███████╗██╗   ██╗████████╗██╗  ██╗
████╗ ████║██╔═══██╗╚══███╔╝██║██║     ██║     ██╔══██╗    ██╔════╝██║     ██╔════╝██║   ██║╚══██╔══╝██║  ██║
██╔████╔██║██║   ██║  ███╔╝ ██║██║     ██║     ███████║    ███████╗██║     █████╗  ██║   ██║   ██║   ███████║
██║╚██╔╝██║██║   ██║ ███╔╝  ██║██║     ██║     ██╔══██║    ╚════██║██║     ██╔══╝  ██║   ██║   ██║   ██╔══██║
██║ ╚═╝ ██║╚██████╔╝███████╗██║███████╗███████╗██║  ██║    ███████║███████╗███████╗╚██████╔╝   ██║   ██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
                                                                                                                               
            v{} by {}
        """.format(__version__, contributors)

        self.banner_label = tk.Label(root, text=ascii_banner, font=("Courier", 12), justify=tk.LEFT, anchor="w", padx=10, pady=10)
        self.banner_label.pack()

        # Create form elements
        self.create_form()
        # Create Start button
        # self.start_button = tk.Button(root, text="Scan Profiles", command=self.execute_command)
        # self.start_button.pack(pady=10)

        # Create scrolled text widget to display output
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill="both")
        
    def create_form(self):
        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown_label = tk.Label(form_frame, text="Select an option:")
        self.dropdown_label.grid(row=0, column=0, padx=10, pady=5)
        # Execute your command here
        command = '"C:/Users/PMYLS/AppData/Local/Programs/Python/Python311/python.exe" "c:/Users/PMYLS/Desktop/DF_Project/MozillaSleuth/MozillaSleuth/mozilla_sleuth.py" profiles'
        result = self.run_command(command)
        options = result.split("\n")[:-1]
        self.dropdown_menu = ttk.Combobox(form_frame, textvariable=self.dropdown_var, values=options)
        self.dropdown_menu.grid(row=0, column=1, padx=10, pady=5)
        self.dropdown_menu.current(0)  # Set default option

        # Checkboxes
        self.checkbox_var1 = tk.BooleanVar()
        self.checkbox_var2 = tk.BooleanVar()
        self.checkbox_var3 = tk.BooleanVar()
        self.checkbox_var4 = tk.BooleanVar()

        self.checkbox_label1 = tk.Checkbutton(form_frame, text="History", variable=self.checkbox_var1)
        self.checkbox_label2 = tk.Checkbutton(form_frame, text="Fingerprints", variable=self.checkbox_var2)
        self.checkbox_label3 = tk.Checkbutton(form_frame, text="Downloads", variable=self.checkbox_var3)
        self.checkbox_label4 = tk.Checkbutton(form_frame, text="Export All", variable=self.checkbox_var4)

        self.checkbox_label1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_label2.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.checkbox_label3.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.checkbox_label4.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Submit button
        self.submit_button = tk.Button(form_frame, text="Submit", command=self.execute_command_from_form)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def execute_command_from_form(self):
        # Get the selected values from the form
        selected_option = self.dropdown_var.get()
        checkbox_values = [
            self.checkbox_var1.get(),
            self.checkbox_var2.get(),
            self.checkbox_var3.get(),
            self.checkbox_var4.get()
        ]
        command = '"C:/Users/PMYLS/AppData/Local/Programs/Python/Python311/python.exe" "c:/Users/PMYLS/Desktop/DF_Project/MozillaSleuth/MozillaSleuth/mozilla_sleuth.py" '
        # Execute your command here
        if checkbox_values[3] == True:
            command += 'export --profile '+selected_option.split(']')[0][-1]
        else:
            if checkbox_values[0] == True:
                command += 'history --profile '+selected_option.split(']')[0][-1]
            else:
                if checkbox_values[2] == True:
                    command = 'downloads --profile '+selected_option.split(']')[0][-1]
                else:
                    if checkbox_values[1] == True:
                        command = 'fingerprint --profile '+selected_option.split(']')[0][-1]
                    
        result = self.run_command(command)

        # Display the result in the scrolled text widget
        self.output_text.insert(tk.END, result)
        self.output_text.insert(tk.END, "\n\n")
        self.output_text.see(tk.END)  # Scroll to the end of the text

    def run_command(self, command):
        # Run the command and capture the output
        try:
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            result = f"Error: {e}"
        return result

if __name__ == "__main__":
    root = tk.Tk()
    # root.attributes("-fullscreen", True)
    gui = GUI(root)
    root.mainloop()
