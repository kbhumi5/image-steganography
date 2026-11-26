""""import tkinter as tk
from tkinter import filedialog, messagebox
from encode import encode_and_encrypt_message
from decode import decode_and_decrypt_message


def select_image():
    path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, path)


def encode_message():
    image_path = image_path_entry.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    if encode_mode.get() == "text":
        if not secret_message_entry.get().strip():
            messagebox.showerror("Error", "Please enter a secret message.")
            return
    else:
        # Ask user to select file to hide
        file_path = filedialog.askopenfilename(title="Select File to Hide (PDF, ZIP, etc.)")
        if not file_path:
            messagebox.showerror("Error", "No file selected for hiding.")
            return
        # Temporarily store path in secret_message_entry for compatibility
        secret_message_entry.delete(0, tk.END)
        secret_message_entry.insert(0, file_path)

    try:
        key, out_image = encode_and_encrypt_message(secret_message_entry, image_path, encode_mode.get())
        if key:
            messagebox.showinfo("Key", f"Keep this key safe:\n{key.decode()}")
    except Exception as e:
        messagebox.showerror("Error", f"Encoding failed: {e}")


def decode_message():
    image_path = image_path_entry.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    if not password_entry.get().strip():
        messagebox.showerror("Error", "Please enter the decryption key.")
        return

    try:
        decode_and_decrypt_message(password_entry, image_path)
    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {e}")


# ---------- GUI ----------
root = tk.Tk()
root.title("Advanced Image Steganography")
root.geometry("480x400")
root.configure(bg="#f4f4f4")

# --- Encode Section
tk.Label(root, text="🔒 ENCODE SECTION", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=(10, 4))

encode_mode = tk.StringVar(value="text")

mode_frame = tk.Frame(root, bg="#f4f4f4")
mode_frame.pack()
tk.Label(mode_frame, text="Choose Mode:", bg="#f4f4f4", font=("Arial", 10, "bold")).pack(anchor="w")

tk.Radiobutton(mode_frame, text="Hide Text Message", variable=encode_mode, value="text", bg="#f4f4f4").pack(anchor="w")
tk.Radiobutton(mode_frame, text="Hide File (any type)", variable=encode_mode, value="file", bg="#f4f4f4").pack(anchor="w")

tk.Label(root, text="Secret Message:", bg="#f4f4f4").pack(pady=(6, 0))
secret_message_entry = tk.Entry(root, width=50)
secret_message_entry.pack()

tk.Label(root, text="Image Path:", bg="#f4f4f4").pack(pady=(6, 0))
image_path_entry = tk.Entry(root, width=50)
image_path_entry.pack()
tk.Button(root, text="Browse Image", command=select_image).pack(pady=3)

tk.Button(root, text="Encode & Encrypt", command=encode_message).pack(pady=8)

# --- Decode Section
tk.Label(root, text="🔓 DECODE SECTION", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=(10, 4))
tk.Label(root, text="Decryption Key:", bg="#f4f4f4").pack()
password_entry = tk.Entry(root, width=50)
password_entry.pack()
tk.Button(root, text="Decode Message", command=decode_message).pack(pady=5)

root.mainloop()
"""
import tkinter as tk 
from tkinter import filedialog, messagebox
from encode import encode_and_encrypt_message
from decode import decode_and_decrypt_message


def select_image():
    path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, path)


def encode_message():
    image_path = image_path_entry.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image or PDF first.")
        return

    if encode_mode.get() == "text":
        if not secret_message_entry.get().strip():
            messagebox.showerror("Error", "Please enter a secret message.")
            return
    elif encode_mode.get() == "pdf":
        if not secret_message_entry.get().strip():
            messagebox.showerror("Error", "Please enter a secret message to hide inside the PDF.")
            return
    else:
        # Ask user to select file to hide
        file_path = filedialog.askopenfilename(title="Select File to Hide (PDF, ZIP, etc.)")
        if not file_path:
            messagebox.showerror("Error", "No file selected for hiding.")
            return
        # Temporarily store path in secret_message_entry for compatibility
        secret_message_entry.delete(0, tk.END)
        secret_message_entry.insert(0, file_path)

    try:
        key, out_path = encode_and_encrypt_message(secret_message_entry, image_path, encode_mode.get())
        if key:
            messagebox.showinfo("Key", f"Keep this key safe:\n{key.decode()}")
    except Exception as e:
        messagebox.showerror("Error", f"Encoding failed: {e}")


def decode_message():
    image_path = image_path_entry.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image or PDF first.")
        return
    if not password_entry.get().strip():
        messagebox.showerror("Error", "Please enter the decryption key.")
        return

    try:
        decode_and_decrypt_message(password_entry, image_path)
    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {e}")


# ---------- GUI ----------
root = tk.Tk()
root.title("Advanced Image & PDF Steganography")
root.geometry("520x420")
root.configure(bg="#f4f4f4")

# --- Encode Section
tk.Label(root, text="🔒 ENCODE SECTION", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=(10, 4))

encode_mode = tk.StringVar(value="text")

mode_frame = tk.Frame(root, bg="#f4f4f4")
mode_frame.pack()
tk.Label(mode_frame, text="Choose Mode:", bg="#f4f4f4", font=("Arial", 10, "bold")).pack(anchor="w")

tk.Radiobutton(mode_frame, text="Hide Text Message (image)", variable=encode_mode, value="text", bg="#f4f4f4").pack(anchor="w")
tk.Radiobutton(mode_frame, text="Hide File inside Image (any type)", variable=encode_mode, value="file", bg="#f4f4f4").pack(anchor="w")
tk.Radiobutton(mode_frame, text="Hide Text inside PDF (PDF steganography)", variable=encode_mode, value="pdf", bg="#f4f4f4").pack(anchor="w")

tk.Label(root, text="Secret Message / File Path:", bg="#f4f4f4").pack(pady=(6, 0))
secret_message_entry = tk.Entry(root, width=60)
secret_message_entry.pack()

tk.Label(root, text="Image / PDF Path:", bg="#f4f4f4").pack(pady=(6, 0))
image_path_entry = tk.Entry(root, width=60)
image_path_entry.pack()
tk.Button(root, text="Browse Cover (Image or PDF)", command=select_image).pack(pady=3)

tk.Button(root, text="Encode & Encrypt", command=encode_message).pack(pady=8)

# --- Decode Section
tk.Label(root, text="🔓 DECODE SECTION", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=(10, 4))
tk.Label(root, text="Decryption Key:", bg="#f4f4f4").pack()
password_entry = tk.Entry(root, width=60)
password_entry.pack()
tk.Button(root, text="Decode Message", command=decode_message).pack(pady=5)

root.mainloop()
