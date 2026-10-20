import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1]
OUT_DIR = sys.argv[2]

H = 96
FW, FH = 44, 104
PAD_TOP = 6

src = Image.open(SRC).convert("RGBA")
a = np.array(src)
mask = a[:, :, 3] > 128
ys, xs = np.where(mask)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
crop = src.crop((x0, y0, x1 + 1, y1 + 1))


def clean(img, target_h, colors=40):
    w = round(img.width * target_h / img.height)
    arr = np.array(img).astype(np.float32)
    arr[:, :, :3] *= arr[:, :, 3:4] / 255.0
    pre = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((w, target_h), Image.LANCZOS)
    p = np.array(pre).astype(np.float32)
    alpha = p[:, :, 3:4]
    rgb = np.where(alpha > 0, p[:, :, :3] / np.maximum(alpha, 1) * 255.0, 0).clip(0, 255)
    opaque = alpha[:, :, 0] > 140
    rgbimg = Image.fromarray(rgb.astype(np.uint8), "RGB")
    q = rgbimg.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    out = np.dstack([np.array(q), (opaque * 255).astype(np.uint8)])
    return out


spr = clean(crop, H)
sh, sw = spr.shape[:2]
alpha = spr[:, :, 3] > 0

rows_with = alpha.sum(axis=1)
hip = int(sh * 0.535)
bottom = sh - 1
foot_rows = alpha[bottom - 6 : bottom + 1]
cols = np.where(foot_rows.any(axis=0))[0]
gaps = [c for c in range(cols.min(), cols.max()) if not foot_rows[:, c].any()]
split = int(np.mean(gaps)) if gaps else sw // 2
print("sprite", sw, sh, "hip", hip, "split", split)

leg_start = hip
crotch = hip
for r in range(sh - 1, hip, -1):
    if alpha[r, split]:
        crotch = r
        break
leg_top = min(sh - 8, crotch - 2)
print("crotch", crotch)

