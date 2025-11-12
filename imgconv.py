import os
import sys
import shutil
import time
import itertools
import threading
from PIL import Image
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)  # Enable colored text on Windows

# Optional imports for extra formats
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None

try:
    import pillow_avif
except ImportError:
    pillow_avif = None

try:
    import imageio.v3 as iio
except ImportError:
    iio = None

try:
    from psd_tools import PSDImage
except ImportError:
    PSDImage = None


# ✨ Fancy animated spinner
def spinner(text, duration=2.5):
    done = False
    def spin():
        for c in itertools.cycle(["|", "/", "-", "\\"]):
            if done:
                break
            sys.stdout.write(f"\r{Fore.CYAN}{text} {c}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")

    t = threading.Thread(target=spin)
    t.start()
    time.sleep(duration)
    done = True
    t.join()


# 🖼️ Conversion Function
def convert_image(input_path, output_path, output_format, resize_percent):
    ext = os.path.splitext(input_path)[1].lower()

    try:
        # PSD
        if PSDImage and ext == ".psd":
            psd = PSDImage.open(input_path)
            img = psd.composite()

        # SVG (safe import)
        elif ext == ".svg":
            try:
                import cairosvg
                png_temp = output_path.replace("." + output_format, ".png")
                cairosvg.svg2png(url=input_path, write_to=png_temp)
                img = Image.open(png_temp)
            except Exception:
                print(f"{Fore.YELLOW}⚠️ Skipping SVG (Cairo not installed or failed): {input_path}")
                return

        # RAW, EXR, HDR, DDS (via imageio)
        elif iio and ext in [".exr", ".hdr", ".dds", ".raw", ".cr2", ".nef", ".arw"]:
            data = iio.imread(input_path)
            img = Image.fromarray(data)

        # Default Pillow-supported
        else:
            img = Image.open(input_path)

        # Resize
        new_size = (
            int(img.width * (resize_percent / 100)),
            int(img.height * (resize_percent / 100))
        )
        img = img.resize(new_size, Image.LANCZOS)

        # Convert and save
        img.save(output_path, output_format.upper())

    except Exception as e:
        print(f"{Fore.RED}⚠️ Failed to convert {input_path}: {e}")


def animated_title():
    title = "=== 🧠 Universal Image Converter & Resizer ==="
    sub = "          by mm.zeinalzadeh@gmail.com"
    for char in title:
        sys.stdout.write(Fore.CYAN + char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()
    for char in sub:
        sys.stdout.write(Fore.YELLOW + char)
        sys.stdout.flush()
        time.sleep(0.01)
    print("\n")
    time.sleep(0.3)


def main():
    animated_title()
    spinner("Loading modules...")

    # Input folder
    input_folder = input(f"{Fore.GREEN}Enter the input folder path: ").strip()
    while not os.path.isdir(input_folder):
        input_folder = input(f"{Fore.RED}❌ Invalid folder. Try again: ").strip()

    # Choose export format
    supported_formats = [
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "ico",
        "ppm", "pgm", "pbm", "tga", "dds", "heic", "heif", "psd", "svg",
        "pdf", "exr", "hdr", "raw", "cr2", "nef", "arw", "avif"
    ]

    print(Fore.CYAN + "\nAvailable export formats:")
    for i, fmt in enumerate(supported_formats, 1):
        print(f"  {i:2d}. {Fore.WHITE}{fmt.upper()}")

    while True:
        try:
            choice = int(input(f"\n{Fore.GREEN}Select export format by number: "))
            if 1 <= choice <= len(supported_formats):
                export_format = supported_formats[choice - 1]
                break
            else:
                print(Fore.RED + "❌ Invalid number. Try again.")
        except ValueError:
            print(Fore.RED + "❌ Please enter a number.")

    # Resize percent
    try:
        resize_percent = float(input(f"{Fore.GREEN}Enter resize percentage (e.g., 50 for 50%): "))
        if resize_percent <= 0:
            raise ValueError
    except ValueError:
        resize_percent = 100.0
        print(Fore.YELLOW + "⚠️ Invalid number. Defaulting to 100% (no resize).")

    # Create export folder automatically in source path
    output_folder = os.path.join(input_folder, "export_mmz")
    if os.path.exists(output_folder):
        print(Fore.MAGENTA + "🗑️  Removing existing export_mmz folder...")
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    print(Fore.CYAN + f"📁 Created export folder: {output_folder}\n")

    # Supported input extensions
    supported_exts = (
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".ico",
        ".ppm", ".pgm", ".pbm", ".tga", ".dds", ".heic", ".heif", ".psd", ".svg",
        ".pdf", ".exr", ".hdr", ".raw", ".cr2", ".nef", ".arw", ".avif"
    )

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_exts)]
    if not files:
        print(Fore.RED + "❌ No supported image files found.")
        sys.exit()

    print(Fore.YELLOW + f"Found {len(files)} image(s). Starting conversion to {export_format.upper()}...\n")
    time.sleep(0.3)

    for i, filename in enumerate(tqdm(files, desc="Processing", unit="image"), 1):
        input_path = os.path.join(input_folder, filename)
        output_name = os.path.splitext(filename)[0] + "." + export_format
        output_path = os.path.join(output_folder, output_name)
        convert_image(input_path, output_path, export_format, resize_percent)

    print(Fore.GREEN + "\n✅ All images converted successfully!")
    print(Fore.CYAN + f"Saved to: {os.path.abspath(output_folder)}")
    print(Fore.MAGENTA + "\n✨ Conversion complete. Have a great day! ✨\n")


if __name__ == "__main__":
    main()
