import os
import threading
import tkinter as tk

from tkinter import filedialog, ttk
from tkinter import messagebox
from settings import GuiAppSettings, MainSettings


class GuiApp:
    def __init__(self, root, extractor):
        self.root = root
        self.extractor = extractor
        self.style = ttk.Style()

        self.title_label = tk.Label(root, text=GuiAppSettings.Labels.title["text"], font=GuiAppSettings.Labels.title["font"])
        self.title_label.pack(pady=20)

        self.choose_directory_label = tk.Label(root, text=GuiAppSettings.Labels.choose_directory["text"])
        self.choose_directory_label.pack()

        self.directory_label = tk.Label(root, text=GuiAppSettings.Labels.directory["text"],
                                        bg=GuiAppSettings.Labels.directory["bg"],
                                        width=GuiAppSettings.Labels.directory["width"],
                                        height=GuiAppSettings.Labels.directory["height"])
        self.directory_label.pack(pady=10)

        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack(pady=5)

        self.choose_directory_btn = tk.Button(root, text=GuiAppSettings.Buttons.browse["text"], command=self.browse_directory)
        self.choose_directory_btn.pack()

        self.start_processing_btn = ttk.Button(root, text=GuiAppSettings.Buttons.start_processing["text"], command=self.process_files)
        self.style.map('TButton',
                       background=GuiAppSettings.Buttons.start_processing["styles"]["background"])
        self.start_processing_btn.pack(pady=20)

        self.progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.pack(pady=20)

        self.output_text = tk.Text(self.root, height=2, wrap=tk.NONE, bg=self.root.cget("bg"), bd=0,
                                   highlightthickness=0, width=50)
        self.output_text.pack(pady=20)

        self.output_text.tag_configure("green", foreground="green")
        self.output_text.tag_configure("black", foreground="black")

        self.output_text.config(state=tk.DISABLED)

        # Create menu
        self.main_menu = tk.Menu(self.root)

        # Item "help"
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label=MainSettings.Menu.menu, menu=self.help_menu)

        # Add the "About" item to the "Help" menu
        self.help_menu.add_command(label=MainSettings.Menu.title, command=self.show_about)

        self.root.config(menu=self.main_menu)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_label.config(text=directory)

    def process_files(self):
        self.start_processing_btn.configure(state=tk.DISABLED)
        self.choose_directory_btn.configure(state=tk.DISABLED)

        directory = self.directory_label.cget("text")
        # output_file_path = "result.txt"

        if directory == GuiAppSettings.Labels.directory["text"]:
            messagebox.showwarning("Warning", GuiAppSettings.Labels.message["error"])
            self.start_processing_btn.configure(state=tk.NORMAL)
            self.choose_directory_btn.configure(state=tk.NORMAL)
            return

        elif not self.extractor.check_pdf_in_directory(directory):
            messagebox.showwarning("Warning", GuiAppSettings.Labels.message["no_pdf"])
            self.start_processing_btn.configure(state=tk.NORMAL)
            self.choose_directory_btn.configure(state=tk.NORMAL)
            return

        thread = threading.Thread(target=self.threaded_processing, args=(directory, GuiAppSettings.Labels.file["name"]))
        thread.start()

    def on_processing_complete(self):
        self.start_processing_btn.configure(state=tk.NORMAL)
        self.choose_directory_btn.configure(state=tk.NORMAL)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, GuiAppSettings.Labels.progress["result"], "green")
        self.output_text.insert(tk.END, GuiAppSettings.Labels.file["name"], "black")
        self.output_text.config(state=tk.DISABLED)

        messagebox.showinfo("Ready", GuiAppSettings.Labels.message["ready"])

        os.startfile(GuiAppSettings.Labels.file["name"])

    def threaded_processing(self, directory, output_file_path):
        self.extractor.process_pdfs_in_directory(directory, output_file_path, self.update_progress)
        self.root.after_idle(self.on_processing_complete)

    def update_progress(self, processed, total):
        percentage = (processed / total) * 100
        self.progress_bar['value'] = percentage
        self.progress_label.config(text=f"{GuiAppSettings.Labels.progress['text']} {processed} из {total}")
        self.root.update_idletasks()

    @staticmethod
    def show_about():
        info_text = f"""
            {MainSettings.Menu.menu_name} {MainSettings.Window.title}
            {MainSettings.Menu.menu_ver} {MainSettings.About.version}
            {MainSettings.Menu.menu_autor} {MainSettings.About.author}
            {MainSettings.Menu.menu_email} {MainSettings.About.email}
            """
        messagebox.showinfo(MainSettings.Menu.title, info_text)

