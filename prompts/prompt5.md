Absolutely. Below is a **complete `prompt.md`** for the **AI Interviewer** project, combining the requirements and MVP direction we've discussed so far, including the core workflow, GitHub integration, log ingestion, LLM investigation, root-cause analysis, patch generation, commit correlation, investigation timeline, and optional PR creation.

You can save this directly as **`prompt.md`** in your project root.

# AI Interviewer — Complete Project Prompt

## 1. Project Overview

Build a production-quality **AI Interviewer** application that conducts intelligent technical interviews using AI.

The system should simulate a real technical interviewer rather than behaving like a simple chatbot.

The AI Interviewer should:

* Understand the candidate's profile and selected interview configuration.
* Ask relevant technical questions.
* Dynamically adapt questions based on the candidate's previous answers.
* Evaluate answers intelligently.
* Ask follow-up questions when necessary.
* Detect strengths and weaknesses.
* Maintain an interview state throughout the session.
* Provide a final performance analysis.
* Generate a structured interview report.
* Provide actionable feedback for improvement.

The application should have a clean, modern, professional interface suitable for a hackathon MVP and capable of being extended into a production application.

---

# 2. Main Objective

The main objective is to create an AI-powered interviewer capable of conducting an end-to-end technical interview.

The interview should feel like a conversation with a knowledgeable human interviewer.

The AI should not simply follow a fixed list of questions.

Instead, it should:

1. Ask an initial question.
2. Analyze the candidate's answer.
3. Determine whether the answer is correct, partially correct, incorrect, incomplete, or unclear.
4. Decide whether a follow-up question is necessary.
5. Adjust the difficulty when appropriate.
6. Move to another topic when the current topic has been sufficiently evaluated.
7. Track performance throughout the interview.
8. Generate a final evaluation at the end.

---

# 3. Core MVP

The MVP must prioritize the following functionality.

## Required MVP Features

### 3.1 Interview Configuration

Allow the candidate to configure:

* Interview type
* Technical domain
* Programming language
* Difficulty
* Interview duration
* Number of questions
* Experience level

Example domains:

* Data Structures and Algorithms
* Python
* Java
* C++
* JavaScript
* SQL
* Database Management
* Operating Systems
* Computer Networks
* System Design
* Machine Learning
* Data Science

Example difficulty levels:

* Beginner
* Intermediate
* Advanced

---

# 4. Candidate Profile

The candidate should be able to provide information such as:

* Name
* Role
* Experience level
* Skills
* Programming languages
* Preferred domain
* Resume information, if supported

The profile should be used by the AI to personalize the interview.

For example:

If the candidate selects:

> Python + Data Structures + Intermediate

the AI should generate questions appropriate for that combination.

---

# 5. AI Interview Engine

The AI Interview Engine is the central component of the application.

It should maintain the complete interview state.

The state should include:

```text
candidate
interview configuration
current question
question number
previous questions
candidate answers
answer evaluations
difficulty
topics covered
topics remaining
scores
follow-up questions
interview progress
```

The interviewer should behave naturally.

---

# 6. Dynamic Question Generation

Questions should be generated dynamically rather than being limited to a static question bank.

The AI should consider:

* Candidate skill level
* Selected technology
* Previous answers
* Previous performance
* Interview progress
* Difficulty
* Topics already covered

Example:

Candidate:

> "I would use a hash map to solve this in O(n)."

The AI may respond with:

> "Good. Why does the hash map allow you to achieve O(n) average time complexity?"

If the candidate answers correctly, the AI can increase difficulty.

If the candidate struggles, the AI can ask a simpler conceptual question.

---

# 7. Adaptive Difficulty

The interview should dynamically adapt.

## If the candidate performs well

Increase difficulty.

Example:

```text
Easy → Medium → Hard
```

## If the candidate struggles

Decrease or maintain difficulty.

Example:

```text
Hard → Medium
```

The system should not change difficulty randomly.

Difficulty changes should be based on answer evaluation.

