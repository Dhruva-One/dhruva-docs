# 9. Cross-cutting Platform Requirements

Area code: XCT. All sample names, numbers and dates come from the designs (sample date Fri 9 Oct 2026; sample groups DPS Group and Saraswati Vidya Niketan, Karnal) and are illustrative.

## 9.1 Purpose, scope and out-of-scope

This section defines the platform services that every role and module relies on: the notifications engine, the approvals engine, the audit trail, reports and exports, the calendar and notices service, search, file handling, integrations, tenancy and data isolation, the canonical data model, data protection, security, non-functional targets, environments and release management, analytics, support and operations, and data import and campus onboarding.

Tagging reminder: `[Design]` is behaviour shown in the designs or inventories; `[Spec]` is added by this specification because the product needs it. Every `[Spec]` figure (retention periods, SLAs, RPO/RTO, rate limits) is an assumption for sign-off, not a client decision.

In scope: behaviour that is shared by two or more areas, plus the platform rules each module must obey.

Out of scope (covered elsewhere):
- Sign-in, OTP, profiles, PIN and biometrics: Section 3 Identity (IDM).
- Ask Dhruva and all AI behaviour: Section AI.
- Per-module business rules (fees, payroll, exams and so on): their own sections. This section only defines the shared mechanisms they use.
- Feature-flag mechanics and tenant administration screens: Section TFC. XCT requirements name flags; TFC defines how flags are switched.
- WhatsApp conversation design: Section WAB. XCT defines delivery, templates and opt-in rules only.
- Not in the MVP per the project scope: health records, library, hostel, CCTV feeds, RFID and GPS hardware integrations. They appear here only as "later".

## 9.2 Actors and roles

| Actor | Interest in this section |
|---|---|
| Group owner, trustee (standalone) | Approvals above campus limits, group roll-ups, read-only payroll and refund log (trustee), scheduled reports |
| Principal, school admin | Approvals queue (bell), campus reports, notices, audit view for the campus |
| HoD, academic coordinator, exam cell | Approvals they own (team leave, timetable, papers) |
| Teachers, HR, finance, front office, transport, security and IT, counsellor, bus attendant | Receive notifications, raise approval requests, upload files, use search |
| Parents and students | Notification settings, quiet hours, consent, data requests |
| Onboarding lead (campus) | Data sheets and import |
| Tenant platform administrator (DhruvaOne staff) | Environments, releases, tenant onboarding, support, breach process |
| Grievance Officer (grievance@dhruvaone.in) | Data-subject requests and complaints |
| Dhruva (assistant) | Prepares drafts and suggestions only; never approves |

## 9.3 Functional requirements

### Notifications engine

The notifications engine turns events from every module into messages on the right channel at the right urgency. Its guiding rule from the designs is "calm": most things are silent and grouped, and only safety interrupts a night. [Design] AppNotifications board, "Rules that keep it calm".

**XCT-NTF-001 · Must · MVP · flag: core · [Design]**
The system shall classify every notification into one of three tiers: Urgent, High or Normal.
- Acceptance: Given an event is raised When the engine routes it Then it carries exactly one tier from the catalogue in Annex 9-A (Notification event table).
- Rules: Urgent breaks quiet hours and repeats once after 5 minutes if unread. High shows a banner during school hours and waits overnight. Normal is silent and grouped.

**XCT-NTF-002 · Must · MVP · flag: core · [Design]**
The system shall hold quiet hours from 9 pm to 7 am by default and release held items at 7 am.
- Acceptance: Given a High notification at 9:40 pm When quiet hours apply Then no banner or sound is produced and the item is delivered at 7:00 am.
- Rules: Parents can change their quiet hours (Notification settings, "Quiet hours · 9:00 pm to 7:00 am · Alerts wait until morning"). The designs show 6 am in two places; see Open questions OQ-1.

**XCT-NTF-003 · Must · MVP · flag: core · [Design]**
The system shall always deliver safety alerts and early-pickup requests through quiet hours, and the user shall not be able to turn them off.
- Acceptance: Given a parent opens Notification settings When they tap the locked toggle "Urgent safety alerts still come through" Then the toast reads "Safety alerts can't be turned off" and the setting is unchanged.
- Rules: Safety alerts cover bus breakdown, early closure, emergencies, gate incidents and early pickups.

**XCT-NTF-004 · Must · MVP · flag: ch.mobile_ios, ch.mobile_android · [Design]**
The system shall map notifications to Android channels "Safety", "Fees", "Bus", "School updates" and "Messages", and use iOS Time Sensitive for Urgent only.
- Acceptance: Given an Android user mutes the "Fees" channel in system settings When a fee reminder is sent Then it is silent on that device and still appears in the in-app notification centre.
- Rules: The "Safety" channel cannot be shipped as mutable by default; the app shall prompt the user if it is muted at system level [Spec].

**XCT-NTF-005 · Must · MVP · flag: core · [Design]**
The system shall deliver every notification to the in-app notification centre, with unread state, filter chips and "Mark all read".
- Acceptance: Given five unread items When the user taps "Mark all read" Then the badge shows 0 and the title shows no unread count. Filter chips are "All", "Unread · N", "Fees", "Bus", "Messages", "School".
- Rules: "School" covers attendance and notices. The inbox is per profile; the bell on a profile shows the count of items needing attention in the other profiles, and "All alerts" lists them labelled by school (see Section 3 Identity, profile switching).

**XCT-NTF-006 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall send fee and early-pickup alerts to WhatsApp when the push notification has not been opened within 30 minutes.
- Acceptance: Given a fee alert pushed at 8:30 am and unopened When 9:00 am is reached Then a WhatsApp message is sent to the parent's registered number and no further WhatsApp copy is sent for that alert.
- Rules: Applies to fees and pickups only. Governed by the setting "WhatsApp if push is not opened". WhatsApp copies of fees and attendance in English or Hindi are a separate parent toggle ("WhatsApp copy").

**XCT-NTF-007 · Must · MVP · flag: ch.sms · [Design]**
The system shall use SMS for gate-safety alerts only, always on and locked for parents.
- Acceptance: Given a gate incident is raised When the parent has push unreachable or unopened Then an SMS is sent. SMS is never used for fees, marketing or notices.
- Rules: A separate "SMS if the app is offline" toggle (bus and safety only, default off) is shown in the Notification settings board; its relation to the locked "SMS for gate safety" is open (OQ-2). SMS OTP for sign-in is governed by Section 3 Identity.

**XCT-NTF-008 · Must · MVP · flag: core · [Design]**
The system shall never send promotional content, and students from Class 6 upwards shall receive homework and results only.
- Acceptance: Given any notification template is created When it is not in the allowed-purpose list (transactional, safety, academic, administrative) Then it cannot be activated.
- Rules: The school decides who may send notices (see XCT-CAL-004). "No marketing, ever."

**XCT-NTF-009 · Must · MVP · flag: core · [Spec]**
The system shall group Normal-tier notifications into batches and apply per-recipient frequency caps.
- Acceptance: Given a parent has 6 Normal notifications within 15 minutes When delivery runs Then they appear as one grouped item per type (for example "Vivaan: 3 updates") and at most 5 High-tier banners per day are shown.
- Rules: Urgent and safety items are never batched or capped. Caps are configurable per tenant within TFC limits.

**XCT-NTF-010 · Must · MVP · flag: core · [Design]**
The system shall let each user set what they receive.
- Acceptance: Given the parent opens Settings > Notifications Then the sections are "WHAT YOU GET" (Fees and receipts, Attendance, Bus and pickups, Exams and results, Teacher messages, School notices), "QUIET HOURS", "HOW IT REACHES YOU" (Push notifications, WhatsApp if push is not opened, SMS for gate safety) and "LANGUAGE" (English or हिन्दी).
- Rules: Staff see the toggles relevant to their role. Language is chosen at sign-in and may be changed here. Numbers and dates stay the same in both languages.

**XCT-NTF-011 · Must · MVP · flag: core · [Design]**
The system shall make every notification tappable to a specific target and show action buttons on Android where designed.
- Acceptance: Given the lock-screen alert "Bus 7 is 10 minutes away" When the parent taps it Then the live map opens; Android shows "Track" and "Mute today".
- Rules: Action buttons shown in the designs: Track, Mute today (bus); Pay now, Remind me (fee); Accept, Swap (cover); Mark now (attendance); Assign, Later (cover for admin); Review (leave); Remind, Later (principal banner). A tapped target for a profile that is not active shall first switch profile (unlocking with PIN or biometrics for staff profiles).

**XCT-NTF-012 · Must · MVP · flag: core · [Spec]**
The system shall track delivery state per notification per channel: created, queued, sent, delivered, opened, failed, expired.
- Acceptance: Given a notice is sent to 2,976 staff When the owner opens it Then "Read by 2,690 of 2,976 · 90%" is computed from app read receipts, with WhatsApp delivery reports shown as a separate figure.
- Rules: Failures retry with back-off up to 3 times within 30 minutes (Normal) or 5 times within 10 minutes (Urgent). Permanent failures (invalid number, opted out) are recorded and surfaced to the sender.

**XCT-NTF-013 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall send WhatsApp messages only to numbers with recorded opt-in and only using approved templates outside the 24-hour customer-service window.
- Acceptance: Given a parent sends STOP When the next alert is due Then no WhatsApp message is sent and the opt-out is recorded with timestamp.
- Rules: Opt-in is captured at parent onboarding (Week 3) and on first inbound message. "Type STOP at any time to stop school alerts" is shown in the business info sheet [Design].

**XCT-NTF-014 · Should · MVP · flag: ch.email · [Spec]**
The system shall send email for payslips, scheduled reports, vendor purchase orders and login invites, and not for urgent alerts.
- Acceptance: Given a payslip is published When the staff member has an email on record Then an email with a link (not an attachment of the PDF) is sent.
- Rules: Email carries no marketing and no sensitive balances in the body.

