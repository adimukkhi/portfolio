import sys
import json
import random
import numpy as np
from PIL import Image
from scipy import ndimage

TEX = sys.argv[1]
OUT = sys.argv[2]


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4)) + (255,)


OUTL = hx("3b0900")
OUTL2 = hx("3e0e0e")
W1, W2, W3, W4, W5 = hx("a27e66"), hx("84654f"), hx("774d30"), hx("6a4d39"), hx("885f42")
C1, C2, C3, C4, C5 = hx("eaeaea"), hx("d1d1d1"), hx("c4c4c4"), hx("b0a79f"), hx("968f88")
CREAM, CREAM2, CREAM3 = hx("e6d9be"), hx("cdbea0"), hx("a39370")
N1, N2, N3, N4 = hx("475470"), hx("2a3650"), hx("1f293f"), hx("37445d")
GLASS, GLASS2 = hx("bcd2d5"), hx("dae8ea")
BLUE, BLUE2 = hx("639bff"), hx("afc5ee")
RED, RED2 = hx("b04029"), hx("c0533c")
YEL, YEL2, YEL3 = hx("c4b770"), hx("a69956"), hx("ead48b")
GRN, GRN2, GRN3 = hx("5f8a4e"), hx("7fae62"), hx("3f6a3a")
CLEAR = (0, 0, 0, 0)


class Spr:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def box(self, x, y, w, h, fill, outline=OUTL, hi=None, lo=None):
        self.rect(x, y, w, h, outline)
        self.rect(x + 1, y + 1, w - 2, h - 2, fill)
        if hi:
            self.rect(x + 1, y + 1, w - 2, 1, hi)
        if lo:
            self.rect(x + 1, y + h - 2, w - 2, 1, lo)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def img(self):
        return Image.fromarray(self.a, "RGBA")


def desk():
    s = Spr(84, 38)
    s.box(0, 0, 84, 8, W1, OUTL, hi=hx("b8957c"), lo=W2)
    s.rect(1, 6, 82, 1, W2)
    s.rect(2, 8, 80, 3, W4)
    s.rect(2, 8, 80, 1, OUTL)
    s.box(3, 10, 26, 27, W2, OUTL, hi=W5)
    for i in range(3):
        y = 12 + i * 8
        s.box(5, y, 22, 7, W5, OUTL2, hi=W1, lo=W3)
        s.rect(14, y + 3, 4, 2, OUTL)
    s.box(74, 10, 7, 27, W2, OUTL, hi=W5)
    s.rect(75, 11, 1, 25, W5)
    s.rect(30, 11, 44, 2, hx("523a2c"))
    return s


def chair():
    s = Spr(24, 30)
    s.box(4, 0, 16, 14, N1, OUTL, hi=hx("5d6c8a"), lo=N4)
    s.rect(6, 3, 12, 6, hx("52617f"))
    s.rect(11, 14, 2, 8, OUTL)
    s.rect(12, 14, 1, 8, C5)
    s.box(1, 22, 22, 3, C3, OUTL)
    s.box(2, 25, 4, 4, C5, OUTL)
    s.box(18, 25, 4, 4, C5, OUTL)
    s.box(10, 25, 4, 4, C5, OUTL)
    return s


def monitor():
    s = Spr(42, 38)
    s.box(0, 0, 42, 30, C2, OUTL, hi=C1, lo=C4)
    s.box(3, 3, 36, 22, N2, OUTL2)
    s.rect(4, 4, 34, 20, N2)
    lines = [(5, 5, 9, BLUE), (16, 5, 6, BLUE2), (5, 9, 14, CREAM2), (22, 9, 8, RED2), (7, 13, 10, BLUE2),
             (19, 13, 12, YEL3), (7, 17, 6, GRN2), (15, 17, 15, CREAM2), (5, 21, 4, BLUE)]
    for x, y, w, c in lines:
        s.hline(x, y, w, c)
    s.rect(3, 3, 36, 1, hx("3c4a6b"))
    s.rect(34, 26, 2, 2, GRN2)
    s.rect(15, 30, 12, 5, C3)
    s.rect(15, 30, 12, 1, OUTL)
    s.rect(15, 30, 1, 5, OUTL)
    s.rect(26, 30, 1, 5, OUTL)
    s.box(9, 34, 24, 4, C4, OUTL, hi=C3)
    return s


