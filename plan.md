# NCERT AI Tutor — Frontend Development Plan

## 1. Project Overview

Build a local React + Vite frontend for an AI-powered study tutor focused specifically on the **NCERT Grade 8 Science textbook**.

The frontend will communicate with an existing local FastAPI backend.

The backend already performs:

1. User question reception.
2. FAISS similarity search over the NCERT textbook.
3. Retrieval of the most relevant textbook chunks.
4. Gemini generation using the retrieved context.
5. Returning the question and generated answer.

The frontend must focus on providing a polished, responsive, modern interface for interacting with this backend.

---

## 2. Existing Backend Contract

The backend is available locally at:

`http://127.0.0.1:8000`

Main endpoint:

`POST /ask`

Full endpoint:

`http://127.0.0.1:8000/ask`

Request body:

```json
{
  "question": "What is photosynthesis?"
}
```

Successful response:

```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is..."
}
```

Possible error response:

```json
{
  "detail": "An error message"
}
```

The frontend must never directly access:

* the Gemini API
* the Gemini API key
* the FAISS database
* the NCERT ZIP archive

The frontend communicates only with FastAPI.

---

## 3. Technology Constraints

Use:

* React
* Vite
* JavaScript
* JSX
* Normal CSS

Do not introduce:

* TypeScript
* Tailwind CSS
* Bootstrap
* Material UI
* unnecessary UI frameworks
* unnecessary dependencies

Keep the frontend lightweight.

---

## 4. Initial Project State

The `frontend` directory already exists and was created using Vite.

The developer has NOT yet:

* run `npm install`
* created custom components
* created pages
* created the API service
* created custom CSS
* copied any generated frontend files

Therefore, build the frontend cleanly from the existing Vite scaffold.

Do not assume any custom files already exist.

---

## 5. Target Folder Structure

Create this structure:

```text
frontend/
├── public/
│
├── src/
│   ├── components/
│   │   ├── Layout.jsx
│   │   ├── Layout.css
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── TopicChips.jsx
│   │   ├── TopicChips.css
│   │   ├── QuestionInput.jsx
│   │   ├── QuestionInput.css
│   │   ├── AnswerPanel.jsx
│   │   └── AnswerPanel.css
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── Home.css
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── styles/
│   │   └── global.css
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

Modify the structure only when there is a strong technical reason.

---

## 6. Component Responsibilities

### Layout

Responsible for:

* page shell
* header placement
* main content area
* footer
* shared application structure

It should not contain the tutoring logic.

### Header

Display:

* application name
* "AI Study Tutor" label
* "NCERT Grade 8 Science" identification
* clean branding

The design should make it obvious that this is an educational NCERT tool rather than a generic AI chatbot.

### TopicChips

Display example questions or topics based on NCERT Grade 8 Science.

Examples:

* Force and Pressure
* Friction
* Sound
* Cell Structure and Functions
* Reproduction in Animals
* Light
* Chemical Effects of Electric Current
* Some Natural Phenomena

Clicking a chip should populate the question input.

### QuestionInput

Responsible for:

* multiline question input
* submit button
* disabled state while loading
* keyboard-friendly interaction
* validation for empty questions

### AnswerPanel

Handle these states:

1. Idle
2. Loading
3. Success
4. Error

The success state should present the answer in a comfortable reading layout.

The loading state should clearly communicate that the tutor is processing the question.

The error state should display a useful human-readable message and allow retrying.

### Home

Own the main page state:

* current question
* current answer
* loading state
* error state

It should call the API service rather than directly using `fetch()` inside multiple UI components.

### API Service

`src/services/api.js` must contain the FastAPI communication.

Use:

```text
http://127.0.0.1:8000/ask
```

POST:

```json
{
  "question": "..."
}
```

Return:

```json
{
  "question": "...",
  "answer": "..."
}
```

Handle network errors and non-successful HTTP responses.

---

## 7. Visual Design

The application should be:

* dark themed
* modern
* clean
* readable
* educational
* professional
* understated

Avoid:

* excessive gradients
* neon cyberpunk styling
* excessive glassmorphism
* giant rounded cards everywhere
* excessive animation
* visual clutter

The design should feel suitable for a student using it for extended study sessions.

---

## 8. Typography

Prioritize readability.

Use a modern readable font stack.

Recommended conceptual roles:

* display/headings: modern geometric sans-serif
* body: highly readable sans-serif
* tiny metadata/badges: optional monospace

Avoid excessively thin text.

Use comfortable:

* font sizes
* line heights
* paragraph widths
* spacing

---

## 9. Color System

Use CSS variables in `global.css`.

Define variables for:

* page background
* elevated background
* panel background
* primary text
* secondary text
* muted text
* border
* accent
* success
* error
* focus state

Do not repeatedly hard-code colors throughout individual CSS files.

---

## 10. Responsive Design

Support:

* desktop
* laptop
* tablet
* mobile

The main content should have a reasonable maximum width.

The question input should remain comfortable on narrow screens.

Buttons and controls must remain usable on touch devices.

---

## 11. Accessibility

Use:

* semantic HTML
* visible labels or accessible labels
* descriptive button text
* keyboard navigation
* visible focus states
* sufficient color contrast

Do not rely only on color to communicate loading, error, or success.

---

## 12. API Integration

The frontend should be connected to the real backend rather than mocked.

Do not implement a fake response layer once the UI is functional.

Use a central API service:

```text
src/services/api.js
```

Do not put the Gemini API key anywhere in the frontend.

---

## 13. Error Handling

Handle at least:

### Empty question

Show a clear validation message.

### Backend unavailable

Display something like:

"Couldn't reach the tutor server. Make sure the FastAPI backend is running."

### HTTP error

Display the backend's `detail` message when available.

### Unexpected response

Fail gracefully rather than crashing the application.

---

## 14. Development Sequence

Implement in this order:

### Step 1

Inspect the existing Vite scaffold.

### Step 2

Run:

```bash
npm install
```

### Step 3

Create folders and components.

### Step 4

Build global styling and theme.

### Step 5

Build Layout and Header.

### Step 6

Build Home page.

### Step 7

Build QuestionInput and TopicChips.

### Step 8

Build AnswerPanel states.

### Step 9

Implement `api.js`.

### Step 10

Connect Home to the API.

### Step 11

Run:

```bash
npm run dev
```

### Step 12

Test against:

```text
http://127.0.0.1:8000
```

---

## 15. Acceptance Criteria

The frontend is considered complete when:

* `npm run dev` starts successfully.
* There are no React import errors.
* There are no browser console errors caused by the frontend.
* The page is responsive.
* The dark theme is consistent.
* The application clearly identifies itself as an NCERT Grade 8 Science AI tutor.
* Topic chips populate the question input.
* The user can submit a question.
* A loading state appears.
* The question is sent to `POST /ask`.
* The returned answer is displayed.
* Backend errors are displayed gracefully.
* No Gemini key exists in the frontend.
* No FAISS logic exists in the frontend.
* Components remain separated and maintainable.

---

## 16. Future Expansion

Design the code so the following can be added later without major restructuring:

* chat history
* chapter selection
* source references
* summary mode
* explanation mode
* quiz mode
* study progress
* saved questions
* authentication
* additional NCERT subjects

Do not implement these features yet unless explicitly requested.
