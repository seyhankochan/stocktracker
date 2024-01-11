import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import mysql.connector
from plyer import notification
import pandas as pd
from reportlab.pdfgen import canvas
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        # Uygulamayı başlatıyorum
        self.root = root
        self.root.title("Stock Tracking - Giriş Ekranı")
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2,
                                       (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2))
        self.root.configure(bg="#9be6e8")  # Arkaplan rengini ayarlıyorum

        # Giriş ekranında kullanılacak resmi ekliyorum
        image_path = "lgoo.png"
        try:
            original_image = Image.open(image_path)
            resized_image = original_image.resize((320, 200), Image.ANTIALIAS)  # Genişlik ve yüksekliği istediğim değerlere ayarlıyorum
            photo = ImageTk.PhotoImage(resized_image)

            # Resmi ekliyorum
            label_image = tk.Label(root, image=photo, borderwidth=0, highlightthickness=0)
            label_image.image = photo
            label_image.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        except Exception as e:
            messagebox.showerror("Hata", f"Resim yüklenirken bir hata oluştu: {str(e)}")

        # Giriş ekranındaki diğer arayüz öğelerini ekliyorum
        self.label_username = tk.Label(root, text="Kullanıcı Adı:", font=("Helvetica", 12, "bold"), bg="#9be6e8")
        self.label_password = tk.Label(root, text="Şifre:", font=("Helvetica", 12, "bold"), bg="#9be6e8")

        self.entry_username = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.entry_password = tk.Entry(root, show='*', font=("Helvetica", 12, "bold"))

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#3498db", font=("Helvetica", 12, "bold"), foreground="#3498db", borderwidth=0)

        self.button_login = ttk.Button(root, text="Giriş Yap", command=self.login, style="TButton")
        self.button_register = ttk.Button(root, text="Kayıt Ol", command=self.open_register_window, style="TButton")

        self.label_username.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.label_password.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)
        self.button_login.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_register.grid(row=4, column=0, columnspan=2, pady=10)

        # MySQL veritabanına bağlanıyorum
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python"
        )
        self.cursor = self.connection.cursor()

        # Kullanıcı tablosunu oluşturuyorum (varsa)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        ''')
        self.connection.commit()

    def login(self):
        # Admin girişi kontrolünü yapıyorum
        adminkullanici = "admin"
        adminsifre = "admin123"
        
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == adminkullanici and password == adminsifre:
            # Admin girişi başarılı
            messagebox.showinfo("Başarılı", "Admin girişi başarılı.")
            self.root.destroy()
            admin_app = AdminApp(tk.Tk())
        else:
            # Kullanıcı girişi kontrolünü yapıyorum, veritabanından çekilerek
            self.cursor.execute('''
                SELECT * FROM users WHERE username = %s AND password = %s
            ''', (username, password))
            user = self.cursor.fetchone()

            if user:
                # Kullanıcı girişi başarılı
                messagebox.showinfo("Başarılı", "Kullanıcı girişi başarılı.")
                self.root.destroy()  # Giriş penceresini kapatıyorum
                inventory_app = InventoryApp(tk.Tk())  # Yeni bir Tkinter penceresi açıyorum
                inventory_app.check_stock_levels()
            else:
                # Geçersiz kullanıcı adı veya şifre hatası
                messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")
    
        
    def open_register_window(self):
        # Kayıt penceresini açıyorum
        register_window = tk.Toplevel(self.root)
        register_app = RegisterApp(register_window, self.connection)

