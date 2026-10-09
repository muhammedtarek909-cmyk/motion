import sys, os, glob
from PIL import Image, ImageDraw
root = sys.argv[1]; out = sys.argv[2]; ids = sys.argv[3:]
TW, TH, COLS = 320, 200, 8
rows = []
for i in ids:
    fs = sorted(glob.glob(os.path.join(root, i, "*.jpg")))
    rows.append((i, fs))
sheet = Image.new("RGB", (COLS * TW, len(rows) * TH), "white")
d = ImageDraw.Draw(sheet)
for r, (i, fs) in enumerate(rows):
    for c, f in enumerate(fs[:COLS]):
        im = Image.open(f); im.thumbnail((TW - 4, TH - 4))
        sheet.paste(im, (c * TW + 2, r * TH + 2))
        d.rectangle([c*TW+2, r*TH+2, c*TW+80, r*TH+18], fill="black")
        d.text((c * TW + 5, r * TH + 4), os.path.basename(f)[:-4], fill="yellow")
sheet.save(out, quality=80)
