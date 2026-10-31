# 5. AI: the Dhruva assistant

## 5.1 Purpose, scope and out-of-scope

Dhruva is the assistant built into every DhruvaOne screen. It reads the school's own records, prepares the first draft of routine work, explains numbers and puts the most important task first. A person always decides. This section defines what Dhruva may do, how it is controlled per tenant, how it stays safe and honest, and how every action is recorded.

In scope:
- Shared AI principles and the AI control plane (enablement, consent, toggles, data use, quotas, kill switch, fallback).
- Ask Dhruva chat, the daily focus card and queue ordering.
- One requirement (or one grouped table) for each `ai.*` flag in the catalogue: cover suggestions, timetable generator, reply drafts, notice drafts, marks from photo, paper generator, lesson-plan drafts, homework marking, remedial grouping, at-risk detection, admissions scoring, fee follow-up, payroll checks, bank matching, security triage, transport alerts, student tutor, voice input, translation, WhatsApp bot.
- Quality, safety, fairness, feedback, evaluation, monitoring and the AI audit trail.
- The Halo orb (Dhruva's face) as a UI requirement.

Out of scope here (covered elsewhere): the screens, approvals and records that Dhruva's drafts feed (each role's module section), the WhatsApp conversation design and templates (Section 8, WhatsApp channel), sign-in and role identity (Section 3, Identity), flag mechanics and tenant administration (Section TFC), notification delivery rules (Section XCT). This section refers to those by ID.

Phase mapping used throughout: MVP = MVP build and go-live (Oct 2026 to Mar 2027); P2 = Phase 1 of the roadmap (Apr to Sep 2027); P3 = Phase 2 (Oct 2027 to Mar 2028).

## 5.2 Actors and roles

| Actor | What they do with Dhruva |
|---|---|
| Owner (group) | Asks about campuses, approvals and onboarding; approves Dhruva-drafted group notices; sets group-level AI policy. |
| Principal | Gets absence watch and approval summaries; approves notices, payroll runs, concessions with Dhruva's pre-checks. |
| Academic coordinator | Cover, timetable generation, remedial groups, parent-query drafts. |
| Exam cell | Date sheets, seating and duties, paper moderation, CBSE record fixes, marks checks. |
| HoD | Reviews Dhruva-flagged papers and plans; leave suggestions. |
| Teacher | Marks from photo, homework marking, paper and lesson-plan drafts, reply drafts, remedial suggestions, notes. |
| Counsellor | Check-in suggestions, free-slot booking, private note drafts. |
| HR and payroll, Finance and accounts | Payroll checks, shortlists, settlement figures; bank matching, bill matching, Tally fixes, fee reminders. |
| Admissions | Enquiry rating, next step, WhatsApp drafts, tour routes, waitlist picks. |
| Security and IT, Transport in-charge, bus attendant | Job grouping and assignee suggestion; breakdown and delay messages; voice or typed questions in Hindi or English. |
| Parent | Ask Dhruva (own children only); WhatsApp assistant. |
| Student (Classes 6 to 12) | Study plan, quests, hint-first tutor. |
| Campus admin (standalone school) | Cover, exam duty roster, leave context; tenant AI settings (with owner or trustee). |
| Tenant AI administrator | Group owner, or campus admin of a standalone school; operates the AI control plane (5.3.5). |
| DhruvaOne platform staff | Operate model providers, evaluation and incident response; cannot read tenant prompts or outputs without a logged, time-boxed support grant [Spec]. |

## 5.3 Functional requirements

### 5.3.1 AI principles (shared platform requirements)

**AI-PRN-001 · Must · MVP · flag: core · [Design]**
The system shall let Dhruva suggest, draft and explain only; anything that changes a record or reaches a family, student or staff member needs a named person's approval first.
- Acceptance: Given Dhruva has drafted a notice, a fee reminder, a timetable or a marks list When nobody has pressed the approving button ("Send", "Approve", "Publish", "Share") Then no record changes and no message leaves the system.
- Acceptance: Given any AI-prepared item When it is approved Then the approver's identity, time and any edits are written to the AI audit log (AI-AUD-001).
- Rules: Source: Website "An assistant in every screen, and a person in charge"; MvpScope "anything it drafts waits for a person to approve".

**AI-PRN-002 · Must · MVP · flag: core · [Design]**
The system shall show the source records or numbers behind every AI answer, suggestion or flag.
- Acceptance: Given an Ask Dhruva answer When it renders Then a source line is visible (for example "Marks and attendance", "Fee invoices", "School calendar and notices").
- Acceptance: Given a suggestion card (cover pick, bank match, at-risk flag) When opened Then a "Why" or "Dhruva checked" explanation names the records and values used.
- Rules: A suggestion that cannot name its source is not shown (see AI-QLT-002).

**AI-PRN-003 · Must · MVP · flag: core · [Design]**
The system shall never let Dhruva make a final decision alone; it recommends one option and the person chooses.
- Acceptance: Given a clash, exception, leave request or admission offer When Dhruva recommends an option Then the screen offers the recommended action and at least one alternative or "Edit", and nothing applies before the tap.
- Rules: Source: Appshell "Never decides alone". Bulk buttons ("Fix all", "Fill with Dhruva", "Verify all") count as an approval by the person who tapped them and are logged per item.

**AI-PRN-004 · Must · MVP · flag: core · [Spec]**
The system shall keep a manual path for every task that has an AI path, so that switching AI off never blocks work.
- Acceptance: Given every `ai.*` flag is off When a teacher takes attendance, enters marks, a coordinator assigns cover or builds a timetable cell by cell, finance matches a bank line, or HR runs payroll Then each task completes with the same final records, minus suggestions.
- Rules: No requirement in any section may depend on an AI output being present. Test: each module's acceptance suite runs once with all `ai.*` flags off.

**AI-PRN-005 · Must · MVP · flag: core · [Spec]**
The system shall visibly mark every AI-produced item (draft, suggestion, flag, read-from-photo value) as "Dhruva" content until a person approves it, and keep a marker after approval.
- Acceptance: Given a draft in an editor When displayed Then it carries the Dhruva ring marker and the words "Drafted by Dhruva" or the screen's design label (for example "Dhruva drafted a reply · edit anything").
- Acceptance: Given an approved record that came from AI When viewed in history Then it shows "Prepared by Dhruva, approved by <name>".

**AI-PRN-006 · Must · MVP · flag: core · [Spec]**
The system shall never present AI output as the school's official statement to a family before approval, and never send AI text under a person's name without that person having approved it.
- Acceptance: Given a reply drafted for Ms. Arora When sent Then the sender recorded is Ms. Arora and the audit log shows her approval.

### 5.3.2 Ask Dhruva chat

**AI-CHT-001 · Must · MVP · flag: ai.assistant_chat · [Design]**
Any signed-in user can open Ask Dhruva from the orb on every phone screen, and from the "Ask Dhruva" button in the desktop header.
- Acceptance: Given any screen on phone or desktop When the user taps the orb or "Ask Dhruva" Then a chat opens with a greeting, a "Dhruva · online" status and suggested questions first, free text second.
- Acceptance: Given the desktop panel When opened Then it is headed "Answers from your records, with sources".
- Rules: Parent greeting example: "Hello Mr. Reddy. Ask me about Navya or Arjun: marks, fees, notices or the week ahead."

**AI-CHT-002 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall offer role-specific suggested questions, drawn from live data, as tappable chips.
- Acceptance: Given the role When chat opens Then 3 to 4 chips are shown, for example Owner: "Which campuses are behind on onboarding?", "Why is Gurugram attendance low?", "How many new students joined this session?"; Parent: "How is Navya doing before the exams?", "What do I need to pay this month?", "What is happening at school next week?"; Student: "What should I revise first?"; Admissions: "Which families should I call first today?"; Security: "What is still open today?".
- Rules: The full catalogue of sample questions per role is in the Annex table "Suggested-question catalogue". Chips are configuration, not code, and can be hidden per role (AI-CTL-004).

**AI-CHT-003 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall answer free-text questions about records the asker may see, in a short form with the key numbers and a source line, and may attach action cards.
- Acceptance: Given a parent types "pay" or "why is October's fee Rs 14,600?" When answered Then the reply shows the break-up (for example Tuition Rs 11,800, Transport Rs 2,800, Late fee Rs 0, Total Rs 14,600), source "Fee invoices", and buttons "Pay now" and "Download invoice".
- Acceptance: Given the status while working When shown Then it reads "Checking your records…" and the final answer appears within 5 seconds at p95 [Spec].
- Rules: Action cards (Pay, Book "10:20 am", Download) call the normal module flows; payments and bookings still need the user's own tap and normal authentication.

**AI-CHT-004 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall reply "I answer questions about your children's school day, marks, fees and notices, from the school's records." (adapted to the role) when a question is outside its scope.
- Acceptance: Given an unrelated question (for example general knowledge) When asked in a parent or student chat Then the scope message is returned and no model-invented answer is given.
- Rules: Staff roles may be allowed a short, clearly labelled general-help answer only if the tenant enables it [Spec]; default off.

**AI-CHT-005 · Must · MVP · flag: ai.assistant_chat · [Spec]**
The system shall scope every answer to the asker's role, profile, campus and linked children, so that no answer exposes data the asker cannot see in the app.
- Acceptance: Given a parent of Navya asks "How is Arjun's classmate doing?" or "Show class average for all students" When answered Then no data about other children is returned; only the class average already shown to parents.
- Acceptance: Given a teacher asks about a student not in their classes When answered Then Dhruva says it cannot show that student and offers to ask the class teacher.
- Acceptance: Given one phone holds a teacher profile and a parent profile When chatting under the parent profile Then no teacher-profile data appears (profiles never mix).
- Rules: Authorisation is enforced in the data-retrieval layer before text reaches the model (Annex: retrieval gateway), never by asking the model to hold back. Counsellor private notes and case history are never retrievable by anyone but the counsellor. Payslips are retrievable only by the owner of the payslip.

**AI-CHT-006 · Must · MVP · flag: ai.assistant_chat · [Spec]**
The system shall keep multi-turn context within a conversation, so follow-ups ("and for Arjun?") resolve against the earlier question.
- Acceptance: Given "What do I need to pay this month?" then "and the late fee?" When answered Then the second reply uses the same child and month.
- Rules: Context window of the last 10 turns; a new conversation starts after 30 minutes idle or on profile switch. Conversation text retention follows AI-CTL-009.

