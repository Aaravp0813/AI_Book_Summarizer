# NCERT AI Tutor — Coding Instructions

## Role

You are working as the frontend engineer for a local React + Vite application called:

**NCERT AI Tutor**

The application is specifically designed to help students study the **NCERT Grade 8 Science textbook**.

Build the frontend directly in the existing Vite project.

---

## Critical Starting Assumptions

The frontend folder already exists.

However:

* `npm install` has NOT been run yet.
* Custom React components do NOT exist yet.
* Custom CSS does NOT exist yet.
* The API service does NOT exist yet.
* No code from another frontend implementation has been copied.
* Do not assume Claude-generated files exist.
* Do not assume custom files already exist.

First inspect the existing project before modifying it.

---

## Project Location

The project is currently under:

```text
E:\My_Projects\AI_Book_Summarizer\
```

The frontend is:

```text
E:\My_Projects\AI_Book_Summarizer\frontend\
```

Do not move the frontend.

---

## Technology

Use:

* React
* Vite
* JavaScript
* JSX
* CSS

Do not use:

* TypeScript
* Tailwind
* Bootstrap
* Material UI
* unnecessary third-party UI packages

Avoid adding dependencies unless they are genuinely required.

---

## Installation

Before implementation, ensure project dependencies are installed:

```bash
npm install
```

Do not reinstall Node.js.

Do not replace Vite unless there is an actual compatibility problem.

---

## Architecture

Use this target architecture:

```text
src/
├── components/
│   ├── Layout.jsx
│   ├── Layout.css
│   ├── Header.jsx
│   ├── Header.css
│   ├── TopicChips.jsx
│   ├── TopicChips.css
│   ├── QuestionInput.jsx
│   ├── QuestionInput.css
│   ├── AnswerPanel.jsx
│   └── AnswerPanel.css
│
├── pages/
│   ├── Home.jsx
│   └── Home.css
│
├── services/
│   └── api.js
│
├── styles/
│   └── global.css
│
├── App.jsx
└── main.jsx
```

---

## Component Rules

### Do not create one giant App.jsx

`App.jsx` should remain a thin root component.

### Keep state where it belongs

The Home page should manage:

* question
* answer
* loading
* error

Reusable components should receive props and callbacks.

### Keep networking out of UI components

Do not put `fetch()` directly into `QuestionInput.jsx`.

Networking belongs in:

```text
src/services/api.js
```

---

## API Contract

The backend is:

```text
http://127.0.0.1:8000
```

The question endpoint is:

```text
POST http://127.0.0.1:8000/ask
```

Request:

```json
{
  "question": "What is photosynthesis?"
}
```

Response:

```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is..."
}
```

Error example:

```json
{
  "detail": "FAISS database is not loaded."
}
```

The frontend should use the response's `answer` field.

---

## API Service Requirements

Create:

```text
src/services/api.js
```

It should export a function similar to:

```javascript
askQuestion(question)
```

Requirements:

* POST JSON
* `Content-Type: application/json`
* return parsed response JSON
* handle network failure
* handle non-2xx HTTP responses
* use backend `detail` when present

Do not include a Gemini API key.

Do not call Google APIs directly from React.

---

## UI Requirements

The application must clearly identify itself as:

**NCERT Grade 8 Science**

Suggested branding:

**NCERT AI Tutor**

Secondary label:

**AI Study Tutor**

The page should not look like a generic ChatGPT clone.

---

## Visual Style

Use a clean dark interface.

Prefer:

* deep neutral background
* elevated dark surfaces
* warm educational accent
* restrained borders
* subtle shadows
* readable typography
* generous whitespace

Avoid:

* excessive neon
* excessive glow
* loud gradients
* decorative animations everywhere
* oversized text
* cluttered dashboards

---

## Typography

Text must be comfortable to read for long study sessions.

Prioritize:

* readable body font
* comfortable line-height
* sensible paragraph width
* strong heading hierarchy

Do not use very small body text.

---

## Global CSS

Put shared tokens in:

```text
src/styles/global.css
```

Use CSS custom properties for:

```text
colors
spacing
radius
font sizes
shadows
transitions
```

Avoid duplicating the same values everywhere.

---

## Header

The Header should communicate:

* NCERT AI Tutor
* AI Study Tutor
* Grade 8 · Science

It should be minimal and polished.

---

## Topic Chips

Provide useful example prompts grounded in Grade 8 Science.

Examples:

* What is force?
* Explain pressure.
* What is friction?
* How does sound travel?
* What is the function of the cell membrane?
* Explain photosynthesis.
* How is light reflected?
* What are chemical effects of electric current?

Clicking a topic should place the example into the question field.

---

## Question Input

Requirements:

* textarea rather than a tiny single-line input
* clear placeholder
* Ask Tutor button
* disabled state during loading
* empty-input validation
* keyboard-friendly behavior
* responsive layout

The input should feel like the main action of the application.

---

## Answer Panel

Must support:

### Idle

Explain that the student can ask a question.

### Loading

Show that the tutor is processing the request.

### Success

Present the answer in a highly readable format.

### Error

Show the error and provide an easy retry mechanism.

The answer area must not become an unreadable wall of text.

---

## Accessibility

Use:

* semantic HTML
* labels where appropriate
* descriptive button text
* visible focus indicators
* accessible interactive elements
* sufficient contrast

Do not use color as the only indicator of success/error.

---

## Responsive Behavior

The page should work on:

* desktop
* laptop
* tablet
* mobile

At narrow widths:

* reduce horizontal padding
* stack controls when appropriate
* make the textarea full width
* make buttons touch-friendly

---

## Code Quality

Write:

* simple React functional components
* clear prop names
* sensible component boundaries
* maintainable CSS
* minimal comments

Do not over-engineer.

Do not generate unused abstractions.

Do not add libraries simply to solve basic CSS/layout problems.

---

## Existing Vite Files

Inspect before replacing:

* `main.jsx`
* `App.jsx`
* `index.css`
* `App.css`
* `vite.config.*`

Remove Vite starter references only when necessary.

Do not damage the working Vite configuration.

---

## Testing Requirements

After implementation:

```bash
npm run dev
```

Confirm:

* application loads
* no compile errors
* no import errors
* UI responds to interaction
* topic chips work
* loading works
* API request works
* backend errors are displayed

Backend should be run separately using:

```bash
python -m uvicorn main:app --reload
```

---

## Security Rules

Never place:

```text
GOOGLE_API_KEY
```

in React.

Never put the FAISS database in the public frontend.

Never hard-code secrets into JSX, CSS, or JavaScript.

The browser only communicates with FastAPI.

---

## Future Compatibility

Keep the current implementation easy to extend with:

* chat memory
* chapter filters
* source display
* summaries
* quizzes
* bookmarks
* progress tracking

Do not implement those features yet unless explicitly instructed.
