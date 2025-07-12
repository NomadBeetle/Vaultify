from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)

    entryP.delete(0, END)
    entryP.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_pass():
    website = entryW.get().title()
    email = entryE.get()
    password = entryP.get()

    data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) > 0 and len(email) > 0 and len(password) > 0:
        try:
            with open("passwords.json", "r") as fh:
                file_data = json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError):
            file_data = {}

        if website in file_data:
            overwrite = messagebox.askyesno(title="Warning", message=f"Entry for {website} already exists. Overwrite?")
            if not overwrite:
                return

        confirm = messagebox.askokcancel(title = website, message = f"This is the data : \nEmail : {email}\nPassword : {password}\nIs it okay to save?")

        if confirm:
            file_data.update(data)
            with open("passwords.json", "w") as fh:
                json.dump(file_data, fh, indent=4)
                pyperclip.copy(file_data[website]["password"])

            entryP.delete(0, END)
            entryW.delete(0, END)

            messagebox.showinfo(title="Success", message="Password saved successfully!")
    else:
        messagebox.showerror(title="OOPS!", message="Please Don't Leave Any Fields Empty!")

# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_pass():
    web_s = entryW.get()
    try:
        with open("passwords.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title = "Error!", message = "No website found!")
    else :
        if web_s in data :
            em = data[web_s]["email"]
            ps = data[web_s]["password"]
            messagebox.showinfo(title = "Website Found!", message = f"Email : {em}\nPassword : {ps}")
        else :
            messagebox.showwarning(title="Not Found", message=f"No details found for '{web_s}'.")


# ---------------------------- UI SETUP ------------------------------- #

#window
window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

#canvas
canvas = Canvas(width = 200, height = 200)
pic = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = pic)

canvas.grid(row = 0, column = 1)

#labels
labelW = Label(text = "Website : ")
labelE = Label(text = "Email/Username : ")
labelP = Label(text = "Password : ")

labelW.grid(row = 1, column = 0)
labelE.grid(row = 2, column = 0)
labelP.grid(row = 3, column = 0)

#entries

entryW = Entry(width = 29, highlightthickness=0)
entryW.grid(row = 1, column = 1, columnspan = 1)
entryW.focus()
entryE = Entry(width = 48, highlightthickness=0)
entryE.grid(row = 2, column = 1, columnspan = 2)
entryE.insert(0, "azaanahmed1369@gmail.com")
entryP = Entry(width = 29, highlightthickness=0)
entryP.grid(row = 3, column = 1)

#buttons
buttonG = Button(text = "Generate Password", highlightthickness=0, command = generate_pass)
buttonG.grid(row = 3, column = 2)
buttonA = Button(text = "Add", width = 45, highlightthickness=0, command = save_pass)

buttonS = Button(text = "Search", highlightthickness=0, command = search_pass, width=14)
buttonS.grid(row = 1, column = 2)
buttonA.grid(row = 4, column = 1, columnspan = 2)

window.mainloop()