**AI-CHT-007 · Should · P2 · flag: ai.assistant_chat · [Design]**
The system shall answer in English or Hindi according to the user's language setting (Me > Language), with a one-tap switch inside chat.
- Acceptance: Given language is Hindi When a question is asked in Hindi or English Then the reply is in Hindi, numbers in the school's number format.
- Rules: Android chat header reads "online · replies in Hindi or English". Appshell lists six languages at first run but only English and Hindi are confirmed; the others are P3 (Open question 1). English is MVP.

**AI-CHT-008 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall show "Cards with real actions" and let the user continue in the module without losing the chat.
- Acceptance: Given the answer "Saturday 17 Oct, 9 am to 12 pm. Ms. Kavya Reddy has a free slot at 10:20 am." When the parent taps "Book 10:20 am" Then the PTM booking flow completes and the chat shows the booking confirmation.

**AI-CHT-009 · Should · MVP · flag: ai.assistant_chat · [Spec]**
The system shall let the user give a thumbs up or down on every answer, and report a wrong number.
- Acceptance: Given an answer When the user taps the thumbs-down Then a one-tap reason list appears ("Wrong number", "Not useful", "Not allowed to see", "Other") and the feedback is stored with the answer (AI-QLT-008).

### 5.3.3 Daily focus card and queue ordering

**AI-FOC-001 · Must · MVP · flag: ai.focus_card · [Design]**
The system shall open every role's home on a Dhruva-prepared card headed "<n> THINGS NEED YOU · 1 OF <n>", showing the most urgent item first with its action button and "Later ›".
- Acceptance: Given 5 open items for the academic coordinator When Today opens Then the heading reads "5 THINGS NEED YOU · 1 OF 5", the first item is the one with highest rank (AI-FOC-002), and "Later ›" moves to the next.
- Acceptance: Given "See all 5 for today · 0 done" When tapped Then all items show and the link becomes "One at a time".
- Acceptance: Given all items done When Today opens Then the heading reads "Nothing needs you today" (parent) or the role's equivalent.

**AI-FOC-002 · Must · MVP · flag: ai.focus_card · [Spec]**
The system shall order the queue by explicit rules, not by the model alone.
- Acceptance: Given mixed items When ranked Then order is: (1) safety and emergencies ("EMERGENCY · NOW"), (2) hard deadlines today, (3) items blocking other people (cover for periods starting soon, payroll before pay date, approvals others wait on), (4) money or compliance at risk (overdue fees, CBSE deadline), (5) everything else by oldest first. Ties broken by earliest deadline.
- Acceptance: Given "Later ›" pressed on an item When the queue re-ranks later the same day Then that item is not shown first again unless its deadline is within 1 hour or it is safety-class.
- Rules: The model may write the card text and propose a rank within a tier; tier assignment is by rule per item type (Annex: queue tiers). Items from the manual path (not AI-prepared) appear in the same queue.

**AI-FOC-003 · Must · MVP · flag: ai.focus_card · [Design]**
The system shall perform the item's work in one tap where the design shows a bulk action, and mark the card done with a confirmation.
- Acceptance: Given "Cover 24 periods today" When "Fill with Dhruva" is tapped Then 24 suggested teachers are assigned as a draft assignment list, toast "Dhruva filled 24 periods · check and change any", and only after "Notify" the card becomes "Cover sorted for today".
- Rules: Further examples: "Remind teachers" (30 reminded, HoDs copied), "Create groups" (6 remedial groups), "Send welcome and book calls" (3 families), "Verify all" (4 corrections), "Use suggestions" (3 leave issues). Each is a bulk approval under AI-PRN-003 and AI-AUD-001.

**AI-FOC-004 · Should · MVP · flag: ai.focus_card · [Design]**
The system shall state, in one line on the card, why the item is first ("7 teachers are away · Dhruva has picked free teachers of the same subject").
- Acceptance: Given any card When displayed Then a reason line and a count of affected people or amounts is shown.

**AI-FOC-005 · Should · P2 · flag: ai.focus_card · [Spec]**
The system shall let a user snooze or hide a card type, and let the tenant set the maximum cards per day (default 8) and quiet times.
- Acceptance: Given quiet hours 9 pm to 6 am When items arise Then no push is sent for non-safety cards (see Section XCT notifications).

**AI-FOC-006 · Should · MVP · flag: ai.focus_card · [Design]**
The system shall produce the end-of-day check for teachers ("After P8 · Dhruva has guessed where each class is") with a guess of On plan, Behind or Ahead that the teacher confirms.
- Acceptance: Given pace data and the lesson log When P8 ends Then a card per class shows Dhruva's guess; the teacher taps "On plan", "Behind" or "Ahead" and a reason if behind; the guess is stored separately from the teacher's confirmed value.
- Rules: The confirmed value feeds the coordinator's and HoD's pace views; the guess alone never does.

### 5.3.4 Generation and decision-support capabilities

#### Cover suggestions (ai.cover_suggestions)

**AI-COV-001 · Must · MVP · flag: ai.cover_suggestions · [Design]**
The academic coordinator (or campus admin of a standalone school) can fill every open cover period with Dhruva's pick of free teachers and change any pick before notifying.
- Acceptance: Given 24 uncovered periods When "Fill with Dhruva" is tapped Then each period shows a starred substitute and a "Why" such as "free · Maths PGT · 1 cover this week", the row dot turns from amber to green, and teachers are notified only after "Notify".
- Acceptance: Given a period When the dropdown "Pick a substitute..." is opened Then three candidates (same subject, free that period) are listed, first starred.
- Rules: Selection order: same subject, free that period, fewest covers this week; never a teacher already at 3 or more covers (tenant-configurable limit); never one on approved leave or on duty. If no candidate qualifies the row stays "No suggestion" and the manual dropdown lists all free teachers. A teacher can decline from the app or WhatsApp ("Can't take the cover?"), which re-triggers the suggestion.

#### Timetable generator (ai.timetable_generator)

**AI-TTG-001 · Must · MVP · flag: ai.timetable_generator · [Design]**
The academic coordinator can generate a draft timetable for the whole school or chosen sections from classes, subjects, periods, teachers and rules, and nothing is shared until approved.
- Acceptance: Given "Generate a new timetable" When the coordinator picks "Whole school · 60 sections" or a subset (up to 4 sections named, else a count), sets "Use from" (default Tue 27 Oct) and presses "Generate" Then a progress panel shows "Reading 60 sections, 193 teachers and 41 rooms", "Placing 2,880 periods for the week", "Checking clashes and your rules", "Balancing teacher load".
- Acceptance: Given generation completes When the draft opens Then the banner reads "DRAFT: Only you can see this. Teachers and parents keep seeing the current timetable until you approve and share it."
- Rules: Draft generation completes within 60 seconds for 60 sections at p95 [Spec]; longer runs continue in background with a notification.

**AI-TTG-002 · Must · MVP · flag: ai.timetable_generator · [Design]**
The system shall apply six configurable rules and report how many are met.
- Acceptance: Given the rule list When shown Then these six are present and on by default: "No teacher teaches more than 3 periods in a row"; "Maths and Science in the first four periods"; "Science and Computer labs as double periods"; "Sports and Art after the break"; "Every teacher within the norm (TGT 30, PGT 26)"; "Class teachers take period 1 in their own class".
- Acceptance: Given one rule is switched off When regenerated Then the chip shows "5/5 rules met"; with all on and met, "6/6 rules met".
- Rules: Norms (TGT 30, PGT 26) and rule texts are tenant configuration. Rules are hard constraints unless the draft explains a bent soft rule (for example "one soft rule bent for 10-C Sports on Fridays because the ground is booked").

**AI-TTG-003 · Must · MVP · flag: ai.timetable_generator · [Design]**
The system shall detect clashes and offer one recommended fix plus alternatives for each, with Show, Apply, Other options and Undo, and a "Fix all" action.
- Acceptance: Given a draft with 4 clashes When opened Then the chip reads "Draft · 3 clashes" style with the count; each card shows kind (teacher in two places, room clash, teacher not available), a Suggested fix, and buttons "Show", "Apply", "Other options".
- Acceptance: Given "✦ Apply all N suggested fixes" is tapped Then every open clash gets its recommended fix, the toast reads "Applied the suggested fix to every open clash", the chip turns "All resolved", and each card keeps "Undo".
- Acceptance: Given a clash is applied When "Undo" is pressed Then the clash reopens and the previous cells return.
- Rules: Clash kinds checked: teacher double-booked, room or lab double-booked or too small, teacher on approved leave or duty (from leave calendar), teacher over norm, subject three days running, class double-booked. A fix that creates a new clash is never recommended; "Fix all" repeats until stable or stops with the remainder listed.

**AI-TTG-004 · Must · MVP · flag: ai.timetable_generator · [Design]**
The coordinator can review the draft per class, see changes against the current timetable and the teacher-load before and after, and approve for one, some or all classes with a "Use from" date.
- Acceptance: Given the grid When a class is selected Then the header reads "Class 9-B · 10 of 46 periods changed", changed cells have a dashed outline, clash cells red, resolved cells teal, and summary chips show clashes, teachers over the norm, rules met and "74% periods unchanged".
- Acceptance: Given the approve dialog When classes are ticked (one, several or all ready classes) and "Use from" is confirmed or changed Then only those classes publish; the state chip becomes "Approved and shared"; until the date everyone keeps seeing the current timetable.
- Acceptance: Given a class still has a clash When approval is attempted Then that class cannot be selected and the dialog says which clashes remain.
- Rules: On publish, teachers and parents are notified of changed periods (Section XCT). The previous timetable stays recoverable for 30 days [Spec]. Approving writes a version record with the approver and "Use from" date.

#### Reply drafts (ai.reply_drafts)

**AI-RPL-001 · Must · MVP · flag: ai.reply_drafts · [Design]**
The system shall draft a reply to each parent, student or HoD message, shown in an editable box, with "Make it shorter", "Write my own" and "Send reply".
- Acceptance: Given a parent message in the teacher inbox When opened Then a box labelled "Dhruva drafted a reply · edit anything" is filled, and "Send reply" is the only action that sends it.
- Acceptance: Given "Make it shorter" When tapped Then the draft is regenerated shorter in place.
- Rules: Drafts use the syllabus, marks and notes the sender may see; for coordinator parent queries "Dhruva drafts from the syllabus and marks records but a human sends"; replies copy the class teacher.

**AI-RPL-002 · Should · MVP · flag: ai.reply_drafts · [Design]**
The system shall route a new parent message to the right person by topic and attach the facts it found.
- Acceptance: Given "+ New message" topics When a parent picks "A question about marks or homework" Then it goes to the class teacher; "Study pace or extra help" goes to the academic coordinator; transport topics go to the transport desk with "What Dhruva found · From the attendant's taps, the pickup list and the fee ledger".

