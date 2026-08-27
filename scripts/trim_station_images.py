"""Trim uniform or near-uniform borders from station image thumbnails.

This improved script saves cropped output into `data/web/station_images_cropped/`
by default so originals are preserved. Use `--inplace` to overwrite originals.

Usage:
  python3 scripts/trim_station_images.py [--tolerance N] [--padding P] [--inplace]

Options:
  --tolerance N   Pixel difference threshold (0-255). Higher = more aggressive. Default 12.
  --padding P     Add P pixels of padding around crop box. Default 2.
  --inplace       Overwrite original images instead of writing to *_cropped/.

Requirements: Pillow (`pip install Pillow`). Run locally.
"""
from PIL import Image, ImageChops
import os
import sys
import argparse

IMG_DIR = os.path.join('data', 'web', 'station_images')


def trim_image(path, outpath, tol=12, padding=2):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    # sample background color from corners (average) to be robust
    samples = [im.getpixel((0, 0)), im.getpixel((w - 1, 0)), im.getpixel((0, h - 1)), im.getpixel((w - 1, h - 1))]
    avg = tuple(int(sum(c[i] for c in samples) / len(samples)) for i in range(4))
    bg = Image.new('RGBA', im.size, avg)

    diff = ImageChops.difference(im, bg)
    # convert to grayscale and threshold by tolerance
    gray = diff.convert('L')
    # create a binary mask where pixels above tolerance are 255
    mask = gray.point(lambda p: 255 if p > tol else 0)
    bbox = mask.getbbox()
    if not bbox:
        return False, None
    left, upper, right, lower = bbox
    left = max(0, left - padding)
    upper = max(0, upper - padding)
    right = min(w, right + padding)
    lower = min(h, lower + padding)
    cropped = im.crop((left, upper, right, lower))
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    cropped.save(outpath)
    return True, outpath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tolerance', type=int, default=12, help='Pixel difference tolerance (0-255)')
    parser.add_argument('--padding', type=int, default=2, help='Padding to add after crop')
    parser.add_argument('--inplace', action='store_true', help='Overwrite original images')
    args = parser.parse_args()

    if not os.path.isdir(IMG_DIR):
        print(f"Directory not found: {IMG_DIR}")
        sys.exit(1)
    files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        print('No image files found in', IMG_DIR)
        return

    out_dir = IMG_DIR
    if not args.inplace:
        out_dir = os.path.join('data', 'web', 'station_images_cropped')
        os.makedirs(out_dir, exist_ok=True)

    changed = 0
    for fn in files:
        path = os.path.join(IMG_DIR, fn)
        outpath = os.path.join(out_dir, fn)
        try:
            ok, saved = trim_image(path, outpath, tol=args.tolerance, padding=args.padding)
            if ok:
                print('Trimmed', fn, '->', saved)
                changed += 1
            else:
                # copy original if not inplace
                if not args.inplace and path != outpath:
                    Image.open(path).save(outpath)
                print('No trim needed for', fn)
        except Exception as e:
            print('Failed', fn, e)
    print(f'Done. Trimmed {changed} / {len(files)} images. Output dir: {out_dir}')


if __name__ == '__main__':
    main()
