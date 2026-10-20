import Phaser from "phaser";
import { ATLAS } from "./atlas.js";

export const WORLD = { width: 800, height: 540 };

const S = 2;
const ROOM = { left: 24, right: 776, top: 24, wallBottom: 184, bottom: 516 };
const DY = 32;
const FRAME = { w: 44, h: 104 };
const FEET = { halfW: 9, h: 7 };
const SPEED = 118;
const REACH = 96;

const DIRS = ["down", "left", "right", "up"];

export default class RoomScene extends Phaser.Scene {
  constructor(onOpenPanel, onHint) {
    super("RoomScene");
    this.onOpenPanel = onOpenPanel;
    this.onHint = onHint;
    this.objects = [];
    this.colliders = [];
    this.facing = "down";
    this.hovered = null;
  }

  preload() {
    this.load.image("beds", "/assets/room/beds_BR.png");
    this.load.image("wardrobes", "/assets/room/wardrobes_BR.png");
    this.load.image("decorations", "/assets/room/decorations_BR.png");
    this.load.image("props", "/assets/room/props_custom.png");
    this.load.image("floorTile", "/assets/room/floor_tile.png");
    this.load.image("wallTile", "/assets/room/wall_tile.png");
    this.load.spritesheet("aditya", "/assets/room/aditya_walk.png", { frameWidth: FRAME.w, frameHeight: FRAME.h });
  }

  create() {
    for (const key of ["beds", "wardrobes", "decorations", "props"]) {
      const tex = this.textures.get(key);
      tex.setFilter(Phaser.Textures.FilterMode.NEAREST);
      for (const [name, r] of Object.entries(ATLAS[key])) tex.add(name, 0, r[0], r[1], r[2], r[3]);
    }
    this.textures.get("aditya").setFilter(Phaser.Textures.FilterMode.NEAREST);

    this.buildShell();
    this.buildWall();
    this.buildFloor();
    this.createPlayer();
    this.createObjects();
    this.createMarker();
    this.bindInput();
    this.cameras.main.setBounds(0, 0, WORLD.width, WORLD.height);
  }

  img(key, frame, x, bottom, depth, opts = {}) {
    const scale = opts.scale ?? S;
    const im = this.add.image(x, bottom + DY, key, frame).setOrigin(0.5, 1).setScale(scale).setDepth((depth ?? bottom) + DY);
    if (opts.flip) im.setFlipX(true);
    return im;
  }

  prop(name, x, bottom, depth, opts) {
    return this.img("props", name, x, bottom, depth, opts);
  }

  blocker(x, y, w, h) {
    this.colliders.push(new Phaser.Geom.Rectangle(x, y + DY, w, h));
  }

  buildShell() {
    this.add.rectangle(WORLD.width / 2, WORLD.height / 2, WORLD.width, WORLD.height, 0x120d1c).setDepth(-10);
    const g = this.add.graphics().setDepth(900);
    g.lineStyle(4, 0x3b0900, 1).strokeRect(ROOM.left - 2, ROOM.top - 2, ROOM.right - ROOM.left + 4, ROOM.bottom - ROOM.top + 4);
    g.fillStyle(0x120d1c, 1);
    g.fillRect(0, 0, WORLD.width, ROOM.top - 3);
    g.fillRect(0, ROOM.bottom + 3, WORLD.width, WORLD.height - ROOM.bottom);
    g.fillRect(0, 0, ROOM.left - 3, WORLD.height);
    g.fillRect(ROOM.right + 3, 0, WORLD.width - ROOM.right, WORLD.height);
    const shade = this.add.graphics().setDepth(899);
    shade.fillStyle(0x000000, 0.1).fillRect(ROOM.left, ROOM.top, 10, ROOM.bottom - ROOM.top);
    shade.fillRect(ROOM.right - 10, ROOM.top, 10, ROOM.bottom - ROOM.top);
    shade.fillStyle(0x000000, 0.14).fillRect(ROOM.left, ROOM.bottom - 8, ROOM.right - ROOM.left, 8);
  }

  buildWall() {
    const w = ROOM.right - ROOM.left;
    const h = ROOM.wallBottom - ROOM.top;
    const wall = this.add.tileSprite(ROOM.left, ROOM.top, w, h, "wallTile").setOrigin(0, 0).setDepth(1);
    wall.setTileScale(S, S);
    const glow = this.add.graphics().setDepth(2);
    glow.fillStyle(0x000000, 0.18).fillRect(ROOM.left, ROOM.top, w, 6);
    glow.fillStyle(0x000000, 0.08).fillRect(ROOM.left, ROOM.top + 6, w, 6);
    const lights = ["lightsA", "lightsB", "lightsC"];
    for (let i = 0, x = ROOM.left + 52; x < ROOM.right; i++, x += 104) {
      this.add.image(x, ROOM.top + 30, "decorations", lights[i % 3]).setOrigin(0.5, 1).setScale(S).setDepth(3);
    }
  }