**XCT-NTF-015 · Must · MVP · flag: core · [Spec]**
The system shall de-duplicate and suppress obsolete notifications.
- Acceptance: Given an "attendance not marked" alert is queued When the teacher marks attendance before delivery Then the alert is cancelled and logged as "suppressed: resolved".
- Rules: A fee-due alert is suppressed after payment. A "decision waiting" alert shows the current count, not each decision.

**XCT-NTF-016 · Must · MVP · flag: core · [Spec]**
The system shall use child's first name and campus short name in parent-facing text and shall not include full marks, balances or medical or counselling detail on the lock screen when "Hide balances on app switcher" is on.
- Acceptance: Given the privacy toggle is on When a fee notification arrives Then the lock screen reads "October fee due Fri 16 Oct" without the amount.
- Rules: Counselling content is never put in a notification body (see counsellor private notes rule, XCT-PRV-006).

**XCT-NTF-017 · Should · P2 · flag: ai.translation · [Spec]**
The system shall render notification text in the recipient's chosen language (English or Hindi) using approved template translations first and Dhruva translation only for free-text notices after the sender approves.
- Acceptance: Given a notice drafted in English When the sender approves the Hindi version Then Hindi recipients receive the Hindi text and others receive English.
- Rules: Phase 1 per roadmap for Dhruva in Hindi and regional languages; template text in Hindi is MVP.

### Approvals engine

One engine handles every request that needs a person to decide. It is reached from the Approvals tab (owner desktop), the bell (principal), the Reviews tab (HoD), Today lists and WhatsApp for leave. [Design] Owner > Approvals, Principal > bell, HoD > Reviews, Finance > Approvals.

**XCT-APR-001 · Must · MVP · flag: mod.approvals · [Design]**
The system shall provide one approvals queue per approver listing pending requests as cards with requester, context, policy line, and "Approve" and "Decline" actions.
- Acceptance: Given the owner approves the 50% Term 2 concession (Rs 35,600) When they tap "Approve" Then the card reads "Approved · Gurugram Sec 45 notified" and the pending count drops by one.
- Rules: Decline requires a reason of at least 5 characters [Spec]. Approve and Decline are final unless a reopen path exists in the owning module.

**XCT-APR-002 · Must · MVP · flag: mod.approvals · [Design]**
The system shall support the following approval types with the routing in the matrix below.
- Acceptance: Given a request of any listed type When it is submitted Then it routes to the approver given by the tenant's current limits and shows "Above the campus limit" when escalated.
- Rules: Limits are tenant data, copyable between campuses ("Approval limits" in Add a campus), editable only by the owner or trustee.

| Type | First approver | Escalates to | Source |
|---|---|---|---|
| Staff leave up to 2 days outside exam weeks | HoD | Principal if longer or in exam weeks | [Design] HoD > Team leave |
| Staff leave up to 3 days (group) | Principal | Group HR (long leave); group finance head second approver over 3 days | [Design] website copy; Finance board |
| Out on duty | HoD | Principal | [Design] Teacher > Out on duty |
| Fee concession up to Rs 25,000 | Principal | Owner above Rs 25,000 or hardship | [Design] Owner > Approvals |
| Fee refund | Principal (policy "Unused full months, minus 10%") | Owner (sample Rs 42,000, Pune) | [Design] Owner > Approvals |
| New staff post | Principal requests | Owner (sample 2 Maths PGT, Rs 1.1L per month) | [Design] |
| Purchase order up to Rs 50,000 | Finance maker-checker | Principal above Rs 50,000; owner above Rs 5 L | [Design] Finance > Purchases |
| Bill or payment above Rs 2 L | Finance | Principal second approval | [Design] Finance |
| Payroll run | HR prepares | Principal approves | [Design] HR > Payroll |
| Final settlement (exit) | HR calculates | Principal | [Design] HR > Exits |
| Timetable publish | Academic coordinator | None (per class or all) | [Design] AC > Timetable |
| Question papers | Teacher sets | HoD reviews, exam cell moderates, print and seal | [Design] Exam > Papers |
| Early pickup by new person | Parent | None (Urgent) | [Design] |
| Standalone: admin's own leave, salary, fee waivers | Trustee | None | [Design] website copy |

**XCT-APR-003 · Must · MVP · flag: mod.approvals · [Design]**
The system shall enforce maker-checker: a person cannot approve a request they raised.
- Acceptance: Given Mr. Gupta raised PV-0452 When he opens its card Then "Approve" is disabled with "You raised this; another approver is needed" [Spec label].
- Rules: Applies to finance vouchers, payroll, concessions and refunds. A second approver is mandatory where the matrix says so (principal for finance above Rs 2 L).

**XCT-APR-004 · Must · MVP · flag: mod.approvals · [Spec]**
The system shall escalate and remind: a reminder to the approver after 24 hours, a second reminder with a note to the requester after 48 hours, and an offered escalation to the next level after 72 hours.
- Acceptance: Given a leave request is untouched for 24 hours When the timer fires Then the HoD receives a Normal "Decision waiting" notification; at 72 hours the requester sees "Forward to principal".
- Rules: Timers pause on public holidays and at night per quiet hours. Safety and early pickups are not approvals and have their own 5-minute repeat. SLA targets are per tenant defaults; payroll approvals use the pay-date minus 3 days.

**XCT-APR-005 · Must · MVP · flag: mod.approvals · [Spec]**
The system shall support delegation: an approver can nominate a delegate for a date range, and delegation shall not exceed the delegator's own authority.
- Acceptance: Given the principal is on leave 12 to 14 Oct and names the vice-principal When a Rs 30,000 concession is raised Then it shows in the delegate's queue labelled "On behalf of Ms. Mehra".
- Rules: Items above the delegator's limit still go up. A delegate cannot approve their own requests. Delegation is logged and visible to the owner. "In charge while you are away" on leave forms is a cover nomination, not an approval delegation [Design].

**XCT-APR-006 · Must · MVP · flag: mod.approvals · [Design]**
The system shall record every decision with who, when, decision, reason, policy applied and Dhruva's preparatory note.
- Acceptance: Given any approval is decided When the record is saved Then the requester is told (for example "Approved · Mr. Anil Sharma is told") and the entry appears in the audit trail.
- Rules: A trustee sees the payroll log and refund log read-only [Design].

**XCT-APR-007 · Must · MVP · flag: mod.approvals · [Design]**
Dhruva shall prepare a summary on each approval card ("DHRUVA CHECKED") and a person shall make the decision.
- Acceptance: Given a bill has a rate mismatch When the card is opened Then the note reads for example "Bill and goods receipt match. Rate is 4% above the PO" and Approve remains a manual action.
- Rules: With ai.* flags off, the card shows the raw facts without the note.

**XCT-APR-008 · Should · MVP · flag: mod.approvals · [Design]**
The system shall support bulk "Approve all" only for Normal-risk items of the same type below a configured amount.
- Acceptance: Given five payments of Rs 62,000 or less When "Pay all 5" is tapped Then each shows Paid and the toast reads "5 payments scheduled · TDS deducted · vouchers sent to Tally".
- Rules: Items needing a second approver are excluded from bulk actions [Spec].

**XCT-APR-009 · Must · MVP · flag: mod.approvals · [Spec]**
The system shall lock a request after decision and allow edits only by creating a new version linked to the original.
- Acceptance: Given a concession is approved When the principal edits the amount Then a new request is created and the original remains in history.
- Rules: Month lock in finance: changes to a closed month need the principal [Design].

**XCT-APR-010 · Should · P2 · flag: mod.approvals · [Design]**
The system shall support purchase and capital approvals beyond the MVP examples, for example "STEM Lab Rs 18.5 L" shown on the principal lock screen.
- Acceptance: Given a capex request above Rs 5 L When raised Then it routes to the owner.
- Rules: Phase 2 per the roadmap; the prototype shows it now (phasing to confirm).

### Audit trail

**XCT-AUD-001 · Must · MVP · flag: core · [Design]**
The system shall log every create, change, delete, approval, export, login, profile switch and permission change.
- Acceptance: Given any record is edited When saved Then an entry records actor profile, tenant, campus, entity, field-level before and after values, timestamp (UTC with IST display), channel and request ID.
- Rules: "100% of changes in an audit trail." Dhruva actions are logged with the human who approved them as actor and "Dhruva" as origin.

**XCT-AUD-002 · Must · MVP · flag: core · [Spec]**
The audit log shall be append-only and tamper-evident.
- Acceptance: Given a user with any role including platform administrators When they attempt to edit or delete an audit entry Then the operation is refused and the attempt is itself logged.
- Rules: Entries are hash-chained per tenant per day; a daily integrity check runs and alerts on mismatch.

**XCT-AUD-003 · Must · MVP · flag: core · [Spec]**
The system shall retain audit entries for 8 years for financial and payroll events and 3 years for other events, then archive or delete.
- Acceptance: Given an entry older than its period When the retention job runs Then it is moved to cold archive; deletion needs approval by the tenant owner and platform lead.
- Rules: Assumption for legal review; Indian statutory periods for accounts differ by Act.

**XCT-AUD-004 · Must · MVP · flag: core · [Spec]**
The system shall restrict audit viewing: principals see their campus; owners and group admin see all campuses in their group; trustees see only the payroll and refund log; others see the history of records they own.
- Acceptance: Given a teacher opens a student's record When they view "History" Then they see only changes to fields they are allowed to see.
- Rules: Counsellor private notes are never exposed in history to others; only "note added" with no content.

**XCT-AUD-005 · Should · MVP · flag: mod.audit_export · [Design]**
The system shall let authorised users search the audit log and export it in CSV or PDF.
- Acceptance: Given the owner filters by approval type and month When they export Then a file is produced and the export itself is logged. "Audit exports for business customers" is a website claim.
- Rules: Export shows names, not internal IDs; limit of 100,000 rows per export, larger requests run in the background and arrive by email link [Spec].

