These prompts were given in chatgpt.

Prompt 1: AI Technical Interviewer — Requirement Gathering

Act as A developer ,
I want u to built Ai technical interviewer with the features that i give
1 st one should be landing page
Next would be the details like recruitment where u give statistics
Then candidate selection
The interview section
Finally the result after completing the interview

The output should looks professional with dark colours and keep it minimal i want a detailed prompt


Prompt 2: Course Learning Page — Feature Requirements

i just need features for course learning page the interviewer checks those pages and then interview the candidate via text in the 4 th slide then the result would be published in  slide so now i want the extra featues that ic ould add in 3 rs slide from top to bottom it should be in 360 px keep it minimalistic and professional


Prompt 3: Interview Result & Feedback Page — Requirements

after  the interview pages comes the last page which shows results and gives feedback.Result page will contain overall score in a pie chart where the pie chart represets mark for each ques then in should generate the feedback based on the 8 questions asked in interview and the project that have completed during the learning phase and also tell where they are best and where they need improvements and also give confidence score based on the above said projects,learning jouney and also provide a downloadable report that contains all the deatils which is the result page and finally complete some heart warming wishes this is my plan for the last page add the features that u want to do so,then give me layout keep this in 390 pixel and i want to tell u that we are doing this for AB talks hakathon this is their requirement to built ai interviewer and we are building that .They have an official website for ab cohort learning the candidates would study in that website and every data would be there in that website u have to use that progress and use those projects and data to give eult  but as of now they have just given curriculum.json file we have to use that data

Prompt 4: Frontend Folder Structure & Project Organization

these are the web pages and i have create ai interviwer in vscode now i need to create a struct for the folder frontend my friend was doing backend and she created backend folder and inserted all the files completed the backend structure now i want u to give me the structure for the frontend

Prompt 5: Dashboard Page — Frontend UI & Interaction Implementation

Hey act as a promp engineer ,i need to copy this prompt and get the frontend code from claude.Give me a complete very detailed prompt that includes all the requirements and animations that i said and i would insert these pictures in claude too.
I am attaching a phtocopy of how exactly the website looks.Use the same colour style font ui for reference i want the website to look in that exact theme .Then the website should be in 390 pixel.please look at the second page for reference i dont want sections like today goal, motivation and continue learning
And i have a sample structure for frontend pushed already in vscode.I am attaching that screenshot here.
I am building the second page the dashboard.there i want the hamburger menu at left and notification bell icon at the right corner at the exact header i want AI Interviewer name.

In that sidebar i want features like
Dashboard
That should bring me to the next 3 pages
Learning journey
AI interview
Results
Settings
Help
Profile
Signout
Introduction/welcome section
And in the home page after header it should aome greeting message like good morning emily
Keep learning, keep building.
Then comes the next section where u should show streaks based on the days using possible animations. Very subtle pulse not aggressive
Then comes the course progress the course progress bar should percentage of completion and how many days has been completed  then the animated progress bar and shows how many completed how many skipped  how many tops completed in first attempt when dashboard opens it should animate from 0/31,5/31,20/31.
And the progress bar fills smoothly

After this comes interview readiness section it shoudl show glowing piechart  and the percentage for 100 and after percentage it should the suggestion like strong/good/week based on the percentage.i//t is dashboard indicator calculated from things such as:
Curriculum progress
Completed modules
Skipped topics//just for understanding no need in ui

At lastQuick Access  it should contain navbar that takes us to the next pages like learning journey,interview,result.
It should be a strong CTA if we start interview click interview then for reultsbinterview results view ur previous performance vlick result learning journey explore your 31 day progress journey click learning journer.

These are the requirements u keep it clean minimal and professional add animation and features where professional


Prompt 6: Mobile App UI Visualization & Page-by-Page Design