**AI-RPL-003 · Should · MVP · flag: ai.reply_drafts · [Design]**
The system shall answer simple student doubts from the teacher's shared notes without involving the teacher, and only surface the rest.
- Acceptance: Given a student doubt covered by a note the teacher shared When asked Then Dhruva answers, cites the note, and the teacher sees only unanswered doubts ("Dhruva has already answered 4 simple doubts from your shared notes").
- Rules: Auto-answers to students are allowed only from teacher-shared material, are labelled as Dhruva, and the teacher can review the list; tenants can require approval instead (AI-CTL-005).

#### Notice drafts (ai.notice_drafts)

**AI-NTC-001 · Must · MVP · flag: ai.notice_drafts · [Design]**
Owner, principal, exam cell, coordinator, transport in-charge, counsellor and admissions users can draft a notice or message with Dhruva and edit it before sending.
- Acceptance: Given the notice composer When a draft chip ("Exam arrangements", "Fee collection", "Diwali wishes", "PTM reminder", "Diwali holiday", "Attendance, Classes 9-12") is tapped Then title and message fill, the toast reads "Dhruva drafted it · edit before sending", and nothing is sent until "Send".
- Acceptance: Given one-to-one mode When a person is chosen Then the greeting uses that person's name.
- Rules: The recipient count line ("3,980 parents will get it") is computed from records, not by the model. Group notices show read counts after sending.

**AI-NTC-002 · Should · MVP · flag: ai.notice_drafts · [Design]**
The system shall draft counsellor invites and private session notes from the counsellor's own tags only.
- Acceptance: Given tags such as "Calmer than last time" When "✦ Draft the note" is pressed Then a note is drafted from those tags alone (toast "Dhruva drafted a private note from your tags") and saved only after the counsellor edits and saves.
- Rules: Notes are private to the counsellor; no session note text is used to train, evaluate or fill other features (AI-CTL-007).

**AI-NTC-003 · Should · MVP · flag: ai.notice_drafts · [Design]**
The system shall draft the transport breakdown or delay message to affected families, with new stop times computed from route data.
- Acceptance: Given "Bus 14 broke down" When the in-charge opens the card Then the message to the 38 families is pre-written in English and Hindi, and sending requires the in-charge's tap.

#### Marks from photo (ai.marks_from_photo)

**AI-MKS-001 · Must · MVP · flag: ai.marks_from_photo · [Design]**
A teacher can photograph a mark-sheet page, and Dhruva reads all marks into the entry list, flagging doubtful ones.
- Acceptance: Given "Snap the mark sheet" When a photo of 36 marks is taken Then the list fills and the toast reads "Dhruva read 36 marks from the photo · 2 need a look".
- Acceptance: Given a mark above the maximum (reads 23, test out of 20) When flagged Then the row is amber with text "Reads as 23, but the test is out of 20" and fix chips "13" and "20".
- Acceptance: Given a blank mark When flagged Then the row shows "No mark on the sheet" with chips "Absent" and "0".
- Rules: Typing marks instead is always available ("Type the marks instead"), with the same checks for over-maximum, blanks and typing slips.

**AI-MKS-002 · Must · MVP · flag: ai.marks_from_photo · [Spec]**
The system shall require the teacher to confirm every read value before marks are saved or shared, showing the photo beside the extracted list.
- Acceptance: Given photo-read marks When the teacher presses "Share" Then flagged rows must be resolved first; non-flagged rows are accepted as shown after the teacher sees the side-by-side view; the saved record stores source "read from photo" and the confirming teacher.
- Rules: The design allows "share with parents today or after HoD check" and shows no confirm step for WhatsApp photo publish (Undo only); this spec requires confirmation on every channel (Open question 2). Any value with OCR confidence below 0.90 [Spec threshold] is always flagged. Images are deleted per AI-CTL-009.

**AI-MKS-003 · Should · MVP · flag: ai.marks_from_photo · [Design]**
The system shall name what it recognised before reading ("This looks like an attendance register for 5-B") and label results "Read from your photo · saved in Dhruva One" with Undo.
- Acceptance: Given a photo via WhatsApp (see AI-WAB-001) When recognised wrongly Then the teacher can reject at the "This looks like..." line and nothing is read.
- Rules: Attendance registers read from photo follow the same confirmation rule (AI-MKS-002) for the in-app path; the WhatsApp path posts a draft summary "Attendance published" only after confirmation reply (Section 8).

**AI-MKS-004 · Should · MVP · flag: ai.marks_from_photo · [Design]**
The system shall add low scorers from entered marks to remedial suggestions and flag the whole list's average and top and bottom values live.
- Acceptance: Given Aditya Rana 5/20 is entered When saved Then he appears in remedial suggestions (AI-REM-001).

#### Paper generator (ai.paper_generator)

**AI-PPR-001 · Must · MVP · flag: ai.paper_generator · [Design]**
A teacher can have Dhruva draft a question paper to the HoD's blueprint (pattern, sections, marks, difficulty mix, chapters taught), with an answer key.
- Acceptance: Given Step 1 picks "Board pattern (80 marks · 3 hours · CBSE 2026–27)" (or Unit test 40 marks, Class test 20 marks, "Copy my last paper", "Start blank") and chapters ticked "Taught" Then Step 2 shows sections A to E (A 20 × 1, B 5 × 2, C 6 × 3, D 4 × 5, E 3 × 4) and Step 3 shows Dhruva's questions with chapter, difficulty chip and marks.
- Acceptance: Given "Another question", "Pin", "Delete", "✦ Redraft section", "+ Write a question", "Fill the gaps" When used Then pinned and teacher-written questions are kept; toast "Section A redrafted · pinned questions kept".
- Rules: No question repeated from the past 3 years of the school's papers; totals and difficulty mix must match the blueprint or show a variance line; chapters not yet taught are excluded unless the teacher overrides. Papers are confidential: drafts visible only to the setter until sent to the HoD.

**AI-PPR-002 · Should · MVP · flag: ai.paper_generator · [Design]**
The system shall check an uploaded or drafted paper against its blueprint and flag questions for the HoD and exam cell.
- Acceptance: Given a paper under HoD review When opened Then a banner reads "Dhruva marked 2 questions for you to look at" or "Dhruva found nothing to flag", and the blueprint check compares chapter marks with plan (for example "Trigonometry 18 marks vs 12 planned").
- Acceptance: Given the exam cell's "Moderate with Dhruva" When pressed Then clean papers are sent to print and flagged ones go back with Dhruva's notes (toast "7 papers sent to print · 2 sent back with Dhruva's notes"), each only after the exam-cell user's approval of the batch.
- Rules: The paper chain is teacher, HoD, exam cell, print and seal; Dhruva flags are advisory. The model provider receives paper content only under the confidentiality terms in AI-CTL-007; strongroom log is unaffected.

**AI-PPR-003 · Should · P2 · flag: ai.exam_planning · [Design]**
The exam cell can have Dhruva draft the date sheet against the holiday and event calendar, and the seating and invigilation plan.
- Acceptance: Given "Draft with Dhruva" When run Then every paper is placed with no class clash and no holiday clash; the exam cell edits, then publishes.
- Acceptance: Given "Generate with Dhruva" for seating When run for 2,190 students and 42 rooms Then two classes are paired per room so neighbours never sit the same paper, in roll order; invigilators (84 a day) have no paper that day, fewest duties, and never their own subject.
- Rules: Campuses without an exam cell use the admin's "Fill the gaps" roster. The scope table lists AI date sheets, seating and duties as MVP; the flag is proposed because the catalogue has no exam-planning key. The same pattern applies to CBSE registration fixes ("Apply Dhruva's 14 fixes", which corrects records only from admission and timetable data, after the exam cell's tap).

#### Lesson plan drafts (ai.lesson_plan_drafts)

**AI-LPL-001 · Must · MVP · flag: ai.lesson_plan_drafts · [Design]**
A teacher can have Dhruva draft a weekly (or two-week, or chapter) lesson plan from the annual plan and class pace, edit any day, and send it to the HoD.
- Acceptance: Given "Plan for One week", classes 10-B and 10-C and mode "✦ Dhruva's draft" When generated Then the output reads "Week of 19–23 Oct · 10-B and 10-C · Draft · only you see it", with 5 lessons of 40 minutes, a teach-activity-practice split chip, and "Dhruva's note" on catch-up (10-C a period behind: Monday adds 10 minutes of catch-up for it only).
- Acceptance: Given sending When any period lacks a topic or activity Then "Add a topic and activity for each lesson first" blocks it; on send, toast "Sent to Dr. Anjali Desai · she usually reviews by Monday".
- Rules: "Fill this day", "Redraft" (pinned days kept) and "Other idea" per activity are available. The HoD's last review comment is shown to the teacher on the next draft. Notes and revision material are also drafted (Revision notes, Formula sheet, Practice questions) from the lesson log or a photo of the teacher's notes, and shared only on the teacher's tap ("Shared in the student app · parents told on WhatsApp"; scheduling allowed).

#### Homework marking (ai.homework_marking)

**AI-HWK-001 · Must · MVP · flag: ai.homework_marking · [Design]**
The system shall check each submitted homework page against the teacher's key, tick questions, and show the teacher only the ones it was unsure about.
- Acceptance: Given Exercise 4.3 with 38 pupils When checked Then tiles show "Handed in 34 / 38", "Need your look 7", "Checked by Dhruva 27", "Missing 4"; a student's page shows ticks per question, a "DHRUVA WASN'T SURE" note, chips Q1 to Q10, a score stepper and comment box.
- Acceptance: Given "Return 27 checked to students" When pressed by the teacher Then marks and comments go to students and parents; before that, students see "Checked by Dhruva, returned by the teacher" status only.
- Rules: Also detects copying, blur and wrong page order. Students never see Dhruva's marks before the teacher returns them (see Open question 2 on the design's "publish without teacher review" note). Subjective answers (essays, long answers) are always "Need your look" unless the teacher enables marking against a rubric.

#### Remedial grouping (ai.remedial_grouping)

**AI-REM-001 · Must · MVP · flag: ai.remedial_grouping · [Design]**
The system shall suggest students who need remedial help from tests, homework and attendance, for the teacher to tick and send to the coordinator.
- Acceptance: Given class data When the list opens Then each row shows class, reason and topic (for example "absent 4 of last 6 days; 6/20 in class test 2; Quadratic equations"); all are ticked; unticking changes the button count ("Send 6 students to Mrs. Sinha" becomes 5).
- Acceptance: Given "Send 6 students to Mrs. Sinha" When pressed Then the list locks to "✓ 6 students sent" and the coordinator receives them.
- Rules: Students whose pattern looks like a wellbeing change (for example 72% to 41% in a month and quieter in class) are not listed as remedial; the row offers "Refer to the counsellor" instead, and only the counsellor sees the reason.

