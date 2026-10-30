# 6. App - Desktop

## 6.1 Purpose, scope and out-of-scope

**Purpose.** The desktop web app is the staffroom and office version of DhruvaOne. It carries the same records, approvals and Dhruva assistance as the phone app, with room for tables, split panes, printing and long forms. Every role opens on what needs that person first (a Dhruva-prepared "n THINGS NEED YOU" card), then offers the working screens for the role.

**This half (06a) covers** the desktop shell shared by all roles, and the leadership and academic role modules:

| Code | Module | Sample persona |
|---|---|---|
| OWN | Group Owner | Mr. V.K. Shunglu, DPS Group |
| PRI | Principal (incl. nine-step campus setup) | Ms. Neelam Mehra; Mrs. Kavita Rawat (setup) |
| ADM | Standalone School Admin (+ trustee approvals) | Mrs. Meena Sharma, Saraswati Vidya Niketan |
| ACO | Academic Coordinator | Mrs. Rekha Sinha |
| HOD | Head of Department | Dr. Anjali Desai, Maths |
| EXM | Exam Cell | Mr. Naveen Chopra |
| CNS | Counsellor | Ms. Ritika Bhalla |
| TCH | Teacher (desktop "staffroom" view) | Ms. Neha Arora |

IDs use `DSK-SHL-nnn` for the shell and `DSK-<ROLE>-nnn` for modules. Section 06b continues with HR, Finance, Admissions, Security & IT, Transport and Student desktop views, and continues the numbering of 6.3.

**Out of scope for this half.** Sign-in, OTP and profile model (see Section 3 Identity, IDM); Ask Dhruva engine behaviour (see Section AI); phone and WhatsApp layouts (see MOB and WAB); flag administration (see TFC); the content of the group-wide audit log and retention policy (see XCT). Not in the MVP at all: health, library, inventory/purchase, hostel, CCTV feeds, and teacher observations (decided 11 Oct 2026 as too intrusive; see open question OQ-6a-01).

**Source tags.** `[Design]` cites the matching board (for example "Academic coordinator > Cover"); `[Spec]` is added by this specification and is not drawn in the designs.

## 6.2 Desktop shell requirements (actors and roles inside the shell)

The shell is the frame shared by every role: left sidebar, top header, the "Ask Dhruva" button, count badges, the "Me" tab, the profile switcher, theme, keyboard and accessibility, limits, sessions and print/export.

**Roles using this half:** Group Owner, Principal, School Admin (standalone), Academic Coordinator, HoD, Exam Cell, Counsellor, Teacher. Parents and the Student desktop views are in 06b. A person may hold several profiles under one number (see DSK-SHL-006); the shell shows exactly one at a time.

**DSK-SHL-001 · Must · MVP · flag: ch.desktop_web · [Design]**
The system shall render a left sidebar whose items depend on the active profile's role, with the sidebar order and labels in the table below.
- Acceptance: Given a Principal profile, When the app loads, Then the sidebar shows Today, Attendance, Absence watch, Fee defaulters, Reports, Calendar, Approvals, Notices, Me, in that order.
- Rules: items hidden by a module flag (see TFC) disappear and their data is retained; the active item is highlighted; the sidebar never lists another role's items.

| Role | Sidebar items (badge in brackets where designed) |
|---|---|
| Group Owner | Overview, Onboarding (1), Campuses, Admissions, Reports, Notices, Calendar, Approvals (3) |
| Principal | Today, Attendance, Absence watch (7), Fee defaulters, Reports, Calendar, Approvals (11), Notices, Me (4) |
| Principal, pre-go-live | Campus setup (n%), Home |
| School Admin | Today (8), People (5), Money (3), Admissions (4), School (2), Me (3) |
| Academic Coordinator | Today (5), Cover (24), Progress, Timetable (AI / Draft / tick), Parent queries (4), Me (7) |
| HoD | Today (4), My classes, Reviews (10), My team (4), Progress, Calendar, Me |
| Exam Cell | Today, Question papers, Exam days, Marks and results, CBSE registration, Me |
| Counsellor | Today (5), My students (3), Sessions, Guidance, Me (7) |
| Teacher | Today (8), Inbox (7), Calendar, Timetable; group "My classes": My students, Marks, Attendance, Remedial; group "Prep": Homework, Question papers, Notes for students, Lesson plans; Me (7) |

**DSK-SHL-002 · Must · MVP · flag: ch.desktop_web · [Design]**
The system shall show a top header on every screen with the screen title, the active campus or school name, the date, and the role's primary header actions.
- Acceptance: Given any role, When a screen opens, Then the header shows "Ask Dhruva" at top right, plus the role action: "+ Notice" (Owner, Principal), "+ Notice to teachers" (Coordinator), "+ Note to my team" (HoD), "+ Notice about exams" (Exam cell), "+ Book a session" (Counsellor), "Save and finish later" (Add a campus wizard only).
- Rules: header actions respect the role's send rights (see 6.4); a header action opens the same composer used on the matching screen.

**DSK-SHL-003 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall provide an "Ask Dhruva" button in the header that opens a side panel of answers from the school's records, with the source named under each answer.
- Acceptance: Given the Principal Today screen, When "Ask Dhruva" is pressed, Then a panel opens with four suggested questions and each answer shows two figures and a source line such as "Class registers marked by teachers today".
- Acceptance: Given free text outside the supported scope, When it is sent, Then the panel replies "In the MVP I answer questions about attendance, absence, fees, staff and notices at your school. Try a suggestion below."
- Rules: answers are scoped to the active profile's data (campus, department or own classes); Dhruva never changes a record from the chat; see Section AI for behaviour.

**DSK-SHL-004 · Must · MVP · flag: ai.focus_card · [Design]**
The system shall open each role's Today screen on a single focus card headed "n THINGS NEED YOU · 1 OF n" with a primary action, a "Later ›" button, an "Up next" queue, and "See all n for today · k done".
- Acceptance: Given 6 open items, When the user acts on the first, Then the header becomes "5 THINGS NEED YOU", the item shows a done state, "k done" increases by one and the sidebar badge falls by one.
- Acceptance: Given "Later ›" is pressed, Then the next card shows and nothing is decided; the skipped item stays in "See all".
- Rules: Dhruva orders cards by urgency and deadline; with ai.focus_card off the same items appear as a plain list ordered by due date; the card never repeats an item already on screen.

**DSK-SHL-005 · Must · MVP · flag: core · [Design]**
The system shall show count badges on sidebar items that equal the number of open items for the active profile and update them without a page reload.
- Acceptance: Given Approvals shows 11, When one is approved, Then the badge shows 10 within 2 seconds.
- Rules: a badge of 0 is hidden; badge counts on Today equal the focus-card total; counts never include other profiles (those appear only in the profile switcher bell, DSK-SHL-006).

**DSK-SHL-006 · Must · MVP · flag: mod.profile_switching · [Design]**
The system shall show the active profile chip in the top bar and let a person with several profiles switch between them without signing out, using the "SWITCH PROFILE" list (school and role, with "n new" counts) or Ctrl + K then a school name.
- Acceptance: Given a teacher at Gurugram who is also a parent at Noida, When "Parent · DPS Noida" is chosen, Then menu, colours and data all change and the toast reads "Switched to DPS Noida Sec 132 · Parent".
- Acceptance: Given a staff profile that was locked, When it is chosen, Then a PIN prompt appears ("Unlock your teacher profile") before any data loads.
- Rules: profiles never mix; a staff member's own children never appear in the staff profile (see Section 3 Identity). The bell shows the count of items waiting in the other profiles and an "All alerts" list labelled "<SCHOOL> · <ROLE>".

**DSK-SHL-007 · Must · MVP · flag: core · [Design]**
The system shall provide a "Me" tab for every staff role with Leave, Payslips and Notices tabs, leave balances, "Apply for leave or out on duty", payslip view with "Email to me" and "Download PDF", and notices addressed to the person.
- Acceptance: Given a teacher opens Me, Then balances read for example "Casual 6 of 12, Earned 19 of 30, Sick 9 of 10" and the Notices tab shows an unread count.
- Rules: who approves the leave depends on the role (table in 6.4, rule R-04); payslips come from the payroll run in DhruvaOne (see 06b HR); Me uses flags mod.hr_leave and mod.payroll for the Leave and Payslips tabs; Notices follow mod.notices.

**DSK-SHL-008 · Should · MVP · flag: ch.desktop_web · [Spec]**
The system shall offer a day and night theme that follows the operating system setting by default and can be overridden in a header menu, with tenant brand colours kept on role accents only.
- Acceptance: Given the OS is in dark mode, When the app loads, Then the night theme shows; When the user picks "Light", Then the choice persists per user across sessions.
- Rules: meaning colours stay constant in both themes (teal on track, blue fine, amber watch, red needs attention); text contrast meets 4.5:1.

**DSK-SHL-009 · Must · MVP · flag: ch.desktop_web · [Spec]**
The system shall be operable by keyboard and meet WCAG 2.1 AA for all desktop screens.
- Acceptance: Given any screen, When the user presses Tab, Then focus moves in reading order with a visible ring; every button, chip, table row and drawer is reachable and closable with Enter, Space and Esc.
- Acceptance: Given Reduce Motion is on, Then Dhruva's orb and progress bars show still poses.
- Rules: shortcuts: Ctrl + K opens the profile and screen finder; "?" lists shortcuts; toasts last 2.5 seconds visually but also post to an ARIA live region; charts have a table alternative; colours are never the only signal (labels or icons accompany them).

**DSK-SHL-010 · Must · MVP · flag: ch.desktop_web · [Spec]**
The system shall support evergreen Chrome, Edge, Firefox and Safari (last two major versions) at widths from 1280 px upward, with a read-only degraded layout down to 1024 px.
- Acceptance: Given a 1366 px laptop, Then the sidebar is expanded and the detail pane sits beside lists; Given 1024 px to 1279 px, Then the sidebar collapses to icons and detail panes open as overlays.
- Rules: below 1024 px the app shows a "Use the phone app for this screen" page with the app-store links, except the sign-in and profile pages; no horizontal page scroll at 1280 px.

**DSK-SHL-011 · Must · MVP · flag: idm.web_login · [Design] + [Spec]**
The system shall ask for the staff PIN again after 15 minutes of inactivity on a staff profile in the browser, and end the whole browser session after 8 hours without activity or 24 hours from sign-in.
- Acceptance: Given a staff profile idle for 15 minutes, When the user clicks anything, Then a PIN prompt covers the screen and unsaved drafts are kept in the page; Given 8 idle hours, Then the user returns to the mobile-number sign-in.
- Rules: the 15-minute PIN rule is [Design]; the 8-hour and 24-hour limits are [Spec] and tenant-configurable between 1 and 24 hours (see TFC); a sign-out on the phone ends web sessions too ("Sign out everywhere").

**DSK-SHL-012 · Must · MVP · flag: mod.reports · [Design] + [Spec]**
The system shall provide a common print and export pattern: every printable screen has a "⎙ Print" action that opens a preview dialog, and every table has a download as Excel or PDF.
- Acceptance: Given a draft timetable, When "⎙ Print" is chosen, Then each page carries a DRAFT mark; Given a live document, Then the page shows its status line ("CURRENT · live now") and "Printed <date>".
- Rules: dialog offers "Save as PDF" and "Print n page(s)"; exports use the same records as the screen so "numbers match what you see on screen"; exports of personal data (defaulters, absence lists, payslips) are written to the audit log (see XCT) with user, time and filter.

**DSK-SHL-013 · Must · MVP · flag: core · [Spec]**
The system shall show a toast confirmation of at most one sentence for every one-tap action, naming the person or group affected, and show a clear message with a retry option when an action fails.
- Acceptance: Given the network drops during "Approve", Then the card stays undecided and the message reads "Could not save. Nothing was changed. Try again."
- Rules: actions are idempotent (see Annex); a double click never sends two reminders or two approvals.

## 6.3 Functional requirements: leadership and academics

### Group Owner (OWN)

**DSK-OWN-001 · Must · MVP · flag: mod.group_scorecard · [Design]**
The Owner can open Overview and see the greeting, the decision card, the "Needs attention" campus, four group tiles, the campus table (lowest health first) and "Coming up".
- Acceptance: Given 14 campuses, Then the header reads "DPS Group · 14 campuses · <date>"; tiles read "Campuses on track 12 of 14", "Fees collected · Jul-Sep 92.7%", "New students · 2026-27 3,824", "Onboarding 18 / 112 data sheets imported"; table columns are Campus, Students present, Fees, New students, Enquiries, Walk-ins.
- Rules: a campus needs attention when attendance or fees fall below 90%; health score is one 0-100 figure; new students count only when the admission fee is paid; each row opens the campus drawer (DSK-OWN-004).

**DSK-OWN-002 · Must · MVP · flag: mod.approvals · [Design]**
The Owner can decide approvals one at a time from the Overview card ("Approve", "Later ›", "Up next", "All approvals") or in full on the Approvals page ("Approve", "Decline").
- Acceptance: Given three requests, When "Approve" is pressed, Then the toast reads "Approved · <campus> notified", the counter drops 3 to 2, and the Approvals badge falls; Decline shows "Declined · requester notified" with toast "Declined · a note was sent".
- Rules: kinds shown are fee concession above Rs 25,000, fee refund (policy "Unused full months, minus 10%") and new teaching posts; each card shows requester, supporters, family dues or vacancy facts and the policy line; every decision is logged with user, time and note.

**DSK-OWN-003 · Must · MVP · flag: mod.group_scorecard · [Design]**
The Owner can open Campuses and see the "Campus scorecard", search "Find a campus by name, city or principal", sort by any column, and see Health score, Attendance, Fees, New students, Enquiries and Walk-ins with the legend "Strong / Fine / Watch / Act now".
- Acceptance: Given the table, When a column header is clicked, Then rows re-sort and an arrow shows the order; footnote reads "Attendance: today. Fees: Jul-Sep. New students: 2026-27, admission fee paid. Enquiries and walk-ins: admissions 2027-28."
- Rules: default order is lowest health score first.

**DSK-OWN-004 · Must · MVP · flag: mod.group_scorecard · [Design]**
The Owner can open a campus drawer with KPI tiles, "Admissions 2027-28" (Enquiries, Walk-ins, Forms given), "Needs your attention" action cards, "Attendance · last 8 weeks" bars with a 92% dashed target, a mini calendar, and the buttons "Message <principal first name>" and "Notice to this campus".
- Acceptance: Given attendance 87.7%, Then the card reads "Attendance is 87.7%, below the 92% target" with "Ask for a plan" (result "Plan requested · reply due Mon") and "Plan a visit" ("Visit booked · Tue 13 Oct", principal told); Given fees 84.3%, Then "Remind parents" ("Reminder sent to parents with dues") and "Ask finance to review" appear.
- Rules: a healthy campus shows "Everything is on track. No action needed." with "Plan a visit" and "Mark reviewed"; the owner never edits classroom data here; clicking a bar selects that week.

**DSK-OWN-005 · Must · MVP · flag: mod.group_scorecard · [Design]**
The Owner can open Admissions and see new students for the current session with "Joined by month", "By campus" bars and "Latest admissions".
- Acceptance: Then the page reads "NEW STUDENTS · SESSION 2026-27 3,824. Counted only when the admission fee is received." and has no action buttons.
- Rules: source is admission-fee receipts in the fee ledger matched to the student record; enquiries are separate and appear on Campuses.

**DSK-OWN-006 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The Owner can open Onboarding to track rollout: four stat tiles, the "Rollout plan" table by batch, and a per-campus checklist of "THE 8 DATA SHEETS" with the people block (Staff accounts, Training, Parents).
- Acceptance: Given the pilot has a fee sheet with 12 rows missing dues dates, When "Review rows" is pressed, Then the toast reads "12 rows fixed with the accounts team · fee sheet imported", "Needs a fix" drops to 0 and data sheets rise to 19 / 112.
- Acceptance: "Remind campus" shows "Reminder sent to the campus lead with the template" and the row reads "Reminder sent today"; "Schedule" shows "Training booked: teachers 45 min, accounts 2 hours · invites sent".
- Rules: status labels "Needs a fix", "In progress", "Not started", "Not due yet"; the eight sheets are Students and parents; Staff and leave balances; Classes, sections, subjects; Timetable; Fee structure and dues; Transport routes and stops; Holiday and exam calendar; Monthly salary sheet; staff accounts are created once the staff sheet imports; parent invites wait for the student sheet.

**DSK-OWN-007 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The Owner can add a campus with the six-step wizard opened from "+ Add a campus", as specified in the table, with "Continue" dimmed and a blocker line until each step is valid.
- Acceptance: Given step 1 with no name, Then the blocker reads "Add the name, city and board"; step 2 "Add the principal and onboarding lead with 10-digit mobiles"; step 4 "Upload or 'Send later' each sheet"; step 5 "Pick both training dates"; step 3 is always valid.
- Acceptance: Given "Add campus" on step 6, Then the success page reads "<Campus> is added" with four ticks (Invites sent, Templates sent, Training booked, On the rollout plan) and buttons "Add another campus" and "Open in Onboarding".
- Rules: the left rail steps are clickable at any time; the campus may be added with items missing (review shows "!" on incomplete cards); fee amounts are never copied; the quick-add dialog in the code is not the product path (see OQ-6a-04).

| Step | Fields and functions |
|---|---|
| 1 Campus details | Campus name*, Short name, City*, State (13 listed), Address, Board* (CBSE, ICSE, State board, IB), Affiliation no., UDISE+ code (11 digits), Students (approx.), Classes offered toggles (Nursery-KG, 1-5, 6-8, 9-10, 11-12) |
| 2 Key people | Principal (name, 10-digit mobile required, email optional), Onboarding lead (name, mobile required), Accounts head (optional), toggle "Send login invites on WhatsApp and email when the campus is added" |
| 3 Settings | "Copy settings from" a campus; five items each "Copy" or "Set up later": Grading scheme and report-card format; School timings and periods; Fee heads (names only); Group holiday calendar; Approval limits. Note: "Fee amounts are never copied" |
| 4 Data sheets | "Download all 8 templates" (toast "8 Excel templates downloaded"); per sheet "Upload" (shows "Checking...") or "Send later" (becomes "Undo"); a sheet with problems offers "Fix 6 rows" or "Import the rest" |
| 5 Go-live plan | Rollout batch cards ("Batch 4", "Batch 5", "With the new session"); teacher training (45 min) and accounts training (2 hours) dates; "WhatsApp number for parents" (group or campus number); "Fee payments go to" (campus bank account or group account); timeline strip |
| 6 Review and add | Five summary cards with "Edit"; "Still needed:" list; primary "Add campus" |

**DSK-OWN-008 · Must · MVP · flag: mod.campus_onboarding · [Design] + [Spec]**
The system shall validate every uploaded data sheet for missing parent mobiles, duplicate students and classes that do not exist, and report the result inline with the count of good rows and problem rows.
- Acceptance: Given a student sheet with 1,180 rows of which 6 lack a parent mobile, Then the result reads "1,174 rows fine · 6 rows have parent mobile numbers missing"; "Import the rest" imports 1,174 and sends 6 to the onboarding lead.
- Rules: the checks are [Design]; file limits (10 MB, .xlsx, template version check, rejecting macros) and row-level error export are [Spec]; re-upload replaces the previous version and keeps it for 30 days.

**DSK-OWN-009 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The Owner can save the wizard as a draft with "Save and finish later" and resume it from Onboarding.
- Acceptance: Given a half-filled wizard, When "Save and finish later" is pressed, Then the toast reads "Saved <name> as a draft · pick it up from Onboarding" and the Onboarding button reads "Continue <name> draft"; resuming toasts "Resumed <name> · step N of 6". With nothing entered the toast reads "Nothing to save yet".
- Rules: one draft per owner at a time in the design; drafts expire after 90 days [Spec]; see OQ-6a-04.

**DSK-OWN-010 · Must · MVP · flag: mod.notices · [Design]**
The Owner can send a notice from Notices in "Group" mode (Campuses chips x Who chips: Principals, Teachers, All staff, Parents) or "One-to-one" mode, with "Draft with Dhruva" buttons "Exam arrangements", "Fee collection", "Diwali wishes", channel chips App and WhatsApp, and a history with read bars.
- Acceptance: Given a group notice to "Principals · all 14 campuses", Then the audience line reads "14 people"; Send is labelled "Add who, title and message" until all three are filled; success toasts "Sent to n people"; history shows "Read by n of N · %" growing as people read.
- Rules: Dhruva drafts but the Owner presses Send ("Dhruva drafted it · edit before sending"); picking specific campuses replaces "All 14"; read receipts come from the app and delivery reports from WhatsApp Business; the campus drawer opens Notices pre-filled (one-to-one to the principal, or group to that campus with Principals and Teachers ticked).

**DSK-OWN-011 · Must · MVP · flag: mod.calendar_ptm · [Design]**
The Owner can view the Calendar (month grid, campus filter "All 14 campuses" or one, colour legend Exam, Holiday, PTM, Event, "This month" list) and open it filtered from a campus drawer.
- Acceptance: Given the filter "All 14 campuses", Then group events show with the count of campuses (for example "Parent-teacher meeting · 4 campuses"); month arrows reach at least three months ahead.
- Rules: calendars are seeded at go-live from each campus's Holiday and exam calendar sheet; the desktop design has no add-event button for the Owner (phone does, see OQ-6a-03).

**DSK-OWN-012 · Must · MVP · flag: mod.reports · [Design]**
The Owner can download or email any of ten ready-made reports from Reports through a right-hand panel and manage "Scheduled emails".
- Acceptance: Given "Monthly group summary", When "Email" is chosen with Send to "Me" and "Group CFO" and How often "1st of each month", Then the button reads "Schedule · 1st of each month" and the toast reads "Scheduled · first email 1 Nov, 8 am"; an invalid address shows "Check the email address"; "All 14 principals" counts as 14 people.
- Acceptance: "Stop" on a schedule toasts "Stopped · <report>".
- Rules: panel options Campus, Period (This month, Last month, This term), Format (PDF, Excel), Send to chips (Me, Group CFO, All 14 principals, Group HR head) plus one free address; the ten reports are in the table below; scheduled emails run at 8 am IST and the file is generated at send time from live data [Spec].

| Report | Format |
|---|---|
| Monthly group summary (one-page board pack) | PDF |
| Attendance summary (campus x grade x section, absentees, reasons) | Excel |
| Fee collection and dues ageing (30/60/90 days) | Excel |
| Defaulters with accountant notes (over 60 days) | Excel |
| New admissions 2026-27 (admission fee paid) | Excel |
| Enquiries and walk-ins 2027-28 (with conversion) | Excel |
| Unit test and term results | PDF |
| Enrolment, gender and RTE ("Ready for the UDISE+ return") | Excel |
| Staff strength and leave register | Excel |
| Campus scorecard | PDF |

### Principal (PRI)

**DSK-PRI-001 · Must · MVP · flag: ai.focus_card · [Design]**
The Principal can open Today and see the focus card, four KPI tiles (Students present, Teachers in school, Fees collected, Approvals waiting), "Student attendance by class" bars with a 92% dashed target, "Who is in today" panels, "Absence watch" and "Coming up".
- Acceptance: Given 6 sections have not marked attendance, Then the first card reads "6 sections haven't marked attendance" with "Remind teachers"; pressing it toasts "Reminder sent to 6 class teachers" and the header drops to "5 THINGS NEED YOU".
- Rules: only this campus is shown with the group figure for comparison ("group 94.3%"); clicking a class bar shows its sections with an "All sections" link; the principal sees who is away but does not assign cover (see R-07).