hair_pix = spr[: int(sh * 0.14)][alpha[: int(sh * 0.14)]][:, :3]
hair_cols = sorted({tuple(int(v) for v in c) for c in hair_pix if sum(int(v) for v in c) < 210 and int(c[0]) < int(c[1]) + 25}, key=sum)
print("hair palette", len(hair_cols))
shirt_ref = tuple(int(v) for v in spr[int(sh * 0.36), sw // 2 - 4, :3])
print("hair", hair_cols, "shirt", shirt_ref)


def canvas():
    return np.zeros((FH, FW, 4), np.uint8)


def paste(dst, img, ox, oy, region=None):
    h, w = img.shape[:2]
    for y in range(h):
        for x in range(w):
            if img[y, x, 3] == 0:
                continue
            dy, dx = oy + y, ox + x
            if 0 <= dy < FH and 0 <= dx < FW:
                dst[dy, dx] = img[y, x]


def make_back(img):
    b = img.copy()
    head_end = int(sh * 0.205)
    rng = np.random.RandomState(4)
    for y in range(0, head_end + 1):
        for x in range(sw):
            if b[y, x, 3]:
                lum = sum(int(v) for v in b[y, x, :3])
                if lum > 210 or y > head_end * 0.55 or x < 4 or x > sw - 5:
                    pick = min(len(hair_cols) - 1, int(abs(rng.randn()) * 2.2))
                    b[y, x, :3] = hair_cols[pick]
    for y in range(head_end + 1, int(sh * 0.225)):
        for x in range(sw):
            if b[y, x, 3]:
                r, g, bl = (int(v) for v in b[y, x, :3])
                if r > 150 and g > 90 and bl > 50 and r > bl + 40:
                    b[y, x, :3] = hair_cols[0]
    px0, px1 = int(sw * 0.50), int(sw * 0.72)
    py0, py1 = int(sh * 0.30), int(sh * 0.42)
    for y in range(py0, py1):
        for x in range(px0, px1):
            if b[y, x, 3]:
                lum = sum(int(v) for v in b[y, x, :3])
                if lum > sum(shirt_ref) + 60 or lum < sum(shirt_ref) - 90 or int(b[y, x, 0]) > int(b[y, x, 2]) + 50:
                    b[y, x, :3] = shirt_ref
    return b


def split_legs(img, left_up=0, right_up=0, left_dx=0, right_dx=0):
    out = img.copy()
    top = leg_top
    for side, up, dx in (("l", left_up, left_dx), ("r", right_up, right_dx)):
        if up == 0 and dx == 0:
            continue
        xs_ = range(0, split) if side == "l" else range(split, sw)
        for x in xs_:
            for y in range(top, sh):
                out[y, x] = 0
        for x in xs_:
            for y in range(top, sh):
                if img[y, x, 3] == 0:
                    continue
                shift_dx = int(round(dx * (y - top) / max(1, sh - top)))
                ny, nx = y - up, x + shift_dx
                if 0 <= nx < sw and 0 <= ny < sh:
                    out[ny, nx] = img[y, x]
    return out


def squeeze(img, factor):
    nw = max(8, int(round(sw * factor)))
    xs_ = (np.arange(nw) / factor).astype(int).clip(0, sw - 1)
    return img[:, xs_], nw


def frame(img, dx=0, dy=0, w=None):
    c = canvas()
    w = w or sw
    ox = (FW - w) // 2 + dx
    oy = FH - sh - 2 + dy
    paste(c, img, ox, oy)
    return c


def torso_shift(img, dx):
    if dx == 0:
        return img
    out = img.copy()
    for y in range(0, leg_top):
        row = img[y].copy()
        out[y] = 0
        if dx > 0:
            out[y, dx:] = row[: sw - dx]
        else:
            out[y, : sw + dx] = row[-dx:]
    return out


def walk_frames(base, side=None):
    frames = []
    seq = [
        dict(l=6, r=0, bob=-2, sway=1),
        dict(l=0, r=0, bob=0, sway=0),
        dict(l=0, r=6, bob=-2, sway=-1),
        dict(l=0, r=0, bob=0, sway=0),
    ]
    for s in seq:
        if side is None:
            im = split_legs(base, left_up=s["l"], right_up=s["r"])
            im = torso_shift(im, s["sway"])
            frames.append(frame(im, dy=s["bob"]))
        else:
            sq, nw = squeeze(base, 0.78)
            global_sw = sw
            scis = 3 if (s["l"] or s["r"]) else 0
            fl = 1 if s["l"] else (-1 if s["r"] else 0)
            c = canvas()
            im = base.copy()
            if scis:
                im = split_legs(base, left_up=s["l"], right_up=s["r"], left_dx=-fl * 3 * side, right_dx=fl * 0)
            sq2, nw2 = squeeze(im, 0.78)
            lean = side
            c = frame(sq2, dx=lean * (1 if (s["l"] or s["r"]) else 0), dy=s["bob"], w=nw2)
            frames.append(c)
    return frames


front = spr
back = make_back(spr)
rows = [
    walk_frames(front),
    walk_frames(front, side=-1),
    walk_frames(front, side=1),
    walk_frames(back),
]
sheet = Image.new("RGBA", (FW * 4, FH * 4), (0, 0, 0, 0))
for r, fr in enumerate(rows):
    for i, f in enumerate(fr):
        sheet.paste(Image.fromarray(f, "RGBA"), (i * FW, r * FH))
sheet.save(f"{OUT_DIR}/aditya_walk.png")

crop_b = src.crop((max(0, x0 - 6), y0 - 4, min(src.width, x1 + 7), y0 + int((y1 - y0) * 0.43)))
pw = 112
portrait = clean(crop_b, round(crop_b.height * pw / crop_b.width), colors=36)
Image.fromarray(np.array(Image.fromarray(portrait, "RGBA").resize((pw, round(crop_b.height * pw / crop_b.width)), Image.NEAREST)), "RGBA").save(f"{OUT_DIR}/aditya_portrait.png")
print("frame", FW, FH, "portrait", Image.open(f"{OUT_DIR}/aditya_portrait.png").size)
