Image Steganography Using Python

Project Overview
This project implements image steganography using Python, allowing users to encode and decode information within images. It combines Least Significant Bit (LSB) steganography with Fernet encryption to protect hidden data.
The application provides a graphical user interface for performing encoding and decoding operations.

Features

- **LSB Steganography:** Hide information within digital images using the Least Significant Bit technique.
- **Encryption & Decryption:** Secure hidden data using Fernet symmetric encryption.
- **Text Hiding:** Encrypt and embed text messages within images.
- **File Hiding:** Encrypt and embed files within images.
- **PDF Functionality:** Store encrypted text in PDF metadata.
- **Graphical User Interface:** Perform operations through a Tkinter-based interface.
- **Email Integration:** Send encoded files through email using Gmail SMTP.

Technologies Used

- Python
- Tkinter
- Pillow (PIL)
- Cryptography (Fernet)
- PyPDF2
- SMTP (Email Integration)

Installation and Setup

 1. Clone the Repository

```bash
git clone https://github.com/kbhumi5/image-steganography.git
```

 2. Navigate to the Project Directory

```bash
cd image-steganography
```

 3. Install Dependencies

```bash
pip install -r requirements.txt
```

 4. Run the Application

Run the project's main GUI entry-point file:

```bash
python main_gui.py
```

 Project Structure

|      File      |      Description       |
|----------------|------------------------|
| `main_gui.py` | Graphical user interface |
| `main.py` | Main application functionality |
| `encode.py` | Encryption and data encoding |
| `decode.py` | Data extraction and decryption |
| `data.py` | Supporting data functionality |
| `mail.py` | Email integration |

 Security Note

- Keep encryption keys confidential and secure.
- Never commit passwords, API keys, or other credentials.
- Use authorised test files and images.
- Email functionality requires appropriately configured credentials.

