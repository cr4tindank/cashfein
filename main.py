from fungsi import Warna, Ukuran, Furniture, Transaction, Stock, Price, datetime

def main():
    # Create instances of the classes
    warna_handler = Warna()
    ukuran_handler = Ukuran()
    furniture_handler = Furniture()
    transaksi_handler = Transaction()
    price_handler = Price()
    stock_handler = Stock()

    # Initialize a list to store transactions
    transactions = []

    # Main loop for the application
    while True:
        print("\n (∩˃o˂∩)★")
        print(" Torica Furniture Store .•*¨*•.¸¸♪=")
        print("1. View Data")
        print("2. Add New Data")
        print("3. Delete Data")
        print("4. Edit Data")
        print("5. Add New Transaction")
        print("6. Delete Transaction")
        print("7. View Transaction")
        print("8. Exit")
        pilihan = input("Enter your choice (1-8): ")

        if pilihan == '1':  # View data
            print("\n=== View Data ===")
            print("1. View Color Data")
            print("2. View Size Data")
            print("3. View Furniture Data")
            print("4. View Price Data")
            print('5. View Stock Data')
            pilihan_lihat = input("Enter your choice (1-5): ")
            if pilihan_lihat == '1':
                    data_dict = warna_handler.list_warna()
                    print("\nColor Data:")
                    print(data_dict)
                
            elif pilihan_lihat == '2':
                    data_dict = ukuran_handler.list_ukuran()
                    print("\nSize Data:")
                    print(data_dict)

            elif pilihan_lihat == '3':
                    data_dict = furniture_handler.list_furniture()
                    print(data_dict)

            elif pilihan_lihat == '4':
                    data_dict = price_handler.list_price()
                    print(data_dict)
            
            elif pilihan_lihat == '5':
                    data_dict = stock_handler.list_stock()
                    print(data_dict)
            else:
                    print("Invalid choice.")

        elif pilihan == '2':  # Add new data
            print("\n=== Add New Data ===")
            print("1. Add Color")
            print("2. Add Size")
            print("3. Add Furniture")
            print("4. Add Price")
            print("5. Add Stock")
            pilihan_tambah = input("Enter your choice (1-5): ")
        
            if pilihan_tambah == '1':
                    new_data= input("Enter new color: ")
                    warna_handler.tambah_warna(new_data)
                    print(f"Color '{new_data}' has been successfully added.")
                
            elif pilihan_tambah == '2':
                    new_data = input("Enter new size: ")
                    ukuran_handler.tambah_ukuran(new_data)
                    print(f"Size '{new_data}' has been successfully added.")
                
            elif pilihan_tambah == '3':
                    new_data = input("Enter new furniture: ")
                    furniture_handler.tambah_furniture(new_data)
                    print(f"Furniture '{new_data}' has been successfully added.")
                
            elif pilihan_tambah == '4':
                new_data = input("Enter price: ")
                price_handler.tambah_price(new_data)
                print(f"Price '{new_data}' has been successfully added.")

            elif pilihan_tambah == '5':
                new_data = input("Enter stock: ")
                stock_handler.tambah_stock(new_data)
                print(f"Stock {new_data}' has been successfully added.")

            else:
                    print("Invalid choice.")

        elif pilihan == '3':  # Delete data
            print("\n Delete Data -ˋˏ✄┈┈┈┈")
            print("1. Delete Color")
            print("2. Delete Size")
            print("3. Delete Furniture")
            print("4. Delete Price")
            print("5. Delete Stock")
            pilihan_hapus = input("Enter your choice (1-5): ")

            if pilihan_hapus == '1':
                    id_hapus = input("Enter Color ID to delete: ")
                    if warna_handler.hapus_warna(id_hapus):
                        print(f"Color with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Color ID '{id_hapus}' not found.")
                
            elif pilihan_hapus == '2':
                    id_hapus = input("Enter Size ID to delete: ")
                    if ukuran_handler.hapus_ukuran(id_hapus):
                        print(f"Size with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Size ID '{id_hapus}' not found.")
                
            elif pilihan_hapus == '3':
                    id_hapus = input("Enter Furniture ID to delete: ")
                    if furniture_handler.hapus_furniture(id_hapus):
                        print(f"Furniture with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Furniture ID '{id_hapus}' not found.")

            elif pilihan_hapus == '4':
                    id_hapus = input("Enter Price ID to delete: ")
                    if price_handler.hapus_price(id_hapus):
                        print(f"Price with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Price ID '{id_hapus}' not found.")

            elif pilihan_hapus == '5':
                    id_hapus = input("Enter Price ID to delete: ")
                    if stock_handler.hapus_stock(id_hapus):
                        print(f"Stock with ID '{id_hapus}' has been successfully deleted.")
                    else:
                        print(f"Stock ID '{id_hapus}' not found.")
            else:
                    print("Invalid choice.")
        
        elif pilihan == '4':  # Edit Data
            print("\n=== Edit Data ===")
            print("1. Edit Color")
            print("2. Edit Size")
            print("3. Edit Furniture")
            print("4. Edit Price")
            print("5. Edit Stock")
            pilihan_edit = input("Enter your choice (1-5): ")

            if pilihan_edit == '1':
                    id_edit = input("Enter Color ID to edit: ")
                    if warna_handler.edit_warna(id_edit):
                        print(f"Color with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Color ID '{id_edit}' not found.")
                
            elif pilihan_edit == '2':
                    id_edit = input("Enter Size ID to edit: ")
                    if ukuran_handler.edit_ukuran(id_edit):
                        print(f"Size with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Size ID '{id_edit}' not found.")
                
            elif pilihan_edit == '3':
                    id_edit = input("Enter Furniture ID to edit: ")
                    if furniture_handler. edit_furniture(id_edit):
                        print(f"Furniture with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Furniture ID '{id_edit}' not found.")
                
            elif pilihan_edit == '4':
                    id_edit = input("Enter Price ID to edit: ")
                    if price_handler. edit_price(id_edit):
                        print(f"Price with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Price ID '{id_edit}' not found.")

            elif pilihan_edit == '5':
                    id_edit = input("Enter Stock ID to edit: ")
                    if stock_handler. edit_stock(id_edit):
                        print(f"Stock with ID '{id_edit}' has been successfully edited.")
                    else:
                        print(f"Stock ID '{id_edit}' not found.")
            else:
                    print("Invalid choice.")
           
        elif pilihan == '5':  # Add new transaction
            print("\n=== Add New Transaction ===")
            color_code =input ("Add the code color: ")
            furniture_code = input("Add the code furniture: ")
            size_code = input("Add the size code: ")
            price_code = input ("Add the price code: ")
            stock_code = input ("Add the stock code: ")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
 
                # Changed this line to pass only 3 arguments (plus self makes 4)
            transaksi = transaksi_handler.tambah_transaksi(furniture_code, color_code, size_code,price_code,stock_code)

            new_transaction = {
                    "timestamp": timestamp,
                    "furniture": furniture_code,
                    "color": color_code,
                    "size": size_code,
                    "price": price_code,
                    "stock":stock_code
                    }
            transactions.append(new_transaction)
            print(f"Transaction successfully added: {new_transaction}")
            
        
        elif pilihan == '6':  # Delete transaction
            print("\n=== Delete Transaction ===")
            if transactions:
                print("Available Transactions:")
                for idx, trans in enumerate(transactions):
                    print(f"{idx}. {trans}")
                
                try:
                    index = int(input("Enter transaction index to delete: "))
                    if 0 <= index < len(transactions):
                        deleted_transaction = transactions.pop(index)
                        print(f"Transaction successfully deleted: {deleted_transaction}")
                    else:
                        print("Invalid transaction index.")
                except ValueError:
                    print("Please enter a valid index number.")
            else:
                print("No transactions available.")

        elif pilihan == '7':  # View transactions
            print("\n=== Transaction History ===")
            if transactions:
                for idx, transaction in enumerate(transactions):
                    print(f"\nTransaction {idx}:")
                    print(f"Timestamp: {transaction['timestamp']}")
                    print(f"Furniture: {transaction['furniture']}")
                    print(f"Color: {transaction['color']}")
                    print(f"Size: {transaction['size']}")
                    print(f"Price: {transaction['price']}")
                    print(f"Stock: {transaction['stock']}")
            else:
                print("No transactions available.")

        elif pilihan == '8':  # Exit
            print("\nThank you for visiting our store ♪¸¸.•*¨*•.!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