---

# 8. Follow-Up Questions

The interviewer should ask follow-up questions when the candidate's answer requires deeper evaluation.

Follow-ups can test:

* Why the solution works
* Time complexity
* Space complexity
* Edge cases
* Alternative solutions
* Practical implementation
* Trade-offs
* Real-world applications

Example:

Question:

> What is the time complexity of binary search?

Candidate:

> O(log n).

AI:

> Correct. Why does the complexity become logarithmic?

---

# 9. Answer Evaluation

Each answer should be evaluated by the AI.

The evaluation should determine:

```text
correctness
technical accuracy
completeness
clarity
reasoning
confidence
depth
```

Possible result:

```json
{
  "correctness": "mostly_correct",
  "score": 8,
  "technical_accuracy": 8,
  "reasoning": 7,
  "clarity": 9,
  "needs_followup": true,
  "feedback": "The candidate correctly identified the approach but did not explain the complexity."
}
```

The internal evaluation should be structured so it can later be used for the final report.

---

# 10. Interview Scoring

Maintain scores throughout the interview.

Possible categories:

* Technical Knowledge
* Problem Solving
* Communication
* Logical Reasoning
* Accuracy
* Depth of Understanding
* Coding Ability
* Time Complexity Knowledge
* System Design Ability

The exact categories should depend on the interview type.

---

# 11. Interview Progress

The UI should show interview progress.

Example:

```text
Question 5 / 10

Progress
██████████░░░░░░░░░░ 50%
```

Also show:

* Current topic
* Current difficulty
* Time remaining
* Questions completed

Do not expose internal AI reasoning.

---

# 12. Interview Interface

The interview page should contain:

## Header

Display:

* AI Interviewer
* Interview type
* Difficulty
* Progress
* Timer

## Main Section

Display:

```text
AI Interviewer

Question:
Explain the difference between stack and queue.
```

## Candidate Answer Area

Provide:

* Text input
* Submit button

If voice functionality is implemented later:

* Start recording
* Stop recording
* Transcript

---

# 13. Interview Conversation

The interface should feel conversational.

Example:

```text
AI Interviewer:
Can you explain how a hash table works?

Candidate:
A hash table stores key-value pairs...

AI Interviewer:
Good. What happens when two keys generate the same hash?

Candidate:
That creates a collision...

AI Interviewer:
Correct. Can you explain two common collision-resolution techniques?
```

The system should maintain context across the entire conversation.

---

# 14. Interview Session Management

Every interview should have a session.

A session should contain:

```text
session_id
candidate_id
configuration
start_time
end_time
status
questions
answers
evaluations
score
final_report
```

Possible statuses:

```text
created
in_progress
completed
cancelled
```

---

# 15. Interview Completion

The interview should end when one of the following occurs:

* Maximum question count reached.
* Configured interview duration expires.
* AI determines sufficient evaluation has been completed.
* Candidate manually ends the interview.

The candidate should receive a completion screen.

---

# 16. Final Interview Report

After completion, generate a structured report.

The report should include:

## Overall Score

Example:

```text
Overall Score: 82 / 100
```

## Performance Summary

Example:

```text
The candidate demonstrated strong understanding of
data structures and algorithms but needs improvement
in complexity analysis and edge-case reasoning.
```

## Category Scores

```text
Technical Knowledge      88%
Problem Solving          84%
Communication            79%
Logical Reasoning        82%
Coding                   80%
```

## Strengths

Example:

```text
- Strong understanding of hash-based data structures
- Good problem decomposition
- Clear communication
```

## Weaknesses

Example:

```text
- Complexity analysis needs improvement
- Some edge cases were missed
- Limited discussion of alternative approaches
```

## Recommendations

Example:

```text
- Practice Big-O analysis
- Solve more graph problems
- Review edge-case handling
```

---

# 17. Question-Level Feedback

The final report should allow the candidate to inspect individual questions.

For every question display:

```text
Question
Candidate Answer
Evaluation
Score
Correct Answer / Expected Approach
Feedback
```

Example:

```text
Question:
What is the time complexity of binary search?

Your Answer:
O(n)

Score:
3 / 10

Feedback:
Binary search operates in O(log n) time because
the search space is divided approximately in half
after each comparison.
```

---

# 18. AI Root Cause / Investigation Concept

The project should use an AI investigation approach where useful.

When an answer is incorrect, the system should not simply mark it wrong.

It should identify why the candidate made the mistake.

Possible reasoning categories:

```text
conceptual misunderstanding
syntax issue
incorrect assumption
incomplete reasoning
complexity misunderstanding
edge-case failure
knowledge gap
```

Example:

```text
Observed:
Candidate repeatedly confuses O(n) and O(log n).

Likely Root Cause:
Incomplete understanding of divide-and-conquer complexity.

Recommended Action:
Practice binary search, merge sort, and divide-and-conquer
complexity analysis.
```

---

# 19. AI Investigation Timeline

A standout feature should be an **AI Investigation Timeline**.

Instead of displaying only a final score, show how the AI reached its conclusions.

Example:

```text
10:01 — Interview Started

10:03 — Strong answer on arrays

10:05 — Candidate struggled with hash collisions

10:07 — Follow-up question generated

10:09 — Candidate demonstrated improved understanding

10:12 — Complexity analysis weakness detected

10:15 — Difficulty adjusted from Medium to Hard

10:20 — Interview completed

10:21 — Final evaluation generated
```

The timeline should present the interview as a structured investigation.

It should be understandable to the candidate.

Do not expose hidden chain-of-thought or private model reasoning.

Only show concise evidence-based events and conclusions.

---

# 20. Git / Code Integration

The application should support GitHub integration where coding/project analysis is required.

The system should be able to connect to a GitHub repository and inspect relevant repository information.

Possible functionality:

* Repository selection
* Branch selection
* Commit history
* Changed files
* Commit messages
* Code changes
* Relevant source files

The application should use this information to support AI analysis.

---

# 21. Git Commit Correlation

A standout feature should be **Git Commit Correlation**.

The AI should attempt to identify which commit introduced a problem.

Example:

```text
Detected Issue:
Null pointer handling failure in authentication flow.

Likely Introduced By:
Commit: a83f91d

Commit Message:
"Refactor authentication middleware"

Confidence:
87%
```

The system should correlate:

```text
issue
code
logs/errors
changed files
commit history
```

The result should clearly explain the evidence used for the correlation without exposing private model reasoning.

---

# 22. Log Ingestion

The application should support log ingestion for debugging/investigation workflows.

Possible sources:

* Uploaded log file
* Pasted logs
* Application logs
* Error stack traces

The system should extract:

```text
timestamp
severity
error
stack trace
service
file
line number
message
```

Example:

```text
ERROR
2026-08-09 10:42:31

File:
auth/service.py

Line:
142

Message:
KeyError: user_id
```

---

# 23. AI Root Cause Analysis

When an error is detected, the AI should analyze:

```text
logs
stack traces
source code
recent commits
repository structure
configuration
```

The output should contain:

```text
Problem
Likely Root Cause
Evidence
Affected File
Affected Line
Related Commit
Recommended Fix
Confidence
```

Example:

```text
Problem:
Authentication request fails when user_id is missing.

Root Cause:
The middleware accesses user_id without validating
whether it exists in the decoded token.

Affected File:
auth/middleware.py

Evidence:
The stack trace points to line 142 and the related
authentication middleware change was introduced in
commit a83f91d.

Confidence:
91%
```

---

# 24. Patch Generation

The AI should be capable of generating a proposed code patch.

The patch should:

* Target the identified file.
* Make the smallest reasonable change.
* Preserve existing behavior.
* Include an explanation.
* Avoid unrelated modifications.

Example:

```diff
- user_id = payload["user_id"]
+ user_id = payload.get("user_id")
+ if not user_id:
+     raise AuthenticationError("Missing user_id")
```

