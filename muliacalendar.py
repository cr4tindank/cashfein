from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import datetime

# Main application window
root = Tk()
root.geometry("700x400")
root.title("Torica Furniture Store")

# Initialize furniture "databases"
furniturecodes = ['1', '2', '3', '4', '5']
furniturenames = ['Sofa', 'Lemari', 'Kursi', 'Meja', 'Lampu']
cnames = StringVar(value=furniturenames)
persediaan = {'1': 280, '2': 190, '3': 450, '4': 350, '5': 560}

# Color dictionary for furniture colors
colornames = {'merah': 'Merah', 'biru': 'Biru', 'kuning': 'Kuning', 'hijau': 'Hijau'}
colorcodes = {'1','2','3','4'}
sizenames = {'small': 'Small', 'medium': 'Medium', 'big': 'Big'}
sizecodes = {'1','2','3'} 

# State variables
selected_color = StringVar()
selected_size = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

# List to store all transactions, including timestamp and other details
transactions = []

# Create container for multiple screens (Frames)
login_frame = Frame(root, bg="blue")
welcome_frame = Frame(root, bg="blue")
main_frame = Frame(root, bg="white")
furniture_management_frame = Frame(root, bg="white")
color_management_frame = Frame(root, bg="white")
size_management_frame = Frame(root, bg="white")

# Switch between frames
def show_frame(frame):
    frame.tkraise()

# --- Login Screen ---
def validate_login():
    first_name = first_name_var.get()
    last_name = last_name_var.get()

    if first_name and last_name:
        welcome_label.config(text=f"Welcome {first_name} {last_name}!")
        show_frame(welcome_frame)
    else:
        messagebox.showerror("Error", "Please enter both first and last names.")

first_name_var = StringVar()
last_name_var = StringVar()

Label(login_frame, text="First Name:", bg="blue", fg="white").grid(row=0, column=0, pady=10, padx=10)
Entry(login_frame, textvariable=first_name_var).grid(row=0, column=1, pady=10, padx=10)

Label(login_frame, text="Last Name:", bg="blue", fg="white").grid(row=1, column=0, pady=10, padx=10)
Entry(login_frame, textvariable=last_name_var).grid(row=1, column=1, pady=10, padx=10)

Button(login_frame, text="Login", command=validate_login).grid(row=2, column=0, columnspan=2, pady=20)

# --- Welcome Screen ---
welcome_label = Label(welcome_frame, text="", bg="blue", fg="white", font=("Arial", 16))
welcome_label.pack(pady=50)

Button(welcome_frame, text="Click me to see our furniture collection", 
       command=lambda: show_frame(main_frame)).pack(pady=10)

