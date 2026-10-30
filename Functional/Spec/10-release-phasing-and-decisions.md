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