  buildFloor() {
    const w = ROOM.right - ROOM.left;
    const h = ROOM.bottom - ROOM.wallBottom;
    const floor = this.add.tileSprite(ROOM.left, ROOM.wallBottom, w, h, "floorTile").setOrigin(0, 0).setDepth(0);
    floor.setTileScale(S, S);
    const shade = this.add.graphics().setDepth(4);
    shade.fillStyle(0x1f1020, 0.22).fillRect(ROOM.left, ROOM.wallBottom, w, 8);
    shade.fillStyle(0x1f1020, 0.1).fillRect(ROOM.left, ROOM.wallBottom + 8, w, 8);

    this.img("decorations", "rugBlue", 470, 372, 10 - DY, { scale: S });
    this.img("decorations", "rugOval", 196, 300, 10 - DY, { scale: S });
  }

  createObjects() {
    const wallBase = 172;

    this.img("wardrobes", "wardrobeBrown", 92, wallBase, wallBase);
    this.blocker(44, 150, 96, 24);

    this.img("wardrobes", "dresserWhite", 202, wallBase, wallBase);
    this.prop("tv", 202, wallBase - 72, wallBase + 1);
    this.blocker(152, 148, 100, 26);

    this.prop("bookshelf", 314, wallBase, wallBase);
    this.prop("corkboard", 314, wallBase - 96, 6);
    this.blocker(266, 150, 96, 24);

    this.prop("desk", 450, 186, 186);
    this.prop("monitor", 436, 128, 187);
    this.prop("keyboard", 438, 140, 188);
    this.prop("mug", 506, 140, 188);
    this.img("decorations", "lampYellow", 400, 132, 188);
    this.prop("chair", 452, 218, 218);
    this.blocker(366, 150, 168, 38);

    this.prop("window", 600, 140, 5);
    this.prop("rod", 600, 36, 7);
    this.prop("curtain", 556, 150, 7);
    this.prop("curtain", 644, 150, 7, { flip: true });

    this.img("beds", "bedBlueSingle", 716, 192, 192);
    this.img("decorations", "clock", 716, 50, 6);
    this.blocker(680, 146, 72, 48);

    this.prop("plant", 62, 214, 214);
    this.blocker(46, 196, 32, 18);

    this.prop("console", 196, 322, 12 - DY);
    this.prop("pad", 246, 332, 13 - DY);

    this.img("wardrobes", "vanityWhite", 742, 446, 446);
    this.blocker(710, 410, 64, 36);

    this.img("wardrobes", "nightstandBrown", 652, wallBase, wallBase);
    this.img("decorations", "lampYellow", 652, wallBase - 36, wallBase + 1);
    this.blocker(636, 156, 34, 18);

    this.prop("backpack", 736, 252, 252);
    this.blocker(722, 240, 28, 12);


    this.addObject("projects", "Projects", { x: 450, y: 232, zone: [366, 52, 168, 136], mark: [436, 48] });
    this.addObject("skills", "Tech Stack", { x: 314, y: 214, zone: [264, 56, 100, 120], mark: [314, 40] });
    this.addObject("about", "About Me", { x: 716, y: 222, zone: [678, 70, 76, 124], mark: [716, 40] });
    this.addObject("contact", "Contact", { x: 202, y: 214, zone: [150, 54, 104, 120], mark: [202, 40] });

    this.cursorBlink = this.add.rectangle(450, 108 + DY, 4, 2, 0xafc5ee).setDepth(190 + DY);
    this.tweens.add({ targets: this.cursorBlink, alpha: 0, duration: 520, yoyo: true, repeat: -1 });
  }

  addObject(id, label, cfg) {
    const [zx, zy0, zw, zh] = cfg.zone;
    const zy = zy0 + DY;
    const zone = this.add.zone(zx + zw / 2, zy + zh / 2, zw, zh).setInteractive({ useHandCursor: true }).setDepth(950);
    zone.on("pointerover", () => {
      this.hovered = id;
      this.onHint(`Click or press E: ${label}`);
    });
    zone.on("pointerout", () => {
      if (this.hovered === id) this.hovered = null;
      this.onHint("");
    });
    zone.on("pointerdown", () => this.openObject({ id, label }));
    this.objects.push({ id, label, x: cfg.x, y: cfg.y + DY, mark: [cfg.mark[0], cfg.mark[1] + DY] });
  }

  createMarker() {
    this.bubble = this.add.sprite(0, 0, "props", "bubble0").setScale(S).setDepth(960).setVisible(false).setOrigin(0.5, 1);
    this.keycap = this.add.image(0, 0, "props", "keycap").setScale(S).setDepth(961).setVisible(false).setOrigin(0.5, 1);
    this.markerT = 0;
  }