The system should show the proposed patch before applying it.

---

# 25. Patch Validation

Before accepting a patch, the system should ideally validate it through:

* Syntax checking
* Tests
* Static analysis
* Relevant existing test suite

Display results such as:

```text
Patch Generated       ✓
Syntax Check          ✓
Unit Tests             ✓
Regression Tests       ✓
```

If tests fail, show the failure rather than claiming the patch is correct.

---

# 26. Optional Pull Request Creation

An optional feature can allow the user to create a GitHub Pull Request from the generated patch.

Workflow:

```text
Detect Issue
     ↓
Root Cause Analysis
     ↓
Generate Patch
     ↓
Validate Patch
     ↓
Review Changes
     ↓
Create Branch
     ↓
Commit Changes
     ↓
Create Pull Request
```

PR details should include:

```text
Title
Description
Root Cause
Changes Made
Tests
Related Commit
```

PR creation should always require explicit user confirmation.

---

# 27. AI Investigation Dashboard

The application should have an investigation/dashboard interface.

Possible sections:

### Investigation Summary

```text
Issue Detected
Root Cause Identified
Confidence: 91%
```

### Evidence

```text
Logs
Stack Trace
Source Code
Git Commit
```

### Timeline

```text
Error Detected
↓
Relevant File Found
↓
Commit Correlated
↓
Root Cause Identified
↓
Patch Generated
↓
Patch Validated
```

### Proposed Fix

Show the generated patch.

### Validation

Show:

```text
Tests Passed
Tests Failed
Warnings
```

---

# 28. Suggested Application Pages

The application can contain:

```text
/
    Landing Page

/login
    Login

/register
    Registration

/dashboard
    Main Dashboard

/interview/setup
    Interview Configuration

/interview/{id}
    Live AI Interview

/interview/{id}/result
    Interview Results

/interview/{id}/timeline
    Investigation Timeline

/interviews
    Interview History

/investigation
    AI Investigation Dashboard

/github
    GitHub Integration

/repository/{id}
    Repository Analysis

/settings
    User Settings
```

---

# 29. Dashboard

The dashboard should provide quick insights.

Example cards:

```text
Total Interviews
Completed Interviews
Average Score
Best Score
```

Additional sections:

```text
Recent Interviews
Performance Trend
Strongest Skills
Skills To Improve
Latest Investigation
```

The dashboard should be visually clean and informative.

---

# 30. UI / UX Requirements

Use a modern developer-focused interface.

The design should be:

* Clean
* Professional
* Minimal
* Responsive
* Easy to understand
* Suitable for a hackathon demonstration

Avoid unnecessary visual clutter.

Prioritize:

```text
clear hierarchy
readability
fast interaction
useful information
```

---

# 31. Recommended Visual Structure

Use:

* Cards
* Tables
* Tabs
* Progress indicators
* Charts
* Timeline components
* Code blocks
* Diff viewers
* Status badges

Example status badges:

```text
PASS
FAIL
WARNING
IN PROGRESS
COMPLETED
```

---

# 32. Backend Architecture