**AI-REM-002 · Must · MVP · flag: ai.remedial_grouping · [Design]**
The academic coordinator can create Saturday remedial groups by topic from the students at risk, with parents told after the coordinator's approval.
- Acceptance: Given "46 students below 40% in 2+ subjects" When "Create groups" is pressed Then 6 remedial groups are drafted by topic, shown for review, and parents are told only after the coordinator confirms.
- Rules: Group size cap and Saturday slots are tenant configuration (default 8 per group) [Spec].

#### At-risk detection (ai.at_risk_detection)

**AI-RSK-001 · Must · MVP · flag: ai.at_risk_detection · [Design]**
The system shall flag students below a threshold on marks, attendance or absence days, with the numbers shown.
- Acceptance: Given default rules When evaluated Then "below 40% in 2 or more subjects" flags a student for academic risk; attendance flags use the principal's setting ("Flag students below 90% / 85% / 75%" or "absent at least 3+ / 5+ / 8+ days in 30"), default 85%.
- Acceptance: Given a flag When opened Then it shows the values, the dates, and the rule that fired.
- Rules: Thresholds are tenant configuration with the CBSE 75% note. Flags are only visible to roles with a need (class teacher, coordinator, principal, counsellor); they are never shown to parents or students as a label.

**AI-RSK-002 · Should · MVP · flag: ai.at_risk_detection · [Design]**
The system shall suggest counsellor check-ins from falling attendance, marks and teacher notes, as suggestions only.
- Acceptance: Given Rohan Tiwari 12-A (attendance 71.8% falling since Aug, Maths 32, Physics 30) When the counsellor opens Check-ins Then he is listed with those numbers and "you decide"; nothing is sent to him or to parents.
- Rules: Parents are told only after the first session unless the counsellor chooses otherwise. Phase: signals from about a year of data are P3 ("early warnings", roadmap Phase 2); MVP uses current-term data only. Flag proposed: ai.counselling_assist for check-in suggestions, free-slot booking and note drafts.

**AI-RSK-003 · Must · MVP · flag: ai.at_risk_detection · [Spec]**
The system shall apply fairness checks to at-risk flags (see AI-QLT-005) and explain each flag in plain words.
- Acceptance: Given a flag When shown Then a "Why flagged" line lists every factor and weight in words and states "Dhruva's flag is advice. A teacher or counsellor decides."

#### Admissions scoring (ai.admissions_scoring)

**AI-ADM-001 · Must · MVP · flag: ai.admissions_scoring · [Design]**
The system shall rate each enquiry hot, warm or cold and propose exactly one next step.
- Acceptance: Given a new enquiry When created Then a temperature chip and a "Dhruva's next step" card with a single button appear (for example "Send welcome and book calls").
- Acceptance: Given a logged call (outcome required: interested, call back, not reachable, not interested) or a tour feedback When saved Then temperature and next step recompute and the change is shown with its reason.
- Rules: Inputs allowed: stage, source, grade, recency, call outcomes, tour feedback, seat availability, response speed. Not allowed: religion, caste, gender, disability, family income unless collected for fee concession and not for scoring, address as a proxy for caste or religion, or parent's occupation [Spec]. Temperature never auto-rejects or auto-closes a family; seat offers and rejections are human decisions.

**AI-ADM-002 · Should · MVP · flag: ai.admissions_scoring · [Design]**
The system shall draft the WhatsApp message from the last call, the campus-tour route from what the family wants to see, and pick the next waitlist families by date and sibling priority.
- Acceptance: Given "9 follow-ups overdue" When "Send follow-ups" is pressed by the admissions user Then 9 personal messages are sent and replies come to the inbox; before it, each draft is editable.
- Acceptance: Given "Nursery: 2 seats free" When "Offer to next 2" is pressed Then offers go to the 2 families Dhruva named, valid 7 days, and the waitlist moves up.
- Rules: Waitlist order rules (date, sibling) are shown with each pick, and the user can substitute another family with a reason.

#### Fee follow-up (ai.fee_followup)

**AI-FEE-001 · Must · MVP · flag: ai.fee_followup · [Design]**
The system shall draft fee reminders in English or Hindi with a pay link, track replies, and turn long-overdue dues into a call list.
- Acceptance: Given overdue dues When the accounts user opens "Fee follow-up" Then drafts are listed per family or per age bucket; sending requires approval; replies are tracked on the family record.
- Acceptance: Given the 90+ day group When opened Then it becomes a call list with call-note fields.
- Rules: Tone limits: no threats, no disclosure of amounts to anyone but the account holder; reminders respect quiet hours and the school's reminder cadence (for example a week before due, receipt after payment). Concession decisions remain in Approvals.

#### Payroll checks (ai.payroll_checks)

**AI-PAY-001 · Must · MVP · flag: ai.payroll_checks · [Design]**
The system shall check each payroll run against the previous month and list exceptions, each with two choices and a recommended first choice.
- Acceptance: Given the October teaching run When prepared Then "Dhruva checked this run against September and found N things to fix"; each exception (for example bank account changed 7 Oct and IFSC does not match, "Blocks payment") shows two choices plus "Open employee".
- Acceptance: Given "Send for approval" When pressed Then the principal receives the summary, what changed and Dhruva's checks; payment cannot be released without her approval.
- Rules: Dhruva also prepares: leave over balance settled as comp-off first else unpaid (suggestion buttons carry the recommended choice), final settlement figures for exits, and the bank file (generated; released only on "Send bank file and release payslips"). A "Blocks payment" exception must be resolved by a person; it cannot be auto-resolved. Salary values go to the model only per AI-CTL-006. Flag proposed for HR drafting items beyond payroll checks (CV shortlist, adverts, letters): ai.hr_assist.

**AI-PAY-002 · Should · MVP · flag: ai.hr_assist · [Design]**
HR can have Dhruva shortlist candidates against a post, draft an advert, and calculate a final settlement for the principal.
- Acceptance: Given 38 applications for PGT Maths When "Dhruva read every CV against the post" Then 6 are shortlisted with reasons and HR chooses who gets a demo-class invite.
- Rules: Shortlisting uses only job-relevant fields (qualification, experience, subject); excluded: name, gender, age, photo, address, marital status, religion [Spec]. A candidate is never rejected by Dhruva.

#### Bank matching (ai.bank_matching)

**AI-BNK-001 · Must · MVP · flag: ai.bank_matching · [Design]**
The system shall auto-match bank statement lines to fee receipts and vouchers, and give each unmatched line a suggestion with two buttons.
- Acceptance: Given a September statement of 1,212 lines When "Dhruva auto-match" runs Then matched lines are listed with the matching key (reference, amount, parent name or phone) and unmatched ones each show a suggestion (unidentified NEFT, bank charges, bounced cheque, gateway fee split, missing payment voucher).
- Acceptance: Given "23 UPI fee payments without a student reference" When "Accept 23 matches" is pressed Then 23 are matched by amount and the parent's phone number, toast "23 UPI payments matched by amount and parent's phone number".
- Rules: Posting and closing the month produces a BRS and stays a finance user action. Match confidence below 0.95 is never auto-accepted; bulk accept is shown only for exact amount plus phone or reference matches [Spec]. Related finance assists (bill-to-PO-to-receipt match, three quotes, TDS calculation, Tally fix suggestions, deposit slip, depreciation journal draft) share this review-and-post pattern under proposed flag ai.finance_assist.

#### Security triage (ai.security_triage)

**AI-SEC-001 · Must · MVP · flag: ai.security_triage · [Design]**
The system shall merge duplicate reports into one job, rank its priority, and suggest the assignee with a reason and availability.
- Acceptance: Given 9 teachers report "Wi-Fi down on Senior block 2nd floor" When Dhruva groups them Then one job shows "9 teachers reported it; Dhruva made it one job · Mr. Ajay Pal is free" with button "Assign Ajay".
- Acceptance: Given an unknown man waiting 40 minutes at Gate 2 When reported Then it is ranked Urgent with "Send Harish" as the suggestion.
- Rules: The in-charge assigns; Dhruva never dispatches. At the gate, Dhruva matches names and photos with the authorised list for early pickups and pre-flags an unlisted person; a decision to release a child is always a guard's. The night roster ("Diwali break: 3 nights without a guard") is filled fairly (at most 2 nights each, rest day after each) and guards are told only after confirmation.

#### Transport alerts (ai.transport_alerts)

**AI-TRN-001 · Must · MVP · flag: ai.transport_alerts · [Design]**
The system shall detect late buses and breakdowns from attendant taps and route data, and draft the parent message and the in-charge's options.
- Acceptance: Given a breakdown with 22 children on board When raised Then the card shows "Bus 14 broke down at Ambience Mall: 22 children on board since 7:14 am · spare Bus 25 is 14 minutes away · Dhruva wrote the message to 38 families" with buttons to send the spare bus and the message.
- Acceptance: Given Bus 9 late 7 of last 10 mornings When asked Then Dhruva shows the pattern and proposed new stop times; routes needing change come as two options for the in-charge to choose.
- Rules: Safety alerts (breakdown, child not picked) bypass quiet hours for staff, and the parent message always needs the in-charge's tap; no location is inferred without attendant taps (no GPS in MVP).

#### Student tutor (ai.student_tutor)

**AI-TUT-001 · Must · MVP · flag: ai.student_tutor · [Design]**
The system shall answer a student's question with a hint first, and let the student reach the teacher only after saying the hint was not enough.
- Acceptance: Given a subject and a question When "Ask" is pressed Then a card "Dhruva's hint · A nudge, not the answer" appears with buttons "Got it now" (saves to doubts list) and "Still stuck?".
- Acceptance: Given "Still stuck?" When tapped Then the question goes to the subject teacher with the hint attached; before that the teacher sees nothing.
- Rules: Dhruva does not give final answers to homework or test questions and says so ("I won't do your homework"); full rules in AI-QLT-006.

**AI-TUT-002 · Must · MVP · flag: ai.student_tutor · [Design]**
The system shall build the student's daily plan from teacher-set work, notes, quizzes and marks (quests for Classes 6 to 8, study plan and readiness for Classes 9 to 12), with the method visible.
- Acceptance: Given "How your 77% is worked out" When opened Then it explains readiness as the average of Revised (share of topics ticked off) and Practice (average over the last 30 days).
- Acceptance: Given a quest When shown Then its source line names the teacher's homework, note or quiz; quests come only from teacher-set material.
- Rules: Points are awarded only on first correct answers; Dhruva marks practice sets and shows missed steps.

