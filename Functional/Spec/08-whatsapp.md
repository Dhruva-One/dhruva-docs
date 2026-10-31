# 8. WhatsApp

## 8.1 Purpose, scope and out-of-scope

**Purpose.** Many parents, grandparents, teachers and support staff (drivers, attendants, guards, housekeeping) will not install another app. DhruvaOne gives each school one official, verified WhatsApp Business number. The school sends short pre-approved alerts first. People can also message "Hi" and get a short menu, buttons and small forms that answer from the same live data as the app. There is no password and no sign-in: the sender's phone number is the key, matched to school records. Anything that needs a person is handed to the front office or HR in working hours. The designs' tagline is "No app? No problem. Just WhatsApp the school."

**In scope**
- The school's WhatsApp Business account per tenant and campus: number, verified profile, templates, sender name, health.
- WhatsApp Business Platform rules the product must obey: 24-hour session window, template approval, opt-in and STOP, media limits, receipts, rate limits, quality rating.
- Matching the sender number to parent, teacher and staff profiles; unknown numbers; shared numbers.
- Conversation flows per audience: parents, teachers, staff (menus, forms, photo reading, voice notes, PIN).
- Free-text understanding, intent fallback, handover to a person, office hours, SLA, hand-back.
- School-initiated (outbound) notifications through WhatsApp: events, templates, frequency caps, quiet hours, language.
- Security, content moderation, admin controls, analytics, cost control, failure modes and fallback to push or SMS.

**Out of scope (covered elsewhere)**
- Sign-in OTP delivery and profile model (Section 3 Identity, IDM). WhatsApp only consumes profile matching.
- The content of the underlying modules (attendance, fees, homework, exams, leave, payroll) and their approval rules; WhatsApp is another front end to them (see the module sections).
- The Dhruva assistant's general behaviour, sources and guardrails (see Section AI); this section sets only what is specific to WhatsApp.
- Tenant switch administration screens and flag mechanics (see Section TFC); this section lists the flags it uses.
- Admissions conversations. The Overview shows an "Admissions enquiries" toggle but no flow; only a placeholder is specified (WAB-PAR-011).
- Hindi/regional beyond Hindi and English; group chats; WhatsApp status; calls (calls go to the office, see WAB-MNU-006).

**Phasing note.** MVP build (Oct to Dec 2026) includes "WhatsApp Business": the school's number, alerts, notices and fee reminders. The conversational assistant ("Dhruva on WhatsApp"), Hindi and regional languages, and multi-child parents appear in roadmap Phase 1 (Apr to Sep 2027). This section maps roadmap Phase 1 to **P2** and roadmap Phase 2 to **P3**. The three phone prototypes are drawn as working boards, so the client must confirm whether the bot moves into MVP (see 8.8, Q1).

**Tag convention.** `[Design]` means shown on WhatsAppOverview, WhatsAppParent, WhatsAppTeacher or WhatsAppStaff. `[Spec]` means the product needs it and the designs do not show it. All names, numbers and amounts in the designs are sample data.

## 8.2 Actors and roles

| Actor | Role in this section |
|---|---|
| Parent / guardian (for example Pooja Sharma) | Receives alerts; chats with Dhruva about their own child; pays fees by UPI; applies for leave |
| Teacher (for example Ms. Shalini Batra) | Marks attendance, posts homework, sends photos of registers and marks sheets, applies for leave, opens payslip |
| Support staff (for example Suresh Yadav, driver of Bus 12) | Payslip, leave, attendance, duty, holidays, salary advance, in Hindi or English, text or voice |
| Dhruva (bot) | Answers from live data, drafts, reads photos and voice notes; never changes a record or reaches a family without the required person approving or the sender confirming |
| Front office agent (for example Anita) | Takes over parent and teacher chats Mon to Sat, 8 am to 4 pm |
| HR agent (for example Priya) | Takes over staff chats Mon to Sat, 9 am to 5 pm |
| Approvers (class teacher, Principal, transport manager, HR) | Decide the requests raised from WhatsApp, in their own app; the answer returns to the chat |
| Campus admin | Sees the "WhatsApp channel" settings card, toggles, usage tiles |
| Tenant admin / group office | Sets group defaults, owns the WhatsApp Business account, budget and templates (see Section TFC) |
| DhruvaOne support | Operates the provider connection; no access to message content except by tenant consent (see WAB-SEC-006) |
| Meta and the provider (BSP) | External parties whose rules and outages the product must handle |

## 8.3 Functional requirements

### 8.3.1 Official school account (number, profile, templates)

**WAB-ACC-001 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall give each tenant its own WhatsApp Business Account (WABA) with one or more registered sender numbers, each bound to a campus or to the whole group.
- Acceptance: Given a tenant completes channel setup When an admin opens "WhatsApp channel" Then it shows each number, the campuses it serves, and a status of "Live", "Setting up", "Limited" or "Paused".
- Rules: The tenant (school) owns the WABA as data fiduciary; DhruvaOne is the processor through a Meta-approved provider. Standalone schools have one number. A group may use one number per campus or one for the group; with a group number the campus is resolved from the matched profile (see 8.8, Q2).

**WAB-ACC-002 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall require the school's own number on the WhatsApp Business Platform through a Meta-approved provider, with verification, before the channel can go "Live".
- Acceptance: Given the checklist is incomplete When the admin tries to switch the channel on Then the card lists the missing steps and the channel stays "Setting up".
- Rules: Checklist: Meta business verification documents, WABA created, number registered (a number already used on the WhatsApp app must be released first), display name approved, two-step verification PIN set, profile completed, first templates approved, opt-in list loaded (Week 3 of campus onboarding). The green tick (official business account) is granted by Meta and cannot be guaranteed; the channel works without it, and the card shows "verified" only when Meta reports it.

**WAB-ACC-003 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall present the account as the verified school number: school logo, name (for example "DPS Gurugram"), tick, subtitle "Official school account".
- Acceptance: Given the profile is approved When a family opens the chat Then the header shows the school name, logo and "Official school account", and messages come only from this number.
- Rules: Meta's banner "This business uses a secure service from Meta to manage this chat. Tap to learn more." is shown by WhatsApp itself and cannot be changed.

**WAB-ACC-004 · Should · MVP · flag: ch.whatsapp · [Spec]**
The system shall manage the sender display name and business profile (about text, address, email, website, category, logo) from the admin card.
- Acceptance: Given the admin edits the display name When they save Then the change is sent to Meta for review, the old name stays live, and the card shows "Name under review" until approved or rejected with the reason.
- Rules: Display name rules are Meta's; a rejected name never replaces the live one.

**WAB-ACC-005 · Should · P2 · flag: ch.whatsapp · [Design]**
The system shall answer "About this chat" (keyword HELP or INFO, and the header "Business info" content) with the audience-specific trust lines.
- Acceptance: Given a registered parent types HELP When Dhruva replies Then the reply contains: "Messages come only from the verified DPS Gurugram number", "Works only for mobile numbers registered with the school", "Fees are paid by UPI. Dhruva never asks for your PIN or OTP", the office hours, and "Type STOP at any time to stop school alerts".
- Rules: Teacher and staff versions use the lines in the designs ("Teacher numbers are checked against school records", "Payslips open only with your 4-digit PIN", "Leave requests go to the Principal" or "Leave and advance requests go straight to your manager", "Works in English and हिंदी, by text or voice note"). School name and hours come from settings, not hard-coded. Also placed in the Meta profile description where it fits.

**WAB-ACC-006 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall sync the account's health (verification, display name status, quality rating, messaging limit tier) from the provider and show it on the admin card.
- Acceptance: Given Meta lowers the quality rating from High to Medium When the callback arrives Then the card shows the new rating within 5 minutes and the tenant admin is notified (see WAB-PLT-007).

### 8.3.2 WhatsApp Business Platform rules

**WAB-PLT-001 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall track a 24-hour customer-service window per contact and send free-form or interactive messages only while it is open.
- Acceptance: Given a contact's last inbound message was 25 hours ago When any module tries to send a non-template message Then the system sends nothing, and either sends an approved template or queues the item for the fallback channel (see WAB-FAL-002).
- Acceptance: Given a contact taps a template quick-reply button or sends any message When the system receives it Then the window reopens for 24 hours from that inbound time.
- Rules: Menus, lists, reply buttons, forms and documents are session messages. Alerts outside the window must be templates. The window is stored per contact per sender number and shown to agents as a countdown.

**WAB-PLT-002 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall manage message templates through their approval lifecycle (see state machine in the Annex).
- Acceptance: Given an admin submits a template When Meta approves it Then its status becomes "Approved" and it can be used; When Meta rejects it Then the status is "Rejected" with Meta's reason, and no event may send it.
- Rules: Only approved templates can be sent. Editing an approved template creates a new version that must be re-approved; the previous approved version stays in use until then. Meta's limits on edits and appeals are enforced as reported by the provider.

**WAB-PLT-003 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall validate template content before submission against Meta's formatting rules.
- Acceptance: Given a body has a variable at the very start, adjacent variables, or no sample values When the admin submits Then submission is blocked with the specific problem.
- Rules: Lower-case snake_case name; category chosen from Utility, Marketing (see WAB-OUT-002) or Authentication (not used by this section); language code per version (en, hi); body up to 1,024 characters; footer up to 60; at most 3 quick-reply buttons or 2 call-to-action buttons (the designs use one or two); button labels within Meta's limit (about 20 to 25 characters); numbered sample values for every variable. Limits are configuration and re-checked at build against current Meta values.

**WAB-PLT-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall record the delivery status of every outbound message (accepted, sent, delivered, read, failed) from provider callbacks.
- Acceptance: Given a message callback arrives out of order (read before delivered) When processed Then the message keeps the furthest state and no state moves backwards.
- Rules: "Read" is available only when the recipient has read receipts on; absence of "read" is never treated as "unread" for compliance. In-app read counts (for example "Read by 34 of 36") use app reads plus WhatsApp "read" where available and state which. Failed messages store Meta's error code and trigger WAB-FAL-005.

**WAB-PLT-005 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall enforce media limits on inbound and outbound files.
- Acceptance: Given a teacher sends a photo larger than the configured limit or in an unsupported type When received Then Dhruva replies "That file is too large or not supported. Please send a clear photo (JPG or PNG)." and nothing is read.
- Rules: Defaults (configuration, verify with provider): image up to 5 MB (JPG, PNG), audio up to 16 MB (OGG/Opus, AAC, MP3, AMR), documents up to 100 MB (PDF only sent by the system), video not read. Inbound media is downloaded immediately (provider media links expire in minutes) and stored in tenant storage. Outbound PDFs (receipts, date sheets, report cards, payslips, holiday list) follow the design name pattern, for example `Receipt_RC-30513_Transport.pdf`, `Payslip_Sep2026_<Name>.pdf`, and show page count and size.

**WAB-PLT-006 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall pace outbound sending so it stays inside provider throughput and Meta's per-recipient pacing, without losing messages.
- Acceptance: Given 3,000 attendance alerts are due at 7:45 am When sent Then all are queued, sent at no more than the configured rate per second per number, urgent items first, and oldest-first within a tier.
- Rules: Per-tenant and per-number token buckets; urgent bypasses the tenant bucket but not the provider limit; retries use exponential backoff and stop at the item's expiry (see WAB-OUT-004).

**WAB-PLT-007 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall watch the quality rating and messaging-limit tier and automatically protect the account.
- Acceptance: Given the rating drops to Low (red) When detected Then non-urgent templates are paused for that number, urgent and in-window replies continue, and the tenant admin is notified with the top-blocked templates.
- Rules: Daily unique-recipient volume is compared with the tier limit; at 80 percent, school-wide broadcasts (notices) are scheduled in batches; at 100 percent, new unique recipients wait for the next window. Users who tap "Block" or "Report" lower quality, so every template carries an STOP instruction (see WAB-OPT-002).

**WAB-PLT-008 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall use interactive message types within WhatsApp's limits.
- Acceptance: Given a menu has more than 3 choices When built Then it is sent as a list message (up to 10 rows, row title up to 24 characters, one "Send" action); When it has 1 to 3 choices Then reply buttons are used.
- Rules: The 8-row topic lists in the designs fit one list. Forms (leave, absentees, homework, PIN, advance) use WhatsApp Flows; if Flows are unavailable on the sender's app version, the same fields are collected one question at a time with reply buttons. A pay link is a call-to-action URL button.

### 8.3.3 Opt-in, opt-out and STOP

**WAB-OPT-001 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall send school alerts only to numbers with a recorded opt-in.
- Acceptance: Given a number has no opt-in When an alert event fires Then no WhatsApp template is sent and the fallback channel is used.
- Rules: Opt-in sources: admission form (families choose alerts at admission), parent onboarding in Week 3 ("app invite and WhatsApp opt-in"), staff HR record at joining, the user messaging first (opens the window for replies but is not opt-in for later alerts unless they tick it, see WAB-OPT-003). Each OptIn stores source, text shown, timestamp, recorder, tenant, number. Bulk import requires a declaration that consent was collected. A confirmation template (`optin_confirmation`) is sent once.

