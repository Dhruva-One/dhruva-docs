# 10. Release phasing and decisions

## 10.1 Phase mapping
| Phase in this document | Roadmap period | Content |
|---|---|---|
| MVP | Build Oct to Dec 2026; pilot at DPS Gurugram Sec 45 from 5 Jan 2027; all 14 campuses live by 31 Mar 2027 | Core platform, data import, role apps, WhatsApp Business, payment gateway, Dhruva drafting for human approval |
| P2 | Phase 1: Apr to Sep 2027 | Session 2027-28 set up, Tally sync, full payroll (PF, ESI, TDS), biometric import, room and lab scheduling, regional languages, Dhruva on WhatsApp, online admission forms, GPS pilot |
| P3 | Phase 2: Oct 2027 to Mar 2028 | GPS and RFID on all buses, online tests and board analytics, purchase, inventory, health, library, visitor and CCTV, early warnings, open APIs |

## 10.2 Decisions taken in this specification
These conflicts or gaps in the designs were resolved as follows so the sections agree. Each should be confirmed by the client.

| # | Topic | Decision taken | Where |
|---|---|---|---|
| 1 | Quiet hours | Default 9 pm to 7 am where the designs show 6 am in places; the duty reminder at 6 am falls inside quiet hours and is therefore delivered at 7 am unless marked Urgent | Sections 7, 9 |
| 2 | SMS | Gate-safety SMS can never be switched off; the optional "SMS if the app is offline" is switchable and off by default | Sections 4, 9 |
| 3 | Marks and learning plans | Teacher confirmation is required on every channel before marks are published, including WhatsApp photo entry; the designs show Undo only | Sections 5, 8 |
| 4 | Feature switches take effect | 95% of changes within 60 seconds, 99.9% within 5 minutes | Sections 3, 4 |
| 5 | WhatsApp phasing | Alerts and a basic inbox are MVP; the conversational bot is P2 because the roadmap lists Dhruva on WhatsApp in Phase 1, although the designs draw the bot as built | Section 8 |
| 6 | Hindi | Bilingual drafts are MVP (designs show them); Hindi chat with Dhruva is P2 | Sections 5, 7 |
| 7 | Class observations | Not specified: the "Book a class observation" button conflicts with the 11 Oct decision to drop observations | Section 6 |
| 8 | Overdue fees in quiet hours | Follow the notification rules: not delivered in quiet hours | Section 9 |
| 9 | Trustee | Trustee is an approver for a standalone admin's own pay, leave and refunds, with a minimal approval screen | Sections 4, 6 |
| 10 | Plans | Essentials, Standard and Premium are placeholder plan names | Section 4 |
| 11 | API conventions (v1.1) | All public paths are under `/v1`, service calls under `/internal/v1`; each API is defined once by its owner section (2.5) | All annexes |
| 12 | Sign-in and profiles (v1.1) | One set of identity APIs: `POST /v1/auth/otp/request` (not `/otp/send`); profiles at `GET /v1/me/profiles` and `POST /v1/me/profiles/{id}/switch` (not `/auth/profiles`, `/auth/switch`); PIN at `/v1/me/pin`, `/v1/me/pin/verify`, `/v1/me/pin/reset` (not `/auth/pin/*`); devices at `/v1/devices` with `POST /v1/auth/logout-all` (not `/auth/sessions`, `revoke-all`, `/auth/devices/register`); `POST /v1/auth/number-add-requests` (not `/add-me`) | Sections 3, 7 |
| 13 | Notification preferences (v1.1) | `GET/PUT /v1/notification-preferences` (not `/notification-settings`) | Sections 7, 9 |
| 14 | Reports (v1.1) | The reports engine owns running and scheduling: `POST /v1/reports/{key}/runs`, `POST /v1/report-schedules` (not `/reports/{key}/run`, `/reports/{key}/schedules`) | Sections 6, 9 |
| 15 | Role home (v1.1) | `GET /v1/dashboard/today` with `/act` and `/defer` for every role on desktop and phone (not `/dsk/today`) | Sections 6, 7 |
| 16 | Approvals (v1.1) | One approval queue `/v1/approvals` for every module; finance uses `module=finance` and the shared decision call (not `/fin/approvals`) | Sections 6, 9 |
| 17 | Audit (v1.1) | One audit API, `GET /v1/audit?category=` and `POST /v1/audit/exports` (not `/idm/audit`, `/tenants/{id}/audit-events`, `/ai/audit`) | Sections 3, 4, 5, 9 |
| 18 | AI settings and kill switch (v1.1) | AI consent, settings, pause, quota and top-up are tenant routes in Section 4; the platform AI kill is a platform kill switch with `scope: ai`. Section 5 keeps usage, explanations, models and evaluations (not `/ai/settings`, `/ai/settings/pause`, `/ai/admin/pause`) | Sections 4, 5 |
| 19 | Timetable (v1.1) | `/v1/timetables/...` in Section 6 is the only timetable API; Dhruva is the generator behind it (not `/ai/timetable/...`) | Sections 5, 6 |
| 20 | Payments and WhatsApp callbacks (v1.1) | Payment results come only from the gateway at `POST /v1/webhooks/gateway`, for app, web and WhatsApp orders. WhatsApp webhooks land on the gateway, which forwards statuses to `POST /internal/v1/wa/events` (not `/wa/payments/callback`, `/v1/webhooks/whatsapp`) | Sections 8, 9 |
| 21 | Events (v1.1) | Each event is defined once: `ai.quota_threshold` (not `ai.quota.threshold`); `ai.paused`, `ai.resumed` and `killswitch.set` (not `ai.kill.*`); `ai.settings_changed` (not `ai.settings.changed`); `timetable.approved` (not `ai.timetable.approved`); `feature.changed` (not `flag.changed`, `idm.flag.changed`); `consent.recorded` and `consent.withdrawn` (not `idm.consent.*`); `device.revoked` (not `auth.session.revoked`); notification events in Section 9 only | Sections 3, 4, 5, 7, 9 |
| 22 | Missing APIs (v1.1) | APIs added for requirements that had none: roles; tenant administrators and hierarchy; owner Insights and admissions; principal attendance and absence watch; fee defaulters; standalone admin views; outcomes; parent queries; HoD team; lesson plans; paper creation; notes; teacher inbox; counselling caseload, referrals, check-ins and careers; parent app; bus attendant trips; telemetry; support. Out on duty uses `/v1/leave` with a type | Sections 3, 4, 6, 7, 9 |
| 23 | Website (v1.1) | The website is specified in Section 11 from the functional overview. Website requests are DhruvaOne sales leads (`POST /v1/leads`), read in the Platform console, never in a school's admissions CRM | Section 11 |
| 24 | Owner Insights (v1.1) | The owner phone Insights tab is specified as MOB-STF-010 | Sections 6, 7 |

## 10.3 Open decisions for the client
Each section ends with its own open questions (3.8, 4.8, 5.8, 6.8 and 6.8b, 7.8, 8.8, 9.8). The ones that most affect scope and cost:

1. Tally sync, purchase and inventory: confirm MVP, P2 or P3 (the prototype shows them now; the roadmap says Phase 1 and Phase 2).
2. Security and IT gate and visitor log: confirm whether a simple gate log is in the MVP.
3. WhatsApp bot depth in the MVP (decision 5).
4. Whether Dhruva may publish marks or learning plans without teacher review for any tenant (default: never).
5. Data retention periods and the DPDP Act consent flow for children's data: needs legal review (Section 9).
6. Plan structure, pricing and which AI features sit in which plan (Section 4).
7. Whether the trustee gets a full role or approval-only access.
8. The administration console, audit-log screen and Platform Owner console need design (Appendix C).
9. Where website requests go after the Platform console: a CRM tool or the console only (Section 11, Q1).
