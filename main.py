from tkinter import *
from tkinter import filedialog, messagebox
import string

from wordlist_generator import generate_wordlist
from find_dialog import open_find_dialog


class GUI_APP:
    def __init__(self, Parent):
        self.parent = Parent

        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        # MAIN MENU
        self.menu_bar = Menu(self.parent)
        self.parent.config(menu=self.menu_bar)

        # FILE MENU
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='MyFile', menu=self.file_menu)

        self.file_menu.add_command(label="Quit", command=self.parent.quit)

        self.menu_bar.add_command(label="+", command=self.add_entry)
        self.menu_bar.add_command(label="-", command=self.remove_entry)
        self.menu_bar.add_command(label="Count: 1", command=self.update_count)
        self.menu_bar.add_command(label="Generate Wordlist", command=self.generate_wordlist_from_gui)
          
        self.parent.bind('<Control-t>',lambda event: self.add_entry())
        self.parent.bind('<Control-r>',lambda event: self.remove_entry())
        
        

        self.import_menu_index = None  # Will track if Import is added

        # Entry list canvas
        self.entry_canvas = Canvas(self.parent, height=200)
        self.entry_canvas.grid(row=1, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self.parent, orient=VERTICAL, command=self.entry_canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.entry_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.entry_frame = Frame(self.entry_canvas)
        self.entry_canvas.create_window((0, 0), window=self.entry_frame, anchor="nw")

        self.entry_frame.bind("<Configure>", lambda e: self.entry_canvas.configure(
            scrollregion=self.entry_canvas.bbox("all")
        ))

        self.entries = []
        self.add_entry()

        self.paned = PanedWindow(self.parent, orient=HORIZONTAL)
        self.paned.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.paned_text = Text(self.paned)
        self.paned.add(self.paned_text)

        self.parent.bind("<Control-f>", self.open_find_dialog)

    def add_entry(self):
        entry = Entry(self.entry_frame, width=40)
        entry.pack(pady=2)
        self.entries.append(entry)
        self.update_count()

    def remove_entry(self):
        if self.entries:
            entry = self.entries.pop()
            entry.destroy()
            self.update_count()
        else:
            messagebox.showwarning("Warning", "No more entries to remove")

    def update_count(self):
        count = len(self.entries)
        self.menu_bar.entryconfig(4, label=f"Count: {count}")

    def generate_wordlist_from_gui(self):
        words = [e.get().strip().lower() for e in self.entries if e.get().strip()]
        if not words:
            messagebox.showerror("Input Error", "Please enter some base words.")
            return

        # Ask for symbols
        symbol_win = Toplevel(self.parent)
        symbol_win.title("Enter Symbols")
        Label(symbol_win, text="Enter symbols (comma-separated):").pack(pady=5)
        symbol_entry = Entry(symbol_win)
        symbol_entry.pack(pady=5)
        Button(symbol_win, text="Generate", command=lambda: self.process_symbols(symbol_entry.get(), words, symbol_win)).pack(pady=5)

    def process_symbols(self, symbols_input, base_words, win):
        win.destroy()
        symbols = [s.strip() for s in symbols_input.split(",") if s.strip()]
        wordlist = generate_wordlist(base_words, symbols)

        try:
            with open("custom_wordlist.txt", "w") as f:
                for word in sorted(wordlist):
                    f.write(word + "\n")
            self.paned_text.delete(1.0, END)
            self.paned_text.insert(END, f"Wordlist saved as 'custom_wordlist.txt'\nTotal words: {len(wordlist)}\n\n")
            self.paned_text.insert(END, "\n".join(sorted(wordlist)))

            # Add Import menu if not already added
            if self.import_menu_index is None:
                self.import_menu_index = self.menu_bar.index("end") + 1
                self.menu_bar.add_command(label="Import", command=self.import_entries)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save wordlist:\n{e}")

    def import_entries(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
            for e in self.entries:
                e.destroy()
            self.entries.clear()
            for line in lines:
                entry = Entry(self.entry_frame, width=40)
                entry.insert(0, line)
                entry.pack(pady=2)
                self.entries.append(entry)
            self.update_count()
            messagebox.showinfo("Imported", f"Imported {len(lines)} entries.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import entries:\n{e}")

    def open_find_dialog(self, event=None):
        open_find_dialog(self.parent, self.paned_text)


if __name__ == "__main__":
    myroot = Tk()
    myroot.title("Advanced Wordlist Generator GUI")
    myroot.geometry('700x600')
    app = GUI_APP(myroot)
    myroot.mainloop()