class RegisterApp:
    def __init__(self, root, connection):
        # Kayıt uygulamasını başlatıyorum
        self.root = root
        self.root.title("Kayıt Ol")
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2,
                                       (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2))

        # Arka plan rengini ayarlıyorum
        self.root.configure(bg="#9be6e8")

        # Etiket tasarımını oluşturuyorum
        self.label_username = tk.Label(root, text="Kullanıcı Adı:", font=("Helvetica", 12, "bold"), bg="#9be6e8")
        self.label_password = tk.Label(root, text="Şifre:", font=("Helvetica", 12, "bold"), bg="#9be6e8")

        # Giriş tasarımını oluşturuyorum
        self.entry_username = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.entry_password = tk.Entry(root, show='*', font=("Helvetica", 12, "bold"))

        # Buton tasarımını oluşturuyorum
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#3498db", font=("Helvetica", 12, "bold"), foreground="#3498db", borderwidth=0)

        self.button_register = ttk.Button(root, text="Kayıt Ol", command=self.register, style="TButton")

        # Grid düzenini ayarlıyorum
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        self.button_register.grid(row=2, column=0, columnspan=2, pady=10)

        self.connection = connection
        self.cursor = self.connection.cursor()  # cursor'ı burada oluşturuyorum

    def register(self):
        # Kullanıcı adı ve şifreyi alıyorum
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            # Hata: Tüm alanları doldurması gerekiyor
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        # Kullanıcı adının veritabanında olup olmadığını kontrol ediyorum
        self.cursor.execute('''
            SELECT * FROM users WHERE username = %s
        ''', (username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            # Hata: Bu kullanıcı adı zaten kullanılıyor
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.")
            return

        # Yeni kullanıcıyı kaydediyorum
        self.cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (username, password))
        self.connection.commit()

        # Başarılı: Kayıt işlemi tamamlandı
        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")

        # Kayıt işlemi tamamlandığında, Kullanıcı Girişi penceresini gösteriyorum
        self.root.destroy()
# Kullanıcı Yönetimi sınıfı
class UserManagement:
    def __init__(self, root, connection):
        self.root = root
        self.root.title("Kullanıcı Yönetimi")
        
        # Kullanıcı Ekle bölümü
        button_width = 20  # İstediğin genişlik değeri
        root.configure(bg="#9be6e8")  # Sayfanın arka plan rengi
        self.label_add_user = tk.Label(root, text="Kullanıcı Ekle", font=("Helvetica", 16, "bold"), bg="#9be6e8", foreground="white")
        self.label_new_username = tk.Label(root, text="Yeni Kullanıcı Adı:", font=("Helvetica", 12, "bold"), bg="#9be6e8", foreground="white")
        self.label_new_password = tk.Label(root, text="Yeni Şifre:", font=("Helvetica", 12, "bold"), bg="#9be6e8", foreground="white")
        
        self.entry_new_username = tk.Entry(root, font=("Helvetica", 12, "bold"), width=button_width)
        self.entry_new_password = tk.Entry(root, show='*', font=("Helvetica", 12, "bold"), width=button_width)
        self.button_add_user = tk.Button(root, text="Kullanıcı Ekle", command=self.add_user, font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=button_width)
        
        # Kullanıcı Kaldır bölümü
        self.label_remove_user = tk.Label(root, text="Kullanıcı Kaldır", font=("Helvetica", 16, "bold"), bg="#9be6e8", foreground="white")
        self.label_remove_username = tk.Label(root, text="Kullanıcı Adı:", font=("Helvetica", 12, "bold"), bg="#9be6e8", foreground="white")
        
        # Combobox eklenen kısım
        self.combobox_remove_username = ttk.Combobox(root, state="readonly", font=("Helvetica", 12), width=button_width)
        self.combobox_remove_username.bind("<<ComboboxSelected>>", self.update_remove_entry)
        
        self.button_remove_user = tk.Button(root, text="Kullanıcı Kaldır", command=self.remove_user, font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=button_width)
        
        # Kullanıcı Güncelle bölümü
        self.label_update_user = tk.Label(root, text="Kullanıcı Güncelle", font=("Helvetica", 16, "bold"), bg="#9be6e8", foreground="white")
        self.label_update_username = tk.Label(root, text="Kullanıcı Adı:", font=("Helvetica", 12, "bold"), bg="#9be6e8", foreground="white")
        self.label_new_password_update = tk.Label(root, text="Yeni Şifre:", font=("Helvetica", 12, "bold"), bg="#9be6e8", foreground="white")
        
        # Combobox eklenen kısım
        self.combobox_update_username = ttk.Combobox(root, state="readonly", font=("Helvetica", 12), width=button_width)
        self.combobox_update_username.bind("<<ComboboxSelected>>", self.update_update_entry)
        
        self.entry_new_password_update = tk.Entry(root, show='*', font=("Helvetica", 12), width=button_width)
        self.button_update_user = tk.Button(root, text="Kullanıcı Güncelle", command=self.update_user, font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=button_width)
        
        # Widget'ları düzenle
        self.label_add_user.grid(row=0, column=0, pady=10, columnspan=2)
        self.label_new_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.label_new_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_username.grid(row=1, column=1, padx=10, pady=5)
        self.entry_new_password.grid(row=2, column=1, padx=10, pady=5)
        self.button_add_user.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.label_remove_user.grid(row=4, column=0, pady=10, columnspan=2)
        self.label_remove_username.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.combobox_remove_username.grid(row=5, column=1, padx=10, pady=5)
        self.button_remove_user.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.label_update_user.grid(row=7, column=0, pady=10, columnspan=2)
        self.label_update_username.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.combobox_update_username.grid(row=8, column=1, padx=10, pady=5)
        self.label_new_password_update.grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_password_update.grid(row=9, column=1, padx=10, pady=5)
        self.button_update_user.grid(row=10, column=0, columnspan=2, pady=10)

        self.connection = connection
        self.cursor = self.connection.cursor()

        # Combobox'ları doldur
        self.fill_comboboxes()

    def fill_comboboxes(self):
        # Veritabanından kullanıcı adlarını al
        self.cursor.execute('SELECT username FROM users')
        users = self.cursor.fetchall()

        # Combobox'ları güncelle
        remove_usernames = [user[0] for user in users]
        update_usernames = [user[0] for user in users]

        self.combobox_remove_username['values'] = remove_usernames
        self.combobox_update_username['values'] = update_usernames

    def update_remove_entry(self, event):
        selected_username = self.combobox_remove_username.get()
        self.entry_remove_username.delete(0, tk.END)
        self.entry_remove_username.insert(0, selected_username)

    def update_update_entry(self, event):
        selected_username = self.combobox_update_username.get()
        self.entry_update_username.delete(0, tk.END)
        self.entry_update_username.insert(0, selected_username)

    def add_user(self):
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        # Kullanıcı adı veya şifre boş olamaz
        if not new_username or not new_password:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        # Kullanıcı adının veritabanında olup olmadığını kontrol et
        self.cursor.execute('''
            SELECT * FROM users WHERE username = %s
        ''', (new_username,))
        existing_user = self.cursor.fetchone()
    
        if existing_user:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.")
            return
    
        # Yeni kullanıcıyı kaydet
        self.cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (new_username, new_password))
        self.connection.commit()
    
        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla eklenmiştir.")

    def remove_user(self):
        username_to_remove = self.combobox_remove_username.get()

        if not username_to_remove:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı seçin.")
            return

        # Kullanıcıyı veritabanından kaldır
        self.cursor.execute('DELETE FROM users WHERE username = %s', (username_to_remove,))
        self.connection.commit()

        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaldırılmıştır.")
        self.fill_comboboxes()

    def update_user(self):
        username_to_update = self.combobox_update_username.get()
        new_password_update = self.entry_new_password_update.get()

        if not username_to_update:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı seçin.")
            return

        # Kullanıcıyı güncelle
        self.cursor.execute('UPDATE users SET password = %s WHERE username = %s', (new_password_update, username_to_update))
        self.connection.commit()

        messagebox.showinfo("Başarılı", "Kullanıcı bilgileri başarıyla güncellenmiştir.")
        self.fill_comboboxes()
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Envanter Takip Uygulaması")
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2,
                                       (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2))
        root.configure(bg="#9be6e8")
        # MySQL veritabanına bağlan
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python"
        )
        self.cursor = self.connection.cursor()

        # Tablo oluştur
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(255),
                quantity INT,
                item_unit VARCHAR(10)
            )
        ''')

        self.connection.commit()

        # Arayüz öğelerini oluştur
        background_color = "#9be6e8"  # Light Blue
        font_style = ('Helvetica', 12, 'bold')

        self.label_item_name = tk.Label(root, text="Öğe Adı:", font=font_style, background=background_color)
        self.label_quantity = tk.Label(root, text="Miktar:", font=font_style, background=background_color)
        self.label_unit = tk.Label(root, text="Birim:", font=font_style, background=background_color)

        self.entry_item_name = tk.Entry(root, font=font_style)
        self.entry_quantity = tk.Entry(root, font=font_style)
        self.combobox_unit = ttk.Combobox(root, values=["kg", "lt", "ml", "adet"], font=font_style)

        # ttk.Style öğesini kullanarak buton stilini değiştir
        self.button_style = ttk.Style()
        self.button_style.configure('Flat.TButton', foreground='#3498db', background='#3498db', width=20,
                                    font=font_style)

        self.button_add_stock = ttk.Button(root, text="Stok Ekle", command=self.add_stock, style='Flat.TButton')
        self.button_show_stock = ttk.Button(root, text="Stokları Görüntüle", command=self.show_stock,
                                            style='Flat.TButton')

        # Depo combobox'ını oluştur
        self.label_depo = tk.Label(root, text="Depo:", font=font_style, background=background_color)
        self.combobox_depo = ttk.Combobox(root, values=["1", "2", "3"], font=font_style)

        self.label_depo.grid(row=3, column=0, padx=10, pady=10)
        self.combobox_depo.grid(row=3, column=1, padx=10, pady=10)

        # Arayüz öğelerini düzenle
        self.label_item_name.grid(row=0, column=0, padx=10, pady=10)
        self.label_quantity.grid(row=1, column=0, padx=10, pady=10)
        self.label_unit.grid(row=2, column=0, padx=10, pady=10)

        self.entry_item_name.grid(row=0, column=1, padx=10, pady=10)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        self.combobox_unit.grid(row=2, column=1, padx=10, pady=10)

        self.button_add_stock.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_show_stock.grid(row=5, column=0, columnspan=2, pady=10)

        # Yeni pencere oluştur (Listbox ve Sil butonu içeriyor)
        self.stock_window = tk.Toplevel(root)
        self.stock_window.title("Stok Listesi")
        self.stock_window.protocol("WM_DELETE_WINDOW", self.close_stock_window)  # Pencere kapatıldığında olayı yakala
        self.stock_window.withdraw()  # Pencereyi gizle

        self.listbox_stock = tk.Listbox(self.stock_window, width=50, height=10, background=background_color,
                                        font=font_style)
        self.listbox_stock.pack(pady=10)

        self.button_delete_stock = ttk.Button(self.stock_window, text="Stok Sil", command=self.delete_stock,
                                              style='Flat.TButton')
        self.button_delete_stock.pack(pady=10)

        self.button_edit_stock = ttk.Button(self.stock_window, text="Stok Düzenle", command=self.edit_stock,
                                            style='Flat.TButton')
        self.button_edit_stock.pack(pady=10)

        self.button_save_pdf = ttk.Button(self.stock_window, text="Kaydet", command=self.save_list_to_pdf,
                                          style='Flat.TButton')
        self.button_save_pdf.pack(pady=10)

        # Stok verilerini saklamak için liste
        self.stock_data = None
    
    def save_to_pdf(self, data):
        try:
            pdf_filename = "stoklistesi.pdf"

            # PDF oluştur
            c = canvas.Canvas(pdf_filename)

            # Başlık ekleyin
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 750, "Stok Raporu")

            # Verileri PDF'ye ekleyin
            c.setFont("Helvetica", 12)
            y_position = 720  # İlk başlangıç yüksekliği

            for item in data:
                c.drawString(100, y_position, item)
                y_position -= 20  # Her öğeden sonra yüksekliği azalt

            # PDF'yi kaydet
            c.save()

            messagebox.showinfo("Başarılı", f"Veriler '{pdf_filename}' dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"PDF oluşturma sırasında bir hata oluştu: {str(e)}")

    def save_list_to_pdf(self):
        # Listbox'tan verileri al
        listbox_data = [self.listbox_stock.get(idx) for idx in range(self.listbox_stock.size())]

        # PDF'ye kaydet
        self.save_to_pdf(listbox_data)
        
    def get_depo_id(self, depo_id):
        self.cursor.execute('''
            SELECT depo.depoID FROM depo WHERE depoID = %s
        ''', (depo_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            messagebox.showerror("Hata", "Depo ID bulunamadı.")
            return None

    def close_stock_window(self):
        self.stock_window.withdraw()

    def add_stock(self):
        item_name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        unit = self.combobox_unit.get()
        depo_selection = self.combobox_depo.get()
    
        if not item_name or not quantity or not unit or not depo_selection:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(depo_selection)
    
        self.cursor.execute('''
            INSERT INTO inventory (depoID, item_name, quantity, item_unit)
            VALUES (%s, %s, %s, %s) 
        ''', (depo_id, item_name, quantity, unit))
        self.connection.commit()
    
        messagebox.showinfo("Başarılı", f"{item_name} ürünü başarıyla eklenmiştir. Miktar: {quantity} {unit}")
    
        # Stok düzeylerini kontrol et ve gerekirse bildirim gönder
        self.check_stock_levels()
    
        self.entry_item_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.combobox_unit.set("")
        self.combobox_depo.set("")  # Depo combobox'ını temizle

    def show_stock(self):
        # Clear the Listbox before populating
        self.listbox_stock.delete(0, tk.END)

        self.cursor.execute('''
            SELECT * FROM inventory
        ''')
        self.stock_data = self.cursor.fetchall()

        for row in self.stock_data:
            item_info = f"{row[1]} - Miktar: {row[2]} - {row[3]} - depo:{row[4]}"
            self.listbox_stock.insert(tk.END, item_info)

        # Pencerenin durumuna bağlı olarak pencereyi göster veya odaklan
        if not self.stock_window.winfo_ismapped():
            self.stock_window.deiconify()
            self.stock_window.focus_set()

    def delete_stock(self):
        selected_item = self.listbox_stock.curselection()

        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return

        selected_id = self.stock_data[selected_item[0]][0]

        self.cursor.execute('''
            DELETE FROM inventory WHERE id = %s
        ''', (selected_id,))
        self.connection.commit()

        # Stock penceresini güncelle
        self.show_stock()

        messagebox.showinfo("Başarılı", "Stok başarıyla silindi.")

    def edit_stock(self):
        selected_item = self.listbox_stock.curselection()
    
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return
    
        selected_id = self.stock_data[selected_item[0]][0]
        selected_name = self.stock_data[selected_item[0]][1]
        selected_quantity = self.stock_data[selected_item[0]][2]
        selected_unit = self.stock_data[selected_item[0]][3]
    
        # Düzenleme penceresini oluştur
        edit_window = tk.Toplevel(self.stock_window)
        edit_window.title("Stok Düzenle")
    
        label_item_name = tk.Label(edit_window, text="Yeni Öğe Adı:")
        label_quantity = tk.Label(edit_window, text="Yeni Miktar:")
        label_unit = tk.Label(edit_window, text="Yeni Birim:")
        label_depo = tk.Label(edit_window, text="Yeni Depo:")
    
        entry_item_name = tk.Entry(edit_window)
        entry_quantity = tk.Entry(edit_window)
        combobox_unit = ttk.Combobox(edit_window, values=["kg", "lt", "ml", "adet"])
        combobox_depo = ttk.Combobox(edit_window, values=["1", "2", "3"])
    
        entry_item_name.insert(0, selected_name)
        entry_quantity.insert(0, selected_quantity)
        combobox_unit.set(selected_unit)
    
        label_item_name.grid(row=0, column=0, padx=10, pady=10)
        label_quantity.grid(row=1, column=0, padx=10, pady=10)
        label_unit.grid(row=2, column=0, padx=10, pady=10)
        label_depo.grid(row=3, column=0, padx=10, pady=10)
    
        entry_item_name.grid(row=0, column=1, padx=10, pady=10)
        entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        combobox_unit.grid(row=2, column=1, padx=10, pady=10)
        combobox_depo.grid(row=3, column=1, padx=10, pady=10)
    
        button_save = tk.Button(edit_window, text="Kaydet", command=lambda: self.save_edited_stock(edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit, combobox_depo))
        button_save.grid(row=4, column=0, columnspan=2, pady=10)

    def save_edited_stock(self, edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit,combobox_depo):
        new_name = entry_item_name.get()
        new_quantity = entry_quantity.get()
        new_unit = combobox_unit.get()
        new_depo = combobox_depo.get()
    
        if not new_name or not new_quantity or not new_unit or not new_depo:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(new_depo)
    
        if depo_id is not None:
            # Veritabanında stok bilgilerini güncelle
            self.cursor.execute('''
                UPDATE inventory SET item_name = %s, quantity = %s, item_unit = %s, depoID = %s
                WHERE id = %s
            ''', (new_name, new_quantity, new_unit, depo_id, selected_id))
            self.connection.commit()
    
            messagebox.showinfo("Başarılı", "Stok başarıyla güncellendi.")
    
            # Düzenleme penceresini kapat
            edit_window.destroy()
    
            # Stock penceresini güncelle
            self.show_stock()

    def check_stock_levels(self):
        self.cursor.execute('''
            SELECT item_name, SUM(quantity) AS total_quantity
            FROM inventory
            GROUP BY item_name
            HAVING total_quantity <= 5
        ''')
        low_stock_items = self.cursor.fetchall()

        if low_stock_items:
            message = "Aşağıdaki ürünlerin stoğu azaldı:\n"
            for item in low_stock_items:
                item_name = item[0]
                total_quantity = item[1]
                message += f"{item_name}: {total_quantity} adet\n"

            self.send_notification("Stok Azaldı", message)

    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Stock Tracking",
            timeout=10  # Bildirimi 10 saniye boyunca göster
        )
class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Paneli")
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2,
                                       (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2))
        root.configure(bg="#9be6e8")
        # MySQL veritabanına bağlan
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python"
        )
        self.cursor = self.connection.cursor()

        # Tablo oluştur
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(255),
                quantity INT,
                item_unit VARCHAR(10),
                depoID INT
            )
        ''')

        self.connection.commit()

        # Arayüz öğelerini oluştur
        background_color = "#9be6e8"  # Light Blue
        font_style = ('Helvetica', 12, 'bold')

        self.label_item_name = tk.Label(root, text="Öğe Adı:", font=font_style, background=background_color)
        self.label_quantity = tk.Label(root, text="Miktar:", font=font_style, background=background_color)
        self.label_unit = tk.Label(root, text="Birim:", font=font_style, background=background_color)
        self.label_depo = tk.Label(root, text="Depo:", font=font_style, background=background_color)

        self.entry_item_name = tk.Entry(root, font=font_style)
        self.entry_quantity = tk.Entry(root, font=font_style)
        self.combobox_unit = ttk.Combobox(root, values=["kg", "lt", "ml", "adet"], font=font_style)
        self.combobox_depo = ttk.Combobox(root, values=["1", "2", "3"], font=font_style)

        self.button_add_stock = ttk.Button(root, text="Stok Ekle", command=self.add_stock, style='Flat.TButton')
        self.button_show_stock = ttk.Button(root, text="Stokları Görüntüle", command=self.show_stock,
                                            style='Flat.TButton')
        self.button_manage_users = ttk.Button(root, text="Kullanıcıları Yönet", command=self.manage_users,
                                              style='Flat.TButton')

        # ttk.Style öğesini kullanarak buton stilini değiştir
        self.button_style = ttk.Style()
        self.button_style.configure('Flat.TButton', foreground='#3498db', background='#3498db', width=20,
                                    font=font_style)

        self.label_item_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.label_quantity.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.label_unit.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.label_depo.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.entry_item_name.grid(row=0, column=1, padx=10, pady=10)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        self.combobox_unit.grid(row=2, column=1, padx=10, pady=10)
        self.combobox_depo.grid(row=3, column=1, padx=10, pady=10)

        self.button_add_stock.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
        self.button_show_stock.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
        self.button_manage_users.grid(row=6, column=0, columnspan=2, pady=20, sticky="nsew")

        # Yeni pencere oluştur (Listbox ve Sil butonu içeriyor)
        self.stock_window = tk.Toplevel(root)
        self.stock_window.title("Stok Listesi")
        self.stock_window.protocol("WM_DELETE_WINDOW", self.close_stock_window)  # Pencere kapatıldığında olayı yakala
        self.stock_window.withdraw()  # Pencereyi gizle

        self.listbox_stock = tk.Listbox(self.stock_window, width=50, height=10, background=background_color,
                                        font=font_style)
        self.listbox_stock.pack(pady=10)

        self.button_delete_stock = ttk.Button(self.stock_window, text="Stok Sil", command=self.delete_stock,
                                              style='Flat.TButton')
        self.button_delete_stock.pack(pady=10)

        self.button_edit_stock = ttk.Button(self.stock_window, text="Stok Düzenle", command=self.edit_stock,
                                            style='Flat.TButton')
        self.button_edit_stock.pack(pady=10)

        self.button_save_pdf = ttk.Button(self.stock_window, text="Kaydet", command=self.save_list_to_pdf,
                                          style='Flat.TButton')
        self.button_save_pdf.pack(pady=10)

        # Stok verilerini saklamak için liste
        self.stock_data = None
        
    def save_to_pdf(self, data):
        try:
            pdf_filename = "stoklistesi.pdf"

            # PDF oluştur
            c = canvas.Canvas(pdf_filename)

            # Başlık ekleyin
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 750, "Stok Raporu")

            # Verileri PDF'ye ekleyin
            c.setFont("Helvetica", 12)
            y_position = 720  # İlk başlangıç yüksekliği

            for item in data:
                c.drawString(100, y_position, item)
                y_position -= 20  # Her öğeden sonra yüksekliği azalt

            # PDF'yi kaydet
            c.save()

            messagebox.showinfo("Başarılı", f"Veriler '{pdf_filename}' dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"PDF oluşturma sırasında bir hata oluştu: {str(e)}")

    def save_list_to_pdf(self):
        # Listbox'tan verileri al
        listbox_data = [self.listbox_stock.get(idx) for idx in range(self.listbox_stock.size())]

        # PDF'ye kaydet
        self.save_to_pdf(listbox_data)
        
    def get_depo_id(self, depo_id):
        self.cursor.execute('''
            SELECT depo.depoID FROM depo WHERE depoID = %s
        ''', (depo_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            messagebox.showerror("Hata", "Depo ID bulunamadı.")
            return None

    def manage_users(self):
        # Kullanıcı yönetimi penceresini aç
        user_management_window = tk.Toplevel(self.root)
        user_management = UserManagement(user_management_window, self.connection)

    def close_stock_window(self):
        self.stock_window.withdraw()

    def add_stock(self):
        item_name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        unit = self.combobox_unit.get()
        depo_selection = self.combobox_depo.get()
    
        if not item_name or not quantity or not unit or not depo_selection:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(depo_selection)
    
        self.cursor.execute('''
            INSERT INTO inventory (depoID, item_name, quantity, item_unit)
            VALUES (%s, %s, %s, %s)
        ''', (depo_id, item_name, quantity, unit))
        self.connection.commit()
    
        messagebox.showinfo("Başarılı", f"{item_name} ürünü başarıyla eklenmiştir. Miktar: {quantity} {unit}")
    
        # Stok düzeylerini kontrol et ve gerekirse bildirim gönder
        self.check_stock_levels()
    
        self.entry_item_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.combobox_unit.set("")
        self.combobox_depo.set("")  # Depo combobox'ını temizle

    def show_stock(self):
        # Clear the Listbox before populating
        self.listbox_stock.delete(0, tk.END)

        self.cursor.execute('''
            SELECT * FROM inventory
        ''')
        self.stock_data = self.cursor.fetchall()

        for row in self.stock_data:
            item_info = f"{row[1]} - Miktar: {row[2]} - {row[3]} - depo:{row[4]}"
            self.listbox_stock.insert(tk.END, item_info)

        # Pencerenin durumuna bağlı olarak pencereyi göster veya odaklan
        if not self.stock_window.winfo_ismapped():
            self.stock_window.deiconify()
            self.stock_window.focus_set()

    def delete_stock(self):
        selected_item = self.listbox_stock.curselection()

        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return

        selected_id = self.stock_data[selected_item[0]][0]

        self.cursor.execute('''
            DELETE FROM inventory WHERE id = %s
        ''', (selected_id,))
        self.connection.commit()

        # Stock penceresini güncelle
        self.show_stock()

        messagebox.showinfo("Başarılı", "Stok başarıyla silindi.")

    def edit_stock(self):
        selected_item = self.listbox_stock.curselection()
    
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return
    
        selected_id = self.stock_data[selected_item[0]][0]
        selected_name = self.stock_data[selected_item[0]][1]
        selected_quantity = self.stock_data[selected_item[0]][2]
        selected_unit = self.stock_data[selected_item[0]][3]
    
        # Düzenleme penceresini oluştur
        edit_window = tk.Toplevel(self.stock_window)
        edit_window.title("Stok Düzenle")
    
        label_item_name = tk.Label(edit_window, text="Yeni Öğe Adı:")
        label_quantity = tk.Label(edit_window, text="Yeni Miktar:")
        label_unit = tk.Label(edit_window, text="Yeni Birim:")
        label_depo = tk.Label(edit_window, text="Yeni Depo:")
    
        entry_item_name = tk.Entry(edit_window)
        entry_quantity = tk.Entry(edit_window)
        combobox_unit = ttk.Combobox(edit_window, values=["kg", "lt", "ml", "adet"])
        combobox_depo = ttk.Combobox(edit_window, values=["1", "2", "3"])
    
        entry_item_name.insert(0, selected_name)
        entry_quantity.insert(0, selected_quantity)
        combobox_unit.set(selected_unit)
    
        label_item_name.grid(row=0, column=0, padx=10, pady=10)
        label_quantity.grid(row=1, column=0, padx=10, pady=10)
        label_unit.grid(row=2, column=0, padx=10, pady=10)
        label_depo.grid(row=3, column=0, padx=10, pady=10)
    
        entry_item_name.grid(row=0, column=1, padx=10, pady=10)
        entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        combobox_unit.grid(row=2, column=1, padx=10, pady=10)
        combobox_depo.grid(row=3, column=1, padx=10, pady=10)
    
        button_save = tk.Button(edit_window, text="Kaydet", command=lambda: self.save_edited_stock(edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit, combobox_depo))
        button_save.grid(row=4, column=0, columnspan=2, pady=10)
    
    def save_edited_stock(self, edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit, combobox_depo):
        new_name = entry_item_name.get()
        new_quantity = entry_quantity.get()
        new_unit = combobox_unit.get()
        new_depo = combobox_depo.get()
    
        if not new_name or not new_quantity or not new_unit or not new_depo:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(new_depo)
    
        if depo_id is not None:  # depo_id'nin geçerli olup olmadığını kontrol et
            # Veritabanında stok bilgilerini güncelle
            self.cursor.execute('''
                UPDATE inventory SET item_name = %s, quantity = %s, item_unit = %s, depoI = %s
                WHERE id = %s
            ''', (new_name, new_quantity, new_unit, depo_id, selected_id))
            self.connection.commit()
    
            messagebox.showinfo("Başarılı", "Stok başarıyla güncellendi.")
    
            # Düzenleme penceresini kapat
            edit_window.destroy()
    
            # Stock penceresini güncelle
            self.show_stock()

    def check_stock_levels(self):
        self.cursor.execute('''
            SELECT item_name, SUM(quantity) AS total_quantity
            FROM inventory
            GROUP BY item_name
            HAVING total_quantity <= 5
        ''')
        low_stock_items = self.cursor.fetchall()

        if low_stock_items:
            message = "Aşağıdaki ürünlerin stoğu azaldı:\n"
            for item in low_stock_items:
                item_name = item[0]
                total_quantity = item[1]
                message += f"{item_name}: {total_quantity} adet\n"

            self.send_notification("Stok Azaldı", message)
                    
    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Stock Tracking",
            timeout=10  # Bildirimi 10 saniye boyunca göster
        )
    def get_depo_id(self, depo_id):
        self.cursor.execute('''
            SELECT depo.depoID FROM depo WHERE depoID = %s
        ''', (depo_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            messagebox.showerror("Hata", "Depo ID bulunamadı.")
            return None
    
    def close_stock_window(self):
        self.stock_window.withdraw()
    
    def add_stock(self):
        item_name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        unit = self.combobox_unit.get()
        depo_selection = self.combobox_depo.get()
    
        if not item_name or not quantity or not unit or not depo_selection:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(depo_selection)
    
        self.cursor.execute('''
            INSERT INTO inventory (depoID, item_name, quantity, item_unit)
            VALUES (%s, %s, %s, %s)
        ''', (depo_id, item_name, quantity, unit))
        self.connection.commit()
    
        messagebox.showinfo("Başarılı", f"{item_name} ürünü başarıyla eklenmiştir. Miktar: {quantity} {unit}")
    
        # Stok düzeylerini kontrol et ve gerekirse bildirim gönder
        self.check_stock_levels()
    
        self.entry_item_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.combobox_unit.set("")
        self.combobox_depo.set("")  # Depo combobox'ını temizle
    
    def show_stock(self):
        # Clear the Listbox before populating
        self.listbox_stock.delete(0, tk.END)
    
        self.cursor.execute('''
            SELECT * FROM inventory
        ''')
        self.stock_data = self.cursor.fetchall()
    
        for row in self.stock_data:
            item_info = f"{row[1]} - Miktar: {row[2]} - {row[3]} - depo:{row[4]}"
            self.listbox_stock.insert(tk.END, item_info)
    
        # Pencerenin durumuna bağlı olarak pencereyi göster veya odaklan
        if not self.stock_window.winfo_ismapped():
            self.stock_window.deiconify()
            self.stock_window.focus_set()
    
    def delete_stock(self):
        selected_item = self.listbox_stock.curselection()
    
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return
    
        selected_id = self.stock_data[selected_item[0]][0]
    
        self.cursor.execute('''
            DELETE FROM inventory WHERE id = %s
        ''', (selected_id,))
        self.connection.commit()
    
        # Stock penceresini güncelle
        self.show_stock()
    
        messagebox.showinfo("Başarılı", "Stok başarıyla silindi.")
    
    def edit_stock(self):
        selected_item = self.listbox_stock.curselection()
    
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir öğe seçin.")
            return
    
        selected_id = self.stock_data[selected_item[0]][0]
        selected_name = self.stock_data[selected_item[0]][1]
        selected_quantity = self.stock_data[selected_item[0]][2]
        selected_unit = self.stock_data[selected_item[0]][3]
    
        # Düzenleme penceresini oluştur
        edit_window = tk.Toplevel(self.stock_window)
        edit_window.title("Stok Düzenle")
    
        label_item_name = tk.Label(edit_window, text="Yeni Öğe Adı:")
        label_quantity = tk.Label(edit_window, text="Yeni Miktar:")
        label_unit = tk.Label(edit_window, text="Yeni Birim:")
        label_depo = tk.Label(edit_window, text="Yeni Depo:")
    
        entry_item_name = tk.Entry(edit_window)
        entry_quantity = tk.Entry(edit_window)
        combobox_unit = ttk.Combobox(edit_window, values=["kg", "lt", "ml", "adet"])
        combobox_depo = ttk.Combobox(edit_window, values=["1", "2", "3"])
    
        entry_item_name.insert(0, selected_name)
        entry_quantity.insert(0, selected_quantity)
        combobox_unit.set(selected_unit)
    
        label_item_name.grid(row=0, column=0, padx=10, pady=10)
        label_quantity.grid(row=1, column=0, padx=10, pady=10)
        label_unit.grid(row=2, column=0, padx=10, pady=10)
        label_depo.grid(row=3, column=0, padx=10, pady=10)
    
        entry_item_name.grid(row=0, column=1, padx=10, pady=10)
        entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        combobox_unit.grid(row=2, column=1, padx=10, pady=10)
        combobox_depo.grid(row=3, column=1, padx=10, pady=10)
    
        button_save = tk.Button(edit_window, text="Kaydet", command=lambda: self.save_edited_stock(edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit, combobox_depo))
        button_save.grid(row=4, column=0, columnspan=2, pady=10)
    
    def save_edited_stock(self, edit_window, selected_id, entry_item_name, entry_quantity, combobox_unit,combobox_depo):
        new_name = entry_item_name.get()
        new_quantity = entry_quantity.get()
        new_unit = combobox_unit.get()
        new_depo = combobox_depo.get()
    
        if not new_name or not new_quantity or not new_unit or not new_depo:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
    
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            messagebox.showerror("Hata", "Miktar bir sayı olmalıdır.")
            return
    
        depo_id = self.get_depo_id(new_depo)
    
        if depo_id is not None:
            # Veritabanında stok bilgilerini güncelle
            self.cursor.execute('''
                UPDATE inventory SET item_name = %s, quantity = %s, item_unit = %s, depoID = %s
                WHERE id = %s
            ''', (new_name, new_quantity, new_unit, depo_id, selected_id))
            self.connection.commit()
    
            messagebox.showinfo("Başarılı", "Stok başarıyla güncellendi.")
    
            # Düzenleme penceresini kapat
            edit_window.destroy()
    
            # Stock penceresini güncelle
            self.show_stock()
    
    def check_stock_levels(self):
        self.cursor.execute('''
            SELECT item_name, SUM(quantity) AS total_quantity
            FROM inventory
            GROUP BY item_name
            HAVING total_quantity <= 5
        ''')
        low_stock_items = self.cursor.fetchall()

        if low_stock_items:
            message = "Aşağıdaki ürünlerin stoğu azaldı:\n"
            for item in low_stock_items:
                item_name = item[0]
                total_quantity = item[1]
                message += f"{item_name}: {total_quantity} adet\n"

            self.send_notification("Stok Azaldı", message)

    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Stock Tracking",
            timeout=10  # Bildirimi 10 saniye boyunca göster
        )
    
# İkinci pencereyi başlatan bir fonksiyon
def start_inventory_app():
    inventory_root = tk.Tk()
    app = InventoryApp(inventory_root)
    inventory_root.mainloop()
    

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginApp(login_root)
    login_root.mainloop()