import hashlib
import tkinter as tk

def on_button_click():
    if hashEntry.get():
        if scramble_invoice(entry.get()) == hashEntry.get():
            button.config(text="✅MATCH✅")
        else:
            button.config(text="❌WRONG❌")
    else:
        button.config(text="👇Hash👇")
        hashEntry.insert(0,scramble_invoice(entry.get()))

def scramble_invoice(invoice_number):
    # Stringify invoice_number
    data = f"{invoice_number}"
    # Hash the data
    hashed_data = hashlib.md5(data.encode()).hexdigest()

    return hashed_data


# Create the main window
window = tk.Tk()
window.title("Invoice Hash")
window.geometry("330x110")

# Create an Entry widget for text input
entry = tk.Entry(window, width=50)
entry.pack(padx=5, pady=5, anchor="w")

# Create a button
button = tk.Button(window, text="👇Hash👇", command=on_button_click)
button.pack(padx=5, pady=5, anchor="w")

# Create an Entry widget for hash input
hashEntry = tk.Entry(window, width=50)
hashEntry.pack(padx=5, pady=5, anchor="w")

# Run the GUI loop
window.mainloop()

#print(f"Scrambled Invoice: {scrambled_invoice}")

#input("Press Enter to exit")
