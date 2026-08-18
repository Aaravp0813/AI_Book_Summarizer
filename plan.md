# NCERT AI Tutor — Frontend Development Plan

## 1. Project Overview

Build and integrate a local React + Vite frontend for an AI-powered study tutor focused on the **NCERT Grade 8 Science textbook**.

The frontend communicates with an existing local FastAPI backend.

The backend is responsible for:

1. Receiving the student's question.
2. Searching the NCERT FAISS vector database.
3. Retrieving relevant textbook chunks.
4. Sending the retrieved context to Gemini.
5. Returning the generated answer to the frontend.

The frontend is responsible for:

1. Providing the user interface.
2. Collecting the student's question.
3. Sending the question to FastAPI.
4. Showing loading, success, and error states.
5. Displaying the generated answer clearly.

The project is currently being developed locally.

---

## 2. Critical Implementation Rule

Before making changes, **inspect the entire project**.

Do not assume that the project is empty.

For every planned step:

* If it is already correctly implemented, skip it.
* If it is partially implemented, complete only what is missing.
* If it is incorrect, fix it.
* If it does not exist, create it.
* Do not overwrite working code unnecessarily.
* Do not create duplicate files or duplicate functionality.
* Do not reinstall dependencies that are already correctly installed.
* Do not rebuild the FAISS database unless necessary.
* Do not rewrite the FastAPI backend merely to implement the frontend.

The **actual state of the project takes precedence over this plan**.

---

## 3. Entire Project Structure

The project root is:

```text
E:\My_Projects\AI_Book_Summarizer\
```

The project may contain:

```text
AI_Book_Summarizer/
├── main.py
├── Book_Summarizer.py
├── faiss_ncert_db/
├── frontend/
├── .env
├── plan.md
├── instruction.md
└── other project files
```

Copilot must inspect the actual directory structure before making changes.

---

## 4. Existing Backend Contract

The backend is expected to run locally at:

```text
http://127.0.0.1:8000
```

Main endpoint:

```text
POST /ask
```

Full endpoint:

```text
http://127.0.0.1:8000/ask
```

Current request format:

```json
{
  "question": "What is photosynthesis?"
}
```

Current successful response:

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

The frontend must communicate with FastAPI only.

The frontend must never directly access:

* Gemini
* the Gemini API key
* FAISS
* the NCERT ZIP archive
* backend `.env` secrets

---

## 5. Technology

Use:

* React
* Vite
* JavaScript
* JSX
* standard CSS

Do not introduce:

* TypeScript
* Tailwind CSS
* Bootstrap
* Material UI
* unnecessary UI frameworks
* unnecessary dependencies

Keep the application lightweight.

---

## 6. Frontend Starting State

The `frontend` directory already exists and was created using Vite.

Before implementation, inspect:

```text
frontend/package.json
frontend/src/
frontend/index.html
frontend/vite.config.*
```

Determine:

* whether dependencies are already installed
* which React/Vite versions are being used
* which starter files exist
* whether any frontend code has already been written

If dependencies are not installed, run:

```bash
npm install
```

If they are already installed and correct, skip installation.

Do not replace Vite or change versions unless there is a genuine compatibility problem.

---

## 7. Target Frontend Architecture

The desired architecture is:

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

This is a target, not a requirement to blindly recreate every file.

If equivalent files/components already exist, reuse and improve them.

---

## 8. Component Responsibilities

### Layout

Responsible for:

* page shell
* header placement
* main content
* footer
* overall structure

It should not contain the tutoring/API logic.

### Header

Display:

* NCERT AI Tutor
* AI Study Tutor
* NCERT Grade 8 Science

It should clearly identify the educational purpose of the application.

### TopicChips

Display example Grade 8 Science questions/topics.

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

* multiline textarea
* submit button
* empty-question validation
* loading/disabled state
* keyboard-friendly interaction
* responsive behavior

### AnswerPanel

Support:

1. Idle
2. Loading
3. Success
4. Error

The answer must be presented in a readable study-friendly format.

### Home

Own the main tutoring state:

* question
* answer
* loading
* error

It should communicate with the API service rather than using `fetch()` throughout UI components.

### API Service

Create:

```text
src/services/api.js
```

if it does not exist.

It is responsible for communicating with:

```text
http://127.0.0.1:8000/ask
```

It should:

* send POST JSON
* parse JSON
* handle network failures
* handle non-2xx responses
* use backend `detail` information when available

---

## 9. Visual Design

The website should be:

* dark themed
* modern
* clean
* readable
* professional
* educational
* understated

Avoid:

* excessive gradients
* neon/cyberpunk styling
* excessive glow
* excessive glassmorphism
* oversized cards
* excessive animation
* visual clutter

The interface should be comfortable for long study sessions.

---

## 10. Typography

Prioritize readability.

Use:

* clear heading hierarchy
* comfortable body font size
* comfortable line height
* reasonable paragraph width
* readable controls