**DSK-PRI-002 · Must · MVP · flag: mod.attendance · [Design]**
The Principal can open Attendance with a Students | Teachers switch, a class x section heat table, totals, "Lowest sections" and teacher presence by department.
- Acceptance: Given Students, Then the legend shows 92% and above, 88-92%, 84-88%, Below 84%, totals read Present, Late, Absent, and each lowest section lists the class teacher's name; Given Teachers, Then each department shows "In today / On leave" with names.
- Rules: clicking a section lists its absentees; staff on approved leave count as on leave, not absent; footnote "Marked by class teachers in the app".

**DSK-PRI-003 · Must · MVP · flag: mod.attendance · [Design]**
The Principal can use Absence watch to list students or teachers missing too much school, measured by Attendance % (below 90, 85, 75) or Days absent (3+, 5+, 8+ in the last 30 school days).
- Acceptance: Given the default 85%, Then the page reads "7 students below 85% · Lowest attendance first" with columns Name, Class, Attendance, Absent (30 days), What we know; "Download this list" toasts "Absence watch list downloaded (Excel)"; "Message parent" toasts "WhatsApp sent to <name>'s parent"; "Ask CT to call" toasts "Class teacher asked to call home today"; for teachers "Message" and "Meet" ("Meeting request sent for Monday, 2 pm").
- Rules: one tap, no confirmation dialog; the default threshold comes from the setup rule (85%, because CBSE requires 75% to sit board exams); "What we know" combines class-teacher notes and Dhruva's pattern finding (ai.at_risk_detection).

**DSK-PRI-004 · Must · MVP · flag: mod.fees · [Design]**
The Principal can open Fee defaulters with four tiles (Collected, Outstanding, Over 90 days, Promised this month), filters by Class and "Overdue for" (Any time, 90+ days, 60-90, 30-60), the family list, and a family drawer.
- Acceptance: Given a filter, Then the list header recomputes "n families · Rs amount" and the button reads "WhatsApp reminder to these n"; pressing it toasts "Fee reminder sent on WhatsApp to 12 families" and each row reads "Reminder sent today".
- Acceptance: In the drawer, "Add" toasts "Note added · accounts can see it", "Invite to meet" toasts "Meeting invite sent to <parent> for Mon 12 Oct, 2 pm", "WhatsApp reminder" toasts "WhatsApp reminder sent to <parent>".
- Rules: statuses are Dispute, Hardship, Promised, On plan, No response; phone numbers are masked (98xxx x4410); a concession above Rs 25,000 cannot be approved here and shows as sent to the group office.

**DSK-PRI-005 · Must · MVP · flag: mod.reports · [Design]**
The Principal can open Reports with Students and Teachers distribution panels and eight ready-made reports, each with "Download" and "Email" and scheduled emails with "Stop".
- Acceptance: Then Students shows enrolled count, Boys/Girls, stage bars (Early, Primary, Middle, Secondary, Senior) and "RTE share by stage" with "Download (UDISE+)"; Teachers shows PRT, TGT, PGT counts, vacancies, a subject table, Students per teacher and Average experience.
- Rules: reports are Attendance register; Absence watch list; Fee collection and dues; Defaulters with accounts notes; Unit test and term results; Enrolment, gender and RTE; Teacher strength; Staff leave register; email and schedule behave as DSK-OWN-012 with recipients limited to campus staff and the group addresses the tenant allows.

**DSK-PRI-006 · Must · MVP · flag: mod.calendar_ptm · [Design]**
The Principal can view the campus Calendar with filters All, Exams, Holidays, PTMs, Events and can add an event with "+ Add".
- Acceptance: Given "Add an event" with name, Type (Exam, Holiday, PTM, Event), Date and the toggle on, When "Add event" is pressed, Then the toast reads "Added to the calendar · parents and staff told"; with the toggle off, "Added to the calendar".
- Rules: only the principal (and roles the tenant grants) can add events; an exam event that overlaps a holiday raises a warning [Spec].

**DSK-PRI-007 · Must · MVP · flag: mod.approvals · [Design]**
The Principal can decide items in Approvals, which share one queue with the Today card, across the kinds in the table below.
- Acceptance: Given "Unit test 3 results and report cards (2,190 students)", When "Approve and publish" is pressed, Then the result reads "2,190 report cards approved · parents and students are told on the app"; "Send back" returns it to the exam cell.
- Acceptance: A decided card becomes a ticked or crossed line with the result message; Decline shows "<label> · note sent".
- Rules: leave over 2 days reaches the principal after the HoD; concessions above Rs 25,000 and new posts go to the owner; teacher notices to parents wait for approval by default; safety cards only need "Noted".

| Kind | Buttons and result |
|---|---|
| Results | "Send back" / "Approve and publish" |
| Staff leave | "Decline" / "Approve" ("Approved · exam cell told about invigilation"); "Ask for details" / "Approve" for sick leave; "Decline" / "Approve if he swaps" for exam-week duty ("Approved on condition · exam cell told to swap his duty"); long leave shows a cover plan ("cover plan goes to the timetable") |
| Payroll | "Ask HR" / "Approve payroll" ("Payroll approved · HR and accounts told · payslips go out on 19 Oct") |
| Safety (information) | "Call transport", "Call security", "Call the parent" / "Noted" ("Noted · in today's safety log") |
| Notice to approve | "Send back" / "Approve and send" ("Sent to 1,980 parents on the app and WhatsApp") |
| Concession (small) | "Decline" / "Approve" ("Approved · fee ledger updated") |

**DSK-PRI-008 · Must · MVP · flag: mod.notices · [Design]**
The Principal can send numbered circulars from Notices to All parents, Classes 9-12, All staff or Teachers, with "Draft with Dhruva" chips ("PTM reminder", "Diwali holiday", "Attendance, Classes 9-12"), App and WhatsApp channels and read bars.
- Acceptance: Given "All parents", Then the count line reads "3,980 parents will get it"; Send reads "Add a title and message" until filled; toast "Sent on the app and WhatsApp".
- Rules: circulars are numbered (Circular 044); history shows "Read by n of N · %"; drafts come from ai.notice_drafts and are never auto-sent.

**DSK-PRI-009 · Must · MVP · flag: mod.hr_leave · [Design]**
The Principal can use Me to apply for leave or out on duty with an "In charge while you are away" choice and see routing text.
- Acceptance: Given leave of 4 days, Then the routing line reads "Goes to Mrs. Kavita Menon, then Mr. Shunglu, because it is more than 3 days."; up to 3 days "Goes to Mrs. Kavita Menon, group HR head. The chairman's office is copied."
- Rules: tabs Leave, Payslips, Notices (group-office notices); see DSK-SHL-007.

**DSK-PRI-010 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The new-campus Principal can complete the nine-step "Campus setup" with a left rail of status (In progress, Done, Needs attention), a "Setup complete n%" bar, a Dhruva tips panel with "NEED A HAND?" contacts, "Back", and "Save and continue" (or "Continue anyway" while a step has an issue).
- Acceptance: Given Welcome, Then tiles show students and staff imported, sections and "7 of 8 data sheets in", "Start setup", and the line "Due before staff training"; progress saves after every step with toast "Saved · pick up where you left off".
- Rules: fields entered by the group (campus, board, affiliation, classes) are locked; "Continue anyway" passes an open issue but "Finish setup" stays blocked until every step is clear; the nine steps are in DSK-PRI-011.

**DSK-PRI-011 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The Principal can confirm how the school runs in nine steps, each with the fields, checks and results in the table below.
- Acceptance: Given step 2 with "Holi and Periodic test 3 fall on the same day", Then "Move PT 3 to Mon 16 Mar" toasts "Periodic test 3 moved to Mon 16 Mar" or "Keep both" clears the alert; Half-yearly and Annual are locked with toast "Half-yearly and annual exams are required by CBSE".
- Acceptance: Given step 3 with a class over its seats, Then the blocker reads "Some classes have more students than seats"; step 4 flags periods over the weekly total ("42 of 40 periods a week · 2 periods too many").
- Acceptance: Given step 9 complete, When "Finish setup" is pressed, Then the toast reads "Setup finished · group office notified" and the page "Your campus is set up" shows next steps (staff logins created, staff training, parent invites, go-live) with "Review setup again" and "Go to my home page".
- Rules: step 6 "Fill with Dhruva's suggestions" toasts "Filled 6 sections · check and change any"; step 7 merging duplicates and confirming RTE students are explicit person actions.

| Step | Time | Choices and checks |
|---|---|---|
| 1 Profile and timings | 4 min | Start 7:40/7:50/8:00; end 1:30/2:20/2:40; periods 7/8/9; length 35/40/45; Saturdays (all off / 2nd and 4th / all working); live strip "Your school day"; optional logo (PNG or SVG, at least 400 px) |
| 2 Session and calendar | 5 | Terms (two or one); assessments; clash alert; calendar list (31 events); tick "I've checked the calendar and it looks right" |
| 3 Classes and sections | 5 | Seats per section 35/40/45; sections per class (− n +); Enrolled and Fill; summary "38 sections · 1,520 seats · 1,180 enrolled" |
| 4 Subjects and periods | 6 | Stage tabs Primary/Middle/Secondary; core subjects locked; optional subjects switchable; third language; weekly period count check |
| 5 Staff and roles | 6 | Vice principal*, Academic coordinator*, Exam in-charge; tag unclear PRT/TGT/PGT posts |
| 6 Class teachers | 4 | Dhruva matches by most periods; manual pick for the rest, free teachers first |
| 7 Students and parents | 4 | Missing parent mobiles ("Ask class teachers" / "Office will fix"); duplicates ("Merge all 3" / "They're different"); "Confirm 41 RTE students"; roll-number rule |
| 8 Rules | 4 | Attendance marking deadline (9:00/9:30/10:00), late cut-off, absent alert timing; Absence watch threshold; teacher notices ("You approve first" / "Send directly"); languages; leave approver |
| 9 Review and finish | 2 | Summary cards with "Edit"; "Still to do:" list; "Finish setup" or "Go to step n" |

**DSK-PRI-012 · Should · MVP · flag: mod.campus_onboarding · [Design]**
The new-campus Principal can see a pre-go-live "Home" showing days to go-live, "Your campus's road to go-live" (Campus setup, Staff training, Parent invites, Go-live) and "Waiting on others" with the onboarding lead's name.
- Acceptance: Given go-live in 144 days, Then the page reads "144 days to go-live"; "After go-live, this page shows" lists the live tabs.
- Rules: after go-live the sidebar switches to the full principal menu.

### Standalone School Admin (ADM)

**DSK-ADM-001 · Must · MVP · flag: ai.focus_card · [Design]**
The Admin can open Today and clear up to eight cards one at a time, with actions in the table below, "Later ›", "Up next" and "See all 8 for today / Hide the full list".
- Acceptance: Given "2 classes have not marked attendance", When "Remind teachers" is pressed, Then the toast reads "Reminder sent to the Class 4-A and 8-B teachers", the header becomes "7 THINGS NEED YOU" and the item reads "Attendance reminders sent · Done".
- Rules: tiles are Students present, Teachers present, October fees in, New enquiries; a card "Who approves what" states "You run the school. No group sits above you." and names the chairperson for the Admin's own leave, salary and fee waivers.

| Card | Action | Result |
|---|---|---|
| Classes not marked | "Remind teachers" | reminder toast |
| Cover needed for 11 periods | "Assign with Dhruva" | "Cover assigned for 11 periods · teachers told on their phones" |
| Leave requests waiting | "Review" | opens People > Leave |
| Families with fees overdue | "Send reminders" | "Reminder sent to 94 families on WhatsApp and SMS" |
| Salary changes to confirm | "Review" | opens Money > Salary |
| Enquiries not called back | "Review" | opens Admissions |
| Notices still drafts | "Open notices" | opens School > Notices |
| Exam duty roster gaps | "Fill the gaps" | "3 duties filled · teachers told" |

**DSK-ADM-002 · Must · MVP · flag: mod.attendance · [Design]**
The Admin can open People > Attendance to see student and teacher attendance and assign cover.
- Acceptance: Given Teachers absent today, Then each row shows reason, periods and "Assign cover" (covered rows read "Covered"); "Remind the 2 teachers" toasts "Reminder sent to the Class 4-A and 8-B teachers"; students are grouped Pre-primary, Class 1 to 3, 4 to 5, 6 to 8, 9 to 10.
- Rules: cover candidates are free teachers (ai.cover_suggestions); assignment is written to School > Timetable "Today's changes" and told on the app.

**DSK-ADM-003 · Must · MVP · flag: mod.hr_leave · [Design]**
The Admin can approve or decline staff leave in People > Leave with one tap per request.
- Acceptance: Given a request, Then the row shows remaining balance, clashes (for example invigilation duties to swap) and free-teacher count; "Approve" toasts "Approved · <name> told", "Decline" toasts "Declined · <name> told"; the Leave badge drops.
- Rules: no confirmation dialog; undo is not offered; sick leave already taken shows "already absent".

**DSK-ADM-004 · Must · MVP · flag: mod.fees · [Design]**
The Admin can use Money > Fees to see collected, pending and reminded counts, a longest-overdue-first list, "Remind" per family and "Remind all 94 families".
- Acceptance: Given "Remind", Then toast "Reminder sent to Mrs. Anita Mehta" and the row reads "Reminded"; "Remind all" toasts "Reminder sent to 94 families on WhatsApp and SMS".
- Rules: the message is a friendly reminder with amount and pay link; fee waivers are not approved here (see DSK-ADM-007).

**DSK-ADM-005 · Must · MVP · flag: mod.payroll · [Design]**
The Admin can use Money > Salary to review "Changes this month" (unpaid leave, new joiner pro-rata, advance recovery) and approve the month after confirming every change.
- Acceptance: Given 3 unconfirmed changes, When approve is pressed, Then the button reads "Confirm the 3 changes first" and the toast the same; after all are confirmed, approval toasts "October salary approved · Mr. R. K. Gupta can see the payroll log".
- Rules: the Admin's own salary is not in her list.

**DSK-ADM-006 · Must · MVP · flag: mod.admissions_crm · [Design]**
The Admin can use Admissions with chips All, New, Visit booked, Form stage, one next-step button per row, and a "Seats left" panel.
- Acceptance: Given a "New" enquiry, When "Book a visit" is pressed, Then toast "<Child>: Visit booked · message sent to the parent"; "Send the form" gives "Form sent on WhatsApp"; "Offer a seat" gives "Seat offered · parent has 3 days to confirm".
- Rules: stages New, Visit booked, Form stage, Seat offered; seats are counted per class out of 40.

**DSK-ADM-007 · Must · MVP · flag: mod.approvals · [Design] + [Spec]**
The system shall route the Admin's own leave, the Admin's own salary and any fee waiver to the trustee (chairperson) and give the trustee a read-only view of the payroll log and refund log only.
- Acceptance: Given the Admin applies for leave, Then the routing line reads "Goes to Mr. R. K. Gupta, chairperson. Mr. Pawan Kumar runs the school day while you are away."; the trustee profile shows only Payroll log, Refund log and an approvals list.
- Rules: the trustee's desktop board is not drawn (see OQ-6a-02); the trustee view, its sign-in and the approvals list are [Spec]; the trustee cannot see any other module (flag mod.trustee_oversight).

**DSK-ADM-008 · Must · MVP · flag: mod.notices · [Design]**
The Admin can use School > Notices, Timetable and Exams: send drafted parent notices ("Send"), see "Today's changes" and "Free teachers, today", and run the Term readiness checklist.
- Acceptance: Given a draft notice, When "Send" is pressed, Then it reads "Sent just now to parents on the app and WhatsApp" and the toast "'Diwali break, 7 to 11 Nov' sent to parents"; the School badge drops.
- Acceptance: Given the roster has gaps, When "Fill the 3 gaps with Dhruva" is pressed, Then toast "3 duties filled · teachers told" and the row reads "Roster complete"; "Remind 3 teachers for marks" toasts "Reminder sent to 3 teachers for Unit Test 2 marks".
- Rules: checklist items are question papers printed and sealed, seating plan, invigilation roster, marks from all teachers; the Admin's Me tab follows DSK-SHL-007.

### Academic Coordinator (ACO)

**DSK-ACO-001 · Must · MVP · flag: ai.focus_card · [Design]**
The Coordinator can open Today and clear the day's cards (Cover, lesson plans, remedial groups, parent queries, timetable) with "Today at a glance" tiles and "Coming up".
- Acceptance: Given "Remind teachers" on lesson plans, Then toast "30 teachers reminded · HoDs copied"; "Create groups" toasts "6 remedial groups created for Saturdays · parents told"; tiles jump to Cover, Progress or Progress > Learning outcomes.
- Rules: the timetable sidebar badge shows "AI" (nothing generated), "Draft" (draft waiting) or a tick (shared).

**DSK-ACO-002 · Must · MVP · flag: mod.cover · [Design]**
The Coordinator can assign substitutes for absent teachers in Cover with a six-column table (Period, Class, Subject, Teacher away, Substitute, Why), a "Teachers away today" list and "Show all 24 periods".
- Acceptance: Given 24 open periods, When "Fill with Dhruva's suggestions" is pressed, Then toast "Dhruva filled 24 periods · check and change any" and the Why column explains each pick ("free · Maths PGT · 1 cover this week").
- Acceptance: Given periods remain, Then "Notify substitutes" is disabled with "Notify unlocks once every period has a teacher · 24 left."; pressed early it toasts "Assign every period first"; when complete the toast is "Substitutes told on the app · class teachers updated" and the button reads "Substitutes notified".
- Rules: candidates are same subject, free that period; Dhruva avoids teachers with 3 or more covers this week; the coordinator can override any pick; absence comes from approved leave.

**DSK-ACO-003 · Must · MVP · flag: mod.pace_tracking · [Design]**
The Coordinator can open Progress > Check-ins and plans to see daily pace check-ins (On plan, Ahead, Behind with reasons), "Why classes fell behind", and lesson-plan submissions by department with "Remind N".
- Acceptance: Given "9 classes lost a period", When "Add catch-up periods" is pressed, Then toast "Catch-up periods added for the week of 2 Nov · teachers told" and the button reads "Done".
- Rules: the coordinator sees the whole school and only chases plans (HoDs review them); the HoD sees the same component for one department.

**DSK-ACO-004 · Must · MVP · flag: mod.marks_results · [Design]**
The Coordinator can open Progress > Learning outcomes with exam pills (Unit test 1, 2, 3, "Term 1 · 30 Oct"), a class x subject heat table, "Show change from Unit test 2" and a risk list "Below 40% in 2+ subjects".
- Acceptance: Given Unit test 3, Then cells are coloured 75%+, 65-75%, 55-65%, below 55%; "✦ Create remedial groups" groups all students on the list for Saturday sessions; per student "Add to remedial".
- Rules: Term 1 appears dashed until results are in; Dhruva's reading names the lowest subjects (ai.at_risk_detection, ai.remedial_grouping).

**DSK-ACO-005 · Must · MVP · flag: ai.timetable_generator · [Design]**
The Coordinator can start a new timetable with "Generate a new timetable" and set the rules in Step 1: Classes (multi-select, default "Whole school · 60 sections"), "Use from" date and six rules.
- Acceptance: Given the class picker, Then a tri-state "Whole school" box, 12 grade rows and chips A to E toggle sections, and the label reads "Whole school · 60 sections", "Class 9-B, 9-C" (up to 4), "10 sections picked" or "Pick one or more classes"; "✦ Generate" with none toasts "Pick the classes first".
- Acceptance: Given "Use from" default Tue 27 Oct, Then the line reads "Until then everyone keeps seeing the current timetable."; "N of 6 rules on" shows the rules: no teacher more than 3 periods in a row; Maths and Science in the first four periods; Science and Computer labs as double periods; Sports and Art after the break; every teacher within the norm (TGT 30, PGT 26); class teachers take period 1 in their own class.
- Rules: with the flag off the Coordinator still edits and approves timetables manually from the current grid (the manual path, see DSK-ACO-007).

**DSK-ACO-006 · Must · MVP · flag: ai.timetable_generator · [Design]**
The system shall generate a private draft and show Step 2 "Review the draft and fix clashes" with a grid, summary chips, clash cards and fix actions.
- Acceptance: Given Generate, Then progress shows four steps ("Reading 60 sections, 193 teachers and 41 rooms", "Placing 2,880 periods for the week", "Checking clashes and your rules", "Balancing teacher load") and then the grid titled "Class 9-B · 10 of 46 periods changed" with chip "Draft · 3 clashes", "Draft · ready to approve" or "Approved and shared".
- Acceptance: Given the draft, Then a banner reads "DRAFT: Only you can see this. Teachers and parents keep seeing the current timetable until you approve and share it."; chips show clashes, teachers over the norm, rules met (for example "6/6 rules met") and "74% periods unchanged"; dashed outline = changed, red = clash, teal = resolved.
- Acceptance: Given clashes, Then each card shows kind, title, "Suggested fix", and "Show", "Apply", "Other options" (two alternatives), and after applying a green line with "Undo"; "✦ Apply all N suggested fixes" toasts "Applied the suggested fix to every open clash".
- Rules: hard conflicts are a teacher in two places, a room double-booked and a teacher on approved leave; soft rules may be bent and are disclosed; "Change rules" returns to Step 1; "Save draft and close" toasts "Draft saved · only you can see it"; the draft survives sign-out [Spec].

**DSK-ACO-007 · Must · MVP · flag: mod.timetable · [Design]**
The Coordinator can view the current timetable by class or by teacher with a picker, see "Who teaches what", and print it.
- Acceptance: Given "By teacher", Then each cell shows class and subject and the block reads "<Teacher> teaches" with periods per week; the grid shows the "Live" chip and period times (P1 8:00 to P8 1:00, break after P4).
- Rules: teachers and parents see only approved timetables on or after the start date.

**DSK-ACO-008 · Must · MVP · flag: ai.timetable_generator · [Design]**
The Coordinator can approve and share per class (one, some or all) in Step 3 "Approve and share this timetable".
- Acceptance: Given the dialog, Then "Approve for" offers "This class · 9-B", "Choose classes" (only unapproved classes) and "All remaining · N" with a live line ("8 classes are ready: ... 9-B, 10-C have open clashes and stay in draft."); "Live from" defaults to the start date; "Share on the app with" lists Teachers (193), Heads of department (11, with the clash report), Parents (2,140 families, app and WhatsApp), Students (Classes 9 to 12), all ticked.
- Acceptance: Given confirm, Then toast "Approved N class(es) · shared with 4 groups · live from Tue 27 Oct"; with none ticked "Pick who to share it with"; with nothing ready the button reads "Nothing ready to approve" and the toast "No class is ready yet. Resolve the open clashes first."
- Rules: a class with an open clash is never approved; once approved it cannot be edited without a new version; the old timetable stays live until the start date; the parent message is "DPS Gurugram: the new timetable starts Tue 27 Oct. Open Timetable in the app to see every period and who teaches it."

**DSK-ACO-009 · Must · MVP · flag: mod.timetable · [Design]**
The Coordinator can withdraw an approved timetable and make another version.
- Acceptance: Given "X of Y classes approved and shared", When "Withdraw all" is pressed, Then toast "Withdrawn · all classes back to draft"; in the Shared state "Withdraw" toasts "Withdrawn · back to draft · the app still shows the old timetable" and "Make another version" returns to Step 1.
- Rules: a withdrawn class returns to draft; the Shared state banner reads "SHARED: Approved by you and sent to teachers and parents on the app. It goes live on the start date."

