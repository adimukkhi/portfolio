import { useEffect, useRef } from "react";
import Phaser from "phaser";
import RoomScene, { WORLD } from "./RoomScene.js";

export default function GameCanvas({ onOpenPanel, onHint, locked }) {
  const hostRef = useRef(null);
  const gameRef = useRef(null);
  const callbacksRef = useRef({ onOpenPanel, onHint });
  callbacksRef.current = { onOpenPanel, onHint };

  useEffect(() => {
    if (!hostRef.current) return;
    const scene = new RoomScene(
      (id, label) => callbacksRef.current.onOpenPanel(id, label),
      (hint) => callbacksRef.current.onHint(hint)
    );
    const game = new Phaser.Game({
      type: Phaser.AUTO,
      parent: hostRef.current,
      width: WORLD.width,
      height: WORLD.height,
      backgroundColor: "#120d1c",
      pixelArt: true,
      roundPixels: true,
      antialias: false,
      scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
      scene: [scene],
    });
    game.registry.set("locked", false);
    gameRef.current = game;
    return () => {
      gameRef.current = null;
      game.destroy(true);
    };
  }, []);

  useEffect(() => {
    gameRef.current?.registry.set("locked", !!locked);
  }, [locked]);

  return <div className="game-canvas" ref={hostRef} aria-label="Interactive pixel-art portfolio room" />;
}
