"""from PIL import Image
from cryptography.fernet import Fernet
from tkinter import messagebox, filedialog
import os


def decode_and_decrypt_message(key_entry, input_image_path):
    #Decodes and decrypts a hidden message or file from an image.
    try:
        key = key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "No decryption key provided.")
            return

        image = Image.open(input_image_path).convert('RGB')
        pixels = list(image.getdata())

        # --- Extract bits from LSB ---
        binary_data = ""
        for pixel in pixels:
            for value in pixel:
                binary_data += format(value, '08b')[-1]

        all_bytes = [int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8)]
        decoded_bytes = bytes(all_bytes)

        header_end = decoded_bytes.find(b'\n')
        if header_end == -1:
            raise ValueError("Corrupted data: header not found.")

        header = decoded_bytes[:header_end].decode(errors="ignore")
        content = decoded_bytes[header_end + 1:]

        parts = header.split("|")
        if len(parts) < 3:
            raise ValueError("Invalid header format.")

        mode = parts[0]
        filename = parts[1]
        size = int(parts[2])

        fernet = Fernet(key)

        if mode == "text":
            decrypted_text = fernet.decrypt(content).decode(errors="ignore")
            messagebox.showinfo("Decoded Message", f"🕵️ Hidden message:\n\n{decrypted_text}")

        elif mode == "file":
            encrypted_data = content[:size]
            decrypted_data = fernet.decrypt(encrypted_data)

            save_path = filedialog.asksaveasfilename(
                title="Save Recovered File As",
                initialfile=filename
            )
            if save_path:
                with open(save_path, "wb") as f_out:
                    f_out.write(decrypted_data)
                messagebox.showinfo("Success", f"✅ File successfully recovered:\n{save_path}")
            else:
                messagebox.showinfo("Cancelled", "File save cancelled by user.")
        else:
            raise ValueError("Unknown mode type in header (expected 'text' or 'file').")

    except Exception as e:
        messagebox.showerror("Decoding Error", f"Failed to decode or decrypt data:\n{e}")
"""

from PIL import Image
from cryptography.fernet import Fernet
from tkinter import messagebox, filedialog
import os
import base64

# PyPDF2 for PDF metadata handling
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None


def decode_and_decrypt_message(key_entry, input_path):
    #Decodes and decrypts a hidden message or file from an image or PDF.
    try:
        key = key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "No decryption key provided.")
            return

        # ---------- PDF decoding ----------
        if input_path.lower().endswith(".pdf"):
            if PdfReader is None:
                messagebox.showerror("Dependency Error", "PyPDF2 is required for PDF steganography. Install with:\n\npip install PyPDF2")
                return

            if not os.path.exists(input_path):
                messagebox.showerror("File Error", "Selected PDF not found.")
                return

            reader = PdfReader(input_path)
            meta = {}
            try:
                if reader.metadata:
                    for k, v in reader.metadata.items():
                        meta[k] = v
            except Exception:
                meta = {}

            # Try to fetch our stored base64 encrypted data
            hidden_b64 = None
            # metadata keys generally have leading '/', but try both
            if '/HiddenData' in meta:
                hidden_b64 = meta.get('/HiddenData')
            elif 'HiddenData' in meta:
                hidden_b64 = meta.get('HiddenData')

            if not hidden_b64:
                messagebox.showerror("Decoding Error", "No hidden data found in PDF metadata.")
                return

            # Ensure string (could be bytes)
            if isinstance(hidden_b64, bytes):
                hidden_b64 = hidden_b64.decode(errors='ignore')

            encrypted_bytes = base64.b64decode(hidden_b64)
            fernet = Fernet(key)
            try:
                decrypted_text = fernet.decrypt(encrypted_bytes).decode(errors="ignore")
                messagebox.showinfo("Decoded Message", f"🕵️ Hidden message:\n\n{decrypted_text}")
            except Exception as e:
                raise ValueError("Decryption failed. Check the key or the file.") from e

            return

        # ---------- Image LSB decoding (existing logic) ----------
        image = Image.open(input_path).convert('RGB')
        pixels = list(image.getdata())

        # Extract bits from LSBs
        binary_data = ""
        for pixel in pixels:
            for value in pixel:
                binary_data += format(value, '08b')[-1]

        # Convert to bytes
        all_bytes = [int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8)]
        decoded_bytes = bytes(all_bytes)

        # Now find header (ends with newline)
        header_end = decoded_bytes.find(b'\n')
        if header_end == -1:
            raise ValueError("Corrupted data: header not found.")

        header = decoded_bytes[:header_end].decode(errors="ignore")
        content = decoded_bytes[header_end + 1:]

        parts = header.split("|")
        if len(parts) < 3:
            raise ValueError("Invalid header format.")

        mode = parts[0]
        filename = parts[1]
        size = int(parts[2])

        fernet = Fernet(key)

        if mode == "text":
            decrypted_text = fernet.decrypt(content).decode(errors="ignore")
            messagebox.showinfo("Decoded Message", f"🕵️ Hidden message:\n\n{decrypted_text}")

        elif mode == "file":
            encrypted_data = content[:size]
            decrypted_data = fernet.decrypt(encrypted_data)

            save_path = filedialog.asksaveasfilename(
                title="Save Recovered File As",
                initialfile=filename
            )
            if save_path:
                with open(save_path, "wb") as f_out:
                    f_out.write(decrypted_data)
                messagebox.showinfo("Success", f"✅ File successfully recovered:\n{save_path}")
            else:
                messagebox.showinfo("Cancelled", "File save cancelled by user.")
        else:
            raise ValueError("Unknown mode type in header (expected 'text' or 'file').")

    except Exception as e:
        # Bubble up helpful message
        messagebox.showerror("Decoding Error", f"Failed to decode or decrypt data:\n{e}")
