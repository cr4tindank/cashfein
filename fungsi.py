import os
from pathlib import Path
from datetime import datetime


class FileHandler:
    def __init__(self, directory=None):
        self.current_directory = directory or os.path.dirname(os.path.abspath(__file__))

    def bacafile(self, nama_file):
        # Membaca file dan mengembalikan isinya sebagai string. Jika file tidak ditemukan, mengembalikan None.
        file_path = Path(self.current_directory) / nama_file
        try:
            with open(str(file_path), 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def editfile(self, nama_file, data, mode='w'):
        #Menulis data ke file dengan mode tertentu 
        file_path = Path(self.current_directory) / nama_file
        with open(str(file_path), mode) as file:
            file.write(data)


class DataItem:
    def __init__(self, file_name, jenis_data, file_handler=None):
        self.file_name = file_name
        self.jenis_data = jenis_data
        self.file_handler = file_handler or FileHandler()

    def parse_dictionary(self, data):
        #Mengonversi data teks ke dictionary, mengabaikan baris pertama (header).
        dict_result = {}
        lines = data.splitlines()
        for line in lines[1:]:  # Abaikan header
            if ':' in line:
                key, value = line.split(':', 1)
                dict_result[key.strip()] = value.strip()
        return dict_result

    def _tulis_kembali_data(self, data_dict):
        #Menulis ulang data dari dictionary ke file dengan format 'Data: Value'.
        content = f"DATA_{self.jenis_data.upper()}\n"
        content += "\n".join(f"{data_key}:{data_value}" for data_key, data_value in data_dict.items())
        self.file_handler.editfile(self.file_name, content)


class Warna(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_warna.txt', 'warna', file_handler)

    def list_warna(self):
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_warna(self, warna):
        data_dict = self.list_warna()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = warna
        self._tulis_kembali_data(data_dict)
        return new_key

    def hapus_warna(self, data_key):
        data_dict = self.list_warna()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_warna(self, data_key):
        data_dict = self.list_warna()
        if data_key in data_dict:
            new_warna = input(f"Enter new color for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_warna
            self._tulis_kembali_data(data_dict)
            return True
        return False


class Ukuran(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_ukuran.txt', 'ukuran', file_handler)
    
    def list_ukuran(self):
        #Return all size data from file
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_ukuran(self, ukuran):
        data_dict = self.list_ukuran()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = ukuran
        self._tulis_kembali_data(data_dict)
        return new_key
    
    def hapus_ukuran(self, data_key):
        data_dict = self.list_ukuran()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False 
    
    def edit_ukuran(self, data_key):
        data_dict = self.list_ukuran()
        if data_key in data_dict:
            new_ukuran = input(f"Enter new size for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_ukuran
            self._tulis_kembali_data(data_dict)
            return True
        return False


class Furniture(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_furniture.txt', 'furniture', file_handler)
    
    def list_furniture(self):
        #Return all furniture data from file
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_furniture(self, furniture):
        data_dict = self.list_furniture()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = furniture
        self._tulis_kembali_data(data_dict)
        return new_key
    
    def hapus_furniture(self, data_key):
        data_dict = self.list_furniture()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_furniture(self, data_key):
        data_dict = self.list_furniture()
        if data_key in data_dict:
            new_furniture = input(f"Enter new furniture for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_furniture
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Stock (DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_stock.txt', 'stock', file_handler)

    def list_stock(self):
        #Return all stock data from file
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_stock(self, stock):
        data_dict = self.list_stock()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = stock
        self._tulis_kembali_data(data_dict)
        return new_key
    
    def hapus_stock(self, data_key):
        data_dict = self.list_stock()
        if data_key in data_dict:
            del data_dict[data_key]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_stock(self, data_key):
        data_dict = self.list_stock()
        if data_key in data_dict:
            new_stock = input(f"Enter new stock for ID {data_key} (current: {data_dict[data_key]}): ")
            data_dict[data_key] = new_stock
            self._tulis_kembali_data(data_dict)
            return True
        return False

class Price(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_harga.txt', 'price', file_handler)
        self.prices = {}  # Dictionary to store prices
        
    
    def list_price(self):
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)
    
    def tambah_price(self, price):
        data_dict = self.list_price()
        new_key = str(max(map(int, data_dict.keys()), default=0) + 1)
        data_dict[new_key] = price
        self._tulis_kembali_data(data_dict)
        return new_key
        
    def hapus_price(self, furniture_id):
        data_dict = self.list_price()
        if str(furniture_id) in data_dict:
            del data_dict[str(furniture_id)]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
    def edit_price(self, price_id):
        if price_id not in self.prices:
            print(f"Price ID '{price_id}' not found.")
            return False
            
        current_price = self.prices[price_id]
        print(f"Current price: {current_price:,.2f}")
        
        new_price_str = input("Enter new price: ")
        new_price = self.format_price(new_price_str)
        
        if new_price is None:
            print("Invalid price format. Please enter numbers only (e.g., 1500000 or 1500000.50)")
            return False
            
        if new_price <= 0:
            print("Price must be greater than 0")
            return False
            
        self.prices[price_id] = new_price
        print(f"Price updated successfully to: {new_price:,.2f}")
        return True

    
    def get_price(self, furniture_id):
        data_dict = self.list_price()
        return data_dict.get(str(furniture_id))


class Transaction(DataItem):
    def __init__(self, file_handler=None):
        super().__init__('data_transaksi.txt', 'transaksi', file_handler)
        

    def list_transaksi(self):
        data = self.file_handler.bacafile(self.file_name) or ""
        return self.parse_dictionary(data)

    def tambah_transaksi(self, furniture_code, color_code, size_code, price_code, stock_code):
        data_dict = self.list_transaksi()
        new_key = str(max((int(k) for k in data_dict.keys() if k.isdigit()), default=0) + 1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # Store transaction data as a formatted string
        transaction_details = f"Timestamp: {timestamp}, Furniture: {furniture_code}, Color: {color_code}, Size: {size_code}, Price: {price_code}, Stock: {stock_code}"
        data_dict[new_key] = transaction_details
        self._tulis_kembali_data(data_dict)
        return new_key


    def hapus_transaksi(self, trans_id):
        data_dict = self.list_transaksi()
        if trans_id in data_dict:
            del data_dict[trans_id]
            self._tulis_kembali_data(data_dict)
            return True
        return False
    
class DateTimeHandler:
    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_date(date_str, current_format="%Y-%m-%d", desired_format="%d-%m-%Y"):
        date_obj = datetime.strptime(date_str, current_format)
        return date_obj.strftime(desired_format)
