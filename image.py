from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from stegano import lsb


class image:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Steganography")
        self.master.geometry("600x500")
        self.master.resizable(0, 0)

        self.image_path = StringVar()
        self.message = StringVar()
        self.password = StringVar()

        self.canvas = Canvas(self.master, width=400, height=400)
        self.canvas.pack(side=TOP, pady=10)

        self.image_label = Label(self.canvas, text="Selected Image Will be Displayed Here", font=("Arial", 10))
        self.image_label.pack(pady=10)

        self.browse_button = Button(self.master, text="Select Image", command=self.browse_image)
        self.browse_button.pack(side=LEFT, padx=10, pady=10)

        self.message_label = Label(self.master, text="Enter Secret Message:", font=("Arial", 10))
        self.message_label.pack(side=TOP, padx=10, pady=10)

        self.message_entry = Entry(self.master, textvariable=self.message, width=40, font=("Arial", 10))
        self.message_entry.pack(side=TOP, padx=10, pady=10)

        self.password_label = Label(self.master, text="Enter Password:", font=("Arial", 10))
        self.password_label.pack(side=TOP, padx=10, pady=10)

        self.password_entry = Entry(self.master, textvariable=self.password, show="*", width=40, font=("Arial", 10))
        self.password_entry.pack(side=TOP, padx=10, pady=10)

        self.hide_button = Button(self.master, text="Hide Message", command=self.hide_message, font=("Arial", 10))
        self.hide_button.pack(side=LEFT, padx=10, pady=10)

        self.retrieve_button = Button(self.master, text="Retrieve Message", command=self.retrieve_message,
                                      font=("Arial", 10))
        self.retrieve_button.pack(side=RIGHT, padx=10, pady=10)

    def browse_image(self):
        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.image_path.set(filepath)
            self.load_image()

    def load_image(self):
        img = Image.open(self.image_path.get())
        img = img.resize((200, 200), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.image, text="")

    def hide_message(self):
        if self.image_path.get() == "":
            messagebox.showerror("Error", "Please select an image")
            return
        if self.password.get() == "":
            messagebox.showerror("Error", "Please enter a password")
            return

        secret = lsb.hide(self.image_path.get(), self.message.get() + self.password.get())
        secret_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        secret.save(secret_path)
        messagebox.showinfo("Success", "Message hidden successfully")
        self.clear_fields()

    def retrieve_message(self):
        if self.image_path.get() == "":
            messagebox.showerror("Error", "Please select an image")
            return
        if self.password.get() == "":
            messagebox.showerror("Error", "Please enter a password")
            return

        secret = lsb.reveal(self.image_path.get())
        secret = secret.replace(self.password.get(), "", 1)

        if secret:
            self.message.set(secret)
            messagebox.showinfo("Success", "Message retrieved successfully")
        else:
            messagebox.showerror("Error", "Incorrect Password")

        self.clear_fields()

    def clear_fields(self):
        self.image_path.set("")
        self.message.set("")
        self.password.set("")
        self.image_label.config(image=None, text="Selected Image Will be Displayed Here")


if __name__ == "__main__":
        root = Tk()
        image(root)
        root.mainloop()


