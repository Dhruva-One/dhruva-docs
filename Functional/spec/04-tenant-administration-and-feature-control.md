# 4. Tenant Administration and Feature Control

Area code: TFC. Every requirement in this section is tagged `[Spec]` unless it says `[Design]`. The designs show no admin console, no feature page, no plan screen and no audit screen. The only designed control surface is the "Campus admin · Settings" card on the WhatsApp overview board (four on/off toggles). Everything else here is the specification of a new capability, requested by the client as: "as an admin enable or disable AI features or other features for a tenant". A list of screens that still need design is in 4.8.

## 4.1 Purpose, scope and out-of-scope

**Purpose.** Let the right person at a school or group decide which parts of DhruvaOne, and which AI abilities, are switched on, for whom, where and from when. Let DhruvaOne staff control what each customer is entitled to. Make every change safe (previewed, approved when risky, reversible) and traceable (audited), and make the switch real everywhere (screens, APIs, WhatsApp, background jobs), not only on the screen.

**The four decisions the client chose (all in scope):**
1. Per-tenant on/off for every module (and every channel, AI capability and identity option in the catalogue).
2. Fine-grained AI controls: consent, per-capability toggles, human-approval policy, quotas, data use, kill switch, pilot.
3. Scoping by campus, role, user group and date (start and optional end).
4. Platform-owner plan gating: what a customer has paid for is an upper limit that no tenant admin can raise.

**In scope:** actors and delegation; the feature catalogue; the Features console; effective-state resolution; behaviour when a feature is off; AI controls; approvals; audit, snapshots and rollback; the runtime evaluation service; notifications about changes; plans and entitlements; a short list of tenant-level settings; group and standalone hierarchy; the Platform Owner console.

**Out of scope (covered elsewhere):**
- What each module does (Sections 5 onward by module; Section 3 Identity for sign-in, PIN, profiles).
- Billing, invoicing and payment collection from customers. This section only reads a plan and its dates.
- The behaviour of AI capabilities themselves (Section AI). This section decides whether they run and how they are governed.
- Role definitions for everyday staff roles (Section 3 and module sections). This section adds only the administration roles in 4.2.
- Data migration, import and campus go-live checklists (Owner > Onboarding is [Design], covered in the owner section). This section only lets a go-live batch drive feature dates (TFC-HIE-005).

**Design status.** `[Design]` items in this section: the four WhatsApp channel toggles; the group owner's approval of items above the campus limit; the standalone chairperson who approves the admin's own leave, salary and fee waivers and reads the payroll and refund log; "Audit trail" claims on the website; the campus setup option "Copy settings from a campus"; AI statements "Dhruva drafts, a person approves". Everything else is new.

## 4.2 Actors and roles

