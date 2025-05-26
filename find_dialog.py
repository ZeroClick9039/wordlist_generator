import string
from tkinter import Toplevel, Label, Entry, Button, messagebox, TclError

def open_find_dialog(parent, text_widget):
    find_win = Toplevel(parent)
    find_win.title("Find")
    find_win.geometry("300x80")
    find_win.transient(parent)

    Label(find_win, text="Find:").pack(pady=5)
    find_entry = Entry(find_win, width=25)
    find_entry.pack()

    def do_find():
        text_widget.tag_remove("highlight", "1.0", "end")
        query = find_entry.get()
        if not query:
            return

        start = "1.0"
        first_match_found = False
        found_any = False
        while True:
            start = text_widget.search(query, start, stopindex="end")
            if not start:
                break

            end = f"{start}+{len(query)}c"

            try:
                char_before = text_widget.get(f"{start} -1c")
            except TclError:
                char_before = None

            try:
                char_after = text_widget.get(end)
            except TclError:
                char_after = None

            boundaries = string.whitespace + string.punctuation

            before_ok = (char_before is None) or (char_before in boundaries)
            after_ok = (char_after is None) or (char_after in boundaries)

            if before_ok and after_ok:
                found_any = True
                text_widget.tag_add("highlight", start, end)
                text_widget.tag_config("highlight", background="yellow", foreground="black")
                if not first_match_found:
                    text_widget.see(start)
                    first_match_found = True

            start = end

        if not found_any:
            messagebox.showinfo("Find", f"No whole word occurrences of '{query}' found.")

    Button(find_win, text="Search", command=do_find).pack(pady=5)
    find_entry.bind("<Return>", lambda event: do_find())
    find_entry.focus()