def keyboard():
    s = Spr(26, 7)
    s.box(0, 0, 26, 7, C2, OUTL, hi=C1)
    for y in (2, 4):
        for x in range(2, 24, 3):
            s.rect(x, y, 2, 1, C5)
    s.rect(8, 5, 10, 1, C5)
    return s


def mug():
    s = Spr(9, 9)
    s.box(0, 1, 7, 8, CREAM, OUTL, hi=C1, lo=CREAM3)
    s.rect(1, 2, 5, 1, hx("6a3a1a"))
    s.box(6, 3, 3, 4, CREAM, OUTL)
    s.rect(7, 4, 1, 2, CLEAR)
    s.px(2, 0, C2)
    s.px(4, 0, C2)
    return s


def tower():
    s = Spr(16, 34)
    s.box(0, 0, 16, 34, C3, OUTL, hi=C1, lo=C4)
    s.box(2, 3, 12, 3, C5, OUTL)
    s.box(2, 8, 12, 3, C5, OUTL)
    s.rect(3, 4, 6, 1, OUTL)
    s.rect(3, 9, 6, 1, OUTL)
    s.box(2, 14, 12, 14, C4, OUTL)
    for y in range(16, 27, 2):
        s.rect(4, y, 8, 1, C5)
    s.rect(11, 30, 2, 2, GRN2)
    s.rect(4, 30, 3, 2, OUTL)
    return s


def tv():
    s = Spr(40, 36)
    s.box(0, 0, 40, 33, CREAM, OUTL, hi=C1, lo=CREAM3)
    s.box(3, 3, 27, 26, hx("23304a"), OUTL)
    s.rect(4, 4, 25, 24, hx("7fb7ff"))
    s.rect(4, 4, 25, 9, hx("a9d2ff"))
    s.rect(4, 22, 25, 6, GRN3)
    s.rect(4, 22, 25, 1, GRN2)
    s.rect(9, 17, 6, 5, RED2)
    s.rect(10, 15, 4, 2, hx("f2c9a0"))
    s.rect(18, 13, 7, 3, C1)
    s.rect(19, 12, 5, 1, C1)
    s.rect(4, 4, 25, 1, GLASS2)
    s.rect(4, 5, 2, 4, GLASS2)
    s.rect(33, 5, 4, 3, C5)
    s.rect(33, 11, 4, 3, C5)
    s.rect(33, 17, 4, 1, OUTL)
    s.rect(33, 19, 4, 1, OUTL)
    s.rect(33, 21, 4, 1, OUTL)
    s.rect(34, 25, 2, 2, RED2)
    s.rect(4, 33, 6, 3, OUTL)
    s.rect(30, 33, 6, 3, OUTL)
    return s


def console():
    s = Spr(24, 8)
    s.box(0, 0, 24, 8, C4, OUTL, hi=C2, lo=C5)
    s.rect(3, 3, 10, 1, OUTL)
    s.rect(3, 5, 10, 1, C5)
    s.rect(18, 3, 2, 2, GRN2)
    return s


def pad():
    s = Spr(16, 10)
    s.box(0, 1, 16, 8, C3, OUTL, hi=C1, lo=C4)
    s.rect(3, 4, 4, 1, OUTL)
    s.rect(4, 3, 1, 3, OUTL)
    s.rect(11, 3, 2, 2, RED2)
    s.rect(9, 5, 2, 2, BLUE)
    return s