  createPlayer() {
    for (const [row, dir] of DIRS.entries()) {
      this.anims.create({
        key: `walk-${dir}`,
        frames: [0, 1, 2, 3].map((i) => ({ key: "aditya", frame: row * 4 + i })),
        frameRate: 9,
        repeat: -1,
      });
    }
    this.shadow = this.add.ellipse(400, 380, 30, 9, 0x000000, 0.28).setDepth(329);
    this.player = this.add.sprite(400, 380, "aditya", 0).setOrigin(0.5, (FRAME.h - 2) / FRAME.h).setDepth(330);
    this.player.anims.play("walk-down");
    this.player.anims.stop();
    this.player.setFrame(0);
  }

  bindInput() {
    const K = Phaser.Input.Keyboard.KeyCodes;
    this.keys = this.input.keyboard.addKeys({
      UP: K.UP, DOWN: K.DOWN, LEFT: K.LEFT, RIGHT: K.RIGHT,
      W: K.W, A: K.A, S: K.S, D: K.D, E: K.E, SPACE: K.SPACE, ESC: K.ESC,
    });
    this.input.on("gameout", () => this.onHint(""));
  }

  openObject(obj) {
    if (this.registry.get("locked")) return;
    this.onOpenPanel(obj.id, obj.label);
  }

  blockedAt(x, y) {
    const box = new Phaser.Geom.Rectangle(x - FEET.halfW, y - FEET.h, FEET.halfW * 2, FEET.h);
    for (const c of this.colliders) if (Phaser.Geom.Intersects.RectangleToRectangle(box, c)) return true;
    return false;
  }

  nearest() {
    let best = null;
    for (const o of this.objects) {
      const d = Phaser.Math.Distance.Between(this.player.x, this.player.y, o.x, o.y);
      if (d < REACH && (!best || d < best.d)) best = { ...o, d };
    }
    return best;
  }

  update(time, delta) {
    const locked = this.registry.get("locked");
    const dt = delta / 1000;
    let vx = 0;
    let vy = 0;
    if (!locked) {
      if (this.keys.LEFT.isDown || this.keys.A.isDown) vx -= 1;
      if (this.keys.RIGHT.isDown || this.keys.D.isDown) vx += 1;
      if (this.keys.UP.isDown || this.keys.W.isDown) vy -= 1;
      if (this.keys.DOWN.isDown || this.keys.S.isDown) vy += 1;
    }
    const moving = vx !== 0 || vy !== 0;
    if (moving) {
      const len = Math.hypot(vx, vy);
      const nx = this.player.x + (vx / len) * SPEED * dt;
      const ny = this.player.y + (vy / len) * SPEED * dt;
      const minX = ROOM.left + 14;
      const maxX = ROOM.right - 14;
      const minY = ROOM.wallBottom + 10;
      const maxY = ROOM.bottom - 6;
      const tx = Phaser.Math.Clamp(nx, minX, maxX);
      if (!this.blockedAt(tx, this.player.y)) this.player.x = tx;
      const ty = Phaser.Math.Clamp(ny, minY, maxY);
      if (!this.blockedAt(this.player.x, ty)) this.player.y = ty;
      this.facing = vx !== 0 ? (vx < 0 ? "left" : "right") : vy < 0 ? "up" : "down";
      const key = `walk-${this.facing}`;
      if (this.player.anims.currentAnim?.key !== key || !this.player.anims.isPlaying) this.player.anims.play(key, true);
    } else if (this.player.anims.isPlaying) {
      this.player.anims.stop();
      this.player.setFrame(DIRS.indexOf(this.facing) * 4 + 1);
    }
    this.player.x = Math.round(this.player.x);
    this.player.y = Math.round(this.player.y);
    this.player.setDepth(this.player.y);
    this.shadow.setPosition(this.player.x, this.player.y - 1).setDepth(this.player.y - 1);

    const near = locked ? null : this.nearest();
    const target = this.objects.find((o) => o.id === this.hovered) || near;
    if (target && !locked) {
      this.markerT += delta;
      const bob = Math.round(Math.sin(this.markerT / 220) * 2);
      this.bubble.setVisible(true).setPosition(target.mark[0], target.mark[1] + bob);
      this.bubble.setFrame(Math.floor(this.markerT / 380) % 2 ? "bubble1" : "bubble0");
      if (near && near.id === target.id) {
        this.keycap.setVisible(true).setPosition(target.mark[0] + 34, target.mark[1] + bob + 2);
      } else this.keycap.setVisible(false);
    } else {
      this.bubble.setVisible(false);
      this.keycap.setVisible(false);
    }

    if (!locked && (Phaser.Input.Keyboard.JustDown(this.keys.E) || Phaser.Input.Keyboard.JustDown(this.keys.SPACE))) {
      if (near) this.openObject(near);
      else this.onHint("Walk up to something and press E.");
    }
    if (Phaser.Input.Keyboard.JustDown(this.keys.ESC)) this.onOpenPanel(null);
  }
}
