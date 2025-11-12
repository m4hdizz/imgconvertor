🧠 Universal Image Converter & Resizer

Convert and resize images in 28 formats:
JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, ICO, PPM, PGM, PBM, TGA, DDS, HEIC, HEIF, PSD, SVG, PDF, EXR, HDR, RAW, CR2, NEF, ARW, AVIF.
Fast, simple & automatic export folder.

⚙️ HOW TO USE (FOR BEGINNERS)

1️⃣ INSTALL PYTHON
Download Python 3.10 or newer from:
https://www.python.org/downloads

During setup, make sure you check:
✅ Add Python to PATH

2️⃣ INSTALL REQUIRED LIBRARIES

Open Command Prompt (CMD) and run:
pip install pillow tqdm pillow-heif pillow-avif-plugin imageio psd-tools cairosvg reportlab

3️⃣ RUN THE PROGRAM

Navigate to your folder:
cd path\to\your\imgconvertor\

Run the program:
python imgconvert.py

You’ll see:
=== 🧠 Universal Image Converter & Resizer ===
by mm.zeinalzadeh@gmail.com

4️⃣ FOLLOW THE ON-SCREEN PROMPTS

The program will ask:

Enter the input folder path:
C:\Users\YourName\Pictures

Select export format (number):
1 for JPG, 2 for PNG, etc.

Enter resize percentage (e.g. 50 for 50%)

✅ Output folder will be created automatically:
C:\Users\YourName\Pictures\export_mmz

All converted images will be saved there.

5️⃣ OPTIONAL: CONVERT TO EXE

To make a standalone Windows app (no Python needed):

Install PyInstaller:
pip install pyinstaller

Then build:
pyinstaller --onefile --noconsole imgconvert.py

The .exe file will appear inside:
dist\imgconvert.exe



License: MIT © 2025