Recommended backend structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── interview.py
│   │   ├── evaluation.py
│   │   ├── github.py
│   │   ├── investigation.py
│   │   └── reports.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── interview.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── evaluation.py
│   │   └── investigation.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── interview_service.py
│   │   ├── evaluation_service.py
│   │   ├── github_service.py
│   │   ├── log_service.py
│   │   ├── root_cause_service.py
│   │   └── patch_service.py
│   │
│   └── utils/
│
├── tests/
│
├── requirements.txt
└── .env
```

Adapt the structure to the actual implementation instead of creating unnecessary files.

---

# 33. Frontend Architecture

Use a simple frontend architecture suitable for rapid development.

Recommended:

```text
frontend/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── interview_setup.html
│   ├── interview.html
│   ├── results.html
│   ├── timeline.html
│   └── investigation.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── interview.js
│       ├── dashboard.js
│       ├── investigation.js
│       └── github.js
```

---

# 34. API Design

Example endpoints:

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

## Interviews

```text
POST /api/interviews
GET  /api/interviews
GET  /api/interviews/{id}
POST /api/interviews/{id}/start
POST /api/interviews/{id}/answer
POST /api/interviews/{id}/end
```

## Evaluation

```text
POST /api/evaluations
GET  /api/interviews/{id}/evaluations
```

## Reports

```text
GET /api/interviews/{id}/report
GET /api/interviews/{id}/timeline
```

## GitHub

```text
GET  /api/github/repos
GET  /api/github/repos/{owner}/{repo}
GET  /api/github/repos/{owner}/{repo}/commits
GET  /api/github/repos/{owner}/{repo}/files
```

## Investigation

```text
POST /api/investigation/logs
POST /api/investigation/analyze
POST /api/investigation/root-cause
POST /api/investigation/patch
POST /api/investigation/validate
```

---

# 35. Database Design

A relational database can contain tables such as:

```text
users
interviews
interview_questions
answers
evaluations
interview_reports
investigations
investigation_events
repositories
commits
patches
pull_requests
```

Example relationship:

```text
User
 │
 ├── Interviews
 │      │
 │      ├── Questions
 │      │      └── Answers
 │      │             └── Evaluations
 │      │
 │      └── Report
 │
 └── Investigations
        │
        ├── Events
        ├── Commits
        └── Patches
```

---

# 36. Authentication

Implement authentication securely.

Requirements:

* User registration
* Login
* Password hashing
* Session/JWT authentication
* Protected routes
* Logout

Never store plain-text passwords.

Never expose API keys to the frontend.

---

# 37. Environment Variables

Sensitive configuration should be stored in `.env`.

Example:

```env
DATABASE_URL=
SECRET_KEY=
OPENAI_API_KEY=
GITHUB_TOKEN=
```

Do not commit `.env` to GitHub.

Use:

```text
.env
```

in `.gitignore`.

---

# 38. AI Provider Abstraction

Do not tightly couple the entire application to a single AI provider.

Create an AI service layer.

Example:

```python
class AIService:
    def generate_question(...)
    def evaluate_answer(...)
    def generate_followup(...)
    def generate_report(...)
    def analyze_root_cause(...)
    def generate_patch(...)
```

This makes it easier to replace the model/provider later.

---

# 39. Prompt Engineering

The AI interviewer should receive structured context.

Example:

```text
You are an expert technical interviewer.

Candidate:
{candidate_profile}

Interview Configuration:
{configuration}

Current Difficulty:
{difficulty}

Questions Already Asked:
{previous_questions}

Previous Answers:
{previous_answers}

Current Topic:
{topic}

Your task:
Generate the next interview question.

Rules:
1. Do not repeat previous questions.
2. Match the requested difficulty.
3. Consider the candidate's previous performance.
4. Ask one clear question.
5. Do not reveal the expected answer.
6. Prefer questions that test understanding rather than memorization.
```

---

# 40. Answer Evaluation Prompt

Use structured evaluation.

Example:

```text
You are evaluating a candidate's technical interview answer.

Question:
{question}

Expected Concept:
{expected_concept}

Candidate Answer:
{answer}

Evaluate:

1. Correctness
2. Technical accuracy
3. Completeness
4. Reasoning
5. Clarity
6. Confidence
7. Whether a follow-up question is required

Return structured JSON.

Do not provide hidden chain-of-thought.
Provide only concise evidence and conclusions.
```

---

# 41. Final Report Prompt

Example:

```text
Generate a professional technical interview report.

Candidate:
{candidate}

Interview:
{configuration}

Questions:
{questions}

Answers:
{answers}

Evaluations:
{evaluations}

Generate:

- Overall score
- Category scores
- Strengths
- Weaknesses
- Topics requiring improvement
- Recommended practice areas
- Final summary

