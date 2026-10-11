#!/usr/bin/env python3
"""Render hardware/mannequin/mannequin.scad as a turntable GIF (media/mannequin-turntable.gif)
and a still (docs/figures/mannequin.png) with a local OpenSCAD.

    python3 tools/render_mannequin.py [--frames 36] [--size 720]

Needs the `openscad` binary (macOS: brew install --cask openscad).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCAD = os.path.join(ROOT, "hardware", "mannequin", "mannequin.scad")
GIF = os.path.join(ROOT, "media", "mannequin-turntable.gif")
PNG = os.path.join(ROOT, "docs", "figures", "mannequin.png")

import glob

CANDIDATES = ["openscad", "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
              os.path.expanduser("~/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD")] + \
             sorted(glob.glob("/opt/homebrew/Caskroom/openscad/*/OpenSCAD*.app/Contents/MacOS/OpenSCAD"))


def find_openscad():
    for c in CANDIDATES:
        p = shutil.which(c) if not c.startswith("/") else (c if os.path.exists(c) else None)
        if p:
            return p
    sys.exit("openscad not found; install it or use the Forge preview endpoint")


def render(openscad, spin, out, size):
    # camera: eye on a 25 deg elevation, looking at the chest; perspective projection
    cam = "0,0,1290,68,0,0,2150"   # center x,y,z, rot x,y,z, distance
    cmd = [openscad, "-o", out, "-D", f"spin={spin}", "--camera=" + cam, "--projection=p",
           f"--imgsize={size},{size}", "--colorscheme=Tomorrow", SCAD]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=36)
    ap.add_argument("--size", type=int, default=720)
    ap.add_argument("--out-size", type=int, default=560)
    args = ap.parse_args()
    openscad = find_openscad()
    tmp = tempfile.mkdtemp()
    frames = []
    for i in range(args.frames):
        spin = 360.0 * i / args.frames
        out = os.path.join(tmp, f"f{i:03d}.png")
        render(openscad, spin, out, args.size)
        im = Image.open(out).convert("RGB")
        im = im.resize((args.out_size, args.out_size), Image.LANCZOS)
        frames.append(im)
        print(f"frame {i + 1}/{args.frames}", end="\r", flush=True)
    print()
    os.makedirs(os.path.dirname(GIF), exist_ok=True)
    os.makedirs(os.path.dirname(PNG), exist_ok=True)
    pal = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(GIF, save_all=True, append_images=pal[1:], duration=90, loop=0, optimize=True)
    frames[int(args.frames * 0.08)].save(PNG)
    print(f"wrote {os.path.relpath(GIF)} ({os.path.getsize(GIF) / 1e6:.1f} MB) and {os.path.relpath(PNG)}")


if __name__ == "__main__":
    main()
