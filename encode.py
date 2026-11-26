"""from PIL import Image
from cryptography.fernet import Fernet
from tkinter import messagebox
import os


def encode_and_encrypt_message(secret_message_entry, input_image_path, mode="text"):
    ""
    Encrypts either a text message or a binary file and embeds it into an image using LSB steganography.
    mode = "text" or "file"
    ""
    try:
        output_path = os.path.splitext(input_image_path)[0] + "_encoded.png"
        image = Image.open(input_image_path).convert('RGB')
        pixels = list(image.getdata())
        width, height = image.size

        # Generate encryption key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # --- Prepare data based on mode ---
        if mode == "file":
            file_path = secret_message_entry.get().strip()
            if not os.path.exists(file_path):
                messagebox.showerror("Error", "Invalid file path.")
                return None, None

            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            encrypted_data = fernet.encrypt(file_bytes)
            metadata = f"file|{file_name}|{len(encrypted_data)}\n".encode()
            combined = metadata + encrypted_data

        else:  # text mode
            secret_message = secret_message_entry.get().strip()
            if not secret_message:
                messagebox.showerror("Error", "Secret message is empty.")
                return None, None

            encrypted_data = fernet.encrypt(secret_message.encode())
            metadata = b"text|none|0\n"
            combined = metadata + encrypted_data

        # --- Convert to binary for embedding ---
        binary_secret = ''.join(format(byte, '08b') for byte in combined)
        max_bits = len(pixels) * 3
        if len(binary_secret) > max_bits:
            raise ValueError("Message/File too large for this image. Try a larger image.")

        # --- Embed bits into pixels ---
        index = 0
        modified_pixels = []
        for pixel in pixels:
            r, g, b = map(lambda x: format(x, '08b'), pixel)
            if index < len(binary_secret):
                r = r[:-1] + binary_secret[index]; index += 1
            if index < len(binary_secret):
                g = g[:-1] + binary_secret[index]; index += 1
            if index < len(binary_secret):
                b = b[:-1] + binary_secret[index]; index += 1
            modified_pixels.append((int(r, 2), int(g, 2), int(b, 2)))
            if index >= len(binary_secret):
                modified_pixels.extend(pixels[len(modified_pixels):])
                break

        # --- Save encoded image ---
        encoded_img = Image.new('RGB', (width, height))
        encoded_img.putdata(modified_pixels)
        encoded_img.save(output_path)

        messagebox.showinfo("Encryption Key", f"Keep this key safe:\n{key.decode()}")
        return key, output_path

    except Exception as e:
        messagebox.showerror("Encoding Error", f"Failed to encode: {e}")
        return None, None
"""
from PIL import Image
from cryptography.fernet import Fernet
from tkinter import messagebox
import os
import base64

# PyPDF2 for PDF metadata handling
try:
    from PyPDF2 import PdfReader, PdfWriter
except Exception:
    PdfReader = None
    PdfWriter = None


def encode_and_encrypt_message(secret_message_entry, input_path, mode="text"):
    """
    Encrypts:
      - text into an image using LSB (mode="text")
      - a binary file into an image (mode="file")
      - text into a PDF metadata field (mode="pdf")
    Returns (key, output_path) or (None, None) on failure.
    """
    try:
        # Generate encryption key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # -------- PDF mode (store encrypted text in PDF metadata) --------
        if mode == "pdf":
            if PdfWriter is None:
                messagebox.showerror("Dependency Error", "PyPDF2 is required for PDF steganography. Install with:\n\npip install PyPDF2")
                return None, None

            if not os.path.exists(input_path):
                messagebox.showerror("File Error", "Selected PDF not found.")
                return None, None

            if not input_path.lower().endswith(".pdf"):
                messagebox.showerror("File Error", "Please select a PDF file for PDF steganography.")
                return None, None

            secret_text = secret_message_entry.get().strip()
            if not secret_text:
                messagebox.showerror("Error", "Secret message is empty.")
                return None, None

            encrypted_data = fernet.encrypt(secret_text.encode())
            b64_encrypted = base64.b64encode(encrypted_data).decode()

            reader = PdfReader(input_path)
            writer = PdfWriter()

            # copy pages
            for p in reader.pages:
                writer.add_page(p)

            # Preserve existing metadata and add HiddenData
            existing_meta = {}
            try:
                if reader.metadata:
                    # reader.metadata keys usually start with '/' (e.g. '/Title')
                    for k, v in reader.metadata.items():
                        if isinstance(k, str) and isinstance(v, (str, bytes)):
                            existing_meta[k] = v
            except Exception:
                existing_meta = {}

            # Add custom metadata entry
            # Use '/HiddenData' key (leading slash is expected by PyPDF2)
            existing_meta['/HiddenData'] = b64_encrypted
            writer.add_metadata(existing_meta)

            output_path = os.path.splitext(input_path)[0] + "_encoded.pdf"
            with open(output_path, "wb") as out_f:
                writer.write(out_f)

            messagebox.showinfo("Encryption Key", f"Keep this key safe:\n{key.decode()}")
            return key, output_path

        # -------- File hiding into image (binary) or text into image (LSB) --------
        # Both use LSB inside image
        output_path = os.path.splitext(input_path)[0] + "_encoded.png"
        image = Image.open(input_path).convert('RGB')
        pixels = list(image.getdata())
        width, height = image.size

        if mode == "file":
            file_path = secret_message_entry.get().strip()
            if not os.path.exists(file_path):
                messagebox.showerror("Error", "Invalid file path.")
                return None, None

            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            encrypted_data = fernet.encrypt(file_bytes)
            metadata = f"file|{file_name}|{len(encrypted_data)}\n".encode()
            combined = metadata + encrypted_data

        else:  # mode == "text"
            secret_message = secret_message_entry.get().strip()
            if not secret_message:
                messagebox.showerror("Error", "Secret message is empty.")
                return None, None

            encrypted_data = fernet.encrypt(secret_message.encode())
            metadata = b"text|none|0\n"
            combined = metadata + encrypted_data

        # Convert to binary string for embedding
        binary_secret = ''.join(format(byte, '08b') for byte in combined)
        max_bits = len(pixels) * 3
        if len(binary_secret) > max_bits:
            raise ValueError("Message/File too large for this image. Try a larger image.")

        # Embed bits into pixels' LSBs
        index = 0
        modified_pixels = []
        for pixel in pixels:
            r, g, b = map(lambda x: format(x, '08b'), pixel)
            if index < len(binary_secret):
                r = r[:-1] + binary_secret[index]; index += 1
            if index < len(binary_secret):
                g = g[:-1] + binary_secret[index]; index += 1
            if index < len(binary_secret):
                b = b[:-1] + binary_secret[index]; index += 1
            modified_pixels.append((int(r, 2), int(g, 2), int(b, 2)))
            if index >= len(binary_secret):
                modified_pixels.extend(pixels[len(modified_pixels):])
                break

        encoded_img = Image.new('RGB', (width, height))
        encoded_img.putdata(modified_pixels)
        encoded_img.save(output_path)

        messagebox.showinfo("Encryption Key", f"Keep this key safe:\n{key.decode()}")
        return key, output_path

    except Exception as e:
        messagebox.showerror("Encoding Error", f"Failed to encode: {e}")
        return None, None
