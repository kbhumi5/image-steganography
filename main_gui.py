"""import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os

# Import your modules
from encode import encode_and_encrypt_message
from decode import decode_and_decrypt_message
from mail import send_email_with_image


class SteganographyApp:
    THUMB_SIZE = (150, 150)

    def __init__(self, root):
        self.root = root
        root.title("Steganography Security System")
        root.configure(bg="#f2f2f2")
        root.geometry("650x780")

        main_frame = tk.Frame(root, bg="#f2f2f2")
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame, bg="#f2f2f2", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame = tk.Frame(self.canvas, bg="#f2f2f2")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self._build_encode_section()
        self._build_separator()
        self._build_decode_section()

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    # ---------------- ENCODE SECTION ----------------
    def _build_encode_section(self):
        frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=0, padx=12, pady=12)
        frame.pack(padx=20, pady=(20, 10), fill="x")

        tk.Label(frame, text="🔒 ENCODE SECTION", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w")

        # --- Encoding mode choice ---
        self.encode_mode = tk.StringVar(value="text")
        mode_frame = tk.Frame(frame, bg="#ffffff")
        mode_frame.pack(pady=(5, 10))

        tk.Label(mode_frame, text="Choose Encoding Mode:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Hide Text Message", variable=self.encode_mode, value="text",
                       bg="#ffffff", font=("Arial", 9)).pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Hide File (any type)", variable=self.encode_mode, value="file",
                       bg="#ffffff", font=("Arial", 9)).pack(anchor="w")

        tk.Label(frame, text="Enter Secret Message:", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        self.secret_entry = tk.Entry(frame, width=60)
        self.secret_entry.pack(pady=4)

        tk.Label(frame, text="Select Cover Image (.png/.jpg/.jpeg):", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        browse_btn = tk.Button(frame, text="Browse Image", command=self.browse_cover_image)
        browse_btn.pack(pady=(6, 4))

        self.encode_preview_label = tk.Label(frame, bg="#ffffff")
        self.encode_preview_label.pack(pady=(0, 6))

        tk.Label(frame, text="Receiver Email (to send encoded image + key):", bg="#ffffff").pack(anchor="w", pady=(6, 0))
        self.receiver_email_entry = tk.Entry(frame, width=60)
        self.receiver_email_entry.pack(pady=4)

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.pack(pady=(8, 0))

        tk.Button(btn_frame, text="ENCODE & SEND", width=18, command=self.encode_and_send).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="CLEAR ENCODE", width=14, command=self.clear_encode_fields).grid(row=0, column=1, padx=6)

        self.encode_image_path = None

    def _build_separator(self):
        sep = tk.Frame(self.scrollable_frame, height=2, bd=0, bg="#e0e0e0")
        sep.pack(fill="x", padx=20, pady=(8, 8))

    # ---------------- DECODE SECTION ----------------
    def _build_decode_section(self):
        frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=0, padx=12, pady=12)
        frame.pack(padx=20, pady=(0, 20), fill="x")

        tk.Label(frame, text="🔓 DECODE SECTION", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w")

        tk.Label(frame, text="Select Encoded Image (.png/.jpg/.jpeg):", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        browse_dec_btn = tk.Button(frame, text="Browse Encoded Image", command=self.browse_encoded_image)
        browse_dec_btn.pack(pady=(6, 4))

        self.decode_preview_label = tk.Label(frame, bg="#ffffff")
        self.decode_preview_label.pack(pady=(0, 6))

        tk.Label(frame, text="Enter Decryption Key:", bg="#ffffff").pack(anchor="w", pady=(6, 0))
        self.decode_key_entry = tk.Entry(frame, width=60)
        self.decode_key_entry.pack(pady=4)

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.pack(pady=(8, 0))

        tk.Button(btn_frame, text="DECODE & SHOW MESSAGE", width=20, command=self.decode_image).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="CLEAR DECODE", width=14, command=self.clear_decode_fields).grid(row=0, column=1, padx=6)

        self.decode_image_path = None

    # ---------------- BROWSING FUNCTIONS ----------------
    def browse_cover_image(self):
        "Select cover image (PNG/JPG only)."
        path = filedialog.askopenfilename(
            title="Select Cover Image (.png/.jpg/.jpeg)",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.encode_image_path = path
            self._show_preview(path, self.encode_preview_label)

    def browse_encoded_image(self):
        "Select encoded image (PNG/JPG only)."
        path = filedialog.askopenfilename(
            title="Select Encoded Image (.png/.jpg/.jpeg)",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.decode_image_path = path
            self._show_preview(path, self.decode_preview_label)

    # ---------------- HELPER METHODS ----------------
    def _show_preview(self, path, label_widget):
        try:
            img = Image.open(path)
            img.thumbnail(self.THUMB_SIZE)
            self._last_preview_image = ImageTk.PhotoImage(img)
            label_widget.configure(image=self._last_preview_image)
        except Exception:
            label_widget.configure(image='')

    def clear_encode_fields(self):
        self.secret_entry.delete(0, tk.END)
        self.receiver_email_entry.delete(0, tk.END)
        self.encode_image_path = None
        self.encode_preview_label.configure(image='')

    def clear_decode_fields(self):
        self.decode_key_entry.delete(0, tk.END)
        self.decode_image_path = None
        self.decode_preview_label.configure(image='')

    # ---------------- ENCODING + EMAIL ----------------
    def encode_and_send(self):
        if not self.encode_image_path or not os.path.exists(self.encode_image_path):
            messagebox.showerror("Error", "Please select a valid cover image.")
            return

        receiver = self.receiver_email_entry.get().strip()
        if not receiver:
            messagebox.showerror("Error", "Please enter receiver email.")
            return

        # If hiding file
        if self.encode_mode.get() == "file":
            # Allow selecting any file type
            file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[
                    ("All Files", "*.*"),
                    ("Text Files", "*.txt"),
                    ("PDF Files", "*.pdf"),
                    ("Word Documents", "*.docx"),
                    ("ZIP Files", "*.zip"),
                    ("Images", "*.png;*.jpg;*.jpeg")
                ]
            )
            if not file_path:
                messagebox.showerror("Error", "No file selected to hide.")
                return
            self.secret_entry.delete(0, tk.END)
            self.secret_entry.insert(0, file_path)
        else:
            if not self.secret_entry.get().strip():
                messagebox.showerror("Error", "Please enter a secret message.")
                return

        try:
            key, output_path = encode_and_encrypt_message(
                self.secret_entry, self.encode_image_path, self.encode_mode.get()
            )
            if key and output_path:
                threading.Thread(
                    target=self._send_email_thread,
                    args=(receiver, key, output_path),
                    daemon=True
                ).start()
            else:
                messagebox.showerror("Error", "Encoding failed — no output generated.")
        except Exception as e:
            messagebox.showerror("Error", f"Encoding error: {e}")

    def _send_email_thread(self, receiver_email, key, output_path):
        try:
            send_email_with_image(receiver_email, key, output_path)
            messagebox.showinfo("Success", f"✅ Email sent successfully.\nSaved image: {output_path}")
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email:\n{e}")

    # ---------------- DECODING ----------------
    def decode_image(self):
        if not self.decode_image_path or not os.path.exists(self.decode_image_path):
            messagebox.showerror("Error", "Please select a valid encoded image.")
            return
        if not self.decode_key_entry.get().strip():
            messagebox.showerror("Error", "Please enter the decryption key.")
            return

        try:
            decode_and_decrypt_message(self.decode_key_entry, self.decode_image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Decoding error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os

# Import your modules
from encode import encode_and_encrypt_message
from decode import decode_and_decrypt_message
from mail import send_email_with_image


class SteganographyApp:
    THUMB_SIZE = (150, 150)

    def __init__(self, root):
        self.root = root
        root.title("Steganography Security System")
        root.configure(bg="#f2f2f2")
        root.geometry("650x780")

        main_frame = tk.Frame(root, bg="#f2f2f2")
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame, bg="#f2f2f2", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame = tk.Frame(self.canvas, bg="#f2f2f2")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self._build_encode_section()
        self._build_separator()
        self._build_decode_section()

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    # ---------------- ENCODE SECTION ----------------
    def _build_encode_section(self):
        frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=0, padx=12, pady=12)
        frame.pack(padx=20, pady=(20, 10), fill="x")

        tk.Label(frame, text="🔒 ENCODE SECTION", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w")

        # --- Encoding mode choice ---
        self.encode_mode = tk.StringVar(value="text")
        mode_frame = tk.Frame(frame, bg="#ffffff")
        mode_frame.pack(pady=(5, 10))

        tk.Label(mode_frame, text="Choose Encoding Mode:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Hide Text Message (image)", variable=self.encode_mode, value="text",
                       bg="#ffffff", font=("Arial", 9)).pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Hide File (any type) inside Image", variable=self.encode_mode, value="file",
                       bg="#ffffff", font=("Arial", 9)).pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Hide Text inside PDF (PDF steganography)", variable=self.encode_mode, value="pdf",
                       bg="#ffffff", font=("Arial", 9)).pack(anchor="w")

        tk.Label(frame, text="Enter Secret Message (or leave blank to choose a file when mode=file):", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        self.secret_entry = tk.Entry(frame, width=60)
        self.secret_entry.pack(pady=4)

        tk.Label(frame, text="Select Cover (Image or PDF):", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        browse_btn = tk.Button(frame, text="Browse Cover", command=self.browse_cover_image)
        browse_btn.pack(pady=(6, 4))

        self.encode_preview_label = tk.Label(frame, bg="#ffffff")
        self.encode_preview_label.pack(pady=(0, 6))

        tk.Label(frame, text="Receiver Email (to send encoded file + key):", bg="#ffffff").pack(anchor="w", pady=(6, 0))
        self.receiver_email_entry = tk.Entry(frame, width=60)
        self.receiver_email_entry.pack(pady=4)

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.pack(pady=(8, 0))

        tk.Button(btn_frame, text="ENCODE & SEND", width=18, command=self.encode_and_send).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="CLEAR ENCODE", width=14, command=self.clear_encode_fields).grid(row=0, column=1, padx=6)

        self.encode_image_path = None

    def _build_separator(self):
        sep = tk.Frame(self.scrollable_frame, height=2, bd=0, bg="#e0e0e0")
        sep.pack(fill="x", padx=20, pady=(8, 8))

    # ---------------- DECODE SECTION ----------------
    def _build_decode_section(self):
        frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=0, padx=12, pady=12)
        frame.pack(padx=20, pady=(0, 20), fill="x")

        tk.Label(frame, text="🔓 DECODE SECTION", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w")

        tk.Label(frame, text="Select Encoded File (.png/.jpg/.jpeg/.pdf):", bg="#ffffff").pack(anchor="w", pady=(8, 0))
        browse_dec_btn = tk.Button(frame, text="Browse Encoded File", command=self.browse_encoded_image)
        browse_dec_btn.pack(pady=(6, 4))

        self.decode_preview_label = tk.Label(frame, bg="#ffffff")
        self.decode_preview_label.pack(pady=(0, 6))

        tk.Label(frame, text="Enter Decryption Key:", bg="#ffffff").pack(anchor="w", pady=(6, 0))
        self.decode_key_entry = tk.Entry(frame, width=60)
        self.decode_key_entry.pack(pady=4)

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.pack(pady=(8, 0))

        tk.Button(btn_frame, text="DECODE & SHOW MESSAGE", width=20, command=self.decode_image).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="CLEAR DECODE", width=14, command=self.clear_decode_fields).grid(row=0, column=1, padx=6)

        self.decode_image_path = None

    # ---------------- BROWSING FUNCTIONS ----------------
    def browse_cover_image(self):
        "Select cover image (PNG/JPG only) or PDF if mode=pdf."
        if self.encode_mode.get() == "pdf":
            path = filedialog.askopenfilename(
                title="Select Cover PDF",
                filetypes=[("PDF Files", "*.pdf")]
            )
        else:
            path = filedialog.askopenfilename(
                title="Select Cover Image (.png/.jpg/.jpeg)",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
            )

        if path:
            self.encode_image_path = path
            # If PDF selected, show text label. If image, show thumbnail.
            if path.lower().endswith(".pdf"):
                self.encode_preview_label.configure(text=f"PDF selected: {os.path.basename(path)}", image='')
            else:
                self._show_preview(path, self.encode_preview_label)

    def browse_encoded_image(self):
        "Select encoded image/pdf"
        path = filedialog.askopenfilename(
            title="Select Encoded File (.png/.jpg/.jpeg/.pdf)",
            filetypes=[("Encoded Files", "*.png;*.jpg;*.jpeg;*.pdf")]
        )
        if path:
            self.decode_image_path = path
            if path.lower().endswith(".pdf"):
                self.decode_preview_label.configure(text=f"PDF selected: {os.path.basename(path)}", image='')
            else:
                self._show_preview(path, self.decode_preview_label)

    # ---------------- HELPER METHODS ----------------
    def _show_preview(self, path, label_widget):
        try:
            img = Image.open(path)
            img.thumbnail(self.THUMB_SIZE)
            self._last_preview_image = ImageTk.PhotoImage(img)
            label_widget.configure(image=self._last_preview_image, text='')
        except Exception:
            label_widget.configure(image='', text='')

    def clear_encode_fields(self):
        self.secret_entry.delete(0, tk.END)
        self.receiver_email_entry.delete(0, tk.END)
        self.encode_image_path = None
        self.encode_preview_label.configure(image='', text='')

    def clear_decode_fields(self):
        self.decode_key_entry.delete(0, tk.END)
        self.decode_image_path = None
        self.decode_preview_label.configure(image='', text='')

    # ---------------- ENCODING + EMAIL ----------------
    def encode_and_send(self):
        if not self.encode_image_path or not os.path.exists(self.encode_image_path):
            messagebox.showerror("Error", "Please select a valid cover image or PDF.")
            return

        receiver = self.receiver_email_entry.get().strip()
        if not receiver:
            messagebox.showerror("Error", "Please enter receiver email.")
            return

        # If hiding file into image
        if self.encode_mode.get() == "file":
            # Allow selecting any file type
            file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[
                    ("All Files", "*.*"),
                    ("Text Files", "*.txt"),
                    ("PDF Files", "*.pdf"),
                    ("Word Documents", "*.docx"),
                    ("ZIP Files", "*.zip"),
                    ("Images", "*.png;*.jpg;*.jpeg")
                ]
            )
            if not file_path:
                messagebox.showerror("Error", "No file selected to hide.")
                return
            self.secret_entry.delete(0, tk.END)
            self.secret_entry.insert(0, file_path)
        else:
            if not self.secret_entry.get().strip():
                messagebox.showerror("Error", "Please enter a secret message.")
                return

        try:
            key, output_path = encode_and_encrypt_message(
                self.secret_entry, self.encode_image_path, self.encode_mode.get()
            )
            if key and output_path:
                threading.Thread(
                    target=self._send_email_thread,
                    args=(receiver, key, output_path),
                    daemon=True
                ).start()
            else:
                messagebox.showerror("Error", "Encoding failed — no output generated.")
        except Exception as e:
            messagebox.showerror("Error", f"Encoding error: {e}")

    def _send_email_thread(self, receiver_email, key, output_path):
        try:
            send_email_with_image(receiver_email, key, output_path)
            messagebox.showinfo("Success", f"✅ Email sent successfully.\nSaved file: {output_path}")
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email:\n{e}")

    # ---------------- DECODING ----------------
    def decode_image(self):
        if not self.decode_image_path or not os.path.exists(self.decode_image_path):
            messagebox.showerror("Error", "Please select a valid encoded file.")
            return
        if not self.decode_key_entry.get().strip():
            messagebox.showerror("Error", "Please enter the decryption key.")
            return

        try:
            decode_and_decrypt_message(self.decode_key_entry, self.decode_image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Decoding error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
