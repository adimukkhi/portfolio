import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "@fontsource/pixelify-sans/400.css";
import "@fontsource/pixelify-sans/600.css";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);