**XCT-AUD-006 · Must · MVP · flag: core · [Design]**
Module screens shall show human-readable history lines where designed.
- Acceptance: Given a HR record is opened for editing Then the banner reads "Record opened for editing · changes are logged". Finance shows a running "Audit trail" of recent actions such as "Mr. Sanjay Gupta approved PV-0452 · Sunrise Facility Services · Rs 1,46,000 · Thu 5:40 pm". Calls on admissions family records show time and note.
- Rules: No dedicated audit-log screen is designed for the MVP; AUD-005 defines one (see Open questions).

### Reports and exports

**XCT-RPT-001 · Must · MVP · flag: mod.reports · [Design]**
The system shall provide a library of ready-made reports, each with title, description, source and format, and Download and Email actions.
- Acceptance: Given the owner opens Reports Then ten reports are listed (see table) and every number matches what is shown on screen.
- Rules: Principal Reports tab has 8 ready-made reports; finance has eight report cards (Day Book, Profit and Loss, Balance Sheet, Ledger Report, Voucher List, Tarij Report, Operational Report, MIS Report).

| Owner report | Format | Source |
|---|---|---|
| Monthly group summary (board pack) | PDF | All modules |
| Attendance summary (campus x grade x section) | Excel | Class registers |
| Fee collection and dues ageing (30/60/90) | Excel | Fee ledger |
| Defaulters with accountant notes (over 60 days) | Excel | Fee ledger and notes |
| New admissions 2026-27 (admission fee paid) | Excel | Fee ledger |
| Enquiries and walk-ins 2027-28 | Excel | Front-office registers |
| Unit test and term results | PDF | Marks |
| Enrolment, gender and RTE ("Ready for the UDISE+ return") | Excel | Student register |
| Staff strength and leave register | Excel | HR and leave |
| Campus scorecard | PDF | All modules |

**XCT-RPT-002 · Must · MVP · flag: mod.reports · [Design]**
The system shall let the user choose campus, period and format for a report and then download it.
- Acceptance: Given Campus "All campuses", Period "This month", Format "Excel" When they tap "Download Excel" Then a file downloads and the toast reads "<Report> (<campus>, <period>) downloaded as Excel".
- Rules: Period chips are report-specific (This month, Last month, This term). Campus scope is limited by role (principal: own campus).

**XCT-RPT-003 · Must · MVP · flag: mod.reports · [Design]**
The system shall email a report once or on a schedule (Every Monday, 1st of each month).
- Acceptance: Given recipients "Me" and "Group CFO" and frequency "Every Monday" When "Schedule · Every Monday" is tapped Then the toast reads "Scheduled · first email Mon 12 Oct, 8 am" and "Scheduled emails · 2 active" updates.
- Rules: "Stop" cancels with "Stopped · <report>". "All 14 principals" counts as 14 recipients. An invalid address shows "Check the email address". The button reads "Pick who gets it" until a recipient is chosen.

**XCT-RPT-004 · Must · MVP · flag: mod.reports · [Spec]**
The system shall apply row-level security at report generation and shall log every export.
- Acceptance: Given a campus accountant requests a group report When generated Then only their campus rows appear.
- Rules: Reports containing student personal data are watermarked with requester and time; scheduled reports run as the schedule owner and stop if that user loses access.

**XCT-RPT-005 · Must · MVP · flag: mod.reports · [Design]**
The system shall prepare the UDISE+ enrolment, gender and RTE report as an Excel file from the student register, and the CBSE registration export as a file for upload to the CBSE portal.
- Acceptance: Given the principal taps Download on "Enrolment, gender and RTE" Then the toast reads "Enrolment, gender and RTE downloaded for UDISE+ (Excel)".
- Rules: No direct portal submission in the MVP. UDISE+ code is 11 digits and held on the campus profile.

**XCT-RPT-006 · Should · MVP · flag: mod.reports · [Spec]**
Large reports shall generate in the background and notify when ready; PDFs shall embed tenant name, campus, generated time and "numbers as of" timestamp.
- Acceptance: Given a report over 20,000 rows When requested Then the user sees "We will tell you when it is ready" and receives a notification with a link valid for 24 hours.
- Rules: Download links are signed and single-tenant.

### Calendar and notices service

**XCT-CAL-001 · Must · MVP · flag: mod.calendar_ptm · [Design]**
The system shall provide a calendar with types Exam, Holiday, PTM and Event, a campus filter ("All 14 campuses" or one) and add-event.
- Acceptance: Given the owner adds an event for two campuses When saved Then it shows in both campus calendars in the Event colour.
- Rules: Group holiday calendar can be copied into a new campus; campus principals may add campus events; group events are owner only. Exam events are checked by date sheets for clashes [Design, Exam cell].

**XCT-CAL-002 · Must · MVP · flag: mod.calendar_ptm · [Design]**
Calendar events shall feed other modules: exam dates, holidays (Diwali break 7 to 11 Nov, reopening 12 Nov), PTM slots, rollout dates.
- Acceptance: Given a holiday is added When attendance is due Then no "not marked" alert fires that day.
- Rules: Holidays pause approval timers (XCT-APR-004).

**XCT-CAL-003 · Must · MVP · flag: mod.notices · [Design]**
The system shall provide notices with audience selection, channel selection (App, WhatsApp), read receipts and delivery reports.
- Acceptance: Given the owner picks Campuses "All 14", Who "Principals", writes title and message When "Send" is tapped Then the toast reads "Sent to 14 people" and the history shows "14 of 14 · 100%" as reads arrive. The button reads "Add who, title and message" until complete.
- Rules: Modes are "Group" and "One-to-one". Both channels are ticked by default. "Read receipts from the app · delivery reports from WhatsApp Business".

**XCT-CAL-004 · Must · MVP · flag: mod.notices · [Spec]**
The system shall permit sending notices only to roles and audiences the sender is allowed to reach, as configured by the school.
- Acceptance: Given a teacher tries to send to all parents Then the option is absent; they can send only to their classes.
- Rules: Matrix in Annex 9-A. Students from Class 6 receive no notices outside homework and results (XCT-NTF-008).

**XCT-CAL-005 · Should · MVP · flag: ai.notice_drafts · [Design]**
Dhruva shall offer drafts ("Exam arrangements", "Fee collection", "Diwali wishes") that the sender must edit or approve before sending.
- Acceptance: Given a draft button is tapped Then the toast reads "Dhruva drafted it · edit before sending" and nothing is sent until "Send".
- Rules: One-to-one drafts address the chosen person by name.

**XCT-CAL-006 · Should · MVP · flag: mod.notices · [Spec]**
Notices shall support attachments (PDF, image) up to 10 MB, scheduled sending, and withdrawal within 15 minutes of sending (withdrawn notices disappear in-app; WhatsApp copies cannot be recalled and the sender is told).
- Acceptance: Given a scheduled notice for 8 am When the sender cancels at 7:50 am Then no message is sent.
- Rules: Withdrawal is logged.

### Search

**XCT-SRC-001 · Should · MVP · flag: mod.global_search · [Spec]**
The system shall provide search across people, classes, notices and records the user is permitted to see, opened by Ctrl + K on desktop and a search field on mobile.
- Acceptance: Given a principal types "Kabir" When results show Then only students at their campus appear, grouped by type, in under 1 second for the 95th percentile.
- Rules: Ctrl + K already switches school on teacher and parent web [Design]; search results include "Switch to <school>" entries for that shortcut. Minimum 2 characters.

**XCT-SRC-002 · Must · MVP · flag: core · [Spec]**
Search shall enforce the same permission checks as the owning module and shall not reveal the existence of records the user cannot open.
- Acceptance: Given a teacher searches a student of another section Then the student does not appear.
- Rules: Search of counsellor notes, payroll and medical-like data is disabled except for authorised roles. Mobile numbers are masked in results unless the role allows full view.

**XCT-SRC-003 · Could · P2 · flag: ai.assistant_chat · [Design]**
Ask Dhruva shall answer questions from records with source lines, using the same permission layer as search (see Section AI).
- Acceptance: Given the owner asks "Why is Gurugram attendance low?" Then an answer shows the records used.
- Rules: "Dhruva never guesses. Every answer shows which records it used."

### File and document handling

**XCT-FIL-001 · Must · MVP · flag: core · [Spec]**
The system shall store files (receipts, payslips, question papers, mark-sheet photos, staff documents, notice attachments, profile photos, data sheets) in tenant-isolated storage with an access check on every download.
- Acceptance: Given a link to a payslip is shared Then it fails for any other user and expires after 15 minutes.
- Rules: Links are signed, short-lived and single-purpose.

**XCT-FIL-002 · Must · MVP · flag: core · [Spec]**
The system shall scan every uploaded file for malware before it becomes available and reject files that fail.
- Acceptance: Given a file with a virus signature is uploaded Then it is quarantined, the uploader sees "This file could not be accepted" and an alert is raised to the platform team.
- Rules: Allowed types: PDF, JPG, PNG, HEIC, XLSX, CSV, DOCX; maximum 10 MB each (data sheets 25 MB); executable and archive types are refused.

**XCT-FIL-003 · Must · MVP · flag: mod.marks_results · [Design]**
The system shall accept photos of mark sheets and registers from the app and WhatsApp, keep the original for 90 days for correction, and then delete the image unless the school opts to retain it.
- Acceptance: Given a teacher snaps a mark sheet When read Then "Dhruva read 36 marks from the photo · 2 need a look" appears and the original is linked to the record.
- Rules: The 90-day period is [Spec]. Photo reading is flagged as prototype-only in design status, see Section AI.

**XCT-FIL-004 · Must · MVP · flag: mod.fees · [Design]**
Fee receipts shall be generated per payment with a unique receipt number (for example RV-10388), stored as PDF, sent on WhatsApp and in-app, and be reversible only by a logged reversal.
- Acceptance: Given a UPI payment of Rs 14,600 completes Then the receipt arrives in the inbox ("Paid Rs 14,600 by UPI. Receipt sent here and on WhatsApp.") and on WhatsApp.
- Rules: Receipts are retained 8 years [Spec]. A bounced cheque reverses the receipt and adds a Rs 500 charge [Design].