#### Voice input (ai.voice_input)

**AI-VOI-001 · Should · P2 · flag: ai.voice_input · [Design]**
Staff, bus attendants and parents can speak a question or request in Hindi or English; Dhruva shows what it heard and asks for confirmation before acting.
- Acceptance: Given a voice note "I need leave tomorrow" When transcribed Then Dhruva replies "I heard: 'I need leave tomorrow' / Shall I apply casual leave for tomorrow, 7 Oct?" with "Yes, apply" and "No"; "No" gives "Okay, nothing was sent."
- Acceptance: Given audio that cannot be understood When processed Then the reply is "Sorry, I didn't understand that. You can open the menu or send a voice note." with "Main menu".
- Rules: Voice for the bus attendant (English or Hindi, in app) is MVP as a typed or spoken question ("Who is absent today?", "What time is the next stop?"); WhatsApp voice follows `ch.whatsapp.voice` (Section 8). Audio is discarded after transcription (AI-CTL-009); the transcript is kept as a prompt.

#### Translation (ai.translation)

**AI-TRL-001 · Should · MVP · flag: ai.translation · [Design]**
The system shall translate drafted notices, fee reminders and transport messages between English and Hindi, with the sender seeing both versions before sending.
- Acceptance: Given a notice draft When "Translate" or Hindi is chosen Then the Hindi text appears next to the English and both are editable; sending applies to the version(s) shown.
- Rules: Bilingual drafting appears in the MVP designs (notices, transport, fee follow-up) even though the scope table puts Hindi Dhruva in Phase 1 (Open question 1). Names, amounts and dates are never translated or reformatted by the model; they are inserted from data after translation [Spec].

**AI-TRL-002 · Should · P2 · flag: ai.translation · [Design]**
The system shall deliver Hindi interface text and Hindi answers for chat, voice and WhatsApp.
- Acceptance: Given a Hindi-language user When chat answers Then Hindi script replies with correct numerals and rupee formatting, and button labels switch to Hindi.
- Rules: Other regional languages: P3.

#### WhatsApp bot (ai.whatsapp_bot)

**AI-WAB-001 · Should · P2 · flag: ai.whatsapp_bot · [Design]**
The system shall let Dhruva answer registered parents, teachers and staff on WhatsApp from live records, using menus and buttons, and hand over to a person on request.
- Acceptance: Given a registered number sends "Hi" When received Then Dhruva greets by name and offers "Choose a topic"; unknown numbers get a polite reply to contact the school office.
- Acceptance: Given "Talk to the school office" When chosen Then "Connecting you to the school office…" and a human takes over until the user types MENU.
- Rules: This section governs the AI behaviour (scoping, drafts, confirmation, audit, never asking for UPI PIN or OTP, payslip behind a 4-digit PIN, "Dhruva never asks for this PIN anywhere else"); Section 8 governs templates, session windows, opt-in and STOP. Chat flags apply: `ch.whatsapp.parent_bot`, `ch.whatsapp.teacher_bot`, `ch.whatsapp.staff_bot`, `ch.whatsapp.photo_upload`, `ch.whatsapp.voice`. Phase 1 per scope. Parents cannot send photos to Dhruva (attachments go to the office).

**AI-WAB-002 · Must · P2 · flag: ai.whatsapp_bot · [Spec]**
The system shall apply the same role-scoped retrieval, approval, audit and quota rules to every WhatsApp AI action as to the app.
- Acceptance: Given a parent whose number is linked to 3 schools When Dhruva asks "Which school?" and the parent picks one Then answers are scoped to that school and profile only.
- Acceptance: Given a leave request or attendance published via WhatsApp When approved or published Then the audit log records channel "whatsapp", number hash and the confirming reply.

**AI-WAB-003 · Should · P2 · flag: ai.whatsapp_bot · [Design]**
The campus admin can see WhatsApp assistant usage: chats this week, percentage answered by Dhruva, percentage handed over, average reply time.
- Acceptance: Given the admin settings card When opened Then tiles show values such as "1,284 chats this week", "91% answered by Dhruva", "9% handed over", "4 sec average reply".

#### Data import checks (ai.data_import_checks)

**AI-IMP-001 · Should · MVP · flag: ai.data_import_checks · [Design]**
The system shall check uploaded onboarding data sheets and suggest campus setup choices, for the onboarding lead or principal to accept.
- Acceptance: Given an uploaded student sheet When checked Then Dhruva lists missing phone numbers, duplicate students and non-existent classes with row numbers, and imports nothing it flagged until a person fixes or skips each row.
- Acceptance: Given campus setup step 6 When "Fill with Dhruva's suggestions" is pressed Then unassigned sections get a class-teacher suggestion (teacher with the most periods in that class, free teachers first), toast "Filled 6 sections · check and change any".
- Rules: Setup tips (for example "use the name as on the CBSE affiliation letter") are advice only.

### 5.3.5 AI control plane

**AI-CTL-001 · Must · MVP · flag: core · [Spec]**
The system shall make AI an explicit, off-by-default tenant setting, enabled only after the tenant AI administrator records consent to the AI data-use terms.
- Acceptance: Given a new tenant When provisioned Then all `ai.*` flags are off and no prompt leaves the platform until "Turn on Dhruva" is completed with a consent record (who, when, terms version).
- Acceptance: Given the terms version changes When the next admin session starts Then re-consent is requested; until then new AI use is paused and existing approvals still work.
- Rules: Group owners set a group default; campuses may only narrow it (cannot turn on what the group forbids).

**AI-CTL-002 · Must · MVP · flag: core · [Spec]**
The tenant AI administrator can switch each AI capability on or off per tenant, campus, role or schedule (see TFC-FLAG-004), and see the effect before saving.
- Acceptance: Given the capability list When a toggle changes Then a preview states what disappears ("Teachers will no longer see 'Snap the mark sheet'; typing marks still works") and applies within 60 seconds.
- Rules: Each toggle writes an audit entry; module flags off imply the module's AI capabilities off.

**AI-CTL-003 · Must · MVP · flag: core · [Spec]**
The system shall support per-role visibility of Dhruva, so a tenant can hide Dhruva for roles such as students or parents while keeping it for staff.
- Acceptance: Given Ask Dhruva is hidden for role Parent When a parent opens the app Then no orb, no focus-card AI wording and no chat entry appear, and manual cards still list tasks.

**AI-CTL-004 · Should · MVP · flag: core · [Spec]**
The system shall let the tenant configure suggested-question chips, tone (formal or friendly), and signature name per role.
- Acceptance: Given a configured chip list When chat opens Then only active chips show.

**AI-CTL-005 · Must · MVP · flag: core · [Spec]**
The system shall let the tenant require human approval for each AI action type, with locked-on defaults that cannot be switched off.
- Acceptance: Given the approval-settings table When viewed Then these are locked on: any message to parents or students; any change to marks, attendance or fees records; payroll release; bank posting; admissions offers; counsellor notes; timetable publish. Others (for example auto-answering simple doubts from shared notes, grouping duplicate jobs) default to "show, no approval needed" and can be set to "approval required".
- Rules: Locked items show a lock icon and the text "Required for safety. Cannot be changed."

**AI-CTL-006 · Must · MVP · flag: core · [Spec]**
The system shall send the model only the minimum fields a task needs, replacing direct identifiers with tokens where the task allows, and block fields marked never-send.
- Acceptance: Given a reply-draft task When the prompt is built Then student names are replaced by tokens (for example S1), phone numbers, addresses, Aadhaar, bank accounts, health and counselling content are removed, and tokens are restored in the draft locally.
- Acceptance: Given the field policy table (Annex) When a developer adds a new AI task Then it must declare fields; undeclared fields are dropped.
- Rules: Never-send for all tasks: Aadhaar and government IDs, bank account and card numbers, UPI PIN/OTP, passwords, health records, counsellor session notes. Names and marks go only to tasks that need them. Payroll tasks use employee IDs and amounts; names are tokenised. Photos for OCR (marks, registers) go to the OCR provider with identifiers cropped where possible and are deleted per AI-CTL-009.

**AI-CTL-007 · Must · MVP · flag: core · [Spec]**
The system shall contractually and technically ensure that tenant data and prompts are not used to train or improve any model, and that providers retain nothing beyond the retention window.
- Acceptance: Given each provider in the model registry When onboarded Then a signed zero-retention or no-training term is recorded and shown on the tenant's "About Dhruva · How your data is used" page.
- Rules: DhruvaOne's own evaluation uses only synthetic data and tenant-approved, de-identified feedback samples (AI-QLT-009). Providers must serve from India region or be covered by the tenant's cross-border consent; default is India region only. The processing roles follow DPDP: school is the data fiduciary, DhruvaOne the processor.

**AI-CTL-008 · Must · MVP · flag: core · [Spec]**
The system shall publish "About Dhruva · How your data is used" in the app Me tab, listing what Dhruva reads, what it sends to the model, retention, and how to turn it off.
- Acceptance: Given Me > About Dhruva When opened Then the page lists data categories sent per capability, retention, provider region and the grievance contact.

**AI-CTL-009 · Must · MVP · flag: core · [Spec]**
The system shall retain prompts, outputs and uploaded images only as long as needed, with tenant-configurable limits.
- Acceptance: Given defaults When time passes Then raw chat text is kept 90 days, prompt and output records for approved actions 1 year (needed by the audit trail, with PII tokens kept as tokens), uploaded photos and audio 24 hours after processing or until the teacher confirms, whichever is later, and never more than 7 days.
- Rules: The AI audit log (AI-AUD-001) is kept 7 years with the underlying records. A user's deletion request (access, correction, deletion approved by the school) removes their chat history within 30 days; audit entries are anonymised, not deleted.

**AI-CTL-010 · Must · MVP · flag: core · [Spec]**
The system shall enforce usage quotas and cost caps per tenant, per capability and per user, and warn before they are reached.
- Acceptance: Given a plan quota of 200,000 AI requests per month and 80% used When the next request is made Then the AI administrator is notified ("Dhruva usage at 80% for October"); at 100% non-essential capabilities (chat, drafts) show "Dhruva is resting for today. You can still do this yourself." while safety capabilities (transport alerts, security triage) continue until a hard cap of 120%.
- Acceptance: Given per-user limits When a user exceeds 60 chat questions per hour or 300 per day Then further questions are throttled with a friendly message.
- Rules: Defaults in the Annex "Limits and defaults". Plan numbers are commercial inputs (Open question 7).

