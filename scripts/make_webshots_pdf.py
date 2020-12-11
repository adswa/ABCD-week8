#!/usr/bin/env python3

import os, sys
from imageio import imread
import numpy as np

def same(p1, p2):
    # for some reason the last "row" could flip a bit, so lets exclude some
    l = p1.shape[0] - 10
    diff = p1[:l] - p2[:l]
    nz = diff != 0
    total_diff = np.sum(nz)
    abs_diff = np.sum(np.abs(diff))
    max_diff = np.max(np.abs(diff))
    if total_diff:
        print(f"difference at {total_diff} for {abs_diff} max of {max_diff}")
        return False
    return True

#url = "http://datasets.datalad.org/repronim/artwork/talks/webinar-2020-reprocomp/"
#url = "http://localhost:8000/"
#name = "slide"

url, name = sys.argv[1:3]
# TEMP:
stop_at = 5

prev_s1 = None
slides = []
for s1 in range(1000):
    prev_s2 = prev_s1
    if stop_at and len(slides) >= stop_at:
        break
    for s2 in range(1000):
        os.system(f"chromium --headless --disable-gpu --window-size=1024,768 --screenshot {url}#/{s1}/{s2}")
        png = imread("screenshot.png")
        if prev_s2 is not None and same(png, prev_s2):
              print(f"End of {s1} at {s2}")
              break
        prev_s2 = png
        slide = f"{name}-{s1:03d}-{s2:03d}.png"
        slides.append(slide)
        os.system(f"mv screenshot.png {slide}")
    if prev_s1 is not None and same(prev_s1, prev_s2):
        print(f"Total end at {s1}")
        break
    prev_s1 = prev_s2
pdf = f"{name}.pdf"
print(f"Converting {len(slides)} to {pdf}")
all_slides = " ".join(slides)
os.system(f"convert {all_slides} {pdf}")