| Actor | Who | What they can do in feature control | Source |
|---|---|---|---|
| Platform Owner (PO) | DhruvaOne staff, in four sub-roles: Platform Admin, Platform Security, Platform Support, Platform Billing | Define plans and the catalogue; set per-tenant entitlements, trials and expiry; flip global or per-tenant kill switches; see usage; read a tenant's configuration (support, with consent and audit). Never reads school records through this console. | Spec |
| Tenant Administrator (TA), group | Group Owner (for example Mr. V.K. Shunglu, DPS Group) or a Group Admin delegated by the Group Owner | Change any feature the plan allows, at tenant, campus, role and user-group scope; accept AI consent; approve or request changes; set delegation to principals; manage tenant settings | Group Owner is Design; Group Admin is Spec |
| Tenant Administrator (TA), standalone | School Admin (for example Mrs. Meena Sharma, Saraswati Vidya Niketan). Where the school has a chairperson or trustee (Mr. R. K. Gupta), the trustee is the second approver for risky changes | As above, for the single school. Risky changes need the second approver. | School Admin is Design; trustee role in feature control is Spec (the design only gives the trustee the admin's own leave, salary, fee waivers and a read-only payroll and refund log) |
| Campus Principal (CP) | Principal of one campus of a group (for example Ms. Neelam Mehra, Gurugram Sec 45) | Within the delegation the group allows: switch features off (narrow) for the campus, request enablement, run a pilot in the campus, view the campus feature list and campus audit. Cannot widen beyond the group, cannot touch plan, consent or other campuses. | Spec |
| Everyone else (teacher, parent, student, HoD, accounts, HR, and so on) | | Experience the result. Can see "Why is this not available?" on a blocked deep link. No edit rights. | Spec |
| System / Dhruva | | Never changes a flag. Dhruva may only report ("Marks from photo is switched off for you") and may draft a change request text for an admin to review. | Spec |

**TFC-ACT-001 · Must · MVP · flag: core · [Spec]**
The system shall give each actor in the table above exactly the rights shown in the permission matrix (Annex 4-A) and no others.
- Acceptance: Given a Campus Principal, When they open the Features page, Then they see only their campus, and the controls for features the group has delegated to them; every other control is disabled with the tooltip "Set by your group office".
- Acceptance: Given a teacher, When they call a feature-admin API, Then the response is 403 `FORBIDDEN_ROLE`.
- Rules: Role rights are checked on the server (see TFC-RUN-005), never only hidden in the UI.

**TFC-ACT-002 · Must · MVP · flag: core · [Spec]**
The Group Owner can appoint a Group Admin and choose which categories (Channels, Modules, AI, Identity) and which campuses that Group Admin may change.
- Acceptance: Given a Group Admin limited to "Modules, campuses Gurugram and Noida", When they try to change an AI feature or the Pune campus, Then the change is refused with "You can change Modules for Gurugram Sec 45 and Noida Expressway only."
- Rules: A Group Admin cannot appoint other admins, accept AI consent, change plan data, or approve their own request. Group Owner can remove a Group Admin at any time; their pending requests are withdrawn.

**TFC-ACT-003 · Must · MVP · flag: core · [Spec]**
The Campus Principal can act only inside the delegation policy set per feature by the tenant admin: "None" (view only), "Narrow only" (can switch off for the campus), "Request" (can raise a request that the group approves), "Full" (can switch on and off for the campus).
- Acceptance: Given policy "Narrow only" on `mod.homework`, When the principal switches it off for the campus, Then it applies immediately; When the principal tries to switch on a feature that is off at tenant level, Then the button reads "Ask group office" and creates a request.
- Rules: Default policy by risk level: Low and Medium = Narrow only; High and Critical = None; AI = Request. Tenant admin can change per feature.

**TFC-ACT-004 · Should · MVP · flag: core · [Spec]**
For a standalone school the system shall route the second approval of risky changes to the trustee (chairperson) when one is registered, and show the trustee a read-only list of changes awaiting approval.
- Acceptance: Given a standalone school with a trustee, When the School Admin requests `ai.payroll_checks`, Then the request shows "Waiting for Mr. R. K. Gupta, chairperson" and the trustee can Approve or Decline from the app or WhatsApp link.
- Rules: Trustee sees only change requests and the payroll and refund log, consistent with the designed trustee limit. If no trustee is registered, see TFC-APR-004.

**TFC-ACT-005 · Must · MVP · flag: core · [Spec]**
The system shall prevent any change that would lock every Tenant Administrator out of the console.
- Acceptance: Given any configuration, When effective state is computed for a Tenant Administrator, Then `ch.desktop_web` and `idm.web_login` are On regardless of rules, and an attempt to disable them for admin roles returns `ADMIN_LOCKOUT_PREVENTED`.
- Rules: The tenant's mobile admin view is not guaranteed; web is the console of record.

**TFC-ACT-006 · Must · MVP · flag: core · [Spec]**
The system shall treat the following capabilities as never switchable by any tenant: sign-in by mobile number and OTP, audit logging, safety alerts and SOS, consent records, data export for the school's own data, and the console itself.
- Acceptance: Given the catalogue, When listing features, Then none of these appear as switchable; the Features page footer reads "Sign-in, safety alerts, audit and data export are always on."
- Rules: These are the only `core` items. Safety alerts may change channel (push, WhatsApp, SMS) but are never suppressed.

## 4.3 Functional requirements

### Feature catalogue (FLAG)

**TFC-FLAG-001 · Must · MVP · flag: core · [Spec]**
The system shall keep one versioned catalogue of feature definitions as the single source of truth for keys, names, categories, dependencies, risk, defaults per plan, and switching rules; the tables below are its initial content.
- Acceptance: Given a feature key used anywhere in the product, When it is not in the catalogue, Then the build fails the "flag lint" check; and the Features page lists exactly the catalogue entries the tenant's plan can see.
- Rules: Only the Platform Owner (Platform Admin) edits the catalogue. Each edit creates a new catalogue version; tenants keep their settings across versions.

**TFC-FLAG-002 · Must · MVP · flag: core · [Spec]**
The system shall give every feature a risk level (Low, Medium, High, Critical) that drives default delegation, approval and consent rules.
- Acceptance: Given a Critical feature, When a Tenant Administrator changes it, Then the two-person rule applies in the direction shown in the "Appr" column.
- Rules: Risk meaning: Low = convenience, no effect on records or families; Medium = reaches users or changes workflow; High = touches student safety, marks, attendance, staff records or family messages; Critical = touches money, payroll, minors' sensitive data, or approvals.

**TFC-FLAG-003 · Must · MVP · flag: core · [Spec]**
The system shall treat every `ai.*` flag as off for a tenant until the tenant has accepted AI consent (TFC-AIC-001), even if the plan includes it.
- Acceptance: Given a new tenant on Premium, When an admin opens an AI feature, Then the status chip is "Requires approval" and the toggle is disabled with the message "Accept the AI data-processing terms first".
- Rules: Non-AI features follow plan defaults.

**TFC-FLAG-004 · Must · MVP · flag: core · [Spec]**
The system shall register new flags proposed by other sections (the `NEW:` flags) in the catalogue before release, with a default that is Off for any feature that reaches families or touches money.
- Acceptance: Given a release containing a flag not in the catalogue, When the release pipeline runs, Then it is blocked until the flag is added with all columns of the catalogue table.
- Rules: The 9 flags proposed in this section are in the Annex "Proposed flags".

**Reading the tables.**
- *E / S / P* = plan tiers Essentials, Standard, Premium (names are placeholders, see 4.8). Values: `On` = included and on by default; `Opt` = included, off until the tenant turns it on; `-` = not included (shows "Locked by plan"). All `ai.*` are `Opt` at best because of consent.
- *Needs* = hard dependencies (see TFC-RES-004). Soft links (a module that merely reads another) are not listed.
- *Risk* L / M / H / C = Low / Medium / High / Critical.
- *Off: data* = what happens to data when the feature is switched off. In every case data is retained, never deleted by a switch (see TFC-DIS-005).
- *Switch* = lowest level that may switch the feature **off**: PO = Platform Owner only; TA = tenant administrator; CP = campus principal also (when delegation allows). Switching **on** or widening is always TA (or PO for locked items).
- *Appr* = second approval (TFC-APR-002): `N` none; `Y-on` needed to turn on or widen; `Y-off` needed to turn off or narrow; `Y` both directions.
- *AI consent* = `Y` consent required; `Y*` consent plus a specific acknowledgement for that capability (sensitive data); `-` not applicable.

#### Channels (9 canonical + 4 proposed)

| Key | Name | What it does | E / S / P | Needs | Risk | Off: data | Switch | Appr | AI consent |
|---|---|---|---|---|---|---|---|---|---|
| ch.desktop_web | Desktop web app | Staff, parents and students use DhruvaOne in a browser | On / On / On | - | H | Web sign-in refused for affected people; data kept | TA | Y-off | - |
| ch.mobile_ios | iPhone app | The iOS app | On / On / On | - | H | iOS sessions end; data kept | TA | Y-off | - |
| ch.mobile_android | Android app | The Android app | On / On / On | - | H | Android sessions end; data kept | TA | Y-off | - |
| ch.whatsapp | Dhruva on WhatsApp | The school's verified WhatsApp number: alerts and chats | Opt / On / On | school's WhatsApp Business number verified | H | Queued messages cancelled; alerts re-route to push (SMS for gate safety); chat log kept | TA | N | - |
| ch.whatsapp.voice | Voice notes | People send voice notes in Hindi or English; Dhruva confirms before acting | - / Opt / On | ch.whatsapp, ai.voice_input | M | Voice notes get "Please type your message"; past transcripts kept per retention | CP | N | Y |
| ch.whatsapp.photo_upload | Photo upload | Teachers send a photo of a register or marks sheet | - / Opt / On | ch.whatsapp | M | Photos refused with "Please use the app to upload"; stored photos kept per retention | CP | N | - |
| ch.whatsapp.staff_bot | Staff bot | Payslip (behind 4-digit PIN), leave, duty, holidays, advance | - / On / On | ch.whatsapp | H | Staff told to use the app; no data change | TA | N | - |
| ch.whatsapp.parent_bot | Parent bot | Attendance, fees, homework, bus, exams, leave, calendar for families | Opt / On / On | ch.whatsapp | M | Parents get the menu "Please use the app"; alerts still go if ch.whatsapp is on | TA | N | - |
| ch.whatsapp.teacher_bot | Teacher bot | Attendance, homework, timetable, notes, leave for teachers | - / On / On | ch.whatsapp | M | Teachers told to use the app | CP | N | - |
| ch.whatsapp.upi_pay (NEW) | UPI fees in chat | Parents pay fees by UPI inside the chat; PDF receipt | - / Opt / On | ch.whatsapp, mod.fees | C | Chat shows "Please pay in the app"; payments in progress still settle (TFC-DIS-004) | TA | Y-on | - |
| ch.whatsapp.payslip (NEW) | Payslips on WhatsApp | Staff open the payslip behind their 4-digit PIN | - / On / On | ch.whatsapp, mod.hr_leave | H | Staff told to use the app | TA | N | - |
| ch.whatsapp.admissions (NEW) | Admissions enquiries | New families ask about seats and fees on WhatsApp | Opt / On / On | ch.whatsapp | M | Enquiry menu hidden; leads kept | CP | N | - |
| ch.sms (NEW) | SMS | SMS for gate safety, and optionally when the app is offline | On / On / On | - | H | Only the optional "SMS if the app is offline" use is switchable; gate-safety SMS never stops | TA | N | - |

#### Modules (32 canonical + 2 proposed)

| Key | Name | What it does | E / S / P | Needs | Risk | Off: data | Switch | Appr | AI consent |
|---|---|---|---|---|---|---|---|---|---|
| mod.attendance | Attendance | Class roll call, absent alerts, repeat-absence flags | On / On / On | - | H | Roll call and alerts stop; history read-only | TA | Y-off | - |
| mod.timetable | Timetable | Timetable build, day view for teachers | On / On / On | - | M | View hidden; published timetable kept | TA | N | - |
| mod.cover | Cover | Cover for absent teachers | On / On / On | mod.timetable | M | Cover list hidden; past cover kept | CP | N | - |
| mod.lesson_plans | Lesson plans | Annual and weekly plans, HoD review | - / On / On | - | L | Plans read-only | CP | N | - |
| mod.pace_tracking | Pace tracking | Syllabus pace per class | - / Opt / On | mod.lesson_plans | L | Pace data kept | CP | N | - |
| mod.homework | Homework | Post homework, parent view | On / On / On | - | L | Past homework visible read-only | CP | N | - |
| mod.marks_results | Marks and results | Marks entry, checks, publishing to parents | On / On / On | - | H | Entry and publishing stop; marks kept | TA | Y-off | - |
| mod.exams | Exams | Date sheets, papers, strongroom log, seating, duties | On / On / On | - | M | Schedules read-only | TA | N | - |
| mod.report_cards | Report cards | CBSE report cards, registration checks | On / On / On | mod.marks_results | H | Issued cards kept; new ones not generated | TA | Y-off | - |
| mod.fees | Fees | Fee ledger, counter receipts, online payment, defaulters, concessions | On / On / On | mod.approvals | C | Collection screens off; gateway settlements still recorded (TFC-DIS-004); ledger kept | TA | Y | - |
| mod.finance_accounts | Finance and accounts | Bills, vendors, purchases, inventory, month close | - / On / On | - | C | Read-only; month locks kept | TA | Y | - |
| mod.tally_sync | Tally sync | TallyPrime connector and daily export | - / Opt / On | mod.finance_accounts | H | Sync stops; unsent vouchers queue held and flagged | TA | Y | - |
| mod.bank_recon | Bank reconciliation | Statement import, matching, BRS | - / Opt / On | mod.finance_accounts | H | Open reconciliations paused | TA | Y-on | - |
| mod.payroll | Payroll | Pay groups, monthly runs, approval, payslips | - / On / On | mod.hr_leave, mod.approvals | C | Run in progress paused; payslips kept | TA | Y | - |
| mod.hr_leave | HR and leave | Employee records, leave, out on duty, corrections, payslip view | On / On / On | mod.approvals | H | Requests stop; balances kept | TA | Y-off | - |
| mod.hiring_onboarding | Hiring and onboarding | Positions, shortlist, joiner checklists, exits | - / On / On | - | M | Records read-only | TA | N | - |
| mod.admissions_crm | Admissions CRM | Pipeline, family profiles, tours, seats, campaigns | Opt / On / On | - | M | Pipeline read-only; campaigns paused | TA | N | - |
| mod.transport | Transport | Routes, stops, students, attendant taps | - / On / On | - | H | Attendant app and parent alerts stop; routes kept | TA | Y-off | - |
| mod.bus_live | Bus live board | Live board from attendant taps; GPS later | - / On / On | mod.transport | M | Board hidden | CP | N | - |
| mod.security_gate | Security and gate | Visitors, early-pickup check, guard roster | - / On / On | - | H | Gate log hidden; pickup check falls back to office phone call | TA | Y-off | - |
| mod.it_helpdesk | IT helpdesk | Jobs log, systems status | - / On / On | - | L | Jobs read-only | CP | N | - |
| mod.counselling | Counselling | Caseload, referrals, private session notes | - / Opt / On | - | C | Notes stay private and unreadable by admins; read by counsellor only | TA | Y-on | - |
| mod.notices | Notices | Notices with read receipts | On / On / On | - | M | Past notices visible | CP | N | - |
| mod.calendar_ptm | Calendar and PTM | School calendar, meetings, reminders | On / On / On | - | L | Calendar read-only | CP | N | - |
| mod.parent_messaging | Parent messaging | Parent queries and replies | On / On / On | - | M | Threads read-only; new queries go to office phone | TA | N | - |
| mod.student_learning | Student learning | Student app: notes, practice, results view | - / Opt / On | - | M | Content kept | TA | N | - |
| mod.approvals | Approvals | Approval chain and limits | On / On / On | - | C | Blocked while dependents (fees, payroll, leave) are on | TA | Y | - |
| mod.reports | Reports | Ready-made reports and exports | On / On / On | - | L | Reports hidden; data kept | CP | N | - |
| mod.group_scorecard | Group scorecard | 14-campus scorecard, compare views (group tenants only) | Group: On / On / On | - | M | View hidden | TA | N | - |
| mod.campus_onboarding | Campus onboarding | Add a campus, rollout batches, data sheets (group only) | Group: On / On / On | - | M | Read-only | TA | N | - |
| mod.audit_export (NEW) | Audit export | Download the audit log as CSV or JSON | - / On / On | - | L | Viewing the log stays on; export hidden | PO | N | - |
| mod.open_api (NEW) | Open APIs (P2) | School-level API access for other systems | - / - / Opt | - | H | Keys revoked; data kept | TA | Y-on | - |
| mod.profile_switching | Profile switching | Switch between profiles of one phone number | On / On / On | idm.multi_profile | M | Users see only the profile last used; other profiles unreachable until re-enabled | PO | N | - |

#### AI capabilities (22 canonical + 3 proposed)

All AI features are Opt at best, need AI consent, and keep a human in the loop (see TFC-AIC-004). When any is off, the manual path in its module works unchanged.

| Key | Name | What it does | E / S / P | Needs | Risk | Off: data | Switch | Appr | AI consent |
|---|---|---|---|---|---|---|---|---|---|
| ai.assistant_chat | Ask Dhruva | Answers from school records, with sources | Opt / Opt / Opt | - | M | Chat history kept per retention | CP | N | Y |
| ai.focus_card | Daily priorities | Dhruva-prepared task list per role | Opt / Opt / Opt | - | L | Static task list shown instead | CP | N | Y |
| ai.cover_suggestions | Cover suggestions | Free-teacher suggestions | - / Opt / Opt | mod.cover | L | Manual free-teacher list | CP | N | Y |
| ai.timetable_generator | Timetable generator | Draft timetable for coordinator to review and publish | - / Opt / Opt | mod.timetable | M | Drafts kept 30 days then archived | TA | N | Y |
| ai.reply_drafts | Reply drafts | Drafts replies to parent queries | - / Opt / Opt | mod.parent_messaging | M | Unsent drafts discarded after 7 days | CP | N | Y |
| ai.notice_drafts | Notice drafts | Drafts notices, translated | Opt / Opt / Opt | mod.notices | M | Unsent drafts kept 7 days | CP | N | Y |
| ai.marks_from_photo | Marks from photo | Reads a photographed marks sheet | - / Opt / Opt | mod.marks_results | H | Unconfirmed readings discarded; entered marks kept | TA | Y-on | Y* |
| ai.paper_generator | Paper generator | Drafts a question paper to the HoD blueprint | - / Opt / Opt | mod.exams | M | Drafts kept 30 days | CP | N | Y |
| ai.lesson_plan_drafts | Lesson plan drafts | Weekly plan from annual plan and pace | - / Opt / Opt | mod.lesson_plans | L | Drafts kept 30 days | CP | N | Y |
| ai.homework_marking | Homework marking | Suggests marks and feedback on homework | - / - / Opt | mod.homework | H | Suggestions discarded; teacher marks kept | TA | Y-on | Y* |
| ai.remedial_grouping | Remedial grouping | Suggests students needing help | - / Opt / Opt | mod.marks_results | M | Suggestions discarded; groups kept | CP | N | Y |
| ai.at_risk_detection | Early warnings (P2) | Flags students at risk after a year of data | - / - / Opt | mod.attendance, mod.marks_results | H | Open flags archived, not deleted | TA | Y-on | Y* |
| ai.admissions_scoring | Admissions scoring | Ranks and scores enquiries | - / - / Opt | mod.admissions_crm | H | Scores hidden; pipeline kept | TA | Y-on | Y* |
| ai.fee_followup | Fee follow-up | Drafts fee reminders (English or Hindi) | - / Opt / Opt | mod.fees | C | Unsent reminders discarded; reminder log kept | TA | Y-on | Y* |
| ai.payroll_checks | Payroll checks | Flags payroll anomalies before approval | - / - / Opt | mod.payroll | C | Flags kept as history | TA | Y-on | Y* |
| ai.bank_matching | Bank matching | Matches bank lines and suggests fixes | - / - / Opt | mod.bank_recon | C | Suggestions discarded; posted entries kept | TA | Y-on | Y* |
| ai.security_triage | Security and IT triage | Groups jobs, suggests assignee | - / Opt / Opt | mod.security_gate or mod.it_helpdesk | M | Manual assignment | CP | N | Y |
| ai.transport_alerts | Transport alerts | Drafts delay and breakdown notes | - / Opt / Opt | mod.transport | M | Manual notes | CP | N | Y |
| ai.student_tutor | Student tutor | Practice and explanations for students | - / - / Opt | mod.student_learning | C | Chats kept per retention | TA | Y-on | Y* |
| ai.voice_input | Voice input | Turns speech into text (app and WhatsApp) | - / Opt / Opt | - | M | Typing only | CP | N | Y |
| ai.translation | Hindi and English | Translates notices and replies | Opt / Opt / Opt | - | L | Shown in written language only | CP | N | Y |
| ai.whatsapp_bot | Dhruva on WhatsApp (free text) | Understands free-text chat; menu stays | - / Opt / Opt | ch.whatsapp | M | WhatsApp becomes buttons and lists only | TA | N | Y |
| ai.exam_planning (NEW) | Exam planner | Date sheets against the calendar, seating, duties | - / Opt / Opt | mod.exams | M | Manual planning | CP | N | Y |
| ai.counselling_assist (NEW) | Counsellor assistant | Check-in suggestions and drafted session notes | - / - / Opt | mod.counselling | C | Drafts discarded; notes kept | TA | Y-on | Y* |
| ai.hr_assist (NEW) | HR assistant | Shortlists candidates, calculates final settlement | - / - / Opt | mod.hiring_onboarding or mod.hr_leave | H | Manual shortlist | TA | Y-on | Y* |

#### Identity (5 canonical)

| Key | Name | What it does | E / S / P | Needs | Risk | Off: data | Switch | Appr | AI consent |
|---|---|---|---|---|---|---|---|---|---|
| idm.biometric | Face ID or fingerprint | Optional unlock on the phone | On / On / On | - | L | People use PIN | TA | N | - |
| idm.app_pin | App PIN | PIN for staff and finance pages | On / On / On | - | C | Not switchable by tenants; Platform Owner only, never for roles with money or payroll access | PO | Y | - |
| idm.multi_profile | Multiple profiles | One number holds several profiles | On / On / On | - | M | Platform Owner only; number resolves to the most recent profile | PO | N | - |
| idm.web_login | Web login | Sign-in on the web | On / On / On | ch.desktop_web | H | Never off for Tenant Administrators (TFC-ACT-005) | TA | Y-off | - |
| idm.sso | Single sign-on (later) | Google or Microsoft sign-in for staff | - / - / Opt | idm.web_login | H | Staff use OTP | TA | Y-on | - |

Sign-in by mobile number and OTP is `core` and has no flag.

### Admin console UX (CON)

The console is a desktop web page "Features" inside Tenant Administration, reachable from the admin's settings. Phone gets a read-only list plus the pause and approve actions. [Spec] throughout.

**TFC-CON-001 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can open a "Features" page listing every catalogue entry visible to the tenant's plan, grouped under the tabs Channels, Modules, AI and Identity.
- Acceptance: Given a Standard tenant, When the page opens, Then it shows each feature's name, one-line description, status chip and scope summary, sorted by category then name, and the header shows the plan name and "Last change: <who>, <when>".
- Rules: Features not in the plan are shown with the chip "Locked by plan" (not hidden), with a link "Ask DhruvaOne about this plan".

**TFC-CON-002 · Must · MVP · flag: core · [Spec]**
The page shall provide search by name, key or description, and filters by category, status, risk, and "changed in the last 30 days".
- Acceptance: Given the search text "photo", When typed, Then results show `ch.whatsapp.photo_upload` and `ai.marks_from_photo` within 300 ms and the count reads "2 features".

**TFC-CON-003 · Must · MVP · flag: core · [Spec]**
Each feature row shall show one status chip from this fixed set.

| Chip | Meaning |
|---|---|
| On | On for the whole tenant, no restricting rules |
| Off | Off for the whole tenant |
| On for some | On with at least one campus, role, group or user-level rule; the chip shows a count, for example "On for some · 3 rules" |
| Scheduled | A future start, end or change exists; chip shows the next date, for example "Off from 2 Nov, 8:00 am" |
| Locked by plan | The plan does not include it, or the plan has expired |
| Requires approval | A change request is waiting, or the feature needs consent first |
| Paused by DhruvaOne | Platform kill switch active; admin cannot override |
| Pilot | AI rollout stage is Shadow or Pilot (TFC-AIC-009) |

- Acceptance: Given a feature with a scheduled change and a campus rule, When shown, Then it shows "On for some" with a small "Scheduled" tag; a feature can show at most one main chip and up to two tags.

**TFC-CON-004 · Must · MVP · flag: core · [Spec]**
Opening a feature shall show a drawer with these parts, in order: summary and risk; dependencies and dependents; current rules table (scope, effect, dates, who set it); "Why is this on or off?" explanation; impact preview; reason field; schedule; AI settings (for `ai.*`); history (last 10 changes); actions.
- Acceptance: Given `ai.marks_from_photo`, When the drawer opens, Then it shows "Needs: Marks and results", "Used by: none", the consent status, quota used this month, and the approval policy for "Teacher confirms before marks are saved".

**TFC-CON-005 · Must · MVP · flag: core · [Spec]**
The scope picker shall let the admin choose "Whole school or group", "Selected campuses", "Selected roles", "Selected user groups", or a combination (campus AND role AND group).
- Acceptance: Given a group tenant, When the admin picks campuses "Gurugram Sec 45" and "R.K. Puram" and role "Teacher", Then the summary reads "Teachers at 2 campuses" and the preview counts those teachers.
- Rules: Standalone schools do not see the campus option. User groups are named lists maintained by the tenant admin (for example "Coordinators 9-12", up to 5,000 members; a group can be filled by role plus grade rule or by pasting phone numbers). Role list = the roles in the tenant.

**TFC-CON-006 · Must · MVP · flag: core · [Spec]**
The drawer shall let the admin schedule a change: "Now", or "From" date and time, with an optional "Until" date and time, in the tenant's time zone (Asia/Kolkata unless changed).
- Acceptance: Given "From 2 Nov 2026, 8:00 am" and "Until 31 Dec 2026, 11:59 pm", When saved, Then the chip shows "Scheduled", the feature turns on at 8:00:00 and returns to its previous state after 23:59:59 on 31 Dec.
- Rules: Start must be at least 5 minutes in the future; end must be after start; at most 10 scheduled changes per feature. A scheduled change can be edited or cancelled until it fires.

**TFC-CON-007 · Must · MVP · flag: core · [Spec]**
Every change shall require a reason of at least 10 characters (a short picklist of common reasons plus free text), and High and Critical changes shall also require the admin to confirm "I understand people will lose access".
- Acceptance: Given an empty reason, When "Save" is pressed, Then the button is disabled with the hint "Add a reason for the record".

**TFC-CON-008 · Must · MVP · flag: core · [Spec]**
Before saving, the system shall show an impact preview computed from live data: people affected by role and campus, pending items by type, scheduled jobs and queued messages, dependent features that will also switch off, and any blocking condition.
- Acceptance: Given the admin switches off `ai.marks_from_photo` for all teachers, When the preview loads (within 2 seconds for up to 5,000 users), Then it reads "14 teachers will lose Marks from photo; 3 pending items will be completed manually" and offers the drain policy of TFC-DIS-003.
- Acceptance: Given a dependent feature, When switching off its parent, Then the preview lists "Also switches off: Voice notes on WhatsApp (needs Voice input)" and requires a tick to continue.
- Rules: Preview is advisory; the numbers are re-computed at apply time and stored in the audit event.

**TFC-CON-009 · Should · MVP · flag: core · [Spec]**
The admin can apply a preset that sets many features in one change request: "Essentials", "Standard", "Full AI".

| Preset | Sets |
|---|---|
| Essentials | Channels web + app; attendance, homework, notices, calendar, marks, fees basics, leave, approvals, reports; all AI off |
| Standard | Essentials + every module in the plan; AI limited to drafting capabilities with human approval on (cover, reply, notice, lesson plan, paper, translation, voice) |
| Full AI | Standard + every AI capability in the plan, each at rollout stage "Pilot" for the Tenant Administrator group only until promoted |

- Acceptance: Given a Standard-plan tenant picks "Full AI", When previewed, Then entries not allowed show "Locked by plan" and entries needing consent or approval show "Requires approval"; applying creates one change request with one audit group id.
- Rules: Presets never skip consent, plan limits, or approvals. Presets are templates owned by DhruvaOne; tenants may save their own named presets (up to 10).

**TFC-CON-010 · Should · MVP · flag: core · [Spec]**
The admin can select many features and apply one action: switch on, switch off, set scope, set schedule, or reset to plan default.
- Acceptance: Given 12 selected features, When "Switch off for selected campuses" is chosen, Then one preview covers all 12, one reason applies, and the result is one change request; features that fail a check are listed with the reason and the rest proceed only if the admin ticks "Apply the others".
- Rules: Maximum 100 features per bulk change.

**TFC-CON-011 · Should · MVP · flag: core · [Spec]**
The admin can open "Compare campuses" to see a features-by-campuses grid, with cells On, Off, Scheduled, or Different for role.
- Acceptance: Given 14 campuses, When opened, Then the grid shows 14 columns, can be filtered to differences only, and clicking a cell opens the rules that decide it.
- Rules: Group tenants only.

**TFC-CON-012 · Should · MVP · flag: core · [Spec]**
The admin can export the current configuration (every feature, scope rules, schedule, plan state) and the effective-state grid as CSV or JSON.
- Acceptance: Given "Export", When chosen, Then a file downloads named `features_<tenant>_<yyyy-mm-dd>.csv` within 10 seconds for up to 200 campuses, and the export is itself audited.

**TFC-CON-013 · Must · MVP · flag: core · [Spec]**
The change flow shall be: edit, preview, reason, (approval if needed), apply; with "Save as draft" for a bundle of edits that is not yet submitted.
- Acceptance: Given a draft with 3 edits, When the admin leaves the page, Then the draft is kept for 14 days and shown as "Draft · 3 changes" for that admin only.

**TFC-CON-014 · Must · MVP · flag: core · [Spec]**
The Campus Principal shall see a reduced Features page for their campus with only the controls that are delegated, and a campus-only change history.
- Acceptance: Given policy "Request" for `ai.cover_suggestions`, When the principal clicks "Ask group office" and adds a reason, Then a request appears for the Group Owner in Approvals, and the principal sees "Waiting for group office".

**TFC-CON-015 · Should · P2 · flag: core · [Spec]**
The console shall be usable at 1280 px and above, by keyboard, with text contrast meeting WCAG 2.1 AA, and shall offer English first and Hindi labels in a later release.
- Acceptance: Given keyboard only, When tabbing through the drawer, Then every control is reachable and chips are not colour-only (each carries its text label).

### Effective-state resolution (RES)

**TFC-RES-001 · Must · MVP · flag: core · [Spec]**
The system shall compute whether a feature is on for a given request using this strict precedence, highest first; the first level that says Off ends the evaluation with that reason.

| Order | Level | Can say | Result and reason code when it says Off |
|---|---|---|---|
| 1 | Platform kill switch (global, per feature version, or per tenant) | Off | `PLATFORM_KILL` |
| 2 | Plan entitlement (plan plus per-tenant overrides, trial, expiry, grace) | Not entitled | `PLAN_LOCKED` or `PLAN_EXPIRED` |
| 3 | Dependencies and prerequisites (parents effective, AI consent accepted, channel set-up complete, quota not hard-stopped) | Not satisfied | `DEPENDENCY_OFF`, `CONSENT_MISSING`, `SETUP_INCOMPLETE`, `QUOTA_EXCEEDED` |
| 4 | Tenant setting (base state, default from plan) | On or Off | `TENANT_SETTING` |
| 5 | Campus override | On or Off, if not locked above | `CAMPUS_OVERRIDE` |
| 6 | Role override | On or Off, if not locked above | `ROLE_OVERRIDE` |
| 7 | User group or individual profile override | On or Off, if not locked above | `USER_OVERRIDE` |

- Acceptance: Given plan Standard excludes `ai.payroll_checks` and the tenant setting is On, When evaluated, Then the result is Off with reason `PLAN_LOCKED`.
- Acceptance: Given tenant setting On, campus override Off for Pune, role override On for "Principal", When a Pune principal is evaluated, Then the result is On (more specific wins) unless Pune's rule is a lock (TFC-RES-003).
- Rules: Levels 1 to 3 are gates that nothing below can open. Levels 4 to 7 are a layered setting where the most specific matching rule wins. Within one level, a Disable rule beats an Enable rule if both match the same request, and between two Enable or two Disable rules the newer one wins.

**TFC-RES-002 · Must · MVP · flag: core · [Spec]**
Each scope rule shall carry: effect (Enable or Disable), selectors (campuses, roles, user groups, profiles, channels, app versions, all optional; all given selectors must match, "AND"), schedule window, rollout stage (for AI), and owner (who set it).
- Acceptance: Given a rule "Disable, roles = Academic coordinator, group = Coordinators 9-12, channel = WhatsApp", When a user matches role and group but uses the app, Then the rule does not apply.
- Rules: A rule with no selectors is the tenant setting. Selectors on `channel` let an admin disable a feature on one surface only.

**TFC-RES-003 · Must · MVP · flag: core · [Spec]**
A higher level shall be able to lock a feature so lower levels cannot override it: the platform locks above the tenant, the tenant admin locks above campus, and a campus principal's rules are always below the tenant.
- Acceptance: Given the tenant admin sets `mod.fees` to Off with "Lock: campuses cannot override", When a principal opens that feature, Then the controls are disabled with "Set by your group office", and any API write returns `LOCKED_BY_HIGHER_LEVEL`.
- Rules: Delegation policy (TFC-ACT-003) is the default lock expression. A lock set after lower rules exist does not delete them; they stay stored but are ignored and shown as "Ignored (locked)".

**TFC-RES-004 · Must · MVP · flag: core · [Spec]**
The system shall enforce dependencies as hard rules at both write time and read time.
- Rules, write time:
  - Switching on a child while its parent is off in the same scope is refused: "Turn on <parent> first".
  - Switching off a parent lists every child that is on in the same scope and asks the admin to confirm; on confirm each child is switched off by a system-authored rule tagged "Auto: parent off", which is audited as part of the same change.
- Rules, read time: A child is evaluated Off with `DEPENDENCY_OFF` if its parent is effectively Off for the same request, even if the child's own rule says On.
- Rules, families: `ai.*` needs its `mod.*`; `ch.whatsapp.*` and `ai.whatsapp_bot` need `ch.whatsapp`; `ch.whatsapp.voice` also needs `ai.voice_input`; `mod.bus_live` needs `mod.transport`; `mod.fees`, `mod.payroll`, `mod.hr_leave` need `mod.approvals`.
- Acceptance: Given `mod.marks_results` is switched off for Class 9-12 coordinators, When `ai.marks_from_photo` is evaluated for them, Then it is Off with `DEPENDENCY_OFF`, and the auto-created rule appears in the drawer as "Auto: parent off".
- Rules: When the parent is later switched on again, children remain Off (auto rules are removed but the child's previous own rules are not restored automatically); the admin sees "3 features that were switched off with this one can be turned back on" with one tap.

**TFC-RES-005 · Must · MVP · flag: core · [Spec]**
The system shall detect conflicts when saving and refuse or warn according to this table.

| Conflict | Handling |
|---|---|
| Two rules at the same level with same selectors and opposite effects | Refuse: "A rule for these people already exists. Edit it instead." |
| Rule below a lock | Refuse (TFC-RES-003) |
| Enable rule where entitlement is missing | Refuse with `PLAN_LOCKED`; offered link "Ask DhruvaOne" |
| Schedule windows overlapping on the same feature and scope | Warn; the later-starting window wins from its start; shown as a timeline in the drawer |
| Change request pending on same feature | Warn: "Another change is waiting for approval"; second change is queued behind it |
| Removing a role or campus that rules refer to | Rules for the removed item are archived and listed in audit |

- Acceptance: Given two admins edit the same feature, When the second saves, Then they see "This feature changed 2 minutes ago. Review the new version" (optimistic concurrency by version number, `409 VERSION_CONFLICT`).

**TFC-RES-006 · Must · MVP · flag: core · [Spec]**
Schedules shall be evaluated by the server clock in UTC against the rule's time zone; start is inclusive and end is exclusive.
- Acceptance: Given a rule "Until 31 Dec 2026, 11:59 pm", When evaluated at 11:59:30 pm, Then the rule still applies; at 12:00:00 am on 1 Jan it no longer applies.
- Rules: Changes take effect within the propagation target (TFC-RUN-004) of their start time; clients do not need to be online at that moment.

**TFC-RES-007 · Should · MVP · flag: core · [Spec]**
The admin can ask "Why is this on or off?" for any feature and any person, and shall receive the decision chain.
- Acceptance: Given the search "Rekha Sinha" and feature `ai.timetable_generator`, When asked, Then the answer reads "Off for Rekha Sinha. Reason: rule 'Coordinators 9-12' (set by Meena Sharma on 30 Oct 2026). Tenant setting is On. Plan allows it." and shows all seven levels with the decisive one highlighted.
- Rules: Only admins can ask; the explanation never shows another school's data.

**TFC-RES-008 · Must · MVP · flag: core · [Spec]**
The system shall treat a safeguard list as always On regardless of rules: sign-in, safety alerts, audit, consent, data export, the admin console for Tenant Administrators, and approvals needed to decide a pending request.
- Acceptance: Given every module switched off, When a parent signs in, Then sign-in works and the app shows "Your school has switched off the features for your role. Contact the school office."

### Behaviour when a feature is off (DIS)

**TFC-DIS-001 · Must · MVP · flag: core · [Spec]**
The system shall hide a switched-off feature from navigation, menus, search results, shortcuts, task lists and Dhruva's suggestions, instead of showing it greyed out.
- Acceptance: Given `mod.homework` is Off for a role, When that role opens the app, Then no Homework tab, card, notification setting or search hit appears.
- Rules: Exception: "Locked by plan" is shown greyed only inside the admin console, never to end users. Fields and buttons that exist inside a visible screen for an off AI feature (for example the "Read from photo" button) are removed, not disabled.

**TFC-DIS-002 · Must · MVP · flag: core · [Spec]**
The system shall refuse every API call and background action for a feature that is effectively Off, with HTTP 403 and the body below.
- Acceptance: Given Off `ai.marks_from_photo`, When a client calls the upload endpoint, Then the response is 403 with code `FEATURE_DISABLED`, `feature` = `ai.marks_from_photo`, `reason` = the reason code, `message` = "Marks from photo is switched off for your school.", and a `request_id`.
- Rules: Message text is localised (English, Hindi); the reason code is not shown to end users, only to admins in the console and logs. Quota exhaustion returns 429 `AI_QUOTA_EXCEEDED` instead (TFC-AIC-006). Unknown flag keys fail closed.

**TFC-DIS-003 · Must · MVP · flag: core · [Spec]**
The system shall handle in-flight items according to a drain policy chosen at disable time, with these defaults by item type.

| Item type | Default policy | Admin may choose |
|---|---|---|
| Drafts waiting for a person (AI notice, reply, paper, plan) | Keep for review for 7 days (30 for papers and plans), then archive; person can still copy text and complete manually | Keep, archive now |
| Pending approvals of the module (leave, concession, purchase) | Pause: card shows "On hold: <feature> switched off", approver can read, cannot decide; resumes on re-enable. After 14 days the requester is told and may withdraw | Drain (let approvers finish), Pause |
| Scheduled jobs (fee reminders, report schedules, Tally sync) | Pause; missed runs are listed, not back-filled | Cancel, Pause |
| Queued outbound WhatsApp messages not yet sent | Cancel; messages of Urgent tier (safety, early pickup) re-route to push and SMS | Cancel only |
| Multi-step runs (payroll run, bank reconciliation, report card batch) | Block the disable until the run is closed or admin picks "Pause run" with approval | Pause with approval |
| AI jobs running | Finish the current call; no new ones | - |
| Offline actions on phones not yet synced | Honoured if made before the change time (TFC-RUN-006) | - |

- Acceptance: Given 3 pending AI drafts when `ai.notice_drafts` is switched off, When the drawer preview is read, Then it says "3 pending items will be completed manually" and on apply the teachers see the drafts under "Drafts · switched off" read-only with a "Copy text" button.

**TFC-DIS-004 · Must · MVP · flag: core · [Spec]**
The system shall never drop money received, safety alerts, or statutory records because a feature is off.
- Acceptance: Given `mod.fees` Off, When the payment gateway sends a settlement callback for a payment started earlier, Then it is recorded, a receipt is generated and the ledger entry is flagged "Received while Fees was off" for the accounts head.
- Acceptance: Given `ch.whatsapp` Off, When a gate early-pickup alert (Urgent) is raised, Then it goes by push and SMS and the event log records "Re-routed".
- Rules: Same for refunds in progress, bank-feed imports for open BRS, and audit events.

**TFC-DIS-005 · Must · MVP · flag: core · [Spec]**
The system shall keep all data of a switched-off feature, never delete it because of a switch, and show it read-only wherever other visible features refer to it.
- Acceptance: Given `mod.homework` Off, When a parent opens a child's term summary, Then past homework counts remain visible as read-only history; creating or editing homework is refused.
- Rules: Data deletion follows retention settings (TFC-SET-006), not switches. Counselling session notes remain private to counsellors even when the module is on or off. Reports that depend on an off module show the section "Not included: <feature> is switched off" instead of silently omitting it.

**TFC-DIS-006 · Must · MVP · flag: core · [Spec]**
The system shall suppress notifications raised by a switched-off feature, in every channel, except the safety and money exceptions of TFC-DIS-004 and the change notices of TFC-NOT-001.
- Acceptance: Given `mod.homework` Off for a campus, When a teacher posts homework by a stale client, Then it is rejected and no parent receives "New homework".
- Rules: Notification settings screens remove the matching switch, for example "Teacher messages" shows only the categories still available.

**TFC-DIS-007 · Must · MVP · flag: core · [Spec]**
Reports and exports shall respect switches: a switched-off module's data appears in scheduled and ad-hoc reports only as read-only history, new exports of its operational lists are refused, and the admin's full data export (core) always includes everything.
- Acceptance: Given `mod.transport` Off, When a principal runs the "student distribution" report, Then the transport column shows "Not included: Transport is switched off" and the full export for the school still contains routes and stops.

**TFC-DIS-008 · Must · MVP · flag: core · [Spec]**
When a feature is switched on again the system shall show previous data, resume paused approvals and jobs (not back-fill missed runs unless the admin picks "Run missed now" with a preview), and not resurrect cancelled queue items or discarded AI drafts.
- Acceptance: Given paused fee reminders and a re-enable, When the admin confirms, Then the next scheduled run goes out on its normal date and the 2 missed runs are listed under "Skipped while off".
- Rules: AI re-enable checks consent version (TFC-AIC-002) and quota.

**TFC-DIS-009 · Must · MVP · flag: ch.whatsapp · [Design]**
The campus admin can switch the WhatsApp channel's four options on or off and see the channel status "Live".
- Acceptance: Given the "Campus admin · Settings" card, When the admin turns off "Voice notes" (Hindi and English), Then the voice option disappears for users of that campus (maps to `ch.whatsapp.voice`); "UPI fee payments in chat" maps to `ch.whatsapp.upi_pay`, "Payslips on WhatsApp" (always behind the staff member's PIN) to `ch.whatsapp.payslip`, and "Admissions enquiries" to `ch.whatsapp.admissions`.
- Rules: This card is the only designed switch surface; it shall be a view into the same flags, not a separate store. Usage tiles on the card (chats this week, answered by Dhruva, handed to office or HR, average reply) are reporting, outside this section.

**TFC-DIS-010 · Must · MVP · flag: core · [Spec]**
The system shall refuse to switch off a feature while a blocking condition holds, and name it.
- Acceptance: Given a payroll run in "review" state, When the admin tries to disable `mod.payroll`, Then the preview shows "Blocked: October teaching payroll is waiting for approval. Close or pause the run first." and Apply is disabled.
- Rules: Blocking conditions: payroll run open; unsettled gateway payments; Urgent early-pickup request pending; open month-end close; report card batch publishing.

### AI controls (AIC)

**TFC-AIC-001 · Must · MVP · flag: core · [Spec]**
Before the first AI feature can be enabled for a tenant, the Group Owner (or standalone School Admin) shall accept the AI data-processing terms, and the system shall record who, the text version, and the timestamp.
- Acceptance: Given no consent, When an admin opens "AI" tab, Then a banner "Turn on Dhruva for your school: read and accept how your data is used" opens the terms; accepting records `AIConsent{tenant, accepted_by, role, consent_version, text_sha256, accepted_at, ip, device, scope}`; before acceptance no AI toggle can be on.
- Rules: Terms text states roles per the website Trust page: school = data fiduciary, DhruvaOne = processor; student data is not sold; no advertising or tracking. Only Group Owner, School Admin, or the trustee (where the school asks for countersign, TFC-APR-004) can accept; a Group Admin cannot. Consent is not tied to a person leaving.

**TFC-AIC-002 · Must · MVP · flag: core · [Spec]**
When the consent text changes (new version), the system shall ask the Tenant Administrator to re-accept within 30 days; AI features continue during that window, then switch to Off with reason `CONSENT_MISSING` until accepted.
- Acceptance: Given version 2 published, When the admin signs in, Then banner "New AI terms. Accept by 29 Nov 2026" shows; on day 31 `ai.*` evaluate Off.
- Rules: For `Y*` capabilities a specific acknowledgement is stored per capability (text version, who, when), for example for Fee follow-up: "Dhruva reads fee dues and drafts messages; a person sends them."

**TFC-AIC-003 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can switch each AI capability on or off independently, at any scope in TFC-CON-005.
- Acceptance: Given `ai.cover_suggestions` On and `ai.timetable_generator` Off, When the coordinator opens Cover, Then free-teacher suggestions appear and the "Generate timetable" button is absent.
- Rules: Turning a capability on requires consent (001), plan (PLN), its module, quota not hard-stopped, and approval where the catalogue says `Y-on`.

**TFC-AIC-004 · Must · MVP · flag: core · [Spec]**
Each AI capability shall carry a "human approval required" policy with one of three values: Locked on, Default on, or Optional, with the starting values below.

| Policy | Capabilities | Rule |
|---|---|---|
| Locked on (cannot be relaxed by any tenant) | `ai.fee_followup`, `ai.payroll_checks`, `ai.bank_matching`, `ai.admissions_scoring`, `ai.at_risk_detection`, `ai.counselling_assist`, `ai.hr_assist`, `ai.student_tutor`, `ai.reply_drafts`, `ai.notice_drafts`, `ai.timetable_generator`, `ai.paper_generator`, `ai.lesson_plan_drafts` | Output is a suggestion or draft; a person approves before any record changes or any family is reached. Matches designed rule: "It never changes a record or messages a family on its own." |
| Default on, relaxable by TA with two-person approval | `ai.marks_from_photo`, `ai.homework_marking`, `ai.remedial_grouping`, `ai.cover_suggestions`, `ai.exam_planning` | Starting value "Teacher or owner confirms". Relaxing writes an audit event with the reason |
| Optional | `ai.assistant_chat`, `ai.focus_card`, `ai.voice_input`, `ai.translation`, `ai.security_triage`, `ai.transport_alerts`, `ai.whatsapp_bot` | Read-only answers or text transforms; no record changes |

- Acceptance: Given `ai.fee_followup`, When an admin opens the approval policy, Then the control shows "Required (set by DhruvaOne)" and cannot be changed.
- Acceptance: Given `ai.marks_from_photo`, When the admin selects "Publish after teacher check only" instead of "Publish at once", Then the change needs a second approver.
- Rules: The designs show marks and learning plans publishing without a teacher review step (and attendance with Undo) as an open decision with the client; the spec default is "teacher confirms" until the client confirms (see 4.8).

**TFC-AIC-005 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can choose which roles see each AI feature, including hiding Dhruva entirely from some roles, using the scope picker's role selector.
- Acceptance: Given `ai.assistant_chat` Off for role "Student" and "Parent", When a student opens the app, Then the orb is not shown; staff keep it.
- Rules: AI-generated content is always labelled "Prepared by Dhruva" wherever shown, in every role (not switchable).

**TFC-AIC-006 · Must · MVP · flag: core · [Spec]**
The system shall enforce a monthly AI quota per tenant, in AI credits (a unit that normalises model cost), with warnings and a hard stop.
- Acceptance: Given a quota of 100,000 credits, When usage reaches 80%, Then admins receive "AI use is at 80% of this month's allowance"; at 100% a banner "AI paused until 1 Nov or until your plan is topped up" shows and AI calls return 429 `AI_QUOTA_EXCEEDED`.
- Rules: Warning thresholds 50%, 80%, 100% (admin can add one more). Allowance comes from the plan; Platform Owner can add a one-off top-up. Tenant admin may set a lower soft cap, per campus allotment (group), and per-capability caps. 10% of allowance is reserved for safety-related capabilities (`ai.security_triage`, `ai.transport_alerts`) so they are not starved. Manual flows are never affected. Month = calendar month in Asia/Kolkata; unused credits do not roll over.

**TFC-AIC-007 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can set data-use options for AI, with these starting values.

| Setting | Options | Default | Who |
|---|---|---|---|
| Use school data to improve DhruvaOne models | Off / On (not available for student personal data) | Off | TA, with approval; Platform Owner may hide |
| Keep AI prompts and outputs | 0 days / 30 days / 90 days | 30 days | TA |
| Hide personal details sent to the model (names, phone numbers) where the task allows | On / Off | On | TA |
| Sources Dhruva may read | Per module tick list (each module the tenant has on) | All switched-on modules except counselling notes | TA; counselling notes excluded unless `ai.counselling_assist` is on |
| Location of processing | India region | India (fixed) | PO only |

- Acceptance: Given "Keep AI prompts and outputs = 0 days", When a prompt is processed, Then no prompt text is stored beyond the request; usage counts and the audit entry (who, which capability, record ids) are still kept.

**TFC-AIC-008 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can press "Pause all AI" to switch every AI capability off at once, without approval, and can resume later; the Platform Owner has equivalent switches per capability, per tenant, or global.
- Acceptance: Given "Pause all AI" is confirmed with a reason, When the next request arrives, Then all `ai.*` evaluate Off with `TENANT_SETTING (paused)` within 60 seconds; the AI tab shows "Paused by <name> on <time>"; "Resume AI" restores the previous states from the pause snapshot.
- Rules: Pause is risk-reducing, so it needs no second approver. Resume of Y* capabilities needs the approval those capabilities already need.

**TFC-AIC-009 · Should · MVP · flag: core · [Spec]**
Each AI feature has a rollout stage: Off, Shadow, Pilot, Live; the admin chooses a stage and, for Shadow and Pilot, a test audience.

| Stage | Meaning |
|---|---|
| Off | Not running |
| Shadow (test mode) | Runs on real inputs but outputs go only to a review queue seen by the admin and named testers; nothing reaches any record, user, or family; usage counts against quota |
| Pilot | Live for a named subset (campuses, roles, user groups, up to N people) with a "Pilot" tag on outputs and a feedback button ("Useful / Not right") |
| Live | Everyone in scope |

- Acceptance: Given `ai.timetable_generator` in Shadow for the coordinator group, When a coordinator generates a timetable, Then the draft appears only under "Dhruva test results" visible to testers and the admin, and no publish button exists.
- Rules: Promotion from Pilot to Live for Y or Y* capabilities follows the approval rule. Stage changes are audited.

**TFC-AIC-010 · Must · MVP · flag: core · [Spec]**
The system shall guarantee that the manual path for every task works when its AI feature is off, in every state (Off, Paused, quota stopped, consent missing, outage).
- Acceptance: Given all `ai.*` Off, When a teacher takes attendance, enters marks, posts a notice, and applies for leave, Then every task completes without error and without any AI prompt.
- Rules: This is a release gate: each module section's acceptance tests run with all AI off.

### Approvals for risky changes (APR)

**TFC-APR-001 · Must · MVP · flag: core · [Spec]**
The system shall classify each change as Immediate (applies at once) or Needs approval, using the catalogue's Appr column and these rules: risk-reducing changes (switching an AI feature off, pausing AI, narrowing scope) are Immediate; risk-increasing changes (turning on or widening a `Y-on` or `Y` feature, relaxing human approval, disabling an `Y-off` or `Y` module) need approval.
- Acceptance: Given the admin turns on `ai.payroll_checks`, When saved, Then the change request status is "Waiting for second approver" and nothing changes until approved.

**TFC-APR-002 · Must · MVP · flag: core · [Spec]**
The system shall apply a two-person rule: the approver must be a different person from the requester, with equal or higher authority, who sees the same impact preview and reason.
- Acceptance: Given the requester is also the only possible approver, When they press Approve, Then it fails with `SELF_APPROVAL_NOT_ALLOWED`.
- Rules: Two-person rule applies at minimum to: AI touching fees (`ai.fee_followup`), payroll (`ai.payroll_checks`), marks (`ai.marks_from_photo`, `ai.homework_marking`), bank (`ai.bank_matching`); disabling or enabling `mod.fees`, `mod.payroll`, `mod.finance_accounts`, `mod.approvals`; relaxing a human-approval policy; changing approval limits (TFC-SET-005); and any change to `idm.app_pin`.

**TFC-APR-003 · Must · MVP · flag: core · [Spec]**
Where a Campus Principal's delegation is "Request", or a principal asks for a campus override of a `Y-on` feature, the Group Owner (or a Group Admin delegated for approvals) shall approve.
- Acceptance: Given a request by Ms. Neelam Mehra for `ai.cover_suggestions` at Gurugram Sec 45, When the Group Owner opens Approvals, Then the card reads "Gurugram Sec 45 asks to turn on Cover suggestions" with the reason, the impact preview, and buttons "Approve" and "Decline"; approving shows "Approved · Gurugram Sec 45 notified" (same wording pattern as the designed approvals).
- Rules: These requests use the existing Approvals tab (owner) and bell (principal), as for concessions.

**TFC-APR-004 · Must · MVP · flag: core · [Spec]**
For a standalone school the second approver is the trustee (chairperson); where no trustee exists, a second admin account ("Deputy admin") can approve; where neither exists, the Platform Owner (Platform Support) can approve after identity check, and the school sees "Approved by DhruvaOne support".
- Acceptance: Given a standalone school with no trustee and no deputy admin, When the admin submits a Critical change, Then the request shows "Needs a second person. Add a deputy admin or ask DhruvaOne support."
- Rules: Open question 4.8 whether the trustee should be given this duty.

**TFC-APR-005 · Must · MVP · flag: core · [Spec]**
A pending change request shall expire after 7 days (reminder at day 3 and day 6), can be withdrawn by the requester, and can be declined by the approver with a required comment.
- Acceptance: Given a request waiting 7 days, When the clock passes, Then status becomes "Expired", nothing is applied and the requester is told.

**TFC-APR-006 · Must · MVP · flag: core · [Spec]**
Approved changes with a schedule shall be applied at their start time, re-checked at apply time (entitlement, consent, blocking conditions, dependencies), and cancelled with a notice if a check now fails.
- Acceptance: Given an approved change scheduled for 2 Nov and a plan that expires on 1 Nov, When the clock reaches 2 Nov, Then the change is cancelled with reason `PLAN_EXPIRED` and both parties are notified.

### Audit, history, snapshots and rollback (AUD)

**TFC-AUD-001 · Must · MVP · flag: core · [Spec]**
The system shall write an immutable audit event for every change of feature configuration, consent, plan, entitlement, kill switch, delegation, tenant setting, approval, rollback, and console export.
- Acceptance: Given any change, When applied, Then exactly one audit event per changed feature exists within 2 seconds, and no API or user, including Platform Owner, can edit or delete it.
- Rules: Storage is append-only with a hash chain (each event stores the previous event's hash) and write-once retention; a nightly job verifies the chain and raises a Platform Security alert on a break. Matches the website claim "100% of changes in an audit trail".

**TFC-AUD-002 · Must · MVP · flag: core · [Spec]**
Each audit event shall record: event id, tenant, actor (id, name, role), when (UTC and tenant time), feature key, scope before and after, effective-state summary before and after, reason, change request and approval ids, approver, schedule, impact preview numbers, source IP, device and app (browser or app version), and request id.
- Acceptance: Given a change by Mrs. Meena Sharma, When the event is opened, Then it shows all fields above and a diff of the rules; fields not known (IP for system actions) show "System".

**TFC-AUD-003 · Must · MVP · flag: core · [Spec]**
Tenant admins can view and filter the audit log (by feature, person, date, scope, type) and export it (CSV or JSON, signed with a checksum), and the Campus Principal sees only their campus.
- Acceptance: Given a filter "AI, last 30 days", When exported, Then the file arrives within 60 seconds for up to 100,000 events (larger exports run in the background with a notification), and a "Export of audit log" event is itself written.
- Rules: Audit export is a business-customer feature (website) and is gated by the plan flag `mod.audit_export`; viewing the log is available on every plan.

**TFC-AUD-004 · Must · MVP · flag: core · [Spec]**
Audit events shall be retained for 7 years by default (configurable 3 to 10 years by Platform Owner per contract), then deleted with a deletion record; event content never contains student personal data beyond ids.
- Acceptance: Given an event older than the retention period, When the monthly job runs, Then it is removed and a summary "Removed 12,481 events older than 7 years" is written.

**TFC-AUD-005 · Must · MVP · flag: core · [Spec]**
The system shall take a configuration snapshot automatically after every applied change batch and every day at 02:00 IST, and the admin can create named snapshots ("Before Term 2").
- Acceptance: Given 5 changes applied in one bulk action, When completed, Then one snapshot exists labelled with the change request id; snapshots list shows date, author, label, number of features differing from current.
- Rules: Keep the last 200 or 24 months, whichever is larger; named snapshots are kept until deleted by TA with approval.

**TFC-AUD-006 · Must · MVP · flag: core · [Spec]**
The admin can preview and restore a previous snapshot in one confirm, creating a normal change request that is subject to plan, consent, dependency, lock and approval checks.
- Acceptance: Given snapshot S-1042 selected, When "Compare with now" is pressed, Then a diff lists each feature and rule that would change, with items that cannot be restored marked "Cannot restore: not in your plan" or "Needs approval"; "Restore" applies the rest after the reason is given.
- Rules: Rollback restores configuration only, not data, drained drafts or cancelled queues. Rolling back is audited as `config.rolled_back` with the source snapshot id. A rollback never overrides a platform kill switch.

### Runtime (RUN)

**TFC-RUN-001 · Must · MVP · flag: core · [Spec]**
The system shall provide a central flag evaluation service used by all backends, web, mobile and WhatsApp bot, so there is one decision logic.
- Acceptance: Given the same context, When evaluated from the web, app, WhatsApp bot and a background job, Then the result and reason are identical.

**TFC-RUN-002 · Must · MVP · flag: core · [Spec]**
The evaluation context shall include: tenant id, campus id, role, profile id, user id, user groups, channel (web, ios, android, whatsapp, job), app version, and time.
- Acceptance: Given a missing tenant id, When evaluated, Then the result is Off with `NO_CONTEXT`.
- Rules: One phone number with several profiles evaluates per profile; profiles never mix.

**TFC-RUN-003 · Must · MVP · flag: core · [Spec]**
The system shall expose the call shape `isEnabled(key, ctx) -> {enabled, reason, stage}` in the backend library and client SDKs, plus a bulk `evaluateAll(ctx)` returning the whole map for the profile.
- Acceptance: Given a client SDK, When `evaluateAll` is called at sign-in or profile switch, Then it returns every key with enabled and stage in one response under 100 KB and the app renders from it.

**TFC-RUN-004 · Must · MVP · flag: core · [Spec]**
The system shall propagate a configuration change to all enforcement points within 60 seconds for 95% of changes and within 5 minutes for 99.9%.
- Acceptance: Given a change is applied at T, When any API request is made at T+60 s, Then it sees the new state in at least 95% of 1,000 test changes.
- Rules: Mechanism: change publishes `feature.changed`; the evaluation service invalidates its cache and notifies clients (web by server push, apps by push or foreground poll); server cache TTL 30 s; client cache TTL 60 s.

**TFC-RUN-005 · Must · MVP · flag: core · [Spec]**
Server-side enforcement is mandatory: every API route and job that belongs to a feature shall declare its flag and be rejected by middleware when Off, regardless of what the client shows.
- Acceptance: Given a rooted or modified client forces a hidden button, When it calls the endpoint, Then the response is 403 `FEATURE_DISABLED`.
- Rules: A route without a declared flag fails CI. Client flag checks are for presentation only. Data fields written by a switched-off feature are rejected, not silently dropped.

**TFC-RUN-006 · Must · P2 · flag: core · [Spec]**
The mobile app shall cache a signed flag snapshot for offline use and apply these rules when offline.

| Case | Behaviour |
|---|---|
| Snapshot age up to 72 hours | Use it; modules usable |
| AI features | Cached snapshot valid for 24 hours; after that treated Off |
| Safety and core | Always available |
| Actions queued offline | On sync the server evaluates the feature at the action's time against the change time; if the action was created before the feature was switched off it is accepted and flagged; otherwise rejected with "Not saved: <feature> was switched off at <time>" |
| Kill switch | Takes effect when the app next reaches the server; actions queued during the kill window are rejected |

- Acceptance: Given attendance marked offline at 8:50 and `mod.attendance` switched off at 9:10, When the phone syncs at 9:30, Then the attendance is accepted and flagged "Marked before Attendance was switched off".
- Rules: Offline mode itself is a Phase 1 item in the roadmap.

**TFC-RUN-007 · Should · MVP · flag: core · [Spec]**
The system shall log evaluations: every denial with reason (sampled at 100% for High and Critical features, 10% for others, capped per tenant), allowed decisions of High and Critical features, and 1% of other allows, and show counts per feature per day in the Platform Owner console and a "Blocked attempts" tab for the tenant admin.
- Acceptance: Given 50 blocked calls to a disabled feature, When the admin opens "Blocked attempts", Then they see the count by day and role, and no personal data of the callers beyond role and campus.
- Rules: Evaluation logs are kept 30 days.

**TFC-RUN-008 · Must · MVP · flag: core · [Spec]**
If the evaluation service cannot be reached, enforcement points shall use their last good local copy (TTL up to 10 minutes, then up to 24 hours for non-AI), and shall fail closed for AI and for kill-switched items.
- Acceptance: Given the service is unreachable for 30 minutes, When a user opens a module, Then it works from the local copy; AI calls are refused with `FEATURE_DISABLED` reason `EVAL_UNAVAILABLE`.

**TFC-RUN-009 · Should · P2 · flag: core · [Spec]**
The Platform Owner can set a minimum app version per feature so a feature runs only on clients that support it, and the context includes `app_version`.
- Acceptance: Given `ai.voice_input` requires app 2.5, When a user on 2.4 signs in, Then the feature is Off with `APP_VERSION_TOO_LOW` and the app suggests updating.

### Notifications to affected people (NOT)

**TFC-NOT-001 · Must · MVP · flag: core · [Spec]**
When a feature changes for a group of people, the system shall tell the affected roles in plain words, in their language (English or Hindi), as a Normal-tier notification and an in-app banner.
- Acceptance: Given Marks from photo is switched off for teachers on 2 Nov, When applied, Then each affected teacher sees "From Mon 2 Nov, Marks from photo is switched off. Type marks or upload the sheet as before." and the Marks screen shows the same line for 7 days.
- Rules: Parents and students are told only when a feature they used goes away or arrives (for example "Bus live board is not available at your school now"); admin-written optional "Message to users" (up to 200 characters, reviewed in the preview) is appended. Quiet hours apply; safety exceptions do not apply because these notices are not safety.

**TFC-NOT-002 · Should · MVP · flag: core · [Spec]**
For scheduled switch-offs the system shall send an advance notice: 3 days before for modules and channels, 24 hours before for AI, none for kill switches (immediate).
- Acceptance: Given a switch-off scheduled for 2 Nov, When the clock reaches 30 Oct at the same time, Then affected roles get "Homework will be switched off on 2 Nov".
- Rules: The admin can untick advance notice per change with a reason.

**TFC-NOT-003 · Must · MVP · flag: core · [Spec]**
The system shall notify admins and approvers of: a change requested for them to approve, approved, declined, expired, applied, failed at apply time, rolled back, plan expiring (30, 7 and 1 days before), AI quota thresholds, consent renewal, and platform kill switches affecting them.
- Acceptance: Given a platform kill switch on `ai.marks_from_photo`, When activated, Then Tenant Administrators receive a High-tier notice "Marks from photo is paused by DhruvaOne. We will tell you when it is back." within 60 seconds and the chip becomes "Paused by DhruvaOne".
- Rules: Group tenants also notify the affected campus principals; standalone tenants notify the trustee for approval items only.

**TFC-NOT-004 · Could · P2 · flag: core · [Spec]**
The system shall offer an in-product "What changed" list per profile, showing the last 30 days of feature changes that affect them.
- Acceptance: Given a teacher, When opening "What changed" in Me, Then they see only items that affected their role or campus.

### Plans and entitlements (PLN)

**TFC-PLN-001 · Must · MVP · flag: core · [Spec]**
The Platform Owner can define plans (initially Essentials, Standard, Premium), each with a list of entitlements per catalogue key (`included-on`, `included-off`, `excluded`), limits (AI credits per month, campus count, WhatsApp message volume, audit export) and an AI quota.
- Acceptance: Given a new plan version, When published, Then existing tenants stay on their current plan version until moved; each plan version is immutable once published.

**TFC-PLN-002 · Must · MVP · flag: core · [Spec]**
The Platform Owner can set per-tenant entitlement overrides: add a feature not in the plan (add-on), remove one, change limits, each with a reason and optional end date.
- Acceptance: Given Karnal on Standard with an add-on for `ai.marks_from_photo` ending 31 Jan 2027, When evaluated before that date, Then plan level passes; after it, `PLAN_LOCKED`.
- Rules: Overrides are audited and shown to the tenant admin as "Included by special arrangement until <date>".

**TFC-PLN-003 · Must · MVP · flag: core · [Spec]**
The Platform Owner can start a trial for a tenant or for a set of features, with an end date; trial features show a "Trial · ends <date>" tag.
- Acceptance: Given a 30-day trial of Full AI, When day 23 arrives, Then admins receive a notice 7 days before expiry; on expiry, trial features evaluate Off unless converted.

**TFC-PLN-004 · Must · MVP · flag: core · [Spec]**
On plan expiry the system shall apply a grace period (default 14 days) with full function and a banner, then switch paid features Off with reason `PLAN_EXPIRED`, while keeping core, safety, sign-in, and data export, and keeping all school data read-only for 90 days.
- Acceptance: Given expiry on 31 Mar 2027, When 14 days pass without renewal, Then non-core features evaluate Off from 15 Apr; admins can still sign in, see read-only data and download the export; on renewal everything returns exactly as configured.
- Rules: Data deletion after exit follows the website Trust rule (deletion 90 days after exit with written confirmation) and is run by a Platform Admin process, not by flags.

**TFC-PLN-005 · Must · MVP · flag: core · [Spec]**
On downgrade the system shall show a "What you will lose" preview (features, people affected, data kept read-only), require the admin to confirm, take effect at the end of the billing period, and keep tenant settings dormant (not deleted).
- Acceptance: Given Premium to Standard, When confirmed, Then at period end features not in Standard evaluate Off with `PLAN_LOCKED`; AI quota reduces; running payroll or batch runs follow TFC-DIS-010; and an upgrade later restores the dormant settings.
- Rules: AI consent remains valid.

**TFC-PLN-006 · Should · MVP · flag: core · [Spec]**
On upgrade, new entitlements appear immediately as `included-off` (or on, per plan default), and the console shows "New with your plan" badges for 30 days.
- Acceptance: Given an upgrade, When the admin opens Features, Then newly available features show "New" and none switches on by itself if it is AI.

### Tenant-level settings (SET)

Only settings that the designs or the product rules justify; each is explained.

**TFC-SET-001 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can open a "School settings" page with these groups only: Identity, Notifications, Language, Approval limits, Data retention, WhatsApp channel; each change is audited like a feature change.
- Acceptance: Given the page, When opened, Then six groups show with last-changed information; Campus Principals see only their campus's values where delegated.

**TFC-SET-002 · Should · MVP · flag: core · [Design]**
The Tenant Administrator can set the display name, short name and logo of the tenant, from which the logo-colour theme of campuses and compare views is derived.
- Acceptance: Given a logo upload (PNG or SVG, up to 1 MB), When saved, Then the app header, WhatsApp account picture and the owner's theme colours update within 5 minutes.
- Rules: The designs show a school logo in the WhatsApp header, campus name and short name fields in campus setup, and a logo-colour glow theme for owner views; no other branding is specified, so none is offered.

**TFC-SET-003 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can set tenant default quiet hours (design default 9 pm to 7 am); parents and users may still change their own; safety alerts and early pickups ignore quiet hours and cannot be turned off.
- Acceptance: Given tenant quiet hours 9 pm to 7 am, When a Normal item is raised at 9:30 pm, Then it waits until 7 am; an Urgent safety alert goes immediately.
- Rules: Designs show two values (9 pm to 7 am in the notification rules and 9 pm to 6 am in one settings board); this spec uses 7 am as default and flags it in 4.8. Tenant admin also sets who may send notices ("the school sets who can send notices"), by role.

**TFC-SET-004 · Should · MVP · flag: core · [Spec]**
The Tenant Administrator can set the default language (English or Hindi, the confirmed pair) and which languages are offered; users choose their own at sign-in.
- Acceptance: Given default Hindi, When a new user signs in, Then the language screen pre-selects Hindi; they can change it in Me > Language.
- Rules: Punjabi, Gujarati, Marathi and Tamil are shown in the language list design but are Phase 1; the setting lists them as "Coming soon".

**TFC-SET-005 · Must · MVP · flag: mod.approvals · [Design]**
The Group Owner (or standalone School Admin with trustee) can set approval limits by item: fee concessions above a campus limit go to the owner (design example ₹25,000); purchases above ₹50,000 go to the principal and above ₹5 L to the owner; finance second approval above ₹2 L; leave: HoD up to 2 days, principal up to 3 days.
- Acceptance: Given a campus concession limit changed from ₹25,000 to ₹30,000, When saved, Then it needs the two-person rule and is applied from the next request (open requests keep their routing).
- Rules: The limits are design examples; the semantics of each approval are in the module sections. "Approval limits" is one of the five items a new campus can copy from another campus (design). Fee amounts are never copied.

**TFC-SET-006 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can view, and within bounds set, data retention periods.

| Data | Default | Range | Source |
|---|---|---|---|
| School records after exit from DhruvaOne | Deleted 90 days after exit with written confirmation | fixed | Design (website Trust) |
| AI prompts and outputs | 30 days | 0 / 30 / 90 | Spec |
| WhatsApp chat log | 12 months | 6 to 24 months | Spec |
| Voice-note audio | 7 days after transcription | 0 to 30 days | Spec |
| Marks-sheet photos | 90 days | 30 to 365 days | Spec |
| Audit events | 7 years | 3 to 10 years, Platform Owner only | Spec |

- Acceptance: Given "WhatsApp chat log = 6 months", When the nightly job runs, Then older chats are deleted and a count is written to the audit log.

**TFC-SET-007 · Must · MVP · flag: ch.whatsapp · [Design]**
The Tenant Administrator (or campus admin) can view WhatsApp channel status for the school number ("+91 124 XXX XXXX · verified", "Live") and set the four toggles of TFC-DIS-009 plus the per-audience switches Parents, Teachers, Staff.
- Acceptance: Given the number is not yet verified, When the admin opens the card, Then status reads "Setup needed" and `ch.whatsapp` cannot be switched on (`SETUP_INCOMPLETE`).
- Rules: Template approval and costs per alert are provider matters (open item in the WhatsApp design).

### Group, campus and standalone hierarchy (HIE)

**TFC-HIE-001 · Must · MVP · flag: core · [Spec]**
The system shall support two tenant types, "group" (2 to 50 campuses) and "standalone" (one school), with the same engine: a standalone school is a tenant with one implicit campus, the campus selector is hidden, and its administrator is the School Admin.
- Acceptance: Given Saraswati Vidya Niketan, When opening the scope picker, Then only "Whole school", roles and user groups appear.

**TFC-HIE-002 · Must · MVP · flag: core · [Spec]**
Settings flow down: tenant to campus to role to user group; lower levels inherit and may override only what the delegation policy and locks allow; a group's change never reaches another tenant.
- Acceptance: Given a tenant setting is changed, When a campus has no override, Then it inherits within 60 seconds; if it has an override the override stands and the console shows "Campus differs" on the tenant row.

**TFC-HIE-003 · Must · MVP · flag: mod.campus_onboarding · [Spec]**
A new campus shall inherit the tenant's feature state and delegation policies at creation, and the add-campus journey can copy another campus's feature overrides as an extra option beside the designed five settings copies.
- Acceptance: Given adding a campus with "Copy features and AI settings from Gurugram Sec 45", When the journey finishes, Then the new campus has the same overrides, none of the approvals or consents are copied, and the audit event reads "Created from Gurugram Sec 45".
- Rules: Design needed: the add-campus step 3 "Settings" shows five copies; "Features" is a proposed sixth.

**TFC-HIE-004 · Should · MVP · flag: core · [Spec]**
The Tenant Administrator can tie a feature change to a campus go-live batch, so that features switch on at the batch's go-live date for the campuses of that batch.
- Acceptance: Given Batch 2 goes live on 19 Jan (R.K. Puram, Noida, Faridabad, Lucknow), When the admin chooses "Turn on with Batch 2", Then four campus rules are created with start = 19 Jan 00:00; if the batch date moves, the rules move and the admin is notified.
- Rules: Pilot-first pattern from the designed rollout: Gurugram Sec 45 pilots on 5 Jan, other batches follow every two weeks.

**TFC-HIE-005 · Must · MVP · flag: core · [Spec]**
If a campus is moved out of a group or a group is dissolved, the campus's rules shall be archived, the campus's AI consent is not carried to a new tenant, and a snapshot is taken before the move.
- Acceptance: Given a campus leaves, When the move completes, Then the old tenant's audit keeps the history and the new tenant starts with plan defaults.

### Platform Owner console (PLT)

**TFC-PLT-001 · Must · MVP · flag: core · [Spec]**
The Platform Owner console shall list all tenants with: name, type (group or standalone), campuses, users, plan, plan status (active, trial, grace, expired), AI usage vs quota, last configuration change, open kill switches, and health flags.
- Acceptance: Given 300 tenants, When filtered by "Grace period", Then the list returns within 2 seconds; clicking a row opens tenant detail.

**TFC-PLT-002 · Must · MVP · flag: core · [Spec]**
Tenant detail shall show plan and overrides, the effective feature grid, consent records, quota usage by capability, change history and approvals, and the platform actions: change plan, add override, start trial, add AI top-up, set grace, suspend.
- Acceptance: Given a suspended tenant, When a user signs in, Then they see "Your school's account is paused. Contact the school office." and safety alerts continue for 7 days.
- Rules: The console never shows school records (students, fees, marks), only configuration and counts.

**TFC-PLT-003 · Must · MVP · flag: core · [Spec]**
Platform Security and Platform Admin can set a kill switch: global (feature, all tenants), per feature version or app version, or per tenant; with a reason, an expected duration and a message shown to admins; one person can switch on, and a second person must lift a global one.
- Acceptance: Given a global kill on `ai.whatsapp_bot` at 11:02, When any tenant's user chats on WhatsApp at 11:03, Then Dhruva replies with the button menu only, and the tenant admins see "Paused by DhruvaOne".
- Rules: A kill switch beats every tenant setting; it never destroys data; every use is audited and visible to affected tenants.

**TFC-PLT-004 · Should · MVP · flag: core · [Spec]**
The console shall show usage: per tenant and per feature, active users, calls, blocked calls, AI credits, WhatsApp messages; and a "feature adoption" view across tenants.
- Acceptance: Given a feature, When opened, Then it shows tenants with it on, number of tenants with Off or scoped, and a 30-day trend.

**TFC-PLT-005 · Should · MVP · flag: core · [Spec]**
Platform Support can use "View as tenant admin (read only)" only when the tenant admin has granted a time-limited consent (default 4 hours), with every view audited and visible to the tenant.
- Acceptance: Given consent is granted, When the 4 hours pass, Then access ends and the tenant's audit shows who looked and when.

**TFC-PLT-006 · Must · MVP · flag: core · [Spec]**
The Platform Owner can maintain the catalogue and plan definitions (TFC-FLAG-001, PLN-001) and can see which tenant would be affected before publishing a change.
- Acceptance: Given a change that removes `ai.remedial_grouping` from Standard, When previewed, Then it lists the tenants where it is currently On.

## 4.4 Business rules and policies

1. **Plan is a ceiling.** No tenant, campus, or user setting can enable anything the plan does not include (TFC-RES-001).
2. **Most specific wins, locks stop it.** Within the layered levels the narrower setting wins unless a higher level locks (TFC-RES-003).
3. **Safe direction is easy; risky direction is checked.** Turning AI off or narrowing is immediate; turning on or widening Critical features needs a second person (TFC-APR-001).
4. **AI never acts alone.** AI drafts and suggests; a person approves anything that changes a record or reaches a family; this is unchangeable for the capabilities listed as Locked on (TFC-AIC-004).
5. **Manual always works.** Every AI feature has a manual alternative that is unaffected when AI is off (TFC-AIC-010).
6. **Data stays.** A switch hides and blocks; it never deletes (TFC-DIS-005). Deletion is only by retention rules and exit.
7. **Money and safety are never dropped** (TFC-DIS-004).
8. **Server decides.** The client display is a courtesy; the server enforces (TFC-RUN-005).
9. **Nothing is silent.** Every change is audited and the affected people are told (TFC-AUD-001, TFC-NOT-001).
10. **Platform above tenant.** The Platform Owner can pause anything for safety; the tenant sees it, cannot override it, and is told.
11. **Separate tenants.** No setting, snapshot, or evaluation ever crosses tenants; a group never reaches a standalone school.
12. **Approval limits (reminder, from designs).** Concessions above the campus limit go to the owner; purchases above ₹50,000 to the principal and above ₹5 L to the owner; the owner does not change campus data directly (the owner changes feature switches, not records); a standalone trustee approves the admin's own leave, salary and fee waivers and may read only the payroll and refund log.

## 4.5 Notifications and approvals raised by this section

| Event | To | Tier | Message pattern | Opens |
|---|---|---|---|---|
| Change request waiting | Approver | Normal | "Meena Sharma asks to turn on Payroll checks. Review" | Approvals |
| Request approved or declined | Requester | Normal | "Approved: Payroll checks. It is on from 2 Nov" / "Declined: <comment>" | Feature drawer |
| Request expired | Requester | Normal | "Your request expired after 7 days" | Request |
| Feature switched off or on for my role | Affected roles | Normal | "From Mon 2 Nov, Marks from photo is switched off." | Banner |
| Advance notice | Affected roles | Normal | "Homework will be switched off on 2 Nov" | Banner |
| Platform kill switch | Tenant admins, principals | High | "Marks from photo is paused by DhruvaOne." | Features |
| AI quota 50, 80, 100% | Tenant admins | Normal (High at 100%) | "AI use is at 80% of this month's allowance" | AI tab |
| Consent renewal | Tenant admins | Normal | "New AI terms. Accept by <date>" | Consent |
| Plan expiring (30, 7, 1 days) | Tenant admins | Normal (High at 1 day) | "Your plan ends on <date>" | Plan |
| Config snapshot restored | Tenant admins | Normal | "Settings restored to <snapshot>" | History |
| Scheduled change cancelled at apply time | Requester and approver | High | "Not applied: <reason>" | Request |

Approvals use the existing Approvals tab (owner) and bell (principal), with the same "Approve" and "Decline" actions and log.

## 4.6 Feature switches in this section

Feature control is itself not switchable (`core`), but it governs these switches that sit inside this section:

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| core | Console, resolution, audit, consent, kill switch | Always on | Cannot be switched by anyone |
| mod.audit_export | Audit log export | Off on Essentials; On on Standard and Premium | Viewing audit is always on |
| ch.whatsapp | WhatsApp settings card (TFC-SET-007) | Per plan | Setup must be verified first |
| mod.approvals | Approval limits setting (TFC-SET-005) | On | Cannot be off while fees, payroll or leave are on |
| mod.campus_onboarding | Copy-features option in add campus (TFC-HIE-003) | On for groups | Group only |

## 4.7 Non-functional requirements (specific to this section)

| Area | Requirement |
|---|---|
| Propagation | 95% of changes seen by every enforcement point within 60 seconds; 99.9% within 5 minutes (TFC-RUN-004) |
| Evaluation latency | `isEnabled` in-process: p99 under 1 ms from cache; remote evaluation p99 under 50 ms; `evaluateAll` under 150 ms |
| Availability | Evaluation service 99.95%; local copy fallback (TFC-RUN-008) |
| Throughput | 5,000 evaluations per second per region at launch; scales horizontally |
| Console performance | Features page loads within 2 seconds for 200 campuses and 100 users per drawer open; impact preview within 2 seconds up to 5,000 users |
| Audit durability | No acknowledged event lost; replicated across zones in India region; 7-year retention default |
| Security | Console access needs staff PIN or biometric (web re-PIN after 15 minutes, as designed); admin actions require recent sign-in (within 15 minutes) for High and Critical changes; all traffic encrypted; platform actions need Platform staff MFA |
| Data residency | Configuration, audit and consent stored in India region only |
| Privacy | Audit and evaluation logs hold ids and roles, not student personal data |
| Scale limits | Rules per feature 200; features per tenant about 100; scheduled changes per feature 10; user group size 5,000; groups per tenant 200 |
| Accessibility | See TFC-CON-015 |
| Test | Each feature has an automated test that proves the server rejects with 403 when Off and the manual path works |

## 4.8 Open questions

**Decisions needed from the client or product owner**
1. Plan names, tiers and what each includes: Essentials, Standard, Premium are placeholders; confirm the entitlement columns of the catalogue.
2. Should the trustee (chairperson) of a standalone school be the second approver for risky feature changes? The design gives the trustee only the admin's own leave, salary, fee waivers and a read-only payroll and refund log.
3. Marks from photo and learning plans publish without a teacher review step in the designs (attendance with Undo). This spec defaults to "teacher confirms"; confirm or change TFC-AIC-004.
4. Should a Group Admin role exist, and what may it do (TFC-ACT-002)? Not in the designs.
5. Default AI quota amounts per plan, and what a credit costs.
6. Quiet hours: 9 pm to 7 am or 9 pm to 6 am (the designs disagree).
7. Retention numbers in TFC-SET-006 (except the 90-day post-exit rule and audit claim) are proposals; confirm with the school's legal adviser.
8. Audit export as a plan feature ("Audit exports for business customers" on the website) versus on every plan.
9. In a standalone school, who are "Class 9 to 12 coordinators" (the client's own example)? The designs show Academic coordinator only in the group; we model it as a role plus a user group.
10. Whether parents consent per child for AI features that process their child's data (website says "parental consent per child under 18"); how that links to TFC-AIC-001 (see Section 3 Identity).
11. Phasing: which flags exist in MVP (Oct-Dec 2026) versus Phase 1 (for example the timetable generator, Dhruva on WhatsApp, Tally sync, full payroll are Phase 1 in the roadmap but prototyped now).
12. Grace period (14 days) and read-only period (90 days) after plan expiry.

**Design needed (screens that do not exist yet)**
1. Tenant Administration home and navigation entry (where it lives in the admin, owner and standalone admin apps).
2. Features page: list, search, filters, chips, bulk bar, compare campuses grid, export.
3. Feature drawer: rules table, scope picker, schedule, reason, impact preview, "Why is this on or off?" explainer.
4. AI tab: consent terms and acceptance, per-capability toggles, human-approval policy, rollout stage and test audience, quota meter, data-use settings, "Pause all AI".
5. Change request and approval cards in the Approvals tab (owner) and the principal's bell; trustee read-only view.
6. Audit log viewer, export dialog, snapshots list and rollback diff view.
7. Plan and entitlements view for the tenant; downgrade preview; trial and expiry banners.
8. School settings page (six groups).
9. Platform Owner console: tenant list, tenant detail, kill switches, usage, catalogue and plan editors, "view as" consent.
10. End-user states: "Switched off for your school" page, "Paused by DhruvaOne" message, WhatsApp reply when a feature is off, on-hold approval card, "Drafts · switched off" list, change banners, "What changed".
11. Phone versions of the pause, approve and read-only list.
12. Add-campus journey step for copying feature settings.

---

## Annex 4-A (engineering)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| Tenant | id, name, type (group, standalone), plan_id, plan_version, plan_status, timezone, default_language | Existing entity; shown for reference |
| Campus | id, tenant_id, name, status | Standalone has one implicit campus |
| FeatureDefinition | key (PK), category, display_name, description, risk, default_by_plan{E,S,P}, depends_on[], depends_mode (all, any), switch_level (PO, TA, CP), approval (N, Y-on, Y-off, Y), ai_consent (none, Y, Y*), human_approval_policy, tenant_types[], min_app_version, catalogue_version, status (active, deprecated) | Source of truth; versioned |
| Feature | tenant_id, key, base_state (on, off), version (int), locked_below (none, campus, role), delegation (none, narrow, request, full), rollout_stage (off, shadow, pilot, live), updated_by, updated_at | TenantFeatureState row for the tenant base; one per tenant per key |
| TenantFeatureState | alias of Feature; holds computed `effective_summary` (on, off, some) for the console | Denormalised for list view |
| ScopeRule | id, tenant_id, key, effect (enable, disable), campuses[], roles[], user_groups[], profiles[], channels[], app_versions, schedule_id, stage, source (admin, auto_parent_off, preset, batch, approval), created_by, created_at, status (active, ignored_locked, archived) | AND across selectors |
| Schedule | id, starts_at, ends_at, timezone, status (pending, active, ended, cancelled), change_request_id | Max 10 per feature |
| Plan | id, name, version, status (draft, published, retired), ai_credits_month, limits{campuses, whatsapp_msgs, audit_export} | Immutable once published |
| PlanEntitlement | plan_id, key, entitlement (included_on, included_off, excluded) | |
| TenantEntitlementOverride | tenant_id, key, entitlement, limit_override, ends_at, reason, created_by | Add-ons, removals, trials |
| Trial | tenant_id, scope (all or keys[]), starts_at, ends_at, converted (bool) | |
| ConfigSnapshot | id, tenant_id, label, kind (auto, daily, named), created_at, created_by, change_request_id, payload (rules+base states+settings), hash | Immutable |
| ChangeRequest | id, tenant_id, requested_by, status, kind (feature, bulk, preset, rollback, settings, plan), items[] (key, before, after), reason, impact_preview (json), drain_policy, schedule, group_id, approver_required (bool), expires_at, created_at | See state machine |
| Approval | id, change_request_id, approver_id, role, decision (approved, declined), comment, decided_at, ip, device | One or more per request |
| AuditEvent | id, tenant_id, seq, prev_hash, hash, type, actor{id,role}, at, key, scope_before, scope_after, effective_before, effective_after, reason, change_request_id, approval_ids[], schedule, impact_preview, ip, device, app_version, request_id | Append-only, hash chained |
| AIConsent | id, tenant_id, consent_version, text_sha256, accepted_by, role, accepted_at, ip, device, scope (all, capability key), kind (terms, capability_ack) | Never deleted |
| AIQuota | tenant_id, month, allowance_credits, used_credits, soft_cap, hard_stop (bool), per_capability_caps{}, per_campus_allotment{}, thresholds[], topup_credits | One row per tenant per month |
| AISetting | tenant_id, retain_days, redact_pii, improve_models, sources[], human_approval{key: policy}, paused (bool), paused_by, paused_at, pause_snapshot_id | |
| UserGroup | id, tenant_id, name, rule (role, grade) or members[], size | Used by ScopeRule |
| KillSwitch | id, scope (global, tenant), tenant_id, key or app_version, reason, message, set_by, set_at, expected_until, lifted_by, lifted_at | |
| EvaluationLogEntry | ts, tenant_id, key, ctx hash (role, campus, channel), result, reason, sample_rate | 30-day retention |
| TenantSettings | tenant_id, display_name, short_name, logo_url, quiet_hours, who_can_send_notices, default_language, languages[], approval_limits{}, retention{}, version | Audited like a feature |

### APIs

All paths are under `/v1` (see 2.5). Errors use the envelope `{"error":{"code","message","feature?","reason?","request_id"}}`.

| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| GET /v1/tenants/{id}/features | List features with plan state, base state, rules summary, chip, pending requests; query `category`, `q`, `status`, `campus` | TA, CP (own campus), PO | 403 `FORBIDDEN_ROLE`, 404 |
| GET /v1/tenants/{id}/features/{key} | Drawer data: rules, dependents, history, preview inputs | as above | 404 `UNKNOWN_FEATURE` |
| PUT /v1/tenants/{id}/features/{key} | Set base state, rules, lock, delegation, stage; requires `reason`, `If-Match: version`; returns a change request (applied or pending) | TA, CP within delegation | 409 `VERSION_CONFLICT`, 422 `PLAN_LOCKED`, `DEPENDENCY_OFF`, `LOCKED_BY_HIGHER_LEVEL`, `CONSENT_MISSING`, `ADMIN_LOCKOUT_PREVENTED`, `BLOCKING_CONDITION` |
| POST /v1/tenants/{id}/features/{key}/preview | Compute impact preview without saving | TA, CP | 422 |
| POST /v1/tenants/{id}/features/{key}/schedule | Add a schedule to a change (starts_at, ends_at) | TA, CP | 422 `SCHEDULE_INVALID`, `TOO_MANY_SCHEDULES` |
| DELETE /v1/tenants/{id}/features/{key}/schedule/{sid} | Cancel a scheduled change | requester, TA | 409 `ALREADY_APPLIED` |
| POST /v1/tenants/{id}/features:bulk | Apply an action to up to 100 features; supports `preset` | TA | 422 per item, 207 partial if `apply_others` |
| GET /v1/features/evaluate | Evaluate `key` or all for a context (`tenant`, `campus`, `role`, `profile`, `channel`, `app_version`); caller identity decides allowed contexts | Service tokens, signed-in client (own context only) | 400 `NO_CONTEXT` |
| GET /v1/tenants/{id}/features/{key}/explain | "Why on or off" for a person | TA, PO | 404 |
| GET /v1/tenants/{id}/change-requests, POST .../{rid}/approve, POST .../{rid}/decline, POST .../{rid}/withdraw | Approvals flow | approver, requester | 403 `SELF_APPROVAL_NOT_ALLOWED`, 409 `REQUEST_NOT_PENDING`, 410 `REQUEST_EXPIRED` |
| GET /v1/tenants/{id}/snapshots | List snapshots | TA | |
| POST /v1/tenants/{id}/snapshots | Create named snapshot | TA | |
| GET /v1/tenants/{id}/snapshots/{sid}/diff | Diff with current | TA | |
| POST /v1/tenants/{id}/snapshots/{sid}:rollback | Create rollback change request | TA | 422 per item |
| GET /v1/tenants/{id}/administrators ; POST /v1/tenants/{id}/administrators ; DELETE /v1/tenants/{id}/administrators/{profileId} | List, assign and remove Tenant Administrators and Group Admins | TA (cannot remove the last one), PO | 422 `ADMIN_LOCKOUT_PREVENTED` |
| GET /v1/tenants/{id}/hierarchy | Group, campus and standalone hierarchy with campus status | TA, PO | 404 |
| GET/POST /v1/tenants/{id}/ai/consent | Read consent state; accept terms or capability acknowledgement | Group Owner or School Admin (trustee countersign if enabled) | 403 `CONSENT_NOT_AUTHORISED`, 409 `STALE_VERSION` |
| GET/PUT /v1/tenants/{id}/ai/settings | AI settings: data use, capability toggles, human approval modes, retention | TA; principal read | 422 `LOCKED_POLICY`, 422 `CONSENT_REQUIRED` |
| POST /v1/tenants/{id}/ai:pause, POST /v1/tenants/{id}/ai:resume | Tenant kill switch | TA | |
| GET/PUT /v1/tenants/{id}/ai/quota | Read, set soft cap, per-campus allotment | TA | 422 |
| GET/PUT /v1/tenants/{id}/settings | Tenant settings (6 groups) | TA | 422 |
| GET /v1/plans, GET /v1/plans/{id}, POST /v1/plans, POST /v1/plans/{id}:publish | Plan management | PO (Platform Admin) | 409 `PLAN_PUBLISHED` |
| PUT /v1/tenants/{id}/plan, PUT /v1/tenants/{id}/entitlements/{key}, POST /v1/tenants/{id}/trial, POST /v1/tenants/{id}/ai/topup | Assign plan, overrides, trials, AI top-up | PO | 422 |
| POST /v1/platform/kill-switches, DELETE /v1/platform/kill-switches/{id} | Global or per-tenant kill and lift, including the platform AI kill (`scope: ai`) | PO (Platform Security, Platform Admin; lift needs second person) | 403 `SECOND_APPROVER_REQUIRED` |
| GET /v1/platform/tenants, GET /v1/platform/tenants/{id}, GET /v1/platform/usage | Platform console | PO | |
| Any feature route | Gated by middleware | feature flag | 403 `FEATURE_DISABLED` with `reason`; 429 `AI_QUOTA_EXCEEDED` |

Example denial body:
```json
{"error":{"code":"FEATURE_DISABLED","message":"Marks from photo is switched off for your school.","feature":"ai.marks_from_photo","reason":"ROLE_OVERRIDE","request_id":"req_8f2c1"}}
```
(`reason` is returned to admin tokens only.)

Configuration audit (feature changes, change requests, snapshots, AI settings) is read and exported through `GET /v1/audit?category=configuration` and `POST /v1/audit/exports` (Section 9); entries link to their change request and snapshot.

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| feature.changed | A change is applied | tenant, key, scope_before/after, effective_after, change_request_id, version, at | Evaluation service cache, client push, audit, notifications |
| feature.scheduled | A schedule is created or edited | key, starts_at, ends_at | Scheduler, notifications |
| feature.schedule_fired | A schedule starts or ends | key, direction, at | Evaluation service, notifications |
| feature.apply_failed | A scheduled or approved change failed its re-check | key, reason | Notifications, audit |
| change_request.created, .approved, .declined, .expired, .withdrawn | Approval lifecycle | request id, approver, comment | Notifications, audit, console |
| config.snapshot_created, config.rolled_back | Snapshot or restore | snapshot id, diff size | Audit, notifications |
| plan.changed, plan.expiring, plan.expired, plan.grace_started, entitlement.changed, trial.started, trial.ending | Plan lifecycle | tenant, plan, dates | Evaluation service, notifications, platform console |
| killswitch.set, killswitch.lifted | Platform kill switch | scope, key, reason, message | Evaluation service, notifications, audit |
| ai.consent_accepted, ai.consent_required, ai.settings_changed, ai.paused, ai.resumed | AI consent, settings and tenant pause | version, by, at | Evaluation service, audit |
| ai.quota_threshold, ai.quota_exhausted, ai.quota_reset | Quota | tenant, used, allowance, threshold | Notifications, AI gateway |
| feature.blocked_attempt | A request was denied (sampled) | key, reason, role, campus, channel | Evaluation log, tenant "Blocked attempts" |
| settings.changed | Tenant settings changed | group, before, after | Audit, notifications |

### State machines / workflows

**Feature state at one scope (derived).**

| From | Trigger | To |
|---|---|---|
| Locked (plan) | Plan or override grants entitlement | Off |
| Off | Admin enables (and checks pass) | On |
| On | Admin disables | Off |
| Off or On | Admin schedules a future change | Scheduled (current state holds until start) |
| Scheduled | Start time reached | On or Off per the change; Scheduled ends when no further dates |
| On or Off | Kill switch set | Paused by DhruvaOne |
| Paused by DhruvaOne | Kill switch lifted | previous state |
| On or Off | Plan expires (after grace) | Locked (plan) |
| Off (AI) | Admin picks Shadow | Shadow; then Pilot; then Live (or back to Off at any time) |

**Change request.**

| State | Next | Condition |
|---|---|---|
| Draft | Submitted | Admin presses Apply after preview and reason |
| Submitted | Applied | Not approval-class, checks pass |
| Submitted | Waiting for approval | Approval-class change |
| Waiting for approval | Approved | Approver differs from requester and is authorised |
| Waiting for approval | Declined, Expired (7 days), Withdrawn | Approver, clock, requester |
| Approved | Scheduled | Has a future start |
| Approved or Scheduled | Applied | At start, re-checks pass |
| Approved or Scheduled | Failed | Re-check fails (plan, consent, blocking condition, dependency); both parties told |
| Applied | Rolled back | A later rollback request restores prior state (the original stays Applied; the history shows the link) |

**Drain on disable.** Apply -> evaluation changes at propagation time -> in-flight handler by type (TFC-DIS-003) -> impact counts stored -> re-enable handler resumes pause only.

### Evaluation pseudo-code

```
isEnabled(key, ctx):
  if ctx.tenant is null: return Off("NO_CONTEXT")
  def = catalogue[key]; if def is null: return Off("UNKNOWN_FEATURE")        # fail closed
  if key in SAFEGUARD(ctx): return On("SAFEGUARD")
  # 1 kill switch
  k = killSwitch.match(key, ctx.tenant, ctx.app_version)
  if k: return Off("PLATFORM_KILL")
  # 2 plan
  e = entitlement(ctx.tenant, key, now)                # plan + override + trial + grace
  if e == excluded: return Off("PLAN_LOCKED")
  if e == expired:  return Off("PLAN_EXPIRED")
  if def.tenant_types and tenant.type not in def.tenant_types: return Off("PLAN_LOCKED")
  # 3 prerequisites
  if key startsWith "ai.":
     if not consent.valid(ctx.tenant, key): return Off("CONSENT_MISSING")
     if ai.paused(ctx.tenant): return Off("TENANT_SETTING")
     if quota.hardStopped(ctx.tenant) : return Off("QUOTA_EXCEEDED")
  if def.setup_required and not setupComplete(ctx.tenant, key): return Off("SETUP_INCOMPLETE")
  if ctx.app_version < def.min_app_version: return Off("APP_VERSION_TOO_LOW")
  for p in def.depends_on (all or any per depends_mode):
     if isEnabled(p, ctx).off: return Off("DEPENDENCY_OFF")
  # 4 tenant base
  state = tenantBase(ctx.tenant, key) ?? planDefault(e, key)        # On | Off
  reason = "TENANT_SETTING"
  # 5-7 layered rules, honouring locks, most specific last
  for level in [CAMPUS, ROLE, USER]:
     if lockedAbove(ctx.tenant, key, level): continue
     rules = activeRules(ctx.tenant, key, level, now)
              .filter(r -> r.matches(ctx))                     # AND of selectors
     if rules not empty:
        r = rules.anyDisable() ? firstDisable(rules) : newest(rules)
        state = r.effect; reason = levelReason(level)
  stage = (state == On and key startsWith "ai.") ? rolloutStage(ctx, key) : null
  if stage == Shadow and not ctx.isTester: state = Off; reason = "SHADOW_ONLY"
  return {enabled: state == On, reason, stage}
```

### Permission matrix

Legend: Y = yes; N = no; R = read only; D = within delegation; A = needs approval where the catalogue says so.

| Capability | Platform Owner | Group Owner | Group Admin | School Admin (standalone) | Trustee | Campus Principal | Others |
|---|---|---|---|---|---|---|---|
| View Features page | Y (config only) | Y | Y (own categories) | Y | R (requests only) | R (own campus) | N |
| Change feature at tenant scope | Y (override) | Y, A | Y (own categories), A | Y, A | N | N | N |
| Change at campus scope | Y | Y, A | Y (own campuses), A | N/A | N | D | N |
| Change at role or user-group scope | Y | Y, A | Y, A | Y, A | N | D (own campus) | N |
| Set locks and delegation | Y | Y | N | Y | N | N | N |
| Schedule a change | Y | Y | Y | Y | N | D | N |
| Approve a change request | Y (support, standalone only) | Y | Y if delegated | N (own request) | Y | N | N |
| Accept AI consent | N | Y | N | Y | Countersign if enabled | N | N |
| Set AI quota and data use | Y (allowance) | Y | N | Y | N | N | N |
| Pause all AI | Y | Y | Y | Y | N | D (own campus, if allowed) | N |
| Create presets and bulk change | Y | Y | Y | Y | N | N | N |
| Compare campuses | Y | Y | Y | N/A | N | N | N |
| View audit log | Y (config events) | Y | Y | Y | R (payroll and refund log, changes awaiting) | R (own campus) | N |
| Export audit log | Y | Y | N | Y | N | N | N |
| Snapshots and rollback | Y | Y, A | N | Y, A | N | N | N |
| Edit tenant settings | N | Y | N | Y | N | D | N |
| Edit approval limits | N | Y, A | N | Y, A | Approves | N | N |
| Plans, entitlements, trials | Y | N | N | N | N | N | N |
| Kill switches | Y (global lift needs 2) | N | N | N | N | N | N |
| Platform usage and tenant list | Y | N | N | N | N | N | N |
| View as tenant admin | Y (Platform Support, with consent) | N | N | N | N | N | N |

### Worked example

Saraswati Vidya Niketan, Karnal (standalone, Standard plan). On Fri 30 Oct 2026, School Admin Mrs. Meena Sharma decides that from Mon 2 Nov, 8:00 am, the four coordinators of Classes 9 to 12 (user group "Coordinators 9-12") no longer use WhatsApp voice notes or the AI timetable generator.

| Step | Feature | Scope rule | Level | Effect | Notes |
|---|---|---|---|---|---|
| 1 | ch.whatsapp.voice | Disable; user group "Coordinators 9-12"; channel any | User group | Off for those 4 | Risk Medium; no approval; Needs ch.whatsapp (On) and ai.voice_input (On) satisfied |
| 2 | ai.timetable_generator | Disable; user group "Coordinators 9-12" | User group | Off for those 4 | Risk-reducing; no approval; manual timetable editing unaffected |
| 3 | Both | Schedule: from 2 Nov 2026 08:00 IST, no end | - | Scheduled chip | Advance notice 3 days (voice) and 24 hours (AI) |
| 4 | Both | Reason: "Pilot with Class 6-8 coordinators first" | - | Audit reason | Min 10 characters met |
| 5 | Preview | "4 coordinators will lose Voice notes and Timetable generator; 1 pending timetable draft will be completed manually" | - | Shown before Apply | Drain: drafts kept 30 days read-only |

Resulting evaluation on Mon 2 Nov 2026 at 08:00:30:

| Person | Feature | Channel | Result | Reason |
|---|---|---|---|---|
| Coordinator A, Class 10 (in group) | ch.whatsapp.voice | WhatsApp | Off | USER_OVERRIDE (rule "Coordinators 9-12"); voice notes get "Please type your message" |
| Coordinator A | ai.voice_input | App (microphone) | On | No rule on `ai.voice_input`; only the WhatsApp voice channel was switched off |
| Coordinator A | ai.timetable_generator | Web | Off | USER_OVERRIDE; the "Generate timetable" button is removed, manual timetable editing unchanged |
| Coordinator B, Class 7 (not in group) | ch.whatsapp.voice | WhatsApp | On | TENANT_SETTING |
| Parent | ch.whatsapp.voice | WhatsApp | On | TENANT_SETTING (parent audience is outside the group) |
| Coordinator A, Sun 1 Nov | both | any | On | Schedule not started |
| Coordinator A, Mon 2 Nov, with Platform kill on `ai.timetable_generator` | ai.timetable_generator | Web | Off | PLATFORM_KILL (decided first, level 1) |

Audit event (extract): `type=feature.changed, actor=Meena Sharma (School Admin), key=ai.timetable_generator, scope_after={rule: disable, group: Coordinators 9-12, from: 2026-11-02T08:00+05:30}, reason="Pilot with Class 6-8 coordinators first", ip=203.x.x.x, device=Chrome 130 / Windows, approval=none (risk-reducing)`.

### Proposed flags

| Proposed key | Controls | Why | Suggested default and plan |
|---|---|---|---|
| ch.whatsapp.upi_pay | UPI fee payment inside the WhatsApp chat | Designed toggle "UPI fee payments in chat" | Opt on Standard, On Premium; Risk Critical; approval Y-on |
| ch.whatsapp.payslip | Payslip on WhatsApp behind the staff PIN | Designed toggle "Payslips on WhatsApp" | On Standard and Premium; Risk High |
| ch.whatsapp.admissions | Admissions enquiries by WhatsApp | Designed toggle "Admissions enquiries" | On Standard and Premium; Risk Medium |
| ch.sms | SMS for gate safety and offline alerts | Notification rules: SMS used for gate safety only | On, safety use cannot be suppressed (only the non-safety "SMS if the app is offline" use is switchable); Risk High |
| mod.audit_export | Audit log export | Website: audit exports for business customers | Off Essentials; On Standard and Premium; Risk Low |
| mod.open_api | Open APIs for the school | Roadmap Phase 2 | Off; Premium only; Risk High; approval Y-on |
| ai.exam_planning | AI date sheets, seating, invigilation | Exam cell design shows these as AI functions | Opt on Standard and Premium; consent Y; Risk Medium |
| ai.counselling_assist | Check-in suggestions and drafted private notes | Counsellor design | Opt on Premium; consent Y*; approval Y-on; Risk Critical |
| ai.hr_assist | Shortlisting and final settlement | HR design | Opt on Premium; consent Y*; approval Y-on; Risk High |

Notes: all nine proposals also appear as rows in the 4.3 catalogue tables, marked (NEW). Flags proposed by other sections must be appended to this catalogue under TFC-FLAG-004.