**XCT-FIL-005 · Must · MVP · flag: mod.exams · [Design]**
Question papers shall be versioned, watermarked per reviewer ("HoD review copy") and accessible only to the chain teacher, HoD, exam cell, and the strongroom log.
- Acceptance: Given a paper is sealed Then its content is locked and visible only to the exam cell until the exam date.
- Rules: The strongroom log records seal and release with person and time [Design]. Access to papers before exam start is logged and alerted [Spec].

**XCT-FIL-006 · Must · MVP · flag: core · [Spec]**
The system shall apply retention by file class and delete or archive on schedule.
- Acceptance: Given the retention table is configured Then the nightly job applies it and logs counts.
- Rules: Table in 9.4.

### Integrations

**XCT-INT-001 · Must · MVP · flag: mod.fees · [Design]**
The system shall integrate with a payment gateway (UPI, cards, net banking; the finance design names Razorpay) using the school's own gateway account, with webhooks verified by signature and settlement reconciliation including fee and GST split.
- Acceptance: Given the gateway confirms payment When the webhook arrives Then the receipt is issued once even if the webhook is delivered twice.
- Rules: No card data is stored (PCI DSS handled by the gateway). Idempotency key per payment [Spec]. Fee payments go to the "Campus bank account" or "Group account" as chosen in the go-live plan.