Do not expose private reasoning.
Base conclusions only on observed interview evidence.
```

---

# 42. Root Cause Analysis Prompt

Example:

```text
You are an expert software debugging assistant.

Analyze the provided:

- Error logs
- Stack traces
- Source code
- Recent changes
- Git commits

Determine:

1. Problem
2. Likely root cause
3. Evidence
4. Affected file
5. Affected line
6. Related commit
7. Confidence
8. Recommended fix

Do not invent evidence.

If the available information is insufficient,
state that clearly.
```

---

# 43. Commit Correlation Prompt

Example:

```text
Identify the Git commit most likely associated
with the detected issue.

Consider:

- Error location
- Changed files
- Commit timestamps
- Commit messages
- Code changes
- Relationship between changed code and failure

Return:

commit_hash
commit_message
affected_files
reason
confidence
```

---

# 44. Patch Generation Prompt

Example:

```text
Generate a minimal patch for the identified issue.

Requirements:

1. Modify only necessary files.
2. Preserve existing behavior.
3. Do not introduce unrelated refactoring.
4. Follow the existing coding style.
5. Explain the change.
6. Identify possible risks.
7. Return the patch in unified diff format.

Do not claim that the patch works unless validation confirms it.
```

---

# 45. Safety and Reliability

The application must not hallucinate technical results.

Important rules:

* Never claim tests passed unless tests actually ran.
* Never claim a commit introduced a bug without evidence.
* Never fabricate repository information.
* Never fabricate logs.
* Never fabricate interview scores.
* Clearly indicate uncertainty.
* Show confidence for AI-generated conclusions.
* Keep evidence separate from assumptions.

---

# 46. Error Handling

The application should gracefully handle:

```text
AI API failure
GitHub API failure
invalid repository
invalid token
database failure
timeout
rate limit
invalid interview input
malformed AI response
missing logs
test failure
patch failure
```

Example:

```text
Unable to analyze the repository because GitHub authentication
failed. Please reconnect your GitHub account.
```

Avoid exposing raw stack traces to normal users.

---

# 47. API Rate Limits

The system should handle AI and GitHub rate limits.

Implement:

* Error handling
* Retry where appropriate
* Exponential backoff where appropriate
* User-friendly messages
* Request validation
* Reasonable caching where useful

Do not endlessly retry failed requests.

---

# 48. Performance

The MVP should remain lightweight.

Avoid unnecessary dependencies.

Prefer:

* REST APIs
* Background processing where necessary
* Efficient database queries
* Pagination
* Caching where useful
* Lazy loading for large repository data

---

# 49. Testing

Create tests for:

## Authentication

```text
registration
login
invalid credentials
protected routes
```

## Interview

```text
interview creation
question generation
answer submission
evaluation
interview completion
```

## AI

```text
valid response
invalid response
fallback handling
```

## GitHub

```text
repository retrieval
commit retrieval
invalid repository
authentication failure
```

## Investigation

```text
log ingestion
root cause analysis
commit correlation
patch generation
```

---

# 50. Git Workflow

The project should be managed through Git.

Typical workflow:

```bash
git status
git add .
git commit -m "Add AI interview engine"
git push
```

Use meaningful commit messages.

Examples:

```text
Add interview configuration
Implement adaptive questioning
Add answer evaluation
Add interview report
Add GitHub integration
Add commit correlation
Add investigation timeline
Add patch generation
```

---

# 51. Local Development

Create a virtual environment.

Windows Git Bash:

```bash
python -m venv venv
```

Activate:

```bash
source venv/Scripts/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run FastAPI/Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application should be accessible through the local development server.

---

# 52. Requirements File

Example dependencies:

```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
httpx
requests
PyJWT
passlib
bcrypt
```

Only add dependencies that are actually required.

Do not introduce unnecessary heavy frameworks.

---

# 53. Hackathon Priorities

If development time is limited, prioritize features in this order.

## Priority 1 — Must Have

