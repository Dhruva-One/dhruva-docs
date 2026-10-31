# 11. Website

Area code: WEB. Source: the website boards in the functional overview (pages 179 to 194, desktop and mobile site). Related sections: Section 3 (sign-in by mobile number and OTP, which the website's Sign in page uses), Section 4 (the Platform Owner console, where website leads are read), Section 9 (privacy, consent and the status page).

## 11.1 Purpose, scope and out-of-scope

**Purpose.** The B2B website explains DhruvaOne to people who buy school software (owners, trustees, principals, admins, IT and procurement). It shows how approvals and data protection work and collects demo, pricing and pilot requests. It also gives parents, students and staff a way to get the app or sign in on a computer. The positioning line is "Learning, reimagined with AI."

**In scope**
- The site shell on desktop and phone: top strip, header, phone menu, footer, night and day modes, and the "Get the app" card.
- Seven visible pages: Home, Product, Solutions (three tabs), Trust, About us, Pricing, and Book a demo.
- The demo, pricing and pilot request form, and what happens to a request after it is sent.
- Sign in by mobile number and one-time code, using the identity services in Section 3.
- Content management, search-engine basics, performance, accessibility and privacy for a public site.

**Out of scope (covered elsewhere or intentionally left out)**
- The Resources and Customers pages, and the role-tab state. These exist in the prototype code but are hidden and are not specified.
- Parent and student content. They are sent to the app (Section 7).
- Prices. The site never shows a price; every plan is "Quoted for your school".
- Live chat, site search and cookie banners. None are designed, and the site sets no non-essential cookies (WEB-NFR-003).

## 11.2 Actors and roles

| Actor | What they do on the website |
|---|---|
| Prospective buyer (owner, trustee, principal, admin, IT, procurement) | Reads the pages, downloads the procurement pack, sends a demo, pricing or pilot request |
| Parent, student or staff member of a live school | Opens the "Get the app" card or signs in on a computer |
| DhruvaOne sales (Platform Owner role, Section 4) | Reads and follows up website requests in the Platform console |
| DhruvaOne marketing | Edits page copy in the content system and publishes the site |

## 11.3 Functional requirements

### 11.3.1 Site shell (WEB-SHL)

**WEB-SHL-001 · Must · MVP · flag: core · [Design]**
Every page shall show the same sticky header and footer.
- Acceptance: Given any page on desktop When it loads Then the header shows the logo (opens Home), the links "Product", "Solutions", "Trust", "About us" and "Pricing" (the current page bold on a grey pill), the night and day toggle, "Sign in" (outlined) and "Book a demo" (dark); the footer shows the line "The calm, intelligent operating system for schools. Made in India.", the Product column, the Legal column, the contacts sales@dhruvaone.in and "Grievance Officer (DPDP Act): grievance@dhruvaone.in", the link "Parent or student? Get the app" and "© 2026 DhruvaOne. Gurugram, India."
- Rules: footer Product items navigate to their pages. Legal items (Privacy notice, Terms, Data processing agreement, Security, Sub-processors, System status) are plain text in the design; see WEB-PAG-010 for publishing them.

**WEB-SHL-002 · Must · MVP · flag: core · [Design]**
The desktop site shall show a top strip with the hosting promise and the app link.
- Acceptance: Given a desktop page When it loads Then the strip shows "Hosted in India · DPDP Act ready" on the left and "Parent or student? Get the app" on the right; on the phone only "Parent or student? Get the app" is shown.

**WEB-SHL-003 · Must · MVP · flag: core · [Design]**
On the phone the header shall collapse into a menu.
- Acceptance: Given the phone site When "Menu" is tapped Then it lists Product, Solutions, Trust, About us, Pricing, Sign in, "Parent or student? Get the app" and a full-width "Book a demo"; choosing an item closes the menu and opens that page at the top.

**WEB-SHL-004 · Should · MVP · flag: core · [Design]**
A visitor can switch the whole site between day and night modes.
- Acceptance: Given any page When the moon button is pressed Then every page switches to the dark navy theme with the star background and the button label becomes "Switch to day mode"; the choice holds while navigating.
- Rules: the design does not remember the choice on reload. [Spec] The site follows the device's dark-mode setting on first visit.

**WEB-SHL-005 · Must · MVP · flag: core · [Design]**
Parents and students can open a "Get the app" card from the top strip, footer or phone menu.
- Acceptance: Given the link "Parent or student? Get the app" When it is pressed Then a card opens with "Looking for your school's app?", the line "Parents and students use the Dhruva One app for fees, attendance, the bus and notices. Download it, or sign in from a computer.", App Store and Google Play badges and a "Scan to download" QR code; "Sign in on desktop" opens Sign in; "Close" or a click outside closes the card.
- Rules: [Spec] the badges and QR code link to the live store listings (Section 7, MOB-STO) once the apps are published; until then they are hidden rather than shown as dead links.

**WEB-SHL-006 · Must · MVP · flag: core · [Design]**
Changing page shall always start the new page at the top and close the phone menu.
- Acceptance: Given the visitor is halfway down a page When any link to another page is chosen Then the new page opens scrolled to the top and the phone menu is closed.

### 11.3.2 Pages (WEB-PAG)

**WEB-PAG-001 · Must · MVP · flag: core · [Design]**
The Home page shall present the product in the designed order of sections.
- Acceptance: Given Home When it loads Then it shows, in order: the hero (eyebrow "AI-POWERED SCHOOL ERP FOR INDIA", headline "Learning, reimagined with AI.", "Book a demo", "See pricing" and the chips "DPDP Act ready", "Data stays in India", "Audit trail on every change"); the numbers strip; "Everything a school runs on, in one place." with nine module cards; "Three kinds of customer. One product that fits each."; "School data chaos, replaced by one student record."; "An assistant in every screen, and a person in charge." with eight Dhruva cards; "You decide who approves what."; the trust panel; the questions; and the closing "See it with your own numbers."
- Rules: each module card's "Explore this module" opens Product; each customer card's "See how it works" opens Solutions with that tab selected. The hero phone mock and the Dhruva orb card are images and are not clickable.

**WEB-PAG-002 · Must · MVP · flag: core · [Design]**
The Product page shall describe the nine modules on one student record.
- Acceptance: Given Product When it loads Then the header reads "Nine modules. One student record." and nine cards show four features each and a "Used by:" line, followed by the Dhruva block and the closing calls to action.
- Rules: module cards are not clickable. [Spec] Any capability that is not in the current release is labelled "Coming soon" with its phase from Section 10 (for example live bus location for parents is a P2 pilot, so it reads "Live bus location (coming soon)").

**WEB-PAG-003 · Must · MVP · flag: core · [Design]**
The Solutions page shall show three customer types as tabs.
- Acceptance: Given Solutions When a tab "School groups", "Standalone schools" or "Education businesses" is chosen Then the content switches at once without moving the page, showing the headline, four feature cards, "Who approves what" and "The first two weeks" for that customer type.
- Rules: arriving from a Home customer card selects the matching tab.

**WEB-PAG-004 · Must · MVP · flag: core · [Design]**
The Trust page shall state the data-protection, security and residency commitments and list sub-processors.
- Acceptance: Given Trust When it loads Then it shows "Built for the data of children." with the four claim blocks (children's data, DPDP Act, security, data residency and exit), the table "Who handles data on our behalf" (cloud hosting, SMS and OTP, WhatsApp Business provider, email delivery, payment gateway, each with its region) and the procurement pack.
- Rules: no certification (ISO, SOC) is claimed; "PCI DSS" is shown only against the payment gateway.

**WEB-PAG-005 · Should · MVP · flag: core · [Spec]**
The procurement pack shall download the real documents once legal has approved them.
- Acceptance: Given approved files for "Security overview", "Data processing agreement" and "Vendor security questionnaire" When "Download" is pressed Then the file downloads; given a file is not yet approved Then its row shows "Available on request" with a link to the demo form instead of the sample toast in the design.

**WEB-PAG-006 · Must · MVP · flag: core · [Design]**
The About us page shall show why the company exists, its values and its team.
- Acceptance: Given About us When it loads Then it shows "We build calm software for schools.", "Why we started", "What we believe" with the three values, "Dhruva One in numbers", "The people behind it" and "Come and meet the team." with "Book a demo" and "See solutions".
- Rules: [Spec] names and photos of the team are published only with each person's written consent; the sample names in the design are not shipped.

**WEB-PAG-007 · Must · MVP · flag: core · [Design]**
The Pricing page shall compare plans without showing prices and end in the request form.
- Acceptance: Given Pricing When it loads Then it shows four plan cards (Standalone, School, Group, Business) each "Quoted for your school", the "Compare plans" table with columns Standalone, School and Group, and the form with "I want to" set to "Get pricing".
- Rules: plan names and contents follow Section 4 (TFC-PLN); when plan names are final (Section 10, decision 10) the website uses the same names.

**WEB-PAG-008 · Must · MVP · flag: core · [Design]**
The questions on Home shall open one at a time.
- Acceptance: Given the seven questions When the page loads Then the first is open; when another is opened Then the open one closes; pressing the open one closes it; "Ask a question" opens the demo form.

**WEB-PAG-009 · Must · MVP · flag: core · [Spec]**
Every claim on the website shall be confirmed by legal and security before it is published.
- Acceptance: Given a page with a claim about compliance, security, certification, residency or timelines When it is submitted for publishing Then it cannot go live until a named legal or security reviewer has approved that version in the content system.
- Rules: the design's own note says "Sample claims for this design. Confirm each statement, certification and timeline with your legal and security teams before publishing."

**WEB-PAG-010 · Must · MVP · flag: core · [Spec]**
The Privacy notice, Terms, Data processing agreement, Security, Sub-processors and System status items shall be real pages before launch.
- Acceptance: Given the footer Legal column When the site launches Then each item opens its page; "System status" shows the live state from `GET /v1/status` (Section 9, XCT-SUP); the Privacy notice names the Grievance Officer and how to raise a data request.

### 11.3.3 Demo, pricing and pilot requests (WEB-DEM)

**WEB-DEM-001 · Must · MVP · flag: core · [Design]**
The request form shall adapt its title and button to the chosen reason.
- Acceptance: Given the form When "I want to" is "Book a demo", "Get pricing" or "Start a pilot" Then the title reads the same words and the button reads "Book my demo", "Get my pricing" or "Ask for a pilot".
- Rules: every "Book a demo" button opens the form with "Book a demo"; the Home and Product "Get pricing" opens it with "Get pricing"; "See pricing" and the Pricing link open the Pricing page with "Get pricing".

**WEB-DEM-002 · Must · MVP · flag: core · [Design]**
The form shall collect the designed fields with their defaults.
- Acceptance: Given the form When it opens Then it shows, in order: "I want to"; "We are a" (Standalone school by default); "Students or learners" (500 to 1,500 by default); "Your role" (Owner or trustee by default); "Your name"; "Work email"; "School or organisation"; "Phone (optional)" with "+91"; and the unticked consent box.

**WEB-DEM-003 · Must · MVP · flag: core · [Design]**
The form shall check the entries in a fixed order and show only the first problem.
- Acceptance: Given the submit button is pressed When an entry is wrong Then one message shows in red above the button, checked in this order: "Please add your name." (under 2 characters), "Please add your school or organisation." (under 2 characters), "Please add a valid work email." (not in the form x@y.z), "Please tick the consent box so we can contact you."; the message clears when all entries are valid.
- Rules: the phone number is not validated in the design. [Spec] When a phone number is entered it must be 10 digits after +91.

**WEB-DEM-004 · Must · MVP · flag: core · [Design]**
The request shall be sent only with the visitor's consent.
- Acceptance: Given the consent box reads "I agree that Dhruva One may contact me about this request. I have read the privacy notice. I can withdraw consent at any time." When it is not ticked Then nothing is sent; when the request is sent Then the consent text version and time are stored with it.
- Rules: [Spec] "privacy notice" links to the Privacy notice page (WEB-PAG-010).

**WEB-DEM-005 · Must · MVP · flag: core · [Spec]**
A valid request shall be recorded and confirmed to the visitor.
- Acceptance: Given a valid form When it is sent Then `POST /v1/leads` stores the request and the page replaces the form with "Thank you. We reply in one working day." and the three "What happens next" steps; given the service cannot be reached Then the form keeps the entries and shows "We could not send this. Please try again, or write to sales@dhruvaone.in."
- Rules: the same person sending the same reason twice within 24 hours updates the first request instead of creating a second one. Requests are rate limited and protected against bots without a visible puzzle.

**WEB-DEM-006 · Must · MVP · flag: core · [Spec]**
DhruvaOne sales shall be told about every request and the visitor shall get an email acknowledgement.
- Acceptance: Given a request is recorded When it is saved Then the sales inbox receives it within 5 minutes and the visitor receives an email from sales@dhruvaone.in repeating what they asked for; the request is visible to the Platform Owner in the console list (`GET /v1/platform/leads`).
- Rules: website requests belong to DhruvaOne, not to any school tenant, so they never appear in a school's admissions CRM (Section 6, DSK-ADS). Where they go next (a CRM tool or the console only) is open question Q1.

### 11.3.4 Sign in (WEB-SGN)

**WEB-SGN-001 · Must · MVP · flag: idm.web_login · [Design]**
A person can start sign-in on the website with the mobile number the school has on record.
- Acceptance: Given "Sign in to Dhruva One" When a number is typed Then only digits are accepted, trimmed to 10, after a fixed "+91"; "Send code" with fewer than 10 digits shows "Enter your 10-digit mobile number"; a valid number requests a code through `POST /v1/auth/otp/request` (Section 3, IDM-OTP).
- Rules: there is no password and no school search. The sample number chips in the design are not shipped.

**WEB-SGN-002 · Must · MVP · flag: idm.web_login · [Design]**
An unknown number shall be told how to get added.
- Acceptance: Given a number that is not in any school's records When "Send code" is pressed Then the page shows "This number is not registered with any school. Ask your school office to add it, then try again."
- Rules: the same message is used in the app (Section 3, IDM-NF), so the website does not reveal more than the app does.

**WEB-SGN-003 · Must · MVP · flag: idm.web_login · [Design]**
A person can enter the one-time code and go back to change the number.
- Acceptance: Given "We sent a 6-digit code to +91 98••• ••210." When fewer than 6 digits are entered and "Verify" is pressed Then "Enter the 6-digit code" shows; when 6 digits are entered Then the code is checked with `POST /v1/auth/otp/verify`; "Use a different number" returns to the number with it kept.
- Rules: the design accepts any code and shows a static "Resend in 0:28"; the build follows Section 3 (code expiry, attempts, live resend timer).

**WEB-SGN-004 · Must · MVP · flag: idm.web_login · [Design]**
After the code is verified the website shall show the school found for the number, or ask which school to open.
- Acceptance: Given one school When verified Then "We found your school" shows the school, place and board, "Signing in as <name>", "Your role" and "Continue as <first name>"; given two or more schools Then "Choose your school" lists them, the button stays grey "Choose a school" until one is picked, pressing it unpicked shows "Choose a school to continue", and once picked it reads "Continue with <school>".
- Rules: the list comes from `GET /v1/me/profiles` and the choice is made with `POST /v1/me/profiles/{id}/switch` (Section 3, IDM-DSC and IDM-PRF).

**WEB-SGN-005 · Must · MVP · flag: idm.web_login · [Spec]**
Continuing shall open the desktop web app signed in to the chosen profile.
- Acceptance: Given a profile is chosen When "Continue" is pressed Then the desktop web app opens on that profile's home without asking for the number again; the website itself keeps no session.
- Rules: the design shows a placeholder "You're in, Pooja" page; the build hands over to the desktop app. Switching school later is done in the app.

**WEB-SGN-006 · Must · MVP · flag: core · [Design]**
The Sign in page shall also offer the app.
- Acceptance: Given Sign in When it loads Then a "Get the Dhruva One app" panel shows "Free on iPhone and Android. Sign in with the same mobile number." with the store badges and QR code (WEB-SHL-005 rules apply).

### 11.3.5 Content, search engines and site quality (WEB-NFR)

**WEB-NFR-001 · Must · MVP · flag: core · [Spec]**
The website shall load fast on a mid-range phone.
- Acceptance: Given a mid-range Android phone on a 4G network When any page is opened from a search result Then the largest content appears within 2.5 seconds at the 75th percentile and the layout does not jump (cumulative layout shift under 0.1).

**WEB-NFR-002 · Must · MVP · flag: core · [Spec]**
The website shall meet WCAG 2.1 AA in both day and night modes.
- Acceptance: Given an accessibility audit When run on every page in both modes Then there are no AA failures; every control works by keyboard and the form errors are announced to screen readers.

**WEB-NFR-003 · Must · MVP · flag: core · [Spec]**
The website shall not track visitors with advertising or cross-site cookies.
- Acceptance: Given a first visit When the page loads Then no third-party advertising or tracking script runs and no non-essential cookie is set, so no cookie banner is needed; any analytics is first-party, cookieless and aggregate.

**WEB-NFR-004 · Should · MVP · flag: core · [Spec]**
Each page shall be ready for search engines and link previews.
- Acceptance: Given any page When fetched by a crawler Then it returns a unique title and description, a canonical address, Open Graph tags and a sitemap entry; Sign in is excluded from search results.

**WEB-NFR-005 · Should · MVP · flag: core · [Spec]**
Marketing can change page copy without a code release.
- Acceptance: Given an edit to page copy in the content system When it is approved (WEB-PAG-009) Then the site rebuilds and the change is live within 15 minutes; a previous version can be restored.

**WEB-NFR-006 · Must · MVP · flag: core · [Spec]**
The website shall be served from India with the same edge protection as the product.
- Acceptance: Given the live site When checked Then it is served over HTTPS behind the CDN and web application firewall, from storage in the India region, with no school data and no server-side session.

## 11.4 Business rules and policies
- The website never shows school data. Sign-in hands over to the desktop app; the sample dashboards on the pages are images.
- The site is the same on desktop and phone in content, states and validation; only layout and the top strip differ.
- Calls to action always lead to one of three outcomes: book a 30-minute demo, get pricing, or start a pilot in one campus at no cost.
- Website requests are DhruvaOne's own sales leads. They are not school records and are not visible to tenants.
- Leads are kept for 24 months after the last contact, then deleted, unless they become a customer contract (Section 9 retention rules apply).

## 11.5 Notifications raised by this section

| Event | Who is told | Channel | Notes |
|---|---|---|---|
| New website request | DhruvaOne sales inbox | Email | Within 5 minutes (WEB-DEM-006) |
| Request received | The visitor | Email | Acknowledgement repeating the request |

## 11.6 Feature switches in this section
The website is not tenant-scoped, so its pages use `core`. Website sign-in uses `idm.web_login`; when a tenant switches it off, the person is told to use the app after the code is verified (Section 3).

## 11.7 Non-functional requirements
See 11.3.5. Availability target: 99.9% monthly, measured at the CDN.

## 11.8 Open questions
- Q1. Where do website requests go after the Platform console: a CRM tool (to be chosen) or the console only?
- Q2. Which content system will marketing use? Until it is chosen the copy lives in the site repository.
- Q3. Final legal text for the Privacy notice, Terms and Data processing agreement, and approval of every claim on the Trust page.

## Annex 11-A (engineering)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| Lead | id, reason (demo, pricing, pilot), org_type, size_band, role, name, work_email, organisation, phone, consent_text_version, consent_at, source_page, utm (optional), status (new, contacted, qualified, closed), owner, created_at, updated_at | Platform-level record, not tenant data; deduplicated on work_email and reason within 24 hours |

### APIs

| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| POST /v1/leads | Record a demo, pricing or pilot request from the website form | Public, rate limited, bot check, CORS limited to the website origin | 422 validation (same order as WEB-DEM-003); 429 rate_limited |
| GET /v1/platform/leads | List and filter website requests | Platform Owner (sales) | 403 |
| PATCH /v1/platform/leads/{id} | Update status and owner of a request | Platform Owner (sales) | 404; 409 stale_version |

Website sign-in uses the Section 3 APIs `POST /v1/auth/otp/request`, `POST /v1/auth/otp/verify`, `GET /v1/me/profiles` and `POST /v1/me/profiles/{id}/switch`, and the footer status page uses `GET /v1/status` (Section 9).

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| lead.received | A website request is recorded or updated | lead_id, reason, org_type, size_band | Sales notification, Platform console |

### Permission matrix

| Capability | Visitor | Signed-in school user | Platform Owner (sales) | Marketing |
|---|---|---|---|---|
| Read pages, open "Get the app" | Yes | Yes | Yes | Yes |
| Send a request | Yes | Yes | n/a | n/a |
| Read and update requests | no | no | Yes | no |
| Edit and publish page copy | no | no | no | Yes (after legal approval for claims) |

### Proposed flags
None. Website pages are `core`; sign-in uses `idm.web_login`.