**WAB-OPT-002 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall stop all school-initiated WhatsApp messages to a number when the user types STOP.
- Acceptance: Given a user sends "STOP" (any case, with spaces) When processed Then within 5 seconds they get "You will no longer get school alerts on WhatsApp. Type START any time to turn them back on." and the OptIn becomes "opted out".
- Rules: Recognised words: STOP, UNSUBSCRIBE, CANCEL, END, QUIT, "बंद", "रुकें", "band", "stop alerts". Every alert template carries "reply STOP to opt out" in the footer. The opt-out is per number per tenant and applies to all profiles on that number at that school. Replies to the user's own requests inside an open window are still allowed (they are not alerts).

**WAB-OPT-003 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall let a user opt in again by typing START, and let parents and staff change alert categories.
- Acceptance: Given an opted-out user types START When processed Then the OptIn is recorded as a new row with source "user keyword" and they get `optin_confirmation`.
- Rules: Category choices (Attendance, Fees, Bus, School notices, Results) are held on the contact and editable from the menu item "Alert settings" (P2) and in the app; STOP overrides all.

**WAB-OPT-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall treat opt-out as binding even for safety alerts, and route those to another channel.
- Acceptance: Given a parent opted out of WhatsApp and a safety or early-pickup alert fires When delivered Then it goes by push and, for gate safety, SMS, and no WhatsApp message is sent.
- Rules: In the app, safety alerts cannot be turned off (see platform rules); on WhatsApp Meta policy requires STOP to be honoured, so the unavoidable channels are push and SMS.

**WAB-OPT-005 · Should · P2 · flag: ch.whatsapp · [Spec]**
The system shall handle "wrong number" and reassigned numbers.
- Acceptance: Given a user replies "wrong number" (or "WRONG NUMBER", "yeh galat number hai") When processed Then the number is marked "Disputed", all outbound and bot data stop, the office is notified, and the user gets "Thank you. We will correct our records."
- Rules: Three consecutive "undeliverable" results on a number also queue a data-quality task for the office to confirm the number. Only the office clears a Disputed flag.

### 8.3.4 Identity matching

**WAB-IDN-001 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall match the sender's WhatsApp number to school records without any password.
- Acceptance: Given a message arrives from +91 98xxxxxx21 When processed Then the number is normalised to E.164, looked up against guardian numbers on student records, teacher and staff records of the tenant, and the matching profiles are loaded.
- Rules: Matching uses the WhatsApp ID supplied by the provider, not any number typed in the message. Matching is within the tenant that owns the receiving sender number (and campus, if the number is campus-bound). Profile model is in Section 3 Identity. Only active records match; a leaver or deactivated guardian does not.

**WAB-IDN-002 · Must · P2 · flag: ch.whatsapp.parent_bot · [Design]**
A parent's number shall give access only to the children linked to that number.
- Acceptance: Given Pooja's number is linked to Vivaan (5-B) When she says "Hi" Then Dhruva greets "Namaste Pooja. I'm Dhruva, the DPS Gurugram assistant. What would you like to know about Vivaan (Class 5-B)?" with the button "Choose a topic".
- Rules: Links are the guardian numbers on the student record created by the school office. A parent never sees another child's marks or data.

**WAB-IDN-003 · Must · P2 · flag: ch.whatsapp.staff_bot · [Design]**
A teacher or staff number shall be matched to the school or HR record and greeted by name.
- Acceptance: Given Ms. Batra's number is on her staff record When she says "Hi" Then Dhruva replies "Namaste Shalini ji. I'm Dhruva, the DPS Gurugram assistant." and lists teacher topics; for Suresh the staff assistant greeting is used, with a language choice (see WAB-STF-001).
- Rules: Role decides the menu. A staff member whose status is not Active (exited, suspended) is treated as unknown.

**WAB-IDN-004 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall reply politely to unknown numbers and share nothing.
- Acceptance: Given a number is on no record When it sends any text Then it gets once per 24 hours: "This number is not registered with the school. Please contact the DPS Gurugram office to add it, then try again." with no menu, and the event is logged.
- Rules: The Overview says unknown numbers get "a polite reply asking them to contact the school office"; wording adapts the website sign-in message. No further replies to repeated messages within 24 hours (anti-abuse). If the "Admissions enquiries" toggle is on, the unknown-number reply adds the choice "Admission enquiry" (see WAB-PAR-011).

**WAB-IDN-005 · Must · P2 · flag: ch.whatsapp.parent_bot · [Spec]**
The system shall handle a number linked to several children (including a number shared by several families).
- Acceptance: Given a number is linked to Vivaan (5-B) and Aarav (9-A) When the parent picks "Today's attendance" Then Dhruva asks "Which child?" with up to 3 reply buttons (or a list for more) plus "Both" for summary topics (attendance, fees, homework, calendar).
- Acceptance: Given the parent picks a child When they pick another topic within 30 minutes Then the same child is used, and the answer header names the child.
- Rules: Multi-child parents are roadmap Phase 1. Child names shown to a number are limited to first name and class. If a number is linked to unrelated families (for example a shared family phone) the same prompt appears; the school office can mark a link "Restricted" to require confirmation by app instead.

**WAB-IDN-006 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall ask which profile is meant when one number holds several profiles, and never mix them.
- Acceptance: Given a number is both a parent and a teacher at this school When it says "Hi" Then Dhruva asks "Which do you mean?" with buttons "Parent" and "Teacher"; the answer is remembered for 30 minutes and "switch" changes it.
- Acceptance: Given a number is linked to 3 schools served by one shared account When it messages Then Dhruva asks "This number is linked to 3 schools. Which one do you mean?" and says "I will remember this school for the next 30 minutes. Type 'switch' to change."
- Rules: Opening a staff profile on a number that also holds a parent profile requires the 4-digit PIN first (staff profiles are locked in the apps for the same reason). Menus, data and colours of profiles never mix in one answer.

**WAB-IDN-007 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall revoke chat access immediately when a number is removed from the record.
- Acceptance: Given the office replaces a guardian number When saved Then the old number is treated as unknown within 1 minute, its open conversation is closed, and its PIN session ends.

### 8.3.5 Conversation engine and menus

**WAB-MNU-001 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall provide a baseline inbox in MVP: replies from registered numbers to alerts are routed to the office inbox and acknowledged.
- Acceptance: Given a parent replies "Please call me" to an alert When received Then the office inbox shows it with the sender's matched child and class, and the parent gets once "Thank you. The school office will reply in working hours." out of hours, or no auto-reply in hours.
- Rules: STOP, START and HELP are handled by the system in MVP; the menu bot arrives in P2.

**WAB-MNU-002 · Must · P2 · flag: ch.whatsapp.parent_bot · [Design]**
The system shall open the parent conversation with the greeting, the "Choose a topic" button and the 8-row topic list.
- Acceptance: Given a registered parent says "Hi" or "Hello", "Hey", "Namaste", "Start", "Menu" When processed Then Dhruva shows the menu text with footer "You can also just type your question" and the list button "Choose a topic".
- Acceptance: Given the list opens Then its title is "What do you need?", the rows are: "Today's attendance", "Fees and receipts", "Homework", "Where is the bus?", "Exams and results", "Apply for leave", "School calendar", "Talk to the school office" (each with its subtitle), and "Send" is disabled until one row is picked.
- Rules: After every answer a "Main menu" button returns to the list with "What else can I help you with?". A disabled topic (flag off) is removed from the list, not greyed. Rows of a module whose flag is off are hidden (for example "Where is the bus?" when mod.bus_live is off).

**WAB-MNU-003 · Must · P2 · flag: ch.whatsapp.teacher_bot · [Design]**
The system shall open the teacher conversation with the day's status and the 8-row teacher list.
- Acceptance: Given Ms. Batra says "Hi" and 5-B attendance is not marked When she gets the reply Then it says "Today's attendance for 5-B is not marked yet. You can type, or just send me a photo of your register." with "Choose a topic"; the rows are "Mark attendance", "Send a photo", "My timetable", "Post homework", "Who needs help?", "Apply for leave", "My payslip", "Talk to the office".
- Rules: If attendance is already marked the status line is omitted.

**WAB-MNU-004 · Must · P2 · flag: ch.whatsapp.staff_bot · [Design]**
The system shall open the staff conversation with a language choice, then the "Staff services" list.
- Acceptance: Given Suresh says "Namaste" When processed Then Dhruva asks to choose a language with buttons "हिंदी" and "English", then shows "How can I help you today, Suresh ji?" with footer "You can also type or send a voice note" and the list button "Open menu".
- Rules: Eight rows are listed in WAB-STF-002.

**WAB-MNU-005 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall echo each tapped choice as the user's own message and reply with a short typing delay.
- Acceptance: Given a user picks a list row and taps Send When processed Then the row title appears as their message, a typing indicator shows, and the answer follows in under 5 seconds at the 95th percentile (the prototype shows about 0.7 to 0.9 seconds).
- Rules: Typing indicator is shown by marking the inbound message read with the typing indicator where the provider supports it; otherwise omitted. The prototype's restart control and toasts are demo aids and are not built.

**WAB-MNU-006 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall define what each composer control does per audience.
- Acceptance: Given a parent or staff member sends a photo or document When received Then Dhruva replies "Attachments go to the school office" and passes it to the office inbox (HR inbox for staff), with the sender, child or employee, and time.
- Acceptance: Given a teacher sends a photo Then the photo flow runs (see WAB-TCH-002).
- Acceptance: Given a user starts a WhatsApp voice or video call to the school number When rejected or unanswered Then Dhruva sends "Calls go to the school office during working hours" with the office phone number.
- Rules: Typed text, taps, list picks, form submissions, photos (teachers), voice notes (staff first, see WAB-VOI-001) are the accepted inputs. Emoji and stickers are accepted as text and ignored for intent. The hint bubble ("Try it: ...") has no equivalent; a one-time tip is added to the first menu message.

**WAB-MNU-007 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall time out open forms and sub-flows and recover from stale taps.
- Acceptance: Given a user opens the leave form and does nothing for 30 minutes When they tap an old button Then Dhruva replies "That step has expired. Let us start again." with "Main menu", and no record is changed.
- Rules: Flow sessions expire after 30 minutes; stale button IDs carry a conversation step token; every record-changing action is idempotent on the provider message ID.

### 8.3.6 Parent flows

**WAB-PAR-001 · Must · P2 · flag: ch.whatsapp.parent_bot · [Design]**
A parent can see today's attendance and the term percentage for the child.
- Acceptance: Given Vivaan is present Then the reply is "Vivaan was marked Present today at 7:48 am. This term: 96% attendance (2 days absent)." with buttons "Apply for leave" and "Main menu".
- Rules: Data from mod.attendance. If not yet marked: "Attendance for Vivaan is not marked yet today." If absent: "Vivaan was marked Absent today." with "Apply for leave" kept as a button so the parent can explain.

**WAB-PAR-002 · Must · P2 · flag: mod.fees · [Design]**
A parent can see what is due and what is paid for the child.
- Acceptance: Given a transport fee is unpaid Then the reply header is "Fees for Vivaan" with "Transport fee (Oct to Dec): Rs 9,600, due 10 Oct" and "Tuition fee: paid till December", a button "Pay Rs 9,600 by UPI", then a second message "Need a receipt for an earlier payment?" with "Last receipt" and "Main menu".
- Acceptance: Given everything is paid Then "All fees are paid." lists each head with its paid-till month and buttons "Latest receipt" and "Main menu".
- Rules: Amounts come from the fee ledger for the matched child only. Fee amounts are shown only to numbers that are fee payers on the record (see WAB-SEC-001).

**WAB-PAR-003 · Must · P2 · flag: ch.whatsapp.upi_pay · [Design]**
A parent can pay the outstanding fee by UPI from the chat, and the money goes straight to the school account.
- Acceptance: Given the parent taps "Pay Rs 9,600 by UPI" Then the sheet "Pay DPS Gurugram" shows "Transport fee · Oct to Dec · Bus 12", the amount, "Pay with any UPI app. Money goes straight to DPS Gurugram. Order RC-30513", app rows Google Pay, PhonePe, Paytm, BHIM UPI, and footer "Secured by UPI · NPCI".
- Acceptance: Given the gateway confirms the payment Then the user gets "Payment received" with "Rs 9,600 for transport (Oct to Dec). Thank you, Pooja! Your receipt is below." and the PDF `Receipt_RC-30513_Transport.pdf` plus "Main menu".
- Rules: The order is created from the fee ledger (the amount cannot be typed or edited by the user); links and orders expire after 30 minutes; success is decided only by the gateway's server callback, never by the user saying "paid". Dhruva never asks for UPI PIN or OTP. Implementation uses the in-chat payment message supported for India where the sender account is eligible, else a call-to-action link to the hosted gateway page with the same order (see 8.8, Q4). Pending, failed and duplicate payments are in WAB-FAL-008.