def bookshelf():
    s = Spr(48, 62)
    s.box(0, 0, 48, 62, W2, OUTL, hi=W1, lo=W3)
    s.rect(1, 1, 46, 3, W1)
    s.rect(1, 3, 46, 1, W5)
    palette = [RED, YEL, BLUE, hx("8bacc4"), RED2, CREAM2, GRN, hx("7f728e")]
    rnd = random.Random(7)
    for i, y in enumerate((6, 24, 42)):
        s.rect(3, y, 42, 14, hx("4a2a18"))
        s.rect(3, y + 14, 42, 3, W5)
        s.rect(3, y + 14, 42, 1, OUTL)
        x = 4
        while x < 42:
            w = rnd.choice([3, 4, 4, 5])
            h = rnd.choice([9, 10, 11, 12, 13])
            if x + w > 44:
                break
            c = rnd.choice(palette)
            s.rect(x, y + 14 - h, w, h, c)
            s.rect(x, y + 14 - h, w, 1, OUTL)
            s.rect(x, y + 14 - h, 1, h, OUTL)
            s.rect(x + 1, y + 16 - h, 1, h - 3, tuple(min(255, v + 30) for v in c[:3]) + (255,))
            x += w + (1 if rnd.random() > 0.35 else 4)
        if i == 1:
            s.box(33, y + 3, 9, 11, GLASS, OUTL, hi=GLASS2)
    s.rect(4, 58, 40, 2, W4)
    s.box(2, 59, 5, 3, W3, OUTL)
    s.box(41, 59, 5, 3, W3, OUTL)
    return s


def plant():
    s = Spr(24, 36)
    for pts in [(11, 3, 3, 16), (5, 9, 4, 10), (15, 7, 4, 12)]:
        s.rect(pts[0], pts[1], pts[2], pts[3], GRN3)
    for (x, y, w, h) in [(2, 8, 8, 8), (12, 4, 9, 8), (8, 0, 8, 8), (1, 15, 9, 6), (14, 14, 9, 6), (6, 9, 9, 8)]:
        s.box(x, y, w, h, GRN, hx("1f3a22"), hi=GRN2)
    s.box(4, 20, 16, 15, RED, OUTL, hi=RED2)
    s.rect(3, 20, 18, 3, RED2)
    s.rect(3, 20, 18, 1, OUTL)
    s.rect(4, 23, 16, 1, OUTL)
    s.rect(6, 26, 2, 7, hx("8a2f1d"))
    return s


def backpack():
    s = Spr(22, 26)
    s.box(2, 4, 18, 21, hx("3f6a8a"), OUTL, hi=hx("5a8fb2"), lo=hx("2f526b"))
    s.box(6, 0, 10, 6, hx("3f6a8a"), OUTL)
    s.rect(9, 2, 4, 2, OUTL)
    s.box(5, 14, 12, 8, hx("5a8fb2"), OUTL, hi=hx("7aa9c8"))
    s.rect(9, 17, 4, 1, OUTL)
    s.rect(4, 8, 14, 1, hx("2f526b"))
    s.box(0, 10, 3, 10, hx("2f526b"), OUTL)
    s.box(19, 10, 3, 10, hx("2f526b"), OUTL)
    return s


