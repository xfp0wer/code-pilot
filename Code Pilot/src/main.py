import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import webbrowser

class TextEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Code Pilot")
        self.create_widgets()

        # Initialize line numbers
        self.create_line_numbers()

        # Bind events to update line count
        self.text_area.bind('<KeyPress>', self.update_line_numbers)
        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<Return>', self.update_line_numbers)
        self.text_area.bind('<Delete>', self.update_line_numbers)

        # Menu
        self.create_menu()

    def create_widgets(self):
        # Create text area with Cascadia Code font
        self.text_area = tk.Text(self.root, wrap="word", undo=True, font=("Cascadia Code", 10))
        self.text_area.pack(side="right", expand=True, fill="both")

        # Scrollbar for text area
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_area.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scrollbar.set)

    def create_line_numbers(self):
        self.line_number_area = tk.Text(self.root, width=4, wrap="none", state="disabled", bd=0)
        self.line_number_area.pack(side="left", fill="y")

        # Synchronize scrolling of text area and line number area
        self.text_area.config(yscrollcommand=self.scroll_text)
        self.line_number_area.config(yscrollcommand=self.scroll_text)

        # Initial update of line numbers
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        # Clear current line numbers
        self.line_number_area.config(state="normal")
        self.line_number_area.delete(1.0, tk.END)

        # Count number of lines in text area
        num_lines = self.text_area.get("1.0", tk.END).count("\n")

        # Update line numbers
        for line in range(1, num_lines + 2):
            self.line_number_area.insert(tk.END, f"{line}\n")

        self.line_number_area.config(state="disabled")

    def scroll_text(self, *args):
        if args and isinstance(args[0], str):
            if args[0] == "scroll":
                self.text_area.yview_scroll(int(args[1]), "units")
            elif args[0] == "moveto":
                self.text_area.yview_moveto(args[1])

        # Synchronize line number area with text area scroll
        text_area_yview = self.text_area.yview()
        self.line_number_area.yview_moveto(text_area_yview[0])

        # Synchronize text area with line number area scroll
        line_number_area_yview = self.line_number_area.yview()
        self.text_area.yview_moveto(line_number_area_yview[0])

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="New Window", accelerator="Ctrl+Shift+N", command=self.new_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.help_menu.add_command(label="Help", command=self.open_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.update_line_numbers()
        self.root.title("Code Pilot - Untitled")

    def new_window(self):
        new_root = tk.Toplevel(self.root)
        editor = TextEditor(new_root)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                    self.update_line_numbers()
                    self.root.title(f"Code Pilot - {file.name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        try:
            if not hasattr(self, "file_path"):
                self.save_as_file()
            else:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    self.root.title(f"Code Pilot - {file.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def save_as_file(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    self.file_path = file.name
                    self.root.title(f"Code Pilot - {file.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def open_help(self):
        # Replace this with the actual link or help content you want to display
        webbrowser.open("https://example.com/help")

    def exit_app(self):
        self.root.quit()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def show_about(self):
        messagebox.showinfo("About", "Code Pilot\nBy: Rylynn J. Hynum\nCreated with Python")


def main():
    root = tk.Tk()
    root.geometry("1025x725")
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
