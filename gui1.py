import tkinter as tk
from tkinter import messagebox, Canvas
from datamanager import DataManager

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Furniture")
        self.geometry("400x400")
        self.data_manager = DataManager()
        self.current_data_type = 'warna'

        self.create_frames()
        self.create_widgets()
        self.show_home()

    def create_frames(self):
        self.home_frame = tk.Frame(self)
        self.furniture_frame = tk.Frame(self)
        self.warna_frame = tk.Frame(self)
        self.ukuran_frame = tk.Frame(self)
        self.warna_tambah_frame = tk.Frame(self)
        self.ukuran_tambah_frame = tk.Frame(self)
        self.furniture_tambah_frame = tk.Frame(self)
        self.detail_frame = tk.Frame(self)
        self.edit_frame = tk.Frame(self)

    def create_widgets(self):
        # Home frame widgets
        canvas = Canvas(self.home_frame, width=400, height=150, bg="#FFA559", highlightthickness=0)
        canvas.create_text(200, 75, text="DATA FURNITURE", font=("Helvetica", 24, "bold"), fill="white")
        canvas.pack()

        frame = tk.Frame(self.home_frame)
        frame.pack(pady=20)

        button_furniture = tk.Button(
            frame, text="Furniture", font=("Helvetica", 12), bg="green", fg="white",
            padx=20, pady=10, command=lambda: self.show_data('furniture')
        )
        button_furniture.grid(row=0, column=0, padx=20)

        button_ukuran = tk.Button(
            frame, text="Ukuran", font=("Helvetica", 12), bg="purple", fg="white",
            padx=20, pady=10, command=lambda: self.show_data('ukuran')
        )
        button_ukuran.grid(row=0, column=1, padx=20)

        button_warna = tk.Button(
            frame, text="Warna", font=("Helvetica", 12), bg="red", fg="white",
            padx=20, pady=10, command=lambda: self.show_data('warna')
        )
        button_warna.grid(row=0, column=2, padx=20)

        # Data frames (Furniture, Warna, Ukuran)
        for data_type, frame, title in [
            ('furniture', self.furniture_frame, "List Furniture"),
            ('warna', self.warna_frame, "List Warna"),
            ('ukuran', self.ukuran_frame, "List Ukuran")
        ]:
            label = tk.Label(frame, text=title, font=("Helvetica", 16))
            label.pack(pady=10)

            listbox = tk.Listbox(frame, width=40, height=10)
            listbox.pack(pady=10)
            listbox.bind("<Double-1>", self.show_detail)

            edit_button = tk.Button(frame, text="Edit", command=lambda f=frame: self.show_edit_dialog(f))
            edit_button.pack(side=tk.LEFT, padx=5, pady=5)

            add_button = tk.Button(frame, text="+", command=lambda dt=data_type: self.show_add_frame(dt))
            add_button.pack(side=tk.LEFT, padx=5, pady=5)

            delete_button = tk.Button(frame, text="-", command=lambda dt=data_type: self.delete_action(dt))
            delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

            back_button = tk.Button(frame, text="Kembali", command=self.show_home)
            back_button.pack(pady=10)

            if data_type == 'furniture':
                detail_button = tk.Button(frame, text="Tampilkan Detail", command=self.show_furniture_detail)
                detail_button.pack(pady=5)

        # Add item frames
        self.create_add_frames()

        # Detail frame
        self.detail_label = tk.Label(self.detail_frame, text="", font=("Helvetica", 12))
        self.detail_label.pack(pady=10)

        back_button = tk.Button(self.detail_frame, text="Kembali", command=self.show_data)
        back_button.pack(pady=10)

    def create_add_frames(self):
        # Warna add frame
        label = tk.Label(self.warna_tambah_frame, text="Tambah Warna Baru", font=("Helvetica", 12))
        label.pack(pady=5)

        self.warna_entry = tk.Entry(self.warna_tambah_frame, width=30)
        self.warna_entry.pack(pady=5)

        tambah_button = tk.Button(self.warna_tambah_frame, text="Tambah", command=self.tambah_warna)
        tambah_button.pack(pady=10)

        # Ukuran add frame
        label = tk.Label(self.ukuran_tambah_frame, text="Tambah Ukuran Baru", font=("Helvetica", 12))
        label.pack(pady=5)

        self.ukuran_entry = tk.Entry(self.ukuran_tambah_frame, width=30)
        self.ukuran_entry.pack(pady=5)

        tambah_button = tk.Button(self.ukuran_tambah_frame, text="Tambah", command=self.tambah_ukuran)
        tambah_button.pack(pady=10)

        # Furniture add frame
        label = tk.Label(self.furniture_tambah_frame, text="Tambah Furniture Baru", font=("Helvetica", 12))
        label.pack(pady=5)

        self.nama_furniture_entry = tk.Entry(self.furniture_tambah_frame, width=30)
        self.nama_furniture_entry.pack(pady=5)

        self.ukuran_var = tk.StringVar()
        self.warna_var = tk.StringVar()

        label = tk.Label(self.furniture_tambah_frame, text="Pilih Ukuran", font=("Helvetica", 10))
        label.pack(pady=5)

        self.ukuran_option = tk.OptionMenu(self.furniture_tambah_frame, self.ukuran_var, *self.data_manager.list_data('ukuran').keys())
        self.ukuran_option.pack(pady=5)

        label = tk.Label(self.furniture_tambah_frame, text="Pilih Warna", font=("Helvetica", 10))
        label.pack(pady=5)

        self.warna_option = tk.OptionMenu(self.furniture_tambah_frame, self.warna_var, *self.data_manager.list_data('warna').keys())
        self.warna_option.pack(pady=5)

        tambah_button = tk.Button(self.furniture_tambah_frame, text="Tambah", command=self.tambah_furniture)
        tambah_button.pack(pady=10)

    def show_add_frame(self, data_type):
        self.hide_all_frames()
        if data_type == 'warna':
            self.warna_tambah_frame.pack()
        elif data_type == 'ukuran':
            self.ukuran_tambah_frame.pack()
        elif data_type == 'furniture':
            self.furniture_tambah_frame.pack()

    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack()

    def show_data(self, data_type=None):
        self.hide_all_frames()
        if data_type:
            self.current_data_type = data_type

        if data_type == 'furniture':
            self.furniture_frame.pack()
        elif data_type == 'warna':
            self.warna_frame.pack()
        elif data_type == 'ukuran':
            self.ukuran_frame.pack()

        self.update_listbox(data_type)

    def hide_all_frames(self):
        for frame in (
            self.home_frame, self.furniture_frame, self.warna_frame, self.ukuran_frame,
            self.warna_tambah_frame, self.ukuran_tambah_frame, self.furniture_tambah_frame,
            self.detail_frame, self.edit_frame
        ):
            frame.pack_forget()

    def update_listbox(self, data_type):
        listbox = self.get_current_listbox(data_type)
        listbox.delete(0, tk.END)
        data_dict = self.data_manager.list_data(data_type)
        for key, value in data_dict.items():
            listbox.insert(tk.END, f"{key}: {value}")

    def get_current_listbox(self, data_type):
        if data_type == 'warna':
            return self.warna_frame.winfo_children()[1]
        elif data_type == 'ukuran':
            return self.ukuran_frame.winfo_children()[1]
        else:
            return self.furniture_frame.winfo_children()[1]

    def tambah_warna(self):
        warna = self.warna_entry.get()
        if not warna:
            messagebox.showerror("Error", "Warna tidak boleh kosong!")
        else:
            self.data_manager.tambah_warna(warna)
            self.update_listbox('warna')
            self.warna_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
