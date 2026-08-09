# PROMPT 3 — AI INTERVIEWER AGENT DEVELOPMENT TRANSCRIPT

## Project: AI Interviewer Agent

This document records the prompts, requirements, implementation decisions, debugging instructions, and UI/UX directions discussed while developing the AI Interviewer Agent.

---

# 1. PROJECT OVERVIEW

We are building an **AI Interviewer Agent** that conducts interviews using AI.

The system should not behave like a simple static questionnaire. The AI should actively participate in the interview by:

- Generating interview questions dynamically
- Asking questions based on the candidate's profile
- Maintaining interview context
- Evaluating candidate responses
- Generating follow-up questions when appropriate
- Producing an AI-generated transcript
- Assessing technical and behavioral performance
- Providing scores and feedback
- Maintaining structured interview data

The application should have a professional, modern, high-quality interface suitable for an actual recruitment/interview platform.

---

# 2. IMPORTANT REQUIREMENT — AI MUST BE USED

The project was specifically required to include AI.

AI should therefore be a meaningful part of the application rather than being used only as a decorative feature.

The AI should contribute to:

1. Question generation
2. Interview flow
3. Candidate response analysis
4. Follow-up question generation
5. Evaluation
6. Transcript generation/processing
7. Final feedback
8. Candidate scoring

The implementation should clearly demonstrate where AI is being used.

---

# 3. AI INTERVIEWER AGENT

The core component is an AI Interviewer Agent.

The agent should behave like an interviewer instead of simply displaying predefined questions.

The expected flow is:

Candidate
↓
Login
↓
Interview setup
↓
AI generates/selects question
↓
Candidate answers
↓
AI analyzes response
↓
AI determines next question
↓
Interview continues
↓
Transcript generated
↓
AI evaluation
↓
Final score and feedback

The AI should maintain context throughout the interview.

---

# 4. INTERVIEW BEHAVIOR

The AI interviewer should:

- Introduce itself professionally
- Explain the interview process
- Ask one question at a time
- Wait for the candidate response
- Analyze the response
- Decide whether a follow-up question is useful
- Adjust question difficulty where appropriate
- Avoid repeatedly asking the same question
- Maintain the conversation context
- Stay within the selected interview domain
- Avoid irrelevant questions
- Complete the interview within a defined number of questions or time limit

The interviewer should feel conversational rather than robotic.

---

# 5. INTERVIEW TYPES

The system should be capable of supporting different interview categories.

Possible categories include:

- Technical Interview
- Behavioral Interview
- HR Interview
- Role-specific Interview
- Mixed Interview

The AI should generate questions according to the selected category.

For example:

Technical:
- Programming
- Data structures
- Algorithms
- Databases
- APIs
- Frameworks
- System design

Behavioral:
- Teamwork
- Leadership
- Conflict resolution
- Problem solving
- Communication

HR:
- Motivation
- Career goals
- Strengths
- Weaknesses
- Company fit

---

# 6. CANDIDATE CONTEXT

The AI interviewer should use candidate information when available.

Candidate information may include:

- Candidate ID
- Name
- Email
- Resume
- Skills
- Education
- Projects
- Experience
- Certifications
- Job role
- Interview type

The candidate's skills and profile should influence question generation.

For example, if a candidate lists:

Python
FastAPI
PostgreSQL
Machine Learning

the AI should be able to generate questions related to those skills instead of asking completely generic questions.

---

# 7. LOGIN PAGE

The login page should be redesigned to look professional and modern.

The login page should NOT display a large "Candidate ID" field/header at the top as the primary identifier.

The user should be able to enter:

- Email
- Password

The interface should include:

- Clean authentication card
- Professional typography
- Proper spacing
- Clear input fields
- Login button
- Forgot password option if supported
- Error message for invalid credentials

Invalid credentials should produce a clear message such as:

"Invalid email or password."

The page should not look like a basic HTML form.

---

# 8. UI/UX REQUIREMENTS

The frontend should have a polished, AI-generated-product quality appearance.

The interface should feel like a modern SaaS/recruitment platform.

Important requirements:

