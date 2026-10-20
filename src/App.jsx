import { useEffect, useRef, useState } from "react";
import GameCanvas from "./game/GameCanvas.jsx";
import { portfolio } from "./data/portfolio.js";

const OBJECTS = {
  projects: { title: "Projects", prompt: "You selected my PC! Want to check out the projects I've built?" },
  skills: { title: "Tech Stack", prompt: "You found my notes and bookshelf! Want to see the languages, frameworks and tools I work with?" },
  about: { title: "About Me & Education", prompt: "That's my bed! Want to read a bit about me, my education and my achievements?" },
  contact: { title: "Contact", prompt: "You found my TV corner! Want to see how to get in touch with me?" },
};

const INTRO = [
  "Hi, I'm Aditya, and welcome to my portfolio! Instead of a plain page, I turned it into a little game. This is my room, so come on in and look around.",
  "Use the ARROW KEYS to walk around. When you get close to something, a speech bubble pops up. Press E to interact with it, or just click it with your mouse.",
  "Here's what everything does: my PC shows my projects, the bookshelf and pinned notes show my tech stack, my bed tells you about me and my education, and the TV has my contact details.",
];

function useTypewriter(text, speed = 22) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    setCount(0);
    if (!text) return undefined;
    const id = setInterval(() => {
      setCount((c) => {
        if (c >= text.length) {
          clearInterval(id);
          return c;
        }
        return c + 1;
      });
    }, speed);
    return () => clearInterval(id);
  }, [text, speed]);
  return [text.slice(0, count), () => setCount(text.length), count >= text.length];
}

function Dialogue({ text, name, buttons }) {
  const [shown, skip, done] = useTypewriter(text);
  return <section className="dlg" aria-live="polite" role="dialog" aria-label={`${name} says`}>
    <div className="dlg-portrait" aria-hidden="true">
      <span className="dlg-tri" />
      <img src="/assets/room/aditya_portrait.png" alt="" />
    </div>
    <div className="dlg-body">
      <div className="dlg-name">{name}</div>
      <p className="dlg-text" onClick={skip}>{shown}{!done && <span className="dlg-caret" />}</p>
      <div className="dlg-actions">
        {buttons.map((b) => <button key={b.label} className={`dlg-btn ${b.primary ? "dlg-open" : "dlg-cancel"}`} onClick={b.onClick}>{b.label}</button>)}
      </div>
    </div>
  </section>;
}

function PanelContent({ id }) {
  if (id === "projects") return <div className="project-list">{portfolio.projects.map((project) => (
    <article className="project-card" key={project.title}>
      <p className="project-subtitle">{project.subtitle}</p>
      <h3>{project.title}</h3>
      <p>{project.description}</p>
      <div className="chips">{project.stack.map((s) => <span key={s}>{s}</span>)}</div>
      <div className="links">
        {project.demo && <a href={project.demo} target="_blank" rel="noreferrer">Live demo ↗</a>}
        {project.source && <a href={project.source} target="_blank" rel="noreferrer">GitHub ↗</a>}
      </div>
    </article>
  ))}</div>;
  if (id === "skills") return <div className="skill-groups">{Object.entries(portfolio.skills).map(([group, skills]) => (
    <section key={group}><h3>{group}</h3><div className="chips">{skills.map((skill) => <span key={skill}>{skill}</span>)}</div></section>
  ))}</div>;
  if (id === "about") return <div>
    <p className="role-line">{portfolio.role}</p><p>{portfolio.intro}</p>
    <h3 className="section-heading">Education</h3>
    <div className="education-list">{portfolio.education.map((item) => <article className="project-card" key={item.degree}>
      <p className="project-subtitle">{item.dates}</p><h3>{item.degree}</h3><p>{item.school}</p>
      {item.detail && <div className="chips"><span>{item.detail}</span></div>}
    </article>)}</div>
    <h3 className="section-heading">Achievements</h3>
    <div className="highlight-list">{portfolio.highlights.map((item) => <div key={item}>✦ {item}</div>)}</div>
  </div>;
  if (id === "contact") return <div className="contact-list">
    <a href={`mailto:${portfolio.contact.email}`}>✉ Email <span>{portfolio.contact.email}</span></a>
    <a href={portfolio.contact.github} target="_blank" rel="noreferrer">⌘ GitHub <span>Open profile ↗</span></a>
    <a href={portfolio.contact.linkedin} target="_blank" rel="noreferrer">▣ LinkedIn <span>Open profile ↗</span></a>
  </div>;
  return null;
}

export default function App() {
  const [pending, setPending] = useState(null);
  const [activePanel, setActivePanel] = useState(null);
  const [introPage, setIntroPage] = useState(0);
  const [hint, setHint] = useState("");
  const pendingRef = useRef(null);
  const introRef = useRef(0);
  pendingRef.current = pending;
  introRef.current = introPage;

  const nextIntro = () => setIntroPage((p) => (p === null ? null : p + 1 >= INTRO.length ? null : p + 1));
  const skipIntro = () => setIntroPage(null);

  useEffect(() => {
    const onKeyDown = (event) => {
      if (event.key === "Escape") {
        setIntroPage(null);
        setActivePanel(null);
        setPending(null);
      } else if (event.key === "Enter") {
        if (introRef.current !== null) {
          event.preventDefault();
          setIntroPage((p) => (p === null ? null : p + 1 >= INTRO.length ? null : p + 1));
        } else if (pendingRef.current) {
          event.preventDefault();
          setActivePanel(pendingRef.current);
          setPending(null);
        }
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const requestObject = (id) => {
    if (!id || !OBJECTS[id] || introRef.current !== null) return;
    setPending(id);
    setActivePanel(null);
  };

  const confirmObject = () => {
    if (!pending) return;
    setActivePanel(pending);
    setPending(null);
  };

  const isLastIntro = introPage === INTRO.length - 1;
  const introButtons = isLastIntro
    ? [{ label: "Let's go", primary: true, onClick: nextIntro }]
    : [{ label: "Next", primary: true, onClick: nextIntro }, { label: "Skip", onClick: skipIntro }];

  return <main className="game-only">
    <div className="game-world">
      <GameCanvas onOpenPanel={requestObject} onHint={setHint} locked={introPage !== null || !!pending || !!activePanel} />
      {introPage !== null && <Dialogue key={`intro-${introPage}`} name="Aditya" text={INTRO[introPage]} buttons={introButtons} />}
      {introPage === null && pending && <Dialogue
        key={pending}
        name="Aditya"
        text={OBJECTS[pending].prompt}
        buttons={[
          { label: "Open", primary: true, onClick: confirmObject },
          { label: "Cancel", onClick: () => setPending(null) },
        ]}
      />}
      {activePanel && <div className="panel-overlay" role="dialog" aria-modal="true" aria-label={OBJECTS[activePanel].title}>
        <section className="pixel-panel content-panel">
          <header className="panel-header">
            <div><p>INVENTORY / FILE OPENED</p><h2>{OBJECTS[activePanel].title}</h2></div>
            <button className="close-button" onClick={() => setActivePanel(null)} aria-label="Close panel">×</button>
          </header>
          <div className="panel-body"><PanelContent id={activePanel} /></div>
          <footer className="panel-footer"><span>PRESS ESC TO CLOSE</span></footer>
        </section>
      </div>}
    </div>

    <div className="controls-hint">{hint || "ARROW KEYS to walk  ·  E to interact  ·  or just click an object"}</div>
  </main>;
}