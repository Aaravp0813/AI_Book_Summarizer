# NCERT AI Tutor — Coding Instructions

## Role

Act as the frontend engineer for a local React + Vite application called:

**NCERT AI Tutor**

The application helps students study the **NCERT Grade 8 Science textbook**.

You are working inside an existing project, not a blank project.

---

## 1. Inspect the Entire Project First

Before changing anything, inspect the entire project rooted at:

```text
E:\My_Projects\AI_Book_Summarizer\
```

Inspect, where present:

```text
main.py
Book_Summarizer.py
faiss_ncert_db/
frontend/
frontend/package.json
frontend/src/
frontend/index.html
frontend/vite.config.*
.env
plan.md
instruction.md
```

Also inspect relevant files nested inside `frontend/src`.

### Do NOT assume:

* the frontend is empty
* dependencies are missing
* files do not exist
* the backend needs modification
* FAISS needs rebuilding

The repository's actual state is authoritative.

---

## 2. Skip Completed Work

For every task you consider:

### Already correct

Skip it.

### Partially implemented

Complete only the missing pieces.

### Incorrect

Fix it.

### Missing

Create it.

### Existing but unnecessary

Do not duplicate it.

Never recreate a working component merely because this instruction document lists a target filename.

---

## 3. Project Technology

Use:

* React
* Vite
* JavaScript
* JSX
* standard CSS

Do not use:

* TypeScript
* Tailwind
* Bootstrap
* Material UI
* unnecessary UI libraries

Do not add dependencies unless genuinely required.

---

## 4. Dependency Installation

Inspect:

```text
frontend/package.json
```

and determine whether dependencies are installed.

If installation is required:

```bash
npm install
```

If dependencies are already installed and correct:

**Do not run unnecessary installation commands.**

Do not replace Vite unless a real compatibility problem exists.

Do not change versions without a technical reason.

---

## 5. Backend

The existing backend is:

```text
main.py
```

It should expose:

```text
GET /
POST /ask
```

Main endpoint:

```text
http://127.0.0.1:8000/ask
```

Current request:

```json
{
  "question": "What is photosynthesis?"
}
```

Current response:

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

### Backend Rule

Do not redesign or rewrite `main.py` as part of the frontend task.

Only modify backend code if inspection reveals a real incompatibility that prevents the frontend from functioning.

If modification is required, make the smallest safe change and preserve:

```text
FastAPI
→ FAISS
→ NCERT context
→ Gemini
```

---

## 6. FAISS

The existing FAISS database belongs to the backend.

The frontend must never:

* import FAISS
* access `index.faiss`
* access `index.pkl`
* load the database
* search the database

The browser communicates only with FastAPI.

---

## 7. Frontend Architecture

Use the following architecture when appropriate:

```text
frontend/
└── src/
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

However:

**Do not create every file blindly.**

Reuse equivalent existing files if they already exist.

---

## 8. React Component Rules

### App.jsx

Keep it thin.

It should primarily establish the root application structure.

Do not put all tutoring logic into App.jsx.

### Home.jsx

Own:

* question
* answer
* loading
* error

It should connect the UI to the API service.

### Layout.jsx

Own:

* header
* main content
* footer
* page shell

It should not own API logic.

### Header.jsx

Display:

* NCERT AI Tutor
* AI Study Tutor
* NCERT Grade 8 Science

### TopicChips.jsx

Provide useful Grade 8 Science example questions.

Clicking one should populate the question input.

### QuestionInput.jsx

Provide:

* textarea
* placeholder
* Ask Tutor button
* validation
* loading/disabled state

Do not put direct API calls here.

### AnswerPanel.jsx

Support:

* idle
* loading
* success
* error

Keep the answer readable.

---

## 9. API Service

Create:

```text
frontend/src/services/api.js
```

if it does not exist.

If it already exists, inspect and reuse it.

It should call:

```text
POST http://127.0.0.1:8000/ask
```

with:

```json
{
  "question": "..."
}
```

It should:

* send JSON
* set `Content-Type`
* parse JSON
* return the API response
* handle network errors
* handle non-2xx responses
* display/use backend `detail` when available

Do not place the Gemini API key in this file.

Do not directly call Gemini from React.

---

## 10. Visual Design

Use a clean dark theme.

The design should feel:

* modern
* professional
* educational
* calm
* readable

Prefer:

* deep neutral backgrounds
* dark elevated surfaces
* restrained borders
* warm accent color
* subtle shadows
* generous spacing

Avoid:

* excessive glow
* cyberpunk aesthetics
* huge gradients
* excessive glass effects
* excessive animation
* clutter

---

## 11. Typography

Prioritize long-session readability.

Use:

* clear headings
* readable body text
* comfortable line height
* sensible paragraph width
* appropriate control sizes

Do not use tiny body text or extremely thin typography.

---

## 12. CSS Architecture

Keep CSS separated by responsibility.

Global variables belong in:

```text
frontend/src/styles/global.css
```

Use CSS custom properties for:

* colors
* spacing
* radius
* typography
* shadows
* focus states
* status colors

Component-specific styling belongs in component CSS files.

Do not create one massive stylesheet unless the existing project already uses that pattern and it is working well.

---

## 13. Accessibility

Use:

* semantic HTML
* labels
* accessible buttons
* keyboard navigation
* visible focus states
* sufficient contrast

Do not communicate success/error using color alone.

---

## 14. Responsive Design

Support:

* desktop
* laptop
* tablet
* mobile

On smaller displays:

* reduce outer padding
* allow controls to stack
* make textarea full width
* keep buttons touch-friendly
* prevent horizontal scrolling

---

## 15. Security

Never expose:

```text
GOOGLE_API_KEY
```

in:

* React
* JSX
* frontend JavaScript
* frontend `.env`
* public assets

The Gemini API key stays on the Python backend.

Never place FAISS files in the public frontend.

---

## 16. Existing Vite Files

Inspect before replacing:

```text
frontend/src/main.jsx
frontend/src/App.jsx
frontend/src/index.css
frontend/src/App.css
frontend/vite.config.*
```

Remove starter references only when necessary.

Do not damage the Vite setup.

---

## 17. Testing

After implementation, run:

```bash
npm run dev
```

Confirm:

* application launches
* no compile errors
* no import errors
* components render
* CSS loads
* topic chips work
* question input works
* loading state works
* API request works
* success state works
* error state works

The backend may be run separately with:

```bash
python -m uvicorn main:app --reload
```

---

## 18. Do Not Over-Engineer

Use simple React functional components.

Do not add abstractions that are not needed.

Do not introduce libraries just for simple UI behavior.

Do not implement:

* chat memory
* authentication
* database-backed users
* quizzes
* progress tracking
* additional subjects

unless explicitly requested.

The current goal is the Grade 8 Science tutor.

---

## 19. Completion Criteria

Before saying the task is complete, verify:

* the frontend runs
* existing functionality remains intact
* all imports work
* API integration works
* errors are handled
* the layout is responsive
* the design is cohesive
* no secrets are exposed
* no duplicate components were created
* no unnecessary dependencies were added

Finally, report:

1. Files created.
2. Files modified.
3. Files skipped because they were already correct.
4. Dependencies installed or changed.
5. Any remaining issues.

**Primary rule: inspect → compare → skip completed work → fix partial work → create missing work → test.**

## Existing Science Database — Canonical Reference

The NCERT Grade 8 Science FAISS database has already been built successfully.

Treat the existing Science implementation as the canonical reference for all future subject indexes.

When modifying `Book_Summarizer.py`:

1. Inspect how the existing Science index was created.
2. Preserve its current chunking and indexing methodology.
3. Generalize that implementation so it can be used for other subjects.

The other subjects must use the same:

- PDF extraction method
- chunk size
- chunk overlap
- text formatting
- embedding model
- embedding batch size
- retry/rate-limit handling
- FAISS construction method
- metadata/source handling

Do not create a separate chunking strategy for Mathematics, Social Science, or English.

IMPORTANT:

Modify the indexing code only.

DO NOT:

- run the index builder
- process the other textbooks
- generate embeddings
- call the Gemini embedding API
- create new FAISS databases
- rebuild the existing Science database
- overwrite existing FAISS files

The new subject indexes will be generated manually later.