**AI-CTL-011 · Must · MVP · flag: core · [Spec]**
The system shall provide a kill switch that stops all AI processing for a tenant (tenant AI administrator) or for all tenants (platform operator) immediately.
- Acceptance: Given "Pause Dhruva" is pressed When confirmed Then within 30 seconds no new model call is made, drafts in progress are marked "Dhruva paused", approved items stay as saved, and every manual path works.
- Rules: The platform kill switch is also bound to automated triggers (provider incident, safety-evaluation failure). Resuming requires an explicit action and is logged.

**AI-CTL-012 · Must · MVP · flag: core · [Spec]**
The system shall define fallback behaviour when AI is off, fails, times out or is rate-limited.
- Acceptance: Given a model call exceeds 15 seconds [Spec] or errors When the user is waiting Then the screen shows "Dhruva is taking too long. Try again, or do this yourself" with the manual control focused; there is one automatic retry for read-only requests and none for approvals.
- Acceptance: Given the focus card cannot be ranked by AI When opened Then the rule-based ranking (AI-FOC-002) shows with plain item titles and no Dhruva reason lines.
- Acceptance: Given cover, bank-match or similar suggestions are unavailable When the page loads Then rule-based fallbacks apply where a rule exists (cover: free teachers by subject and fewest covers; bank: exact reference and amount) and otherwise the list is shown without suggestions.
- Rules: Provider failover to a secondary model within the same data-use terms is allowed if its terms are recorded (AI-CTL-007); otherwise degrade rather than fail over.

**AI-CTL-013 · Should · MVP · flag: core · [Spec]**
The system shall rate-limit AI endpoints per user, per tenant and per IP, and detect prompt-injection attempts in user-supplied text and uploads.
- Acceptance: Given text in an uploaded document or parent message that tells the model to ignore rules When processed Then it is treated as data, a guard flags it, the answer ignores it, and the event is logged.
- Rules: Retrieved content is passed to the model delimited and typed as data; the model cannot call write APIs, only create Suggestions (Annex).

### 5.3.6 Quality, safety, fairness and audit

**AI-QLT-001 · Must · MVP · flag: core · [Spec]**
The system shall assign each AI output a confidence level and apply thresholds by action type.
- Acceptance: Given an output When confidence is below the capability's threshold (OCR 0.90; classification 0.80; bank match 0.95; generation uses a self-check score 0.70) Then it is shown flagged ("Dhruva is not sure") or not shown, never silently accepted.
- Rules: Thresholds are platform defaults, tightenable by tenant, not loosenable below the platform floor.

**AI-QLT-002 · Must · MVP · flag: core · [Design]**
When Dhruva is unsure or lacks data, it shall say so, show what it did find, and offer a person or a manual route.
- Acceptance: Given data is missing (for example no marks yet) When asked Then the answer says "I don't have this yet" with what is available, never a guess.
- Acceptance: Given low confidence When displayed Then the reason, such as "DHRUVA WASN'T SURE", appears on the item and the item is routed to the person.

**AI-QLT-003 · Must · MVP · flag: core · [Design]**
The system shall take every number, date, name and amount in an AI answer or draft from records, never from the model's text.
- Acceptance: Given a draft or answer When generated Then each figure is placed by the application from a query result (templated slot) and verified by a post-check that every numeral in the text exists in the retrieved data; failures block display and retry once, then fall back to "I couldn't confirm the numbers".
- Rules: Aggregates are computed by the system (SQL), not by the model. The post-check logs misses as quality incidents.

**AI-QLT-004 · Must · MVP · flag: core · [Spec]**
The system shall apply content filters to inputs and outputs for all roles, stricter for students and anything reaching families.
- Acceptance: Given an output with abuse, sexual content, self-harm advice, caste or religion bias or personal data of others When filtered Then it is blocked and replaced by a neutral message; a safety incident is logged.
- Rules: Drafts to families run an extra tone check (no threats, no shaming, no medical or legal claims).

**AI-QLT-005 · Must · MVP · flag: core · [Spec]**
The system shall test at-risk and admissions scoring for bias and keep them explainable.
- Acceptance: Given each release When evaluated Then flag rates by gender, RTE status, house, transport route and campus are compared on a held-out set; a disparity above 1.25 times the overall rate blocks release until reviewed.
- Rules: Prohibited inputs are listed in AI-ADM-001 and AI-PAY-002. Every flag has "Why flagged". A person can mark "Not a concern" and that suppresses the flag for 30 days.

**AI-QLT-006 · Must · MVP · flag: ai.student_tutor · [Spec]**
The system shall apply child-safety rules to the student tutor.
- Acceptance: Given a student message about self-harm, abuse, bullying or fear When detected Then Dhruva answers with a calm, fixed supportive message and the school's helpline, and notifies the counsellor and class teacher per school policy (message text shown to the student: "I'm worried about you. I've asked someone at school to check in.").
- Acceptance: Given a request for the final answer to homework, an exam question, or to write an essay When asked Then Dhruva gives hints and steps only.
- Acceptance: Given a request to chat about topics off-curriculum, personal data, contact details or to meet anyone When asked Then Dhruva declines and redirects.
- Rules: Tutor answers come only from the teacher's notes and curriculum; no external browsing; no image generation of people; session text is visible to the child's class teacher on escalation only, not routinely; no advertising or tracking. Parents see tutor usage counts, not transcripts, unless the child's profile is under policy review. For Classes 6 to 8 interaction is more tightly scoped than for 9 to 12 (reading level and word limit).

**AI-QLT-007 · Must · MVP · flag: core · [Spec]**
The system shall explain any AI output on request ("How is this worked out?") in plain language, listing inputs, rules and the model's role.
- Acceptance: Given a readiness score, at-risk flag, temperature chip, bank match or cover pick When "How? ⓘ" is tapped Then a sheet explains the inputs and the rule in under 120 words.

**AI-QLT-008 · Should · MVP · flag: ai.assistant_chat · [Spec]**
The system shall capture feedback and corrections: thumbs, reason, and the edit the user made to a draft before approving.
- Acceptance: Given a draft edited before sending When sent Then the original and final text (de-identified) are stored as a correction with the draft's PromptTemplate version.
- Rules: Edit distance is a quality metric (AI-QLT-009). Feedback is visible to the tenant AI administrator in aggregate.

**AI-QLT-009 · Must · MVP · flag: core · [Spec]**
The platform shall evaluate each capability before release and monitor it in production.
- Acceptance: Given a new PromptTemplate or ModelConfig When proposed Then it passes an offline evaluation set per capability (accuracy of numbers 100% for grounded slots, OCR mark accuracy at least 98%, clash-free timetable 100% of produced drafts, cover pick legality 100%) before rollout, and is rolled out to 5% of tenants first.
- Acceptance: Given production When running Then dashboards track approval rate, edit distance, thumbs-down rate, fallbacks, latency p50 and p95, cost per request and guard hits; alert if approval rate falls 15 points week on week or any grounded-number mismatch occurs.
- Rules: Evaluation sets contain synthetic or consented, de-identified data only.

**AI-AUD-001 · Must · MVP · flag: core · [Design]**
The system shall log every AI action, with who asked, what was produced, what it was based on, and who approved it, and make the log viewable by the tenant AI administrator and principal.
- Acceptance: Given any AIRequest, Suggestion or Approval When it occurs Then an immutable log entry exists with actor, role, profile, campus, channel, capability, template and model version, input record IDs, output hash, decision (approved, edited, rejected, expired), approver and time.
- Acceptance: Given the AI log screen When filtered by capability, person or date Then entries list within 3 seconds for a 90-day range and can be exported to CSV.
- Rules: Website claim "every approval is logged" must hold for every row of Section 5.3.4. Entries are append-only and cannot be edited by tenant users.

**AI-AUD-002 · Should · MVP · flag: core · [Spec]**
The system shall let a user see what Dhruva did on their behalf and undo reversible actions within the stated window.
- Acceptance: Given a published item with Undo (marks, attendance from photo) When "Undo" is pressed within 24 hours or before dependent actions (report card compiled) Then the prior state is restored, parents told of a correction if they had been notified, and the audit shows the reversal.

### 5.3.7 Halo orb (UI requirement)