```text
Authentication
Interview setup
AI question generation
Answer submission
Answer evaluation
Adaptive questioning
Interview completion
Final report
```

## Priority 2 — Strong Differentiators

```text
AI Investigation Timeline
Git Commit Correlation
```

## Priority 3 — Advanced

```text
GitHub repository integration
Log ingestion
Root cause analysis
Patch generation
Patch validation
```

## Priority 4 — Optional

```text
Automatic Pull Request creation
Voice interview
Advanced analytics
```

---

# 54. 36-Hour Hackathon MVP Strategy

The application should be optimized for a short hackathon development cycle.

The strongest combination is:

### Core MVP

```text
Log ingestion
GitHub integration
LLM root cause analysis
Patch generation
Optional PR creation
```

### Standout Feature 1

```text
Git Commit Correlation
```

### Standout Feature 2

```text
AI Investigation Timeline
```

These features should make the project visually impressive while remaining technically believable and feasible.

---

# 55. Demo Flow

The final demo should tell a clear story.

## Step 1 — Start Dashboard

Show:

```text
AI Interviewer Dashboard
```

## Step 2 — Configure Interview

Select:

```text
Python
Data Structures
Intermediate
10 Questions
```

## Step 3 — Start Interview

AI asks the first question.

## Step 4 — Answer

Candidate submits an answer.

## Step 5 — AI Evaluation

AI evaluates the answer.

## Step 6 — Adaptive Follow-Up

AI asks a follow-up based on the answer.

## Step 7 — Difficulty Adjustment

Demonstrate adaptive difficulty.

## Step 8 — Finish Interview

Generate final report.

## Step 9 — Show Investigation Timeline

Show how the AI identified strengths/weaknesses over the interview.

## Step 10 — Demonstrate GitHub Investigation

Connect repository.

Show:

```text
Error
↓
Log
↓
Source Code
↓
Commit
↓
Root Cause
↓
Patch
```

## Step 11 — Show Commit Correlation

Example:

```text
Likely introduced by:
a83f91d — Refactor authentication middleware
```

## Step 12 — Show Patch

Display the generated diff.

## Step 13 — Optional PR

Create a Pull Request after user confirmation.

---

# 56. Demo Story

The project should be presented as more than:

> "An AI chatbot that asks interview questions."

The stronger positioning is:

> **An AI-powered technical interviewer that understands candidate responses, adapts the interview dynamically, identifies knowledge gaps, and produces evidence-based performance insights.**

For the engineering investigation component:

> **An AI software investigation assistant that connects logs, source code, Git history, and AI reasoning to identify root causes and generate validated fixes.**

---

# 57. Important UX Principle

Do not overload the candidate with technical internal information during the interview.

The candidate should see:

```text
Question
Progress
Timer
Answer
Feedback
```

The investigation/debugging interface can expose more technical details.

---

# 58. AI Transparency

When showing AI-generated conclusions, distinguish:

```text
Observed Evidence
AI Conclusion
Confidence
Recommended Action
```

Example:

```text
Observed Evidence:
Candidate incorrectly calculated binary-search complexity
in two consecutive questions.

AI Conclusion:
Candidate may need additional practice with logarithmic
complexity.

Confidence:
89%
```

---

# 59. Do Not Expose Chain of Thought

The application must never display hidden model reasoning or private chain-of-thought.

Instead display concise reasoning summaries such as:

```text
Why this conclusion?

The candidate gave incorrect complexity estimates
in two related questions.
```

This provides transparency without exposing private reasoning.

---

# 60. Code Quality Requirements

The generated implementation should:

* Follow clean architecture principles.
* Use meaningful variable names.
* Keep functions focused.
* Avoid duplicated code.
* Validate inputs.
* Handle errors.
* Keep secrets out of source code.
* Use environment variables.
* Use database transactions appropriately.
* Add comments only where useful.
* Avoid unnecessary abstractions.

---

# 61. Final Product Requirements

The completed AI Interviewer should provide a complete flow:

```text
User
 ↓
Login
 ↓
Dashboard
 ↓
Interview Configuration
 ↓
AI Interview
 ↓
Question
 ↓
Candidate Answer
 ↓
AI Evaluation
 ↓
Adaptive Follow-Up
 ↓
Difficulty Adjustment
 ↓
Interview Completion
 ↓
Performance Report
 ↓
Investigation Timeline
```

For the engineering investigation workflow:

```text
Repository / Logs
 ↓
Log Ingestion
 ↓
Error Detection
 ↓
Source Code Analysis
 ↓
Git History Analysis
 ↓
Commit Correlation
 ↓
Root Cause Analysis
 ↓
Patch Generation
 ↓
Patch Validation
 ↓
Optional Pull Request
```

---

# 62. Definition of Done

The project is considered complete when:

* [ ] User can register and log in.
* [ ] User can configure an interview.
* [ ] User can start an interview.
* [ ] AI generates relevant questions.
* [ ] Candidate can submit answers.
* [ ] AI evaluates answers.
* [ ] AI asks contextual follow-ups.
* [ ] Difficulty adapts based on performance.
* [ ] Interview progress is visible.
* [ ] Interview can be completed.
* [ ] Final score is generated.
* [ ] Strengths are generated.
* [ ] Weaknesses are generated.
* [ ] Recommendations are generated.
* [ ] Question-level feedback is available.
* [ ] Investigation timeline is available.
* [ ] GitHub integration works.
* [ ] Commit history can be inspected.
* [ ] Relevant commits can be correlated.
* [ ] Logs can be ingested.
* [ ] Root cause analysis works.
* [ ] AI can generate a proposed patch.
* [ ] Patch can be validated.
* [ ] Optional PR creation works.
* [ ] Authentication is secure.
* [ ] Secrets are stored in environment variables.
* [ ] Errors are handled gracefully.
* [ ] Application runs locally.
* [ ] Git workflow is clean.
* [ ] Demo flow works end-to-end.

---

# 63. Master Instruction for AI Coding Assistant

When implementing this project, follow these rules:

1. Understand the existing codebase before modifying it.
2. Do not rewrite working functionality unnecessarily.
3. Preserve existing APIs unless a change is required.
4. Keep frontend and backend responsibilities separated.
5. Do not hard-code API keys or secrets.
6. Use environment variables for sensitive configuration.
7. Keep the implementation lightweight.
8. Prefer simple, maintainable solutions.
9. Do not introduce unnecessary dependencies.
10. Validate all external API responses.
11. Handle AI failures gracefully.
12. Never fabricate AI, GitHub, log, test, or database results.
13. Never claim tests passed unless they actually passed.
14. Never expose model chain-of-thought.
15. Display concise evidence-based explanations instead.
16. Keep the UI professional and demo-ready.
17. Make the application responsive.
18. Use meaningful error messages.
19. Preserve backward compatibility where possible.
20. Before modifying files, identify exactly which files need to change.
21. After implementation, test the affected functionality.
22. Keep commits focused and descriptive.
23. Do not modify unrelated modules.
24. Do not delete existing functionality unless explicitly requested.
25. Prioritize the MVP before advanced features.

---

# 64. Final Product Vision

The final product should feel like an **AI technical interviewer + AI engineering investigation assistant**, rather than a collection of disconnected AI features.

The central experience should be:

```text
UNDERSTAND
     ↓
INTERVIEW
     ↓
EVALUATE
     ↓
ADAPT
     ↓
IDENTIFY GAPS
     ↓
EXPLAIN
     ↓
INVESTIGATE
     ↓
CORRELATE
     ↓
FIX
```

The application should demonstrate that AI can understand technical conversations, evaluate engineering knowledge, investigate software problems, connect evidence across logs and Git history, and produce actionable results.

The final demo should emphasize:

**AI Interview Intelligence + Evidence-Based Evaluation + Git Commit Correlation + AI Investigation Timeline + Root Cause Analysis + Automated Patch Generation.**