**XCT-INT-002 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall use the WhatsApp Business Platform with a number set up with the school (group number or campus's own number), approved templates, and delivery reports.
- Acceptance: Given the Go-live plan chose "Campus's own number" Then outbound messages use that sender.
- Rules: Behaviour of conversations: Section WAB.

**XCT-INT-003 · Must · MVP · flag: core · [Design]**
The system shall send SMS (OTP and gate safety), push (APNs and FCM) and email through replaceable provider adapters.
- Acceptance: Given the primary SMS provider returns a failure When retry limits are reached Then the secondary provider is used [Spec].
- Rules: Providers are listed as sub-processors.

**XCT-INT-004 · Should · MVP · flag: mod.tally_sync · [Design]**
The system shall sync with TallyPrime: vouchers pushed, ledgers, vendors and cost centres pulled, every 30 minutes and on demand, with ledger mapping, voucher counts, sync log and failed vouchers each with a suggested fix.
- Acceptance: Given the connector is online When "Sync now" is tapped Then the last-sync time updates and failed vouchers list a reason and fix.
- Rules: Phasing (MVP daily export versus two-way sync in Phase 1) to be confirmed with the client (OQ-4). Tally company is per campus, for example "DPS Gurugram Sec 45 (2026-27)"; closed year is view-only.

**XCT-INT-005 · Should · MVP · flag: mod.bank_recon · [Design]**
The system shall import bank statements: HDFC and ICICI daily feeds, SBI by statement upload, then auto-match, review, post and close with a BRS.
- Acceptance: Given the statement for 12 Sep is imported Then matched lines show with suggested matches for unmatched lines.
- Rules: Ignore and Hold post nothing. The ICICI salary-account bank file is generated for payroll [Design]; the transfer is a person's action.

**XCT-INT-006 · Should · MVP · flag: ch.desktop_web · [Design]**
The system shall import spreadsheets (CSV and Excel) as described in 9.3 Data import.
- Acceptance: See XCT-IMP-001.
- Rules: As above.

**XCT-INT-007 · Could · P2 · flag: mod.open_api · [Design]**
The following are "later" only and shall not be built for the MVP: bus GPS (pilot Phase 1, all buses Phase 2), RFID and face gates (Phase 2), biometric attendance import (Phase 1), CCTV links (Phase 2), Google and Microsoft sign-in (idm.sso, later), open APIs (Phase 2).
- Acceptance: Given a tenant admin looks at integrations Then these appear as "Coming later" and cannot be enabled.
- Rules: Website tiles list GPS, biometric and Tally; they are marketing claims to confirm.

### Tenancy and data isolation

**XCT-TEN-001 · Must · MVP · flag: core · [Design]**
The system shall support two tenant types: group (several campuses) and standalone school, with a standalone school's data completely separate from every other tenant.
- Acceptance: Given a parent has children at DPS Gurugram and at Saraswati Vidya Niketan When they switch profile Then no data crosses; only the phone number links the profiles.
- Rules: "Not part of DPS Group, so its fees, staff and records are kept in a completely separate space."

**XCT-TEN-002 · Must · MVP · flag: core · [Spec]**
Every business table shall carry tenant_id and campus_id and every query shall be filtered by them in the data layer (row-level security), not only in application code.
- Acceptance: Given an automated test runs every API as a user of campus A When it requests campus B IDs Then each returns 404 or 403 and none returns data.
- Rules: Platform staff access to tenant data is by time-boxed support grants only, logged and visible to the tenant.

**XCT-TEN-003 · Must · MVP · flag: core · [Design]**
Campus data shall be separate within a group: "Fees, circulars and teachers here belong to the Noida campus only."
- Acceptance: Given a Noida accountant searches a Gurugram student Then nothing is found.
- Rules: Group roles (owner, group CFO, group HR head) have defined cross-campus scope (below).

**XCT-TEN-004 · Must · MVP · flag: mod.group_scorecard · [Design]**
The system shall compute the group scorecard from campus data: six measures (health score, attendance, fees, new students, enquiries, walk-ins) sorted lowest health first, with colours Strong (teal), Fine (blue), Watch (amber), Act now (red) and a dashed 92% attendance target line.
- Acceptance: Given the owner opens Campuses Then "Campuses on track: 12 of 14" and each row opens the campus. New students count only students whose admission fee is received (3,824 for 2026-27).
- Rules: The owner cannot change campus data directly. Roll-ups are aggregates only; row-level student data is not exposed to the owner outside approved reports. Aggregates refresh at least every 15 minutes [Spec]; the "as of" time is shown.

**XCT-TEN-005 · Must · MVP · flag: core · [Spec]**
Cross-campus rules: a person may hold different roles at different campuses as separate profiles; transfers of a student between campuses create a transfer record and copy the academic history, with fees ledger closed at source and opened at destination.
- Acceptance: Given a student moves from Noida to Gurugram When the transfer is approved by both principals Then history is visible at Gurugram and the Noida record becomes read-only.
- Rules: Student transfer flow detail is not designed (OQ-6).

**XCT-TEN-006 · Must · MVP · flag: mod.profile_switching · [Design]**
A profile shall be defined as (phone number, tenant, role) and a user's staff and parent profiles shall never mix; a staff member's own children shall not appear in the staff profile.
- Acceptance: Given Neha is teacher and parent When in the teacher profile Then no child of hers is listed.
- Rules: See Section 3 Identity.

### Data protection and privacy

All items in this block are **[Spec] requirements that need legal review** before sign-off. They reflect the Digital Personal Data Protection Act 2023 and its Rules as understood at drafting; the designs state only the roles and promises in the Trust page copy (school as data fiduciary, DhruvaOne as processor, parental consent per child under 18, grievance contact).

**XCT-PRV-001 · Must · MVP · flag: core · [Spec]**
The system shall record verifiable parental consent for every child's data before the child's profile is activated for any parent-facing service.
- Acceptance: Given a parent is invited When they first open the app Then they see the consent notice for each child in English or Hindi and must accept per child; acceptance stores who, when, notice version and mobile number verified by OTP.
- Rules: Children are those under 18. The method of verification (OTP to the parent number on school record, cross-checked with admission records) needs legal review. Without consent the child's data is available to the school only for core school functions the law permits.

**XCT-PRV-002 · Must · MVP · flag: core · [Spec]**
The system shall not track, profile or send targeted advertising to children and shall not sell data.
- Acceptance: Given the analytics pipeline is inspected Then no advertising identifiers, third-party ad SDKs or behavioural profiling of students exist.
- Rules: "No ads or tracking, no sale of student data" per Trust page. Product telemetry of children is limited to aggregate functional events (XCT-ANA-002).

**XCT-PRV-003 · Must · MVP · flag: core · [Spec]**
The system shall collect only the data needed for a stated purpose and publish a purpose table in the privacy notice.
- Acceptance: Given a new field is proposed Then it needs a purpose, a retention period and an owner in the data dictionary before release.
- Rules: Student fields in the MVP: class, section, roll, parent phones, gender, RTE, DOB, address.

**XCT-PRV-004 · Must · MVP · flag: core · [Spec]**
The system shall support data-subject requests (access, correction, erasure, nomination, grievance) raised by parents or staff to the school, approved by the school, and fulfilled within 30 days.
- Acceptance: Given a parent requests a copy of data When the school approves Then a machine-readable export (JSON and CSV plus PDF summary) is produced and sent securely; the event is logged.
- Rules: Erasure excludes data the school must keep by law (fee ledger, TC records); those are flagged and retained with reason. Requests route to the Grievance Officer (grievance@dhruvaone.in) and the school's principal or admin.

**XCT-PRV-005 · Must · MVP · flag: core · [Spec]**
The system shall delete or anonymise a tenant's personal data within 90 days after exit and give written confirmation.
- Acceptance: Given a tenant leaves When 90 days pass Then data and backups beyond the backup cycle are purged and a confirmation is issued with date and scope.
- Rules: "Deletion 90 days after exit with written confirmation" per Trust page. A data export in open formats is provided before deletion.

**XCT-PRV-006 · Must · MVP · flag: mod.counselling · [Design]**
Counsellor session notes shall be private to the counsellor; no other role, including the principal, can read them, and they shall not appear in notifications, search or audit detail.
- Acceptance: Given the principal searches a student's name Then counselling notes never appear; only the referral state shows where the design allows.
- Rules: Sudden-change cases pass from teacher to counsellor as referrals, not as notes.

**XCT-PRV-007 · Must · MVP · flag: core · [Spec]**
The system shall maintain a breach process: detect, contain, assess, notify the school (fiduciary) within 24 hours of confirmation, and support notice to the Data Protection Board and affected persons as required.
- Acceptance: Given a breach is confirmed Then the platform lead opens an incident, the school's owner or admin is notified in writing within 24 hours, and a timeline is kept.
- Rules: Statutory timelines are for legal review. Post-incident review within 10 working days.

**XCT-PRV-008 · Should · MVP · flag: core · [Spec]**
The system shall show "About Dhruva · How your data is used" explaining what Dhruva reads and that it never changes records or messages families on its own.
- Acceptance: Given the user opens Me > About Dhruva Then the notice is shown with a link to Privacy and Terms.
- Rules: Hide balances on app switcher is a user toggle [Design].

**XCT-PRV-009 · Must · MVP · flag: core · [Spec]**
The system shall not use customer data to train shared AI models unless the tenant agrees in writing; prompts sent to AI providers shall exclude children's direct identifiers where the task allows.
- Acceptance: Given a draft is requested Then names are replaced by tokens in the provider call where the output does not need them.
- Rules: Legal review needed.

### Security

All [Spec] unless noted; targets are assumptions for client confirmation.

**XCT-SEC-001 · Must · MVP · flag: core · [Design]**
The system shall encrypt data in transit (TLS 1.2 or higher) and at rest (AES-256), and keep all data and backups in India.
- Acceptance: Given a scan of public endpoints Then TLS below 1.2 is refused and no plain HTTP is served.
- Rules: Matches the Trust page claims (India region, backups in India).

**XCT-SEC-002 · Must · MVP · flag: core · [Spec]**
Authorisation shall be enforced on the server for every API call by role, tenant, campus and record ownership; UI hiding is never the control.
- Acceptance: Given a parent calls a staff endpoint directly Then the response is 403 and the attempt is logged.
- Rules: Permission matrix in Annex 9-A and per-section matrices.

**XCT-SEC-003 · Must · MVP · flag: core · [Spec]**
The system shall rate-limit sensitive endpoints: OTP request (5 per number per hour, 1 per 30 seconds), OTP verify (5 attempts then 15-minute lock), PIN (5 attempts then forced re-OTP), API (per user and per IP).
- Acceptance: Given the sixth OTP request in an hour Then the response is "Too many attempts. Try again later." and no SMS is sent.
- Rules: OTP is 6 digits and expires in 5 minutes (see Section 3 Identity for the authoritative figure).

**XCT-SEC-004 · Must · MVP · flag: core · [Spec]**
All inputs shall be validated server-side (type, length, range, allow-list) and outputs encoded; uploads follow XCT-FIL-002.
- Acceptance: Given a script is posted in a notice title Then it is stored as text and rendered inert.
- Rules: Parameterised queries only.

**XCT-SEC-005 · Must · MVP · flag: core · [Spec]**
Secrets (provider keys, gateway keys, signing keys) shall be held in a managed secret store, rotated at least yearly or on exposure, and never in code, logs or client apps.
- Acceptance: Given a repository scan runs in CI Then it fails the build if a secret pattern is found.
- Rules: Gateway webhook secrets rotate with a dual-key overlap.

**XCT-SEC-006 · Must · MVP · flag: core · [Design]**
Staff and finance pages shall require PIN or biometrics even when signed in; web re-asks for the PIN after 15 minutes on a staff profile; "Sign out everywhere" shall revoke all device sessions.
- Acceptance: Given a staff profile is idle 15 minutes on the web When the user acts Then the PIN prompt appears.
- Rules: Authoritative detail in Section 3 Identity.

**XCT-SEC-007 · Must · MVP · flag: core · [Spec]**
The platform shall run vulnerability management: dependency scanning on every build, critical fixes within 7 days and high within 30 days, an annual independent penetration test, and a security review before each major release.
- Acceptance: Given a critical advisory is published for a dependency Then a ticket exists within 1 business day and a fix is shipped within 7 days.
- Rules: Annual penetration test is a Trust page claim. No ISO or SOC certification is claimed.

**XCT-SEC-008 · Must · MVP · flag: core · [Spec]**
The platform shall take encrypted daily backups with a tested restore, targeting recovery point of 24 hours maximum (15 minutes for the transactional database via continuous log shipping) and recovery time of 4 hours.
- Acceptance: Given a quarterly restore drill Then a full tenant restore completes within 4 hours and is recorded.
- Rules: Targets are assumptions (OQ-8). "Daily backups with tested restore" is a Trust page claim.

**XCT-SEC-009 · Should · MVP · flag: core · [Spec]**
Staff accounts shall use multi-factor authentication for web access (OTP plus PIN) and finance payment actions shall require PIN or biometrics at the time of approval.
- Acceptance: Given a payment approval is tapped Then PIN or biometrics is requested.
- Rules: SSO for staff is later (idm.sso).

### Non-functional requirements

**XCT-NFR-001 · Must · MVP · flag: core · [Spec]**
The platform shall be available 99.5% monthly during school hours (6 am to 8 pm IST, Monday to Saturday) and 99.0% outside them, excluding announced maintenance.
- Acceptance: Given monthly uptime is measured at the edge Then the reported figure meets the target.
- Rules: Maintenance windows are announced 48 hours ahead and avoid exam days and pay days.

**XCT-NFR-002 · Must · MVP · flag: core · [Spec]**
The platform shall meet the performance budgets in the table below on a mid-range Android phone on 4G.

| Operation | Target (95th percentile) |
|---|---|
| App cold start to Today list | 3 s |
| Screen navigation after load | 1 s |
| Take attendance, submit | 2 s |
| Owner Overview with 14 campuses | 2.5 s |
| Search results | 1 s |
| Push to device (Urgent) | 5 s |
| Report generation up to 20,000 rows | 30 s |
| Bulk import of 5,000 rows validated | 60 s |

**XCT-NFR-003 · Must · MVP · flag: core · [Spec]**
The platform shall scale to the sample load: 14 campuses, 43,240 students, 2,976 staff, with headroom for 3x, and peaks of 10 to 15 minutes at 7:30 to 9:30 am (attendance, bus alerts) and fee due dates.
- Acceptance: Given a load test of 3,000 concurrent teachers marking attendance and 40,000 push alerts in 5 minutes Then budgets in XCT-NFR-002 hold.
- Rules: 4,120 students at the largest sample campus (Gurugram Sec 45) and 1,500 at a large standalone school.

**XCT-NFR-004 · Must · MVP · flag: core · [Spec]**
The platform shall emit structured logs, metrics and traces with a tenant and request ID, and alert on error rate, latency, queue depth, notification failure rate and integration failures.
- Acceptance: Given the Tally connector fails for 60 minutes Then an alert is raised and the finance user sees a failure banner.
- Rules: Logs contain no OTPs, PINs, full phone numbers or counselling content.

**XCT-NFR-005 · Must · MVP · flag: core · [Spec]**
All interfaces shall meet WCAG 2.1 AA: contrast, focus order, labels, text scaling to 200%, touch targets at least 44 pt, and no information by colour alone (colours carry meaning plus text such as "Act now").
- Acceptance: Given an accessibility audit of the top 20 screens Then there are no AA failures at release.
- Rules: The colour meanings teal, blue, amber and red always appear with a label.

**XCT-NFR-006 · Must · MVP · flag: ai.translation · [Design]**
The UI shall be available in English and Hindi (Devanagari) with numbers and dates identical in both; regional languages are Phase 1.
- Acceptance: Given the user selects "हिन्दी" Then all MVP screens and templates render in Hindi without truncation.
- Rules: The bus attendant app is English or Hindi, Hindi first.

**XCT-NFR-007 · Must · MVP · flag: core · [Spec]**
Supported clients: current and previous major versions of Chrome, Edge, Safari and Firefox on desktop; iOS 16 or later; Android 9 or later (including low-memory devices); WhatsApp current version. Attendance and bus-attendant screens shall degrade gracefully on poor networks, with offline queueing as a Phase 1 item.
- Acceptance: Given the phone loses connectivity during attendance Then the app shows "Saved on this phone · will send when online" [Spec label] only after offline mode is delivered; in the MVP it shows a retry message and keeps the entries on screen.
- Rules: Offline mode is on the Phase 1 roadmap.

**XCT-NFR-008 · Must · MVP · flag: core · [Spec]**
Data residency: all production data, backups and logs shall reside in India; sub-processors that process personal data outside India require written tenant consent and legal review.
- Acceptance: Given an architecture review Then no personal data store lies outside India.
- Rules: AI model providers fall under this rule.

### Environments and release management

**XCT-ENV-001 · Must · MVP · flag: core · [Spec]**
The platform shall maintain development, staging (production-like with synthetic data) and production environments; no production personal data shall be copied to lower environments.
- Acceptance: Given a staging refresh Then data is generated or masked (names, phones, addresses replaced).
- Rules: Sample data in the designs is the seed for demos.

**XCT-ENV-002 · Must · MVP · flag: core · [Spec]**
Releases shall be staged: staging verification, canary on the pilot tenant, then batches, with the ability to roll back within 30 minutes; the mobile apps follow store review with a minimum supported version check.
- Acceptance: Given a release causes errors above threshold Then rollback is executed and recorded.
- Rules: No releases on exam days, pay days or the first week of a campus's go-live. Database migrations are backward compatible for one release.

**XCT-ENV-003 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The system shall support tenant and campus onboarding by the owner: the "Add a campus" wizard, rollout batches and the Onboarding tab.
- Acceptance: Given the owner completes Step 6 "Review and add" Then the page "<Campus> is added" shows "<batch> · goes live <date> · n of 8 data sheets already in" and four ticks: Invites sent, Templates sent, Training booked, On the rollout plan.
- Rules: Detail in XCT-IMP series below. Onboarding KPIs: "14 campuses in 5 batches", "18 / 112 data sheets imported", "1 needs a fix".

**XCT-ENV-004 · Should · MVP · flag: core · [Spec]**
The system shall migrate a new academic session (for example 2027-28 from 1 April 2027) through a controlled rollover: carry forward students by promotion rules, close the old account year view-only, reset leave balances per policy, and require principal confirmation.
- Acceptance: Given the principal confirms rollover Then the closed year shows "2025-26 is closed and audited · view only" style locking for the prior session.
- Rules: Phase 1 per roadmap.

### Analytics and product telemetry

**XCT-ANA-001 · Should · MVP · flag: mod.telemetry · [Spec]**
The system shall collect product telemetry for feature use, task completion, errors and performance, to measure roadmap targets (95% of sections mark attendance by 9:30, 70% of parents active monthly, 50% of fees paid online, 90% of test tasks done without help).
- Acceptance: Given the pilot runs Then a dashboard shows these measures per campus daily.
- Rules: Aggregated by campus; no message content.

**XCT-ANA-002 · Must · MVP · flag: core · [Spec]**
Telemetry shall exclude advertising identifiers, third-party trackers and content of student records, and shall carry only pseudonymous user IDs; users can opt out of non-essential telemetry in Settings.
- Acceptance: Given the privacy review Then no student personal data appears in telemetry payloads.
- Rules: Related: XCT-PRV-002.

**XCT-ANA-003 · Should · MVP · flag: mod.group_scorecard · [Design]**
Business analytics shown to customers (scorecard, funnel, attendance, results) shall use the same records as the reports and state the data sources.
- Acceptance: Given the owner opens a number Then the source line is shown (for example "Admission-fee receipts in the fee ledger").
- Rules: No separate analytics store may disagree with module data.

### Support and operations

**XCT-SUP-001 · Must · MVP · flag: core · [Design]**
The app shall provide "Help and support" with "Chat with Dhruva or call the school office", and the school office is the first line of support for end users.
- Acceptance: Given the user opens Me > Help and support Then both options show.
- Rules: With ai.assistant_chat off, only the call option and a help form show.

**XCT-SUP-002 · Must · MVP · flag: core · [Spec]**
DhruvaOne shall run tiered support for school staff: onboarding lead (campus), group admin, then DhruvaOne support with severity targets (S1 outage: respond 30 minutes, 24x7 during go-live; S2: 4 hours; S3: next business day).
- Acceptance: Given an S1 incident Then the status page is updated within 30 minutes.
- Rules: The "20-minute help call" in campus onboarding is part of onboarding, not support [Design].

**XCT-SUP-003 · Should · MVP · flag: core · [Spec]**
The platform shall publish a status page (components: sign-in, app, WhatsApp delivery, payments, Tally connector, reports) with incident history, and notify tenant owners of S1 and S2 incidents.
- Acceptance: Given the SMS provider is degraded Then the page shows "Degraded: sign-in codes" and an owner notice is sent.
- Rules: Systems status of the school's own network is the Security and IT "Systems" screen, not this page [Design].

**XCT-SUP-004 · Must · MVP · flag: core · [Spec]**
Runbooks shall exist for: OTP provider outage, WhatsApp template rejection, payment webhook backlog, Tally sync failure, mass notification storm, tenant data restore, suspected breach, and onboarding import failure.
- Acceptance: Given an on-call engineer opens an alert Then it links to its runbook.
- Rules: Each runbook is reviewed after each incident or at least every 6 months.

### Data import and campus onboarding

Eight data sheets are provided as Excel templates, one set per campus. [Design] Owner > Add a campus > Step 4 "Data sheets" and Onboarding.

| # | Sheet | Sample size in design | Key validation |
|---|---|---|---|
| 1 | Students and parents | 1,180 rows (1,174 fine, 6 missing parent mobile) | Required: name, class, section, parent mobile; no duplicate student; class exists |
| 2 | Staff and leave balances | 86 staff | Required: name, mobile, role; leave balance within annual entitlement |
| 3 | Classes, sections and subjects | 38 sections, 11 subjects | Unique class-section; subject codes |
| 4 | Timetable | 38 section timetables, 8 periods | Teacher and room not double-booked; classes exist |
| 5 | Fee structure and dues | 7 fee heads | Amounts numeric; heads mapped; opening dues per student exist |
| 6 | Transport routes and stops | 9 routes, 74 stops, 412 riders | Every rider is a known student; stop belongs to route |
| 7 | Holiday and exam calendar | 31 events, session 2026-27 | Dates in session; no overlap of exams with holidays |
| 8 | Monthly salary sheet | "First upload due before go-live payroll" | Staff exist; amounts numeric |

The eight sheets match the Add a campus design. The brief lists rooms and subjects as items; the designs have rooms inside the Timetable data (41 rooms and labs in the AC timetable model), and subjects in sheet 3. Rooms are therefore part of sheets 3 and 4.

**XCT-IMP-001 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The system shall let the owner or onboarding lead download all eight templates and upload each sheet or mark it "Send later".
- Acceptance: Given the owner taps "Download all 8 templates" Then the toast reads "8 Excel templates downloaded". Each sheet shows "Upload" and "Send later" (which becomes "Undo"). The counter reads "n of 8 imported · n left for the campus".
- Rules: "Send later" sheets go to the onboarding lead with the template and a 20-minute help call. Continue is blocked with "Upload or 'Send later' each sheet".

**XCT-IMP-002 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The system shall validate every upload before import, showing "Checking..." and a result summary.
- Acceptance: Given the student sheet has 6 rows with no parent mobile Then the result reads "1,174 rows fine · 6 rows have parent mobile numbers missing" with "Fix 6 rows" (toast "6 parent numbers added from the admission forms") or "Import the rest" (1,174 imported, 6 sent to the lead).
- Rules: Dhruva checks for missing phone numbers, duplicate students and non-existent classes.

**XCT-IMP-003 · Must · MVP · flag: mod.campus_onboarding · [Spec]**
The system shall apply the following validation rules and report every failing row with row number, column, reason and a fix hint.
- Acceptance: Given a sheet has errors Then a downloadable error file lists them and no partial import happens unless the user chooses "Import the rest".
- Rules: Mobile is exactly 10 digits, starting 6 to 9; DOB not in the future and age consistent with class (Nursery to Class 12) with a warning not a block; email format; duplicates detected on name plus DOB plus parent mobile; class and section codes must exist in sheet 3 or already in the system; amounts non-negative with two decimals; dates ISO or DD-MM-YYYY; UDISE+ code 11 digits; file under 25 MB and 20,000 rows; character set UTF-8 including Devanagari.

**XCT-IMP-004 · Must · MVP · flag: mod.campus_onboarding · [Spec]**
The sheets shall import in dependency order (3, 1, 2, 4, 5, 6, 7, 8) and a sheet that depends on a missing one shall be held with "Waiting for Classes, sections, subjects".
- Acceptance: Given the timetable is uploaded before classes Then it is held and imports automatically when sheet 3 is complete.
- Rules: Re-uploading a sheet updates matched rows (by natural key) and never deletes records not in the sheet unless the user chooses "Replace all" with confirmation.

**XCT-IMP-005 · Must · MVP · flag: mod.campus_onboarding · [Spec]**
Imports shall be idempotent, reversible within 7 days of the first import (rollback of the batch) and fully audited.
- Acceptance: Given an import batch is rolled back Then records created by it are removed or deactivated, provided no dependent transactions exist, and the rollback is logged.
- Rules: Sheets 5 and 8 are rolled back only before any receipt or payroll run uses them.

**XCT-IMP-006 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The Add a campus wizard shall provide six steps, each with the stated blocker until valid, and "Save and finish later".
- Acceptance: Step 1 needs "Add the name, city and board"; Step 2 needs "Add the principal and onboarding lead with 10-digit mobiles"; Step 3 is always valid; Step 4 needs every sheet uploaded or "Send later"; Step 5 needs "Pick both training dates"; Step 6 "Add campus". "Save and finish later" toasts "Saved <name> as a draft · pick it up from Onboarding".
- Rules: Settings copied: Grading scheme and report-card format, School timings and periods, Fee heads (names only), Group holiday calendar, Approval limits. "Fee amounts are never copied."

**XCT-IMP-007 · Must · MVP · flag: mod.campus_onboarding · [Design]**
The system shall track rollout by batch: go-live date, data sheets, staff trained, parents joined, status, and run the four-week plan (Week 1 data, Week 2 staff training, Week 3 parent onboarding, Week 4 live).
- Acceptance: Given Batch 1 (Gurugram Sec 45, 5 Jan 2027) has 6 of 8 sheets Then the row shows "Needs a fix". Staff accounts are created from the staff sheet; staff invites by SMS and parent invites by WhatsApp and app.
- Rules: Teacher training 45 minutes and accounts training 2 hours on campus.

**XCT-IMP-008 · Should · MVP · flag: mod.campus_onboarding · [Spec]**
The system shall provide a go-live gate checklist per campus: all eight sheets imported, principal and onboarding lead logged in, at least 95% of students with a parent mobile, approval limits set, gateway account verified, WhatsApp number approved.
- Acceptance: Given a campus passes the checklist Then "Ready to go live" shows and the principal confirms.
- Rules: The thresholds are assumptions for sign-off.

## 9.4 Business rules and policies

**Approval limits (tenant data, defaults from the designs).** Concession above Rs 25,000 to the owner; PO above Rs 50,000 to the principal; above Rs 5 L to the owner; finance second approval above Rs 2 L; HoD leave up to 2 days outside exam weeks; principal leave up to 3 days in a group; group HR for long leave.

**Retention defaults [Spec, subject to legal review].**

| Data class | Retention | Then |
|---|---|---|
| Audit log (financial and payroll) | 8 years | Cold archive |
| Audit log (other) | 3 years | Archive |
| Fee receipts and vouchers | 8 years | Archive |
| Student academic record | Life of the student record plus 3 years after leaving; transfer certificate data permanent | Anonymise |
| Attendance records | 5 years | Aggregate |
| Staff records | Employment plus 7 years | Delete |
| Mark-sheet photos and register photos | 90 days | Delete |
| Counselling notes | Per counsellor policy; default 5 years after leaving | Delete with counsellor and principal consent log (principal sees no content) |
| Notification delivery logs | 13 months | Delete |
| Gate and visitor log | 1 year | Delete |
| Product telemetry | 13 months | Aggregate |
| Backups | 35 days | Overwritten |
| Departed tenant data | 90 days after exit | Delete with written confirmation [Design] |

**Other rules.**
- Dhruva drafts; a person approves anything that changes a record or reaches a family (Product principle, see Section AI).
- Module flag off hides and blocks the feature but retains its data; AI flag off leaves the manual path in place.
- Quiet hours and tier rules are not configurable below the safety floor.
- Approvals use tenant limits current at submission time; later limit changes do not alter pending routing unless the approver escalates.
- Reports state "numbers as of" time and use the same records as screens.

## 9.5 Notifications and approvals raised by this section

| Trigger | Recipient | Tier | Notes |
|---|---|---|---|
| Report scheduled email sent | Recipients | Normal (email) | Subject names report and period |
| Report ready (background) | Requester | Normal | Link valid 24 hours |
| Import validation complete | Owner, onboarding lead | Normal | Counts and issues |
| Import "Send later" sheet pending | Onboarding lead | Normal | Template and help-call link |
| Rollout milestone (training booked, invites sent) | Owner, principal | Normal | Part of the success page ticks |
| Consent pending for child | Parent | Normal | Reminder after 3 days, then 7 days |
| Data request raised or due | Principal or admin, Grievance Officer | High | Due in 30 days |
| Integration failure (Tally, bank feed, gateway) | Finance, platform team | High | Per runbook |
| Approval waiting, reminder, escalation | Approver, requester | Normal | XCT-APR-004 |
| Delegation started or ended | Delegate, owner | Normal | |
| Breach confirmed | School owner or admin | Urgent | Written notice within 24 hours |

Approvals raised by this section: audit deletion (platform lead and tenant owner), erasure of legally retained data (principal), import rollback after 7 days (platform lead) and replacement of a whole data sheet ("Replace all", owner or onboarding lead).

## 9.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| core | Sign-in, audit, safety alerts, consent, security | On, not switchable | Cannot be disabled |
| mod.approvals | Approvals queue and routing | On | Off hides queues; requests then follow the module's own manual path |
| mod.notices | Notices composer, read receipts | On | Off keeps history |
| mod.calendar_ptm | Calendar and PTM | On | |
| mod.reports | Report library and schedules | On | Scheduled sends pause, data retained |
| mod.group_scorecard | Group roll-ups | On for groups | Off for standalone |
| mod.campus_onboarding | Add-a-campus and imports | On | Off after all campuses live is allowed |
| mod.tally_sync | Tally connector | Off until confirmed | Phasing open |
| mod.bank_recon | Bank statement import | On for tenants with finance | |
| mod.profile_switching | Profile switcher | On | Section 3 |
| ch.whatsapp | WhatsApp delivery | On | Per sub-flag in WAB |
| ai.notice_drafts, ai.translation, ai.assistant_chat | Drafts and translation | On | Manual path always stays |
| ch.sms | SMS for gate safety | On | Locked for parents |
| ch.email | Email delivery | On | |
| mod.audit_export | Audit search and export | On | Business tier |
| mod.global_search | Search | On | |
| mod.telemetry | Telemetry | On | User opt-out for non-essential |
| mod.open_api | Later integrations listing | Off | Not buildable in MVP |

## 9.7 Non-functional requirements (section-specific)

The platform-wide targets are in XCT-NFR-001 to 008 above. In addition:
- Notification fan-out: Urgent to 95% of recipients within 10 seconds of the event; Normal within 5 minutes [Spec].
- Audit write must be in the same transaction as the change; failure to write blocks the change.
- Search index lag at most 60 seconds.
- Group scorecard computed from pre-aggregated tables, at most 15 minutes stale.
- Import of 20,000 rows completes within 3 minutes.

## 9.8 Open questions

- OQ-1 Quiet hours end at 6 am in the Notification settings and Me screens and at 7 am in AppNotifications, AppInbox and onboarding. This spec uses 9 pm to 7 am as default; client to confirm.
- OQ-2 The Notification settings board shows "SMS if the app is offline" (bus and safety, default off) while AppInbox shows "SMS for gate safety" (always on, locked). Reconcile: this spec keeps SMS for gate safety locked and treats bus SMS as an optional extra.
- OQ-3 The Notification settings board says quiet hours let "only safety alerts and overdue fees" through; the rules board says safety and early pickups only. This spec follows the rules board; overdue fees wait until 7 am.
- OQ-4 Tally sync, bank reconciliation and purchase and inventory phasing (MVP versus Phase 1 and 2) are pending client confirmation.
- OQ-5 Dhruva publishing marks, attendance and learning plans without a teacher review step is flagged unconfirmed; this spec assumes review remains possible and logged.
- OQ-6 Student transfer between campuses and between sessions is not designed.
- OQ-7 No audit-log screen is designed; XCT-AUD-005 defines a minimal one.
- OQ-8 RPO and RTO, uptime and retention figures are assumptions awaiting client and legal confirmation.
- OQ-9 Consent flow and the DPDP Act position (fiduciary versus processor roles, verification method for children's consent, cross-border processing of AI calls) need legal review.
- OQ-10 What "Ask my school to add me" sends is not drawn.
- OQ-11 Web versus app login interpretation and the location of "Switch school" (top chip versus Settings) are unreconciled, see Section 3 Identity.
- OQ-12 Sample claims on the website Trust page (penetration test, MFA for staff, data export) must be confirmed before publishing.
- OQ-13 Whether eight data sheets include rooms: the designs do not list a rooms sheet; rooms are assumed inside Timetable.

---

## Annex 9-A (engineering)

### Data entities

Canonical entities and relationships across areas.

| Entity | Key fields | Notes / relationships |
|---|---|---|
| Tenant | id, type (group, standalone), name, status, region | Root of isolation; has many Campus |
| Campus | id, tenant_id, name, short_name, city, state, board, affiliation_no, udise_code, batch, go_live_date | Belongs to Tenant; owns most records |
| AcademicSession | id, tenant_id, label (2026-27), start, end, status | Closed sessions view-only |
| Person | id, name, mobile, email, language | One per human; many Profile |
| Profile | id, person_id, tenant_id, campus_id, role, status | (phone, tenant, role); parent profile links to children |
| Role / Permission | role, capability, scope | RBAC; scope: self, section, department, campus, group |
| Student | id, campus_id, admission_no, name, dob, gender, rte, class_id, section_id, roll, address, status | Many Guardian |
| Guardian | id, person_id, student_id, relation, mobile, authorised_pickup | Child links created by school office |
| Consent | id, student_id, guardian_id, notice_version, method, timestamp, withdrawn_at | Verifiable parental consent |
| Staff | id, person_id, campus_id, employee_id, role, type (teaching, non-teaching, contract, visiting), payroll_group_id, status | HR record |
| Class / Section / Subject / Room | ids, campus_id, codes, weekly norms | Timetable data model |
| TimetableVersion / Period | id, section_id, day, period, subject, teacher, room, status (draft, approved, live) | Approval per class |
| AttendanceRecord | student_id or staff_id, date, period, status, marked_by, source | Staff includes "On duty" |
| LeaveRequest / OutOnDuty | id, staff_id, type, from, to, in_charge, status, approver | Approval engine |
| Homework / Notes / LessonPlan | ids, class, teacher, status | Teacher area |
| Exam / Paper / Mark / ReportCard | ids, stage (set, review, moderate, sealed), values | Papers chain |
| FeeHead / FeeStructure / Invoice / Payment / Receipt | amounts, due dates, mode, gateway_ref | Receipt number per type |
| Concession / Refund | student_id, amount, policy, status | Approval engine |
| Voucher / Ledger / Vendor / PO / Bill / BankLine | numbers, TDS, status, match | Finance |
| Payroll / PayrollRun / Payslip | group, period, status | HR |
| TransportRoute / Stop / Trip / TripEvent | route, stop, rider, taps | Attendant taps |
| Enquiry / Application / Tour | stage, source, campus | Admissions CRM |
| Referral / Session / Note (counsellor) | private flag | Never shared |
| GateVisit / Job / Asset | status, priority | Security and IT |
| Notice | id, sender, audience, channels, body, status | Read receipts per recipient |
| Notification / DeliveryAttempt | id, recipient profile, event, tier, channel, state, timestamps | Section 9.3 notifications |
| NotificationPreference | profile_id, topics, quiet_start, quiet_end, channels, language | |
| ApprovalRequest / ApprovalStep / Delegation | id, type, entity_ref, amount, requester, approver, status, policy, decision, reason | Approval engine |
| CalendarEvent | id, campus_id, type, start, end, audience | |
| File | id, tenant_id, class, owner_ref, hash, scan_status, retention_until | Storage |
| AuditEntry | id, tenant_id, actor, origin, entity, action, before, after, ts, hash | Append-only |
| ReportDefinition / ReportSchedule / ReportRun | id, owner, params, frequency, recipients | |
| ImportBatch / ImportRow | id, sheet type, status, counts, errors | Reversible |
| Integration / SyncLog | provider, config ref, status | Tally, bank, gateway |
| ConsentOfTelemetry / DataRequest | id, type, status, due | Privacy |
| FeatureFlag / FlagAssignment | key, scope (tenant, campus, role, schedule), value | Section TFC |

### APIs

Paths are indicative. All are tenant-scoped through the session; all return 401 unauthenticated, 403 forbidden, 404 for out-of-scope IDs, 429 when rate-limited.

| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| GET /v1/notifications | List own notifications, filters | Own profile | 401 |
| POST /v1/notifications/{id}/read, /v1/notifications/read-all | Mark read | Own | 404 |
| GET/PUT /v1/notification-settings | Read and update preferences | Own; locked toggles ignored | 422 locked setting |
| POST /v1/devices | Register push token | Own | 422 |
| POST /v1/notices | Create notice | Per sender audience rules | 403 audience, 422 missing title |
| GET /v1/notices/{id}/receipts | Read counts and delivery | Sender, principal, owner | 403 |
| GET /v1/approvals?status=pending | Queue | Approver | |
| POST /v1/approvals | Raise request | Requester role | 422 limit config missing |
| POST /v1/approvals/{id}/decision | Approve or decline | Approver, not requester | 409 already decided, 403 self-approval, 422 reason required |
| POST /v1/approvals/delegations | Create delegation | Approver | 422 exceeds authority |
| GET /v1/audit | Search audit | Per XCT-AUD-004 | 403 |
| POST /v1/audit/exports | Export audit | Owner, principal | 413 too large |
| GET /v1/reports | Library | Role | |
| POST /v1/reports/{id}/runs | Generate | Role, campus scope | 202 background |
| POST /v1/report-schedules, DELETE /v1/report-schedules/{id} | Schedule and stop | Owner, principal | 422 recipients |
| GET/POST /v1/calendar/events | Calendar | Role | 403 scope |
| GET /v1/search?q= | Search | Per record permissions | 422 short query |
| POST /v1/files | Upload (signed URL) | Role | 415 type, 413 size, 422 scan failed |
| GET /v1/files/{id} | Signed download | Owner or role | 403, 410 expired |
| POST /v1/imports, GET /v1/imports/{id}, POST /v1/imports/{id}/rollback | Data import | Owner, onboarding lead | 422 validation, 409 dependency |
| GET /v1/imports/templates | Download 8 templates | Same | |
| POST /v1/campuses, PATCH /v1/campuses/{id} | Add campus | Owner | 422 step invalid |
| POST /v1/consents | Record consent | Guardian | 409 duplicate |
| POST /v1/data-requests | Raise request | Guardian, staff | |
| POST /v1/webhooks/gateway, /webhooks/whatsapp | Provider callbacks | Signature verified | 401 bad signature |
| POST /v1/integrations/tally/sync | On-demand sync | Finance | 503 connector offline |
| GET /v1/status | Health for status page | Public | |

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| notification.created | Module raises an event needing a message | recipient, event type, tier, targets | Delivery workers |
| notification.delivered / opened / failed | Channel callbacks | channel, timestamps, reason | Read counts, fallback timers |
| notification.fallback_due | 30 minutes unopened (fees, pickups) | notification id | WhatsApp sender |
| approval.requested | Request raised | type, amount, approver chain | Notifications, queue |
| approval.decided | Approve or decline | decision, approver, reason | Requester, owning module, audit |
| approval.reminder_due / escalation_offered | Timers | request id, hours waiting | Notifications |
| audit.appended | Any change | entry id | Integrity job |
| report.generated / report.schedule_fired | Run completes | report id, file id | Email, notifications |
| file.scanned | Scan result | file id, clean or quarantined | Uploader, platform alerts |
| import.completed / import.rolled_back | Import ends | batch id, counts | Onboarding tracker |
| campus.created / campus.go_live | Wizard finished, go-live | campus id, batch | Invites, training, scorecard |
| consent.recorded / consent.withdrawn | Parent action | student, guardian | Access gates |
| datarequest.opened / datarequest.fulfilled | Privacy | type, due date | Grievance Officer |
| integration.sync_failed | Connector error | provider, reason | Finance, platform alerts |
| flag.changed | Flag edit | key, scope | All clients |

### State machines / workflows

- Notification: created -> queued -> sent -> delivered -> opened; branches: failed (retry then failed_final), suppressed (resolved before send), expired (past usefulness window), held (quiet hours) -> released at 7 am.
- Approval: draft -> pending (level 1) -> [escalated -> pending (level 2)] -> approved or declined -> closed; also withdrawn by requester before decision; reminder at 24 h and 48 h, escalation offer at 72 h.
- Delegation: scheduled -> active -> ended; revoked.
- Import batch: uploaded -> checking -> needs_fix or valid -> imported (or partially imported) -> rolled_back (within 7 days).
- Campus: draft -> added -> data_in -> trained -> parents_invited -> live; flags "needs a fix" if sheets fail.
- File: uploaded -> scanning -> clean or quarantined -> available -> expired or deleted.
- Data request: raised -> school review -> approved or rejected -> fulfilled (within 30 days).
- Report schedule: active -> paused (owner left or flag off) -> stopped.
- Consent: pending -> given -> withdrawn.

### Permission matrix

Legend: Y yes, own = own records, camp = own campus, grp = group-wide, R = read only, - none.

| Capability | Owner | Trustee | Principal | HoD | Teacher | Finance | HR | Parent | Platform admin |
|---|---|---|---|---|---|---|---|---|---|
| Set approval limits | Y | Y | - | - | - | - | - | - | - |
| Decide approvals within limit | grp | R log | camp | team leave | - | maker-checker | - | pickup only | - |
| View audit | grp | payroll and refund R | camp | own records | own records | finance entries | HR entries | - | via support grant only |
| Export audit | grp | - | camp | - | - | - | - | - | - |
| Run and schedule reports | grp | - | camp | team | - | finance reports | HR reports | - | - |
| Send notices | Y | - | camp | team | classes | - | staff | - | - |
| Edit calendar | grp | - | camp | - | - | - | - | - | - |
| Search people | grp | - | camp | team | classes | camp | camp | own children | - |
| Upload files | Y | - | Y | Y | Y | Y | Y | limited | - |
| Run import | Y | - | camp (onboarding lead) | - | - | - | - | - | assist |
| Notification settings | own | own | own | own | own | own | own | own | - |
| Raise data request | - | - | - | - | own | - | own | own | - |
| Manage integrations | grp view | - | - | - | - | camp | - | - | Y |
| View group scorecard | Y | - | - | - | - | - | - | - | - |

### Consolidated notification-event table

Rows marked [Design] come from the AppNotifications catalogue and lock-screen samples; rows marked [Spec] are added by this specification for events other sections raise. Channel codes: P push, W WhatsApp fallback or copy, S SMS, E email, I in-app only.

| Event | Audience | Message (sample) | Tier | Tap opens | Channels | Source |
|---|---|---|---|---|---|---|
| Child marked present | Parent | Vivaan reached school · 7:52 am | Normal | Attendance | P, I, W copy | [Design] |
| Child absent, not marked by 9 am | Parent | Vivaan is marked absent. Tap if this is wrong. | High | Message teacher | P, I, W copy | [Design] |
| Fee due in 7 days, then overdue | Parent | October fee Rs 14,600 is due Fri 16 Oct | Normal | Pay | P, I, W after 30 min | [Design] |
| Bus 10 minutes away or late | Parent | Bus 7 is 10 minutes from your stop | High | Live map | P, I | [Design] |
| Early pickup by someone new | Parent | Kiara 3-B: pickup by uncle. Is this OK? | Urgent | Approve or refuse | P, I, W after 30 min, S | [Design] |
| Class attendance not marked | Teacher | 7-C attendance not marked | Normal | Mark | P, I | [Design] |
| Sections not marked by deadline | Principal | 3 sections have not marked attendance. Remind teachers? | High (banner) | Remind or Later | P, I | [Design] |
| Cover assigned | Teacher | Cover 8-B, period 4 · Room 12 | High | Timetable | P, I | [Design] |
| Cover needed | School admin | Cover needed for 11 periods | High | Assign or Later | P, I | [Design] |
| Leave decided | Staff | Casual leave Mon 12 Oct approved | Normal | Leave | P, I | [Design] |
| Leave requests waiting | Principal, admin | 3 leave requests waiting | Normal | Review | P, I | [Design] |
| Decision waiting | Principal, admin | 2 decisions need you | Normal | Today | P, I | [Design] |
| Safety incident | Principal, security | Unknown man near Gate 2 | Urgent | Job | P, I, S | [Design] |
| Attendance trend down | Principal | Attendance down 6 pts · Grades 9 to 12 | Normal | Attendance | P, I | [Design] |
| Salary credited | Staff | October salary credited · payslip ready | Normal | Payslip | P, I, E link | [Design] |
| Salary changes to confirm | Admin | October salary: 3 changes · Confirm before Fri 30 Oct | Normal | Payroll | P, I | [Design] |
| Results published | Parent, student | Term 1 results are out | Normal | Results | P, I | [Design] |
| Receipt issued | Parent | Receipt: transport fee Rs 2,800 | Normal | Receipt | I, W | [Design] |
| Date sheet and admit cards | Parent, student | Term 1 exams start Mon 12 Oct | Normal | Learn | P, I | [Design] |
| Holiday notice | Parents, staff | Diwali break 7 to 11 Nov | Normal | Notice | P, I, W | [Design] |
| Teacher message or homework | Parent | Maths worksheet 4 is in the diary | Normal | Message | P, I | [Design] |
| Bus breakdown, early closure, emergency | Parents, staff | Safety alert | Urgent | Alert | P, I, S | [Design] |
| Owner notice | Selected audience | Notice title | Normal | Notice | P, I, W | [Design] |
| Approval reminder or escalation | Approver, requester | Decision waiting 24 h | Normal | Approvals | P, I | [Spec] |
| Report ready | Requester | Your report is ready | Normal | Report | P, I | [Spec] |
| Import finished | Owner, onboarding lead | 1,174 rows imported · 6 need a fix | Normal | Onboarding | P, I | [Spec] |
| Consent needed | Parent | Please confirm consent for Vivaan | Normal | Consent | P, I, W | [Spec] |
| Data request due | School admin | Data request due in 5 days | High | Request | P, I, E | [Spec] |
| Integration failure | Finance, platform | 3 vouchers failed to sync | High | Tally sync | P, I | [Spec] |
| Gate visitor waiting | Host staff | Visitor waiting for approval | High | Gate | P, I | [Spec] |

### Proposed flags

| Key | Purpose |
|---|---|
| ch.sms | SMS channel for gate-safety alerts (locked on for parents) |
| ch.email | Email delivery for payslips, reports, POs, invites |
| mod.audit_export | Audit search and export screen |
| mod.global_search | Cross-record search and Ctrl + K |
| mod.telemetry | Product telemetry collection |
| mod.open_api | Shows later integrations as "Coming later", not enableable |