- High pixel-quality visual design
- Clean spacing
- Consistent typography
- Modern cards
- Soft borders
- Subtle shadows
- Professional buttons
- Clear hierarchy
- Responsive layout
- Smooth interactions
- Consistent colors
- Accessible contrast

Avoid:

- Excessive gradients
- Random colors
- Oversized elements
- Poor spacing
- Basic browser-style inputs
- Inconsistent border radius
- Cluttered layouts

The interface should look like a production-level application.

---

# 9. LOGIN UI REFERENCE

The desired login UI direction is inspired by a modern polished authentication interface.

The input/card areas should have:

- Soft background
- Rounded corners
- Clear border
- Subtle shadow
- Proper internal padding

The visual appearance should be similar in quality to a professionally generated UI mockup.

The box colors should not be harsh.

The interface should feel premium but still simple.

---

# 10. FRONTEND TECHNOLOGY

Frontend stack:

- React
- Vite
- JavaScript/JSX
- CSS

Expected structure:

frontend/
├── public/
│   └── favicon.svg
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │
│   ├── pages/
│   │
│   ├── services/
│   │
│   ├── hooks/
│   │
│   ├── context/
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css

React Router should be used for page navigation.

---

# 11. BACKEND TECHNOLOGY

Backend stack:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- python-dotenv
- HTTPX
- OpenAI API
- LangChain where appropriate

The backend should expose REST APIs for:

- Authentication
- Candidate information
- Interview creation
- Interview questions
- Candidate answers
- AI evaluation
- Transcript
- Results

---

# 12. ENVIRONMENT VARIABLES

Sensitive API keys must NOT be hardcoded.

Use a `.env` file.

Example:

OPENAI_API_KEY=your_api_key_here

Other environment-specific values should also be stored in `.env`.

The `.env` file must not be committed to GitHub.

The project should contain an appropriate `.gitignore`.

---

# 13. AI SERVICE ARCHITECTURE

AI-related logic should be separated from normal API routes.

Recommended structure:

backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── interviewer_agent.py
│   │   ├── evaluation_service.py
│   │   └── transcript_service.py
│   ├── core/
│   └── main.py

AI logic should not be scattered across multiple route files.

---

# 14. AI INTERVIEWER AGENT LOGIC

The interviewer agent should receive structured context.

Example context:

{
  "candidate": {
    "name": "...",
    "skills": ["Python", "FastAPI", "SQL"],
    "experience": "...",
    "projects": [...]
  },
  "interview_type": "technical",
  "role": "Backend Developer",
  "conversation_history": [...]
}

The agent should use this information to determine the next appropriate question.

---

# 15. QUESTION GENERATION

The AI should generate questions that are:

- Relevant
- Clear
- Non-repetitive
- Appropriate for the candidate's level
- Related to the job role
- Related to candidate skills
- Increasingly challenging where appropriate

Questions should not all have the same structure.

For example:

Instead of repeatedly asking:

"What is FastAPI?"

the AI can progressively ask:

1. What is FastAPI and why would you use it?
2. How does dependency injection work in FastAPI?
3. How would you structure a production FastAPI application?
4. How would you handle authentication?
5. How would you optimize a slow endpoint?

This creates a more realistic interview experience.

---

# 16. FOLLOW-UP QUESTIONS

One of the most important AI features is adaptive follow-up questioning.

If the candidate gives an incomplete answer, the AI should be able to ask:

"Could you explain how you would handle that in a production environment?"

If the candidate gives an excellent answer, the AI can increase difficulty.

If the answer is incorrect, the AI can ask a clarifying question before moving on.

The AI should not blindly generate the next predefined question.

---

# 17. ANSWER EVALUATION

Each candidate response should be evaluated by the AI.

Possible evaluation criteria:

- Technical correctness
- Relevance
- Completeness
- Clarity
- Depth
- Problem-solving ability
- Communication

Example structured evaluation:

{
  "score": 8,
  "technical_accuracy": 8,
  "relevance": 9,
  "clarity": 7,
  "depth": 8,
  "feedback": "Good understanding of FastAPI dependency injection..."
}

The exact scoring format can be adjusted based on the backend implementation.

