from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime
import csv
import os

def validate_and_create_new_row(event):
    global entries, y_offset
    if all([entry.get().strip() for entry in entries]):
        try:
            datetime.datetime.strptime(entries[2].get(), "%Y-%m-%d").date()
            datetime.datetime.strptime(entries[3].get(), "%Y-%m-%d").date()
        except ValueError:
            return

        # If all fields are valid, create a new row of Entry fields
        y_offset += 25
        create_entries()

def submit():
    global all_entries
    is_all_filled = all([entry.get().strip() for entry_row in all_entries for entry in entry_row])
    if not is_all_filled:
        result = messagebox.askyesno("Warning", "Some fields are empty. Do you want to proceed?")
        if not result:
            return  # If the user selects 'No', then return and don't proceed with the submission

    for entries in all_entries:
        try:
            date_in_obj = datetime.datetime.strptime(entries[2].get(), "%Y-%m-%d").date()
            date_out_obj = datetime.datetime.strptime(entries[3].get(), "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            return

        if date_in_obj > date_out_obj:
            print("Check-in date cannot be later than check-out date.")
            return

        print("Name: ", entries[0].get())
        print("Room: ", entries[1].get())
        print("Date In: ", date_in_obj)
        print("Date Out: ", date_out_obj)

        # Create directory if it doesn't exist
        directory = os.path.join(" ",title_var.get().strip())
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write to CSV file within the directory
        with open(os.path.join(directory, 'housingList.csv'), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([entry.get() for entry in entries])

    # Clear fields and move the y_offset for the next row
    for entries in all_entries:
        for entry in entries:
            entry.delete(0, 'end')

def create_entries():
    global entries, all_entries
    entries = []
    fields = ["Name", "Room", "Date In (YYYY-MM-DD)", "Date Out (YYYY-MM-DD)"]
    for i, field in enumerate(fields):
        if y_offset == 20:  # Only create headers on the first row
            Label(canvas, text=field).place(x=20+180*i, y=y_offset)
        entry = Entry(canvas)
        entry.place(x=20+180*i, y=y_offset+30)
        entry.bind("<Tab>", validate_and_create_new_row)
        entries.append(entry)
    all_entries.append(entries)

def open_sign_in():
    global canvas, y_offset, all_entries
    if title_var.get().strip() == "":
        print("Please enter a valid title.")
        return

    sign_in = Toplevel(root)
    sign_in.title("Housing Sign In System - " + title_var.get().strip())

    # Add customizable background
    canvas = Canvas(sign_in, width=938, height=938)
    canvas.pack()

    load = Image.open("background.jpeg")  # Add your image file path here
    render = ImageTk.PhotoImage(load)
    img = canvas.create_image(200, 300, image=render)

    all_entries = []
    y_offset = 20
    create_entries()

    # Submit Button
    submit_button = Button(canvas, text="Submit", command=submit)
    submit_button.place(x=820, y=50)

# Create homepage
root = Tk()
root.title("Housing System Home Page")

# Set default window size
root.geometry("400x200")

# Title prompt
title_var = StringVar()
Label(root, text="Title for Housing").pack()
title_entry = Entry(root, textvariable=title_var)
title_entry.pack()

# Create and Modify buttons
create_button = Button(root, text="Create Printable Housing Sign-In Sheet", command=open_sign_in)
create_button.pack()

modify_button = Button(root, text="Modify Housing Sign-In Sheet", command=open_sign_in)
modify_button.pack()

root.mainloop()