def corkboard():
    s = Spr(52, 38)
    s.box(0, 0, 52, 38, W3, OUTL, hi=W1)
    s.rect(2, 2, 48, 34, hx("b48a62"))
    rnd = random.Random(3)
    for _ in range(46):
        s.px(rnd.randint(3, 48), rnd.randint(3, 34), rnd.choice([hx("a07a55"), hx("c79c74")]))
    notes = [(5, 5, 11, 10, YEL3), (19, 4, 10, 11, hx("f1b8c8")), (33, 6, 12, 10, BLUE2), (6, 19, 12, 11, hx("bfe3b5")),
             (22, 19, 10, 10, CREAM), (35, 20, 11, 11, hx("f6c28a"))]
    for x, y, w, h, c in notes:
        s.rect(x + 1, y + 1, w, h, hx("7a5a40"))
        s.rect(x, y, w, h, c)
        for i in range(2, h - 2, 3):
            s.hline(x + 2, y + i, w - 4 - (i % 2) * 2, hx("6a6a7a"))
        s.rect(x + w // 2 - 1, y - 1, 2, 2, RED)
    return s


def window():
    s = Spr(52, 56)
    s.box(0, 0, 52, 56, CREAM, OUTL, hi=C1, lo=CREAM3)
    for r in range(2):
        for c in range(2):
            x, y = 4 + c * 22, 4 + r * 24
            s.box(x, y, 20, 22, hx("8bacc4"), OUTL2)
            s.rect(x + 1, y + 1, 18, 8, hx("a9cbe0"))
            s.rect(x + 1, y + 13, 18, 8, hx("b5d8c0") if r == 1 else hx("a0c3d8"))
            s.rect(x + 3, y + 3, 7, 3, C1)
            s.rect(x + 5, y + 2, 6, 1, C1)
            s.rect(x + 2, y + 2, 1, 7, GLASS2)
    s.rect(24, 4, 4, 46, CREAM)
    s.rect(4, 26, 44, 4, CREAM)
    s.rect(24, 4, 1, 46, OUTL)
    s.rect(27, 4, 1, 46, OUTL)
    s.box(-2 if False else 0, 52, 52, 4, W2, OUTL, hi=W1)
    return s


def curtain(flip=False):
    s = Spr(14, 62)
    s.box(0, 0, 14, 60, RED, OUTL, hi=RED2)
    for x in (3, 7, 11):
        s.vline(x, 2, 56, hx("8a2f1d"))
    for x in (4, 8):
        s.vline(x, 2, 56, RED2)
    s.rect(0, 22, 14, 3, hx("e0b45a"))
    s.rect(0, 22, 14, 1, OUTL)
    s.rect(0, 24, 14, 1, OUTL)
    return s


def rod():
    s = Spr(76, 6)
    s.rect(2, 1, 72, 3, W3)
    s.rect(2, 1, 72, 1, OUTL)
    s.rect(2, 3, 72, 1, OUTL)
    s.box(0, 0, 5, 6, YEL3, OUTL)
    s.box(71, 0, 5, 6, YEL3, OUTL)
    return s


def bubble():
    frames = []
    for f in range(2):
        s = Spr(20, 18)
        s.box(0, 0, 20, 14, C1, OUTL, lo=C3)
        s.rect(7, 14, 4, 2, OUTL)
        s.rect(8, 13, 2, 3, C1)
        s.rect(8, 16, 2, 1, OUTL)
        for i in range(3):
            y = 5 + (1 if f == 1 and i == 1 else 0) - (1 if f == 1 and i != 1 else 0)
            s.rect(4 + i * 5, y, 3, 3, OUTL)
        frames.append(s)
    return frames


def keycap():
    s = Spr(14, 15)
    s.box(0, 0, 14, 13, C2, OUTL, hi=C1)
    s.rect(1, 11, 12, 2, C5)
    s.rect(0, 12, 14, 1, OUTL)
    for y, w in ((3, 6), (5, 4), (7, 6)):
        s.hline(4, y, w, OUTL)
    s.vline(4, 3, 5, OUTL)
    return s


def cat():
    s = Spr(24, 16)
    o = hx("c6783a")
    o2 = hx("e6a36a")
    s.box(2, 4, 20, 11, o, OUTL, hi=o2)
    s.box(0, 6, 5, 8, o, OUTL)
    s.box(15, 0, 8, 8, o, OUTL, hi=o2)
    s.rect(15, 0, 2, 2, OUTL)
    s.rect(21, 0, 2, 2, OUTL)
    s.rect(17, 3, 4, 1, OUTL2)
    s.rect(6, 7, 1, 7, hx("a85b2a"))
    s.rect(10, 7, 1, 7, hx("a85b2a"))
    s.rect(14, 7, 1, 5, hx("a85b2a"))
    return s


def floor_tile():
    w, h = 64, 32
    s = Spr(w, h)
    base = [hx("c9b698"), hx("c2af90"), hx("ccba9d"), hx("c6b394")]
    rnd = random.Random(11)
    offs = [0, 22, 41, 11]
    for r in range(4):
        y = r * 8
        s.rect(0, y, w, 8, base[r])
        s.rect(0, y, w, 1, hx("d6c6aa"))
        s.rect(0, y + 7, w, 1, hx("a89573"))
        x = offs[r]
        for sx in (x, (x + 32) % w):
            s.vline(sx, y, 8, hx("a89573"))
            s.vline((sx + 1) % w, y + 1, 7, hx("d6c6aa"))
        for _ in range(7):
            gx, gy = rnd.randint(0, w - 4), y + rnd.randint(2, 5)
            s.hline(gx, gy, rnd.randint(2, 4), hx("b8a584"))
    return s


def wall_tile():
    w, h = 32, 80
    off = 16
    s = Spr(w, h)
    for x in range(w):
        col = N2 if (x // 8) % 2 == 0 else hx("2e3a56")
        s.vline(x, 0, 42 + off, col)
    for x in range(0, w, 8):
        s.vline(x, 0, 42 + off, hx("26314a"))
    s.rect(0, 38 + off, w, 2, hx("1f293f"))
    s.rect(0, 40 + off, w, 1, CREAM2)
    s.rect(0, 41 + off, w, 2, CREAM)
    s.rect(0, 43 + off, w, 1, CREAM3)
    s.rect(0, 44 + off, w, 1, OUTL)
    s.rect(0, 45 + off, w, 13, N4)
    for x in (0, 15):
        s.box(x + 2, 47 + off, 12, 9, hx("3d4a68"), N3, hi=hx("4a5879"))
    s.rect(0, 58 + off, w, 1, OUTL)
    s.rect(0, 59 + off, w, 4, hx("594038"))
    s.rect(0, 59 + off, w, 1, hx("7a5a4a"))
    s.rect(0, 63 + off, w, 1, OUTL)
    return s


def bookshelf():
    s = Spr(48, 46)
    s.box(0, 0, 48, 46, W2, OUTL, hi=W1, lo=W3)
    s.rect(1, 1, 46, 3, W1)
    s.rect(1, 3, 46, 1, W5)
    palette = [RED, YEL, BLUE, hx("8bacc4"), RED2, CREAM2, GRN, hx("7f728e")]
    rnd = random.Random(7)
    for i, y in enumerate((5, 22)):
        s.rect(3, y, 42, 13, hx("4a2a18"))
        s.rect(3, y + 13, 42, 3, W5)
        s.rect(3, y + 13, 42, 1, OUTL)
        x = 4
        while x < 40:
            w = rnd.choice([3, 4, 4, 5])
            h = rnd.choice([8, 9, 10, 11, 12])
            if x + w > 41:
                break
            c = rnd.choice(palette)
            s.rect(x, y + 13 - h, w, h, c)
            s.rect(x, y + 13 - h, w, 1, OUTL)
            s.rect(x, y + 13 - h, 1, h, OUTL)
            s.rect(x + 1, y + 15 - h, 1, max(1, h - 3), tuple(min(255, v + 30) for v in c[:3]) + (255,))
            x += w + (1 if rnd.random() > 0.35 else 3)
        if i == 0:
            s.box(35, y + 3, 8, 10, GLASS, OUTL, hi=GLASS2)
    s.box(2, 42, 5, 4, W3, OUTL)
    s.box(41, 42, 5, 4, W3, OUTL)
    return s


def corkboard():
    s = Spr(46, 30)
    s.box(0, 0, 46, 30, W3, OUTL, hi=W1)
    s.rect(2, 2, 42, 26, hx("b48a62"))
    rnd = random.Random(3)
    for _ in range(34):
        s.px(rnd.randint(3, 42), rnd.randint(3, 26), rnd.choice([hx("a07a55"), hx("c79c74")]))
    notes = [(4, 4, 9, 9, YEL3), (16, 3, 9, 10, hx("f1b8c8")), (28, 5, 10, 9, BLUE2), (6, 16, 10, 9, hx("bfe3b5")),
             (20, 16, 9, 9, CREAM), (32, 16, 10, 9, hx("f6c28a"))]
    for x, y, w, h, c in notes:
        s.rect(x + 1, y + 1, w, h, hx("7a5a40"))
        s.rect(x, y, w, h, c)
        for i in range(2, h - 2, 3):
            s.hline(x + 2, y + i, w - 4 - (i % 2) * 2, hx("6a6a7a"))
        s.rect(x + w // 2 - 1, y - 1, 2, 2, RED)
    return s


def trim_rect(sheet_arr, x, y, w, h):
    sub = sheet_arr[y : y + h, x : x + w, 3] > 0
    ys, xs = np.where(sub)
    return [int(x + xs.min()), int(y + ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


beds = np.array(Image.open(f"{TEX}/beds_BR.png").convert("RGBA"))
wards = np.array(Image.open(f"{TEX}/wardrobes_BR.png").convert("RGBA"))
decos = np.array(Image.open(f"{TEX}/decorations_BR.png").convert("RGBA"))

atlas = {"beds": {}, "wardrobes": {}, "decorations": {}, "props": {}}
for name, rect in {
    "bedRedSingle": (14, 22, 36, 60), "bedRedDouble": (62, 22, 52, 60),
    "bedWhiteSingle": (126, 22, 36, 60), "bedWhiteDouble": (174, 22, 52, 60),
    "bedGreenSingle": (14, 102, 36, 60), "bedGreenDouble": (62, 102, 52, 60),
    "bedBlueSingle": (14, 182, 36, 60), "bedBlueDouble": (62, 182, 52, 60),
}.items():
    atlas["beds"][name] = trim_rect(beds, *rect)
for name, rect in {
    "wardrobeBrown": (14, 30, 52, 68), "wardrobeBrownOpen": (78, 30, 68, 70),
    "wardrobeTan": (14, 110, 52, 68), "wardrobeWhite": (14, 190, 52, 68), "wardrobeWhiteOpen": (78, 190, 68, 70),
    "dresserBrown": (206, 22, 52, 44), "dresserBrownDrawers": (206, 70, 52, 44),
    "dresserTan": (206, 118, 52, 44), "dresserWhite": (206, 214, 52, 44), "dresserWhiteKnobs": (206, 262, 52, 44),
    "nightstandBrown": (158, 18, 19, 24), "stoolA": (72, 272, 16, 14), "stoolB": (104, 272, 16, 14), "stoolC": (88, 288, 16, 14), "nightstandWhite": (158, 210, 36, 24),
    "benchWhite": (22, 278, 36, 20),
    "vanityBrown": (14, 302, 36, 48), "vanityWhite": (110, 302, 36, 48),
}.items():
    atlas["wardrobes"][name] = trim_rect(wards, *rect)
for name, rect in {
    "frameSunset": (130, 17, 44, 30), "clock": (97, 28, 14, 14),
    "lampWhite": (96, 51, 15, 23), "lampYellow": (112, 51, 15, 23), "lampSmall": (129, 53, 14, 21), "sconce": (144, 53, 16, 21),
    "lightsA": (94, 78, 52, 10), "lightsB": (94, 88, 52, 10), "lightsC": (94, 97, 52, 10),
    "mirrorGold": (144, 79, 16, 34), "mirrorSilver": (160, 79, 17, 34),
    "rugOval": (15, 126, 66, 52), "rugBlue": (92, 126, 72, 52),
}.items():
    atlas["decorations"][name] = trim_rect(decos, *rect)

sprites = {
    "desk": desk(), "chair": chair(), "monitor": monitor(), "keyboard": keyboard(), "mug": mug(), "tower": tower(),
    "tv": tv(), "console": console(), "pad": pad(), "bookshelf": bookshelf(), "plant": plant(), "backpack": backpack(),
    "corkboard": corkboard(), "window": window(), "curtain": curtain(), "rod": rod(), "keycap": keycap(), "cat": cat(),
    "floor": floor_tile(), "wall": wall_tile(),
}
b = bubble()
sprites["bubble0"], sprites["bubble1"] = b

x = y = 0
rowh = 0
W = 256
placed = []
for name, sp in sprites.items():
    if x + sp.w + 1 > W:
        x = 0
        y += rowh + 1
        rowh = 0
    placed.append((name, sp, x, y))
    atlas["props"][name] = [x, y, sp.w, sp.h]
    x += sp.w + 1
    rowh = max(rowh, sp.h)
H = y + rowh
sheet = Image.new("RGBA", (W, H), CLEAR)
for name, sp, px, py in placed:
    sheet.paste(sp.img(), (px, py))
sheet.save(f"{OUT}/props_custom.png")
sprites["floor"].img().save(f"{OUT}/floor_tile.png")
sprites["wall"].img().save(f"{OUT}/wall_tile.png")
with open(f"{OUT}/../../../src/game/atlas.js", "w") as f:
    f.write("export const ATLAS = " + json.dumps(atlas, indent=2) + ";\n")
print("sheet", W, H)