ok now i have some clarity about this now i want to visualize how actually it will look like so i will give the theme based on that can u pls display some pages based on our requirements or features use a theme like black and violet (note: i will give the color and bg theme and also font don't change these keep it as it is and also there is Day 1- 31 topics in hierarchical so tell me what features they have used and also if i want to use animations like they were used what features we need to use and how it will b look like.
it is perfectly ok but we have to edit some changes and it is mobile based application so it is page by page and also in result page at bottom i need to download the report
---

These prompt were given in claude.


prompt 6:LOGIN page code PROMPT
Yes, this is an existing React + Vite project.
I don't want a new project or a new folder.
Please work directly inside the existing project and inspect the actual source files before making any changes.
I already have:
Interview page
Results & Feedback page
My friend is working on:
Dashboard
Learning Journey
I only want to ADD the Login page to this existing application.
First inspect:
package.json
src structure
App.jsx
routing setup
existing Interview page
existing Results page
existing theme/styles/components
Then add the Login page using the project's existing conventions.
Do not create:
another React project
another frontend folder
another package.json
another src folder
another node_modules
duplicate App.jsx
duplicate router
Do not overwrite my Interview or Results pages.
Use the existing routing and theme system if one already exists.
The Login page should have:
AI Interviewer
Email
Password
Forgot Password?
Login button
Dark/Light theme toggle
Use the same ABTalks visual style:
black/deep dark background, violet/purple accents, subtle glow, dark cards, rounded corners, soft borders, white text and muted gray text.
Do not introduce a different color palette or redesign the visual style.
Make it mobile-first for 390px with no horizontal scrolling.
For now, use mock login validation. After successful login, navigate to the existing Dashboard route.
No signup, Google login, GitHub login, voice, or audio.
Please modify only the minimum existing files needed and add only the Login-related files required.
Before changing anything, show me which existing files you found and where you plan to add the Login page.


Prompt 7:to get exact code for dashboard page


Act as a senior frontend engineer and UI/UX designer specializing in React dashboards and premium AI SaaS products.
I am building an AI Technical Interviewer for an AB Talks / AI Cohort hackathon.
IMPORTANT:
I ALREADY HAVE A REACT + VITE FRONTEND PROJECT CREATED.
DO NOT create a new React project.
DO NOT initialize Vite.
DO NOT create another frontend folder.
DO NOT change my project architecture unnecessarily.
I already have this frontend structure:
frontend/
│
├── public/
│
├── src/
│   ├── assets/
│   │   └── hero.png
│   │
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── LearningTimeline.jsx
│   │   ├── SkillCoverage.jsx
│   │   └── QuestionCard.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── LearningJourney.jsx
│   │   ├── Interview.jsx
│   │   └── Results.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── package.json
├── package-lock.json
├── vite.config.js
├── eslint.config.js
└── index.html
I am currently building ONLY:
src/pages/Dashboard.jsx
You may modify/create the minimum supporting CSS/component code required for the Dashboard to work properly, but do not unnecessarily restructure my project.
==================================================
PROJECT PURPOSE
==================================================
The application is called:
AI INTERVIEWER
It is an AI-powered technical interviewer designed around a candidate's 31-day AI engineering learning journey.
The candidate studies an AI curriculum containing topics such as:
RAG
Vector Databases
Prompt Engineering
Agentic AI
MCP
AI Deployment
Production AI Systems
The platform uses the candidate's learning progress to prepare them for an adaptive technical interview.
The overall application has these pages:
Login
Dashboard
Learning Journey
AI Interview
Results
I am currently implementing PAGE 2 — DASHBOARD.
==================================================
2. VISUAL REFERENCE
I will attach screenshots/images along with this prompt.
USE THE ATTACHED SCREENSHOTS AS THE PRIMARY VISUAL REFERENCE for:
overall color palette
typography
spacing
card shapes
borders
gradients
glow effects
icon style
visual hierarchy
overall futuristic AI SaaS feeling
The reference design uses:
very dark / near-black background
dark navy surfaces
neon purple primary accent
blue/purple gradients
subtle teal secondary accents
glowing borders
glassmorphism
rounded cards
soft shadows
futuristic AI dashboard aesthetic
clean modern typography
minimal cyberpunk-inspired design
IMPORTANT:
Do NOT blindly copy every section visible in the screenshot.
The screenshots are visual references.
My written requirements below are the exact requirements for this Dashboard.
==================================================
3. RESPONSIVE DESIGN REQUIREMENT
The main target viewport is:
390px wide mobile screen.
Design the Dashboard specifically for:
390px
It should also gracefully work between approximately:
360px — 430px
The layout must NEVER horizontally overflow.
Do not create a desktop sidebar that permanently occupies screen width.
Use a mobile hamburger navigation.
The main content should have comfortable horizontal padding, approximately:
16px
The UI should feel like a polished mobile AI application.
==================================================
4. DASHBOARD HEADER
At the very top create a compact mobile header.
Structure:
┌──────────────────────────────────────┐
│ ☰    AI INTERVIEWER              🔔 │
└──────────────────────────────────────┘
LEFT:
Hamburger menu button.
CENTER/LEFT:
AI INTERVIEWER
RIGHT:
Notification bell icon.
The header should remain clean and minimal.
Use icons rather than text symbols wherever possible.
The hamburger button should have a subtle hover/tap animation.
Notification bell should have a very subtle notification indicator, for example a tiny glowing dot.
Do NOT make the notification animation distracting.
==================================================
5. HAMBURGER MENU / MOBILE SIDEBAR
When the hamburger icon is clicked, open a mobile navigation drawer.
The drawer should slide in smoothly from the left.
Use a dark glassmorphism background.
Example:
┌──────────────────────────────┐
│ AI INTERVIEWER           ✕   │
│                              │
│ 🏠 Dashboard                │
│                              │
│ 📚 Learning Journey          │
│                              │
│ 🎯 AI Interview              │
│                              │
│ 📊 Results                   │
│                              │
│ ───────────────────────────  │
│                              │
│ ⚙ Settings                  │
│ ? Help                       │
│                              │
│ ───────────────────────────  │
│                              │
│ 👤 Profile                  │
│                              │
│ Sign Out                     │
└──────────────────────────────┘
Navigation items:
Dashboard
Learning Journey
AI Interview
Results
Settings
Help
Profile
Sign Out
The following navigation behavior should exist:
Dashboard → Dashboard.jsx
Learning Journey → LearningJourney.jsx
AI Interview → Interview.jsx
Results → Results.jsx
Settings → placeholder interaction for now
Help → placeholder interaction for now
Profile → placeholder interaction for now
Sign Out → placeholder interaction for now
If React Router is already installed, use it.
If React Router is NOT installed, do not install unnecessary dependencies. Use the simplest navigation approach compatible with the current project.
The drawer should include:
slide-in animation
dark overlay behind it
close button
close when clicking outside the drawer
active navigation item
subtle hover/tap animation
==================================================
6. WELCOME / INTRODUCTION SECTION
Immediately below the header:
Good morning, Emily 👋
Keep learning, keep building.
The greeting should feel personalized.
Use:
Good morning, Emily 👋
with a slightly larger font.
Below it:
Keep learning, keep building.
Use a softer muted text color.
Animation:
When the Dashboard loads:
greeting should fade in
subtitle should slightly slide upward
animation should be fast and subtle
Do NOT use dramatic animations.
==================================================
7. PROGRESS / STREAK SECTION
🔥 12
Day Streak
It shouls show daws with filled dots ,based on whether they have complete or not
STREAK ANIMATION
==================================================
The streak should have a very subtle animation.
Example:
🔥 12
The flame can:
gently pulse
slightly scale up/down
have a subtle glow
Do NOT make the flame bounce continuously.
The animation should feel premium and professional.
Suggested behavior:
scale:
1 → 1.05 → 1
slowly.
The glow should also subtly pulse.
==================================================
9. COURSE PROGRESS
Create a Course Progress section.
Title:
COURSE PROGRESS
Show:
20 / 31 days completed
64%
Then:
20 Completed
18 First Attempt
2 Skipped
Use one horizontal progress bar.
The bar should use a purple → blue gradient.
Example:
20 / 31
64%
━━━━━━━━━━━━━━━━━━━━░░░░
The progress bar should have:
rounded edges
gradient fill
subtle glow
smooth animation
==================================================
10. COURSE PROGRESS ANIMATION
IMPORTANT.
Do NOT immediately display:
20 / 31
Instead animate the numbers when the Dashboard loads.
Animation:
0 / 31
↓
5 / 31
↓
10 / 31
↓
15 / 31
↓
20 / 31
At the same time:
0%
↓
16%
↓
32%
↓
48%
↓
64%
The progress bar should smoothly fill from:
0%
to:
64%
Use a smooth easing animation.
The animation should take approximately:
1000–1500ms.
Do not make it excessively slow.
The supporting numbers can also count upward.
Example:
Completed:
0 → 20
First Attempt:
0 → 18
Skipped:
0 → 2
Use a reusable count-up mechanism if appropriate.
==================================================
11. INTERVIEW READINESS
This is one of the most important Dashboard sections.
Create:
INTERVIEW READINESS
Show a glowing circular/pie-style progress visualization.
Example:
       82
     /    \
    |      |
     \    /

82 / 100
INTERVIEW READY
Below it:
Strong foundation across your completed curriculum.
The readiness indicator should visually communicate:
82%
Use a circular progress ring rather than a traditional chart library unless a chart library already exists.
Use:
purple gradient
subtle blue glow
dark center
animated progress ring
==================================================
12. INTERVIEW READINESS STATUS
The status depends on percentage.
Use these states:
0–49:
BUILDING
50–79:
ALMOST READY
80–100:
INTERVIEW READY
For the example candidate:
82%
INTERVIEW READY
The status should be visually clear.
Do not call this:
Interview Score.
It is only:
Interview Readiness.
IMPORTANT:
This readiness value represents a dashboard indicator derived from:
curriculum progress
completed modules
first-attempt success
skipped topics
breadth of topics covered
These calculations do NOT need to be shown in the UI.
For this frontend demo, you can use mock data.
==================================================
13. READINESS ANIMATION
When the section enters the screen:
The circular ring should animate from:
0%
to:
82%
The number should count:
0
↓
20
↓
40
↓
60
↓
82
The ring should progressively fill.
Use:
smooth easing
approximately 1000–1400ms
subtle glow
Do not use flashy spinning animations.
==================================================
14. QUICK ACCESS
At the bottom create:
QUICK ACCESS
This section should allow navigation to the other major pages.
There should be three actions.
---
A. LEARNING JOURNEY
📚
Learning Journey
Explore your 31-day learning progress
→
Clicking this should navigate to:
LearningJourney.jsx
---
B. AI INTERVIEW
🎯
AI Technical Interview
Test your technical understanding
[ Start Interview → ]
This should be the strongest CTA.
Clicking it should navigate to:
Interview.jsx
---
C. RESULTS
📊
Interview Results
View your previous performance
→
Clicking it should navigate to:
Results.jsx
==================================================
15. QUICK ACCESS INTERACTIONS
Each action should feel interactive.
On hover/touch:
card slightly lifts
border becomes brighter
purple glow becomes slightly stronger
arrow moves slightly right
Example:
→
becomes:
→  slightly translated right
Do not make cards shake or bounce.
For the AI Interview CTA:
Use a stronger purple gradient button.
Example:
[ Start AI Interview → ]
It should have:
gradient background
subtle glow
hover brightness
slight arrow movement
==================================================
16. PAGE LOAD ANIMATIONS
The Dashboard should feel polished when first opened.
Use a staggered entrance animation.
Order:
Header fades in
Greeting fades/slides in
Progress card appears
Course progress animates
Interview readiness appears
Quick Access cards appear
Use subtle animations.
Example timing:
Header:
0ms
Greeting:
100ms
Progress:
200ms
Readiness:
350ms
Quick Access:
500ms
Do NOT make the page look like everything is flying around.
The animations should feel like a premium SaaS dashboard.
==================================================
17. SCROLL ANIMATION
The dashboard should be vertically scrollable.
Because this is a 390px mobile screen, do NOT try to fit everything into one screen.
Use:
vertical scrolling
comfortable spacing
sticky header if appropriate
Cards can subtly fade/slide into view as they become visible.
Do not overuse scroll animations.
==================================================
18. DESIGN SYSTEM
Use this visual language throughout.
Background:
near-black navy / black
Example visual direction:
#05050A
#080812
#0B0B16
Primary:
neon purple
Secondary:
electric blue
Accent:
teal
Text:
white / near-white
Secondary text:
muted gray-blue
Borders:
very subtle purple/blue tinted borders
Cards:
dark translucent navy with glass effect.
Use:
backdrop-filter: blur(...)
where appropriate.
==================================================
19. TYPOGRAPHY
Use a clean modern font similar to:
Inter
If Inter is not already available locally, use a clean system fallback:
Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
Typography hierarchy:
Page title:
20–24px
Section titles:
12–14px uppercase with letter spacing
Main metrics:
28–36px
Body:
13–15px
Supporting text:
11–13px
Do not use oversized desktop typography.
==================================================
20. CARDS
Cards should have:
border-radius:
14–18px
Subtle border:
rgba(...)
Soft shadow.
Very subtle neon glow.
Avoid excessive glassmorphism.
The interface should remain readable.
==================================================
21. ICONS
Use clean modern icons.
If an icon library is already installed, use it.
If no icon library is installed, use simple inline SVG icons.
Do NOT add a large dependency only for a few icons unless necessary.
Icons should be:
18–20px.
Use icons for:
hamburger
notification
home
learning
interview
results
settings
help
profile
sign out
arrow
flame
==================================================
22. MOBILE UX
This is extremely important.
Target:
390px
Also test mentally at:
360px
The UI must:
fit without horizontal scrolling
have touch-friendly buttons
have at least approximately 44px tap targets
maintain readable text
avoid tiny controls
keep sufficient spacing
avoid desktop-style multi-column layouts
At 390px:
ONE COLUMN ONLY.
Do not place multiple large cards side-by-side.
==================================================
23. DASHBOARD CONTENT ORDER
The exact vertical order should be:
HEADER
↓
WELCOME
Good morning, Emily 👋
Keep learning, keep building.
↓
YOUR PROGRESS
🔥 12 Day Streak
M t w t f s s
.  .    .   .  .  .  .
20 / 31 Learning Progress
64%
20 Completed
18 First Attempt
2 Skipped
↓
INTERVIEW READINESS
82 / 100
INTERVIEW READY
Circular glowing progress
↓
QUICK ACCESS
Learning Journey
AI Technical Interview
Results
==================================================
24. DO NOT ADD THESE SECTIONS
IMPORTANT.
Do NOT add:
Today's Goal
Today's Motivation
Continue Learning
Recent Activity
Leaderboard
Achievements
Calendar
Chat
Video
Audio
Voice interview
Emotion detection
unnecessary analytics
unnecessary promotional sections
Keep the Dashboard minimal.
==================================================
25. FUNCTIONALITY
The page must actually work.
Hamburger:
opens/closes navigation drawer.
Navigation:
Dashboard
Learning Journey
AI Interview
Results
must navigate to the corresponding pages.
Quick Access buttons must navigate.
The Start AI Interview button must navigate to:
Interview.jsx
Results must navigate to:
Results.jsx
Learning Journey must navigate to:
LearningJourney.jsx
If those pages are currently placeholders, navigation should still work.
==================================================
26. MOCK DATA
For now use mock data inside the Dashboard.
Example:
candidateName = "Emily Chen"
streak = 12
completedDays = 20
totalDays = 31
firstAttempt = 18
skipped = 2
readiness = 82
Do NOT hardcode these values into multiple places.
Create a small data object at the top of the component.
Example conceptually:
const candidate = {
name: "Emily Chen",
streak: 12,
completedDays: 20,
totalDays: 31,
firstAttempt: 18,
skipped: 2,
readiness: 82
};
This will later be replaced by backend API data.
==================================================
27. CODE QUALITY
Write clean React code.
Use functional components.
Use React hooks where appropriate.
Do not create unnecessary complexity.
Keep Dashboard.jsx readable.
If a component should be reusable, you may create a small component.
Possible reusable components:
ProgressBar
ReadinessRing
QuickAction
MobileDrawer
But do not create dozens of files.
Use semantic HTML.
Use accessible buttons.
Add aria-labels to icon-only buttons.
==================================================
28. CSS REQUIREMENTS
Write responsive CSS.
The main dashboard container should behave like:
width: 100%;
max-width: 390px;
But make sure it can still display correctly on a 360px screen.
Do NOT hardcode:
width: 390px;
for every element.
Instead use:
width: 100%;
box-sizing: border-box;
with appropriate padding.
The application itself should adapt to the viewport.
==================================================
29. ANIMATION IMPLEMENTATION
Prefer CSS animations and lightweight React logic.
Required animations:
Page fade-in
Greeting slide/fade
Course progress count-up
Progress bar fill
First-attempt count-up
Skipped count-up
Streak subtle pulse
Interview readiness number count-up
Interview readiness circular ring fill
Quick action entrance
Button hover/tap
Hamburger drawer slide-in
Overlay fade-in
Arrow movement on CTA hover
Keep all animations subtle.
Respect:
prefers-reduced-motion
If the user has reduced motion enabled, minimize/disable non-essential animations.
==================================================
30. PERFORMANCE
Do not use heavy animation libraries unless already installed.
Do not use huge background videos.
Do not use canvas unnecessarily.
Do not use complicated chart libraries for one circular readiness indicator.
Prefer:
CSS
SVG
React hooks
for lightweight animations.
==================================================
31. FINAL VISUAL GOAL
The final Dashboard should feel like:
A premium futuristic AI engineering platform.
Not:
A generic student dashboard.
Not:
A colorful children's dashboard.
Not:
A desktop enterprise admin panel squeezed into mobile.
It should feel:
futuristic
intelligent
minimal
premium
technical
professional
dark
polished
The purple glow should be noticeable but restrained.
==================================================
32. IMPORTANT SCREENSHOT REFERENCE
I am attaching screenshots showing the overall visual style of the complete application.
Use them as visual inspiration.
The dashboard should visually belong to the same product as:
Login
Learning Journey
AI Interview
Results
Maintain consistent:
colors
fonts
border radius
glow
spacing
button style
card style
icons
==================================================
33. WHAT I WANT FROM YOU
Now generate the actual frontend implementation.
I want:
Dashboard.jsx
Any required CSS changes.
Any small reusable component only if genuinely necessary.
Navigation functionality.
Working hamburger drawer.
Working progress animations.
Working readiness ring animation.
Working quick-action buttons.
Fully responsive 360–390px mobile design.
Clean, production-quality React code.
IMPORTANT:
Do NOT generate a new Vite project.
Do NOT generate package.json unless absolutely necessary.
Do NOT create a new folder structure.
Do NOT replace my existing project.
Work with my existing:
frontend/src/
structure.
Before giving the code, briefly explain which existing files you will modify and why.
Then provide the complete code for each file.
Make the code ready to paste directly into my existing VS Code project.
If a dependency is required, first check whether it can be avoided using CSS/SVG/React. Prefer no new dependency.
The final result should closely match the attached visual reference while following all of the written Dashboard requirements above.


Promp 8:learning journey page code prompt

You are an expert React frontend engineer and UI/UX designer.
I am building a mobile-first AI Interviewer web application using React + Vite + React Router.
I already have a working Dashboard page. My friend is separately developing the Interview page and Results page.
YOUR TASK:
Build ONLY the "Learning Journey" page.
Do NOT redesign or rewrite my Dashboard, Interview, Results, Login, or other existing pages.
==================================================
FIRST: INSPECT THE EXISTING PROJECT
==================================================
Before writing any code, inspect my existing project structure and existing files.
The project currently follows this structure:
frontend/
├── public/
│   └── favicon.svg
│
├── src/
│   ├── assets/
│   │   └── hero.png
│   │
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── MobileDrawer.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── LearningTimeline.jsx
│   │   ├── SkillCoverage.jsx
│   │   └── QuestionCard.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── LearningJourney.jsx
│   │   ├── Interview.jsx
│   │   └── Results.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── package.json
├── package-lock.json
├── vite.config.js
└── eslint.config.js
IMPORTANT:
My actual project may have some of these files already and some may be empty.
DO NOT assume files contain code just because they exist.
Inspect the actual files first.
==================================================
2. VERY IMPORTANT: PREVIOUS ERRORS MUST NOT HAPPEN
I previously had these problems:
LearningJourney.jsx was empty.
There was a filename casing mismatch:
Learningjourney.jsx
vs
LearningJourney.jsx
React Router navigation to /learning did not work.
I previously got:
"requested module ... does not provide an export named default"
I previously got:
"Invalid hook call"
Some routes had empty elements such as:
<Route path="/learning" element={} />
My existing Dashboard was working, but navigation to Learning Journey was broken.
DO NOT repeat any of these problems.
Therefore:
The page MUST have a default export.
The filename MUST be exactly:
src/pages/LearningJourney.jsx
Do NOT create:
Learningjourney.jsx
learningjourney.jsx
LearningJourney.js
Use exactly:
LearningJourney.jsx
The component must end with:
export default LearningJourney;
or:
export default function LearningJourney() {
...
}
==================================================
3. ROUTING
I already use React Router.
The route should be:
<Route path="/learning" element={<LearningJourney />} />
The import should be:
import LearningJourney from "./pages/LearningJourney";
DO NOT create another router.
DO NOT create another BrowserRouter.
DO NOT create a second React root.
DO NOT modify React versions.
DO NOT install another version of React.
DO NOT create duplicate React dependencies.
Use the existing React + React DOM + React Router setup.
If App.jsx currently has broken/empty route elements, fix ONLY the minimum required routing issue.
The existing routes should remain conceptually:
/login
/dashboard
/learning
/interview
/results
Do NOT replace the Interview or Results components with placeholders.
==================================================
4. IMPORTANT: PRESERVE MY EXISTING DASHBOARD
My Dashboard page is already designed and working.
DO NOT rewrite Dashboard.jsx.
DO NOT replace its UI.
DO NOT change its layout.
DO NOT change its animations.
DO NOT change its existing components unless absolutely necessary for the Learning Journey route.
The Learning Journey page should visually feel like it belongs to the same application.
==================================================
5. MY EXISTING COMPONENTS
I already have components such as:
Navbar.jsx
MobileDrawer.jsx
ProgressBar.jsx
LearningTimeline.jsx
SkillCoverage.jsx
QuestionCard.jsx
I also have existing styling such as:
Dashboard.css
ReadinessRing.css
MobileDrawer.css
You may reuse existing components where appropriate.
However:
Do not blindly reuse a component if its design doesn't match the Learning Journey page.
If a new component is required, create it cleanly.
Prefer reusable components.
==================================================
6. DESIGN REFERENCES
I am attaching reference images.
Use the images ONLY as visual/UI references.
DO NOT place the screenshots themselves inside the website.
DO NOT use the screenshots as background images.
DO NOT create an <img> tag containing the reference screenshot.
Recreate the UI using HTML, JSX, CSS, SVG, gradients, borders, cards, icons and animations.
The final website must look like a real application rather than a screenshot.
The main visual language should match the attached references:
dark almost-black background
subtle navy undertones
purple/violet primary glow
occasional blue/cyan/green accents
glassmorphism-style cards
thin glowing borders
soft shadows
rounded corners
clean modern typography
minimal futuristic AI dashboard aesthetic
The UI should feel professional and premium.
Avoid making it look like a gaming website.
==================================================
7. MOBILE-FIRST REQUIREMENT
This is extremely important.
The page MUST work beautifully at:
390px width
This is the primary target.
Also make it responsive for:
360px
375px
390px
414px
768px
1024px
1440px
Do NOT design desktop first and simply shrink it.
Design the mobile layout intentionally.
At 390px:
no horizontal scrolling
no clipped cards
no overflowing text
no elements outside viewport
no broken timeline
no buttons extending beyond screen
no microscopic text
no giant cards that waste space
Use responsive CSS.
==================================================
8. PAGE HEADER
At the top of the page create a clean mobile header.
It should contain:
LEFT:
Back arrow
CENTER:
Learning Journey
RIGHT:
Filter icon
The visual hierarchy should resemble the reference image.
Header should be minimal.
Do not make the header unnecessarily tall.
Use a subtle bottom border or very subtle separation.
The back arrow should navigate back to:
/dashboard
The filter icon can be visually present and interactive.
For now, filtering can be a simple UI interaction if no backend exists.
==================================================
9. OVERALL PROGRESS SECTION
Immediately below the header, create the main progress card.
This is one of the most important sections.
The card should contain:
Small label:
Overall Progress
Main title:
31-Day AI Engineering Cohort
Progress percentage:
64%
Progress information:
20 / 31 days completed
Layout should closely resemble the supplied Learning Journey reference.
Example visual hierarchy:
Overall Progress
31-Day AI Engineering Cohort                         64%
[=========================----------]
20 / 31 days completed
The 64% should be visually prominent.
Use the existing application purple gradient.
Suggested gradient direction:
purple → violet → subtle blue
Do not make it too bright.
==================================================
10. PROGRESS ANIMATION
IMPORTANT:
The Dashboard animation in my previous version was TOO FAST.
Do NOT repeat that.
For Learning Journey:
Progress animation should be subtle and professional.
When the page first loads:
progress bar should animate from approximately 0% to 64%
duration around 1400–1800ms
use ease-out
no bouncing
no excessive glow
no rapid flashing
The number should also count from 0 → 64.
The animation should feel like:
smooth
calm
premium
intentional
NOT:
fast
game-like
bouncy
aggressive
Once the animation completes, the progress should remain stable.
Do not continuously animate the progress bar.
==================================================
11. COURSE ROADMAP
Below the progress card:
Heading:
Course Roadmap
Subtle supporting text can be added if useful.
The roadmap is the main feature of this page.
The reference uses a vertical learning path.
Recreate that concept using actual HTML/CSS.
DO NOT use the screenshot.
==================================================
12. ROADMAP CONTENT
The roadmap should initially show approximately 5–6 phase cards.
Do NOT dump all 31 days onto the main screen.
The main roadmap should be visually clean.
Use these core learning topics:
PHASE 1
Env & Tooling
Description:
Local AI stack, Git, Ollama
Progress:
66%
PHASE 2
Data
Description:
Coverage data & structured queries
Progress:
50%
PHASE 3
Embeddings & Vector
Description:
Knowledge base + retrieval
Progress:
75%
PHASE 4
LLM & Prompting
Description:
Prompting, fine-tune basics
Progress:
40%
PHASE 5
App Build
Description:
Streamlit chatbot + FastAPI
PHASE 6
Agentic + MCP
Description:
Tools, agents, MCP servers
You can add additional phases if needed for the expanded curriculum, but the INITIAL collapsed roadmap should remain concise and mobile-friendly.
==================================================
13. ROADMAP CARD DESIGN
Each phase should look like a premium glass card.
Example:
┌────────────────────────────────────┐
│ Phase 1                         01 │
│                                    │
│ ⚙  Env & Tooling                   │
│    Local AI stack, Git, Ollama     │
│                                    │
│ [==================-----]     66%  │
└────────────────────────────────────┘
Use:
dark translucent background
subtle border
rounded corners
soft colored glow
phase number on right
icon on left
title
description
progress bar
percentage
Do not make the borders extremely bright.
==================================================
14. ROADMAP COLOR SYSTEM
Use the application's existing purple theme as the primary color.
However, individual roadmap phases can have subtle accent variations:
Phase 1:
Purple
Phase 2:
Blue
Phase 3:
Teal/Cyan
Phase 4:
Purple/Magenta
Phase 5:
Pink/Purple
Phase 6:
Orange/Amber
The accent should mainly appear in:
node glow
icon border
progress bar
tiny highlights
The overall application must still feel unified.
Do not make every card a completely different color.
==================================================
15. VERTICAL ROADMAP / TIMELINE
This is very important.
The roadmap should visually behave like a journey.
Create a vertical timeline on the left side.
Example:
●
│
●
│
●
│
●
│
●
Each node corresponds to a phase.
The line should be subtle.
The active/current phase node can have:
purple glow
subtle pulse
brighter border
Completed phases can have a filled/glowing node.
Locked/upcoming phases can have a dimmer node.
The cards should connect visually to the timeline.
==================================================
16. ROADMAP ANIMATION
I am attaching a separate animation video as reference.
Use that animation as inspiration for the roadmap behavior.
The reference animation has:
a vertical journey/timeline
glowing circular nodes
cards appearing along the path
subtle movement
phase-by-phase progression
smooth scroll/reveal behavior
Recreate the FEELING of that animation.
DO NOT embed the video.
DO NOT use the video as a website asset.
Build the animation with CSS/React.
Most importantly:
THE ANIMATION MUST BE SLOW AND PROFESSIONAL.
Use something around:
500–800ms for individual card reveals
with staggered delays.
Do NOT make every card fly in rapidly.
Do NOT make the page feel like an advertisement.
Do NOT continuously pulse every element.
Only subtle glow/pulse should be used for the active node.
==================================================
17. SCROLL REVEAL
As the user scrolls down:
roadmap cards can gently:
opacity:
0 → 1
transform:
translateY(20px) → translateY(0)
Use a smooth easing curve.
The animation should trigger once.
Do not repeatedly animate every time the user slightly scrolls up/down.
Use IntersectionObserver if necessary.
Avoid heavy animation libraries unless already installed.
Prefer native React + CSS.
==================================================
18. ROADMAP PROGRESS BARS
Each phase with a known percentage should have a progress bar.
Examples:
Env & Tooling → 66%
Data → 50%
Embeddings & Vector → 75%
LLM & Prompting → 40%
The progress bars should animate gently when their card enters the viewport.
Duration:
approximately 900–1200ms
Use ease-out.
No bounce.
No rapid flashing.
==================================================
19. EXPANDABLE CURRICULUM
After the visible roadmap cards, create a large button:
View Full 31-Day Curriculum →
OR
Expand Curriculum →
Use the visual style from the reference.
This button is important.
When clicked:
expand the complete curriculum.
It should NOT navigate to another page.
Instead, smoothly reveal the detailed 31-day curriculum below.
The button should change to:
Collapse Curriculum ↑
when expanded.
==================================================
20. EXPANDED 31-DAY CURRICULUM
When the curriculum is expanded, show all 31 days.
Each day should have:
Day number
Topic
Status
Progress if applicable
Example:
Day 1
Environment Setup
Completed
Day 2
AI Assistant
Completed
Day 3
First AI Project
Completed
...
Day 18
Agents with Tools
Completed
Day 19
Multi-Agent Systems
Completed
Day 20
AI Deployment
Completed
Day 21
MCP (Model Context Protocol)
In Progress — 20%
Day 22
Advanced MCP
Locked
Day 23
Security Best Practices
Locked
...
Day 31
Capstone Project
Locked
Use a vertical timeline for the detailed curriculum.
Completed:
purple glowing check icon + green/success status
In progress:
purple/blue highlighted card + progress percentage
Locked:
dimmed icon + muted text + lock indicator
==================================================
21. EXPANDED CURRICULUM ANIMATION
When "Expand Curriculum" is clicked:
Do NOT suddenly dump all 31 cards onto the page.
Use a smooth expansion.
Possible approach:
max-height
opacity
transform
or a controlled CSS transition.
The transition should take approximately:
500–700ms
Keep it smooth.
The 31 items themselves can have a subtle stagger, but keep it restrained.
==================================================
22. END OF PAGE
At the very bottom of the Learning Journey page, after the curriculum section, add a primary CTA.
Text:
Start AI Interview →
This is important.
The button should navigate to:
/interview
Use the same visual language as the Dashboard CTA.
Purple gradient background.
Rounded corners.
Subtle glow.
On hover:
slightly brighter
On active:
very small scale-down effect
Do NOT use exaggerated animations.
On mobile:
button should be full-width with appropriate horizontal margins.
==================================================
23. IMPORTANT NAVIGATION BEHAVIOR
The Learning Journey page must be reachable from the Dashboard.
The MobileDrawer already has:
onNavigate("/learning")
Do not remove this.
Make sure:
Dashboard
→ Learning Journey
actually works.
Also:
Learning Journey
→ Back arrow
→ Dashboard
must work.
Learning Journey
→ Start AI Interview
→ /interview
must work.
Do not break:
Dashboard
→ /results
Dashboard
→ /interview
==================================================
24. MOBILE DRAWER
My MobileDrawer currently includes:
Dashboard
Learning Journey
AI Interview
Results
Settings
Help
Profile
Sign Out
Do NOT remove the Learning Journey item.
It already uses:
onNavigate("/learning")
Keep this behavior.
If there is a routing issue, fix the routing rather than removing the navigation item.
==================================================
25. EXISTING NAVBAR
I currently have a Navbar component.
It contains:
AI INTERVIEWER
hamburger menu
profile avatar
Do not duplicate the Navbar unnecessarily.
However, the Learning Journey reference has its own compact page header:
back arrow
Learning Journey
filter icon
For this page, use the appropriate existing navigation architecture while preserving consistency.
Do not create two competing headers.
==================================================
26. ICONS
Use clean modern icons.
If an icon library is already installed, use it.
If no icon library is installed, use simple inline SVG icons.
Do NOT add a huge dependency just for icons.
Avoid emoji icons such as:
📚
🎯
⚙️
inside the main Learning Journey design.
The Learning Journey page should look professional.
==================================================
27. TYPOGRAPHY
Follow the typography style shown in the attached references.
Use:
clean sans-serif
strong heading hierarchy
medium-weight body text
muted secondary text
bright white headings
purple accent text
Avoid excessive uppercase text.
Do not use huge desktop typography on mobile.
==================================================
28. BACKGROUND
The page background should be:
very dark navy/black
not pure white.
Use subtle radial gradients/glows in the background.
Example concept:
black/navy base
with extremely subtle:
purple glow
blue glow
Do not make the entire background purple.
Keep it premium and minimal.
==================================================
29. CARD STYLE
Cards should have approximately:
border-radius:
16–20px
background:
rgba(10, 12, 25, 0.75)
border:
1px solid rgba(...)
backdrop-filter:
blur(...)
shadow:
very subtle
Avoid excessive glassmorphism.
The reference is dark and clean, not overly glossy.
==================================================
30. ACCESSIBILITY
Buttons must have:
aria-label where necessary
Keyboard accessibility
visible focus state
Do not use divs as buttons when a button should be used.
Ensure text contrast is readable.
==================================================
31. PERFORMANCE
Keep the page lightweight.
Do not add:
Three.js
GSAP
Framer Motion
large animation libraries
unless the project already uses them.
CSS animations + React state + IntersectionObserver are enough.
Avoid unnecessary rerenders.
==================================================
32. DO NOT MODIFY MY FRIEND'S PAGES
These files belong to my friend:
Interview.jsx
Results.jsx
DO NOT rewrite their contents.
Do not replace them with dummy components.
Do not create fake Interview or Results pages.
Only ensure routing points to them correctly.
==================================================
33. DO NOT MODIFY DASHBOARD
Dashboard.jsx is already created.
DO NOT regenerate it.
DO NOT replace its design.
DO NOT change its content.
Only make the smallest routing change necessary if /learning navigation requires it.
==================================================
34. FILES TO CREATE/MODIFY
Prefer this implementation:
src/pages/LearningJourney.jsx
src/styles/LearningJourney.css
If reusable components are necessary, you may create:
src/components/LearningRoadmap.jsx
src/components/CurriculumList.jsx
But don't create unnecessary files.
Do not create duplicate components.
==================================================
35. DATA-DRIVEN IMPLEMENTATION
Do not hard-code 31 separate JSX blocks manually.
Create structured arrays such as:
const phases = [
{
id: 1,
title: "Env & Tooling",
description: "Local AI stack, Git, Ollama",
progress: 66,
...
},
...
];
And:
const curriculum = [
{
day: 1,
title: "Environment Setup",
status: "completed"
},
...
];
Then map over them.
This makes the page easy to update later.
==================================================
36. RESPONSIVE ROADMAP
At 390px width:
The timeline should remain visible.
The phase card should occupy most of the remaining width.
Example conceptual layout:
       ●
       │
       │  ┌───────────────────────┐
       │  │ Phase 1          01   │
       │  │ Env & Tooling         │
       │  │ Local AI stack...     │
       │  │ ███████████──  66%    │
       │  └───────────────────────┘
       │
       ●
       │
       │  ┌───────────────────────┐
       │  │ Phase 2          02   │
       │  │ Data                  │
       │  └───────────────────────┘

Do NOT put the cards side-by-side on mobile.
==================================================
37. DESKTOP RESPONSIVENESS
On larger screens, increase the max-width.
For example:
max-width:
1100–1200px
Center the content.
The roadmap can become wider while retaining the vertical journey structure.
Do not make cards unnecessarily huge.
==================================================
38. FILTER BUTTON
The header has a filter icon.
Make it functional enough to demonstrate interaction.
When clicked, show a small filter panel/popover with options such as:
All
Completed
In Progress
Locked
Filtering should affect the detailed curriculum.
If implementing full filtering makes the code unnecessarily complex, keep the UI functional with React state and simple filtering.
==================================================
39. COMPLETED / CURRENT / LOCKED STATES
Use clear visual states.
COMPLETED:
✓
bright
subtle green success indicator
IN PROGRESS:
●
purple glow
visible progress
LOCKED:
🔒 or inline SVG lock
muted
low opacity
Do not use emoji for the actual polished UI if SVG icons are available.
==================================================
40. NO IMAGE AS WEBSITE CONTENT
The attached screenshots are references.
They are NOT assets.
Do not add them to:
src/assets
Do not import them.
Do not use them as backgrounds.
Recreate the UI from scratch.
==================================================
41. IMPORTANT ANIMATION RULE
The page should feel ALIVE but CALM.
Animation hierarchy:
PAGE LOAD:
subtle fade/slide
PROGRESS:
slow count-up
ROADMAP:
gentle reveal
TIMELINE:
subtle node glow
CARDS:
small translateY
BUTTON:
small hover transition
EXPAND:
smooth height/opacity
Avoid:
fast animations
constant movement
large scaling
bouncing
shaking
flashing
excessive glowing
The previous Dashboard animation was too fast.
This Learning Journey page must be noticeably more controlled.
==================================================
42. REDUCED MOTION
Respect:
@media (prefers-reduced-motion: reduce)
Disable or greatly reduce animations.
==================================================
43. CSS QUALITY
Do not put huge amounts of inline CSS inside JSX.
Use:
LearningJourney.css
for the page.
Use clear class names such as:
.learning-page
.learning-header
.learning-progress-card
.learning-progress-bar
.learning-roadmap
.roadmap-node
.roadmap-card
.phase-card
.curriculum-section
.curriculum-item
.start-interview-btn
Avoid generic class names such as:
.container
.card
.box
which could conflict with existing Dashboard styles.
==================================================
44. AVOID GLOBAL CSS BREAKAGE
Do not globally overwrite:
body
button
h1
h2
p
*
unless absolutely necessary.
Scope styles to the Learning Journey page.
If global styles must be changed, explain why.
==================================================
45. ROUTE VALIDATION
After implementation, verify:
npm run dev
Then verify:
http://localhost:5173/learning
Also verify:
http://localhost:5173/dashboard
Make sure Dashboard still works.
Verify:
/interview
/results
are not broken.
==================================================
46. CHECK FOR IMPORT/EXPORT ERRORS
Before finishing, specifically check for:
default export errors
incorrect file casing
incorrect import paths
missing CSS imports
undefined components
missing React imports
invalid JSX
invalid hooks
duplicate React
duplicate BrowserRouter
incorrect Route syntax
The Learning Journey component must be a valid React component.
==================================================
47. DO NOT USE INVALID ROUTE SYNTAX
Never generate this:
<Route path="/learning" element={} />
Correct:
<Route
path="/learning"
element={<LearningJourney />}
/>
==================================================
48. DO NOT CREATE INVALID HOOK USAGE
Hooks such as:
useState
useEffect
useMemo
useRef
must only be used:
inside React components
or inside custom hooks.
Do not call hooks at module level.
==================================================
49. FINAL UI STRUCTURE
The final Learning Journey page should roughly be:
┌─────────────────────────────────────┐
│ ←       Learning Journey       ◇    │
├─────────────────────────────────────┤
│                                     │
│ Overall Progress                    │
│                                     │
│ 31-Day AI Engineering Cohort    64% │
│                                     │
│ ████████████████████──────          │
│                                     │
│ 20 / 31 days completed              │
│                                     │
└─────────────────────────────────────┘

Course Roadmap

        ●
        │
        │  ┌─────────────────────────┐
        │  │ Phase 1             01  │
        │  │ Env & Tooling           │
        │  │ Local AI stack...       │
        │  │ ███████████───     66%  │
        │  └─────────────────────────┘
        │
        ●
        │
        │  ┌─────────────────────────┐
        │  │ Phase 2             02  │
        │  │ Data                    │
        │  │ Coverage data...        │
        │  │ ███████───────     50%  │
        │  └─────────────────────────┘
        │
        ●
        │
        │  Phase 3
        │  Embeddings & Vector
        │
        ●
        │
        │  Phase 4
        │  LLM & Prompting
        │
        ●
        │
        │  Phase 5
        │  App Build
        │
        ●
        │
        │  Phase 6
        │  Agentic + MCP



┌─────────────────────────────────────┐
│      View Full 31-Day Curriculum → │
└─────────────────────────────────────┘

When expanded:
Day 1   Environment Setup          ✓ Completed
Day 2   AI Assistant               ✓ Completed
Day 3   First AI Project           ✓ Completed
...
Day 20  AI Deployment              ✓ Completed
Day 21  MCP                        20% In Progress
Day 22  Advanced MCP               🔒 Locked
...
Day 31  Capstone Project           🔒 Locked

┌─────────────────────────────────────┐
│          Start AI Interview →      │
└─────────────────────────────────────┘
==================================================
50. IMPORTANT VISUAL PRIORITY
The page should NOT look crowded.
Priority order:
Learning Journey header
31-Day AI Engineering Cohort
64% overall progress
Course Roadmap
Phase cards
Expandable curriculum
Start AI Interview CTA
Everything else is secondary.
==================================================
51. FINAL REQUIREMENT
After writing the code:
Tell me exactly which files you created.
Tell me exactly which files you modified.
Clearly state that Dashboard.jsx, Interview.jsx and Results.jsx were preserved.
Show the final LearningJourney route.
Check for syntax/import/export errors.
Make sure the project can run with:
npm run dev
Do NOT give me pseudo-code.
Give me complete working code.
Do NOT leave placeholders such as:
// add your code here
Do NOT leave:
element={}
Do NOT leave empty components.
The final result must be a functioning Learning Journey page integrated into my existing React application.


prompt 9:Edits and alteration code prompt

this is the website i created i have few more modifications to do  the interview readiness in my page does not lood so good it feels pain could u please make the pichart little bigger and make the layout as it was in the refernce image then i also nee to change some animations like in the dashboard page the course progress line and pie chart moves very faster make the progress bar move litle slower give me the code based on our above conversation dont change complete structure and code do only necessary corrections

prompt 10:INTERVIEW SCREEN code prompt

I’m starting my part of the ABTalks AI Interviewer project. I’m handling the interview screen. I’ve attached the UI reference we’re following. Please use it as the main visual reference and keep the same overall look throughout the page. I want this screen to feel like a proper AI technical interview, not like a normal quiz. This is a mobile-first application, so make sure it feels natural at a 390px width. For the theme, keep the same ABTalks style from the reference:
●deep black / near-black background
●violet and purple as the main accent colors
●subtle purple/blue glow effects
●dark glass-style cards
●soft borders
●rounded corners
●white text with muted gray secondary text
●clean modern typography
●premium AI/technology feel Please don't introduce a different color palette or redesign the visual style. The candidate should first see a short introduction before starting. After starting, there should be exactly 8 questions. The candidate should type their answer, submit it, see a short AI evaluation/loading state, and then receive the next question. The questions will eventually come from our backend and should adapt based on the candidate's previous answers and the topics they have already completed in the 31-day ABTalks learning journey. For now, use sensible mock data. The interview is completely text based, so don't add microphone, voice, audio, or speech-to-text features. Please look at the existing project before coding and reuse the current styles/components where possible. Keep the page clean and don't make the mobile screen crowded. Let's build the interview page first.
Edit in code:

1st one is my expecting out but i got the output as 2nd img so refer the 1st imag and make the changes align it in center and and make it professionala nd imressive don't change the color or theme just do as it but it should like 1 img

prompt 11:Result page code prompt.

Now I want to work on the Results & Feedback screen for the same ABTalks AI Interviewer. This page comes immediately after the 8-question interview, so it should feel like a continuation of the interview rather than a completely different page. Please follow the same reference design and keep the exact visual language from the Interview page. For the theme, keep:
●deep black / near-black background
●violet and purple primary accents
●subtle purple/blue glow
●dark glass-style cards
●thin soft borders
●rounded corners
●white primary text
●muted gray secondary text
●clean modern typography
●premium AI/technology aesthetic Keep everything comfortable on a 390px mobile screen. Don't make it look like a compressed desktop page. I want the candidate to first see their overall interview score and a clear indication of how they performed. Then show how they performed across the 8 questions. I also want to connect the interview result back to their ABTalks learning journey, so the candidate can understand how they performed on topics such as RAG, Vector Databases, Agentic AI, etc. After that, show:
●key strengths
●areas that need improvement
●practical next steps The feedback should feel useful and actionable rather than just showing numbers. At the very bottom of the page, add a prominent "Download Full Report" button. This will eventually connect to our backend report generation, so use mock data for now. Please check the existing Interview page before building this so both screens feel like one consistent product. Don't add authentication or voice features. Build the Results page first, and we'll refine the UI after seeing it.