**WAB-PAR-004 · Must · P2 · flag: mod.fees · [Design]**
A parent can receive receipts as PDF.
- Acceptance: Given an earlier payment exists When the parent taps "Last receipt" Then Dhruva sends `Receipt_RC-29877_Tuition_Jul-Sep.pdf` (1 page, size shown) with "Tuition fee, Jul to Sep · paid 2 Jul"; after a payment the button reads "Latest receipt".
- Rules: Receipts are the same documents the app issues; a receipt older than the retention shown in the fee module is refused with "Please ask the school office for this receipt" and "Talk to the school office".

**WAB-PAR-005 · Must · P2 · flag: mod.homework · [Design]**
A parent can see this week's homework and a tip to help.
- Acceptance: Given homework exists Then "Homework this week" lists subject, task, due, and "Set by Ms. Shalini Batra", with buttons "How can I help him?" and "Main menu".
- Acceptance: Given the parent taps "How can I help him?" Then Dhruva replies with a short tip drawn from the child's recent results (for example times tables for Maths).
- Rules: The tip is a draft by Dhruva (ai.reply_drafts off => button hidden); it never names other children. For a child of Class 6 and above, homework goes to the student app too (see platform rule: no marketing, students from Class 6 get homework and results only).

**WAB-PAR-006 · Must · P2 · flag: mod.bus_live · [Design]**
A parent can see where the child's bus is and ask to be alerted 5 minutes before the stop.
- Acceptance: Given Bus 12 has a recent stop tap When the parent picks "Where is the bus?" Then a location card "Bus 12 · live location, Near Sector 29 · updated 1 min ago" with a "LIVE" badge is followed by "Bus 12 will reach DLF Phase 4, Galleria at about 2:22 pm (12 min). Driver: Suresh Yadav · Attendant: Kamla Devi" and buttons "Alert me 5 min before", "Main menu".
- Acceptance: Given the parent taps "Alert me 5 min before" Then "Done. I'll message you when Bus 12 is 5 minutes away." and at that moment the template `bus_five_min` is sent, even outside quiet hours.
- Rules: In the MVP position comes from the attendant's stop taps, not GPS (see Section on Transport); the card says "updated N min ago" with the age of the last tap; if older than 20 minutes it says "Position not updated recently" and offers "Talk to the school office". A static location pin is sent (WhatsApp live location sharing is not available to a business); the "LIVE" badge is a text label. The alert is per child per day and not repeated.

**WAB-PAR-007 · Must · P2 · flag: mod.exams · [Design]**
A parent can see the exam date sheet, the latest result and the report card.
- Acceptance: Given Term 1 is scheduled Then the reply header is "Term 1 assessments" with "Start Mon 19 Oct · 4 subjects", "Latest result, Unit test 2: English A1, Maths B1", the PDF `Term1_Datesheet_Class5B.pdf` (2 pages), and buttons "Send report card", "Main menu".
- Acceptance: Given the parent taps "Send report card" Then Dhruva sends `ReportCard_UT2_Vivaan_Sharma.pdf` with "Unit test 2 report card with teacher remarks".
- Rules: Only published results (see mod.marks_results, mod.report_cards); results held by the exam cell are not shown. A parent sees only their own child's marks. Fee-hold on report cards, if the school uses it, applies the same way as in the app.

**WAB-PAR-008 · Should · P2 · flag: mod.calendar_ptm · [Design]**
A parent can see the school calendar and ask for a PTM reminder.
- Acceptance: Given events exist Then "Coming up" lists the next dated items (for example "Fri 9 Oct: Sports Day heats, wear house colours"), with buttons "Remind me about the PTM", "Main menu".
- Acceptance: Given the parent taps "Remind me about the PTM" Then Dhruva says "Done. I'll remind you on Fri 30 Oct with Vivaan's teachers and time slot." and sends `ptm_reminder` on the day before.