**DSK-ACO-010 · Must · MVP · flag: mod.timetable · [Design]**
The Coordinator can print any timetable state with the "Print timetable" dialog.
- Acceptance: Given a draft, Then the note reads "This is a draft. Every page is marked DRAFT so nobody mistakes it for the live timetable." and the preview shows a DRAFT watermark; What to print: "This class", "One teacher", "Every class" (60 pages), "Master sheet" (2 pages); Include: teacher names, signature line; Colour or Black and white; A4 or A3 landscape; "Save as PDF" toasts "Saved as PDF · timetable.pdf".
- Rules: header "DPS Gurugram · Sector 45, Weekly timetable · 2026-27", status line "CURRENT · live now", "DRAFT · not shared" or "APPROVED · from Tue 27 Oct".

**DSK-ACO-011 · Must · MVP · flag: mod.parent_messaging · [Design]**
The Coordinator can answer parent queries in Parent queries with "✦ Draft a reply with Dhruva", an editable box and "Send reply".
- Acceptance: Given an open query, When "Draft a reply" is pressed, Then toast "Dhruva drafted a reply · edit before sending"; "Send reply" is greyed until there is a draft and then toasts "Reply sent to Mrs. Ritu Arora on the app" and the list tag reads "Replied".
- Rules: the class teacher is copied; a human always sends (ai.reply_drafts).

**DSK-ACO-012 · Must · MVP · flag: mod.hr_leave · [Design]**
The Coordinator can use Me (Leave, Payslips, Notices) and name an in-charge person.
- Acceptance: Then the form routing reads "Goes to Ms. Neelam Mehra, principal. Your in-charge handles cover and exam queries while you are away."; Out on duty "No leave is used; cover for your work is arranged as for leave."
- Rules: see DSK-SHL-007.

### Head of Department (HOD)

**DSK-HOD-001 · Must · MVP · flag: ai.focus_card · [Design]**
The HoD can open Today with the decision card ("1 OF 3 · 14 DECISIONS"), four tiles (Leave to review, Papers to review, Lesson plans in, results), "Your team today" and the meeting agenda, and send a note with "+ Note to my team".
- Acceptance: Given the note composer, When sent, Then toast "Note sent to all 18 Maths teachers · it appears in their Inbox under 'From your HoD'".
- Rules: tiles jump to Team leave, Papers, Lesson plans and Progress > Results; the HoD sees only whether cover is needed.

**DSK-HOD-002 · Must · MVP · flag: mod.timetable · [Design]**
The HoD can open My classes to use the same tools as any teacher for their own sections, with "NEXT" period card, day strip and "4 things for your own classes".
- Acceptance: Then entries open attendance, homework check, own lesson plan ("reviewed by Mrs. Sinha, you are the HoD") and inbox.
- Rules: the HoD's own plan is reviewed by the coordinator, never by herself; behaviour is as DSK-TCH-002 to DSK-TCH-012.

**DSK-HOD-003 · Must · MVP · flag: mod.lesson_plans · [Design]**
The HoD can review lesson plans in Reviews > Lesson plans, grouped To review, Late, Not submitted, Reviewed, and open a plan detail with objectives, daily activities, resources, assessment and "Quick feedback" chips.
- Acceptance: Given a plan, When "Approve plan" is pressed, Then the row reads "Reviewed", the tab count drops, toast "Plan approved · Mr. Sanjeev Khanna told"; "Send back with feedback" toasts "Sent to <name>: '<chip text>'".
- Rules: chips are "Add a competency-based question", "Too much for 6 periods", "Add support for weaker students", "Good plan, go ahead"; "Remind all 5" toasts "Reminders sent · each teacher sees 'Lesson plan for 19-23 Oct' on Today"; approved plans go to the coordinator's tracker.

**DSK-HOD-004 · Must · MVP · flag: mod.exams · [Design]**
The HoD can review question papers in Reviews > Question papers with "Read the paper" and "Blueprint check" views, per-question "Comment" chips, and actions to send back or approve.
- Acceptance: Given a paper, Then Dhruva shows "Dhruva marked 2 questions for you to look at" (or "Dhruva found nothing to flag"); the blueprint view compares planned and set marks per chapter and the difficulty split; "Approve · send to exam cell" moves the stage to "With exam cell"; "Send back to setter" toasts "Sent back to <setter> with your note · due Sat 10 Oct, 12 pm".
- Rules: comment chips are "Too long for the marks", "Wording unclear", "Repeated from a past paper", "Swap for another chapter"; "✦ Draft a note from the flags and comments" toasts "Note drafted from the checks and your comments"; the PDF is watermarked "HoD review copy"; a paper cannot reach printing without HoD approval.

**DSK-HOD-005 · Must · MVP · flag: mod.hr_leave · [Design]**
The HoD can decide team leave in My team > Leave with Dhruva's suggestion on each request: "Approve", "Send to principal", "Decline".
- Acceptance: Given a 1-day casual request outside exam weeks, When "Approve" is pressed, Then toast "Approved · Ms. Neha Arora and the coordinator told"; a 5-day request offers "Send to principal" with a Dhruva-drafted cover plan ("Sent to Ms. Neelam Mehra with your recommendation and the cover plan", chip "With principal").
- Rules: the HoD approves up to 2 days outside exam weeks; longer leave or leave in exam week goes to the principal; approved leave goes to the coordinator for cover and to HR for the leave register.

**DSK-HOD-006 · Must · MVP · flag: mod.pace_tracking · [Design]**
The HoD can see the team in My team > Team (stat tiles, "Needs you", "Behind on syllabus", "All good") and open a teacher detail with load, plan status, pace and homework, "Send a note" and "Remind about plan".
- Acceptance: Given a teacher, When "Remind about plan" is pressed, Then toast "Reminder sent to <name> · shows on her Today in the teacher app"; "Send a note" toasts "Note sent · it appears in <teacher>'s Inbox in the teacher app" and adds a HISTORY line.
- Rules: "Book a class observation" appears in the design but conflicts with the 11 Oct decision; it is not built (see OQ-6a-01).

**DSK-HOD-007 · Should · MVP · flag: mod.calendar_ptm · [Design]**
The HoD can run Meetings: agenda for the next department meeting ("Add", "Send agenda to the team"), "Actions from" earlier meetings, and "Resource requests" with "New request" sent to the coordinator.
- Acceptance: Then "Send agenda to the team" toasts "Agenda sent to 18 Maths teachers"; a request toasts "Request sent to Mrs. Rekha Sinha".
- Rules: meetings and resource requests are desktop-only.

**DSK-HOD-008 · Must · MVP · flag: mod.pace_tracking · [Design]**
The HoD can open Progress with sub-tabs Syllabus, Check-ins, Results and Homework for the department.
- Acceptance: Syllabus shows sections coloured "On plan or ahead 92-98%", "85-92%", "Below 85%" with a chapter list per section and "Message teacher" and "Plan catch-up periods" / "Mark as on track"; Check-ins shows On plan, Ahead, Behind and "Not checked in yet" with "Remind 4 teachers" and "Ask Mrs. Sinha"; Results shows averages against the school target, "Weakest topics" with "Plan a revision week for these topics", and "Add all to remedial"; Homework shows turnaround days and % returned in 3 days with "Add to Thursday's meeting".
- Rules: the HoD sees only the own department; the coordinator sees the whole school.

**DSK-HOD-009 · Should · MVP · flag: mod.calendar_ptm · [Design]**
The HoD can view the department Calendar by "Month" or "Whole year" with filters All, Department, Exams, Holidays, PTMs, Events.
- Acceptance: Whole year shows "Session 2026-27 · 46 dates · tap a month" with twelve month cards.
- Rules: read-only apart from department meetings.

**DSK-HOD-010 · Must · MVP · flag: mod.hr_leave · [Design]**
The HoD can use Me; own leave routes to the vice principal.
- Acceptance: Then routing reads "Goes to Mr. Rajiv Bhatia, vice principal."; over 2 days "Goes to Mr. Rajiv Bhatia, then Ms. Neelam Mehra, because it is more than 2 days."
- Rules: see DSK-SHL-007.

### Exam Cell (EXM)

**DSK-EXM-001 · Must · MVP · flag: ai.focus_card · [Design]**
The Exam cell can open Today with the focus card and "Term 1 at a glance" tiles (Exams start, Papers sealed, Seating plan, CBSE records).
- Acceptance: Given "Moderate with Dhruva", Then the toast reads "7 papers sent to print · 2 sent back with Dhruva's notes"; "Remind setters" toasts "Setters and HoDs reminded"; "Seal and log" toasts "18 papers sealed · strongroom log updated"; "Remind teachers" toasts "6 teachers reminded on the app · due Mon 12 Oct".
- Rules: tiles jump to the matching tab; "+ Notice about exams" opens the notice composer.

**DSK-EXM-002 · Must · MVP · flag: mod.exams · [Design]**
The Exam cell can track papers through the pipeline "Teacher sets → HoD reviews → you moderate → printed and sealed in the strongroom" using five stage chips (Not set yet, With HoD, Moderation · exam cell, Approved · printing, Printed and sealed) that filter the list.
- Acceptance: Given a paper in moderation, When "Clear for print" is pressed, Then toast "Class 8 English cleared · printing" and counts update (9 to 8, 0 to 1); bulk "Clear all for print (9)" is disabled when none are in moderation.
- Rules: stage order is fixed; nothing is printed until the exam cell clears it; per-row actions are "Remind setter", "Nudge HoD", "Clear for print", "Mark printed"; opening a row shows the paper reader and blueprint check as in DSK-HOD-004; the date-sheet grid is coloured by paper status.

**DSK-EXM-003 · Must · MVP · flag: mod.exams · [Design] + [Spec]**
The Exam cell can log printed papers into the strongroom with "Seal and log".
- Acceptance: Given 18 printed papers, When "Seal and log" is pressed, Then each is marked sealed with user and time and the toast reads "18 papers sealed · strongroom log updated".
- Rules: the log entry is append-only and exportable [Spec]; the sealed count feeds the Today tile.

**DSK-EXM-004 · Must · MVP · flag: ai.exam_planning · [Design]**
The Exam cell can generate seating and invigilation with "✦ Generate seating and duties", view rooms, seating charts and the duty roster, and print door lists.
- Acceptance: Given Term 1, Then summary tiles read for example "2,190 students seated", "42 rooms · 2 classes each", "84 invigilators a day", "3-4 duties per teacher in the week"; a room opens a chart where two classes alternate seats in roll order; "Print door lists and seating charts" toasts "42 door lists and seating charts ready to print (PDF)".
- Rules: never two same-paper neighbours; no teacher invigilates their own subject or a day they have a paper; with the flag off the exam cell builds rooms and rosters manually.

**DSK-EXM-005 · Must · MVP · flag: mod.exams · [Design]**
The Exam cell can fill invigilation gaps caused by approved leave with a picker "Pick an invigilator..." or "Fill with Dhruva".
- Acceptance: Given 2 gaps, Then each offers two teachers with "no paper that day" and duty counts; "Fill with Dhruva" toasts "Ms. Sonia Kapoor and Mr. Vivek Batra assigned · told on the app".
- Rules: swaps requested through the coordinator are applied here (see R-07).

**DSK-EXM-006 · Must · MVP · flag: ai.exam_planning · [Design]**
The Exam cell can draft and publish a date sheet in Exam days > Date sheets: choose exam and window, five rules, "✦ Draft", then "Change rules" or "Publish date sheet".
- Acceptance: Given Unit test 4, Then tiles show "0 clashes with the calendar", "35 papers placed", "5 / 5 rules met", "86 invigilators a day (max)"; publishing toasts "Unit test 4 date sheet published · teachers, students and parents told" and setters get deadlines automatically.
- Rules: rules are skip holidays and events; one paper a day per class; Maths never on the first day; Maths and Science not back-to-back; same subject on the same day across a stage; Classes 1-5 class tests are set by class teachers outside this date sheet.

**DSK-EXM-007 · Must · MVP · flag: mod.marks_results · [Design]**
The Exam cell can monitor marks entry and checks in Marks and results: exam pills, a class x subject grid of % sections entered, "Not entered yet", "Remind teachers", and "Dhruva checked the marks" with per-check "Check" and "Send to <teacher>".
- Acceptance: Given 6 sections pending, When "Remind teachers" is pressed, Then toast "6 teachers reminded on the app · due Mon 12 Oct" and chips read "Reminded"; checks cover marks over the maximum, absent students with marks and section averages falling by an unusual amount.
- Rules: marks cannot be compiled while sections or checks are open.

**DSK-EXM-008 · Must · MVP · flag: mod.report_cards · [Design]**
The Exam cell can compile results and CBSE report cards and send them to the principal for approval.
- Acceptance: Given everything clear, When "Compile results and report cards" is pressed, Then toast "2,190 report cards compiled · ranks and grades worked out", then "Sent to Ms. Neelam Mehra for approval before parents see them"; while open items remain the toast is "Clear the pending sections and checks first".
- Rules: parents and students see report cards only after principal approval; compile is repeatable until approval.

**DSK-EXM-009 · Must · MVP · flag: mod.cbse_registration · [Design]**
The Exam cell can prepare CBSE registration for Classes 10 and 12: progress "Records ready 618 / 640", issue cards (Name differs, Date of birth differs, Subject code missing, Photo missing or blurred), "Apply Dhruva's 14 fixes", "Ask 8 parents on WhatsApp" and "Export when all records are ready".
- Acceptance: Given Apply, Then toast "14 records corrected from admission and timetable data" and counts rise; "Ask parents" toasts "8 parents asked on WhatsApp · Dhruva updates the records as they reply"; Export is disabled until clear and then toasts "CBSE registration file exported · upload it on the CBSE portal".
- Rules: the export is a file for the CBSE portal (no portal integration); corrections from existing data are applied only after the exam cell presses Apply; fee-paid count shows beside the deadline.

**DSK-EXM-010 · Must · MVP · flag: mod.hr_leave · [Design]**
The Exam cell can use Me; routing reads "Goes to Ms. Neelam Mehra, principal. Leave in exam weeks is usually declined unless urgent."
- Acceptance: Then the in-charge list names the deputy and a cell member.
- Rules: see DSK-SHL-007.

### Counsellor (CNS)

**DSK-CNS-001 · Must · MVP · flag: mod.counselling · [Design]**
The Counsellor can open Today with the focus card, four tiles (New referrals, Sessions today, Ongoing students, Interest surveys), "Today's sessions" and "Free today", with every screen carrying "Session notes are private to you. Teachers and parents only see what you choose to share."
- Acceptance: Given "Book first sessions", Then toast "3 first sessions booked in free periods · students told privately"; "Remind students" toasts "62 students reminded on the app"; "Send invites" toasts "Invite sent to 1,280 parents on WhatsApp".
- Rules: nothing is announced to the class or teachers.

**DSK-CNS-002 · Must · MVP · flag: mod.counselling · [Design]**
The Counsellor can manage My students in segments Referrals, Ongoing and Check-ins with a student detail panel (reason, referrer, context, "DHRUVA SUGGESTS", next session, "CASE HISTORY · ONLY YOU CAN SEE IT").
- Acceptance: Given a free slot chosen, Then toast "Session booked today at 10:05 · Aditya Rawat told privately" and status "First session booked"; "Meet parent" offers slots and toasts "Parent of <name> invited for <slot> · you can add the counsellor note afterwards"; "Message parent" toasts "Message to <name>'s parent drafted · you review before it goes"; "Close case" toasts "Case closed · you can reopen it any time".
- Rules: parents are told only after the first session unless the counsellor chooses otherwise; case history is visible to the counsellor only.

**DSK-CNS-003 · Must · MVP · flag: ai.at_risk_detection · [Design]**
The Counsellor can review Dhruva's check-in suggestions and decide with "Not now" or "Book check-in".
- Acceptance: Given a suggestion, When "Book check-in" is pressed, Then toast "Quiet check-in booked with <name> for Monday" and chip "✓ Check-in booked · Mon"; "Not now" shows "✓ Not needed for now".
- Rules: Dhruva watches attendance, marks and teacher notes but only suggests; students are never contacted without the counsellor's tap.

**DSK-CNS-004 · Must · MVP · flag: mod.counselling · [Design]**
The Counsellor can run Sessions with the day's timeline, "Free periods today", and "Write note" with tag pills, "✦ Draft the note" and "Save privately".
- Acceptance: Given selected tags, When "✦ Draft the note" is pressed, Then toast "Dhruva drafted a private note from your tags" and an editable text appears; "Save privately" toasts "Note saved · only you can see it" and the Today card counts down to "Today's notes written".
- Rules: tags include "Calmer than last time", "Sleeping better", "Practised breathing", "Worried about pre-boards", "Talked to parents", "Next: mock-test plan"; default wording is "Nothing to share with teachers"; group sessions are supported; students can request sessions privately from their app.

**DSK-CNS-005 · Should · MVP · flag: mod.counselling · [Design]**
The Counsellor can use Guidance > Career guidance: Class 10 stream choice (survey progress, stream split) and Class 12 plans after school (CUET, JEE Main, NEET, abroad), and press "Share stream reports with parents".
- Acceptance: Given 268 reports, When shared, Then toast "268 stream reports shared with parents · Dhruva added a note for each" and the button reads "✓ Reports shared with parents".
- Rules: stream suggestions are advisory; reports reach parents only on the counsellor's press; exam dates are indicative.

**DSK-CNS-006 · Should · MVP · flag: mod.counselling · [Design]**
The Counsellor can run Guidance > Programmes (workshops) and press "Invite parents".
- Acceptance: Then toast "Invites sent for '<name>'" or "Invite sent to 1,280 parents on WhatsApp"; programmes show registrations and a status (Planned, Registrations open, Parents invited).
- Rules: Dhruva writes the invite; the counsellor sends.

**DSK-CNS-007 · Must · MVP · flag: mod.hr_leave · [Design]**
The Counsellor can use Me; routing reads "Goes to Ms. Neelam Mehra, principal. Your booked sessions are moved and students are told privately."
- Acceptance: Then the in-charge list offers the special educator and the coordinator.
- Rules: see DSK-SHL-007.

### Teacher (TCH)

**DSK-TCH-001 · Must · MVP · flag: ai.focus_card · [Design]**
The Teacher can open Today with the top-three task card, the dark "NEXT" period card with a period strip, the "End-of-day check · 20 seconds" and "Your day".
- Acceptance: Given "1 OF 3 · 8 THINGS TODAY", When "Later ›" is pressed, Then the next task shows; "See all 8 for today · 0 done" expands the list; completed tasks show a done state ("Attendance marked · 10-C · 35 present · 3 absent · parents told").
- Rules: the period card's action changes with the period (Take attendance, Open today's lesson, Snap marks, Share revision notes, Open the cover worksheet); the card avoids repeating the period's task; with nothing pending it reads "All done for today".

**DSK-TCH-002 · Must · MVP · flag: mod.attendance · [Design]**
The Teacher can mark attendance with everyone present by default, parents' notes pre-marked, tap-to-mark-absent, and "Submit · n present, n absent".
- Acceptance: Given 38 students and 2 pre-marked, Then the counter reads "36 Present · 2 Absent"; tapping another name updates to "Submit · 35 present, 3 absent"; submit toasts "Attendance saved · parents of 3 absent students told on WhatsApp" and the screen reads "✓ Submitted at 8:04".
- Rules: a repeat absence shows "<Name> is absent again (5 of the last 7 days). Dhruva will tell Mrs. Sinha and suggest a call to his parents."; corrections after submit follow the campus rule (see R-09).

**DSK-TCH-003 · Must · MVP · flag: mod.marks_results · [Design]**
The Teacher can enter marks by "Snap the mark sheet" or "Type the marks instead", with flags for over-maximum, blank and doubtful marks and a share choice.
- Acceptance: Given a photo, Then toast "Dhruva read 36 marks from the photo · 2 need a look" with amber rows and fix chips (for example "13", "20", "Absent", "0"); the save button reads "Fix 2 marks first", then "Save marks"; save toasts "Saved · parents see marks at 4 pm · 2 students added to remedial suggestions" or "Saved · sent to Dr. Desai to check".
- Rules: "AB" means absent; no save with flags or blanks; "Parents see it today" or "After Dr. Desai checks"; typing mode offers the same checks (ai.marks_from_photo off leaves typing).

**DSK-TCH-004 · Must · MVP · flag: mod.homework · [Design]**
The Teacher can review homework in Homework: pills per class, tiles (Handed in, Need your look, Checked by Dhruva, Missing), filters, scanned work with a score stepper and comment, and "Return to student".
- Acceptance: Given 27 checked, When "Return 27 checked to students" is pressed, Then toast "27 returned with Dhruva's marks and your comment · students and parents see them now"; "Remind 4 missing" toasts "Reminder sent to the students and their parents"; one return toasts "Returned to Advait Singh · 5/10".
- Rules: reasons shown include no working, copied pattern, blurry page, different order; with ai.homework_marking off the teacher marks every page by hand.

**DSK-TCH-005 · Must · MVP · flag: mod.homework · [Design]**
The Teacher can set new homework with "+ Set new homework": Class, What to set ("From the book", "Dhruva writes it", "Reading"), Due, note, preview and "Send to 10-C".
- Acceptance: Then toast "Homework set for 10-C · due Tue 13 Oct · students and parents see it on the app. Dhruva checks the pages when they come in."
- Rules: "Dhruva writes it" requires ai.homework_marking or ai.lesson_plan_drafts; otherwise only the book and reading options show.

**DSK-TCH-006 · Must · MVP · flag: mod.parent_messaging · [Design]**
The Teacher can use Inbox: filters All, From your HoD, Parents, Students; a thread with an editable "Dhruva drafted a reply" and "Make it shorter", "Write my own", "Send reply"; and "+ Message a class or parents".
- Acceptance: Given an empty reply, Then "Send reply" flashes "Write a reply first"; a valid send flashes "Sent to <name>", the unread dot and badge fall.
- Acceptance: Given the composer, Then chips show "10-C parents · 38" etc., templates "Exam reminder", "Homework", "PTM", "Write my own", the toggle "Also send in Hindi", errors "Pick at least one group" and "Write the message first", and success "Sent to N people · Dhruva tells you tonight who hasn't read it".
- Rules: replies go to the app; HoD messages stay within staff; "Messages you sent" shows read counts; Dhruva answers simple doubts from shared notes and shows only the rest (ai.reply_drafts).

**DSK-TCH-007 · Must · MVP · flag: mod.exams · [Design]**
The Teacher can build a question paper in Question papers in three steps (Pattern and chapters; Sections and marks; Review and edit) and send it to the HoD.
- Acceptance: Given the pattern, Then the side panel shows marks add up (for example "80/80"), complexity mix and the blueprint check ("Matches Dr. Desai's blueprint" or "Differs from Dr. Desai's blueprint"); "✦ Draft the paper" with unbalanced marks flashes "Marks add up to N of 80 · use Balance with Dhruva"; "Send to Dr. Desai" is disabled with "N marks still to add" until balanced and then toasts "Sent to Dr. Anjali Desai · you'll see her comments here".
- Rules: pattern options are board pattern (80 marks, 3 hours), unit test (40, 1½ hours), class test (20, 40 minutes), copy last paper, start blank; per question "Another question", "Pin", "Delete"; per section "✦ Redraft section" keeping pinned questions; "Print" marks DRAFT; "Word file" downloads; flow is teacher to HoD to exam cell (ai.paper_generator off keeps manual drafting).

