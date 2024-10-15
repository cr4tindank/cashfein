from fungsi import baca_file, parse_dictionary, tambah_data, hapus_data, data_furniture


def main():
    # Main loop for the application
    while True:
        print("\n==== Menu Utama ====")
        print("1. Lihat Data")
        print("2. Tambah warna dan Ukuran")
        print("3. Hapus Data")
        print("4. Buat data furniture")
        print("5. Keluar Aplikasi")
        pilihan = input("Pilih opsi (1/2/3/4/5): ")

        if pilihan == '1':
            print("\n1. Lihat Data Warna")
            print("2. Lihat Data Ukuran")
            print("3. Lihat Data Furniture")
            pilihan_lihat = input("Pilihan: ")
            if pilihan_lihat == '1':
                try:
                    isi = baca_file(nama_file="idwarna.txt")
                    data_dict = parse_dictionary(isi)
                    print("\nData Warna yang dibaca adalah Dictionary:")
                    print(data_dict)
                except FileNotFoundError:
                    print("File idwarna.txt tidak ditemukan.")
            elif pilihan_lihat == '2':
                try:
                    isi = baca_file(nama_file="idukuran.txt")
                    data_dict = parse_dictionary(isi)
                    print("\nData Ukuran yang dibaca adalah Dictionary:")
                    print(data_dict)
                except FileNotFoundError:
                    print("File idukuran.txt tidak ditemukan.")
            elif pilihan_lihat == '3':
                try:
                    isi = baca_file(nama_file="idfurniture.txt")
                    data_dict = parse_dictionary(isi)
                    print("\nData Furniture yang dibaca adalah Dictionary:")
                    print(data_dict)
                except FileNotFoundError:
                    print("File idfurniture.txt tidak ditemukan.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '2':  # Add new data
            print("\nPilih File yang ingin ditambah: ")
            print("1. Data Warna")
            print("2. Data Ukuran")
            pilihan_tambah = input("Pilihan: ")
            if pilihan_tambah == '1':
                new_data = input("Masukkan warna baru: ")
                tambah_data(nama_file="idwarna.txt", data=new_data)
                print(f"Warna '{new_data}' berhasil ditambahkan.")
            elif pilihan_tambah == '2':
                new_data = input("Masukkan ukuran baru: ")
                tambah_data(nama_file="idukuran.txt", data=new_data)
                print(f"Ukuran '{new_data}' berhasil ditambahkan.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '3':  # Delete data
            print("\nPilih File yang ingin dihapus: ")
            print("1. Data Warna")
            print("2. Data Ukuran")
            print("3. Data Furniture")
            pilihan_hapus = input("Pilihan: ")
            if pilihan_hapus == '1':
                id_hapus = input("Masukkan ID warna yang akan dihapus: ")
                hapus_data(nama_file="idwarna.txt", id_hapus=id_hapus)
                print(f"Data warna dengan ID '{id_hapus}' berhasil dihapus.")
            elif pilihan_hapus == '2':
                id_hapus = input("Masukkan ID ukuran yang akan dihapus: ")
                hapus_data(nama_file="idukuran.txt", id_hapus=id_hapus)
                print(f"Data ukuran dengan ID '{id_hapus}' berhasil dihapus.")
            elif pilihan_hapus == '3':
                id_hapus = input("Masukkan ID furniture yang akan dihapus: ")
                hapus_data(nama_file="idfurniture.txt", id_hapus=id_hapus)
                print(f"Data furniture dengan ID '{id_hapus}' berhasil dihapus.")
            else:
                print("Pilihan tidak valid.")

        elif pilihan == '4':  # Create furniture data
            print("\nBuat Data Furniture: ")
            data_furniture()

        elif pilihan == '5':  # Exit
            print("Terima kasih telah menggunakan aplikasi!")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()
