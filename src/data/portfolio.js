// Replace the placeholder name, email, and profile URLs before publishing.
export const portfolio = {
  name: "Aditya Mukherjee",
  role: "Computer Science Engineering Student | Full-Stack Developer",
  intro: "Computer Science Engineering student at VIT Vellore with hands-on experience building and deploying full-stack applications across the MERN and Flask stacks. Skilled in Python, JavaScript, React, Node.js, Express.js, MongoDB, and generative AI integration, with experience designing RESTful APIs and secure backend systems. Placed in the Top 10 at IEEE Computer Society HackBattle.",
  education: [
    { degree: "B.Tech in Computer Science Engineering", school: "Vellore Institute of Technology (VIT), Vellore, Tamil Nadu", dates: "Jul 2026 – Jun 2030" },
    { degree: "High School Diploma in PCM", school: "The Khaitan School, Noida, Uttar Pradesh", dates: "Apr 2024 – May 2026", detail: "GPA: 90.2%" }
  ],
  projects: [
    {
      title: "AdiFlash",
      subtitle: "AI-Powered Multimodal Flashcard Generator",
      description: "Developed and deployed a full-stack learning application that converts text, PowerPoint presentations, and audio/video recordings into interactive 3D flashcards. Integrated the Google GenAI SDK with structured JSON outputs for AI-powered content classification and flashcard generation, and used the Google Files API and python-pptx for multimodal content extraction. Implemented persistent flashcard storage and session management using Flask-SQLAlchemy and SQLite, deploying the application on Railway.",
      stack: ["Python", "Flask", "Gemini API", "SQLite", "Google Files API", "python-pptx"],
      demo: "", source: "https://github.com/adimukkhi/flashcards"
    },
    {
      title: "FolkSocial",
      subtitle: "Secure Social Media Micro-Platform",
      description: "Built a full-stack social platform with session-based authentication using Flask-Login and password hashing using Flask-Bcrypt. Designed relational data models with cascading deletion rules and implemented asynchronous interactions using JavaScript Fetch API to update UI states without full-page reloads.",
      stack: ["Python", "Flask", "SQLite", "SQLAlchemy", "ES6 JavaScript"],
      demo: "", source: "https://github.com/adimukkhi/folk-social"
    },
    {
      title: "FolkNotes",
      subtitle: "Full-Stack Notes Management Application",
      description: "Developed and deployed a MERN-stack notes application with RESTful CRUD APIs, MongoDB persistence, dynamic search, favourites, and timestamp-based sorting. Implemented responsive grid/list views, persistent DaisyUI theme customization with 31 themes, colour-coded notes, and Upstash Redis-backed API rate limiting.",
      stack: ["React", "Node.js", "Express.js", "MongoDB", "Redis", "Tailwind CSS", "DaisyUI"],
      demo: "https://folknotes.onrender.com/", source: "https://github.com/adimukkhi/folknotes"
    }
  ],
  skills: {
    "Programming Languages": ["Python", "JavaScript (ES6)", "C++", "C", "SQL"],
    "Frontend Development": ["React", "HTML5", "CSS3", "Tailwind CSS", "DaisyUI", "Jinja2"],
    "Backend Development": ["Node.js", "Express.js", "Flask", "REST APIs", "CRUD Systems"],
    "Databases & ORM": ["MongoDB", "Mongoose", "SQLite", "Flask-SQLAlchemy"],
    "AI & API Integration": ["Google Gemini API", "Google GenAI SDK", "Axios", "Fetch API"],
    "Tools & Deployment": ["Git", "GitHub", "Vite", "Railway", "Vercel","Upstash Redis"]
  },
  highlights: [
    "Top 10 at IEEE Computer Society HackBattle",
    "Built and deployed applications across MERN and Flask",
    "Experience with secure authentication, REST APIs, and generative AI"
  ],
  contact: {
    email: "aditya.mukherjee2019@gmail.com",
    github: "https://github.com/adimukkhi",
    linkedin: "https://www.linkedin.com/in/aditya-mukherjee-568067359/"
  }
};