---

# 18. INTERVIEW SCORING

The final interview score should be calculated using individual evaluation results.

Possible categories:

Technical Knowledge
Problem Solving
Communication
Role Knowledge
Adaptability

The final score should not be based on a single answer.

It should aggregate the candidate's performance throughout the interview.

---

# 19. AI TRANSCRIPT

The project has a strict requirement to demonstrate AI usage.

Therefore, an AI transcript should be maintained as part of the interview process.

The transcript should contain:

- AI questions
- Candidate responses
- Follow-up questions
- Interview timestamps where available
- Evaluation information where appropriate

Example:

INTERVIEWER:
Explain how you would design a REST API using FastAPI.

CANDIDATE:
I would first define the API routes...

INTERVIEWER:
How would you handle authentication?

CANDIDATE:
I would use JWT-based authentication...

The transcript should be available after the interview.

---

# 20. AI TRANSCRIPT OF DEVELOPMENT PROMPTS

Because multiple AI tools were used while building the project, the project should maintain a record of AI development prompts.

The project may include:

ai_transcript/
├── prompt1.md
├── prompt2.md
├── prompt3.md
└── README.md

These files document the prompts used with AI assistants during development.

The transcript demonstrates responsible use of AI during development.

---

# 21. PROMPT DOCUMENTATION

Every prompt file should describe:

- What was requested
- Why it was requested
- Technical requirements
- UI requirements
- Changes requested
- Debugging instructions
- Important constraints

The goal is to make the AI-assisted development process transparent and reproducible.

---

# 22. BACKEND API REQUIREMENTS

Possible endpoints:

POST /auth/login

POST /interviews

GET /interviews/{id}

POST /interviews/{id}/questions

POST /interviews/{id}/answers

POST /interviews/{id}/evaluate

GET /interviews/{id}/transcript

GET /interviews/{id}/results

The exact endpoint names can be adapted to the existing backend.

---

# 23. FRONTEND INTERVIEW PAGE

The interview screen should clearly display:

- Interview title
- Candidate information
- Progress indicator
- Current AI question
- Answer input
- Submit/Next button
- Interview timer if implemented
- Interview status

The interface should make it obvious whether the user is:

- Waiting for the AI
- Answering
- Submitting
- Moving to the next question
- Completing the interview

---

# 24. INTERVIEW EXPERIENCE

The interview should feel like a real conversation.

Example:

AI:
"Welcome to your Backend Developer interview. We'll begin with some questions about your experience with Python and APIs."

AI:
"Can you explain how you would design a REST API using FastAPI?"

Candidate:
"I would create routes using FastAPI..."

AI:
"Good. How would you secure those endpoints?"

Candidate:
"I would use JWT authentication..."

AI:
"Can you explain how you would validate and refresh JWT tokens?"

The sequence should be generated dynamically based on context.

---

# 25. ERROR HANDLING

The application should handle:

- Invalid login
- Missing API key
- AI API failures
- Network errors
- Invalid candidate data
- Empty candidate responses
- Database errors
- Timeout errors
- Unexpected AI responses

The frontend should display user-friendly error messages.

Do not expose raw backend stack traces to users.

---

# 26. AI RESPONSE VALIDATION

AI output should preferably be structured.

For example:

{
  "next_question": "...",
  "reason": "...",
  "difficulty": "medium",
  "evaluation_required": true
}

Structured output should be validated before being used by the application.

If the AI returns invalid output, the backend should handle the failure safely.

---

# 27. TESTING

The project should include tests for:

- Authentication
- Interview creation
- Question generation
- Answer submission
- AI evaluation
- Transcript generation
- Error handling

Pytest is used for backend testing.

Example:

python -m pytest -v

Tests should be fixed whenever import or configuration errors occur.

---

# 28. COMMON DEVELOPMENT ISSUE — BACKEND NOT RUNNING

If the React frontend displays API-related errors, first verify that the FastAPI backend is running.

Example:

uvicorn app.main:app --reload

The backend should normally be accessible through:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Frontend and backend must both be running during full-stack testing.

---

# 29. CORS

