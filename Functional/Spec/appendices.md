# Appendix A: Feature flag registry

Every requirement names the flag that switches it off. "Canonical" flags were defined up front; "registered here" flags were proposed while writing the sections and are registered now. Section 4 defines how flags work and carries the full catalogue with defaults, dependencies and risk. The last column shows how many requirements in each area use the flag.

| Flag | Status | Description (registered flags) | Requirements by area |
|---|---|---|---|
| `ai.admissions_scoring` | canonical |  | AI (2) |
| `ai.assistant_chat` | canonical |  | AI (12), DSK (5), MOB (6), XCT (1) |
| `ai.at_risk_detection` | canonical |  | AI (3), DSK (1), WAB (1) |
| `ai.bank_matching` | canonical |  | AI (1) |
| `ai.cover_suggestions` | canonical |  | AI (1) |
| `ai.data_import_checks` | registered here | Dhruva checks of imported data sheets | AI (1) |
| `ai.exam_planning` | registered here | Dhruva date sheets, seating and invigilation duties | AI (1), DSK (2) |
| `ai.fee_followup` | canonical |  | AI (1) |
| `ai.focus_card` | canonical |  | AI (6), DSK (7), MOB (2) |
| `ai.homework_marking` | canonical |  | AI (1) |
| `ai.hr_assist` | registered here | Candidate shortlisting and final-settlement calculation | AI (1) |
| `ai.lesson_plan_drafts` | canonical |  | AI (1) |
| `ai.marks_from_photo` | canonical |  | AI (4), MOB (2) |
| `ai.notice_drafts` | canonical |  | AI (3), XCT (1) |
| `ai.paper_generator` | canonical |  | AI (2) |
| `ai.payroll_checks` | canonical |  | AI (1), DSK (1) |
| `ai.remedial_grouping` | canonical |  | AI (2) |
| `ai.reply_drafts` | canonical |  | AI (3) |
| `ai.security_triage` | canonical |  | AI (1) |
| `ai.student_tutor` | canonical |  | AI (3), DSK (7) |
| `ai.timetable_generator` | canonical |  | AI (4), DSK (3) |
| `ai.translation` | canonical |  | AI (2), MOB (3), WAB (2), XCT (2) |
| `ai.transport_alerts` | canonical |  | AI (1) |
| `ai.voice_input` | canonical |  | AI (1), MOB (3) |
| `ai.whatsapp_bot` | canonical |  | AI (3), WAB (1) |
| `ch.desktop_web` | canonical |  | DSK (5), XCT (1) |
| `ch.email` | registered here | Email notifications and scheduled report emails | XCT (1) |
| `ch.mobile_android` | canonical |  | MOB (3), XCT (1) |
| `ch.mobile_ios` | canonical |  | MOB (3), XCT (1) |
| `ch.mobile_offline` | registered here | Offline queue for attendance and bus taps with sync | MOB (11) |
| `ch.mobile_push` | registered here | Push notifications on the phone app | MOB (12) |
| `ch.sms` | registered here | SMS: gate-safety messages (cannot be suppressed) and optional "SMS if the app is offline" | WAB (1), XCT (1) |
| `ch.whatsapp` | canonical |  | IDM (4), TFC (2), MOB (3), WAB (55), XCT (3) |
| `ch.whatsapp.admissions` | registered here | Admissions enquiries by WhatsApp | WAB (1) |
| `ch.whatsapp.handover` | registered here | Handover from the bot to a school person, with inbox and SLA | WAB (11) |
| `ch.whatsapp.parent_bot` | canonical |  | IDM (2), WAB (4) |
| `ch.whatsapp.payslip` | registered here | Payslip on WhatsApp behind the staff PIN | WAB (3) |
| `ch.whatsapp.photo_upload` | canonical |  | WAB (4) |
| `ch.whatsapp.staff_bot` | canonical |  | IDM (1), WAB (4) |
| `ch.whatsapp.teacher_bot` | canonical |  | WAB (2) |
| `ch.whatsapp.upi_pay` | registered here | Pay fees by UPI inside the WhatsApp chat | WAB (3) |
| `ch.whatsapp.voice` | canonical |  | WAB (3) |
| `idm.app_pin` | canonical |  | IDM (7), MOB (3) |
| `idm.biometric` | canonical |  | IDM (2), MOB (2) |
| `idm.multi_profile` | canonical |  | IDM (7), MOB (1) |
| `idm.sso` | canonical |  | IDM (1) |
| `idm.web_login` | canonical |  | IDM (1), DSK (1), WEB (5) |
| `mod.admissions_crm` | canonical |  | DSK (10) |
| `mod.approvals` | canonical |  | TFC (1), DSK (6), MOB (1), XCT (10) |
| `mod.attendance` | canonical |  | DSK (8), MOB (5), WAB (3) |
| `mod.audit_export` | registered here | Download the audit log (viewing is always on) | XCT (1) |
| `mod.bank_recon` | canonical |  | DSK (1), XCT (1) |
| `mod.bus_live` | canonical |  | DSK (3), MOB (3), WAB (1) |
| `mod.calendar_ptm` | canonical |  | DSK (5), MOB (4), WAB (1), XCT (2) |
| `mod.campus_onboarding` | canonical |  | TFC (1), DSK (7), XCT (9) |
| `mod.cbse_registration` | registered here | CBSE board registration checks | DSK (1) |
| `mod.counselling` | canonical |  | DSK (5), XCT (1) |
| `mod.cover` | canonical |  | DSK (1), MOB (1) |
| `mod.exams` | canonical |  | DSK (5), WAB (1), XCT (1) |
| `mod.fees` | canonical |  | DSK (5), MOB (8), WAB (3), XCT (2) |
| `mod.finance_accounts` | canonical |  | DSK (8) |
| `mod.global_search` | registered here | Global search across records the user may see | XCT (1) |
| `mod.group_scorecard` | canonical |  | DSK (4), MOB (1), XCT (2) |
| `mod.hiring_onboarding` | canonical |  | DSK (3) |
| `mod.homework` | canonical |  | DSK (4), MOB (2), WAB (3) |
| `mod.hr_leave` | canonical |  | DSK (20), MOB (2), WAB (3) |
| `mod.it_helpdesk` | canonical |  | DSK (4) |
| `mod.lesson_plans` | canonical |  | DSK (4) |
| `mod.marks_results` | canonical |  | DSK (5), MOB (4), XCT (1) |
| `mod.notices` | canonical |  | DSK (3), MOB (2), WAB (2), XCT (3) |
| `mod.open_api` | registered here | School-level API access and later integrations (P3) | XCT (1) |
| `mod.pace_tracking` | canonical |  | DSK (4) |
| `mod.parent_messaging` | canonical |  | DSK (2), MOB (2) |
| `mod.payroll` | canonical |  | DSK (6), WAB (1) |
| `mod.procurement_inventory` | registered here | Purchases, vendors, inventory and assets (P3) | DSK (4) |
| `mod.profile_switching` | canonical |  | IDM (3), DSK (1), MOB (9), XCT (1) |
| `mod.remedial` | registered here | Remedial groups and Saturday sessions | DSK (1) |
| `mod.report_cards` | canonical |  | DSK (3), MOB (1) |
| `mod.reports` | canonical |  | DSK (6), XCT (6) |
| `mod.security_gate` | canonical |  | DSK (3), MOB (2) |
| `mod.student_gamification` | registered here | Quests, XP, house points and badges for students | DSK (3) |
| `mod.student_learning` | canonical |  | IDM (3), DSK (3), MOB (12) |
| `mod.tally_sync` | canonical |  | DSK (1), XCT (1) |
| `mod.telemetry` | registered here | Product telemetry and analytics | XCT (1) |
| `mod.timetable` | canonical |  | DSK (6), MOB (2), WAB (1) |
| `mod.transport` | canonical |  | DSK (6), MOB (12), WAB (2) |