**WAB-PAR-009 · Must · P2 · flag: mod.attendance · [Design]**
A parent can apply for leave for the child through guided steps, and the class teacher approves in her app.
- Acceptance: Given the parent picks "Apply for leave" Then "Sure. Which day will Vivaan miss school?" with buttons "Tomorrow, 7 Oct", "Fri, 9 Oct", "Other dates".
- Acceptance: Given "Other dates" Then the form "Leave for Vivaan" shows From and To date chips and "Continue"; with one missing it says "Please choose both dates."
- Acceptance: Given the dates are set Then "And the reason?" with "Unwell", "Family function", "Other"; then "Leave request sent to Ms. Shalini Batra (class teacher) for <day>. I'll tell you here when she replies."
- Acceptance: Given the teacher approves in her app Then `leave_decision` arrives: "Leave approved: Ms. Shalini Batra approved Vivaan's leave for <day>." (with "Get well soon, Vivaan!" for Unwell) and the footer "Homework for the day will be shared here".
- Rules: The date chips are generated from school working days (the prototype's dates are sample). Past dates and non-working days are refused with "That day is not a school day." A declined leave sends the teacher's reason. The leave is only a request until approved (see Section on Attendance for status "Leave approved"). Other: free text up to 200 characters is stored as the reason.

**WAB-PAR-010 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
A parent can ask for a person ("Talk to the school office") (see WAB-HND-001).
- Acceptance: Given the parent picks the row Then the handover starts as defined in 8.3.9.

**WAB-PAR-011 · Could · P3 · flag: ch.whatsapp.admissions · [Design]**
A new family can ask about seats and fees through the "Admissions enquiries" setting.
- Acceptance: Given the toggle is on and an unknown number types "admission" When processed Then Dhruva collects child name, class sought and parent name and creates an enquiry in Admissions CRM, with a reply "Thank you. The admissions team will call you."
- Rules: The designs show the toggle only and no flow; the flow here is the minimum viable. Consent for contact is taken in the first message. Not a scoring or decision tool.

### 8.3.7 Teacher flows

**WAB-TCH-001 · Must · P2 · flag: ch.whatsapp.teacher_bot · [Design]**
A teacher can mark class attendance by naming the absentees; everyone else is marked present.
- Acceptance: Given Ms. Batra picks "Mark attendance" Then Dhruva says "Class 5-B · 36 students. Tell me who is absent. Everyone else is marked present." with the flow button "Mark absentees".
- Acceptance: Given the form "Absent today · 5-B" opens Then it asks "Absent student" with the roster and a "Nobody is absent" choice and submit "Submit attendance"; with nothing chosen it says "Please choose an option."
- Acceptance: Given she submits Kabir Arora Then "Attendance submitted: 35 present, 1 absent in 5-B. Parents of Kabir Arora have been messaged." with footer "Saved in Dhruva One" and "Main menu"; with "Nobody is absent": "36 of 36 present in 5-B."
- Acceptance: Given attendance is already marked Then "Already done today. 35 present, 1 absent (Kabir Arora)."
- Rules: Only the class teacher of the section (or the teacher on the period, or a teacher the coordinator delegated) may mark; others get "This class is not assigned to you." The roster has 36 names, so the form uses a searchable single-choice list and an "Add another absentee" repeat (the design says "You can send this again to add more"); a text option "Roll numbers, for example 3, 17" is also accepted. Parent alerts go through WAB-OUT-008, with the timing in WAB-TCH-003. Writes the same attendance record as the app (mod.attendance), with channel "whatsapp" in audit. Repeat absence is flagged to the coordinator as in the app.

**WAB-TCH-002 · Must · P2 · flag: ch.whatsapp.photo_upload · [Design]**
A teacher can send a photo of an attendance register, marks sheet or notebook page, and Dhruva reads it and publishes it.
- Acceptance: Given she picks "Send a photo" Then Dhruva says "Send a photo from your gallery: an attendance register, a marks sheet or your notes and learning plan. I read it and publish it for you. No typing needed." with "Open gallery"; the paperclip and camera do the same.
- Acceptance: Given she sends a photo Then Dhruva first states what it recognised ("Got it. This looks like an attendance register for 5-B. Reading it…") and, in about 3 seconds, the result with footer "Read from your photo · saved in Dhruva One" and buttons "Undo", "Main menu".
- Acceptance: Given the photo has no register, marks or notes Then "I couldn't find an attendance register, marks sheet or notes in this photo. Could you send a clear photo of the page?" with "Choose another photo", "Main menu".
- Rules: Needs ai.marks_from_photo. With the AI flag off, the "Send a photo" row says "Photo reading is switched off for your school. Use Mark attendance or the app." The sender's profile decides which class and subject she may publish for (see WAB-SEC-008). See WAB-TCH-003 to -005 for the three document types.

**WAB-TCH-003 · Must · P2 · flag: ch.whatsapp.photo_upload · [Design]**
Dhruva shall publish an attendance register read from a photo, with Undo and a safeguard against misreads.
- Acceptance: Given the photo is recognised as the 5-B register and every name is matched Then Dhruva publishes "Attendance published: 5-B · today / 35 present, 1 absent (Kabir Arora) / Kabir's parents have been messaged." with "Undo".
- Acceptance: Given "Undo" is tapped Then "Done, I've taken that back. Parents can no longer see it. You can send a clearer photo any time." with "Send another photo", and "attendance done today" resets.
- Rules: [Spec] additions: (a) if any mark is unreadable, a name does not match the roster, or confidence is below the configured threshold, Dhruva shows what it read and asks "Is this right?" with "Yes, publish" / "Fix it" before publishing; (b) absentee alerts to parents are held for the "undo window" (default 2 minutes) so that Undo can stop them; (c) Undo is available for 30 minutes and withdraws parent alerts not yet sent and marks sent ones "corrected" with a correcting message "Correction: Kabir was marked present." The design publishes with Undo only; whether to add the confirm step for all photos is open (8.8, Q5).

**WAB-TCH-004 · Must · P2 · flag: ch.whatsapp.photo_upload · [Design]**
Dhruva shall publish marks read from a marks-sheet photo.
- Acceptance: Given a marks sheet is recognised Then "Marks published: Maths · Unit test 2 · 5-B / 36 students read, out of 25 / Class average 18.4, highest 24. / Each parent sees only their own child's marks."
- Rules: Dhruva checks the same errors as the app: marks above the maximum, blanks, duplicate roll numbers; any issue shows a "Please check" list before publishing. Publication to parents follows the tenant setting "Share with parents: now or after HoD check" (see Section on Marks); under "after HoD check" the reply says "Sent to the HoD for checking." The design publishes at once; the project's open decision on review is Q5.

**WAB-TCH-005 · Should · P2 · flag: ch.whatsapp.photo_upload · [Design]**
Dhruva shall publish a learning plan read from a notebook-page photo.
- Acceptance: Given a notebook page is recognised Then "Learning plan published: Maths · week of 12 Oct · 5-B" with Mon/Wed/Fri lines and "Students and parents can see it in the app and on WhatsApp."
- Rules: Routed to the lesson-plan flow (mod.lesson_plans): where a HoD review step exists it applies and the reply says "Sent to Dr. Desai for review" (see Section on Academics).

**WAB-TCH-006 · Must · P2 · flag: mod.timetable · [Design]**
A teacher can see today's periods, including cover, and decline a cover.
- Acceptance: Given the teacher picks "My timetable" Then a header with the date ("Friday 9 Oct") lists periods ("1 · 7-C Maths", "4 · Cover: 6-D for Mr. Sandeep Bedi (set by Dhruva)") and buttons "Can't take the cover?", "Main menu".
- Acceptance: Given she taps "Can't take the cover?" Then "Okay. I've asked Dhruva to find another free teacher for 6-D, Period 4. I'll confirm here."
- Rules: Decline raises a new cover search for the coordinator (mod.cover, ai.cover_suggestions). Without the AI flag the coordinator gets a manual task. A confirmation message follows when a replacement is set.

**WAB-TCH-007 · Must · P2 · flag: mod.homework · [Design]**
A teacher can post homework to every parent of the class.
- Acceptance: Given she picks "Post homework" Then the form "Post homework · 5-B" shows Subject (Maths, English, Hindi, Science), Task (free text, placeholder "Worksheet 5, Q1 to 10"), Due (Tomorrow, Mon 12 Oct, Wed 14 Oct) and "Send to parents"; with a field empty it says "Please fill all three."
- Acceptance: Given she submits Then "Sent to the parents of 5-B (36 families). <Subject>: <task>, due <due>."
- Rules: Subject chips come from the teacher's assigned subjects and sections. Due chips are the next working days. Parents get it on WhatsApp via `homework_posted` (opted-in) and in the app. The post is the teacher's own act; a school that requires moderation of homework routes it for approval first (see mod.approvals).

**WAB-TCH-008 · Should · P2 · flag: mod.homework · [Design]**
A teacher can see how many parents read the homework and remind the rest.
- Acceptance: Given about 5 minutes after posting Then `homework_delivery_summary` arrives: "Read by 34 of 36: Your <Subject> homework has been read by 34 parents. 2 have not opened it yet." with "Remind the 2", "Main menu".
- Acceptance: Given she taps "Remind the 2" Then "Done. I've sent a gentle reminder to the 2 parents." and one reminder only is sent per post.
- Rules: Counts mix app opens and WhatsApp reads and show "n have WhatsApp read receipts off" in the detail. The summary arrives within the 24-hour window, so it is a free-form message when she has chatted that day, otherwise the template.

**WAB-TCH-009 · Should · P2 · flag: ai.at_risk_detection · [Design]**
A teacher can see Dhruva's notes on her class and send a drafted note to a parent.
- Acceptance: Given she picks "Who needs help?" Then "Dhruva's notes · 5-B" lists up to 5 students with the reason (for example "Kabir Arora: absent 3 of the last 5 days") with footer "Based on attendance and marks in Dhruva One" and "Message Kabir's parents", "Main menu".
- Acceptance: Given she taps "Message Kabir's parents" Then Dhruva shows the draft "Dear Mr. Arora, Kabir has missed 3 of the last 5 days. Is everything okay? Please tell us if we can help. – Ms. Batra, 5-B" with "Send it" and "Cancel"; only "Send it" delivers it.
- Acceptance: Given the parent replies Then the reply is relayed to the teacher: "Mr. Arora (parent): <text>".
- Rules: The draft is Dhruva's suggestion; a person approves by tapping "Send it" (see ai.reply_drafts). Notes never name students outside her sections. Sent as a template if the parent's window is closed. Without the AI flag, "Who needs help?" shows the attendance and marks lists without wording.

**WAB-TCH-010 · Must · P2 · flag: mod.hr_leave · [Design]**
A teacher can see her leave balance and apply for leave, which goes to the Principal.
- Acceptance: Given she picks "Apply for leave" Then "Your leave balance: Casual 7 · Sick 5 · Earned 12 days. Which day do you need leave?" with day buttons, then "And the reason?" with "Unwell", "Personal", "Training".
- Acceptance: Given she completes it Then "Leave request for <day> sent to Ms. Neelam Mehra (Principal). I'll tell you here when it is approved."; on approval `leave_decision` says "Ms. Neelam Mehra (Principal) approved your leave for <day>. Dhruva arranged cover for 5-B Maths: Mr. Sandeep Bedi." with footer "Your class has been informed".
- Rules: The approver follows the school's chain (HoD for up to 2 days outside exam weeks, else Principal; see Section on HR); the designed text names the Principal. The request is created in the same leave table as the app. Longer ranges than the two day chips use "Other dates".

**WAB-TCH-011 · Must · P2 · flag: ch.whatsapp.payslip · [Design]**
A teacher can open her payslip on WhatsApp only after entering her 4-digit PIN.
- Acceptance: Given no PIN session exists Then "Your payslip is protected. Please enter your 4-digit PIN to open it." with "Enter PIN"; the sheet "Enter your PIN" says "Dhruva never asks for this PIN anywhere else.", field "4-digit PIN" (masked), submit "Open payslip", error "Please enter 4 digits."
- Acceptance: Given the PIN is correct Then `Payslip_Sep2026_Shalini_Batra.pdf` with "September 2026 / Gross Rs 58,000 · Deductions Rs 7,420 / Net pay Rs 50,580, credited on 1 Oct to HDFC ••2290" and buttons "Previous month", "Main menu".
- Rules: PIN policy is WAB-SEC-002 (the prototype accepts any 4 digits; the product verifies). The PIN session is remembered only for 15 minutes of inactivity. Bank account is masked.

**WAB-TCH-012 · Could · P3 · flag: mod.notices · [Design]**
A teacher can see which parents have read a notice and remind the rest, and see class attendance for the month.
- Acceptance: Given the Overview lists these as capabilities When built Then they follow the homework read-count pattern (WAB-TCH-008) and the attendance summary pattern (WAB-PAR-001).
- Rules: The designs list them without a flow; marked P3.

**WAB-TCH-013 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
A teacher can ask for the office ("Talk to the office") (see WAB-HND-001).

### 8.3.8 Staff flows

**WAB-STF-001 · Must · P2 · flag: ch.whatsapp.staff_bot · [Design]**
Staff can choose Hindi or English; the choice sets the whole interface (text, list titles, button labels, form labels, validation messages).
- Acceptance: Given Suresh taps "हिंदी" Then the greeting "सुरेश जी, आज मैं आपकी क्या मदद करूँ?", the button "मेनू खोलें" and the list title "स्टाफ़ सेवाएँ" appear; typing "English" later switches back.
- Rules: Stored on the staff contact and used for templates (WAB-OUT-006). A first-time staff member sees the bilingual prompt "Please choose your language. कृपया अपनी भाषा चुनें।" All strings exist in both languages; none falls back to English silently (missing Hindi string is a build error).

**WAB-STF-002 · Must · P2 · flag: ch.whatsapp.staff_bot · [Design]**
The staff menu shall list eight services, in English and Hindi.
- Acceptance: Given the list opens Then rows are: "Payslip" (वेतन पर्ची), "Leave balance" (बची हुई छुट्टियाँ), "Apply for leave" (छुट्टी के लिए आवेदन), "My attendance" (मेरी हाज़िरी), "Today's duty" (आज की ड्यूटी), "Holiday list" (छुट्टियों की सूची), "Salary advance" (वेतन अग्रिम), "Talk to HR" (HR से बात करें).
- Rules: "Today's duty" shows only for staff with a route, post or shift assignment (drivers, attendants, guards, housekeeping); for others it is hidden. Rows follow the module flags.

**WAB-STF-003 · Must · P2 · flag: ch.whatsapp.payslip · [Design]**
Staff can open the payslip behind the 4-digit PIN they set with HR.
- Acceptance: Given the staff taps "Payslip" Then "For your safety, payslips are protected with your 4-digit PIN." with "Enter PIN" ("PIN डालें"); the sheet "Open your payslip" says "Enter the 4-digit PIN you set with HR. Don't share it with anyone."; error "Please enter 4 digits."
- Acceptance: Given the PIN is correct Then `Payslip_Sep2026_Suresh_Yadav.pdf` with "Gross Rs 24,000 · Deductions Rs 2,550 / Net pay Rs 21,450, credited on 1 Oct to SBI ••4821" and "Previous month" (`Payslip_Aug2026_Suresh_Yadav.pdf`), "Main menu".
- Rules: See WAB-SEC-002. A staff member with no PIN set gets "Please ask HR to set your PIN" and "Talk to HR".

**WAB-STF-004 · Must · P2 · flag: mod.hr_leave · [Design]**
Staff can see leave balances and apply for leave through a short form sent to the manager.
- Acceptance: Given "Leave balance" Then "Casual: 4 days / Sick: 6 days / Earned: 9 days" with "Apply for leave", "Main menu".
- Acceptance: Given "Apply for leave" Then "Fill in the short form and I'll send it to Vinod Kumar (transport manager)." with "Fill leave form"; the form "Apply for leave" asks "Type of leave" (Casual, Sick, Earned), From, To, submit "Send to manager"; error "Please choose the type and both dates."
- Acceptance: Given it is sent Then "Leave request for <dates> sent to Vinod Kumar. A relief driver will be arranged for Bus 12."; on approval `leave_decision`: "Vinod Kumar approved your leave for <dates>. Rakesh will drive Bus 12."
- Rules: The approver and the relief line depend on the role (relief wording only for drivers and attendants). Balance is checked before sending: over-balance leave is sent with "This is more than your balance. HR will check." as in the app's comp-off or unpaid handling.

**WAB-STF-005 · Should · P2 · flag: mod.attendance · [Design]**
Staff can see their attendance for the month and today's check-in.
- Acceptance: Given "My attendance" Then "September: present 25 of 26 days / Today: checked in at 6:12 am, Gate 2".
- Rules: Data from staff attendance (see Section on HR). If no check-in yet: "Today: not checked in yet."

**WAB-STF-006 · Must · P2 · flag: mod.transport · [Design]**
Staff on duty can see today's duty.
- Acceptance: Given Suresh picks "Today's duty" Then a route card "Route 12 · 14 stops, Starts Sector 45 depot · ends DLF Phase 4" and text "Route 12 · Bus HR-26-AB-1212 / Morning pickup: 6:30 am · 38 students / Afternoon drop: 1:40 pm / Attendant: Kamla Devi" with "Report a problem", "Main menu".
- Rules: For guards and housekeeping the card shows post, shift, and gate or area. Hidden when no duty is assigned.

**WAB-STF-007 · Must · P2 · flag: mod.transport · [Design]**
Staff on a route can report a problem and the transport desk is alerted.
- Acceptance: Given "Report a problem" Then "What happened?" with "Bus breakdown", "Running late", "Student issue"; any choice replies "Transport desk alerted. Vinod Kumar will call you in 2 minutes. Parents on Route 12 will be informed if needed."
- Rules: [Spec] The three options are separate reasons: each creates a transport desk job with its type; breakdown starts the breakdown checklist; running late asks "How many minutes?" (5, 10, 15+) and, if over 10, a parent alert is drafted for the transport in-charge to approve, never sent by Dhruva alone. "Student issue" asks "Which student?" or free text. The 2-minute call promise is configurable (default 5) and the desk sees a countdown.

**WAB-STF-008 · Should · P2 · flag: mod.hr_leave · [Design]**
Staff can see the holiday list.
- Acceptance: Given "Holiday list" Then "Next holiday: Diwali break, 20 to 24 Oct" and the PDF `Holiday_List_2026-27_DPS_Gurugram.pdf` (1 page).

**WAB-STF-009 · Should · P2 · flag: mod.payroll · [Design]**
Staff can request a salary advance up to Rs 10,000, to be recovered from the next salary.
- Acceptance: Given "Salary advance" Then "You can request up to Rs 10,000. It is recovered from your next salary." with "Request advance"; the form "Salary advance" asks "Amount (Rs)" (placeholder 5000) and "Reason" (Medical, Family, Education, Other), submit "Send request"; error "Enter an amount up to Rs 10,000 and choose a reason."
- Acceptance: Given it is sent Then "Advance request for Rs <amount> sent to HR. You'll get an answer here within 2 working days."
- Rules: [Spec] The limit and the 2-day promise are tenant settings. One open request per person; a second one gets "You already have an advance request open." HR decides in the payroll module (the designs show no approval screen); the decision returns as a template and, if approved, becomes a recovery line in the next payroll run. Needs approval trail in mod.approvals.

**WAB-STF-010 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
Staff can ask HR ("Talk to HR", Mon to Sat, 9 am to 5 pm) (see WAB-HND-001).

### 8.3.9 Free-text understanding and fallback

**WAB-NLU-001 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall map typed text to topics with ordered keyword rules that work without any AI.
- Acceptance: Given a parent types "where is the bus?" Then the bus flow runs; given "fee receipt" Then fees runs; the first matching rule in the order below wins.
- Rules: Greetings (menu, hi, hello, hey, namaste, start, मेनू, नमस्ते) show the menu in every audience.

| Audience | Keyword order (first match wins) |
|---|---|
| Parent | bus, where, van, driver -> bus; fee, pay, receipt, due, money -> fees; attend, present, "absent today" -> attendance; homework, hw, assignment, worksheet -> homework; exam, result, marks, report, test -> exams; leave, absent, sick, "holiday for" -> leave; ptm, calendar, holiday, event, diwali, sports -> calendar; office, call, talk, teacher, complain -> office |
| Teacher | photo, picture, upload, gallery, marks, "learning plan", "lesson plan", notes -> photo; attend, present, absent -> attendance; timetable, period, schedule, cover -> timetable; homework, hw, worksheet -> homework; help, struggle, flag, who, weak -> who needs help; leave, sick, off, balance -> leave; payslip, salary, "pay stub", वेतन -> payslip; office, call, talk -> office |
| Staff | payslip, "salary slip", slip, वेतन, पर्ची, तनख्वाह, सैलरी -> payslip; balance, बची -> leave balance; leave, chhutti, छुट्टी -> apply leave; attendance, हाज़िरी -> attendance; duty, route, ड्यूटी, रूट -> duty; holiday, अवकाश -> holidays; advance, अग्रिम, loan -> advance; hr, talk, बात -> HR |

**WAB-NLU-002 · Should · P2 · flag: ai.whatsapp_bot · [Spec]**
The system shall use an intent classifier as a second step when keywords do not match, and confirm before acting on a low-confidence guess.
- Acceptance: Given a parent types "Vivaan ka result kab aayega" and no keyword matches When classified with confidence at or above the threshold Then the exams flow runs; between the low and high thresholds Then Dhruva asks "Do you mean exams and results?" with "Yes" and "No, show menu"; below the low threshold the fallback runs.
- Rules: The classifier only chooses a topic from the audience's allowed list; it does not write answers or invent data. Answers are always built from live records by the same flows. Text with a record-changing intent (leave, advance, attendance) always goes into the guided flow and is never executed from the sentence alone. With ai.whatsapp_bot off, only WAB-NLU-001 and the fallback apply.

**WAB-NLU-003 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall offer the office when it cannot answer.
- Acceptance: Given text matches nothing Then "I don't have an answer for that yet. Shall I ask the school office for you?" with buttons "Ask the office" and "Main menu" (staff: "Sorry, I didn't understand that. You can open the menu or send a voice note." with "Main menu", plus "Ask HR").
- Rules: After 2 consecutive unmatched messages Dhruva offers the office again without repeating the same sentence. Every unmatched text is logged (anonymised after 90 days) for intent improvement.

**WAB-NLU-004 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall recognise Hindi, English and Roman-script Hindi (Hinglish) in text.
- Acceptance: Given "chhutti chahiye" or "छुट्टी चाहिए" When typed Then the leave flow runs in the user's language.
- Rules: Keyword tables carry Devanagari and common Roman spellings. Roman Hindi uses the same keyword list; the classifier (WAB-NLU-002) is the fallback. Spelling variants are managed by a table, not code.

**WAB-NLU-005 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall treat emergency and safety words as an urgent escalation.
- Acceptance: Given text contains words such as "accident", "fire", "missing", "lost child", "hurt", "bus accident", "दुर्घटना", "बच्चा नहीं मिला" When detected Then Dhruva replies "I am alerting the school office right now. If this is an emergency, please call <office number>." and the office inbox shows the message flagged Urgent regardless of office hours.
- Rules: Out-of-hours it also notifies the on-call person set by the campus admin (see Section on Security for the safety job). It never tries to answer the content itself.

**WAB-NLU-006 · Should · P2 · flag: ch.whatsapp · [Spec]**
The system shall handle abuse and off-topic messages without escalating needlessly.
- Acceptance: Given a message is abusive When detected Then Dhruva replies once "Please keep messages respectful so we can help you." and the conversation is flagged for the office; no repeated replies.
- Rules: See WAB-SEC-007 for moderation. Off-topic chat gets the fallback.

### 8.3.10 Voice and language

**WAB-VOI-001 · Should · P2 · flag: ch.whatsapp.voice · [Design]**
Staff can send voice notes in Hindi or English and Dhruva understands them.
- Acceptance: Given Suresh sends a voice note of 4 seconds Then within 10 seconds Dhruva replies "I heard: 'I need leave tomorrow' / Shall I apply casual leave for tomorrow, 7 Oct?" with "Yes, apply" and "No" (Hindi: "मैंने सुना: 'मुझे कल छुट्टी चाहिए'", "हाँ, आवेदन करें", "नहीं").
- Acceptance: Given the audio cannot be understood Then "Sorry, I didn't understand that. You can open the menu or send a voice note." with "Main menu".
- Rules: Needs ai.voice_input. Voice notes up to 60 seconds are processed, longer ones get "Please send a shorter voice note." The prototype's fixed transcript is not the product; real recognition accuracy by accent is a pilot measurement (see 8.7). Audio is kept 30 days and then deleted; the transcript stays as the message text.

**WAB-VOI-002 · Must · P2 · flag: ch.whatsapp.voice · [Design]**
The system shall confirm what it heard and act only after the sender says yes.
- Acceptance: Given "Yes, apply" is tapped Then the leave request is sent to the manager exactly as in WAB-STF-004; given "No" Then "Okay, nothing was sent."
- Rules: Voice never opens or reveals a payslip or any PIN-protected item (the PIN is entered in the form only); voice never changes a record without the confirm tap; voice that names a person other than the sender is refused.

**WAB-VOI-003 · Could · P3 · flag: ch.whatsapp.voice · [Design]**
Parents and teachers can send voice notes too (the Overview toggle "Voice notes: Hindi and English" is school-wide).
- Acceptance: Given a parent sends a voice note Then the same hear-and-confirm pattern applies to the parent topics.
- Rules: The designs show only the toast "Hold to record a voice message" for parents and teachers; until built they get "Voice notes are not available yet. Please type or choose a topic."

**WAB-VOI-004 · Should · P2 · flag: ai.translation · [Spec]**
The system shall reply in the user's language for parents and teachers.
- Acceptance: Given a parent's language is Hindi (chosen in the app at sign-in or by typing "Hindi") When replies and templates are sent Then Hindi strings are used.
- Rules: Parent and teacher prototypes are English only. Strings are maintained translations, not live machine translation; free text from a teacher to a parent is translated only if the teacher approves the translation (see Notices in Section on Notices). Language is a field on the contact; unknown language falls back to the school default.

### 8.3.11 Handover to people

**WAB-HND-001 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
The system shall hand a chat to a person when the user asks or Dhruva cannot help.
- Acceptance: Given a parent picks "Talk to the school office" (or taps "Ask the office") in office hours Then the chat shows the system line "Connecting you to the school office…", a person's greeting such as "Anita · Front office: Hello Mrs. Sharma, this is Anita from the DPS Gurugram front office. How can I help you?", and the line "Type MENU at any time to go back to Dhruva".
- Rules: Staff see "Connecting you to HR…" and "Priya · HR: Namaste Suresh ji, Priya from HR here. How can I help you?". The agent's name is the real agent who claimed the chat; before an agent claims it the line "Connecting you to the school office…" stays and a Handover is "waiting". Dhruva passes a summary (who, which child, the last topic, any attachment) to the agent.

**WAB-HND-002 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
The system shall use set office hours for parents, teachers and staff, and say what happens outside them.
- Acceptance: Given the hours are Mon to Sat, 8 am to 4 pm (parents and teachers) and 9 am to 5 pm (staff, HR) When a handover is requested inside Then it goes to the queue; When requested outside Then Dhruva replies "The school office is closed now. It opens Mon to Sat, 8 am to 4 pm. Your message is saved and the office will reply by <next opening + 2 hours>." and the chat stays in "waiting-human".
- Rules: The designs say only that Dhruva "says when they'll reply" out of hours; the wording is [Spec]. Hours are per audience, per campus, with school holidays from the calendar; shown in the "Business info" text. Emergency words bypass hours (WAB-NLU-005).

**WAB-HND-003 · Must · P2 · flag: ch.whatsapp.handover · [Spec]**
Front office and HR agents shall work chats from an inbox in the DhruvaOne web app.
- Acceptance: Given a handover is waiting When an agent opens "WhatsApp inbox" Then they see sender, matched profile (child and class, or employee), last 10 messages, topic summary, waiting time, 24-hour window countdown, and buttons "Take it", "Reply", "Hand back to Dhruva", "Resolve".
- Rules: Parent and teacher queues go to Front office & admissions users of the campus; staff queues go to HR & admin users. Parent queries of academic type may be assigned to the coordinator (see Section on Parent messaging). Only agents with the role see the inbox. An agent sees the profile data they could see in the app, no more.

**WAB-HND-004 · Must · P2 · flag: ch.whatsapp.handover · [Spec]**
The system shall measure and escalate response time.
- Acceptance: Given a handover has waited 10 minutes inside office hours Then the queue turns amber and notifies the agents; at 15 minutes the campus admin is notified; given it has waited past the SLA at the next opening Then it appears first.
- Rules: Default SLA: first human reply within 15 minutes in hours, within 2 hours of the next opening if out of hours; resolution within one working day. Values are tenant settings. The SLA clock stops on the first human reply, not on an auto-acknowledgement. The designs' replies ("I'll check and call you back by 4 pm today") are typed by the agent; the product does not auto-promise a callback time.

**WAB-HND-005 · Must · P2 · flag: ch.whatsapp.handover · [Design]**
While a person has the chat, Dhruva shall stay quiet and only react to a return word.
- Acceptance: Given the chat is in "human" state When the user types "MENU", "Hi", "Hello", "Hey", "Namaste" or "Start" Then Dhruva returns, shows the menu, and the Handover is closed as "handed back by user".
- Rules: Dhruva sends a single acknowledgement "Thank you, I've noted this" for the first user message that arrives before an agent claims the chat; after that, only agents reply. STOP is always honoured. Attachments from the user in this state go to the agent.

**WAB-HND-006 · Must · P2 · flag: ch.whatsapp.handover · [Spec]**
The system shall hand back to Dhruva and resolve conversations cleanly.
- Acceptance: Given an agent taps "Resolve" Then the user gets "Is there anything else? Type MENU for Dhruva." and the conversation closes as "resolved"; given an agent taps "Hand back to Dhruva" the menu is shown.
- Acceptance: Given no message from either side for 24 hours Then the conversation closes as "resolved (idle)".
- Rules: Agents may add an internal note and a tag (fees, transport, admission, complaint, other). Closed chats stay searchable by authorised users.

**WAB-HND-007 · Must · P2 · flag: ch.whatsapp.handover · [Spec]**
The system shall let an agent reply after the 24-hour window has closed only with an approved template.
- Acceptance: Given the window has closed and the agent writes a reply When sent Then the agent sees "The 24-hour window is closed. Send the 'Reply from school' template?" and sending uses `office_followup`; the user's tap on "Continue" reopens the window and releases the agent's queued text.
- Rules: The agent's text is held (up to 7 days) and sent only after the user taps; it is never merged into the template.

### 8.3.12 Outbound notifications

**WAB-OUT-001 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall send school-initiated WhatsApp messages only for the events in the catalogue below, each with a clear next step.
- Acceptance: Given an event fires for an opted-in contact When routing allows Then the matching template is sent with its variables filled from the source record.
- Rules: The catalogue extends the notification catalogue of the platform (see Section XCT notifications). No marketing messages, ever, except as WAB-OUT-002 allows.

| Event | Audience | Template | Tier | Button | Phase | Flag |
|---|---|---|---|---|---|---|
| Child marked present | Parent | `attendance_present` | Normal | none | MVP | mod.attendance |
| Child absent, not marked present by 9 am | Parent | `attendance_absent` | High | "Message teacher" | MVP | mod.attendance |
| Bus 5 minutes away (on request) / 10 minutes away or late | Parent | `bus_five_min`, `bus_late` | High | "Track" (opens app) | MVP | mod.bus_live |
| Fee due in 7 days, then overdue | Parent | `fee_reminder` | Normal | "Pay by UPI" | MVP | mod.fees |
| Payment received | Parent | `payment_receipt` (PDF) | Normal | none | P2 | mod.fees |
| Circular / notice | Parent, Teacher, Staff | `circular_notice` | Normal | "Got it" | MVP | mod.notices |
| Homework posted | Parent | `homework_posted` | Normal | none | MVP | mod.homework |
| Results published | Parent | `results_published` | Normal | "View result" | P2 | mod.marks_results |
| PTM reminder | Parent | `ptm_reminder` | Normal | none | P2 | mod.calendar_ptm |
| Leave decided | Parent, Teacher, Staff | `leave_decision` | Normal | none | P2 | mod.hr_leave |
| Class attendance not marked | Teacher | `attendance_reminder_teacher` | Normal | "Mark now" | P2 | mod.attendance |
| Cover assigned | Teacher | `cover_assigned` | High | "Accept" / "Can't" | P2 | mod.cover |
| Homework delivery summary | Teacher | `homework_delivery_summary` | Normal | "Remind the 2" | P2 | mod.homework |
| Parent reply to teacher's note | Teacher | `parent_reply_relay` | Normal | none | P2 | ai.reply_drafts |
| Salary credited | Staff | `salary_credited` | Normal | "View payslip" | P2 | mod.payroll |
| Duty reminder | Staff (route or post) | `duty_reminder` | Normal | none | P2 | mod.transport |
| Office or HR reply after window closed | All | `office_followup` | Normal | "Continue" | P2 | handover |
| Opt-in confirmed | All | `optin_confirmation` | Normal | none | MVP | ch.whatsapp |

**WAB-OUT-002 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall use Utility templates for all alerts and allow Marketing templates only for admissions campaigns to people who opted in.
- Acceptance: Given the Admissions CRM schedules an "Open House" campaign When sent Then it uses a Marketing-category template, only to enquiry contacts with a marketing opt-in, and counts in the marketing frequency cap.
- Rules: Marketing is not sent to current parents or staff. Admissions campaigns need their own opt-in wording and appear separately in cost (WAB-ANA-003).

**WAB-OUT-003 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall route each event to the best channel and avoid duplicates.
- Acceptance: Given a parent has the app with push on When an attendance alert fires Then push is sent and no WhatsApp message is sent; Given the parent has no app or push is off Then WhatsApp is the primary channel.
- Acceptance: Given a fee or pickup alert was pushed and not opened for 30 minutes Then a WhatsApp message follows (platform fallback rule), and no further copy after that.
- Rules: Notices from the owner or principal go to both channels when "App" and "WhatsApp" are ticked (default both). Per contact a "preferred channel" can be overridden by the family. Duplicate suppression key: event ID plus contact.

**WAB-OUT-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall cap how many school-initiated templates one person gets and expire stale alerts.
- Acceptance: Given a parent already received 8 templates in 24 hours When another Normal alert fires Then it is moved to the digest or app, not sent; Urgent is never capped.
- Rules: Defaults: Normal max 8 per recipient per 24 hours; notices max 3 per day (Urgent excluded); fee reminders at most 1 per 3 days and 3 per due cycle. User-requested alerts ("Alert me 5 min before", PTM reminder) are exempt. Expiry: attendance and bus alerts expire after 2 hours, fee reminders after 24 hours, notices after 48 hours; an expired alert is dropped and logged. Caps are tenant settings.

**WAB-OUT-005 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall respect quiet hours.
- Acceptance: Given quiet hours are 9 pm to 7 am When a Normal or High alert fires at 10 pm Then it waits until 7 am (still inside its expiry, else it is dropped) and Urgent is sent at once.
- Rules: Same default and tiers as the platform (Normal, High, Urgent; see Section XCT). Exceptions: alerts a user asked for, and staff duty reminders that are scheduled by the school for the recipient's shift (the design sends one at 6:00 am), which follow a per-audience schedule instead (see 8.8, Q7). Parents can change their quiet hours; safety and early-pickup alerts cannot be turned off but follow the channel rule in WAB-OPT-004.

**WAB-OUT-006 · Should · P2 · flag: ai.translation · [Design]**
The system shall send alerts in the recipient's language, and bilingual for staff where the design shows it.
- Acceptance: Given a driver's language is Hindi When `duty_reminder` is sent Then the Hindi line is shown; for `salary_credited` and `duty_reminder` the template body carries English and Hindi together (design: Hindi line below the English).
- Rules: Parent and teacher templates are approved per language (en, hi); the sender chooses by contact language. Missing translation falls back to English and raises a content task.

**WAB-OUT-007 · Must · MVP · flag: mod.notices · [Spec]**
The system shall track delivery and read of notices sent through WhatsApp together with app reads.
- Acceptance: Given a notice goes to 2,976 recipients When viewed in the notice screen Then it shows delivered, read (WhatsApp read or app open) and failed counts, and a "Remind" action for unread people which respects WAB-OUT-004.
- Rules: "Got it" button taps count as a confirmed read. Read counts say "Read by n of m" and the figure excludes people whose receipts are off only when stated.

**WAB-OUT-008 · Must · MVP · flag: mod.attendance · [Design]**
The system shall message parents about attendance in the forms shown in the designs.
- Acceptance: Given Vivaan is marked present at 7:48 am Then "Attendance: Vivaan Sharma reached school at 7:48 am and was marked present" arrives (7:49 am in the sample); given a child is not marked present by 9 am Then `attendance_absent` arrives with "Tap if this is wrong" semantics (button "Message teacher").
- Rules: One message per child per day per type; for a parent with two children the system sends one per child. A correction message is sent if the record changes (see WAB-TCH-003).

**WAB-OUT-009 · Must · MVP · flag: mod.fees · [Design]**
The system shall send fee reminders with a "Pay by UPI" button.
- Acceptance: Given a transport fee of Rs 9,600 is due on 10 Oct When the reminder fires at 9:00 am Then the text "Fee reminder: Transport fee Rs 9,600 for Oct to Dec is due on 10 Oct." and the button "Pay by UPI" are sent.
- Rules: In MVP the button opens the gateway payment page; the in-chat sheet arrives with WAB-PAR-003 (P2). Reminder wording is drafted by Dhruva (ai.fee_followup) and sent by the rule set by accounts; no reminder to a parent who has an open dispute or concession pending.

**WAB-OUT-010 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall return approver decisions to the chat.
- Acceptance: Given the class teacher approves leave in her app Then the parent's `leave_decision` is sent within 1 minute with the footer shown in WAB-PAR-009.
- Rules: Inside the window it is sent as a normal message (cheaper), otherwise as the template.

**WAB-OUT-011 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall handle replies to templates.
- Acceptance: Given a parent taps a quick-reply or types a reply to an alert When received Then buttons run their action ("Got it" confirms the notice, "Message teacher" opens a teacher thread or the office inbox) and free text goes to the bot (P2) or the office inbox (MVP).

### 8.3.13 Security

**WAB-SEC-001 · Must · MVP · flag: core · [Spec]**
The system shall not show sensitive data until the sender is verified at the level that data needs.

| Data class | Examples | Verification needed on WhatsApp |
|---|---|---|
| Public | School calendar, holiday list, hours | Registered number or none |
| Child basic | Attendance, bus, homework | Registered guardian number (active) |
| Child sensitive | Marks, report card, fee dues, receipts | Registered guardian number marked fee-payer or contact for that child; not "Disputed" |
| Staff basic | Timetable, leave balance, duty, holidays | Active staff number |
| Staff sensitive | Payslip, bank mask, advance status | Staff number plus the 4-digit PIN session |
| Never on WhatsApp | Counsellor notes, health data, other children's data, full DOB, full bank account, Aadhaar, passwords, OTP | Not offered |

- Acceptance: Given a number is "Disputed" or a PIN is missing When sensitive data is asked for Then Dhruva replies with the refusal ("Please enter your PIN" or "Please contact the school office") and shows none of it.

**WAB-SEC-002 · Must · P2 · flag: ch.whatsapp.payslip · [Spec]**
The system shall verify the staff PIN securely and limit attempts.
- Acceptance: Given three wrong PINs in a row When submitted Then the PIN is locked for 30 minutes with "Too many tries. Please try again after 30 minutes or ask HR to reset your PIN."; a correct PIN resets the count.
- Rules: The PIN is the 4-digit PIN set with HR (the same one used for the apps' profile lock unless the school separates them; see 8.8, Q9). It is entered only in the form (WhatsApp Flow), stored only as a salted hash, never logged or shown in the transcript (the echo reads "PIN entered"). If a user types digits in a chat message after "Enter PIN", the system does not treat them as a PIN and says "Please use the form. Never type your PIN in the chat." The PIN session lasts 15 minutes of inactivity (the same as the web re-PIN) and ends on "switch". Lock events are alerts to HR. PINs that are trivially guessable (0000, 1234) are refused at set-up.

**WAB-SEC-003 · Must · P2 · flag: ch.whatsapp.upi_pay · [Spec]**
The system shall keep payments safe: the user's own UPI app and UPI PIN complete every payment.
- Acceptance: Given a payment is started Then DhruvaOne and WhatsApp never receive the UPI PIN or OTP, and the pay link works only for the order it was created for.
- Rules: The pay link is single-use, tied to the child and order, expires in 30 minutes, and carries no PII in the URL. Amount is fixed by the ledger. Partial payment and part-heads are not offered unless the fee module allows them. Refunds never happen from chat. Any message that asks a parent for card, UPI PIN or OTP is blocked by the content check (WAB-SEC-007). Dhruva states "Dhruva never asks for your PIN or OTP" in the pay message.

**WAB-SEC-004 · Must · MVP · flag: core · [Spec]**
The system shall minimise personal data in templates and replies.
- Acceptance: Given the lock screen shows a template preview When an alert is sent Then it contains the child's first name and class, the time or amount needed, and never marks, diagnoses, bank numbers (only the last four digits), or other children.
- Rules: Salary amounts appear in `salary_credited` in the design; a tenant switch "Hide amounts in alerts" (default off, see 8.8, Q8) removes them and keeps "View payslip". Payslip PDFs sent to WhatsApp stay on the user's phone and in WhatsApp's own storage, which the school cannot retract; the PIN gate is the control, and this limit is disclosed to tenant admins when they enable payslips.

**WAB-SEC-005 · Must · MVP · flag: core · [Spec]**
The system shall secure the integration end to end.
- Acceptance: Given a webhook request arrives with an invalid signature When received Then it is rejected with 401 and logged; valid ones are processed once by message ID.
- Rules: HTTPS only; the provider's signature header is verified with the app secret; access tokens and secrets are stored per tenant in the secret vault and rotated on staff leaving DhruvaOne; media is stored encrypted at rest in the India region; per-tenant isolation in all queries; no message content in application logs (IDs only).

**WAB-SEC-006 · Must · MVP · flag: core · [Spec]**
The system shall retain and delete chat data on a defined schedule.
- Acceptance: Given retention defaults When 12 months pass Then message bodies are redacted to metadata; given a 90 day audio or media age Then the file is deleted.
- Rules: Defaults: text 12 months, inbound photos 90 days, audio 30 days, payslip document sends keep metadata only. Tenant admins can shorten. Data subject requests (access, correction, deletion) follow the school's DPDP process; opt-out data is kept as the proof that STOP was honoured. DhruvaOne support cannot read content without the tenant's explicit, time-limited consent, which is audited.

**WAB-SEC-007 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall moderate content in both directions.
- Acceptance: Given an agent or a teacher's drafted note contains a blocked phrase (abuse, requests for card, UPI PIN, OTP or password, political or commercial promotion) When about to be sent Then it is blocked with a reason and nothing is sent.
- Acceptance: Given an inbound message is abusive or threatening toward staff Then it is flagged to the campus admin and the agent can reply with a template "We cannot continue this chat" and block the number from the bot (the block is reviewable).
- Rules: Templates and Dhruva-drafted notices are approved by a person before reaching families. Images from parents are not opened by Dhruva; agents see them with a "Contains images" notice and can delete them. Child images and ID-card photos sent by parents are stored in the conversation only and not in student records unless an agent files them.

**WAB-SEC-008 · Must · MVP · flag: core · [Design]**
The system shall apply the same permissions, approvals and audit as the app to every WhatsApp action.
- Acceptance: Given a teacher posts homework from WhatsApp When viewed in the audit log Then the entry shows actor, role, class, channel "WhatsApp", provider message ID, time, and the record changed.
- Rules: A WhatsApp action never grants more rights than the same person has in the app; if the app requires approval, WhatsApp raises the same approval. Dhruva prepares or suggests; a person approves or the sender confirms. Every conversation turn is stored with the matched profile ID.

### 8.3.14 Admin controls

**WAB-ADM-001 · Must · MVP · flag: ch.whatsapp · [Design]**
Campus admins can see and control the channel from a "WhatsApp channel" settings card.
- Acceptance: Given the admin opens Settings Then the card shows the number ("+91 124 XXX XXXX · verified") with the status "Live", rows Parents (Attendance, fees, homework, bus, exams, leave), Teachers (Attendance, homework, timetable, leave), Staff (Payslips, leave, duty, holidays, advance), the four toggles and the four usage tiles.
- Rules: Group admins set defaults for all campuses; campus admins can override within what the group allows (see Section TFC). Rows list only what the tenant's flags allow.

**WAB-ADM-002 · Must · MVP · flag: ch.whatsapp · [Design]**
Admins can enable the channel per audience and per campus.
- Acceptance: Given the admin switches Parents off for Campus A Then parents at Campus A get no alerts or bot replies on WhatsApp and the fallback channels are used; their data is kept.
- Rules: Audience flags are ch.whatsapp.parent_bot, ch.whatsapp.teacher_bot, ch.whatsapp.staff_bot; alerts per audience are switched with ch.whatsapp.alerts (NEW). A schedule (for example off during exam week) is supported by TFC. When a bot flag is off but alerts stay on, replies from users go to the office inbox.

**WAB-ADM-003 · Must · MVP · flag: ch.whatsapp · [Design]**
Admins can switch the four channel features.
- Acceptance: Given the toggles "UPI fee payments in chat" (money goes straight to the school account), "Payslips on WhatsApp" (always behind the staff member's PIN), "Voice notes" (Hindi and English), "Admissions enquiries" (new families can ask about seats and fees) When changed Then the related rows disappear or appear within 1 minute for new messages.
- Rules: They map to ch.whatsapp.upi_pay, ch.whatsapp.payslip, ch.whatsapp.voice, ch.whatsapp.admissions; the default is off until the school confirms each, except voice which follows ai.voice_input.

**WAB-ADM-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
Admins can manage templates: see status, edit, submit, retire.
- Acceptance: Given a template is "Rejected" When the admin opens it Then Meta's reason is shown with "Edit and resubmit"; "Approved" templates show quality (High/Medium/Low), sends in 30 days, delivery and read rates.
- Rules: DhruvaOne ships a starter set (the catalogue in WAB-OUT-001) in English and Hindi with sample variables, submitted through the provider on the tenant's behalf at setup. Tenants can edit wording within the placeholders; deleting a template in use is blocked.

**WAB-ADM-005 · Must · P2 · flag: ch.whatsapp.handover · [Spec]**
Admins can set office hours, holidays, the queue members and the SLA.
- Acceptance: Given hours are changed to "Mon to Sat, 8 am to 4 pm" Then the "Business info" text and the out-of-hours reply use the new hours at the next message.
- Rules: Per audience, per campus. Queue members come from Front office & admissions and HR & admin users. A holiday is taken from the school calendar.

**WAB-ADM-006 · Should · MVP · flag: ch.whatsapp · [Spec]**
Admins can set quiet hours, frequency caps, language defaults and the monthly budget.
- Acceptance: Given the admin sets quiet hours 8 pm to 7 am Then Normal and High alerts wait accordingly; the cap and budget fields reject non-numeric or negative values.
- Rules: See WAB-OUT-004, -005, WAB-ANA-004.

**WAB-ADM-007 · Should · MVP · flag: ch.whatsapp · [Spec]**
Admins can send a test message and preview each template.
- Acceptance: Given the admin enters their own number When "Send test" is pressed Then the template is sent with sample data and labelled "Test"; nothing is recorded as a family alert.

### 8.3.15 Analytics and cost control

**WAB-ANA-001 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall show usage tiles on the admin card.
- Acceptance: Given a week of use Then the card shows "chats this week" (for example 1,284), "% answered by Dhruva" (91%), "% handed to office or HR" (9%), and "average reply" in seconds (4 sec).
- Rules: Definitions: a chat is a conversation opened by an inbound message or by a reply to an alert; "answered by Dhruva" means the conversation closed without entering waiting-human; "handed over" means it entered waiting-human; average reply is the mean time from inbound message received to Dhruva's reply accepted by the provider, excluding photo and voice processing. The design numbers are sample data. Before the bot exists (MVP) the tiles show "Alerts sent", "Delivered", "Read", "Replies".

**WAB-ANA-002 · Should · P2 · flag: ch.whatsapp · [Spec]**
The system shall give admins deeper analytics.
- Acceptance: Given the admin opens "WhatsApp analytics" Then they can filter by campus, audience and date and see: sends, delivered, read and failed per template; opt-ins, opt-outs, STOP rate; unmatched-number count; top topics; fallback ("Ask the office") rate; handover count, median first-response time and SLA breaches; photo and voice reads; PIN failures; quality rating history.
- Rules: Group admins see a campus comparison. Message content is not shown in analytics.

**WAB-ANA-003 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall record the billable category of every message so cost is attributable to a tenant and campus.
- Acceptance: Given the provider callback or invoice line gives the pricing category (Utility, Marketing, Authentication, or free service reply) When processed Then the message stores category, billable yes or no, and the rate from the tenant's rate card effective on that date.
- Rules: The Overview says rates are "to be confirmed with the provider" and that school-initiated alerts cost per alert while replies inside a chat the person started cost less or nothing; so the rate card is data entered and dated, not code. Meta's pricing is per message by category and changes; the code reads categories, not prices. Monthly totals are by tenant, campus, audience, template and category and reconciled with the provider invoice (differences over 2 percent flagged).

**WAB-ANA-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall support a monthly spend budget with alerts and a safe cap.
- Acceptance: Given a budget of Rs 50,000 When spend reaches 70, 90 and 100 percent Then the tenant admin is notified; at 100 percent Normal and High templates move to push, Urgent and free in-window replies continue.
- Rules: The budget is optional; "No cap" is a valid setting. The cost view shows spend to date, forecast to month end, cost per family and the top templates; broadcast notices show a pre-send estimate ("About Rs 2,800 for 2,976 people").

### 8.3.16 Failure modes and fallback

**WAB-FAL-001 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall detect a WhatsApp or provider outage and protect delivery.
- Acceptance: Given more than 20 percent of sends fail with provider or network errors over 5 minutes (or the provider reports an incident) When detected Then a circuit opens: new alerts are queued, Urgent and High go to push and SMS at once, and the admin card shows "WhatsApp delayed".
- Rules: Queued Normal items are retried with backoff and released when the circuit closes (a probe every minute), subject to their expiry (WAB-OUT-004). Inbound messages missed during an outage are replayed from the provider's retries; replies are sent after recovery.

**WAB-FAL-002 · Must · MVP · flag: ch.sms · [Spec]**
The system shall follow a fallback ladder when WhatsApp cannot deliver.
- Acceptance: Given a WhatsApp send fails permanently or the window is closed with no suitable template When the event is Urgent Then push is tried, then SMS; for High, push; for Normal, push only; the audit shows each attempt.
- Rules: Platform rule: SMS is used for gate safety only; this section extends it to Urgent safety and to staff who have no app, as a tenant choice, with DLT-registered SMS templates (India). SMS carries a short text and a link, no marks, fees or payslip data. Fee and pickup fallback to WhatsApp after 30 minutes unopened remains (WAB-OUT-003); the reverse (WhatsApp failed, push fallback) is this requirement.

**WAB-FAL-003 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall handle template rejection and pausing.
- Acceptance: Given Meta rejects `fee_reminder` When the callback arrives Then the admin and DhruvaOne support are notified with Meta's reason, the event moves to push only, and a suggested rewrite is shown for the admin to approve and resubmit.
- Rules: If an approved template is paused for low quality, the event falls back the same way until it is reinstated; a rewrite is never submitted without a person.

**WAB-FAL-004 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall handle a number that is blocked, restricted, disconnected or flagged.
- Acceptance: Given Meta restricts the number When detected Then all school-initiated sends stop, all events use push and SMS under WAB-FAL-002, the card shows "Paused: number restricted", and support is alerted.
- Rules: Recovery steps (appeal, reregistration, backup number if the tenant has one) are shown on the card. A tenant should keep a second registered number for the group in P2 (8.8, Q2). The tenant's families are told by an app notice if the number changes.

**WAB-FAL-005 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall handle recipients who cannot be reached.
- Acceptance: Given a message fails with a "not on WhatsApp", "blocked the business" or "undeliverable" error 3 times in a row When processed Then the contact is marked "WhatsApp undeliverable", WhatsApp is skipped for that person, and an office task "Check this parent's number" is created.
- Rules: A new inbound message from that number clears the mark.

**WAB-FAL-006 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall fail safely inside conversations.
- Acceptance: Given a data source cannot answer (fee ledger down) When a parent asks for fees Then Dhruva says "I can't check this right now. Please try again in a few minutes." with "Ask the office" and "Main menu", and never guesses.
- Rules: A failed write never shows "sent"; the user sees "That did not go through. Nothing was saved." Retries do not duplicate (idempotency, WAB-MNU-007). Photo reading failures say "I could not read this photo. Please send a clearer one." and the teacher's own typed way stays available.

**WAB-FAL-007 · Must · MVP · flag: core · [Spec]**
The system shall process webhooks reliably.
- Acceptance: Given the same message ID arrives twice Then it is handled once; given the processor is down the provider's retries are accepted within 7 days of backlog and replayed in order per contact.
- Rules: The webhook returns 200 within 3 seconds after queuing; slow work (photo reading, ASR) runs asynchronously and Dhruva sends "Reading…" first.

**WAB-FAL-008 · Must · P2 · flag: ch.whatsapp.upi_pay · [Spec]**
The system shall handle payment failures and delays.
- Acceptance: Given a UPI payment is pending When the user asks "Did my payment go through?" Then Dhruva says "Your payment is still being confirmed. We will message you when it is done." and the receipt follows on the gateway callback; given the payment fails Then "The payment did not go through. No money was taken. Try again" with a new link.
- Rules: Duplicate payments for the same order are caught by the ledger and refunded by accounts (never by chat); a payment confirmed after the 30-minute link expiry still produces a receipt (template `payment_receipt`); mismatched amounts raise an accounts task.

## 8.4 Business rules and policies

1. The verified school number is the only sender. Dhruva never asks for UPI PIN, OTP, passwords or card numbers; the screens and the HELP text say so [Design].
2. The phone number is the key; no password. Staff pay data and the staff profile on a shared number need a PIN [Design].
3. A parent sees only their own child's data; each parent sees only their own child's marks [Design].
4. Dhruva prepares, drafts and suggests. A person approves anything that changes a record or reaches a family: leave goes to the class teacher, Principal, manager or HR; drafted notes go only on "Send it"; photo-read data can be undone [Design, extended by Spec for safeguards].
5. School-initiated messages need opt-in, use approved templates, and stop on STOP [Design, Spec].
6. Role permissions, approvals and audit logs of the app apply to every WhatsApp action [Design].
7. Office hours for handover: Mon to Sat 8 am to 4 pm (parents, teachers), 9 am to 5 pm (staff, HR); configurable [Design].
8. Staff chat is Hindi-first: short answers, large buttons, bilingual alerts, voice input [Design].
9. Fees are paid by UPI inside the chat only where the tenant switched it on; money goes straight to the school account and the receipt is a PDF [Design].
10. Out-of-window messages are templates only; the bot is silent while a person is in the chat [Spec, Design].
11. Cost is tracked per tenant and never silently exceeds the budget cap [Spec].
12. Unknown numbers get no data and one polite reply per day [Design, Spec].

## 8.5 Notifications and approvals raised by this section

| Trigger on WhatsApp | Who is notified | Approval needed | Result back to WhatsApp |
|---|---|---|---|
| Parent leave request | Class teacher (app) | Class teacher approves or declines | `leave_decision` to parent |
| Teacher leave request | Principal (or HoD within limits) | Approver per chain | `leave_decision`; cover arranged and class informed |
| Staff leave request | Manager (for example transport manager) | Manager | `leave_decision` with relief line |
| Salary advance | HR | HR decision in payroll | Answer within 2 working days |
| Cover decline | Coordinator | New cover search | Confirmation when replaced |
| Breakdown or delay report | Transport desk | none (alert); parent alert approved by in-charge | Call-back confirmation |
| Photo-read attendance | Parents of absentees | Teacher is the person; Undo window | Correction message if undone |
| Photo-read marks | Parents or HoD | Per marks setting | Reply states publication state |
| Drafted parent note | Parent | Teacher taps "Send it" | Parent reply relayed |
| Handover waiting | Front office or HR queue; campus admin on SLA breach | none | Agent reply |
| Emergency words | Office inbox (Urgent), on-call | none | Immediate reply |
| STOP, "wrong number" | Office (wrong number only) | none | Confirmation text |
| Template rejected or paused, quality drop, number restricted | Tenant admin, DhruvaOne support | Admin approves a rewrite | Event falls back to push |
| Budget at 70, 90, 100 percent | Tenant admin | none | Behaviour per WAB-ANA-004 |
| PIN lockout | HR | none | Lock message to the user |

## 8.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| ch.whatsapp | The WhatsApp account, outbound alerts framework, STOP/START, baseline inbox | On when the number is Live | Master switch; off sends all events to push (and SMS under rules) |
| ch.whatsapp.parent_bot | Parent conversations, menu and flows | Off until launch | Per campus |
| ch.whatsapp.teacher_bot | Teacher conversations | Off until launch | Per campus |
| ch.whatsapp.staff_bot | Staff conversations (Hindi and English) | Off until launch | Per campus |
| ch.whatsapp.voice | Voice notes (admin toggle "Voice notes") | Off | Needs ai.voice_input |
| ch.whatsapp.photo_upload | Photo of register, marks, notes (teachers) | Off | Needs ai.marks_from_photo |
| ai.whatsapp_bot | Intent classifier for free text | Off | Menus and keywords work without it |
| ai.voice_input | Speech recognition | Off | See Section AI |
| ai.translation | Hindi/English strings and alert languages | On | Hindi first for staff |
| ai.reply_drafts | Drafted parent notes, tips | On | Person approves |
| ai.marks_from_photo | Reading photos | Off | Prototype status; see Q5 |
| mod.* (attendance, fees, homework, exams, marks_results, report_cards, bus_live, transport, calendar_ptm, hr_leave, payroll, timetable, cover, notices) | Each topic row and alert | Per tenant | Row hidden when the module is off; data kept |
| ch.whatsapp.alerts | School-initiated templates per audience | On with channel | Separates alerts from the bot |
| ch.whatsapp.upi_pay | UPI payment in chat (toggle "UPI fee payments in chat") | Off | Needs payment gateway account |
| ch.whatsapp.payslip | Payslips on WhatsApp (toggle "Payslips on WhatsApp") | Off | Always behind the PIN |
| ch.whatsapp.admissions | Admissions enquiries (toggle "Admissions enquiries") | Off | Flow minimal, P3 |
| ch.whatsapp.handover | Talk to office / HR | On | Off hides the row and routes to the app form |
| ch.sms | SMS fallback for Urgent and staff without app | Off | Needs DLT templates |

## 8.7 Non-functional requirements (specific to this section)

- **Latency.** Bot reply to a menu tap or text: 95th percentile 5 seconds, median 2 seconds. Photo read acknowledgement within 3 seconds; result within 15 seconds at the 95th percentile. Voice reply within 10 seconds. Payment confirmation message within 15 seconds of the gateway callback [Spec].
- **Alert latency.** Attendance alert sent within 60 seconds of the record; bus 5-minute alert within 30 seconds of the trigger; at 3,000 recipients per campus per morning all sent within 10 minutes [Spec].
- **Availability.** Webhook endpoint 99.9 percent monthly; no loss of inbound messages during deployment (queue before processing) [Spec].
- **Accuracy pilots.** Photo reading: report the share of registers and mark sheets published without correction; voice: share of Hindi and English notes confirmed with "Yes, apply" on first try. Targets are set after the Gurugram Sec 45 pilot (from 5 Jan 2027) [Spec].
- **Scale.** 14 campuses, tens of thousands of contacts per tenant; per-tenant rate and budget isolation so one tenant cannot use up another's throughput [Spec].
- **Accessibility and language.** Short messages (under 400 characters where possible), buttons within WhatsApp limits, Devanagari rendering tested on low-end Android, bilingual strings complete for staff [Design, Spec].
- **Auditability.** Every inbound and outbound message, state change, handover and setting change is logged with tenant, campus, profile, provider message ID [Design, Spec].
- **Compliance.** DPDP Act roles (school fiduciary, DhruvaOne processor), India-region storage, Meta Commerce and Business Policy, TRAI DLT for SMS fallback [Spec].

## 8.8 Open questions

1. **Bot phase.** The designs build the three phone prototypes and the Overview says "New feature"; mvp-scope puts "Dhruva on WhatsApp" in Phase 1 (Apr to Sep 2027) and only "WhatsApp Business" alerts in the MVP build. Confirm which flows are in the first release.
2. **Number plan for DPS Group.** One number for all 14 campuses or one per campus; do we keep a backup number; does a standalone school buy its own number or share a platform number (which would need the "which school" prompt)?
3. **Green tick.** Is "verified" a launch condition or a goal? Meta grants it at its discretion.
4. **In-chat payment mechanism.** The design shows a UPI app sheet inside the chat. Confirm whether the provider and gateway support in-chat payment for the tenant, or whether to use a link to a hosted payment page.
5. **Review before publishing.** Attendance, marks and learning plans publish with Undo only (project open decision). Should low-confidence photo results always ask first, and should marks wait for HoD check by default? This spec adds a confirm step on doubts and a 2-minute alert hold; confirm.
6. **Bus alert timing.** WhatsApp offers "Alert me 5 min before" on request; the platform catalogue sends "10 minutes away or late" by push. Confirm both and the default for families without the app.
7. **Quiet hours vs duty reminders.** The staff duty reminder is drawn at 6:00 am, inside the 9 pm to 7 am quiet period. Confirm a per-audience exception.
8. **Amounts on the lock screen.** The salary alert shows "Rs 21,450" and the account tail. Keep as designed or default to hidden?
9. **PIN.** Is the WhatsApp payslip PIN the same as the app profile PIN or a separate one set with HR? Is 4 digits enough (SIM swap risk)?
10. **Opt-in proof.** Do admission forms already capture WhatsApp consent text? For existing parents imported from Excel, what wording and evidence do we need?
11. **Early pickup.** Platform sends pickup alerts with "Approve or refuse"; WhatsApp has no approval button in the designs. Add one, or link to the app?
12. **Marketing templates.** Are admissions campaign templates (Open House) in scope for this channel and under which opt-in?
13. **Agent tooling.** The designs show only the person's messages in the chat; confirm where agents work (web inbox, shared device, or the provider's own console) and who staffs the queue per campus.
14. **Out-of-hours text.** The designs say Dhruva "says when they'll reply" but show no wording; confirm the text above.
15. **Languages beyond Hindi.** Regional languages are Phase 1; which first?

---

## Annex 8-A (engineering)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| WaAccount | id, tenant_id, campus_scope (all or campus ids), waba_id, phone_number_id, display_number, display_name, verified_badge, status (setting_up, live, limited, paused), quality_rating, messaging_tier, provider, secret_ref, rate_card_id, budget_monthly, created_at | One per sender number; secrets in vault only |
| WaContact | id, tenant_id, wa_id (E.164), account_id, profile_ids[], language, preferred_channel, window_expires_at, pin_state (none, set, locked_until), pin_session_until, selected_profile_id, selected_profile_until, selected_child_id, status (active, undeliverable, disputed, blocked), last_inbound_at | One per number per account; PIN hash stored in the identity service, not here |
| OptIn | id, contact_id, tenant_id, category (alerts, marketing), source (admission, onboarding, hr, keyword, import), evidence_text, status (opted_in, opted_out), recorded_by, at | Append-only rows; latest wins |
| Conversation | id, tenant_id, campus_id, contact_id, profile_id, audience, state (bot, waiting_human, human, resolved), flow, flow_step, flow_token, opened_by (inbound, alert_reply), opened_at, closed_at, close_reason, containment (bool), language | One open per contact per account |
| Message | id, conversation_id, wamid, direction, type (text, interactive, template, image, audio, document, location, flow), body_redacted, template_id, media_ref, status (queued, accepted, sent, delivered, read, failed), error_code, category, billable, price_ref, event_id, sent_by (bot, agent_id, system), created_at, status_at | Unique on wamid; no PIN or secrets in body |
| Template | id, tenant_id, account_id, name, language, category, status, version, body, header, footer, buttons[], variables[], quality, meta_template_id, reject_reason, last_synced_at | Version rows keep history; unique (account, name, language, version) |
| Handover | id, conversation_id, queue (office, hr), reason (user_request, fallback, emergency, bot_failure), status (queued, claimed, active, resolved, handed_back, expired), claimed_by, requested_at, first_response_at, resolved_at, sla_due_at, tags[], notes | SLA values from WaSettings |
| WaSettings | tenant_id, campus_id, audience flags, toggles, hours per audience, holidays_ref, quiet_hours, caps, budget, hide_amounts, undo_window_seconds, sla values, language_default | Group defaults, campus overrides |
| WaOutbound | id, event_id, contact_id, template_id, tier, not_before, expires_at, attempts, fallback_path, status (pending, sent, deferred, dropped, fallback), reason | Queue and audit of delivery decisions |
| WaUsageMeter | tenant_id, campus_id, month, category, count, cost, template_id | Aggregates for cost and analytics |
| WaFlowSession | id, contact_id, flow_id, token, step, payload_ref, expires_at | Form state; payload purged on completion |

### APIs

| Method and path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| GET /wa/webhook/{account_id} | Provider verification handshake | Verify token | 403 bad token |
| POST /wa/webhook/{account_id} | Inbound messages and status callbacks (messages, statuses, template and quality updates); delivery statuses, opt-outs and in-chat payment notices are forwarded to the platform (`POST /internal/v1/wa/events`, Section 9) | HMAC signature header | 401 bad signature; 200 on duplicate (idempotent on wamid) |
| POST /wa/send | Send one message (text, interactive, template, document) | Internal service; tenant-scoped | 409 window closed (template required); 422 template not approved; 429 rate limit; 451 contact opted out |
| POST /wa/notify | Request an event notification (resolves channel, template, caps, quiet hours) | Internal modules | 422 unknown event; 202 deferred or dropped with reason |
| GET /wa/accounts, PATCH /wa/accounts/{id} | View and edit account settings, profile, display name | Tenant admin; campus admin (own campus) | 409 name under review |
| GET /wa/templates, POST /wa/templates, PUT /wa/templates/{id}, POST /wa/templates/{id}/submit, DELETE /wa/templates/{id} | Manage templates | Tenant admin; campus admin read | 422 validation list; 409 template in use |
| POST /wa/templates/sync | Pull template status and quality from the provider | Tenant admin; scheduler (every 15 min) | 502 provider |
| GET /wa/conversations, GET /wa/conversations/{id} | Inbox list and transcript | Front office, HR agents; campus admin | 403 outside queue scope |
| POST /wa/conversations/{id}/claim, /reply, /handback, /resolve, /note | Agent actions | Agent roles | 409 already claimed; 409 window closed (offer template) |
| POST /wa/optin, DELETE /wa/optin/{contact_id} | Record or withdraw opt-in manually or by import | Front office, HR; tenant admin (import) | 422 missing evidence |
| GET/PUT /wa/settings | Audience flags, toggles, hours, caps, budget | Tenant admin; campus admin within group limits | 403 above group limit |
| GET /wa/analytics, GET /wa/usage | Tiles, analytics, cost | Campus admin, tenant admin | none |
| POST /wa/flows/endpoint | Encrypted data exchange for WhatsApp Flows (roster, dates, PIN check) | Provider-signed; per flow token | 400 bad token; 410 expired |
| GET /wa/media/{id} | Authenticated media fetch for agents | Agent roles | 404 expired and deleted |

Payment results for in-chat fee payments come only from the payment gateway, at `POST /v1/webhooks/gateway` (Section 9). The fees module records the payment once, by gateway payment id, and asks the gateway to send the receipt.

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| wa.message.received | Inbound message stored | conversation_id, contact_id, type, wamid | Bot, inbox, analytics |
| wa.message.status | Provider status callback | wamid, status, error_code | Outbound queue, notices, analytics |
| wa.contact.identified | Number matched | profile ids, audience | Bot, audit |
| wa.contact.unmatched | Unknown number | wa_id hash | Audit, abuse limiter |
| wa.optin.recorded / wa.optout.recorded | Opt-in or STOP | source, category | Outbound routing, audit |
| wa.conversation.opened / closed | State change | state, containment | Analytics |
| wa.handover.requested / claimed / handed_back / resolved / sla_breached | Handover steps | queue, waiting_seconds | Inbox, notifications, analytics |
| wa.flow.completed | Form submitted | flow, record_ref | Modules (attendance, leave, homework, advance) |
| wa.photo.read | Photo processed | doc_type, confidence, record_ref | Modules, audit |
| wa.voice.transcribed | Audio processed | language, confidence | Bot |
| wa.pin.failed / locked / session_started | PIN steps | contact_id, count | Security, HR |
| wa.template.submitted / approved / rejected / paused | Template lifecycle | template_id, reason | Admin notifications |
| wa.account.quality_changed / limit_reached / restricted | Meta health change | old, new | Outbound control, admin |
| wa.outbound.fallback_used | Channel switched | event_id, from, to, reason | Notification service, audit |
| wa.cost.threshold_reached | Spend at 70, 90, 100 percent | tenant_id, pct | Admin notifications, outbound control |
| wa.payment.completed / failed | The fees module confirms or fails an in-chat order (from the gateway callback, Section 9) | order_id, amount | Bot (receipt or retry message) |

### State machines / workflows

**Conversation**

| From | Event | To |
|---|---|---|
| (none) | Inbound message from a matched number | bot |
| bot | User asks for a person, taps "Ask the office", emergency word, bot failure twice | waiting_human |
| waiting_human | Agent claims, in office hours | human |
| waiting_human | Out of hours: stays until opening; at opening the queue is released | waiting_human |
| human | Agent "Hand back" or user types MENU, Hi, Hello, Hey, Namaste, Start | bot |
| human | Agent "Resolve" | resolved |
| bot | Flow done and no message for 30 minutes | resolved |
| any | 24 hours idle | resolved (idle) |
| resolved | New inbound message | bot (new conversation) |

Sub-states within bot: awaiting_choice, awaiting_form, awaiting_pin, awaiting_confirm (voice, photo doubt), awaiting_language.

**Template approval**

| From | Event | To |
|---|---|---|
| draft | Admin submits (validation passes) | pending |
| pending | Meta approves | approved |
| pending | Meta rejects | rejected (reason) |
| rejected | Admin edits and resubmits (or appeals) | pending |
| approved | Quality falls | paused (auto) |
| paused | Quality recovers or admin edits | approved or pending |
| approved | Meta disables, or admin retires | disabled |
| approved | Admin edits | new version in pending; old version stays approved until the new one is approved |

**Opt-in**: unknown -> opted_in (source) -> opted_out (STOP) -> opted_in (START or form). **Message**: queued -> accepted -> sent -> delivered -> read; any -> failed. **Handover**: queued -> claimed -> active -> resolved or handed_back; queued -> expired (no response after 7 days, closed with a note). **Outbound decision**: pending -> (opt-in? window? caps? quiet hours? budget? circuit?) -> sent, deferred, dropped (expired), or fallback.

### Permission matrix

| Capability | Parent | Teacher | Staff | Front office agent | HR agent | Campus admin | Tenant admin | DhruvaOne support |
|---|---|---|---|---|---|---|---|---|
| Chat with bot (own scope) | Yes | Yes | Yes | n/a | n/a | n/a | n/a | n/a |
| Pay fee by UPI | Yes (own child) | no | no | no | no | no | no | no |
| Open payslip (with PIN) | no | Yes (own) | Yes (own) | no | no | no | no | no |
| Post homework, attendance, photo | no | Yes (own classes) | no | no | no | no | no | no |
| View conversations | Own | Own | Own | Parent and teacher queue, own campus | Staff queue | All, own campus | All (view) | By consent only |
| Claim, reply, hand back, resolve | no | no | no | Yes | Yes (staff queue) | Yes | no | no |
| Edit office hours, queues | no | no | no | no | no | Yes | Yes | no |
| Toggle features and audiences | no | no | no | no | no | Yes (within group limits) | Yes | no |
| Manage and submit templates | no | no | no | no | no | View | Yes | Assist on request |
| Edit display name and profile | no | no | no | no | no | no | Yes | Assist |
| View analytics | no | no | no | No (SLA tile only) | No (SLA tile only) | Yes | Yes (all campuses) | Aggregate |
| View cost and set budget | no | no | no | no | no | View | Yes | Aggregate |
| Record or import opt-ins | no | no | no | Yes | Yes | Yes | Yes | no |
| Clear "Disputed" number flag | no | no | no | Yes | Yes | Yes | Yes | no |
| Export transcripts | no | no | no | no | no | Yes (audit) | Yes (audit) | no |

### Proposed flags

| Flag | Meaning |
|---|---|
| ch.whatsapp.alerts | School-initiated WhatsApp templates per audience, separate from the conversational bot |
| ch.whatsapp.upi_pay | UPI fee payment inside the chat (admin toggle "UPI fee payments in chat") |
| ch.whatsapp.payslip | Payslips on WhatsApp behind the PIN (admin toggle "Payslips on WhatsApp") |
| ch.whatsapp.admissions | Admissions enquiries on WhatsApp (admin toggle "Admissions enquiries") |
| ch.whatsapp.handover | Handover to front office or HR and the agent inbox |
| ch.sms | SMS as a last fallback for Urgent alerts and staff without the app |