The FastAPI backend should allow the React development server to communicate with it.

For Vite, the development frontend is commonly hosted on:

http://localhost:5173

Configure CORS appropriately.

Do not use unrestricted CORS in production unless there is a specific reason.

---

# 30. GIT REQUIREMENTS

The project is maintained using Git.

Before committing:

git status

Review modified files.

Do not accidentally commit:

.env

venv/

node_modules/

temporary files

build artifacts

AI API keys

If only intended files are modified, stage those files explicitly.

Example:

git add <file>

Then:

git commit -m "Update AI interviewer"

Then push to the correct branch.

---

# 31. IMPORTANT .ENV ISSUE

A modified `.env` file may appear in:

git status

Example:

Changes not staged for commit:
    modified: ../backend/.env

The `.env` file should generally remain local and should not be committed if it contains secrets.

If `.env` is already tracked, it should be removed from Git tracking while retaining the local file, and `.gitignore` should be configured appropriately.

---

# 32. UI QUALITY STANDARD

The frontend should be treated as a production-quality product rather than a college-project prototype.

Target characteristics:

- Pixel-perfect spacing
- Consistent design system
- Modern typography
- Strong visual hierarchy
- Responsive layout
- Professional color palette
- High-quality cards
- Clean icons
- Smooth transitions
- Clear states
- Accessible forms

The AI-generated UI should look polished enough for a project demonstration.

---

# 33. DEVELOPMENT PRINCIPLE

Do not rewrite working functionality unnecessarily.

When modifying the application:

1. Inspect the existing structure.
2. Identify the exact component/file responsible.
3. Make the smallest safe change.
4. Preserve existing functionality.
5. Test the affected feature.
6. Fix regressions before moving to the next feature.

Avoid replacing the entire project when only a small component needs modification.

---

# 34. AI IMPLEMENTATION PRINCIPLE

AI should be integrated into the actual application workflow.

Do not create fake AI responses such as:

"AI generated question..."

without actually invoking the configured AI service.

Where AI is unavailable, the application may provide a controlled fallback for development, but production behavior should use the actual AI service.

---

# 35. SECURITY

Important security requirements:

- Never hardcode API keys.
- Store secrets in `.env`.
- Never expose API keys to React.
- AI API calls should happen through the backend.
- Validate user input.
- Authenticate protected endpoints.
- Avoid exposing internal errors.
- Sanitize transcript/output where necessary.

---

# 36. EXPECTED FINAL APPLICATION

The completed AI Interviewer Agent should provide:

### Candidate

- Login
- Interview setup
- AI interview
- Dynamic questions
- Adaptive follow-ups
- Answer submission
- Interview progress
- Transcript
- Final results

### AI

- Question generation
- Context awareness
- Adaptive questioning
- Answer evaluation
- Scoring
- Feedback
- Transcript support

### Backend

- Authentication
- Database
- Interview APIs
- AI service
- Evaluation service
- Transcript service

### Frontend

- Professional login
- Dashboard/interview interface
- Interview screen
- Results screen
- Transcript screen
- Responsive UI

---

# 37. FINAL GOAL

The final system should demonstrate that the project is a genuine **AI-powered Interviewer Agent**, not merely a CRUD application with an AI label.

The strongest demonstration should show:

Candidate logs in
→ selects/starts interview
→ AI introduces itself
→ AI asks a dynamically generated question
→ candidate answers
→ AI analyzes the response
→ AI asks an adaptive follow-up
→ interview continues
→ AI evaluates performance
→ transcript is generated
→ candidate receives final score and feedback.

The AI behavior, backend architecture, frontend quality, and transcript documentation should all support this workflow.

---

# 38. DEVELOPMENT CONTEXT

Multiple AI assistants were used during development, including ChatGPT and Claude.

The prompts used during development should be preserved as part of the project documentation.

This file represents the third major prompt/documentation stage of the AI-assisted development process.

The purpose of maintaining these prompt files is to demonstrate:

- How AI was used during development
- What requirements were communicated to AI
- How the architecture evolved
- How UI requirements were communicated
- How debugging was performed
- How AI-assisted development contributed to the final product

---

