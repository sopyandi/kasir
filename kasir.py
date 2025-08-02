import tkinter as tk
from tkinter import ttk, messagebox

# Daftar harga
barang_harga = {
    "indomie-g": 3000,
    "indomie-k": 2500,
    "beras": 12000,
    "telur": 2000,
    "minyak": 14000,
    "sabun": 4000
}

def tambah_baris():
    new_item = tree.insert("", "end", values=(len(tree.get_children())+1, "", "", "", "", "Hapus"))
    tree.update_idletasks()
    tree.after(100, lambda: fokus_kan_input(new_item, "#2"))

def hapus_baris(item=None):
    if item:
        tree.delete(item)
        reset_nomor()
    update_total()

def reset_nomor():
    for i, item in enumerate(tree.get_children(), start=1):
        values = list(tree.item(item)["values"])
        values[0] = i
        tree.item(item, values=values)

def update_total():
    total = 0
    for child in tree.get_children():
        values = tree.item(child)["values"]
        try:
            total += int(values[4])  # Kolom Total sekarang di index 4
        except:
            continue
    total_label.config(text=f"Total: Rp{total}")

def proses_bayar():
    total = 0
    for child in tree.get_children():
        values = tree.item(child)["values"]
        try:
            total += int(values[4])
        except:
            continue

    try:
        uang = int(uang_entry.get())
    except:
        messagebox.showerror("Error", "Masukkan uang tunai dalam angka!")
        return

    if uang < total:
        messagebox.showwarning("Kurang", "Uang tidak cukup!")
    else:
        kembali = uang - total
        messagebox.showinfo("Sukses", f"Pembayaran berhasil!\nKembalian: Rp{kembali}")
        for item in tree.get_children():
            tree.delete(item)
        uang_entry.delete(0, tk.END)
        update_total()
        tambah_baris()

def aktifkan_input(item, column):
    x, y, width, height = tree.bbox(item, column)
    entry_popup = tk.Entry(tree, font=("Arial", 11))
    entry_popup.place(x=x, y=y, width=width, height=height)

    current = tree.set(item, column)
    entry_popup.insert(0, current)
    entry_popup.focus()

    def simpan_input():
        new_value = entry_popup.get()
        entry_popup.destroy()

        values = list(tree.item(item)["values"])
        col_index = int(column[1]) - 1
        values[col_index] = new_value.strip()

        nama = values[1]
        jumlah = values[2]

        if column == "#2":  # Nama
            if nama in barang_harga:
                harga = barang_harga[nama]
                values[3] = str(harga)
                try:
                    jumlah_int = int(jumlah)
                    if jumlah_int > 0:
                        values[4] = str(harga * jumlah_int)
                    else:
                        values[4] = "0"
                except:
                    values[2] = ""
                    values[4] = "0"
                tree.item(item, values=values)
                update_total()
                entry_popup.after(100, lambda: fokus_kan_input(item, "#3"))
                return
            else:
                values[3] = "-"
                values[4] = "0"

        elif column == "#3":  # Jumlah
            try:
                jumlah_int = int(jumlah)
                values[2] = str(jumlah_int)
                harga = barang_harga.get(nama, 0)
                if nama in barang_harga and jumlah_int > 0:
                    values[3] = str(harga)
                    values[4] = str(harga * jumlah_int)
                else:
                    values[4] = "0"
            except:
                values[2] = ""
                values[4] = "0"

            if nama in barang_harga and values[2].isdigit() and int(values[2]) > 0:
                if tree.index(item) == len(tree.get_children()) - 1:
                    tambah_baris()

        tree.item(item, values=values)
        update_total()

    def on_tab(event):
        simpan_input()
        return "break"

    entry_popup.bind("<Return>", lambda e: simpan_input())
    entry_popup.bind("<FocusOut>", lambda e: simpan_input())
    entry_popup.bind("<Tab>", on_tab)

def fokus_kan_input(item, column):
    bbox = tree.bbox(item, column)
    if bbox:
        x, y, width, height = bbox
        aktifkan_input(item, column)

def on_click(event):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item:
        if column == "#6":
            hapus_baris(item)
        elif column in ("#2", "#3"):
            aktifkan_input(item, column)

def on_delete_key(event):
    selected = tree.selection()
    for item in selected:
        hapus_baris(item)

# GUI Utama
root = tk.Tk()
root.title("Kasir Warung Otomatis - Mode Tabel")
root.geometry("960x560")

# FRAME UTAMA
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# FRAME KIRI (1/7)
frame_kiri = tk.Frame(main_frame, width=960//7, bg="#f0f0f0")
frame_kiri.pack(side="right", fill="y")  # awalnya "left"
frame_kiri.pack_propagate(False)

# FRAME KANAN (6/7)
frame_kanan = tk.Frame(main_frame)
frame_kanan.pack(side="left", fill="both", expand=True)  # awalnya "right"

# Label Total dan Tombol Tambah di atas
top_frame = tk.Frame(frame_kanan)
top_frame.pack(fill="x", pady=(10, 0), padx=10)

total_label = tk.Label(top_frame, text="Total: Rp0", font=("Arial", 18))
total_label.pack(side="left")

tambah_button = tk.Button(top_frame, text="+ Tambah", font=("Arial", 11), command=tambah_baris)
tambah_button.pack(side="right")

# Tabel Treeview
tree = ttk.Treeview(frame_kanan, columns=("No", "Nama", "Jumlah", "Harga", "Total", "Hapus"), show="headings", height=12)
tree.heading("No", text="No")
tree.heading("Nama", text="Nama Barang")
tree.heading("Jumlah", text="Jumlah")
tree.heading("Harga", text="Harga")
tree.heading("Total", text="Total")
tree.heading("Hapus", text="")

tree.column("No", anchor="center", width=50)
tree.column("Nama", anchor="center", width=180)
tree.column("Jumlah", anchor="center", width=80)
tree.column("Harga", anchor="center", width=100)
tree.column("Total", anchor="center", width=120)
tree.column("Hapus", anchor="center", width=80)

tree.pack(pady=10, padx=10, fill="both", expand=True)
tree.bind("<Button-1>", on_click)
root.bind("<Delete>", on_delete_key)

# Total dan Pembayaran
frame_total = tk.Frame(frame_kanan)
frame_total.pack(pady=10)

tk.Label(frame_total, text="Uang Tunai:", font=("Arial", 12)).pack()

uang_entry = tk.Entry(frame_total, font=("Arial", 12))
uang_entry.pack(pady=5)

tk.Button(frame_total, text="Bayar", font=("Arial", 12), command=proses_bayar, bg="orange").pack(pady=10)

# Tambah baris pertama otomatis
tambah_baris()

root.mainloop()