**AI-HLO-001 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall show the Halo orb as the one colourful element on every phone screen and as the "Ask Dhruva" entry on desktop, in six states.
- Acceptance: Given the orb When used Then states are: Idle (breathes slowly, blinks every 4 s; default); Listening (eyes tall, violet pulse, mic open); Thinking (ring spins fast, eyes glance up and right); Done (smiling eyes for 2 s after a task finishes); Needs you (amber ring and pulse, urgent only: overdue fees, safety); Quiet hours (dim ring, closed eyes, no sound or buzz).
- Acceptance: Given "Reduce motion" is on When any state shows Then it is a still pose and the ring does not spin.
- Rules: The multi-colour ring appears only on Dhruva (icon, orb, assistant button, first-run splash), never on buttons or text, so it always means AI. AI moments use the Dhruva colour (#8B3CF0); Deep #14183A is the orb background. Parent tab bar puts Dhruva in the centre; staff phones show the orb floating; Android uses an extended "Ask Dhruva" button. The orb also appears as the Dhruva marker on drafts (AI-PRN-005). When AI is off for the role (AI-CTL-003) the orb is removed, not greyed.

**AI-HLO-002 · Should · MVP · flag: ai.assistant_chat · [Spec]**
The orb shall expose accessible names and state to screen readers ("Dhruva, thinking") and respect system dark mode and larger text.
- Acceptance: Given a screen reader When the orb changes state Then it announces the state; touch target is at least 44 pt.

## 5.4 Business rules and policies

1. Approval rule: any AI item that changes a record or reaches a person outside the approver's own screen needs a named human approval (AI-PRN-001, AI-CTL-005).
2. Truth rule: numbers, names, dates and amounts come from records; the model supplies wording only (AI-QLT-003).
3. Scope rule: Dhruva sees exactly what the asker could open in the app; role, campus and profile boundaries are enforced before the model is called (AI-CHT-005).
4. Privacy rule: minimum fields, tokenised identifiers, never-send list, no training on tenant data (AI-CTL-006, AI-CTL-007).
5. Manual rule: every AI task has a manual path (AI-PRN-004).
6. Child rule: Dhruva never gives students final answers, never contacts families on its own and escalates safety signals to people (AI-QLT-006).
7. Fairness rule: no prohibited attributes in scoring; flags are advice with reasons (AI-QLT-005).
8. Delegation rule: bulk buttons are allowed because the tapper approves the whole batch and sees the count first; each item is still logged.
9. Language rule: English now; Hindi from P2; names, amounts and dates are inserted from data in all languages.
10. Money rule: Dhruva never initiates, approves or releases a payment, refund, concession or salary; it only prepares.
11. Stale-data rule: an answer is labelled with the data's as-of time when any source is older than 24 hours ("As of 6:00 am").

## 5.5 Notifications and approvals raised by this section

| Trigger | Who is notified or asked | Channel | Notes |
|---|---|---|---|
| Suggestion proposed (cover, remedial, bank, etc.) | Owner of the task (role queue) | Focus card, in-app | No push unless deadline tier 1 or 2 (AI-FOC-002). |
| Draft ready for approval (notice, reply, reminders) | Author | In-app | Expires per AI-CTL-005 settings. |
| Timetable draft ready or clash left | Academic coordinator | In-app, push | Draft stays private. |
| Timetable approved | Affected teachers, parents | App, WhatsApp | Section XCT rules; effective on "Use from" date. |
| AI quota at 80% or 100% | Tenant AI administrator | In-app, email | AI-CTL-010. |
| Kill switch used, AI paused or resumed | Tenant AI administrator, principal, owner | In-app, email | AI-CTL-011. |
| Provider incident or safety-evaluation failure | Platform operators, affected tenants' AI administrators | Email | Auto-pause possible. |
| Student safety signal in tutor | Counsellor, class teacher | In-app urgent | AI-QLT-006; text to student fixed. |
| Consent or terms version change | Tenant AI administrator | In-app | AI-CTL-001. |
| Feedback "wrong number" reported | Platform quality team | Internal | AI-QLT-008. |

## 5.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| core | AI control plane, consent, kill switch, audit, safety (cannot be disabled) | On | The tenant AI enablement itself is a setting, not a flag (AI-CTL-001). |
| ai.assistant_chat | Ask Dhruva chat, orb, thumbs | Off until tenant consent; then On | Orb hidden if off. |
| ai.focus_card | Dhruva-prepared task card and queue text | On after consent | Rule-based list remains when off. |
| ai.cover_suggestions | Free-teacher cover picks | On after consent | Needs mod.cover. |
| ai.timetable_generator | Timetable generation, clash fixes | On after consent | Needs mod.timetable. |
| ai.reply_drafts | Reply and message drafts, topic routing | On | Needs mod.parent_messaging. |
| ai.notice_drafts | Notice, invite, note drafts | On | Needs mod.notices. |
| ai.marks_from_photo | Photo reading of marks and registers | Off in MVP pilot, enable per campus | Prototype status (design-status); needs mod.marks_results. |
| ai.paper_generator | Paper drafts and blueprint checks | On | Needs mod.exams. |
| ai.lesson_plan_drafts | Lesson plan and notes drafts | On | Needs mod.lesson_plans. |
| ai.homework_marking | Homework checking | On | Needs mod.homework. |
| ai.remedial_grouping | Remedial suggestions and groups | On | |
| ai.at_risk_detection | At-risk flags, check-in suggestions input | On | Fairness checks always on. |
| ai.admissions_scoring | Enquiry temperature and next step | On | Needs mod.admissions_crm. |
| ai.fee_followup | Fee reminder drafts and tracking | On | Needs mod.fees. |
| ai.payroll_checks | Payroll exception checks | On | Needs mod.payroll. |
| ai.bank_matching | Bank statement matching | On | Needs mod.bank_recon. |
| ai.security_triage | Job grouping, assignee, roster fill | On | Needs mod.security_gate or mod.it_helpdesk. |
| ai.transport_alerts | Delay and breakdown drafts, patterns | On | Needs mod.transport. |
| ai.student_tutor | Hint-first tutor, daily plan | Off until school and parent consent | Needs mod.student_learning; AI-QLT-006. |
| ai.voice_input | Speech to text | Off in MVP | P2. |
| ai.translation | English and Hindi drafting and answers | Off | P2 for chat; drafts MVP. |
| ai.whatsapp_bot | Dhruva on WhatsApp | Off | P2; also needs ch.whatsapp. |

## 5.7 Non-functional requirements (specific to AI)

- Latency: chat answers p95 under 5 seconds; draft generation under 10 seconds p95; timetable under 60 seconds; OCR of a 36-row sheet under 8 seconds p95.
- Availability: AI features 99.5% monthly; manual paths follow platform availability (not reduced by AI outage).
- Accuracy targets: grounded-number errors 0 tolerated; OCR mark accuracy at least 98% before confirmation; cover and clash suggestions legal 100%.
- Cost: per-tenant monthly cost is metered per capability; cost per active user shown to platform operators; model selection by cheapest model passing evaluation.
- Data residency: model inference in India region for prompts containing student or staff data.
- Observability: every request has a trace ID visible in the audit log; user-visible error text never contains provider messages.
- Accessibility: orb, chat and cards meet WCAG 2.1 AA; reduced motion supported.
- Scalability: 1 million AI requests a day across tenants at launch capacity [Spec].

## 5.8 Open questions

1. Languages: the app's first-run offers six languages (English, Hindi, Punjabi, Gujarati, Marathi, Tamil) while notification rules and the scope table confirm only English and Hindi for Dhruva, with Hindi and regional in Phase 1. Confirm that Hindi chat is P2, and whether bilingual drafting (notices, fee, transport) is MVP as the prototypes show.
2. Publishing without teacher review: design-status says marks and learning plans publish without a teacher review step, and WhatsApp photo publish has Undo only. This spec requires teacher confirmation (AI-MKS-002, AI-HWK-001). Confirm with the client.
3. Photo reading is a prototype; which OCR provider, languages of handwriting (Hindi, English) and expected accuracy are not decided.
4. Which model providers, and whether any inference must run on-premises or in an India region only; whether providers must be named on the Sub-processors page.
5. Retention defaults in AI-CTL-009 (90 days chat, 1 year prompts and outputs, 24 hours images) need school and legal confirmation.
6. Whether students under a given age may use the tutor without a separate parental consent (the DPDP rule is consent for each child under 18).
7. Commercial: monthly quota, cost cap and overage policy per plan.
8. Whether the AI audit log is visible to the principal at campus level in groups, or only to the group's tenant AI administrator.
9. Whether Ask Dhruva may answer general (non-school) questions for staff.
10. Whether at-risk "early warning" signals using a year of data move earlier than P3.
11. Thresholds in the design (for example 85% attendance flag, below 40% in 2 subjects) are samples; confirm defaults per board.

## Annex 5-A (engineering)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| AITenantSettings | tenant_id, ai_enabled, consent_id, terms_version, group_default, kill_state, region, quota_plan, cost_cap | One per tenant; campus overrides in AICapabilitySetting. |
| AIConsent | id, tenant_id, signed_by, role, terms_version, signed_at | Immutable. |
| AICapabilitySetting | tenant_id, campus_id?, role?, schedule?, flag_key, enabled, approval_mode, locked | Mirrors TFC flags; locked = approvals that cannot be turned off. |
| ModelConfig | id, provider, model, version, region, purpose (chat, draft, ocr, classify, translate, stt), max_tokens, temperature, timeout_ms, status, terms_ref, cost_per_unit | Registry; rollout percentage. |
| PromptTemplate | id, capability, version, locale, body, slots[], field_policy_ref, status, eval_run_id | Versioned, reviewed; slots filled from data. |
| FieldPolicy | capability, field, treatment (send, tokenise, hash, never) | Drives AI-CTL-006. |
| AIRequest | id, tenant_id, campus_id, actor_id, profile_id, role, channel, capability, input_refs[], template_id, model_id, prompt_tokens, completion_tokens, latency_ms, status, error, trace_id, created_at | Inputs by reference, not copy. |
| AIOutput | id, request_id, content_ref, grounding_refs[], confidence, guard_results, numbers_check, created_at, purge_at | Content encrypted; purged per retention. |
| Suggestion | id, tenant_id, capability, target_entity (type, id), proposed_payload, reason, source_refs[], confidence, state, rank_tier, expires_at, created_for_role | Never writes to the target. |
| ApprovalLink | id, suggestion_id, approver_id, action (approve, edit, reject, bulk), edited_payload_diff, result_entity_ref, channel, approved_at, batch_id | Links the Suggestion to the resulting record change. |
| Draft | id, suggestion_id, kind (notice, reply, plan, paper, reminder), body_by_locale, state, owner_id | Editable text. |
| Feedback | id, output_id, user_id, thumb, reason, original_text_ref, final_text_ref, edit_distance, created_at | De-identified before any export. |
| UsageMeter | tenant_id, capability, period, requests, tokens_in, tokens_out, cost, errors, fallbacks | Rolled up hourly. |
| QuotaPolicy | plan, capability, monthly_requests, per_user_hour, per_user_day, hard_cap_pct | |
| AIAuditEntry | id, ts, tenant_id, actor, role, channel, capability, event, request_id, suggestion_id, approval_id, model_version, template_version, decision, hash_chain | Append-only. |
| SafetyIncident | id, tenant_id, type, severity, request_id, handled_by, status | Student safety, injection, number mismatch. |
| EvalRun | id, capability, template_id, model_id, dataset, metrics, passed, ran_at | Gate for rollout. |

### APIs

| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| POST /v1/ai/ask | Ask Dhruva a question (conversation id optional) | Any signed-in profile with ai.assistant_chat | 403 AI_DISABLED; 429 RATE_LIMITED; 503 AI_UNAVAILABLE; 422 OUT_OF_SCOPE |
| GET /v1/ai/ask/suggestions | Suggested questions for role | Signed-in profile | 403 AI_DISABLED |
| GET /v1/ai/conversations/{id} | Conversation history | Owner of conversation | 404; 410 PURGED |
| POST /v1/ai/conversations/{id}/feedback | Thumbs and reason | Owner | 404 |
| GET /v1/ai/focus | Ranked task list with reasons | Signed-in profile | 200 with rule-based list if AI unavailable |
| POST /v1/ai/focus/{itemId}/later | Defer item | Owner | 404 |
| GET /v1/ai/suggestions | List suggestions for current role (filter by capability, state) | Role queue | 403 |
| GET /v1/ai/suggestions/{id} | Suggestion with reason and sources | Role queue | 404 |
| POST /v1/ai/suggestions/{id}/approve | Approve (optionally edited payload) | Role that owns the target action | 409 STALE_TARGET; 403 NOT_APPROVER; 409 EXPIRED |
| POST /v1/ai/suggestions/{id}/reject | Reject with reason | Same | 409 |
| POST /v1/ai/suggestions/batch-approve | Approve many with one confirmation | Same; max 500 per call | 207 per-item results |
| POST /v1/ai/drafts | Create a draft (notice, reply, paper, plan, reminder) | Capability role | 400 MISSING_SLOT; 429; 503 |
| PATCH /v1/ai/drafts/{id} | Edit or shorten or translate | Owner | 409 |
| POST /v1/ai/drafts/{id}/send | Approve and send through the module's own API | Owner with send rights | 403; 409 |
| POST /v1/ai/ocr/marks | Read a mark sheet photo into a draft entry | Teacher of the class | 413 IMAGE_TOO_LARGE; 422 UNREADABLE |
| POST /v1/ai/ocr/{id}/confirm | Confirm read values | Same | 409 FLAGS_OPEN |
| POST /v1/ai/homework/{id}/check | Run checking on a set | Teacher | 422 NO_KEY |
| POST /v1/ai/voice/transcribe | Speech to text | Signed-in profile with ai.voice_input | 415; 422 UNINTELLIGIBLE |
| POST /v1/ai/translate | Translate a draft | Signed-in profile with ai.translation | 422 UNSUPPORTED_LOCALE |
| GET /v1/ai/usage | Usage and cost per capability | Tenant AI administrator, principal (read) | 403 |
| GET /v1/ai/explain/{outputId} | "How is this worked out" | Anyone who can see the output | 404 |
| GET /v1/ai/models | Model registry (read) | Platform operator | 403 |
| POST /v1/ai/eval/runs | Run an evaluation | Platform quality | 400 |

These AI functions are defined once, elsewhere (see 2.5):
- AI consent, settings, tenant pause and resume, quota and top-up: Section 4 (`/v1/tenants/{id}/ai/...`). The platform-wide AI kill is a platform kill switch with `scope: ai` (`POST /v1/platform/kill-switches`).
- Timetable generation and clash fixing: Section 6 (`/v1/timetables/...`). The generator runs when `ai.timetable_generator` is on.
- AI audit log: `GET /v1/audit?category=ai` and `POST /v1/audit/exports` (Section 9).

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| ai.request.completed | A model call ends | request_id, capability, latency, tokens, status | UsageMeter, monitoring |
| ai.request.failed | Model call errors or times out | request_id, error_class, fallback_used | Monitoring, fallback |
| ai.suggestion.created | A suggestion is proposed | suggestion_id, capability, role queue, tier | Focus card, notifications |
| ai.suggestion.edited | A person edits a draft or payload | suggestion_id, diff size | Feedback |
| ai.suggestion.approved | Approved (single or batch) | suggestion_id, approver, batch_id, result_ref | Module services, audit, notifications |
| ai.suggestion.rejected | Rejected | suggestion_id, reason | Feedback, audit |
| ai.suggestion.expired | Expiry reached | suggestion_id | Focus card, audit |
| ai.safety.incident | Content or student-safety trigger | type, severity, request_id | Counsellor, platform, audit |
| ai.feedback.submitted | Thumb or correction | output_id, thumb, reason | Evaluation |
| ai.eval.completed | Evaluation run ends | capability, metrics, passed | Release pipeline |

Consumed from other sections: `ai.quota_threshold`, `ai.quota_exhausted`, `ai.settings_changed`, `ai.paused`, `ai.resumed` and `killswitch.set` (Section 4); `timetable.approved` (Section 6).

### State machines / workflows

Suggestion states:

| From | Event | To | Rule |
|---|---|---|---|
| (none) | Dhruva proposes | proposed | Visible only to the role queue. |
| proposed | Person edits | edited | Stays editable; diff stored. |
| proposed, edited | Person approves | approved | Record change executed by the module service within the same transaction or compensated; ApprovalLink created. |
| proposed, edited | Person rejects | rejected | Reason optional; no change. |
| proposed, edited | Expiry (default 7 days, 24 hours for cover, 1 hour for safety alerts), or target changed (stale) | expired | Not executable; regeneration allowed. |
| approved | Undo within window | reverted | Only for reversible kinds (AI-AUD-002). |

Other flows:
- Ask pipeline: authenticate profile, resolve scope, retrieval gateway fetches only permitted records, build prompt with field policy, call model, grounding and number check, content filter, respond with sources, log.
- Draft flow: generate, edit, approve and send through the module's own API (so existing permission and notification rules apply), log.
- Timetable flow: draft (private), clashes resolved or applied, per-class approval with use_from, publish, notify.
- Kill switch: set state, reject new calls, mark in-flight, notify, resume by explicit action.

### Permission matrix

Legend: R = receives and uses; A = approves or sends; C = configures; V = views logs; blank = none.

| Capability | Owner | Principal | Coordinator | Exam cell | HoD | Teacher | Counsellor | HR | Finance | Admissions | Security/IT | Transport | Parent | Student | Campus admin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ask Dhruva (scoped) | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| Focus card | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| Cover suggestions | | | A | | | R (own cover) | | | | | | | | | A |
| Timetable generator | | R | A | | | R | | | | | | | | | A |
| Reply drafts | | A | A | | A | A | | | | | | A | | | A |
| Notice drafts | A | A | A | A | A | A | A | | | A | | A | | | A |
| Marks from photo | | | | R | | A | | | | | | | | | |
| Paper generator | | | | A (moderate) | A (review) | A (set) | | | | | | | | | |
| Lesson plans | | | R | | A (review) | A | | | | | | | | | |
| Homework marking | | | | | R | A | | | | | | | | R (status) | |
| Remedial grouping | | R | A | | | A | R (referral) | | | | | | | | |
| At-risk detection | | R | R | | R | R (class) | R | | | | | | | | R |
| Admissions scoring | R | R | | | | | | | | A | | | | | |
| Fee follow-up | R | R | | | | | | | A | | | | | | A |
| Payroll checks | | A (approve) | | | | | | A | R | | | | | | |
| Bank matching | | | | | | | | | A | | | | | | |
| Security triage | | | | | | | | | | | A | | | | |
| Transport alerts | | R | | | | | | | | | | A | R | | |
| Student tutor | | | | | | R (escalations) | R (safety) | | | | | | R (counts) | R | |
| Voice, translation | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| WhatsApp bot | | | | | | R | | R (staff) | | | | R (staff) | R | | C (settings) |
| AI settings, quotas, kill switch | C (group) | R | | | | | | | | | | | | | C (standalone) |
| AI audit log | V | V | | | | | | | | | | | | | V |

Notes: Parents and students never see other people's data (AI-CHT-005); owner is the tenant AI administrator for groups; DhruvaOne platform staff hold platform kill switch and evaluation rights only.

### Model and provider abstraction requirements

- All model calls go through one AI gateway service; modules never call providers directly.
- A ModelConfig registry maps purpose (chat, draft, classify, OCR, speech to text, translation, embeddings) to provider and model, with per-tenant overrides, region pinning, timeouts, retries, circuit breaker, and weighted rollout for new versions.
- Providers are replaceable behind a common interface (messages, tools off by default, structured JSON output, streaming optional, usage reporting); no provider-specific prompt text outside PromptTemplate adapters.
- The gateway enforces, before any call: tenant AI enabled, capability flag, role visibility, quotas, field policy and tokenisation, region, kill state; and after: grounding and number checks, content filters, confidence, audit write, usage metering.
- Retrieval gateway: the only path from model prompts to data; takes the asker's identity and returns records already filtered by the same authorisation as the app; returns IDs and values with source labels used in the "Source" line.
- Models never receive write credentials; they return structured Suggestions or Drafts, and module services execute on Approval.
- Deterministic engines (timetable solver, cover ranking, bank-match rules, queue tiers, queue sort) compute results; the model writes explanations and wording only. Fallbacks use the same engines.
- Prompt and template changes are versioned, evaluated (EvalRun) and rolled out gradually; every output records template and model version.
- Zero-retention and no-training terms recorded per provider; secrets and keys in a managed vault; provider outage triggers fallback or pause by policy.
- Cost control: per-request token caps, per-capability budgets, caching of identical read-only answers within one data version (never across users or tenants).

Suggested-question catalogue (sample, from the designs; configurable per role):

| Role | Questions |
|---|---|
| Owner | "Which campuses are behind on onboarding?"; "Why is Gurugram attendance low?"; "How many new students joined this session?" |
| Principal | "How are admissions going?"; "Which classes have the lowest attendance?" |
| Academic coordinator | "Who has taken the most cover periods this week?" |
| HR | "What changed in pay since September?"; "Whose probation ends this month?"; "Which documents expire soon?" |
| Finance | Three questions on collections, dues and bank status (as built). |
| Admissions | "Which families should I call first today?"; "How many seats are left?" |
| Security | "What is still open today?"; "Is everything ready for Monday's exams?" |
| Transport | "Which buses are late most often?" |
| Admin (standalone) | "Who is absent today?" |
| Parent | "How is Navya doing before the exams?"; "What do I need to pay this month?"; "What is happening at school next week?" |
| Student | "What should I revise first?" |
| Attendant | "Who is absent today?"; "What time is the next stop?" (Hindi or English, voice or text) |

Queue tiers (AI-FOC-002): T1 safety and emergencies; T2 deadline today; T3 blocks others; T4 money or compliance at risk; T5 other, oldest first.

Limits and defaults: chat 60 per user per hour, 300 per day; draft 30 per user per hour; OCR 20 images per user per day; timetable generations 10 per day per tenant; AI request timeout 15 s (OCR 30 s, timetable background); retention per AI-CTL-009; suggestion expiry 7 days default; conversation context 10 turns.

### Proposed flags

| Flag | Why needed |
|---|---|
| ai.exam_planning | AI date sheets, seating and invigilation planning, exam duty roster fill (AI-PPR-003); the catalogue has only ai.paper_generator. |
| ai.counselling_assist | Check-in suggestions, free-slot booking, counsellor note and invite drafts (AI-RSK-002, AI-NTC-002); sensitive, so switchable separately from at-risk detection. |
| ai.hr_assist | CV shortlisting, advert drafts, final settlement calculation (AI-PAY-002), separate from payroll checks. |
| ai.finance_assist | Bill-to-PO-to-receipt matching, quotes comparison, TDS calculation, Tally fix suggestions, deposit slip and journal drafts (AI-BNK-001 rules). |
| ai.data_import_checks | Dhruva checks of uploaded data sheets and campus setup suggestions (missing phones, duplicates, class teacher matching) during onboarding; designed in the owner and principal setup journeys but not in the catalogue. |