**DSK-TCH-008 · Should · MVP · flag: mod.student_learning · [Design]**
The Teacher can make and share notes in Notes for students: pick Classes, Chapter and What to make (Revision notes, Formula sheet, Practice questions), edit in "Edit / Student view", and share with a time and parent option.
- Acceptance: Given share, Then toast "Shared in the student app · parents told on WhatsApp" or "Scheduled for Tomorrow 7 am · you can still edit until then"; the panel offers "Edit and share again" and "Pull back" (toast "Pulled back. Students no longer see it until you share again.").
- Rules: sources are the lesson log or photos of the teacher's notes; "Your recent notes" shows open counts such as "34 of 78 opened".

**DSK-TCH-009 · Must · MVP · flag: mod.lesson_plans · [Design]**
The Teacher can create a lesson plan in Lesson plans: mode (Dhruva's draft or Start blank), span, classes, lesson shape in minutes, style, extras, homework level, check type and resources, "✦ Redraft with these settings", day-level edit and "Send to Dr. Anjali Desai".
- Acceptance: Given a plan with an empty day, When "Send" is pressed, Then the message reads "Add a topic and activity for each lesson first"; a valid send toasts "Sent to Dr. Anjali Desai · she usually reviews by Monday".
- Rules: "Fit to 40 minutes" toasts "Adjusted to 40 minutes"; "Pin this day" survives redraft; Print marks DRAFT; with ai.lesson_plan_drafts off the plan is written manually.

**DSK-TCH-010 · Must · MVP · flag: mod.remedial · [Design]**
The Teacher can send students for Saturday remedial from Remedial and My students: tick rows, "Send 6 students to Mrs. Sinha", or "Refer to the counsellor".
- Acceptance: Given 6 ticked, Then toast "Sent to Mrs. Rekha Sinha · she adds them to Saturday remedial groups and tells parents"; "Refer to the counsellor" toasts "Referred to Ms. Ritika Bhalla, counsellor · only she sees the reason".
- Rules: suggestions come from tests, homework and attendance (ai.remedial_grouping); wellbeing concerns go to the counsellor, not remedial; the reason is visible to the counsellor only.

**DSK-TCH-011 · Must · MVP · flag: mod.attendance · [Design]**
The Teacher can view My students per class with KPIs (Class average, Attendance, Need help), filters and a student detail with "Suggest for Saturday remedial", "Message parent", "Refer to counsellor".
- Acceptance: Then "Suggest for Saturday remedial" toasts "<Name> suggested for Saturday remedial · Mrs. Sinha told"; "Message parent" toasts "Message sent to <family> family · replies come to your Messages".
- Rules: a top performer has no remedial button; a teacher sees only own classes; the pace chip comes from the end-of-day check.

**DSK-TCH-012 · Must · MVP · flag: mod.pace_tracking · [Design]**
The Teacher can send the end-of-day check per class (On plan, Behind, Ahead, with a reason when behind) in about 20 seconds.
- Acceptance: Given Dhruva's guess, When sent, Then the card reads "Sent · Dr. Desai and Mrs. Sinha can see where each class is"; reasons are Students needed more time, Event or assembly, I was away, Test or exam.
- Rules: the check is optional per class; unsent classes appear on the HoD's "Not checked in yet".

**DSK-TCH-013 · Should · MVP · flag: mod.calendar_ptm · [Design]**
The Teacher can view the Calendar (Month or Whole year; filters All, My duties, Exams, Holidays, PTMs, Events) and the Timetable (Today / Week).
- Acceptance: Then duties (invigilation, plan due, meetings) show in a distinct "Your duty" colour; the week grid shows "↻ 8-A" for cover and the footer "27 teaching periods · 1 cover this week · 12 free".
- Rules: the calendar is read-only for teachers; new timetables appear only on their start date.

**DSK-TCH-014 · Must · MVP · flag: mod.hr_leave · [Design]**
The Teacher can use Me to apply for leave or "Out on duty" and see payslips and notices.
- Acceptance: Given "Out on duty" with a part-day choice, Then the Today list shows "Waiting for Dr. Desai" then "Approved · cover arranged", no leave is used and attendance shows On duty; leave routing reads "Goes to Dr. Anjali Desai, HoD. Mrs. Rekha Sinha arranges cover for your classes."; notices requiring "Confirm" toast "Confirmed · <sender> can see it".
- Rules: payslip shows earnings, deductions and "Email to me" / "Download PDF"; see DSK-SHL-007.

## 6.3b Functional requirements: operations and students

Conventions for this half of Section 6. Phase mapping: MVP = build Oct-Dec 2026 and go-live; P2 = roadmap "Phase 1" (Apr-Sep 2027); P3 = roadmap "Phase 2" (Oct 2027-Mar 2028). Every requirement here is also switched off when `ch.desktop_web` is off for the tenant, campus or role (see TFC); that flag is not repeated on each block. Where a screen exists on the phone as well, the phone behaviour is specified in Section 7 (App - Mobile); this half specifies the desktop web app only. Every operations role opens on "Today": one card at a time, headed "N THINGS NEED YOU · 1 OF N", prepared by Dhruva, with "Later ›" and "See all N for today · M done". That pattern is specified once as DSK-HRP-001 and reused (by reference) in the other operations roles.

Priority notes: "Must" = needed for the role to work a normal day; "Should" = designed and expected at go-live but a manual workaround exists; "Could" = convenience.

### HR and payroll (DSK-HRP)

Actor: HR and payroll executive (sample: Ms. Nandini Rao). Sidebar: Today, Employees, Attendance & leave, Payroll, Hiring & onboarding, Exits, Me. Scope: all staff of the one campus the role is attached to (sample: 296 staff, 193 teaching, 103 non-teaching).

**DSK-HRP-001 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can work a Dhruva-prepared daily queue on "Today" and clear it one card at a time.
- Acceptance: Given 6 open items, When HR opens Today, Then the first card shows "6 THINGS NEED YOU · 1 OF 6", an "Up next" list of the next four items and "See all 6 for today · 0 done".
- Acceptance: Given HR taps "Later ›", When the card is deferred, Then the next card comes forward and the deferred item stays in the list as not done.
- Acceptance: Given the condition behind a card is met (for example all corrections verified), When HR returns to Today, Then the card is gone and the "done" count and sidebar badges have updated.
- Rules: the queue order in the design is: payroll run, attendance corrections, leave issues affecting pay, joiners, exits with open items, expiring documents. Each card has a one-tap action ("Open payroll", "Verify all", "Use suggestions", "Send reminders", "Chase both", "Request renewals") that performs the whole step and shows a confirmation such as "4 corrections verified · attendance updated". Queue and counts are the same data as the phone (Section 7).

**DSK-HRP-002 · Should · MVP · flag: mod.hr_leave · [Design]**
HR sees today's staffing picture, payroll status and upcoming events on one page.
- Acceptance: Given the Today page, Then four KPI tiles show "Present today", "On leave", "Not marked yet" (link "See who" opens Attendance & leave > Today's attendance) and "Open positions".
- Acceptance: Then a payroll card shows the number of exceptions, total net pay, employee count, pay date and a 5-segment progress bar, with button "Open payroll" selecting the Teaching run.
- Acceptance: Then "Headcount" shows teaching vs non-teaching and the share who left this year, and "Coming up" lists dated events (joiners, payroll to principal, probation end, salary credit, document expiries).
- Rules: header buttons "+ Notice to staff" (opens a notice draft that Dhruva can write; sending follows the notice rules of the notices module) and "Ask Dhruva".

**DSK-HRP-003 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can search, filter and save views of the staff directory.
- Acceptance: Given "296 people", When HR types in search, Then rows match on name, role or department.
- Acceptance: Filter pills "All", "Teaching", "Non-teaching", "Contract & visiting", "On probation", "Documents pending", "Joining soon" narrow the table (columns Employee, Role, School, Type, Status); the footer reads "Showing 12 of 296 · click anyone to open their profile".
- Acceptance: The three smart tiles ("Documents due", "Probation ending", "Joining soon") act as filters; tapping again clears. When a filter is active a bar shows the filter's action and "+ Save as my view"; saving shows "Saved · find it under My views".
- Rules: bar actions are "Request renewals" ("Renewal requests sent · police verification forms and contract drafts"), "Ask HoD for review" ("Asked the HoD for Ms. Farah Khan's review"), "Send induction reminder" ("Imran and Sneha asked for the missing items"); each flips to a ticked state ("Sent ✓", "Asked ✓", "Reminded ✓").

**DSK-HRP-004 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can open an employee profile with Overview, Attendance, Payroll and Documents tabs.
- Acceptance: Given a row is clicked, Then the profile shows initials, name, status chip, role, school, employee ID, joining date and any alert (for example "Bank details changed on 7 Oct · check before payroll").
- Acceptance: Overview shows department, employment type, school, reports to, date of joining, payroll group, salary (annual CTC, monthly gross, last net pay) and leave balance bars (Casual, Sick, Earned).
- Acceptance: Attendance shows the current month calendar (present, holiday, leave, late) and a one-line summary; a joiner shows "Starts on 12 Oct". Payroll lists the last six payslips (gross, net) and opens a payslip. Documents lists Offer letter, ID and address proof, Qualification certificates, Police verification, Bank and PF form, each with a status chip; tapping a missing item sends "<document> requested from <name>".
- Rules: contract staff show "No leave: paid a fixed fee as per contract"; visiting staff show "No leave: paid for periods taught". Salary and bank fields are visible only to HR, accounts, principal and the employee.

**DSK-HRP-005 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can add an employee, edit a record, issue a letter and start an exit; every change is logged.
- Acceptance: "+ Add employee" opens a record where Dhruva fills what it can from the offer letter ("New employee: Dhruva fills what it can from the offer letter").
- Acceptance: "Edit" shows "Record opened for editing · changes are logged"; every saved change writes an audit entry (who, field, old, new, time).
- Acceptance: "Issue letter" offers templates (experience, salary certificate, NOC) pre-filled by Dhruva; "Start exit" opens Exits for that person.
- Rules: a change to bank account, IFSC, UAN or PAN raises a payroll alert on the profile until HR marks it verified. [Spec] letters are generated as PDF and stored in the employee's Documents.

**DSK-HRP-006 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can verify or reject HoD-approved attendance corrections.
- Acceptance: Given tab "Corrections · 4", Then each row shows the person, type (Missed check-in, Late arrival, On duty), date, reason, approving HoD and a tag "Changes pay" or "No pay change".
- Acceptance: "Verify" turns the row to "✓ Verified"; "Reject" shows "Rejected · person told"; "Verify all HoD-approved (4)" shows "4 corrections verified · attendance updated" then "✓ All verified".
- Rules: corrections were checked by Dhruva against the timetable before listing. Open corrections block "Lock attendance" in every run (DSK-HRP-010).

**DSK-HRP-007 · Must · MVP · flag: mod.hr_leave · [Design]**
HR can settle leave that exceeds balance as comp-off first, else unpaid, and the choice flows into payroll.
- Acceptance: Given tab "Leave issues · 3", Then each row shows the person, leave type, days asked, days left, comp-off days available and buttons such as "Use 2 comp-off days", "Mark 2 days unpaid", "Ask the principal to waive", "Use 1 comp-off, 1 unpaid".
- Acceptance: When chosen, the row shows "✓ 2 comp-off days used · no pay cut"; unpaid days appear on the run's "Leave without pay" line.
- Rules: Dhruva's rule is shown in a box: "Comp-off first, unpaid days only when none are left." Comp-off is earned from approved extra duty (annual day, Saturday invigilation). "Use suggestions" on Today applies Dhruva's recommended choice to all issues ("3 leave issues settled · staff told on the app"). Unsettled issues show ₹0 on the leave-without-pay line and "3 leave issues not settled yet" in Review changes. HoDs, not HR, approve the leave itself.

**DSK-HRP-008 · Should · MVP · flag: mod.attendance · [Design]**
HR can see today's staff attendance by group and chase unmarked staff.
- Acceptance: Tab "Today's attendance" shows "Present by group" (Teaching x of y, Non-teaching x of y), "Not marked yet · 6" with "Remind all 6", and "On leave today" (9, "Showing 4 of 9") with leave type, dates and approver (or "Waiting for <principal>").
- Acceptance: "Remind all 6" shows "6 staff reminded to mark attendance"; an individual reminder shows "Reminder sent · they can check in with one tap from Today".
- Rules: night-shift staff whose shift ended in the morning appear until they mark; this tab is desktop only.

**DSK-HRP-009 · Must · MVP · flag: mod.payroll · [Design]**
HR can run four separate payrolls, each with its own five-step run.
- Acceptance: Given tab "Payroll runs · 4", Then the left list shows Teaching staff, Non-teaching staff, Contract staff and Visiting & part-time, each with headcount, pay basis, pay date and net, and the footer "All payrolls this month: ₹1,98,20,000 net across 4 runs".
- Acceptance: A stepper shows "Lock attendance", "Review changes", "Fix exceptions", "Approve", "Pay"; step 1 is renamed "Collect invoices", "Count periods", "Count sessions" or "Count days" for other pay bases. Steps are sequential and gated.
- Acceptance: A run summary panel is always visible: People, Gross pay, Provident fund, Professional tax, Income tax (TDS), Net pay with basis and pay date.
- Rules: each run has its own date and its own approver; one employee belongs to exactly one payroll. [Spec] run states: Draft, Locked, Reviewed, Exceptions cleared, With principal, Approved, Paid; a Paid run is immutable (corrections go to the next run as an arrears line).

**DSK-HRP-010 · Must · MVP · flag: mod.payroll · [Design]**
HR can lock attendance (or invoices, periods, sessions) for a run, including an early cut-off date.
- Acceptance: Given open corrections, When HR taps "Lock attendance", Then the button flashes "Verify the 4 attendance corrections first" and nothing locks.
- Acceptance: Given all corrections verified and an early pay date, Then the step reads "Lock attendance to 15 Oct · Paying early: the rest of October is counted as present" and locking flashes "Attendance locked to 15 Oct · rest of the month counted as present".
- Acceptance: For contract runs "Use the 9 invoices received" flashes "9 invoices locked · a late invoice joins the next run"; for per-period runs "Use these counts" flashes "Counts locked for this run" (periods taught are taken from the timetable and class attendance).

**DSK-HRP-011 · Must · MVP · flag: mod.payroll · [Design]**
HR can review what changed since last month before continuing.
- Acceptance: "Review changes" lists joiners (pro-rated days), leavers, confirmations after probation, DA arrears, "Leave without pay", agency invoices and periods taught, each with a signed rupee amount; "Changes look right" advances.
- Rules: Dhruva's chat answers "What changed in pay since September?" from the same data and cites "September and October salary sheets".

**DSK-HRP-012 · Must · MVP · flag: ai.payroll_checks · [Design]**
HR can resolve each payroll exception with one of two suggested choices before approval.
- Acceptance: Given "Dhruva checked this run against September and found N things to fix", Then each exception shows a severity tag ("Blocks payment", "Likely error", "Needs info", "Check invoice", "Check periods"), the evidence and two buttons plus "Open employee".
- Acceptance: Example outcomes: "Salary held · he has been asked to visit HR"; "Verified · paid to the new account"; "Duplicate removed · pay up 9%"; "Asked on WhatsApp · PF filed when it arrives"; "Paying ₹4,11,000 · note sent to the agency"; "Paying 48 periods · ₹19,440 net".
- Acceptance: The continue button reads "2 left to fix" and is disabled until zero remain, then "Continue to approval".
- Rules: every decision writes a note on the run ("note added for the principal", "note sent to the agency"). With ai.payroll_checks off, HR sees the same run without Dhruva's flags and must review manually; the gates in DSK-HRP-009 still apply. [Spec] a "Hold salary" decision excludes that employee from the bank file and carries to a supplementary run.

**DSK-HRP-013 · Must · MVP · flag: mod.payroll · [Design]**
HR can send a run to the principal for approval and then release the bank file and payslips.
- Acceptance: "Send for approval" flashes "Sent to Ms. Neelam Mehra" and the run shows "With principal"; on approval it shows "<principal> approved Teaching staff".
- Acceptance: "Send bank file and release payslips" (or "...payment statements" for non-monthly runs) generates the salary-account bank file and flashes "Teaching staff paid · 188 payslips on Mon 19 Oct, early for Dussehra".
- Rules: approval chain is configurable per payroll (DSK-HRP-014). [Spec] the bank file is released only on the pay date or later, only if the salary account funding check from Finance (DSK-FIN-020) shows sufficient balance, and release requires HR to confirm a second time; payslips become visible in staff "Me" at 6 am on the pay date.

**DSK-HRP-014 · Should · MVP · flag: mod.payroll · [Design]**
HR can set up payrolls: pay basis, date, earnings, deductions, approver and members.
- Acceptance: Given tab "Payroll setup", Then HR can edit "Payroll name"; "Pay basis" (Monthly salary, Fixed fee or invoice, Per period, Per session, Per day); "Pay date" (1st, 7th, 25th, Last working day, moving to the previous working day when it falls on a Sunday); "Earnings" toggles (Basic, DA, HRA, Transport, Night duty, Contract fee, Per-period rate, Per-session rate); "Deductions" (PF 12%, ESI, Professional tax, TDS on salary, TDS 2% (194C), TDS 10% (194J)); "Approval" (Principal approves; HoD confirms, principal approves; Principal approves invoices over ₹1 lakh).
- Acceptance: "Save payroll" shows "Saved · '<name>' · changes apply from the next run, <date>". "Remove" and "Add" in the member list flash "<name> removed from / added to <payroll>".
- Acceptance: An alert lists anyone with a signed contract in no payroll (for example "Mr. Kunal Mehta ... isn't in any payroll, so he wouldn't be paid") with "Add to this payroll".
- Rules: "+ New payroll" lets Dhruva suggest a payroll ("Sports coaches"; "Use suggestion" moves 4 coaches in). Setup is desktop only. Statutory deductions beyond the toggles (full PF/ESI/TDS filing) are P2.

**DSK-HRP-015 · Must · MVP · flag: mod.hiring_onboarding · [Design]**
HR can track joiner checklists to completion.
- Acceptance: Given tab "Onboarding & openings", Then each joiner shows a percentage and checklist items with an owner (Candidate, HR, IT and admin, Academic coordinator, HoD): Offer letter signed, Documents uploaded, Police verification, Bank and PF form, Email / ID card and app login, Timetable assigned or Lab safety induction.
- Acceptance: Tapping an item toggles its tick and the percentage bar updates; "Send reminders" (Today) sends WhatsApp reminders and the card becomes "Joiners reminded".
- Rules: [Spec] an item owned by another role is ticked by that owner in their own app; HR can override with a reason that is logged.

**DSK-HRP-016 · Should · MVP · flag: mod.hiring_onboarding · [Design]**
HR can manage open positions and invite Dhruva's shortlisted candidates to demo classes.
- Acceptance: The "Open positions" table shows Role, School, Applied, Shortlisted, Demo, Offer and Days open (red above 20 days); tapping a post opens "Shortlists" with the requesting HoD or in-charge, the funnel (Applied, "Shortlisted by Dhruva", Demo class, Offer) and candidate cards with a one-line summary.
- Acceptance: "Invite" flashes "<name> invited to a demo class"; "Invite all to a demo class · Thu 15 Oct" flashes "Demo classes booked for Thu 15 Oct · the HoD is told".
- Acceptance: "+ New opening" opens "pick the post · Dhruva writes the advert".
- Rules: "Dhruva read every CV against the post · you choose": Dhruva never rejects or invites on its own. With the shortlist flag off, HR sees the applicant list unranked. [Spec] CVs are retained for 12 months after the post closes unless the candidate asks for deletion.

**DSK-HRP-017 · Must · MVP · flag: mod.hiring_onboarding · [Design]**
HR can run an exit: documents, clearance, assets and a final settlement sent to the principal.
- Acceptance: Given the Exits list (name, "N to do" or "Closed", role, resignation and last-day dates), Then the selected person shows three stages: Documents (resignation letter, handover note, exit interview), Clearance (Library, Accounts, IT) and Assets (laptop, ID card and keys), each item with owner and status "Received" or "Pending".
- Acceptance: Pending items offer "Remind" ("Reminder sent to <owner>") and "Mark received"; "Chase both" on Today triggers both.
- Acceptance: "Final settlement: ₹21,400 · 12 days earned leave encashed · no gratuity (under 5 years)" is shown as "Sent for approval once the 2 open items are done"; when none remain, "Send settlement for approval" flashes "Final settlement sent to Ms. Neelam Mehra for approval".
- Rules: settlement is blocked until every line is received; approval goes to the principal; "+ Start an exit" asks for person and last day and lists every step. Exits are desktop only (phone shows "Exits are on the desktop"). [Spec] on the last day the person's app login is set to read-only for payslips and tax documents for 12 months, then closed.

**DSK-HRP-018 · Should · MVP · flag: mod.hr_leave · [Design]**
HR can use the staff "Me" page for own leave, payslips and notices.
- Acceptance: Tabs "Leave", "Payslips", "Notices · 7"; apply by Type (Casual, Earned, Sick, Out on duty), dates (no past dates, half-day when one day), Reason pills and "In charge while you are away"; routing text states the principal approves and more than 3 days goes on to the group HR head.
- Acceptance: Payslip detail shows earnings, deductions, net, tax and PF year to date, "Email to me" and "Download PDF"; notices that need acknowledgement show "Confirm" then "Confirmed · <name> can see it".
- Rules: identical on all staff roles (see Section 7 for the shared Me page); the in-charge names differ per role.

**DSK-HRP-019 · Could · MVP · flag: ai.assistant_chat · [Design]**
HR can ask Dhruva about records, attendance, leave, payroll, hiring and exits.
- Acceptance: Suggested questions "What changed in pay since September?", "Whose probation ends this month?", "Which documents expire soon?"; answers carry stat chips and a source line (for example "Staff records").
- Acceptance: Other questions get "In the MVP I help with staff records, attendance, leave, payroll, hiring and exits. I answer from your records and show the source."

### Finance and accounts (DSK-FIN)

Actor: Accounts in-charge (sample: Mr. Sanjay Gupta), with assistants as makers, the principal and owner as approvers, and the CA as an external filer. Sidebar: Today, Approvals, Fees, Payments (Purchase bills, Vendors, Inventory), Bank and Tally (Bank reconciliation, Tally sync), Accounts (Vouchers, Ledgers, Setup), Reports, Compliance and month-end, Me. An "Account year" selector ("2026–2027" / "2025–2026 (closed)") sits at the top of every page.

**DSK-FIN-001 · Must · MVP · flag: mod.finance_accounts · [Design]**
The accounts in-charge can clear a Dhruva-prepared daily queue.
- Acceptance: Given the Today page, Then the first card reads "6 THINGS NEED YOU · 1 OF 6", ordered by urgency: move salary money, bank lines to review, Tally failures, deposit counter cash, bills to approve, items below reorder level.
- Acceptance: Tapping an action runs it at once and shows a confirmation for about 3 seconds; the card re-renders as done with a tick and counts fall.
- Rules: pattern as DSK-HRP-001. "Later ›" never completes anything. [Spec] every one-tap action that posts to the books is idempotent and logged with user and time; the confirmation includes an "Undo" for 10 seconds only where no external message or bank instruction has been sent.

**DSK-FIN-002 · Should · MVP · flag: mod.finance_accounts · [Design]**
The accounts in-charge sees live balances, approvals and cash outlook below the queue.
- Acceptance: Tiles "Approvals · 6 waiting for you · ₹7,53,120 in total" and "4 of 7 steps left to close September"; KPI tiles Total assets, Total liabilities, This month income, This month expense; "Recent transactions" (Voucher, Date, Particulars, Type, Amount) with "All vouchers"; "Financial summary"; "Cash coming and going" (dated expected inflows and outflows).
- Rules: figures are real time from the ledger; header buttons "Ask Dhruva" and "+ New voucher".

**DSK-FIN-003 · Must · MVP · flag: mod.approvals · [Design]**
The accounts in-charge can approve or send back each maker's request, with Dhruva's pre-check.
- Acceptance: Given "6 waiting for you", Then each card shows type chip (Payment voucher, Purchase bill, Fee concession, Journal voucher, Fee refund), title, purpose, amount, maker and time; "Approve" greys it to "✓ Approved" and toasts "Approved · <maker> is told".
- Acceptance: "Details" opens maker, a "DHRUVA CHECKED" note (amber or green), a "Note for the maker (needed to send back)" and "Approve" / "Send back"; sending back without a note is refused; with a note it marks "↩ Sent back" and toasts "Sent back to <maker> with your note".
- Acceptance: A running "Audit trail" shows each action with actor, item, amount and time, newest first.

**DSK-FIN-004 · Must · MVP · flag: mod.approvals · [Design]**
The system enforces maker-checker and a second approval above ₹2 L.
- Acceptance: Given the banner "Maker–checker is on: nobody can approve their own entry, and anything above ₹2 L also needs the principal", When a user opens an item they created, Then Approve is disabled with the reason.
- Acceptance: Given an item above ₹2 L (diesel bill ₹2,10,000, depreciation journal ₹4,12,000), When the accounts in-charge approves, Then the card shows "✓ Approved · with the principal" and toasts "Approved · sent to the principal for the second approval"; the voucher posts only after the second approval.
- Rules: [Spec] the ₹2 L threshold is tenant-configurable; the second approver can never be the maker or first approver; thresholds are evaluated on the voucher total including GST. Purchase approval limits are in DSK-FIN-009.

**DSK-FIN-005 · Must · MVP · flag: mod.approvals · [Design]**
Fee concessions and refunds follow a defined approval chain before any journal posts.
- Acceptance: Given a concession from a class teacher or admissions, Then the accounts in-charge checks it, the principal recommends and, above the owner limit or for hardship, the owner approves; nothing posts to Tally until the last approver acts.
- Acceptance: From Fees > "Today and approvals", "Send to principal" shows "Sent to Ms. Neelam Mehra · the journal posts to Tally once she approves".
- Rules: concessions above ₹25,000 go to the owner (tenant approval limit); sibling and staff-ward discounts follow the fee policy; refunds require verified bank details. See Section 6.4b for the limits table.

**DSK-FIN-006 · Must · MVP · flag: mod.fees · [Design]**
Accounts can see fees collected today by mode and close the counter day with a deposit slip.
- Acceptance: "Collected today" lists UPI, Card, Net banking, Cash at counter, Cheque with count and amount; "Day close · counter" shows cash and cheques to deposit; "Make deposit slip" toasts "Deposit slip ready to print · contra voucher sent to Tally".
- Rules: app payments reach the bank on their own and need no deposit. [Spec] the slip locks the day's counter receipts; a late receipt for that day needs the accounts in-charge to reopen it with a reason.

**DSK-FIN-007 · Must · MVP · flag: mod.fees · [Design]**
Accounts can view dues by age and fee head and send reminders with a pay link.
- Acceptance: "Outstanding by age" shows 0-30, 30-60, 60-90, over 90 days with amount and families; "Fee heads · Jul–Sep" shows tuition, annual charges, transport (synced from Transport), activities, exam fee.
- Acceptance: "Send reminders with a pay link" changes to "✓ Reminders sent to 2,614 families" and the 90+ day families become a counter call list.
- Rules: with ai.fee_followup off, reminders use the plain template without Dhruva's drafted wording. [Spec] a family with an open dispute or approved concession in progress is excluded from reminders.

**DSK-FIN-008 · Must · P3 · flag: mod.procurement_inventory · [Design]**
Accounts can match a vendor bill to the purchase order and goods receipt (three-way match) before paying.
- Acceptance: Given the pipeline "Requisition → PO → goods received → bill → payment" with stage counts, When a row is picked, Then the match shows PO quantity and rate, goods received and vendor bill, plus an alert such as "Bill rate ₹4,750 against ₹4,550 on the PO: ₹2,400 more".
- Acceptance: A mismatch offers "Pay PO rate, debit note" (toast "Approved at the PO rate · debit note of ₹2,400 sent to <vendor>") or "Accept new rate" (toast "New rate accepted · purchase voucher posted"); a clean match offers approve ("Purchase voucher posted to Tally · payment scheduled ... with TDS").
- Rules: a mismatch is never silent; a partly received PO (190 of 200 reams) means the bill should be for the quantity received. Phase note: purchases were Phase 2 in the original roadmap and appear in the prototype; see 6.8b.

**DSK-FIN-009 · Should · P3 · flag: mod.procurement_inventory · [Design]**
Accounts can raise requisitions, compare three vendor quotes and send a purchase order.
- Acceptance: Tab "Requisitions" lists each request with requester, item, quantity and estimate; three quotes show price, delivery days and rating, the best is pre-selected, another can be tapped; the button sends the PO ("PO sent to <vendor> on email and WhatsApp").
- Rules: POs above ₹50,000 need the principal and above ₹5 L the owner; a "Local market (cash)" quote is flagged "No GST bill".

**DSK-FIN-010 · Should · P3 · flag: mod.procurement_inventory · [Design]**
Accounts can manage vendors with TDS, MSME and document checks, and pay them in batches.
- Acceptance: Table columns Vendor, Category, TDS, Outstanding, Due; filters "All 8 / To pay 5 / On hold 1"; a vendor detail shows GSTIN, rating, outstanding and documents (PAN, GST certificate, "Bank details: Verified by penny test", MSME "pay within 45 days", agreement).
- Acceptance: "Pay all 5" toasts "5 payments scheduled · TDS deducted · vouchers sent to Tally"; held vendors are excluded; "Schedule payment" pays one vendor.
- Rules: TDS section and rate come from the vendor master; MSME vendors are flagged before day 45; vendors sync both ways with Tally.

**DSK-FIN-011 · Could · P3 · flag: mod.procurement_inventory · [Design]**
Accounts can view stock against reorder levels, issue stock and see the asset register.
- Acceptance: Tabs "Stock", "Issue requests", "Asset register"; items below reorder show "Below reorder"; "Raise requisitions" toasts "3 requisitions raised · Dhruva asked 3 vendors each for quotes"; an issue button toasts "<item> issued · stock updated".

**DSK-FIN-012 · Must · MVP · flag: mod.bank_recon · [Design]**
Accounts can reconcile each bank account in four steps and close the month with a statement.
- Acceptance: Given account cards (fee collection, salaries, operations) with balance and line counts, Then a bar shows "Import statement", "Auto-match · 1,184 matched by Dhruva", "Review unmatched · 28 left", "Post and close"; the side panel shows balance per bank, uncleared cheques, items to post and "Difference with books".
- Acceptance: Each unmatched item shows Dhruva's suggestion and two buttons: for example "Match to Aanya's fee" / "Ask the parent"; "Create journal" / "Ignore"; "Reverse receipt, tell parent" / "Hold"; "Split gateway fee" / "Review"; "Create payment voucher" / "Review"; group "Accept 23 matches".
- Acceptance: At zero items "Post and close September" becomes active and toasts "September closed · bank reconciliation statement saved and sent to Tally".
- Rules: a bounced cheque reverses the receipt and adds a ₹500 charge; "Ignore" and "Hold" post nothing and leave the item "Left for later"; HDFC and ICICI come by feed, SBI by statement upload. With ai.bank_matching off, all lines arrive unmatched for manual matching.

**DSK-FIN-013 · Must · P2 · flag: mod.tally_sync · [Design]**
Accounts can sync vouchers and masters with TallyPrime and fix failed vouchers.
- Acceptance: The page shows connector status ("Tally connector online · Sync now · Last sync 9:00 am"), the connection card (version, company, schedule every 30 minutes and on demand, direction), "Didn't reach Tally · 3" each with a reason and two fixes (for example "Map to 'Transport Fee Income'" / "Create ledger in Tally").
- Acceptance: "Sync now" changes to "Synced just now" and toasts "Synced with Tally · 6 vouchers sent · 0 failed"; a fixed item reads "✓ Fixed · posted to Tally"; "Fix and resync" on Today fixes all.
- Acceptance: Sub-tabs "Ledger mapping", "Voucher types" (counts per type) and "Sync log" (time, sent, failed).
- Rules: vouchers go to Tally with receipt or bill number; ledgers, vendors and cost centres come back. Phase note: Tally two-way sync is Phase 1 in the roadmap (P2); the prototype shows it now (see 6.8b).

**DSK-FIN-014 · Must · MVP · flag: mod.finance_accounts · [Design]**
Accounts can create and browse vouchers, with Dhruva filling a draft from a sentence.
- Acceptance: "+ New voucher" opens "New voucher · PV-0450" with type (Receipt, Payment, Contra, Journal, Purchase, Sales), auto-number, date, Dr/Cr lines ("Add line", "Remove"), a live total and balance check ("Enter the amounts" / "✓ Balanced" / "Difference ₹x"), narration and "✦ Fill in".
- Acceptance: "Fill in" with "paid electricity bill 1,84,000 from SBI" fills the ledgers and toasts "Dhruva filled the voucher · check the ledgers and save"; with no amount it says "Add an amount, e.g. 'paid electricity bill 1,84,000 from SBI'".
- Acceptance: Save is enabled only when balanced; success toast "<no> saved · posted to the ledgers and sent to Tally". The Vouchers list filters by type.
- Rules: a voucher by an assistant goes into Approvals as a maker request. flag note: "Fill in" is ai.finance_assist (proposed).

**DSK-FIN-015 · Should · MVP · flag: mod.finance_accounts · [Design]**
Accounts can maintain ledgers, ledger groups and account setup.
- Acceptance: Ledgers: pills All, Assets, Liabilities, Income, Expenses, Funds; detail with opening balance, GST/TDS applicability, "In Tally as … · synced"; "New ledger" needs a name ("Give the ledger a name") and toasts "Ledger created · it reaches Tally at the next sync".
- Acceptance: Setup: Ledger mapping for new fee heads ("Mapped · ledger created here and in Tally"), Voucher types, Account year, Account main, Ledger groups ("Group created · also created in Tally at the next sync"), Main groups.
- Rules: "Account main" (society name, PAN, TAN, GSTIN, 12A/80G, books start, cost centres, bank accounts) is edited by the group finance head and audited each year; the school accounts in-charge sees it read-only.

**DSK-FIN-016 · Must · MVP · flag: mod.finance_accounts · [Design]**
Accounts can lock a month and manage account years.
- Acceptance: In "Account year", twelve month tiles show Locked / Open · current / Future; "lock September" toasts "September locked · no one can post or change September vouchers"; "create 2027-28" toasts "2027–28 created · closing balances carry forward on 1 Apr 2027".
- Acceptance: Selecting a closed year toasts "2025–26 is closed and audited · view only".
- Rules: after a lock, changes need the principal's approval; the lock button is enabled only when all month-end steps are done (DSK-FIN-019).

**DSK-FIN-017 · Must · MVP · flag: mod.reports · [Design]**
Accounts can open the eight standard reports and export them.
- Acceptance: The hub lists Day Book, Profit & Loss, Balance Sheet, Ledger Report, Voucher List, Tarij Report (trial balance), Operational Report and MIS Report with a summary strip; each opens with "Back" and Excel and PDF buttons ("<Report> exported to Excel" / "saved as PDF").
- Acceptance: P&L and Balance Sheet group by main group and show a balanced check; Tarij shows Dr = Cr; Ledger Report has a ledger picker with running balance; MIS shows fee realisation, cost per student, salaries ÷ income, surplus margin and budget vs actual.
- Rules: data is real time and respects the selected account year. The drafted segments "Statutory dues" and "Budget vs actual" are not in the hub (see 6.8b).

**DSK-FIN-018 · Must · MVP · flag: mod.finance_accounts · [Design]**
Accounts can track statutory filings and send ready filings to the CA.
- Acceptance: "Statutory calendar" lists TDS 24Q, TDS 26Q, ITR-7 and others with status "Ready to file" / "Needs data"; "See all 10 filings" shows upcoming and filed (TDS deposit, GSTR-1, GSTR-3B, PF ECR, ESI, Form 10B).
- Acceptance: "Send to CA" toasts "TDS return 24Q · Q2 sent to your CA with the working files" and the row reads "Sent to <CA> · you'll see the acknowledgement here"; "Send the emails" for missing vendor PAN makes the filing ready.
- Rules: the CA confirms every filing; due dates in the design are samples, so [Spec] they come from a statutory calendar maintained by DhruvaOne and reviewable by the CA. GST applies to uniform and book-shop sales only (school fees are exempt).

**DSK-FIN-019 · Must · MVP · flag: mod.finance_accounts · [Design]**
Accounts can work a seven-step month-end close and lock the month.
- Acceptance: Steps: bank reconciliation of all accounts; fee receipts posted; salary journal and TDS liability; vendor bills for the month ("Accrue both bills"); depreciation journal ("Review in Approvals"); Tally sync ("Fix and resync"); trial balance reviewed ("Mark as reviewed"); a progress bar fills and each step gets a result line.
- Acceptance: With all steps done the "lock September" button is enabled with "Locking stops anyone from changing September entries. Reports for September become final."; after lock: "September is closed and locked".

**DSK-FIN-020 · Must · MVP · flag: mod.finance_accounts · [Design]**
Accounts can schedule the transfer that funds the salary account before payroll.
- Acceptance: Given salaries of ₹1.98 Cr due 19 Oct and ₹48 L in the salary account, Then Today shows "Move ₹1.55 Cr to the salary account by Fri 16 Oct" and "Schedule transfer" turns the card to "Salary account funded · Transfer scheduled for Fri 16 Oct · contra voucher sent to Tally".
- Rules: the principal approves the transfer on her phone; the amount is computed from approved payroll runs. [Spec] if the balance is short on the day before the pay date, HR and the principal are alerted (see 6.5b).

**DSK-FIN-021 · Should · MVP · flag: mod.hr_leave · [Design]**
The accounts in-charge can use the staff "Me" page (leave, payslips, notices) as in DSK-HRP-018; in-charge names differ (Ms. Priya Nair handles payments and the bank while away).

**DSK-FIN-022 · Could · MVP · flag: ai.assistant_chat · [Design]**
Accounts can ask Dhruva about fees, bank, bills, vendors, stock and Tally.
- Acceptance: Suggested questions "Do we have enough cash for salaries on the 19th?", "Which vendors do we owe the most?", "Is Tally up to date?" with chips and a source ("Bank feeds and October payroll"); other questions get "In the MVP I help with fees, the bank, bills, vendors, stock and Tally. I answer from your books and show the source."

### Admissions CRM (DSK-ADS)

Actor: Admissions counsellor (sample: Ms. Isha Bhardwaj) with the front office adding walk-ins. Sidebar: Today, Enquiries, Campus tours, Seats & offers, Campaigns, Reports, Me. Scope: the campus admissions season (sample: 2027-28, 410 seats).

**DSK-ADS-001 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can clear a Dhruva-prepared daily queue and see season KPIs.
- Acceptance: Cards (pattern of DSK-HRP-001): new enquiries welcomed ("Send welcome and book calls"), overdue follow-ups ("Send follow-ups"), tours today ("Open tours"), offers expiring ("Remind families"), seats freed ("Offer to next 2"), Open House reminder ("Send reminder").
- Acceptance: KPI tiles "Enquiries", "Tours done", "Offers out", "Admitted" (with seats); "Where families are" shows the six-stage funnel; "Dhruva noticed" shows one data insight.
- Rules: each action shows a confirmation ("Welcome sent to 3 families · calls booked for this morning"); WhatsApp messages go out in English and Hindi per family language, and sending uses approved templates (DSK-ADS-009).

**DSK-ADS-002 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can view every family as a board by stage or as a list.
- Acceptance: "Board" has columns New, Contacted, Tour booked, Toured, Applied, Offer made, Admitted with season counts and "Showing a sample of each stage · counts are the whole season"; "List" adds stage pills.
- Acceptance: Each card shows child and grade, parent, source, temperature chip (Hot red, Warm amber, Cold blue) and Dhruva's one next step ("Call within the day", "Book a campus tour", "Send the application link while interest is high"...).
- Acceptance: Temperature pills "All families", "Hot · 6", "Warm · 5", "Cold · 1"; a banner "2 hot families have not toured yet. Call them first." with "Show hot only".
- Rules: with ai.admissions_scoring off, temperature is set by hand (default Warm) and next-step text falls back to stage defaults.

**DSK-ADS-003 · Must · MVP · flag: mod.admissions_crm · [Design]**
Staff can add an enquiry.
- Acceptance: "+ New enquiry" opens a panel: "Parent", "Child", "Applying for" (Nursery, KG, Class 1, Class 6, Class 9, Class 11), "How they heard" (Walk-in, Phone call, Referral, Website); "Save · first call due today" adds a New, Warm family and sends the welcome WhatsApp ("<child> added · first call due today · welcome WhatsApp sent").
- Rules: [Spec] parent mobile is mandatory and validated; a duplicate of an existing parent mobile and child name is flagged before saving; consent to contact is recorded. Enquiries from the website form and WhatsApp arrive in the same board.

**DSK-ADS-004 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can work a family record: next step, call, WhatsApp, temperature, documents and history.
- Acceptance: The record shows child, grade, parent, masked phone, source, temperature and stage chips and a 7-step stage bar; "Dhruva's next step" has one button by stage: "Call now", "Book a tour", "Start tour", "Send application link", "Make an offer", "Record fee paid", "Send welcome kit", each with its confirmation (for example "Offer letter sent · valid for 7 days").
- Acceptance: "Call" and "WhatsApp" open the action ("WhatsApp to Mrs. Neha Kapoor · Dhruva drafted it from the last call"); the counsellor can edit before sending. Override pills "Hot", "Warm", "Cold".
- Acceptance: Details show "Interested in", "Transport" (stop and bus seats from route lists), "Fees" by grade band, "Documents" (Birth certificate, Photo, Last report card, Transfer certificate: Received, Later, Missing, Not needed, Before joining) and "History".
- Rules: "Record fee paid" admits the child and tells accounts and the class teacher; fees paid in the app do the same on their own. [Spec] admitting a child creates a student record draft for the registrar to complete; it never creates a live student automatically without the fee-paid event.

**DSK-ADS-005 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can log a call with an outcome.
- Acceptance: Outcome pills "Interested", "Call back", "Not reachable", "Not interested" plus a note; saving without an outcome shows "Pick how the call went"; success shows "Call logged · next follow-up set" and a History row.
- Acceptance: A reachable call on a New family moves it to Contacted; "Not reachable" shows "Logged · Dhruva will remind you to try again at 5 pm".

**DSK-ADS-006 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can run campus tours: route, live checklist, feedback and the follow-up it triggers.
- Acceptance: The list shows each tour (child, parent, time, "Today"/"Booked"); the route is generated from the family's recorded interests (for example Reception, Junior wing, Art room, Swimming pool, Transport desk) and each stop can be ticked with progress "1 of 5 stops".
- Acceptance: Feedback: interest pills "Very interested", "Interested", "Not sure", "Not interested"; "They liked" (Teachers, Facilities, Sports, Transport, Results, Values); "What holds them back" (Fees, Distance, Class size, Seat not sure, Comparing schools); Dhruva's suggestion changes with interest. Saving without interest shows "Pick how interested they are".
- Acceptance: Very interested or Interested: "Saved · application link sent on WhatsApp" and the family moves to Applied; otherwise "Saved · follow-up set" and it stays Toured.
- Rules: tour confirmation WhatsApp with map and parking is sent when the tour is booked.

**DSK-ADS-007 · Must · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can see seats by grade, manage offers and mark fees paid.
- Acceptance: "Seats for 2027-28" table: Grade, Seats, Offers, Admitted, Waitlist, Left and status chip ("Offers ≈ seats" red; "Under 25% filled" amber; "On track" green) with a fill bar.
- Acceptance: "Offers waiting for the fee" shows each offer with expiry and chip "Fee due" / "Reminded" / "Fee paid"; "Fee paid" per offer toasts "Vanya admitted · fee recorded · accounts told".
- Rules: offers are valid 7 days; an unpaid offer past expiry lapses and its seat returns to the pool [Spec]; fees paid in the app update the row on their own.

**DSK-ADS-008 · Should · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can offer freed seats to the waitlist in the right order.
- Acceptance: The waitlist block states "Ordered by date, with sibling priority" and the next families (staff child, sibling); "Offer the 2 free Nursery seats" toasts "Offers sent to the next 2 Nursery families" and the waitlist moves up.
- Rules: order is date, then sibling and staff-child priority; the counsellor confirms before offers go (Dhruva picks, a person sends).

**DSK-ADS-009 · Should · MVP · flag: mod.admissions_crm · [Design]**
The counsellor can run the Open House campaign and view WhatsApp message performance.
- Acceptance: Campaigns shows Open House (date, registrations by source, programme) and "Send reminder to 126 families" ("Reminder sent to 126 families", English and Hindi).
- Acceptance: A message table lists Welcome (within 5 minutes of an enquiry), Tour confirmation, Application link, Admission fee reminder (3 days before expiry) with sent count and read/reply rate.
- Rules: all messages use pre-approved WhatsApp templates in English and Hindi; opted-out families are skipped [Spec].

**DSK-ADS-010 · Should · MVP · flag: mod.reports · [Design]**
The counsellor can read the funnel and source-conversion reports.
- Acceptance: "Funnel · 2027-28 so far" shows Enquiry, Contacted, Toured, Applied, Offer, Admitted with counts and conversion from the previous stage and a plain-language insight; "Which sources bring families who join" shows Source, Enquiries, Admitted, Conversion with bars green at 10% or more.
- Rules: computed live from season records. [Spec] export to Excel/PDF as in other reports.

**DSK-ADS-011 · Should · MVP · flag: mod.hr_leave · [Design]**
The counsellor uses the staff "Me" page as in DSK-HRP-018 (in charge: Ms. Neha Khanna takes tours and calls). Ask Dhruva (ai.assistant_chat) answers "Which families should I call first today?", "Which grades still have seats?" and "Where do families drop off?" with source lines.

### Security and IT (DSK-SEC)

Actor: Security and IT in-charge (sample: Mr. Rakesh Thakur). Sidebar: Today, Jobs, Gate, Systems, Team, Me. Scope: one campus (sample: 12 guards, 2 technicians).

**DSK-SEC-001 · Must · MVP · flag: mod.it_helpdesk · [Design]**
The in-charge can clear a Dhruva-prepared queue of security and IT items.
- Acceptance: Given "6 THINGS NEED YOU · 1 OF 6", Then cards offer one-tap actions such as "Send Harish", "Call her mother", "Assign Sunil", "Assign Ajay", "Nudge hosts", "Fill with Dhruva"; an assignment moves the linked job from New to Assigned and the done card reads "Gate 2: Harish is on it · Updates come to you as he reports back".
- Acceptance: "Right now" tiles show Open jobs, Visitors on campus (with waiting), Systems "4 of 6", Guards on duty; "Coming up" lists dated events (exams, fence repair, fire drill, Diwali break); header "+ Report a problem" opens Jobs.
- Rules: pattern as DSK-HRP-001; done items stay in the "done" total.

**DSK-SEC-002 · Must · MVP · flag: mod.it_helpdesk · [Design]**
The in-charge can see one jobs log for security and IT, filtered by type, with Dhruva grouping repeats.
- Acceptance: "Jobs · 6 open" with filters "All", "Security", "IT"; each row shows title, type, location, report time, status chip and priority chip (Urgent, High, Normal, Low); sorted New, Assigned, In progress, Resolved.
- Acceptance: When 9 teachers report the same Wi-Fi fault, Then one job exists ("Dhruva grouped 9 reports into one job") and all nine reporters are linked to it.
- Rules: with ai.security_triage off, jobs are not grouped, priority is set by the reporter's category and no assignee is suggested.

**DSK-SEC-003 · Must · MVP · flag: mod.it_helpdesk · [Design]**
The in-charge can open a job, assign it and move it to resolved; the reporter is told.
- Acceptance: The detail shows reporter, time, description, four-step bar and "Dhruva suggests" (person, role, reason such as "free now · 1 minute away"); "Assign <name>" flashes "<name> assigned · told on his phone"; then "Mark in progress" and "Mark resolved" ("Resolved · <reporter> told").
- Acceptance: A resolved job appears under Systems > "Recently fixed" with technician and time taken.
- Rules: [Spec] any staff member can report a problem from their app (form in Section 7), including a photo and location; a job with no update for 24 hours at High or Urgent is escalated to the in-charge's principal.

**DSK-SEC-004 · Must · MVP · flag: mod.security_gate · [Design]**
Gate staff and the in-charge can manage visitors: approve waiting visitors, check out, and register walk-ins.
- Acceptance: Counters "Expected today", "On campus", "Waiting", "Checked out"; "Waiting for their host" rows show visitor, host, purpose and minutes waiting with "Approve" ("<name> approved · badge printed"); "On campus now" rows have "Check out" ("<name> checked out").
- Acceptance: Walk-in panel: Meeting pills "Class teacher", "Admissions", "Accounts", "Principal's office", "✓ Photo taken at the gate tablet", "Ask the host to approve" ("Host asked to approve · usually under 5 minutes").
- Rules: "Nudge hosts" for visitors waiting over 10 minutes reminds hosts, and hosts approve in their own app. Phase note: full visitor management is Phase 2 in the roadmap and the simple gate log is pending client decision (see 6.8b).

**DSK-SEC-005 · Must · MVP · flag: mod.security_gate · [Design]**
The in-charge can verify early pickups against the authorised list.
- Acceptance: "Early pickups today · 4" lists child, class, collector, relationship and status ("Authorised", "Not on the list"); an authorised collector with a photo match offers "Allow and log" ("<child> signed out · parent told"); an unlisted collector offers "Call parent" and only after "Parent confirmed · pickup allowed and logged with photo" can the pickup be allowed.
- Rules: an unlisted adult can never be released without a parent call; every pickup is logged with photo, time and guard and the parent is told. Early-pickup parent alerts cannot be turned off (see Section 7).

**DSK-SEC-006 · Must · MVP · flag: mod.it_helpdesk · [Design]**
The in-charge can see the health of systems and an exam-readiness checklist.
- Acceptance: Six tiles (Internet, Wi-Fi, CCTV, Smart boards, Printers, Backup) with status OK / Watch / Down and counts; tile buttons "Open the job" / "Raise a job" ("Job raised for the 2 smart boards · Mr. Sunil Kumar assigned").
- Acceptance: "Ready for Term 1 exams?" lists checks (strongroom camera, wall clocks in all exam rooms, PA, spare toner) with "Assign the remaining checks"; "Recently fixed" shows count and average time.
- Rules: status colour derives from linked jobs and alerts, never typed in; resolving the Wi-Fi or CCTV job turns the tile and checklist item green. [Spec] device status comes from monitoring feeds where available; otherwise from jobs only (the MVP has no CCTV feed).

**DSK-SEC-007 · Should · MVP · flag: mod.security_gate · [Design]**
The in-charge can see guards and technicians on duty and fill the night roster fairly.
- Acceptance: "Guards on duty" with post and status ("At post", "On a job"); technicians with live job counts; "Night guards · Diwali break" shows a roster with red "No guard yet" gaps; "Fill the 3 gaps with Dhruva" fills them and tells guards on WhatsApp ("3 nights filled · guards told on WhatsApp").
- Rules: fairness: no more than 2 nights per guard and a rest day after each night; Dhruva proposes and the in-charge accepts.

**DSK-SEC-008 · Should · MVP · flag: mod.hr_leave · [Design]**
The in-charge uses the staff "Me" page as in DSK-HRP-018 (in charge: Mr. Baldev Singh runs gates, Mr. Ajay Pal the IT desk). Ask Dhruva (ai.assistant_chat) answers "What is still open today?", "Is everything ready for Monday's exams?", "How many visitors came this week?".

### Transport in-charge (DSK-TRN)

Actors: Transport in-charge (sample: Mr. Vinod Bhatt) on desktop; Bus attendant on phone only (Section 7). Sidebar: Today, Live board, Safety checks, Parent messages, Routes & students, Fleet, Transport fees, Reports, Me. Scope: all buses and riders of the campus (sample: 24 buses, 1,046 children).

**How the attendant's taps drive this desktop (see Section 7, Bus attendant app).** The attendant app records four event kinds: stop arrival ("Reached stop"), per-child result ("On the bus", "Not here", "Left at the stop", "Handed to <person>" or "Stays on the bus"), trip start/finish ("Reached school") and SOS or help requests. The desktop never asks anyone to enter this data: it consumes it. Bus position and status on the Live board (no GPS), boarded counts on Today, headcount mismatches on Safety checks, parent-message facts and the incident counts on Reports are all derived from these events. GPS feeds only speed and route-deviation alerts (DSK-TRN-006).

**DSK-TRN-001 · Must · MVP · flag: mod.bus_live · [Design]**
The in-charge sees an emergency banner above everything and can dispatch a spare bus in one tap.
- Acceptance: Given a breakdown, Then a red "EMERGENCY · NOW" banner shows bus, place, children on board, cause, spare bus ETA and "Dhruva wrote the message to 38 families"; "Send spare bus and tell parents" flashes "Bus 25 sent with Mr. Kishore · 38 families told · school informed" and the banner becomes "Bus 14 handled · spare Bus 25 reaches the children at 7:31 am · parents told".
- Acceptance: "Call bus" flashes "Calling <attendant>…".
- Rules: the family message goes in English and Hindi and is shown to the in-charge before sending in the bus detail; in the banner the one-tap action is the in-charge's approval. [Spec] a breakdown banner stays until the in-charge marks it handled; the board and the banner never disagree on bus state.

**DSK-TRN-002 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can clear a Dhruva-prepared queue and see transport KPIs.
- Acceptance: Cards (pattern of DSK-HRP-001): bus not started ("Call Mrs. Meena"), late bus ("Tell parents"), route review ("Send options"), parent messages ("Open messages"), riders without fee ("Review"), papers due ("Book renewals").
- Acceptance: KPI tiles "Buses out", "Children on board", "Late or stopped", "Transport fees 92%"; "Buses right now" mini-list with link to Live board; safety tile "7 safety checks need you" opens Safety checks; header "+ Update parents" lets the in-charge pick one bus or all and Dhruva drafts in English and Hindi.
- Rules: Today counts and nav badges follow live events; "Tell parents" sends the worked-out new time per stop ("36 families told the new time for their stop").

**DSK-TRN-003 · Must · MVP · flag: mod.bus_live · [Design]**
The in-charge can see where every bus is from the attendants' stop taps, for morning pickup and afternoon drop.
- Acceptance: Tabs "Morning pickup" / "Afternoon drop"; one row per bus with route, current place, children boarded of capacity, status chip (on time green, late amber, needs you red, at school blue) and a dot trail of stops; "16 more buses on time · showing the 8 that matter now".
- Acceptance: The bus detail shows registration, status, route, attendant and driver, "22 of 38 picked up", a stop list with times and counts ("due 7:08" for future stops), "Call attendant" and "Message parents" (draft shown, "you check before it goes"), and for a breakdown the "Breakdown checklist · Spare bus, parents and school in one step".
- Acceptance: Afternoon drop shows per bus "33 of 41 handed over · 8 on the bus", the next stop, and exceptions such as a child kept on the bus ("Mother called · will collect from school at 2:45 pm") and closed trips.
- Rules: "works without GPS"; a bus with no tap for longer than its expected gap (default 10 minutes [Spec]) shows a grey "No update" state and appears on Today.

**DSK-TRN-004 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can run the headcount check: bus taps against class attendance.
- Acceptance: "812 boarded · 806 checked into class" lists mismatches with times (boarded at 7:21, marked absent at 8:10), chip "Check now" or "Check", and actions "Alert <class teacher>" ("<teacher> told · <child> is on campus, not in class") and "Ask the class teacher"; explained cases show no action.
- Rules: a mismatch appears only after class attendance is marked or the cut-off passes. See DSK-TRN-005.

**DSK-TRN-005 · Must · MVP · flag: mod.bus_live · [Design]**
The in-charge can review speed and route alerts from GPS and mark them handled.
- Acceptance: Rows show bus, kind (Speed, Route), detail ("Overspeeding: 62 km/h on Sohna Road (limit 40)"), time and action ("Call the driver" with "logged in the driver's record", "Ask the attendant", "Mark as seen" with "Logged"); handled rows read "Handled".
- Rules: speed limit is 40 km/h in the city (configurable); with ai.transport_alerts off, raw alerts still list but Dhruva's grouping and drafted messages are off.

**DSK-TRN-006 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can cover absent or late drivers and attendants.
- Acceptance: "Staff cover today" lists each bus with "Needs cover" / "Covered"; "Send cover" with a named spare ("Mrs. Kamla Devi (at school, 6 km away)") flashes "Mrs. Kamla Devi sent to Bus 21" and the row reads "Covered · ... 34 families told"; a half-day cover can span both drops.
- Rules: covering staff get the bus's attendant view for that trip [Spec]; the Live board shows the bus as Late when a cover is sent before departure.

**DSK-TRN-007 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can answer parent transport messages with the facts attached.
- Acceptance: Threads are tagged by bus and type (Late bus, Pickup by someone new, Stop change, Complaint, Fee) with status New / Replied / With coordinator; each shows "What Dhruva found" (from taps, the pickup list and the fee ledger) and an editable drafted reply.
- Acceptance: "Send reply" flashes "Reply sent to <name>" ("✓ Reply sent on the app, with an SMS backup"); "Forward to coordinator" flashes "Forwarded to <coordinator> · <name> told".
- Rules: a request for pickup by a new person is never approved here: the reply asks the parent to add the person with a photo under Pickup in the parent app. With ai.reply_drafts off, the reply box is empty and facts are still shown.

**DSK-TRN-008 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can plan route changes with seat, time and fee impact, then approve them.
- Acceptance: "Children to move" lists each child with reason and current bus; Dhruva's options per child are labelled "Fits" or "Bus is full" and show added minutes, seats free now and after, fee slab change (for example "₹2,800 -> ₹3,300 a month (over 10 km)"), families affected and a new stop-time table.
- Acceptance: "Approve and tell everyone" is disabled for unsuitable options; on approval: "Route updated · <parent> told the new pickup time · 12 families told the new stop times · attendant's list updated" and "✓ Approved · <child> moves to Bus 9 from Monday · parents, attendant and fee bill updated".
- Acceptance: Route pills (Bus 7, 9, 12, 21) show stops, times and children per stop with a seat bar (full in red).
- Rules: a full bus cannot take a child; slabs apply automatically (Up to 5 km ₹2,200; 5 to 10 km ₹2,800; over 10 km ₹3,300 a month, tenant-configurable [Spec]); the fee change is billed through the fee ledger after the principal's fee policy. Route review options for many riders go to the principal ("Send options").

**DSK-TRN-009 · Must · MVP · flag: mod.transport · [Design]**
The in-charge can track fleet papers and service and book renewals.
- Acceptance: Table Bus, Registration, Seats, Insurance, Fitness, Permit, Pollution, Service, dates ending this month in red; banner "Bus 7's fitness certificate ends 20 Oct and Bus 18's insurance ends 28 Oct" with "Book both renewals" ("Fitness test booked for Bus 7 · Bus 18 insurance renewal sent to accounts").
- Acceptance: Bus detail offers "Book the renewal", "Send spare bus", "Book a service" ("Service booked · Sat 17 Oct"), "Message driver" (drafted for review).
- Rules: [Spec] alerts at 30, 14 and 7 days before expiry; an expired fitness or insurance blocks the bus from the roster until the in-charge records a renewal with a reason.

**DSK-TRN-010 · Must · MVP · flag: mod.fees · [Design]**
The in-charge can see transport fees against routes and costs and fix mismatches with the fee ledger.
- Acceptance: Totals (Billed, Collected, Still due, Running cost a month) and "By route · October" table (Children, Paid, Due, Fees, Cost, Surplus; negative in red); "Sync now" flashes "Fees synced from accounts · 4 new payments since 7:20 am".
- Acceptance: "23 children ride without a transport fee" offers "Bill from October" ("23 families billed for transport from October · accounts told"); "6 families pay but aren't on any route" offers "Ask: add a stop or refund"; "Remind 41 families with dues" sends WhatsApp reminders with a pay link.
- Rules: the check runs on every sync; billing changes are made by accounts through the fee ledger and the in-charge's button creates a request to accounts [Spec].

**DSK-TRN-011 · Should · MVP · flag: mod.reports · [Design]**
The in-charge can read transport reports for the principal.
- Acceptance: Period pills "October to date", "Term 1", "This session"; KPI tiles (On-time arrivals vs target, Average delay, Cost per child a month, Seats used); weekly on-time bars; incident counts against last month (Breakdowns, Speeding alerts, Child not handed over, Late start by attendant, Parent complaints); "By route" table; "Download Excel / PDF".

**DSK-TRN-012 · Should · MVP · flag: mod.hr_leave · [Design]**
The in-charge uses the staff "Me" page as in DSK-HRP-018 (in charge: Mr. Mahesh Rana). Ask Dhruva (ai.assistant_chat) answers "Which buses are late most often?", "Is transport paying for itself?", "Which buses have seats free?" with sources.

### Student desktop, Classes 6 to 8 (DSK-STM)

Actor: middle-school student (sample: Myra Kapoor, 7-B). Sidebar: Home, Timetable, Homework, Notes & revision, Ask a teacher, Marks, Attendance, Holistic progress, Leave. A student sees only their own data; parents see the same marks and homework in the parent app. Tone: friendly and game-flavoured; no rankings between children.

**DSK-STM-001 · Must · MVP · flag: mod.student_learning · [Design]**
The student sees three daily quests picked by Dhruva from teacher-set work, one card at a time.
- Acceptance: Home shows the focus card "3 THINGS NEED YOU · 1 OF 3" with "Start homework" / "Start" and "Later ›", an "Up next" list, "Today's quests · 0 of 3 done" and a "How it works" link ("Dhruva picks 3 a day from work your teachers set. Each one adds XP, house points and a step toward a badge.").
- Acceptance: Each quest row shows title, source line, "+30 XP", "+3 house pts", the badge it feeds and a "Go" button; done quests turn green with a tick; when all done: "All 3 quests done · streak saved! Come back tomorrow for new ones."
- Rules: quests come only from teacher-set homework, notes and quizzes; with ai.student_tutor off, the three quests are the three earliest-due teacher items.

**DSK-STM-002 · Should · MVP · flag: mod.student_gamification · [Design]**
The student earns XP, levels and a streak, and gives house points.
- Acceptance: The level card shows "Level 7 · Explorer", XP to next level, streak and progress bar; Level 8 "Navigator" at 1,500 XP; completing a quest updates XP, the bar and house points live.
- Rules: 10 XP = 1 house point; XP is awarded on first correct answers only (a retry round gives "practice only, no extra points"); the streak counts days with at least one completed quest [Spec]. Switching the flag off hides XP, levels, streaks, house points and badges and leaves quests as a plain to-do list.

**DSK-STM-003 · Should · MVP · flag: mod.student_gamification · [Design]**
The student can view the house cup and six badges.
- Acceptance: "House cup" lists four houses with points and "You gave Raman 45 points this week"; "Badges" shows Homework hero, Quiz champ, Note ninja, Curious mind, Perfect week, Bookworm with progress and the quests that feed each.
- Rules: house totals are public across houses; personal marks are not.

**DSK-STM-004 · Should · MVP · flag: ai.student_tutor · [Design]**
The student can play a five-question warm-up quiz.
- Acceptance: Five questions of three options; after answering the correct option turns green with a one-line reason; toasts "Correct! +10 XP" / "Not quite · see why below"; summary "Full marks! 5 of 5" with "+50 XP · Quiz champ +1" or "N of 5 right"; "Try again" gives "New round · practice only, no extra points".
- Rules: questions derive from yesterday's lesson and teacher notes. Phone-only subject games ("Maths pop") and whiz badges are specified in Section 7.

**DSK-STM-005 · Must · MVP · flag: mod.timetable · [Design]**
The student can see the class timetable by day and week, with the date sheet.
- Acceptance: "Day | Week" switch; weekday pills; eight periods with subject, teacher and a "NEXT" tag on today's view; break after P4; date-sheet chips for the term exams on Home (not tappable).
- Rules: shows the class's own published timetable, including cover teachers [Spec]. The school calendar is phone only in the design; see 6.8b.

**DSK-STM-006 · Must · MVP · flag: mod.homework · [Design]**
The student can open homework and submit it by photo, file or typing.
- Acceptance: The list shows subject, due or set date and chip "To do" (+XP), "Submitted", "Returned · 8/10"; a "To do" item offers "Photo of my notebook", "Upload a file", "Type my answer" then "Submit".
- Acceptance: Submit without a choice toasts "Pick how you want to submit"; success toasts "Submitted on time · +30 XP", the chip becomes "Submitted" and the badge count drops; a returned item shows marks and teacher feedback.
- Rules: [Spec] late submissions are accepted and marked "Late" (the design shows no late rule; see 6.8b); photo uploads are compressed and virus-scanned; max 10 files and 25 MB per submission.

**DSK-STM-007 · Should · MVP · flag: mod.lesson_plans · [Design]**
The student can read teacher notes, save them offline and practise from them.
- Acceptance: Notes show subject, teacher, date and "NEW"; opening shows key points, "Save offline" ("Saved for offline reading") and "Practise 8 questions from this sheet" ("Practice opened · Dhruva marks it and shows the steps you missed"); opening clears NEW and counts toward Note ninja.
- Rules: flag note: teacher notes are published through the teacher's Make area; offline save on desktop uses browser storage only.

**DSK-STM-008 · Must · MVP · flag: ai.student_tutor · [Design]**
The student can ask a question and get a hint first; the teacher is reached only after "Still stuck?".
- Acceptance: Choose a subject, type, "Ask" shows "Dhruva's hint · A nudge, not the answer"; "Got it now" toasts "Great! +5 XP for working it out"; "Still stuck? Ask <teacher>" sends it ("Sent to <teacher> · you'll get a reply here") and the thread appears under "My questions". Empty question toasts "Type your question first".
- Rules: Dhruva gives hints, not answers ("I won't do your homework for you, but I'll help you get there"). With ai.student_tutor off, "Ask" goes straight to the subject teacher.

**DSK-STM-009 · Must · MVP · flag: mod.marks_results · [Design]**
The student can see marks and attendance (read-only), visible only to the student and parents.
- Acceptance: Marks shows "Unit test 3 · out of 40" per subject with a bar, percentage and change versus the last test; footnote "Only you and your parents see your marks." Attendance shows percent, days present and an October calendar with absence reasons.
- Rules: marks appear only after the teacher releases them (parent and student see the same numbers).

**DSK-STM-010 · Should · MVP · flag: mod.report_cards · [Design]**
The student can read the holistic progress card and save a reflection.
- Acceptance: Six domains with four levels (Beginner, Progressing, Proficient, Advanced), activities, teacher remark and "In my own words" with "Save my reflection" ("Saved · your class teacher sees it on your progress card").

**DSK-STM-011 · Must · MVP · flag: mod.attendance · [Design]**
The student can apply for leave, confirmed first by a parent and then approved by the class teacher.
- Acceptance: From, To, reason pills ("Unwell", "Family function", "Doctor's appointment", "Other"), details; the button steps "Pick the dates" -> "Pick a reason" -> "Send · Wed 21 Oct – Thu 22 Oct"; toasts "Sent to Mrs. Ritu Kapoor to confirm", then "Leave approved by Ms. Pallavi Shah".
- Acceptance: End before start shows "The end date is before the start date"; Sundays are not counted.
- Rules: if the parent does not confirm within 48 hours the request lapses and the student is told [Spec].

**DSK-STM-012 · Could · MVP · flag: ai.assistant_chat · [Design]**
The student can ask "What should I revise first?" and "What homework is due?" in a side panel with sources; other questions get "I help you plan revision and give hints. I won't do your homework for you, but I'll help you get there."

### Student desktop, Classes 9 to 12 (DSK-STS)

Actor: senior student (sample: Navya Reddy, 10-C). Same sidebar as STM. No XP or levels: "study points". A student sees only their own data.

**DSK-STS-001 · Must · MVP · flag: mod.student_learning · [Design]**
The student sees an Exam Mode banner and the day's focus cards.
- Acceptance: Banner shows "3 days to Term 1", first paper line (subject, date, time, hall and seat), readiness ring, streak and points; focus card "3 THINGS NEED YOU · 1 OF 3" starts with homework ("Start homework") then study tasks ("Mark as done").
- Rules: banner appears from 14 days before the first exam [Spec]; seat info shows when the exam cell publishes seating.

**DSK-STS-002 · Must · MVP · flag: ai.student_tutor · [Design]**
The student sees a daily study plan made by Dhruva from marks and the date sheet.
- Acceptance: "Today's study plan · 0 of 3 done" lists timed items with reason, points, house points, the achievement fed and "Open the revision sheet" (jumps to the linked note); ticking a task toasts "Nice work · +20 study points"; all done reads "Plan done for today · +70 points earned. Take a break!".
- Rules: plan items derive from weak spots under "Work on these" (with evidence such as "Unit test 3 · 2 of 5 wrong"). With the flag off, the plan is replaced by the date sheet and teacher notes list.

**DSK-STS-003 · Must · MVP · flag: ai.student_tutor · [Design]**
The student can see how ready they are for each exam and how the score is worked out.
- Acceptance: "How ready am I?" shows two bars per subject (Revised, Practice) and an overall ring; "How your 77% is worked out" explains: per subject the average of Revised (share of topics ticked off) and Practice (average of practice sets and class tests in the last 30 days); overall is the average of the five subjects; tip "Fastest way up: ...".
- Rules: readiness for a subject updates once a timed paper is scored.

**DSK-STS-004 · Should · MVP · flag: ai.student_tutor · [Design]**
The student can take a five-question quick practice from past board papers with reasons shown.
- Acceptance: Summary "Full marks! 5 of 5 · +50 study points" or "N of 5 right"; reason after each answer.

**DSK-STS-005 · Should · MVP · flag: ai.student_tutor · [Design]**
The student can sit a timed past-paper practice marked by Dhruva.
- Acceptance: A 15:00 countdown (red below 2 minutes), question buttons 1 to 6 with marks, "Next question" / "‹ Back", "0 of 6 answered", "Pause and leave" ("Practice paused · your answers are saved"); time up submits automatically; "Submit · Dhruva marks it" shows score ring, "Finished in m:ss of 15:00", "+30 study points · Board ready +1" and a per-question review with worked solutions; "Try new questions" ("Dhruva made 6 new questions on the ones you missed").
- Rules: the design intends the plan item "Maths · 10 past board questions (timed)" to open this screen but the built button is "Mark as done"; this spec requires the link (see 6.8b). Only a submitted paper counts toward Board ready and readiness.

**DSK-STS-006 · Should · MVP · flag: mod.student_gamification · [Design]**
The student can see house standing and six achievements (Board ready, Problem solver, Steady scholar, Doubt clearer, Full month, Top 10%); 10 study points = 1 house point.

**DSK-STS-007 · Must · MVP · flag: mod.timetable · [Design]**
The student can see the class timetable (day, week) and date-sheet chips; the school calendar with class-specific events is phone only in the design.

**DSK-STS-008 · Must · MVP · flag: mod.homework · [Design]**
The student can open and submit homework (photo, file, typed) as DSK-STM-006; success toast "Submitted to <teacher>" (no XP); returned items show marks, feedback and "Checked by Dhruva, returned by <teacher>".
- Rules: Dhruva pre-checks and the teacher releases marks.

**DSK-STS-009 · Should · MVP · flag: mod.lesson_plans · [Design]**
The student can read revision notes, save offline and "Practise 5 questions from this sheet" as DSK-STM-007.

**DSK-STS-010 · Must · MVP · flag: ai.student_tutor · [Design]**
The student can ask a question with hint first; "Got it now" saves to the doubts list ("Saved to your doubts list", no XP); "Still stuck? Ask <teacher>" sends it; closed doubts feed "Doubt clearer".

**DSK-STS-011 · Must · MVP · flag: mod.marks_results · [Design]**
The student can see marks and attendance read-only (as DSK-STM-009) with change since the last test, visible only to student and parents.

**DSK-STS-012 · Should · MVP · flag: mod.report_cards · [Design]**
The student can read the holistic card: co-scholastic grades, life skills, career line (with counsellor session date), activities, class-teacher remark, and save a reflection ("My goal for Term 1, and how I will reach it").

**DSK-STS-013 · Must · MVP · flag: mod.attendance · [Design]**
The student can apply for leave with the same two-step approval as DSK-STM-011 (parent confirms, class teacher approves).

**DSK-STS-014 · Could · MVP · flag: ai.assistant_chat · [Design]**
The student can ask "What should I revise first?" and "What homework is due?" with sources and attendance stat chips.


## 6.4 Business rules and policies

| ID | Rule | Tag |
|---|---|---|
| R-01 | Dhruva prepares, drafts and suggests; a person approves anything that changes a record or reaches a family. No AI action is silent. | [Design] |
| R-02 | Concessions above Rs 25,000 go to the group owner; the limit is copied with campus settings and is editable per tenant. Refunds follow "Unused full months, minus 10%". New teaching posts always go to the owner. | [Design] |
| R-03 | Campus needs attention when attendance or fees are below 90%; the group attendance target is 92%; the Absence watch default is 85%; CBSE minimum is 75%. | [Design] |
| R-04 | Leave routing: teacher to HoD (up to 2 days outside exam weeks, else principal); HoD to vice principal (principal over 2 days); coordinator, exam cell and counsellor to principal; principal to group HR head (chairman too over 3 days); standalone Admin to the trustee. | [Design] |
| R-05 | Teacher notices to parents wait for principal approval unless the campus rule is "Send directly". | [Design] |
| R-06 | Report cards, results and the timetable reach families only after approval (principal for results; coordinator for timetable). | [Design] |
| R-07 | Cover is the academic coordinator's job; invigilation is the exam cell's; the principal sees who is away but assigns neither. | [Design] |
| R-08 | A class with an open timetable clash is never approved; an approved class needs a new version to change; the old timetable stays live until the start date. | [Design] |
| R-09 | Attendance is default-present; submitted registers lock for the teacher. A correction after submission is made by the class teacher with a reason and shown to the coordinator; HR verifies corrections affecting pay. | [Design] locked state; correction flow [Spec] |
| R-10 | Counsellor notes and case history are private to the counsellor; sharing is an explicit act. | [Design] |
| R-11 | New students are counted only when the admission fee receipt exists. | [Design] |
| R-12 | Every approval, decline, send and publish is logged with user, role, time, target and note (see XCT audit). | [Design] "every decision is logged" + [Spec] |
| R-13 | Scope: Owner reads all campuses; Principal, Coordinator, Exam cell, Counsellor see one campus; HoD one department; Teacher own classes; Admin one standalone school. Cross-tenant access is impossible. | [Design] + [Spec] |
| R-14 | A one-tap action has no confirmation dialog when it is reversible or only sends a reminder; irreversible acts (approve and publish, publish date sheet, approve and share timetable, export to CBSE, close campus setup) show the result summary before confirming. | [Spec] |

## 6.5 Notifications and approvals raised by this section

| Trigger | To | Channel and tier | Tap opens |
|---|---|---|---|
| Approval waiting (concession, refund, post) | Owner | App, Normal; WhatsApp optional | Approvals |
| Approval decided | Requester | App, Normal | The request |
| Onboarding blocker or fixed sheet | Owner, campus lead | App, Normal | Onboarding |
| Setup finished | Owner, group office | App, Normal | Onboarding |
| Sections not marked by deadline | Principal, Admin | App, High in school hours | Today |
| Cover assigned or changed | Substitute, class teacher | App, High | Timetable |
| Plan or paper returned with feedback | Teacher | App, Normal | Reviews |
| Leave decided | Applicant, coordinator, HR | App, Normal | Leave |
| Timetable approved and shared | Teachers, HoDs, parents, students | App and WhatsApp, Normal | Timetable |
| Report cards approved | Parents, students | App, Normal | Results |
| Date sheet published | Teachers, students, parents | App and WhatsApp, Normal | Date sheet |
| Notice sent | Audience | App and WhatsApp, Normal | Notice |
| Absence recorded | Parent | WhatsApp, High if unmarked by 9 am | Attendance |
| Counsellor booking | Student | App, private, High | Sessions |

Approval chains raised here: fee concession (accounts, principal, owner); refund (principal, owner); new post (principal, owner); leave (R-04); paper (teacher, HoD, exam cell); plan (teacher, HoD, coordinator tracker); results (exam cell, principal); timetable (coordinator); notice (teacher, principal); trustee items for the standalone Admin. Quiet hours and tier behaviour follow Section XCT; Urgent tier is not used by desktop actions.

## 6.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| ch.desktop_web | Whole desktop app and shell | On | Off blocks desktop sign-in; phone unaffected |
| idm.web_login | Browser sign-in with staff PIN prompt | On | See DSK-SHL-011 |
| mod.profile_switching | Profile chip, bell, Ctrl + K | On | Single-profile users see no switcher |
| ai.assistant_chat | Ask Dhruva button | On | Button hidden when off |
| ai.focus_card | Focus card on Today | On | Plain ordered list when off |
| mod.group_scorecard | Overview, Campuses, Admissions (owner) | On | Group tenants only |
| mod.campus_onboarding | Onboarding, Add a campus, principal setup | On | Off after all campuses are live |
| mod.approvals | Approvals queues and chains | On | |
| mod.reports | Reports, print, export, scheduled emails | On | |
| mod.notices, ai.notice_drafts | Notices and drafts | On | Manual composer stays when AI is off |
| mod.calendar_ptm | Calendars | On | |
| mod.attendance, mod.fees, mod.payroll, mod.hr_leave | Attendance views, defaulters, payroll approval, Me leave and payslips | On | |
| mod.cover, ai.cover_suggestions | Cover table and suggestions | On | Manual pickers stay |
| mod.timetable, ai.timetable_generator | Timetable view, print; generator | On | Manual editing stays |
| mod.pace_tracking, mod.lesson_plans | Check-ins, plans, syllabus | On | |
| mod.exams, mod.marks_results, mod.report_cards | Papers, exam days, marks, report cards | On | |
| mod.homework, ai.homework_marking, ai.marks_from_photo, ai.paper_generator, ai.lesson_plan_drafts, ai.reply_drafts | Teacher tools | On | Manual path in every case |
| ai.remedial_grouping, ai.at_risk_detection | Remedial and check-in suggestions | On | |
| mod.counselling | Counsellor module | On | |
| mod.parent_messaging, mod.student_learning | Inbox, parent queries, notes | On | |
| mod.admissions_crm | Admin admissions tab | On | |
| NEW flags | See Proposed flags | On | |

## 6.7 Non-functional requirements (specific to this section)

- **DSK-NFR-01 Performance [Spec].** First screen after sign-in renders within 2.5 seconds at the 75th percentile on a 20 Mbps link; list screens of up to 5,000 rows page in 200-row chunks; badge updates within 2 seconds.
- **DSK-NFR-02 Timetable generation [Spec].** A whole-school draft (60 sections, 193 teachers, 41 rooms) completes within 60 seconds; the 4-second animation is a display minimum, not a target; a failure leaves the current timetable untouched and shows "Could not build a draft. Your current timetable is unchanged."
- **DSK-NFR-03 Autosave [Spec].** Wizards and long forms (Add a campus, campus setup, paper builder, lesson plan) autosave every 10 seconds and on step change; losing the tab never loses more than 10 seconds of input.
- **DSK-NFR-04 Concurrency [Spec].** Two people editing the same record see "Updated by <name> just now" and the second save is rejected with a refresh prompt (optimistic versioning).
- **DSK-NFR-05 Scale [Spec].** A group tenant of 50 campuses and 150,000 students loads Overview within 3 seconds using precomputed daily and hourly aggregates.
- **DSK-NFR-06 Exports [Spec].** Excel and PDF exports under 100,000 rows are generated in under 30 seconds; larger ones run as background jobs with a link by email.
- **DSK-NFR-07 Privacy [Spec].** Counsellor data is encrypted separately at rest; support and platform staff cannot read it; masked phone numbers on lists; exported lists carry a footer naming the user and time.
- **DSK-NFR-08 Availability [Spec].** 99.5% monthly in school hours (7 am to 5 pm IST) with planned maintenance on Sunday nights.

## 6.8 Open questions (this half)

1. **OQ-6a-01 Class observation.** The HoD design offers "Book a class observation", but the Project record says teacher observations were dropped on 11 Oct as too intrusive. Spec treats it as not built; confirm removal of the slot picker and the "HISTORY" observation lines.
2. **OQ-6a-02 Trustee.** No trustee screen exists. Confirm whether the trustee signs in on the desktop app (assumed, with a three-item view) or approves from WhatsApp only.
3. **OQ-6a-03 Owner add-event.** Phone Calendar lets the owner add events; desktop does not. Confirm whether owner-added events apply to one campus or all and whether principals see them.
4. **OQ-6a-04 Add a campus.** The code also contains a quick-add dialog. Confirm the six-step wizard is the only path and whether more than one draft may exist.
5. **OQ-6a-05 Quiet hours.** Boards say 9 pm to 6 am and 9 pm to 7 am; desktop shows no quiet hours but sends reminders. Confirm one default (Section XCT).
6. **OQ-6a-06 Principal's Ask Dhruva scope.** Free text is limited to four topics in the MVP; confirm whether the owner's panel may answer cross-campus questions beyond the three samples.
7. **OQ-6a-07 Absence correction.** The designs lock a submitted register but show no correction path; confirm who may correct and whether parents are re-notified.
8. **OQ-6a-08 Phasing.** Exam seating/duties, date sheets and CBSE registration are in the MVP table; confirm whether they are MVP or P2 for pilot campuses.
9. **OQ-6a-09 Report scheduling.** Confirm that scheduled emails to external addresses (CFO) need a tenant-level allow list for data protection.
10. **OQ-6a-10 Languages.** The app has six languages; notices and Dhruva support two (English, Hindi). Confirm desktop language scope.


## 6.4b Business rules

| # | Rule | Applies to |
|---|---|---|
| BR-1 | Dhruva prepares, a person approves anything that changes a record, moves money or reaches a family. One-tap "do the whole step" buttons are the person's approval of Dhruva's draft. | All DSK-xxx |
| BR-2 | Maker-checker: nobody approves their own entry. Above ₹2 L (tenant-configurable) a second approver, the principal, is also required; the second approver is never the maker or first approver. | DSK-FIN-003/004 |
| BR-3 | Approval limits (tenant-configurable, sample): fee concession above ₹25,000 to the owner; hardship concessions: accounts check, principal recommends, owner approves; purchase order above ₹50,000 to the principal, above ₹5 L to the owner; contract invoice above ₹1 lakh to the principal; leave over 3 days to the principal then group HR head. | FIN, HRP |
| BR-4 | A month lock stops posting and edits; later changes need the principal's approval. A closed account year is view-only. | DSK-FIN-016 |
| BR-5 | Payroll gates: attendance cannot lock while corrections are open; approval cannot be requested while exceptions remain; the bank file cannot be released before approval; a paid run is immutable. | DSK-HRP-009 to 013 |
| BR-6 | Each employee is in exactly one payroll; an employee with a signed contract in no payroll is flagged. | DSK-HRP-014 |
| BR-7 | Leave over balance: comp-off first, then unpaid; comp-off comes only from approved extra duty. | DSK-HRP-007 |
| BR-8 | Final settlement is blocked until every document, clearance and asset line is received; gratuity applies after 5 years of service; approval by the principal. | DSK-HRP-017 |
| BR-9 | Bank reconciliation: bounced cheque reverses the receipt and adds a ₹500 charge (tenant-configurable); "Ignore" and "Hold" post nothing. | DSK-FIN-012 |
| BR-10 | Vendor payments deduct TDS by the vendor master section and rate; MSME vendors are paid within 45 days; vendors on hold are excluded from batch payment. | DSK-FIN-010 |
| BR-11 | Admissions: offers are valid 7 days; waitlist order is date, then sibling and staff-child priority; admission happens only when the admission fee is recorded or paid. Seat status: under 25% filled flagged amber; offers at or above seats flagged red. | DSK-ADS-007/008 |
| BR-12 | Gate: an unlisted adult is never given a child without a parent call (or parent code on the bus); every pickup is logged with photo and the parent is told. | DSK-SEC-005, DSK-TRN-003 |
| BR-13 | Night roster fairness: at most 2 nights per guard and a rest day after each night. | DSK-SEC-007 |
| BR-14 | Transport: a full bus cannot take a child; fee slabs by distance apply automatically; a route change updates parents, the attendant list and the fee bill; speed limit 40 km/h in the city. | DSK-TRN-008 |
| BR-15 | Bus status comes from attendant taps, not GPS; GPS drives only speed and route alerts. | DSK-TRN-003/005 |
| BR-16 | Students: marks and attendance are visible only to the student and parents; house totals are public. Dhruva gives hints, not answers; the teacher is contacted only after "Still stuck?". | DSK-STM/STS |
| BR-17 | Student leave needs the parent's confirmation, then the class teacher's approval; Sundays are not counted. | DSK-STM-011 |
| BR-18 | [Spec] Retention: audit entries, vouchers and payroll records 8 years; CVs 12 months after the post closes; gate visitor and pickup logs 1 year; tour and call logs for the season plus 1 year; job logs 2 years; student quiz and practice data for the session plus 1 year. | All |
| BR-19 | [Spec] Money is stored in paise as integers, rounded half-up at line level; all times are Asia/Kolkata; every record change writes an audit entry. | All |

## 6.5b Notifications and approvals

| Trigger | To | Channel | Approver or action |
|---|---|---|---|
| Payroll run sent for approval | Principal | App push (High) | Approve or return; HR told |
| Salary account short before pay date [Spec] | HR, accounts in-charge, principal | App push (Urgent) | Accounts schedules transfer |
| Attendance correction verified or rejected | Employee (and HoD) | App push | None |
| Leave issue settled | Employee | App push ("told on the app") | None |
| Joiner reminder, document renewal, police verification forms | Joiner, employee | WhatsApp | None |
| Probation review requested | HoD | App push | HoD review |
| Final settlement | Principal | App push | Approve |
| Approval item created (voucher, bill, concession, journal, refund) | Accounts in-charge, then principal/owner by limit | App push | Approve or send back with note; maker told |
| Fee reminders with pay link | Families | WhatsApp, app | Accounts sends |
| PO | Vendor | Email, WhatsApp | After approval limits |
| Bounced cheque | Parent | App, WhatsApp | Accounts sends |
| Filing pack | CA | Email | CA files |
| Welcome, tour confirmation, application link, offer, fee reminder, Open House | Families | WhatsApp (English and Hindi) | Counsellor |
| Admission fee recorded | Accounts, class teacher | App | None |
| Job assigned, job resolved | Assignee, reporter | App push | None |
| Camera job assigned (exam week) | Exam cell | App push | None |
| Visitor waiting over 10 minutes | Host | App push (High) | Host approves |
| Early pickup | Parent | App push (Urgent, cannot be turned off) | Parent call if unlisted |
| Night roster filled | Guards | WhatsApp | None |
| Breakdown, late bus, stop change, staff cover | Families on the bus | App push, WhatsApp, SMS backup | In-charge sends |
| Child not at stop, left at stop, stays on bus | In-charge, parent | App push (Urgent) | In-charge calls |
| SOS | In-charge, principal, driver | App push, call (Urgent) | In-charge calls attendant within 2 minutes |
| Route review options | Principal | App push | Principal decides |
| Student leave request | Parent, then class teacher | App push | Parent confirms; teacher approves |
| Student doubt after "Still stuck?" | Subject teacher | App push (Normal) | Teacher replies |

Quiet hours and tiers follow XCT (Urgent breaks quiet hours; High waits overnight outside school hours; Normal is grouped). Students from Class 6 receive homework and results notifications only; no marketing is sent to students.

## 6.6b Feature switches

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| mod.payroll | HR payroll runs and setup (DSK-HRP-009 to 014) | On | Off: data kept, staff payslips from last run remain visible |
| mod.hr_leave | Employee records, corrections, leave issues, staff Me page | On | "Me" leave page on every staff role depends on it |
| mod.hiring_onboarding | Joiners, openings, shortlists, exits | On | |
| ai.payroll_checks | Exception flags and recommended choices | On | Off: manual review, gates unchanged |
| mod.fees, ai.fee_followup | Fee views, deposit slip, reminders; drafted wording | On | |
| mod.finance_accounts | Today, vouchers, ledgers, setup, reports, compliance, month-end | On | |
| mod.approvals | Approvals queue and second-approver rule | On | Cannot be off while mod.finance_accounts is on [Spec] |
| mod.bank_recon, ai.bank_matching | Reconciliation; auto-matching | On | |
| mod.tally_sync | Tally connector | Off until configured | P2 per roadmap |
| mod.reports | Report hubs (finance, admissions, transport) | On | |
| mod.procurement_inventory | Purchases, vendors, inventory, assets | Off | P3 per roadmap |
| ai.finance_assist | "✦ Fill in" on vouchers | On | |
| ai.hr_assist | Dhruva's CV shortlist | On | |
| mod.admissions_crm, ai.admissions_scoring | Admissions CRM; temperature and next step | On | |
| mod.it_helpdesk, mod.security_gate, ai.security_triage | Jobs and systems; gate and roster; grouping and assignee suggestion | On | Gate default may be Off pending client decision |
| mod.transport, mod.bus_live, ai.transport_alerts | Fleet, routes, fees, messages; live board and safety; grouped alerts and drafts | On | Safety checks and SOS remain (core) |
| mod.student_learning, ai.student_tutor | Quests, study plan, readiness, hints, timed paper | On | |
| mod.student_gamification | XP, levels, streak, house points, badges, achievements | On | Per campus and per class band |
| mod.homework, mod.marks_results, mod.report_cards, mod.timetable, mod.attendance, mod.lesson_plans, mod.calendar_ptm | Student pages | On | Owned by other sections |
| ai.assistant_chat, ai.reply_drafts | Ask Dhruva panel; drafted replies | On | |

## 6.7b Non-functional requirements

- Performance [Spec]: Today pages render prepared cards in under 2 s at p95; one-tap actions confirm in under 1 s excluding external calls; lists of 5,000 rows (vouchers, employees, families) page or virtualise with search under 500 ms.
- Live board freshness [Spec]: a stop tap appears on the desktop within 5 s at p95; the desktop falls back to polling every 15 s if the live channel drops and shows "Reconnecting…".
- Offline [Spec]: the attendant app queues taps on the phone and replays them in order; the desktop shows the event time, not the sync time, and marks late-arriving taps.
- Tally and bank integrations [Spec]: retries with back-off, idempotent voucher keys (voucher number plus company), failed items surfaced, never silently dropped; bank feeds fetched at least daily.
- Security [Spec]: role-scoped access per campus; payroll, bank and salary fields masked for non-HR roles; masked parent phones in admissions (98110 ••219); approvals and payroll release require a fresh OTP if the session is older than 15 minutes; all exports watermarked with user and time.
- Auditability [Spec]: every approval, send, lock, payroll decision, pickup and SOS is immutable in the audit log with actor, device and time.
- Accessibility [Spec]: WCAG 2.1 AA; all status chips carry text, not colour alone; keyboard operation of every one-tap action; Hindi and English for family-facing messages.
- Data protection: parental consent per child under 18; student data never sold; DPDP roles as in XCT.
- Browser support [Spec]: current and previous two versions of Chrome, Edge, Safari, Firefox; layouts for 1280 px and wider, usable at 1024 px.

## 6.8b Open questions

1. Tally sync (Phase 1 in the roadmap) and purchases, vendors, inventory and budgets (Phase 2) appear in the finance prototype; confirm with the client whether they move into the MVP. This spec marks them P2 and P3.
2. Security and IT: visitor management and CCTV were Phase 2; the prototype shows a simple gate log. Confirm whether the gate ships in the MVP.
3. Sample data conflicts: Admissions headline "58 admitted of 410 seats" differs from per-grade admitted counts; the Security Today card says Diwali nights "22, 24 and 25 Oct" while the roster shows 8, 10 and 11 Nov. Which is correct?
4. Late homework: no late-submission rule is designed. Proposed here: accept and mark "Late".
5. Timed paper: the design intends the plan item to open the paper but the button is "Mark as done". This spec requires the link; confirm.
6. School calendar and subject games appear only on the student phone; should the desktop get the calendar (this spec says no)?
7. Group roles: group HR head and group finance head appear in routing text and Account main edit rights, but no group-level HR or finance screens exist here. Who builds them?
8. Reports hub: "Statutory dues" and "Budget vs actual" are drafted but not reachable. Include them?
9. Admissions offers: the designs show no principal approval for offers; confirm none is needed (this spec assumes none, with counsellor sending).
10. Transport: fee change from a route move changes the bill; who approves the billing change (accounts or in-charge)? This spec makes it a request to accounts.
11. Student leave: should an unconfirmed request lapse after 48 hours (assumed)?
12. HR for multi-campus groups: sample shows one campus; define whether HR sees other campuses (assumed no).
13. Retention periods in BR-18 need school or legal confirmation.


## Annex 6-A (part 1)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| Tenant, Campus | tenant_id, group_id?, campus_id, board, affiliation_no, udise_code, health_score | Standalone school is a tenant with one campus |
| Profile, StaffRole | profile_id, person_id, tenant_id, campus_id, role, locked | One row per number-tenant-role |
| ApprovalRequest | id, kind, raised_by, amount, policy_ref, state, current_approver, decided_by, note, decided_at | Kinds: concession, refund, post, leave, payroll, notice, results, safety_ack |
| CampusOnboarding | campus_id, batch, go_live, sheets[8] (state, rows_ok, rows_bad), training, parents_invited, draft_json | Draft per owner |
| CampusSetup | campus_id, step_state[9], answers_json, finished_at | Group-locked fields flagged |
| Notice | id, scope, audience_filter, channels, author, status, approved_by, circular_no | Read receipt and delivery tables |
| NoticeReceipt | notice_id, person_id, channel, read_at, delivered_at | |
| Report, ReportSchedule | report_key, params, format, recipients[], cadence, next_run, created_by | |
| CalendarEvent | id, campus_id, type, date, notify_flag, source | |
| CoverAssignment | id, date, period, class, subject, absent_teacher, substitute, why, state | Created from approved leave |
| PaceCheckin | teacher_id, class, date, status, reason | |
| LessonPlan | id, teacher_id, week, state, hod_comment, version | |
| Timetable, TimetableDraft | id, scope[sections], rules[], start_date, state, clashes[], approved_sections[], audience | Version chain |
| Paper | id, setter, class, subject, exam, stage, blueprint_diff, sealed_at, sealed_by | Strongroom log rows |
| DateSheet, SeatingPlan, DutyRoster | exam, rules, grid, rooms, duties | |
| MarksSheet | assessment_id, section, entries[], state, share_mode, flags | |
| ReportCardBatch | exam, students, state, approved_by | |
| CbseRecord | student_id, issues[], fixed, asked_parent_at, exported_at | |
| CounsellorCase, Session, SessionNote | case_id, student_id, referrer, status, note (encrypted) | Visible to counsellor only |
| Homework, HomeworkSubmission | class, due, key, submissions[] with checks and flags | |
| RemedialSuggestion | student_id, reason, topic, state | |
| Leave, OutOnDuty | applicant, type, dates, in_charge, route, state | |

### APIs

| Method and path | Purpose | Authz and role scope | Key errors |
|---|---|---|---|
| GET /v1/dashboard/today | Focus card and tiles for the active profile | Any staff role | 401, 423 (locked profile) |
| POST /v1/approvals/{id}/decision | Approve, decline, send back, noted | Approver for the current step | 409 already decided; 403 above limit |
| GET /v1/group/campuses?sort= | Scorecard | Owner | 403 |
| GET /v1/group/campuses/{id}/drawer | Campus drawer data | Owner | 404 |
| POST /v1/group/campuses/{id}/actions | Ask for plan, plan a visit, remind parents, mark reviewed | Owner | 422 |
| POST /v1/onboarding/campuses | Create campus from wizard | Owner | 422 per field |
| PUT /v1/onboarding/drafts/me | Save or resume wizard draft | Owner | 413 |
| POST /v1/onboarding/campuses/{id}/sheets/{n}/upload | Validate and import a sheet | Owner, campus lead | 415, 422 with row errors |
| POST /v1/onboarding/campuses/{id}/remind | Remind campus lead | Owner | 429 |
| PUT /v1/setup/{campus}/steps/{n} | Save a setup step | Principal | 422, 423 locked field |
| POST /v1/setup/{campus}/finish | Finish setup | Principal | 409 steps open |
| POST /v1/notices | Create and send or submit for approval | Role send rights | 422 audience empty |
| POST /v1/reports/{key}/run | Download | Role scope | 400 |
| POST /v1/reports/{key}/schedules | Schedule email | Owner, Principal | 422 invalid email |
| POST /v1/calendar/events | Add event | Principal (Owner per OQ-6a-03) | 422 |
| GET/POST /v1/cover?date= and /cover/notify | Cover table, fill, notify | Coordinator, Admin | 409 periods open |
| POST /v1/timetables/drafts | Generate draft | Coordinator | 422 no classes; 504 timeout |
| POST /v1/timetables/drafts/{id}/clashes/{c}/apply | Apply or undo a fix | Coordinator | 409 |
| POST /v1/timetables/{id}/approve | Approve and share a class set | Coordinator | 409 clash open |
| POST /v1/timetables/{id}/withdraw | Withdraw | Coordinator | 409 |
| POST /v1/leave and /leave/{id}/decision | Apply, route, decide | Per R-04 | 422 |
| PATCH /v1/papers/{id}/stage | Stage change with comments | Teacher, HoD, Exam cell | 409 order, 403 |
| POST /v1/exams/{id}/seating, /datesheet, /duties | Generate plans | Exam cell | 422 |
| POST /v1/marks/{assessment}/save | Save marks | Teacher | 422 flags open |
| POST /v1/report-cards/compile | Compile and send to principal | Exam cell | 409 open checks |
| POST /v1/cbse/apply-fixes, /ask-parents, /export | CBSE steps | Exam cell | 409 |
| POST /v1/counselling/cases/{id}/sessions, /notes | Book, write note | Counsellor | 403 other roles |
| POST /v1/attendance/registers | Submit register | Class teacher | 409 locked |
| POST /v1/homework/{id}/return | Return checked work | Teacher | 422 |
| POST /v1/remedial/send | Send suggestions to coordinator | Teacher | 422 |

### Events

| Event | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| approval.requested / approval.decided | A request is raised or decided | id, kind, amount, approver, note | Notifications, audit, Today |
| campus.created / onboarding.sheet_imported | Wizard confirms or a sheet imports | campus, batch, rows_bad | Notifications, scorecard |
| setup.finished | Principal finishes setup | campus, answers | Owner, onboarding, identity (staff logins) |
| notice.sent / notice.read | Send; app read | audience count, channel | Reports, notifications |
| cover.assigned | Substitutes notified | date, periods, teachers | Timetable, teacher apps |
| timetable.draft_created / approved / withdrawn | Generator and approval steps | classes, start_date, audience | Notifications, student, parent |
| leave.decided | Leave routed result | applicant, route, dates | Cover, HR, calendar |
| paper.stage_changed / paper.sealed | Workflow step | paper, from, to, user | Exam cell, audit |
| datesheet.published | Publish | exam, dates | Parents, setters |
| marks.saved / marks.flagged | Entry saved or checks fail | assessment, flags | Exam cell, remedial |
| reportcards.compiled / approved | Compile, principal approval | exam, count | Parent app |
| cbse.export_ready | All records clear | counts | Exam cell |
| attendance.submitted | Register submitted | section, absentees | Parents (WhatsApp), coordinator |
| counselling.session_booked / note_saved | Booking, private note | case (no content in event) | Student app only |
| report.scheduled_sent | Cron email sent | report, recipients | Audit |

### State machines / workflows

- **Approval request:** raised, pending(approver n), approved or declined or sent_back or forwarded (to next approver); terminal states notify the requester; decisions are immutable.
- **Timetable class:** none, draft(open clashes), draft(ready), approved(shared, pending start), live, withdrawn(draft); approved is immutable; edits create version n+1.
- **Cover period:** open, suggested, assigned, notified; notify requires all assigned.
- **Paper:** not_set, with_teacher, with_hod, moderation, approved_printing, printed_sealed; back-transitions are send-back with comment only.
- **Lesson plan:** not_submitted, late, submitted(to review), reviewed or sent_back.
- **Marks:** not_entered, entered_flagged, entered_clear, compiled, with_principal, published.
- **Campus onboarding:** draft, added, setup_in_progress, setup_finished, training_booked, parents_invited, live.
- **Counsellor case:** referral_new, first_session_booked, ongoing, closed (reopen allowed).
- **Leave:** applied, with_approver, forwarded, approved or declined; out-on-duty follows the same path without balance use.

### Permission matrix

| Capability | Owner | Principal | Admin | Coordinator | HoD | Exam cell | Counsellor | Teacher |
|---|---|---|---|---|---|---|---|---|
| Read all campuses | Yes | No | No | No | No | No | No | No |
| Add campus | Yes | No | No | No | No | No | No | No |
| Approve concession above limit, refund, post | Yes | No | No | No | No | No | No | No |
| Approve small concession, results, payroll | No | Yes | Salary only | No | No | No | No | No |
| Approve leave | Principal's own (via HR) | Yes (per R-04) | Yes (staff) | No | Team up to 2 days | No | No | No |
| Send notice to parents | Yes | Yes | Yes | To teachers | To own team | Exam notices | Parents of own cases | Own classes (approval default) |
| Add calendar event | Per OQ-6a-03 | Yes | Yes | No | Dept meetings | No | No | No |
| Assign cover | No | No | Yes | Yes | No | No | No | No |
| Generate and approve timetable | No | No | Manual only | Yes | No | No | No | No |
| Review lesson plan / paper | No | No | No | Chase only | Yes | Moderate | No | Own |
| Compile report cards | No | Approve | No | No | No | Compile | No | No |
| Read counsellor notes | No | No | No | No | No | No | Yes | No |
| Mark attendance / marks | No | No | No | No | Own classes | No | No | Own classes |
| Export CBSE file | No | No | No | No | No | Yes | No | No |

### Proposed flags

| Flag | Controls |
|---|---|
| mod.remedial | Remedial suggestions list, Saturday groups and sending to the coordinator |
| mod.cbse_registration | CBSE registration checks and export |
| mod.trustee_oversight | Trustee read-only payroll and refund log and approvals |
| ai.exam_planning | Dhruva-drafted date sheets (manual date sheets remain) |
| ai.exam_planning | Dhruva-generated seating and invigilation (manual remains) |

## Annex 6-A (part 2)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| Employee | id, campus_id, name, role, dept, type (teaching, non-teaching, contract, visiting), status, reports_to, doj, probation_end, payroll_id, ctc, bank (acct, ifsc), uan, pan, leave balances | Bank/UAN/PAN edits flag payroll |
| EmployeeDocument | id, employee_id, kind, status, expiry, file_ref | Police verification has expiry |
| AttendanceCorrection | id, employee_id, date, type, reason, approved_by, pay_effect, hr_status (pending, verified, rejected) | Blocks lock |
| LeaveIssue | id, leave_id, days_over, comp_off_available, choice (comp_off, unpaid, waive), settled_by | Feeds LWP line |
| CompOff | id, employee_id, earned_on, source_duty_id, used_on | |
| Payroll | id, name, basis, pay_day_rule, earnings[], deductions[], approval_rule, members | One payroll per employee |
| PayrollRun | id, payroll_id, period, cutoff_date, state, totals, approved_by, paid_at, bank_file_ref | See states |
| PayrollLine | run_id, employee_id, components[], net, hold flag, source refs | Paise integers |
| PayrollException | id, run_id, employee_id, severity, evidence, options[], decision, note | Gate for approval |
| Opening, Candidate, Shortlist | post, requester, stage counts; candidate score, summary, demo_slot | Dhruva ranks, person invites |
| Onboarding | joiner_id, items[{owner, status}], percent | |
| Exit | id, employee_id, last_day, items[{stage, owner, status}], settlement, state | |
| Voucher | id, type, number, date, lines[{ledger, dr, cr}], narration, maker, approvals[], tally_status, locked | Numbers per type and year |
| Ledger, LedgerGroup, CostCentre | name, group, opening, gst/tds flags, tally_name | |
| ApprovalItem | id, kind, ref, amount, maker, steps[{role, user, status, note}], dhruva_note | Maker != approver |
| Concession, Refund | student_id, amount, reason, policy_check, chain | |
| BankAccount, BankLine, ReconMatch | feed, amount, date, ref; match type, suggestion, status | |
| TallySyncLog, TallyFailure | time, sent, failed; voucher, reason, fixes | |
| Vendor, PurchaseOrder, GoodsReceipt, VendorBill, Requisition, Quote | GSTIN, TDS, MSME, docs; qty, rate | P3 |
| StockItem, Asset | reorder level, qty; register values | P3 |
| MonthLock, AccountYear | month, locked_by; year, state | |
| Filing | kind, period, status, ca_ack | |
| Enquiry/Family | child, grade, parent, phone, source, stage, temperature, interests, docs, fee | Masked phone in UI |
| CallLog, Tour, TourFeedback | outcome, note; route stops; interest, liked, barriers | |
| SeatPlan, Offer, WaitlistEntry | grade, seats; expires_at, status; priority | |
| Campaign, MessageTemplate | event, audience; locale, status | |
| Job | id, type, title, location, reporters[], priority, status, suggested_assignee, assignee, system_ref | Grouped reports |
| Visitor, EarlyPickup | host, photo, times; student, collector, authorised, parent_confirmed | |
| SystemStatus, RosterSlot | kind, count, state; date, guard | |
| Bus, Route, Stop, Rider | registration, papers; stops, times; stop, state, pickup list | |
| TripEvent | trip_id, kind (stop_arrival, child_result, start, school_arrival, sos), stop, student, actor, ts, offline flag | Source for live board |
| SafetyAlert, StaffCover, ParentThread | kind, bus, status; bus, covering; type, facts, draft | |
| FleetPaper, FeeSync, RouteChange | expiry; mismatches; options, approved | |
| Quest, XpEvent, Badge, HouseTotal | source, xp; student, delta; counters; house, points | gamification flag |
| StudyPlanItem, Readiness, PracticeAttempt | slot, topic, points; subject, revised, practice; paper, answers, score | |
| Doubt | student, subject, question, hint_shown, escalated, answer | |
| LeaveRequest (student) | dates, reason, parent_confirmed_at, approved_by | |

### APIs

| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| GET /dsk/today?role= | Prepared queue and tiles | Own role | 403 flag off |
| POST /dsk/today/{card}/act, /defer | Run or defer a card | Own role | 409 already done |
| GET /hr/employees?filter=&q= ; GET/PATCH /hr/employees/{id} | Directory, profile, edit (audited) | HR, principal | 422 invalid IFSC |
| POST /hr/corrections/{id}/verify, /reject ; POST /hr/corrections/verify-all | Verify | HR | 409 not HoD-approved |
| POST /hr/leave-issues/{id}/settle | Comp-off, unpaid, waive | HR | 409 no comp-off |
| GET /payroll/runs ; POST /payroll/runs/{id}/lock, /review, /exceptions/{eid}/decide, /submit, /release | Run steps | HR; approve: principal | 409 gate failed, 422 funding short |
| POST /payroll/runs/{id}/approve | Principal approval | Principal | 403 not approver |
| GET/POST/PATCH /payroll/payrolls ; POST /payroll/payrolls/{id}/members | Setup | HR | 409 member in other payroll |
| GET /hiring/openings ; POST /hiring/openings/{id}/invite | Openings and demo invites | HR | |
| PATCH /hiring/onboarding/{id}/items/{item} | Tick item | HR or owner | |
| GET/POST /exits ; POST /exits/{id}/settlement/submit | Exit | HR | 409 open items |
| GET /fin/approvals ; POST /fin/approvals/{id}/approve, /send-back | Approvals | Accounts, principal, owner | 403 maker, 422 note needed |
| POST /fin/concessions/{id}/submit | Concession chain | Accounts | |
| GET /fin/fees/today ; POST /fin/fees/deposit-slip ; POST /fin/fees/reminders | Fees | Accounts | |
| GET /fin/bank/{acct}/recon ; POST /fin/bank/lines/{id}/resolve ; POST /fin/bank/{acct}/close | Reconciliation | Accounts | 409 items left |
| GET /fin/tally/status ; POST /fin/tally/sync ; POST /fin/tally/failures/{id}/fix | Tally | Accounts | 502 connector offline |
| GET/POST /fin/vouchers ; POST /fin/vouchers/fill | Vouchers and fill-in | Accounts, makers | 422 unbalanced |
| GET/POST /fin/ledgers, /fin/groups | Masters | Accounts; Account main: group finance head | 403 |
| POST /fin/periods/{month}/lock ; POST /fin/years | Locks and years | Accounts | 409 steps open |
| GET /fin/reports/{kind}?year=&format= | Reports and export | Accounts, principal | |
| GET /fin/compliance ; POST /fin/filings/{id}/send-to-ca | Filings | Accounts | |
| /fin/purchases, /vendors, /inventory (CRUD, match, pay) | P3 | Accounts | 409 mismatch |
| GET /adm/families ; PATCH /adm/families/{id} ; POST /adm/families/{id}/calls, /next-step | CRM | Counsellor, front office | 422 outcome missing |
| POST /adm/enquiries | New enquiry | Counsellor, front office | 409 duplicate |
| GET/POST /adm/tours ; POST /adm/tours/{id}/feedback | Tours | Counsellor | 422 interest missing |
| GET /adm/seats ; POST /adm/offers ; POST /adm/offers/{id}/fee-paid ; POST /adm/waitlist/offer | Seats | Counsellor | 409 no seat |
| POST /adm/campaigns/{id}/send ; GET /adm/reports | Campaigns, reports | Counsellor | |
| GET /sec/jobs ; POST /sec/jobs/{id}/assign, /status | Jobs | In-charge | 409 closed |
| GET /sec/gate/visitors ; POST /sec/gate/visitors/{id}/approve, /checkout ; POST /sec/gate/walkins | Gate | Guard, in-charge | |
| POST /sec/gate/pickups/{id}/allow, /call-parent | Pickups | Guard, in-charge | 403 unlisted without call |
| GET /sec/systems ; GET/POST /sec/roster | Systems, roster | In-charge | |
| GET /trn/board?trip= ; GET /trn/buses/{id} | Live board | In-charge | |
| POST /trn/buses/{id}/spare ; POST /trn/trips/{id}/notify | Spare bus and parent update | In-charge | 409 spare busy |
| GET /trn/safety ; POST /trn/safety/{id}/handle ; POST /trn/cover | Safety, cover | In-charge | |
| GET/POST /trn/threads/{id}/reply, /forward | Messages | In-charge | |
| GET /trn/route-planner ; POST /trn/route-changes/{id}/approve | Routes | In-charge | 409 bus full |
| GET /trn/fleet ; POST /trn/fleet/{id}/renewal | Fleet | In-charge | |
| GET /trn/fees ; POST /trn/fees/sync ; POST /trn/fees/{kind}/act | Fees | In-charge | |
| POST /trn/events (from attendant app) | TripEvent ingest, idempotent by client id | Attendant | 409 duplicate, 403 other bus |
| GET /stu/home, /plan, /readiness, /quests | Student views | Student (self) | |
| POST /stu/quests/{id}/complete ; POST /stu/quiz/{id}/answer | Quests and quiz | Student | |
| POST /stu/papers/{id}/start, /answer, /submit | Timed paper | Student | 409 expired |
| POST /stu/doubts ; POST /stu/doubts/{id}/escalate | Hint-first questions | Student | |
| POST /stu/leave | Leave request | Student | 422 dates |

### Events

| Event | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| hr.correction.verified | Correction verified | employee, date, pay_effect | Payroll, attendance |
| hr.leave_issue.settled | Choice made | leave, choice, days | Payroll, employee app |
| payroll.run.locked / submitted / approved / paid | State change | run, totals | Finance, principal app, audit |
| payroll.exception.decided | Decision | run, employee, decision | Audit |
| hr.exit.settlement_submitted | Sent | exit, amount | Principal approvals |
| fin.approval.decided | Approve or send back | item, step, note | Maker, audit |
| fin.voucher.posted | Voucher saved or approved | voucher, lines | Tally, reports |
| fin.bank.reconciled | Account closed | account, month, brs_ref | Month-end, Tally |
| fin.period.locked | Month lock | month | All modules |
| tally.sync.completed / failed | Sync | sent, failed | Finance Today |
| fees.payment.received | Payment | student, amount, mode | Admissions, transport fee sync, recon |
| adm.family.stage_changed | Stage change | family, from, to | Reports, Dhruva |
| adm.admitted | Fee paid | family, grade | Accounts, class teacher, registrar |
| adm.offer.expiring | 3 days before expiry | offer | Reminder |
| sec.job.assigned / resolved | State change | job, assignee | Reporter, exam cell |
| sec.pickup.logged | Pickup allowed | student, collector, photo | Parent app |
| trn.trip.event | Attendant tap | see TripEvent | Live board, parent app, headcount, reports |
| trn.bus.breakdown | Marked or reported | bus, riders | Banner, parent messages |
| trn.route.changed | Approved | child, bus, fee slab | Parents, attendant, fee ledger |
| trn.safety.alert | Speed, route or headcount | bus, kind | Safety checks |
| stu.quest.completed, stu.practice.scored, stu.doubt.escalated | Student actions | student, points, topic | Gamification, readiness, teacher inbox |
| stu.leave.requested | Student submits | dates | Parent app, class teacher |

### State machines / workflows

- PayrollRun: Draft -> Locked (needs 0 open corrections) -> Reviewed -> ExceptionsCleared (0 open) -> WithPrincipal -> Approved -> Paid; WithPrincipal -> Returned -> Reviewed.
- Correction: Pending -> Verified | Rejected. LeaveIssue: Open -> Settled.
- Exit: Started -> InProgress -> SettlementSent -> Approved -> Closed.
- ApprovalItem: Submitted -> FirstApproved -> (SecondApproved if above threshold) -> Posted; any step -> SentBack -> Resubmitted.
- Bank recon (per account-month): Imported -> AutoMatched -> Reviewing -> Posted/Closed.
- Voucher: Draft -> PendingApproval -> Posted -> SyncedToTally | SyncFailed -> Fixed. Month: Open -> Locked.
- Family stage: New -> Contacted -> TourBooked -> Toured -> Applied -> OfferMade -> Admitted (any -> Closed).
- Offer: Sent -> FeePaid | Lapsed (7 days). Tour: Booked -> InProgress -> FeedbackSaved.
- Job: New -> Assigned -> InProgress -> Resolved. Pickup: Pending -> (Authorised | ParentCalled) -> Allowed -> Logged.
- Trip: NotStarted -> Running(stop n) -> AtSchool -> EmptyChecked -> Closed; child per stop: ToPickUp -> OnBus | NotHere -> (Came | LeftAtStop); afternoon: OnBus -> HandedTo | StaysOnBus.
- Breakdown: Reported -> SpareSent -> Handled.
- RouteChange: Proposed -> Approved -> Applied.
- Timed paper: NotStarted -> InProgress <-> Paused -> Submitted -> Marked. Doubt: Hint -> Resolved | Escalated -> Answered.

### Permission matrix

| Capability | HR | Accounts in-charge | Accounts assistant | Counsellor | Sec/IT | Transport | Principal | Owner | Student |
|---|---|---|---|---|---|---|---|---|---|
| Employee records edit | Y | | | | | | R | | |
| Verify corrections, settle leave issues | Y | | | | | | R | | |
| Run payroll steps | Y | | | | | | R | | |
| Approve payroll, settlement | | | | | | | Y | | |
| Create vouchers | | Y | Y (maker) | | | | | | |
| Approve vouchers, bills, refunds | | Y (not own) | | | | | Y (second, above limit) | Y (above owner limit) | |
| Lock month, account year | | Y | | | | | A (after lock) | | |
| Edit Account main | | R | | | | | | | |
| Bank recon, Tally | | Y | R | | | | R | | |
| Admissions CRM full | | | | Y | | | R | R | |
| Gate approve/checkout | | | | | Y | | | | |
| Jobs assign | | | | | Y | | R | | |
| Live board, safety, fleet, routes | | | | | | Y | R | | |
| Attendant events | | | | | | Y (read) | R | | |
| Own quests, plan, homework, leave | | | | | | | | | Y (self) |
| Ask Dhruva | Y | Y | Y | Y | Y | Y | Y | Y | Y |

Key: Y = can do; R = read only; A = approves changes. Roles outside this section (teachers, class teachers, parents, HoDs) act through their own sections.

### Proposed flags

| Flag | Meaning | Default |
|---|---|---|
| mod.procurement_inventory | Purchases, vendors, inventory, assets (DSK-FIN-008 to 011) | Off |
| mod.student_gamification | XP, levels, streaks, house points, badges, achievements | On |
| ai.finance_assist | Dhruva fill-in on new vouchers | On |
| ai.hr_assist | Dhruva's CV shortlist for open positions | On |