---

# Appendix B: Glossary

| Term | Meaning |
|---|---|
| Dhruva | The AI assistant (shown as a glowing orb). It prepares, drafts, explains and suggests; a person approves. |
| Tenant | One customer space: a group of campuses or a standalone school. Data never crosses tenants. |
| Group | Several campuses under one owner (sample: DPS Group). |
| Campus | One school inside a group. |
| Standalone school | A school outside any group, with its own admin and optional trustee. |
| Tenant Administrator | The person who controls the tenant's features and settings (Section 4). |
| Platform Owner | DhruvaOne staff who manage plans, entitlements and kill switches. |
| Profile | A role at a school attached to one mobile number. One number can hold several. |
| Feature flag | A named switch (for example `ai.marks_from_photo`) that a tenant administrator can set per tenant, campus, role or date. |
| Entitlement | What a plan allows a tenant to switch on. |
| Approval | A request that needs a named person's decision, with a limit, reason and record. |
| Cover | A period taught by a different teacher because the usual teacher is away. |
| PTM | Parent-teacher meeting. |
| HoD | Head of department. |
| PGT / TGT | Post-graduate and trained-graduate teacher grades. |
| CBSE | Central Board of Secondary Education. |
| UDISE+ | Government school data collection reports referred to in the designs. |
| OTP | One-time code sent to a mobile number. There are no passwords. |
| UPI | India's instant payment system used for fee payments. |
| Template message | A pre-approved WhatsApp message used outside the 24-hour session window. |
| DPDP Act | India's Digital Personal Data Protection Act 2023. |
| MVP, P2, P3 | Release phases (Section 1.4). |

---

# Appendix C: Design gaps

Screens and decisions that this specification defines but the prototypes do not yet show. Items marked [Spec] in the sections trace to this list.

| Area | Gap |
|---|---|
| Tenant control | No administration console designed: feature catalogue, scope and schedule, impact preview, presets, AI consent, quotas, audit and rollback, plan and Platform Owner consoles. The only designed switch surface is the WhatsApp "Campus admin · Settings" card. |
| Roles | No screen for the trustee; the Group Admin role does not appear in the designs. |
| Audit | No audit-log viewing screen. |
| Identity | PIN set-up and reset, biometric failure, session expiry and "Sign out everywhere" edge cases, student sign-in by age band, what "Ask my school to add me" sends, number-change recovery. |
| Mobile | Attendant "Start trip" screen, payment gateway screens, offline and sync states, deep links, force-update screen. |
| Desktop | Correcting a submitted attendance register; late-homework rule; school calendar on the student desktop; group-level HR and finance screens; adding calendar events on the owner desktop; entry point to the timed past paper for senior students. |
| Approvals | Escalation timers, delegation and service levels are not shown. |
| Data | Student transfer between campuses; where the rooms sheet sits among the eight data sheets. |
| WhatsApp | Agent inbox and handover SLA, out-of-hours reply, PIN lockout, multi-child and shared-number prompts, account-health and failure states, bus alert timing (5 or 10 minutes). |
| AI | Consent flow, quotas and cost caps, retention defaults, fallback when AI is off or fails, kill switch, confidence thresholds, child-safety rules for the tutor. |
| Conflicts in the designs | Quiet-hours default (6 am or 7 am), tab bars differ between boards, SMS toggles conflict, language count differs between boards. |
