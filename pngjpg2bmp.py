#!/usr/bin/env python3
import os
import sys
from PIL import Image

def usage():
    print(f"Usage: {sys.argv[0]} <src_dir> <dst_dir>")
    print("  src_dir: source directory containing PNG/JPG images")
    print("  dst_dir: destination directory for BMP images")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

src_dir = sys.argv[1]
dst_dir = sys.argv[2]

if not os.path.exists(src_dir):
    print(f"Error: Source directory '{src_dir}' does not exist")
    sys.exit(1)

os.makedirs(dst_dir, exist_ok=True)

for fname in os.listdir(src_dir):
    if fname.lower().endswith((".jpg", ".jpeg", ".png")):
        src_path = os.path.join(src_dir, fname)
        base, _ = os.path.splitext(fname)
        dst_path = os.path.join(dst_dir, base + ".bmp")

        try:
            with Image.open(src_path) as img:
                # convert unsupported modes to rgb
                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")

                img.save(dst_path, format="BMP")
            print(f"converted {src_path} -> {dst_path}")

        except Exception as e:
            print(f"skipped {src_path} ({e})")