Avoid overly thin or tiny body text.

---

## 11. Color System

Use CSS variables in:

```text
src/styles/global.css
```

Define variables for:

* page background
* surfaces
* primary text
* secondary text
* muted text
* border
* accent
* success
* error
* focus
* spacing
* radius
* typography
* shadows

Avoid repeatedly hard-coding identical values.

---

## 12. Responsive Design

Support:

* desktop
* laptop
* tablet
* mobile

Ensure:

* question input remains usable on small screens
* buttons remain touch-friendly
* no horizontal overflow occurs
* content spacing adapts appropriately

---

## 13. Accessibility

Use:

* semantic HTML
* accessible labels
* descriptive buttons
* visible focus states
* keyboard navigation
* sufficient contrast

Do not rely solely on color for status information.

---

## 14. Error Handling

Handle:

### Empty question

Show an understandable validation message.

### Backend unavailable

Display a clear message such as:

> Couldn't reach the tutor server. Make sure the FastAPI backend is running.

### Backend HTTP error

Display the backend `detail` message when available.

### Unexpected response

Fail gracefully rather than crashing.

---

## 15. Backend and Frontend Separation

Backend:

```text
main.py
```

is responsible for:

```text
Question
  ↓
FAISS
  ↓
NCERT context
  ↓
Gemini
  ↓
Answer
```

Frontend:

```text
frontend/
```

is responsible for:

```text
User
  ↓
React
  ↓
FastAPI
  ↓
React
```

Do not move FAISS or Gemini logic into React.

Do not expose the Gemini API key.

---

## 16. Development Workflow

### Step 1 — Inspect

Inspect the entire repository.

Identify:

* existing backend
* existing FAISS database
* indexing script
* `.env`
* frontend state
* installed dependencies
* existing React components
* existing CSS

### Step 2 — Determine Completed Work

Compare the real project state against this plan.

Mark each task internally as:

* Complete
* Partial
* Missing
* Broken

### Step 3 — Install Dependencies Only If Needed

If `frontend/node_modules` is absent or dependencies are not installed:

```bash
npm install
```

Otherwise skip.

### Step 4 — Implement Missing Frontend Pieces

Create only missing files.

Modify only files that actually need changes.

### Step 5 — Connect API

Implement or fix:

```text
src/services/api.js
```

Use the existing FastAPI `/ask` contract.

### Step 6 — Integrate Components

Connect:

```text
Layout
Header
TopicChips
QuestionInput
AnswerPanel
Home
App
```

only where they are required.

### Step 7 — Validate

Run:

```bash
npm run dev
```

Test the UI.

If backend testing is required:

```bash
python -m uvicorn main:app --reload
```

---

## 17. Acceptance Criteria

The frontend is complete when:

* `npm run dev` starts successfully.
* Existing working functionality has not been unnecessarily broken.
* There are no React import errors.
* There are no frontend runtime errors.
* The page is responsive.
* The dark theme is consistent.
* The application clearly identifies itself as an NCERT Grade 8 Science tutor.
* Topic chips work.
* A student can enter a question.
* Loading state appears during the API request.
* The question is sent to `POST /ask`.
* The returned answer is displayed.
* Backend errors are handled gracefully.
* No Gemini API key exists in the frontend.
* No FAISS logic exists in the frontend.
* The architecture remains maintainable.

---

## 18. Future Expansion

Keep the architecture easy to extend later with:

* chat history
* chapter selection
* source references
* summary mode
* explanation mode
* quiz mode
* saved questions
* study progress
* authentication
* additional NCERT subjects

Do not implement future features unless explicitly requested.

---

## 19. Final Rule

**Inspect first. Reuse existing work. Skip completed steps. Fix incomplete work. Create only what is missing. Do not rewrite functioning code without a reason.**

## Existing Science Vector Database — Reference Implementation

The **NCERT Grade 8 Science FAISS database has already been created successfully**.

The existing Science database is the reference implementation for all other subjects.

Do NOT rebuild, regenerate, overwrite, or otherwise modify the existing Science database during this task.

When extending the indexing system to other subjects, use the **same indexing methodology already used to create the Science database**, including:

- PDF text extraction method
- chunk size
- chunk overlap
- text formatting
- embedding model
- embedding batch size
- retry/rate-limit handling
- FAISS construction method
- metadata/source handling, if already present

The goal is to generalize the existing Science indexing pipeline rather than create a different indexing pipeline for each subject.

The intended architecture is:

Science
  ↓
Existing indexing pipeline
  ↓
Science FAISS database ✅ already exists

Mathematics
  ↓
Same indexing pipeline
  ↓
Mathematics FAISS database

Social Science
  ↓
Same indexing pipeline
  ↓
Social Science FAISS database

English
  ↓
Same indexing pipeline
  ↓
English FAISS database

The existing Science database must remain untouched during this task.