# --- Main Menu Screen (Furniture App) ---
def showPersediaan(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        code = furniturecodes[idx]
        name = furniturenames[idx]
        stock = persediaan[code]
        statusmsg.set(f"Persediaan {name} ({code}) {stock}")
    sentmsg.set('')  # Clear sent message

def calculate_price(furniture_code, size):
    """Calculate the price of a furniture item based on its code and size."""
    base_price = 500_000  # Base price for code '1' and small size
    price_increase = int(furniture_code) * 500  # Increase price based on furniture code
    size_increase = {"small": 0, "medium": 500_000, "big": 1_000_000}  # Size-based increase
    
    # Calculate final price
    return base_price + price_increase + size_increase.get(size, 0)

def sendtocart(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = furniturenames[idx]
        code = furniturecodes[idx]
        color = selected_color.get()
        size = selected_size.get()  # Get selected size

        if persediaan[code] > 0 and color and size:
            price = calculate_price(code, size)  # Calculate price based on furniture code and size
            
            # Open a calendar window to select the transaction date
            def select_date():
                date_window = Toplevel(root)
                date_window.title("Select Transaction Date")
                date_window.geometry("300x300")

                # Create a calendar widget
                cal = Calendar(date_window, selectmode='day', 
                               year=datetime.datetime.now().year, 
                               month=datetime.datetime.now().month, 
                               day=datetime.datetime.now().day)
                cal.pack(padx=10, pady=10)

                def on_date_select():
                    selected_date = cal.get_date()
                    # Format the date as needed
                    formatted_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
                    
                    persediaan[code] -= 1
                    
                    transaction = {
                        "timestamp": formatted_date,
                        "furniture": name,
                        "color": colornames[color],
                        "size": size.capitalize(),
                        "price": f"Rp. {price:,.0f}"
                    }
                    transactions.append(transaction)
                    sentmsg.set(f"Transaksi anda: {transaction['furniture']} ({transaction['size']} - {transaction['color']}) seharga {transaction['price']} | Stok tersisa: {persediaan[code]}")
                    statusmsg.set(f"Persediaan {name} ({code}) {persediaan[code]}")
                    
                    date_window.destroy()

                # Add a button to confirm the selected date
                Button(date_window, text="Confirm Date", command=on_date_select).pack(pady=10)

            # Open the date selection window
            select_date()
        else:
            if persediaan[code] <= 0:
                sentmsg.set(f"Maaf, stok {name} sudah habis!")
            else:
                sentmsg.set("Tolong pilih warna dan ukuran.")

def open_transactions():
    """Open a new window to display all transactions."""
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions available.")
        return

    trans_window = Toplevel(root)
    trans_window.title("All Transactions")
    trans_window.geometry("700x300")

    # Define Treeview columns
    columns = ("timestamp", "furniture", "color", "size", "price")

    # Create Treeview with columns for each transaction detail
    tree = ttk.Treeview(trans_window, columns=columns, show="headings", height=10)
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Define headings for each column
    tree.heading("timestamp", text="Transaction Date")
    tree.heading("furniture", text="Furniture")
    tree.heading("color", text="Color")
    tree.heading("size", text="Size")
    tree.heading("price", text="Price")

    # Insert all transactions into the Treeview
    for trans in transactions:
        tree.insert("", "end", values=(trans["timestamp"], trans["furniture"], trans["color"], trans["size"], trans["price"]))

def save_transactions_to_file():
    """Save all transactions to a text file."""
    if not transactions:
        messagebox.showinfo("Save Transactions", "No transactions to save.")
        return

    file_name = "data_transaksi.txt"  

    try:
        with open(file_name, 'w') as file:
            for trans in transactions:
                line = f"{trans['timestamp']}, {trans['furniture']}, {trans['color']}, {trans['size']}, {trans['price']}\n"
                file.write(line)

        messagebox.showinfo("Save Successful", f"Transactions have been saved to {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save transactions: {str(e)}")

def furniture_actions():
    """Provide a comprehensive furniture management dialog."""
    # Create a dialog window for furniture actions
    furniture_action_window = Toplevel(root)
    furniture_action_window.title("Furniture Management")
    furniture_action_window.geometry("300x250")


    # Create buttons for different furniture actions
    Button(furniture_action_window, text="View Furniture", command=view_furniture).pack(pady=5)
    Button(furniture_action_window, text="Add Furniture", command=add_furniture).pack(pady=5)
    Button(furniture_action_window, text="Edit Furniture", command=edit_furniture).pack(pady=5)
    Button(furniture_action_window, text="Delete Furniture", command=open_delete_furniture).pack(pady=5)

    # Action buttons
def view_furniture():
        """Open the furniture view window."""
        furniture_window = Toplevel(root)
        furniture_window.title("Furniture List")
        furniture_window.geometry("500x300")

    # Create Treeview to display furniture
        columns = ("Code", "Name", "Stock")
        tree = ttk.Treeview(furniture_window, columns=columns, show="headings")
        tree.heading("Code", text="Code")
        tree.heading("Name", text="Name")
        tree.heading("Stock", text="Stock")

    # Insert furniture data
        for i, name in enumerate(furniturenames):
            code = furniturecodes[i]
            stock = persediaan.get(code, 0)
            tree.insert("", "end", values=(code, name, stock))

            tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def add_furniture():
     """Open the add furniture window."""
add_window = Toplevel(root)
add_window.title("Add New Furniture")
add_window.geometry("300x200")

furniture_name_var = StringVar()
stock_var = StringVar()

Label(add_window, text="Furniture Name:").pack(pady=5)
Entry(add_window, textvariable=furniture_name_var).pack(pady=5)

Label(add_window, text="Stock Quantity:").pack(pady=5)
Entry(add_window, textvariable=stock_var).pack(pady=5)

def save_furniture():
        name = furniture_name_var.get()
        code = str(len(furniturecodes) + 1)  # Generate new code
        stock = stock_var.get()
        
        if name and stock.isdigit():
            furniturenames.append(name)
            furniturecodes.append(code)
            persediaan[code] = int(stock)
            cnames.set(furniturenames)  # Update listbox display
            
            # Save the new furniture to a text file
            with open("data_furniture.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            add_window.destroy()
            messagebox.showinfo("Success", f"{name} has been added to the inventory!")
        else:
            messagebox.showerror("Error", "Please enter a valid name and stock quantity.")
            
        Button(add_window, text="Add Furniture", command=save_furniture).pack(pady=10)    


        add_window = Toplevel(root)
        add_window.title("Add New Furniture")
        add_window.geometry("300x200")

        furniture_name_var = StringVar()
        stock_var = StringVar()

        Label(add_window, text="Furniture Name:").pack(pady=5)
        Entry(add_window, textvariable=furniture_name_var).pack(pady=5)

        Label(add_window, text="Stock Quantity:").pack(pady=5)
        Entry(add_window, textvariable=stock_var).pack(pady=5)

        Button(add_window, text="Add Furniture", command=save_furniture).pack(pady=10)

def edit_furniture():
        """Open the edit furniture window."""
        if not furniturenames:
            messagebox.showinfo("Edit Furniture", "No furniture to edit.")
        return

edit_window = Toplevel(root)
edit_window.title("Edit Furniture")
edit_window.geometry("400x300")

    # Dropdown to select furniture
selected_furniture_var = StringVar()
furniture_options = [f"{code}. {name}" for code, name in zip(furniturecodes, furniturenames)]
selected_furniture_var.set(furniture_options[0])

Label(edit_window, text="Select Furniture to Edit:").pack(pady=5)
furniture_menu = OptionMenu(edit_window, selected_furniture_var, *furniture_options)
furniture_menu.pack(pady=5)

    # Editable fields
Label(edit_window, text="New Furniture Name:").pack(pady=5)
name_var = StringVar()
Entry(edit_window, textvariable=name_var).pack(pady=5)

Label(edit_window, text="New Stock Quantity:").pack(pady=5)
stock_var = StringVar()
Entry(edit_window, textvariable=stock_var).pack(pady=5)

def load_furniture_data():
        """Load selected furniture data into edit fields."""
        code = selected_furniture_var.get().split(".")[0]
        index = furniturecodes.index(code)
        name_var.set(furniturenames[index])
        stock_var.set(str(persediaan.get(code, 0)))

def save_furniture_changes():
        """Save changes to the selected furniture item."""
        try:
            code = selected_furniture_var.get().split(".")[0]
            index = furniturecodes.index(code)
            
            new_name = name_var.get().strip()
            new_stock = int(stock_var.get())

            if new_name and new_stock >= 0:
                # Update furniture name
                furniturenames[index] = new_name
                
                # Update stock
                persediaan[code] = new_stock

                # Update listbox
                cnames.set(furniturenames)

                # Save to file (optional)
                with open("data_furniture.txt", "w") as file:
                    for code, name in zip(furniturecodes, furniturenames):
                        file.write(f"{code}:{name}\n")

                messagebox.showinfo("Success", "Furniture updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter valid name and stock.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

        Button(edit_window, text="Load Data", command=load_furniture_data).pack(pady=5)
        Button(edit_window, text="Save Changes", command=save_furniture_changes).pack(pady=10)

def open_delete_furniture():
        """Open the delete furniture window."""
        if not furniturenames:
            messagebox.showinfo("Delete Furniture", "No furniture to delete.")
            return

delete_window = Toplevel(root)
delete_window.title("Delete Furniture")
delete_window.geometry("400x200")

    # Dropdown to select furniture
selected_furniture_var = StringVar()
furniture_options = [f"{code}. {name}" for code, name in zip(furniturecodes, furniturenames)]
selected_furniture_var.set(furniture_options[0])

Label(delete_window, text="Select Furniture to Delete:").pack(pady=10)
furniture_menu = OptionMenu(delete_window, selected_furniture_var, *furniture_options)
furniture_menu.pack(pady=10)

def confirm_delete():
        """Confirm and delete the selected furniture item."""
        code = selected_furniture_var.get().split(".")[0]
        index = furniturecodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Are you sure you want to delete {furniturenames[index]}?"
        )

        if confirm:
            # Remove from lists and dictionaries
            del furniturenames[index]
            del furniturecodes[index]
            del persediaan[code]

            # Update listbox
            cnames.set(furniturenames)

            # Save updated list to file
            with open("data_furniture.txt", "w") as file:
                for code, name in zip(furniturecodes, furniturenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "Furniture item deleted.")
            delete_window.destroy()

        Button(delete_window, text="Delete Furniture", command=confirm_delete).pack(pady=20)

def color_actions():
    """Provide a comprehensive color management dialog."""
    # Create a dialog window for color actions
    color_action_window = Toplevel(root)
    color_action_window.title("Color Management")
    color_action_window.geometry("300x250")

    # Create buttons for different furniture actions
    Button(color_action_window, text="View color", command=view_color).pack(pady=5)
    Button(color_action_window, text="Add color", command=add_color).pack(pady=5)
    Button(color_action_window, text="Edit color", command=edit_color).pack(pady=5)
    Button(color_action_window, text="Delete color", command=open_delete_color).pack(pady=5)

    # Action buttons
def view_color():
        """Open the color view window."""
        color_window = Toplevel(root)
        color_window.title("Color List")
        color_window.geometry("500x300")

    # Create Treeview to display color
        columns = ("Code", "Name")
        tree = ttk.Treeview(color_window, columns=columns, show="headings")
        tree.heading("Code", text="Code")
        tree.heading("Name", text="Name")
        
    # Insert color data
        for code, name in colornames.items():
            tree.insert("", "end", values=(code,name))
            tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def add_color():
     """Open the add color window."""
add_color_window = Toplevel(root)
add_color_window.title("Add New Color")
add_color_window.geometry("300x200")

    # Variables for new color
color_code_var = StringVar()
color_name_var = StringVar()  # This will store the display name

    # Create and layout widgets
Label(add_color_window, text="Color Code:").pack(pady=5)
Entry(add_color_window, textvariable=color_code_var).pack(pady=5)

Label(add_color_window, text="Display Name:").pack(pady=5)
Entry(add_color_window, textvariable=color_name_var).pack(pady=5)

def save_color():
        name = color_name_var.get()
        code = str(len(colorcodes) + 1)  # Generate new code
        
        if name ():
            colornames.append(name)
            colorcodes.append(code)
            cnames.set(colornames)  # Update listbox display
            
            # Save the new color to a text file
            with open("data_warna.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            add_window.destroy()
            messagebox.showinfo("Success", f"{name} has been added to the inventory!")
        else:
            messagebox.showerror("Error", "Please enter a valid name.")

        add_window = Toplevel(root)
        add_window.title("Add New color")
        add_window.geometry("300x200")

        color_name_var = StringVar()
        

        Label(add_window, text="color Name:").pack(pady=5)
        Entry(add_window, textvariable=color_name_var).pack(pady=5)

        Button(add_window, text="Add color", command=save_color).pack(pady=10)

def edit_color():
        """Open the edit color window."""
        if not colornames:
            messagebox.showinfo("Edit color", "No color to edit.")
        return

edit_window = Toplevel(root)
edit_window.title("Edit color")
edit_window.geometry("400x300")

    # Dropdown to select color
selected_color_var = StringVar()
color_options = [f"{code}. {name}" for code, name in zip(colorcodes, colornames)]
selected_color_var.set(color_options[0])

Label(edit_window, text="Select color to Edit:").pack(pady=5)
color_menu = OptionMenu(edit_window, selected_color_var, *color_options)
color_menu.pack(pady=5)

    # Editable fields
Label(edit_window, text="New color Name:").pack(pady=5)
name_var = StringVar()
Entry(edit_window, textvariable=name_var).pack(pady=5)

def load_color_data():
        """Load selected color data into edit fields."""
        code = selected_color_var.get().split(".")[0]
        index = colorcodes.index(code)
        name_var.set(colornames[index])
        
def save_color_changes():
        """Save changes to the selected color item."""
        try:
            code = selected_color_var.get().split(".")[0]
            index = colorcodes.index(code)
            
            new_name = name_var.get().strip()
            
            if new_name  >= 0:
                # Update color name
                colornames[index] = new_name
                
                # Update listbox
                cnames.set(colornames)

                # Save to file (optional)
                with open("data_warna.txt", "w") as file:
                    for  name in zip(colorcodes, colornames):
                        file.write(f"{code}:{name}\n")

                messagebox.showinfo("Success", "Color updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter valid name ")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

        Button(edit_window, text="Load Data", command=load_color_data).pack(pady=5)
        Button(edit_window, text="Save Changes", command=save_color_changes).pack(pady=10)
        
def open_delete_color():
        """Open the delete color window."""
        if not colornames:
            messagebox.showinfo("Delete color", "No color to delete.")
            return

delete_window = Toplevel(root)
delete_window.title("Delete color")
delete_window.geometry("400x200")

    # Dropdown to select color
selected_color_var = StringVar()
color_options = [f"{code}. {name}" for code, name in zip(colorcodes, colornames)]
selected_color_var.set(color_options[0])

Label(delete_window, text="Select Color to Delete:").pack(pady=10)
color_menu = OptionMenu(delete_window, selected_color_var, *color_options)
color_menu.pack(pady=10)

def confirm_delete():
        """Confirm and delete the selected color item."""
        code = selected_color_var.get().split(".")[0]
        index = colorcodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Are you sure you want to delete {colornames[index]}?"
        )

        if confirm:
            # Remove from lists and dictionaries
            del colornames[index]
            del colorcodes[index]
            

            # Update listbox
            cnames.set(colornames)

            # Save updated list to file
            with open("data_warna.txt", "w") as file:
                for code, name in zip(colorcodes, colornames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "color item deleted.")
            delete_window.destroy()

        Button(delete_window, text="Delete color", command=confirm_delete).pack(pady=20)

def size_actions():
    """Provide a comprehensive size management dialog."""
    # Create a dialog window for size actions
    size_action_window = Toplevel(root)
    size_action_window.title("Size Management")
    size_action_window.geometry("300x250")

    # Create buttons for different furniture actions
    Button(size_action_window, text="View size", command=view_size).pack(pady=5)
    Button(size_action_window, text="Add size", command=add_size).pack(pady=5)
    Button(size_action_window, text="Edit size", command=edit_size).pack(pady=5)
    Button(size_action_window, text="Delete size", command=open_delete_size).pack(pady=5)

    # Action buttons
def view_size():
        """Open the size view window."""
        size_window = Toplevel(root)
        size_window.title("Size List")
        size_window.geometry("500x300")

    # Create Treeview to display size
        columns = ("Code", "Name")
        tree = ttk.Treeview(size_window, columns=columns, show="headings")
        tree.heading("Code", text="Code")
        tree.heading("Name", text="Name")
        
    # Insert size data
        for code, name in sizenames.items():
            tree.insert("", "end", values=(code, name))

            tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def add_size():
     """Open the add size window."""
add_size_window = Toplevel(root)
add_size_window.title("Add New Size")
add_size_window.geometry("300x200")

    # Variables for new size
size_code_var = StringVar()
size_name_var = StringVar()  # This will store the display name

    # Create and layout widgets
Label(add_size_window, text="Size Code:").pack(pady=5)
Entry(add_size_window, textvariable=size_code_var).pack(pady=5)

Label(add_size_window, text="Display Name:").pack(pady=5)
Entry(add_size_window, textvariable=size_name_var).pack(pady=5)

def save_size():
        name = size_name_var.get()
        code = str(len(sizecodes) + 1)  # Generate new code
       
        
        if name():
            sizenames.append(name)
            sizecodes.append(code)
            cnames.set(sizenames)  # Update listbox display
            
            # Save the new size to a text file
            with open("data_ukuran.txt", "a") as file:
                file.write(f"{code}:{name}\n")

            add_window.destroy()
            messagebox.showinfo("Success", f"{name} has been added to the inventory!")
        else:
            messagebox.showerror("Error", "Please enter a valid name.")

        add_window = Toplevel(root)
        add_window.title("Add New Size")
        add_window.geometry("300x200")

        size_name_var = StringVar()

        Label(add_window, text="Size Name:").pack(pady=5)
        Entry(add_window, textvariable=size_name_var).pack(pady=5)

        Button(add_window, text="Add Size", command=save_size).pack(pady=10)

def edit_size():
        """Open the edit size window."""
        if not sizenames:
            messagebox.showinfo("Edit Size", "No size to edit.")
        return

edit_window = Toplevel(root)
edit_window.title("Edit size")
edit_window.geometry("400x300")

    # Dropdown to select furniture
selected_size_var = StringVar()
size_options = [f"{code}. {name}" for code, name in zip(sizecodes, sizenames)]
selected_size_var.set(size_options[0])

Label(edit_window, text="Select Size to Edit:").pack(pady=5)
size_menu = OptionMenu(edit_window, selected_size_var, *size_options)
size_menu.pack(pady=5)

    # Editable fields
Label(edit_window, text="New Size Name:").pack(pady=5)
name_var = StringVar()
Entry(edit_window, textvariable=name_var).pack(pady=5)

def load_size_data():
        """Load selected size data into edit fields."""
        code = selected_size_var.get().split(".")[0]
        index = sizecodes.index(code)
        name_var.set(sizenames[index])
       
def save_size_changes():
        """Save changes to the selected size item."""
        try:
            code = selected_size_var.get().split(".")[0]
            index = sizecodes.index(code)
            
            new_name = name_var.get().strip()
            if new_name >= 0:
                # Update furniture name
                sizenames[index] = new_name
                
                # Update listbox
                cnames.set(sizenames)

                # Save to file (optional)
                with open("data_ukuran.txt", "w") as file:
                    for code, name in zip(sizecodes, sizenames):
                        file.write(f"{code}:{name}\n")

                messagebox.showinfo("Success", "Size updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter valid name.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

        Button(edit_window, text="Load Data", command=load_size_data).pack(pady=5)
        Button(edit_window, text="Save Changes", command=save_size_changes).pack(pady=10)
        

def open_delete_size():
        """Open the delete size window."""
        if not sizenames:
            messagebox.showinfo("Delete Size", "No size to delete.")
            return

delete_window = Toplevel(root)
delete_window.title("Delete Size")
delete_window.geometry("400x200")

    # Dropdown to select furniture
selected_size_var = StringVar()
size_options = [f"{code}. {name}" for code, name in zip(sizecodes, sizenames)]
selected_size_var.set(size_options[0])

Label(delete_window, text="Select Size to Delete:").pack(pady=10)
size_menu = OptionMenu(delete_window, selected_size_var, *size_options)
size_menu.pack(pady=10)

def confirm_delete():
        """Confirm and delete the selected furniture item."""
        code = selected_size_var.get().split(".")[0]
        index = sizecodes.index(code)

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Are you sure you want to delete {sizenames[index]}?"
        )

        if confirm:
            # Remove from lists and dictionaries
            del sizenames[index]
            del sizecodes[index]

            # Update listbox
            cnames.set(sizenames)

            # Save updated list to file
            with open("data_ukuran.txt", "w") as file:
                for code, name in zip(sizecodes, sizenames):
                    file.write(f"{code}:{name}\n")

            messagebox.showinfo("Delete Successful", "Size item deleted.")
            delete_window.destroy()

        Button(delete_window, text="Delete Size", command=confirm_delete).pack(pady=20)

# Placeholder functions for menu actions
def open_main_menu():
    show_frame(main_frame)

def exit_app():
    root.quit()

def add_transaction():
    add_furniture()

def edit_transaction():
    if not transactions:
        messagebox.showinfo("Edit Transaction", "No transactions to edit.")
        return

    # Create a new window to select and edit a transaction
    edit_window = Toplevel(root)
    edit_window.title("Edit Transaction")
    edit_window.geometry("400x300")

    # Dropdown to select transaction
    selected_transaction_var = StringVar()
    transaction_options = [f"{i+1}. {t['furniture']} - {t['size']} - {t['color']} - {t['price']}" for i, t in enumerate(transactions)]
    selected_transaction_var.set(transaction_options[0])  # Default to the first transaction

    Label(edit_window, text="Select Transaction to Edit:").pack(pady=5)
    transaction_menu = OptionMenu(edit_window, selected_transaction_var, *transaction_options)
    transaction_menu.pack(pady=5)

    # Editable fields for transaction details
    Label(edit_window, text="Furniture Name:").pack(pady=5)
    furniture_name_var = StringVar()
    Entry(edit_window, textvariable=furniture_name_var).pack(pady=5)

    Label(edit_window, text="Furniture Code:").pack(pady=5)
    furniture_code_var = StringVar()
    Entry(edit_window, textvariable=furniture_code_var).pack(pady=5)

    Label(edit_window, text="Stock Quantity:").pack(pady=5)
    stock_var = StringVar()
    Entry(edit_window, textvariable=stock_var).pack(pady=5)

    Label(edit_window, text="Price:").pack(pady=5)
    price_var = StringVar()
    Entry(edit_window, textvariable=price_var).pack(pady=5)

    # Function to load selected transaction data
    def load_selected_transaction():
        index = int(selected_transaction_var.get().split(".")[0]) - 1
        selected_transaction = transactions[index]

        furniture_name_var.set(selected_transaction["furniture"])
        furniture_code_var.set(furniturecodes[furniturenames.index(selected_transaction["furniture"])])
        stock_var.set(persediaan[furniture_code_var.get()])
        price_var.set(selected_transaction["price"])

    # Button to load data of selected transaction
    Button(edit_window, text="Load Data", command=load_selected_transaction).pack(pady=5)

    # Save changes made to the transaction
    def save_edited_transaction():
        try:
            index = int(selected_transaction_var.get().split(".")[0]) - 1
            edited_furniture_name = furniture_name_var.get()
            edited_code = furniture_code_var.get()
            edited_stock = int(stock_var.get())  # Ensure stock is an integer
            edited_price = price_var.get()

            # Update the transaction data
            transactions[index]["furniture"] = edited_furniture_name
            transactions[index]["price"] = edited_price

            # Update furniture database as well
            if edited_code in furniturecodes:
                furniturenames[furniturecodes.index(edited_code)] = edited_furniture_name
                persediaan[edited_code] = edited_stock
            else:
                messagebox.showerror("Error", "Invalid furniture code.")

            messagebox.showinfo("Edit Successful", "Transaction has been successfully updated.")
            edit_window.destroy()  # Close the edit window after saving

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data for all fields.")

    Button(edit_window, text="Save Changes", command=save_edited_transaction).pack(pady=20)

# Usage: Attach the new edit_transaction function to the help menu.
    data_mastering_menu.add_command(label="Edit Transaction", command=edit_transaction)


def delete_transaction():
    if not transactions:
        messagebox.showinfo("Delete Transaction", "No transactions to delete.")
        return

    # Membuat list pilihan transaksi berdasarkan deskripsi (nama furniture dan rincian lain)
    transaction_options = [f"{i+1}. {t['furniture']} - {t['size']} - {t['color']} - {t['price']}" for i, t in enumerate(transactions)]
    
    # Membuka jendela dialog untuk memilih transaksi yang ingin dihapus
    delete_window = Toplevel(root)
    delete_window.title("Delete Transaction")
    delete_window.geometry("400x200")

    Label(delete_window, text="Pilih transaksi yang ingin dihapus:").pack(pady=10)
    
    selected_transaction_var = StringVar()
    selected_transaction_var.set(transaction_options[0])  # Default ke transaksi pertama

    # Dropdown menu untuk memilih transaksi
    transaction_menu = OptionMenu(delete_window, selected_transaction_var, *transaction_options)
    transaction_menu.pack(pady=10)

    # Fungsi untuk menghapus transaksi yang dipilih
    def confirm_delete():
        selected_index = int(selected_transaction_var.get().split(".")[0]) - 1
        selected_transaction = transactions[selected_index]

        confirm = messagebox.askyesno(
            "Delete Confirmation", 
            f"Apakah Anda yakin ingin menghapus transaksi ini?\n{selected_transaction['furniture']} - {selected_transaction['size']} - {selected_transaction['color']} - {selected_transaction['price']}"
        )

        if confirm:
            transactions.pop(selected_index)  # Hapus transaksi yang dipilih
            messagebox.showinfo("Delete Successful", "Transaksi berhasil dihapus.")
            delete_window.destroy()  # Tutup dialog setelah transaksi dihapus

    Button(delete_window, text="Delete Transaction", command=confirm_delete).pack(pady=20)


# Create and grid the outer content frame
c = ttk.Frame(main_frame, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create widgets
lbox = Listbox(c, listvariable=cnames, height=5)
lbl_color = ttk.Label(c, text="Pilih warna furniture:")
lbl_size = ttk.Label(c, text="Pilih ukuran:")

# Color radio buttons
g1 = ttk.Radiobutton(c, text='Merah', variable=selected_color, value='merah')
g2 = ttk.Radiobutton(c, text='Biru', variable=selected_color, value='biru')
g3 = ttk.Radiobutton(c, text='Kuning', variable=selected_color, value='kuning')
g4 = ttk.Radiobutton(c, text='Hijau', variable=selected_color, value='hijau')

# Size radio buttons
s1 = ttk.Radiobutton(c, text='Big', variable=selected_size, value='big')
s2 = ttk.Radiobutton(c, text='Medium', variable=selected_size, value='medium')
s3 = ttk.Radiobutton(c, text='Small', variable=selected_size, value='small')

send = ttk.Button(c, text='Send to cart', command=sendtocart, default='active')
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

# Grid the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N, S, E, W))

# Grid for color options
lbl_color.grid(column=1, row=0, padx=10, pady=5, sticky=W)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
g4.grid(column=1, row=4, sticky=W, padx=20)

# Grid for size options (beside color options)
lbl_size.grid(column=2, row=0, padx=10, pady=5, sticky=W)
s1.grid(column=2, row=1, sticky=W, padx=20)
s2.grid(column=2, row=2, sticky=W, padx=20)
s3.grid(column=2, row=3, sticky=W, padx=20)

send.grid(column=2, row=4, sticky=E)
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=6, columnspan=2, sticky=(W, E))

# Configure grid resizing
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# Set event bindings
lbox.bind('<<ListboxSelect>>', showPersediaan)
lbox.bind('<Double-1>', sendtocart)
root.bind('<Return>', sendtocart)

# Attach frames to the root window
for frame in (login_frame, welcome_frame, main_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Create the menu bar
menubar = Menu(root)

# File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Main Menu", command=open_main_menu)
file_menu.add_command(label="Open Transaction", command=open_transactions)
file_menu.add_command(label="Save Transactions", command=save_transactions_to_file)  # Added this line
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Data mastering Menu
data_mastering_menu = Menu(menubar, tearoff=0)
data_mastering_menu.add_command(label="Furniture", command= furniture_actions)
data_mastering_menu.add_command(label="Color", command= color_actions)
data_mastering_menu.add_command(label="Size", command= size_actions)  
data_mastering_menu.add_command(label="Delete Transaction", command=delete_transaction)
menubar.add_cascade(label="Data Mastering", menu=data_mastering_menu)

# Attach the menu bar to the root window
root.config(menu=menubar)

# Show the login frame initially
show_frame(login_frame)

# Start the GUI loop
root.mainloop()
