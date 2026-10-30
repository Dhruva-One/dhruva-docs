# 3. Identity Management

Area code: IDM. Related sections: Section 4 (Tenant feature control and administration, TFC) defines the Tenant Administrator role and the flag mechanism; Section 5 (Desktop), Section 6 (Mobile) and Section 7 (WhatsApp) consume the identity services defined here; cross-cutting audit and notification rules live in XCT.

## 3.1 Purpose, scope and out-of-scope

### Purpose
DhruvaOne has one rule for identity: **the school's record is the account.** A person never creates an account, a username or a password. The school (through the student sheet, the staff sheet, HR, or the office) records a mobile number against a person; that number, proved by a one-time code (OTP), is the only credential. One number can open several profiles (for example parent at DPS Gurugram, parent at DPS Noida, parent at Saraswati Vidya Niketan, teacher and Head of Maths at DPS Gurugram). Profiles never mix: each is a separate window onto one school's data with its own role, menu and permissions. Staff profiles and sensitive actions sit behind an app PIN or phone biometric (Face ID, fingerprint).

### In scope
- Sign-in by mobile number and OTP on the iOS/Android app, the website sign-in page and the desktop web app.
- Handling of unregistered numbers, discovery of schools and roles from a verified number, multiple profiles and switching.
- Strict separation of data between profiles, campuses and tenants.
- App PIN, biometric unlock, step-up for sensitive actions, app lock.
- Sessions, tokens, devices, sign-out and revocation.
- Role catalogue, permission scope model, role assignment and lifecycle (invite, activate, change, deactivate, offboard).
- Person and profile records, parent-child linking and guardian verification, student accounts by age band, staff identity from HR.
- Identity of WhatsApp users (number matching, PIN, shared numbers, unknown numbers).
- Privacy, consent and audit of identity events; recovery when a mobile number changes; tenant-level identity controls.

### Out of scope (covered elsewhere)
- Content of role home screens (sections of each role) and approval chains (see Section XCT approvals).
- Feature-flag engine and flag scheduling (see TFC).
- Notification delivery tiers (see XCT notifications); this section only defines identity-related alerts.
- Single sign-on with Google or Microsoft (idm.sso): shown as a website tile, planned later (P3); only the extension points are defined here.
- Passwords, security questions and email-link sign-in: deliberately not offered.

## 3.2 Actors and roles

| Actor | Identity relevance |
|---|---|
| Any signed-in person | Signs in by OTP, switches profiles, sets PIN and biometric, manages own devices. |
| Parent / guardian | Profile per school (children of one school grouped); can create or switch off a child's student login. |
| Student (Classes 6-8, 9-12) | Own student login only from the age/class band the school enables; no login for younger children (Junior pod inside the parent app). |
| Staff (teaching, non-teaching, support) | Identity created from the staff sheet and HR record; staff profiles are PIN-protected. |
| Group Owner, Principal, Standalone School Admin, Trustee | Approvers; step-up required on approvals. |
| School office / front office | Records and corrects mobile numbers and child links for families (school office creates child links). |
| HR and payroll | Source of truth for staff identity; triggers activation, role change and offboarding. |
| Tenant Administrator (NEW, defined in Section 4) | Manages users, role assignments, identity policy and idm.* flags inside the tenant, without default access to academic, fee or HR content. |
| DhruvaOne support (platform) | Break-glass access to identity records of a tenant only on a written school request, always audited. |
| Dhruva (AI) | Never signs in, never holds a profile; acts only inside the session of the person who asked, with that person's permissions. |

The full role catalogue with scopes is in 3.3.8.

## 3.3 Functional requirements

### 3.3.1 Mobile number and OTP sign-in (app, website, desktop web)

**IDM-OTP-001 · Must · MVP · flag: core · [Design]**
A person can start sign-in by entering the mobile number the school has on record, with country code +91 and a 10-digit number.
- Acceptance: Given the sign-in screen "Enter your mobile number" When the person types digits Then the field accepts digits only and trims to 10; the line "Your number is only used to sign you in and to send school messages." is visible; the button reads "Send code".
- Acceptance: Given fewer than 10 digits When "Send code" is tapped Then the message "Enter your 10-digit mobile number" is shown and no code is sent.
- Rules: Same flow and wording on the iOS/Android app (Design: App shell > Login), the website "Sign in to Dhruva One" page and the desktop web app. Non-Indian numbers are out of scope for MVP (see Open questions).

**IDM-OTP-002 · Must · MVP · flag: core · [Design]**
The system shall send a 6-digit one-time code by SMS and show it only masked on screen.
- Acceptance: Given a registered number When "Send code" is tapped Then the screen "Enter the 6-digit code" shows "Sent to +91 98••• ••210 by SMS. It expires in 10 minutes." with six boxes and a "Verify" button that is disabled until six digits are entered.
- Acceptance: Given fewer than 6 digits on the web page When "Verify" is pressed Then the message "Enter the 6-digit code" is shown.
- Rules: The masked form keeps the first two and last three digits ("+91 98••• ••210"). The full number is never shown after the first screen except to the owner of the profile in Me.

**IDM-OTP-003 · Must · MVP · flag: core · [Design]**
The app shall auto-fill the code from the phone's SMS where the platform allows it.
- Acceptance: Given the iOS keyboard suggestion "From Messages 482913" or the Android SMS-sourced code When the person taps it Then the six boxes fill and "Verify" becomes active.
- Rules: SMS body follows the platform one-time-code format so autofill works (domain-bound on iOS, app hash on Android) [Spec]. The code is never shown in a push notification.

**IDM-OTP-004 · Must · MVP · flag: core · [Spec]**
The system shall enforce OTP validity, attempt and resend limits.
- Acceptance: Given an issued code When 10 minutes pass Then verification fails with "This code has expired. Send a new code." and the challenge is closed.
- Acceptance: Given a code When the wrong code is entered 5 times Then the challenge is closed with "Too many wrong codes. Send a new code." 
- Acceptance: Given a challenge When "Resend code" is used Then the previous code stops working at once.
- Rules: Code is single-use, stored only as a salted hash, generated by a cryptographic random source, compared in constant time. Resend cooldown 30 seconds (design shows a 0:24 / 0:28 countdown). At most 3 resends per challenge and 5 challenges per number per rolling hour.

**IDM-OTP-005 · Must · MVP · flag: core · [Spec]**
The system shall lock sign-in for a number or source that exceeds the abuse limits.
- Acceptance: Given 5 closed challenges for one number in one hour When a 6th code is requested Then the screen says "Too many attempts. Try again in 30 minutes." and no SMS is sent.
- Acceptance: Given more than 10 code requests from one IP address in 10 minutes across different numbers When another is requested Then the request is blocked and a CAPTCHA or device-attestation check is required [Spec].
- Rules: Responses for registered and unregistered numbers take the same time and the same rate-limit budget so numbers cannot be enumerated at scale (see IDM-NF-002). Lockouts are visible to the Tenant Administrator in the identity audit view and never expose the code.

**IDM-OTP-006 · Should · MVP · flag: core · [Design]**
A person can ask for the code on WhatsApp instead of SMS.
- Acceptance: Given the code screen When "Use WhatsApp instead" is tapped Then a new challenge is issued over the school's verified WhatsApp number (authentication template) and the screen keeps the same masked wording with "by WhatsApp".
- Rules: Available only when ch.whatsapp is on for the tenant and the number has WhatsApp opt-in; otherwise the link is hidden. Same limits as IDM-OTP-004; SMS and WhatsApp codes count against one budget.

**IDM-OTP-007 · Must · MVP · flag: core · [Design]**
A person can correct a wrong number without leaving the flow.
- Acceptance: Given the code screen When "Use a different number" is chosen Then the number screen reopens with the previous number kept and any open challenge closed.

**IDM-OTP-008 · Must · MVP · flag: idm.web_login · [Design]**
A person can sign in on the website or the desktop web app with the same mobile number and OTP.
- Acceptance: Given the page "Sign in to Dhruva One" (for parents, students, staff and school admins on a computer) When the number and code are verified Then the person sees "We found your school" (one profile), "Choose your school" (several), or the profile picker per IDM-DSC-001, then lands on the desktop view of the profile.
- Rules: The page also shows the panel "Get the Dhruva One app" (App Store, Google Play, "Scan to download"). When idm.web_login is off the page shows only the app panel. The desktop web app is additionally gated by ch.desktop_web.

**IDM-OTP-009 · Must · MVP · flag: core · [Spec]**
The system shall deliver OTP through a provider with failover and shall never reveal provider failure details.
- Acceptance: Given the primary SMS route fails or is not delivered within 20 seconds When the person waits Then the screen offers "Use WhatsApp instead" (where allowed) and the failed route is logged as an event.
- Rules: SMS must use DLT-registered sender and template (India). Provider is a listed sub-processor (SMS/OTP provider). OTP content is the only message category sent without the person's opt-in.

**IDM-OTP-010 · Must · MVP · flag: core · [Spec]**
The system shall not offer or accept passwords, and shall use OTP only for proof of the number.
- Acceptance: Given any sign-in surface When inspected Then there is no password, username, security-question or "forgot password" control.
- Rules: Biometric and PIN (3.3.5) unlock the app but never replace OTP at first sign-in on a device or after a session is revoked.

### 3.3.2 Number not registered, and discovery of school and role

**IDM-NF-001 · Must · MVP · flag: core · [Design]**
The system shall tell a person whose number is on no school record how to get in, with two ways forward.
- Acceptance: Given an unregistered number When "Send code" is tapped Then the app shows "We could not find this number" with "+91 90000 12345 is not on any school's record yet. Ask your school office to add it, or try the number you gave at admission." and buttons "Try another number" and "Ask my school to add me".
- Acceptance: Given the website or desktop web When the number is unregistered Then the inline message "This number is not registered with any school. Ask your school office to add it, then try again." is shown.

**IDM-NF-002 · Must · MVP · flag: core · [Spec]**
The system shall limit what an unregistered-number check reveals.
- Acceptance: Given any number When it is checked Then the response never names a school, person or role before OTP is verified.
- Acceptance: Given an unregistered number When the check is made Then the rate limits of IDM-OTP-005 apply and no OTP is sent.
- Rules: Design shows the "not found" screen before the code step; to stay consistent with enumeration protection the check is permitted but throttled (10 checks per IP per 10 minutes). See Open questions for the alternative (send OTP first, reveal later).

**IDM-NF-003 · Should · MVP · flag: core · [Spec]**
"Ask my school to add me" shall create an add-request that reaches the school office, because the designs do not draw what the button sends.
- Acceptance: Given the not-found screen When "Ask my school to add me" is tapped Then the person enters name, optional school name or code and relationship (parent, staff, student), consents to be contacted, and sees "Sent. The school office will contact you."
- Acceptance: Given a request When it is received Then the school's office queue shows it as "Number add request" with the number masked until the office opens it; it expires after 30 days.
- Rules: The request never creates a profile; only the office or HR can (IDM-LIF-001). Rate limit: 3 requests per number per day. Matching school is found by typed school name or code, never by number.

**IDM-DSC-001 · Must · MVP · flag: idm.multi_profile · [Design]**
After OTP the system shall find every school and role linked to the number and show the right next step.
- Acceptance: Given a verified number with one active profile When sign-in succeeds Then "We found your school" shows school, place and board (for example "DPS Gurugram Sec 45, Gurugram · DPS Group · CBSE"), "Signing in as Pooja Sharma", "Your role: Parent of Vivaan (5-B) and Aarav (2-A)" and "Continue as Pooja".
- Acceptance: Given 2 or more schools When sign-in succeeds Then "Choose your school: This number is registered with 2 schools. Pick the one to open now." shows cards; the button is grey "Choose a school" until one is picked, then "Continue with <school>".
- Acceptance: Given several profiles (app) When sign-in succeeds Then "Hi Neha, who are you today?" shows "One login, 4 profiles on this number", grouped by school group, campus and role, with new-item chips, and "Continue as teacher" (label follows the selection).
- Rules: With idm.multi_profile off, only the profile chosen at sign-in is opened and the person signs out to change (see IDM-PRF-005).

**IDM-DSC-002 · Must · MVP · flag: idm.multi_profile · [Design]**
A person can ask the app to reopen the last profile used.
- Acceptance: Given the picker When "Open the last profile I used next time" is ticked Then the next sign-in or app open goes straight to that profile (after biometric/PIN if required) and the picker is available from the profile chip.
- Rules: A locked staff profile never opens straight on a new device before PIN setup (IDM-LCK-001).

**IDM-DSC-003 · Must · MVP · flag: core · [Spec]**
The system shall show only active, current profiles in discovery.
- Acceptance: Given a number with a deactivated profile or a child who has left When discovery runs Then the profile is not listed, and if no profiles remain the person sees the unregistered screen (IDM-NF-001).
- Rules: Profiles in "Invited" state are listed as "Accept invite" only when opened from the invite link; otherwise the first successful sign-in activates them (IDM-LIF-002).

### 3.3.3 Multiple profiles and switching

**IDM-PRF-001 · Must · MVP · flag: idm.multi_profile · [Design]**
One mobile number shall be able to hold any number of profiles, each being one (person, school or campus, role) combination.
- Acceptance: Given Pooja Sharma's number When profiles are listed Then she has Parent at DPS Gurugram (Vivaan 5-B, Aarav 9-A together), Parent at DPS Noida (Myra 2-A), Parent at Saraswati Vidya Niketan (Ananya 3-A) and Teacher at DPS Gurugram (Science, 8-A, 8-B).
- Rules: Rule "same school, same screen": children of one school appear together in one parent profile with a child chip. Rule "another campus is another profile": the same group's other campus is a separate profile. Rule "another school is another tenant".

**IDM-PRF-002 · Must · MVP · flag: mod.profile_switching · [Design]**
A person can switch profile from the header chip without signing out.
- Acceptance: Given any home screen When the chip showing school and role is tapped Then the sheet "Switch profile" lists the phone number (masked), one row per profile (school, role tag, children or classes, "needs you" line such as "Fee due ₹9,600 · 2 new"), a tick on the current one and the dashed button "+ Add a profile with another number".
- Acceptance: Given another profile is tapped When it is not locked Then a short hand-over screen ("Switching to DPS Noida Sec 132. Parent of Rhea and Veer. Your teacher profile stays signed in and one tap away.") appears, the home reloads with that profile's colours and menu, and the toast "Switched to <school> · <role>" shows.
- Rules: Tapping the current profile only closes the sheet. The profile in use (school and role) is visible at the top of every screen.

**IDM-PRF-003 · Must · MVP · flag: mod.profile_switching · [Design]**
A person can see alerts from all profiles and jump to the right one.
- Acceptance: Given the bell on the header When tapped Then "All alerts" lists alerts from every profile labelled "<SCHOOL> · <ROLE>"; tapping one switches to that profile and, for a locked staff profile, asks for PIN or biometric first.
- Rules: The bell badge counts items needing the person in other profiles (aria: "<n> items need you in your other profiles"). Alert text from a locked staff profile shows only a generic line until unlocked (for example "You have items in Teacher · DPS Gurugram") [Spec].

**IDM-PRF-004 · Should · MVP · flag: idm.multi_profile · [Design]**
A person can add a profile that belongs to another number.
- Acceptance: Given the switch sheet When "+ Add a profile with another number" is tapped Then the person enters the other number and verifies it by OTP, after which that number's profiles join the sheet on this device.
- Rules: Profiles added this way stay tied to that number's own Person (no merge, see IDM-REC-003). Each added number has its own session, so signing out of one does not affect the others. Maximum 5 numbers per device [Spec].

**IDM-PRF-005 · Must · MVP · flag: idm.multi_profile · [Spec]**
With multi-profile switched off for a tenant, the system shall keep one profile per sign-in.
- Acceptance: Given idm.multi_profile is off for DPS Group When a person with two DPS profiles signs in Then the picker still lists them, one is opened, the profile chip does not open the switch sheet, and "Sign out to use another profile" is shown in Me.
- Rules: Profiles of other tenants are unaffected by one tenant's flag; if the person also has a profile in a tenant with the flag on, the switch sheet shows only those profiles.

**IDM-PRF-006 · Must · MVP · flag: mod.profile_switching · [Design]**
A person can switch profile from the desktop web app.
- Acceptance: Given the desktop view When the "SWITCH PROFILE" menu is used, or Ctrl + K is pressed and a school name typed Then the profile switches as on the phone with the same toast.
- Rules: Staff profiles ask for the PIN again after 15 minutes of inactivity in that browser (IDM-LCK-005).

**IDM-PRF-007 · Must · MVP · flag: idm.multi_profile · [Design]**
A person can switch school and campus later from settings as well.
- Acceptance: Given Me (or the gear on the notification centre) When "Switch profile" (shows current, "Teacher at DPS Gurugram · now") is chosen Then the same sheet opens.
- Rules: Design records show the switch at the top chip (ProfileSwitch board) and in Settings (design decision). Both entry points are built and open the same sheet.

### 3.3.4 Strict data separation between profiles and tenants

**IDM-SEP-001 · Must · MVP · flag: core · [Design]**
The system shall never mix data between profiles of the same person.
- Acceptance: Given Neha Arora with a teacher profile and a parent profile When she uses the teacher profile Then her own children never appear in lists, searches, Ask Dhruva answers, notices or reports; when she uses the parent profile no class data appears.
- Acceptance: Given the footer "Your own children never appear in your staff profile." When shown Then it appears on the profile picker for staff.
- Rules: Separation is enforced by the server on every request (profile id in the token), not by the app only.

**IDM-SEP-002 · Must · MVP · flag: core · [Design]**
The system shall isolate tenants completely.
- Acceptance: Given Saraswati Vidya Niketan (standalone) and DPS Group When any user of one calls any API Then no row, count, file or search hit from the other is returned.
- Acceptance: Given the Noida campus of DPS Group When a Gurugram parent profile is active Then the line "Fees, circulars and teachers here belong to the Noida campus only. Nothing from Gurugram is mixed in." holds for Noida profiles in the reverse direction.
- Rules: Each tenant has its own tenant id on every record, per-tenant encryption keys [Spec], and per-tenant caches. Only the Person (the mobile number) is global; it holds no school data.

**IDM-SEP-003 · Must · MVP · flag: core · [Spec]**
The system shall bind each token and each Dhruva request to exactly one profile.
- Acceptance: Given a session When an access token is issued Then it carries one profile id, tenant id and scope; switching profile issues a new token and the old one is not valid for the new profile.
- Acceptance: Given Ask Dhruva or any AI action When it runs Then it uses the active profile's scope and cites only records that profile may see.
- Rules: Group-level roles (Owner, group HR) may query across campuses of the same group tenant only. Cross-tenant queries do not exist.

**IDM-SEP-004 · Must · MVP · flag: core · [Spec]**
The system shall keep the lists shown before profile selection free of school data.
- Acceptance: Given a verified number before a profile is picked When the picker loads Then it shows school name, role, child first names and counts of "new" items only, and never fee amounts, marks or health or counselling details.
- Rules: The "needs you" line on the switch sheet may show fee amounts only for the current profile's own family and only after the profile's lock (if any) has been passed.

### 3.3.5 PIN, biometric and app lock

**IDM-LCK-001 · Must · MVP · flag: idm.app_pin · [Design]**
A staff person can protect staff profiles with a 4-digit app PIN.
- Acceptance: Given a staff profile opened for the first time on a device When no PIN exists Then the person must create one before the home screen opens; the Security row shows "App PIN: Required for staff pages and payments" with "Change".
- Acceptance: Given the lock screen "Unlock your teacher profile" When shown Then it carries the message "Staff profiles are protected, so a child with your phone cannot open your class data.", a four-dot keypad, "Use Face ID" (or fingerprint on Android) and "Cancel".
- Rules: PIN rejects trivial values (0000, 1234, repeated or sequential digits) and, where known, the person's birth year [Spec]. A parent-only profile can use the PIN voluntarily unless the tenant requires it (IDM-ADM-003).

**IDM-LCK-002 · Must · MVP · flag: idm.biometric · [Design]**
A person can turn on Face ID or fingerprint to unlock the app on a phone.
- Acceptance: Given first launch or Security When "Turn on Face ID" (iOS) or "Turn on fingerprint" (Android) is chosen Then the OS biometric prompt appears; after success the next app open asks for the biometric instead of the code and the screen says "Skip the code next time. Your login stays on this phone only, and you can turn it off in Settings."
- Acceptance: Given "Not now" When chosen Then sign-in continues without it and the toggle "Open with Face ID" stays off.
- Rules: Biometric data never leaves the phone; the app only receives pass/fail from the OS and uses it to release a device-held key (IDM-SES-005). If the OS enrolment changes (new face or finger added) the biometric is switched off and the PIN is asked [Spec].

**IDM-LCK-003 · Must · MVP · flag: idm.app_pin · [Design]**
The system shall ask for PIN or biometric before a staff profile opens on a switch.
- Acceptance: Given a locked staff profile When it is chosen from the sheet, the "All alerts" list or the picker Then "Unlock your teacher profile" appears; success shows the toast "Unlocked · Teacher at DPS Gurugram" (or "Unlocked with Face ID · Teacher at DPS Gurugram").
- Rules: Teacher, HoD, accounts, HR, principal, owner, admin and every other non-parent role count as staff profiles. Cancel returns to the previous profile.

**IDM-LCK-004 · Must · MVP · flag: idm.app_pin · [Design]**
The system shall require PIN or biometric for payments and approvals (step-up).
- Acceptance: Given a parent about to pay fees, or finance/principal/owner about to approve, release money or open a payslip When the action is confirmed Then PIN or biometric is asked if the last unlock was more than 5 minutes ago [Spec: window].
- Acceptance: Given Accounts ("Payments ask for PIN or biometrics") When a payment or bank file is released Then the unlock prompt appears and the action is logged with "step-up: pin" or "step-up: biometric".
- Rules: Default sensitive-action list in 3.4; tenants can add (IDM-ADM-003) but not remove payments, approvals or payslips. Dhruva can prepare these actions but the person unlocks them.

**IDM-LCK-005 · Must · MVP · flag: idm.app_pin · [Design]**
The browser shall ask for the PIN again after 15 minutes of inactivity on a staff profile.
- Acceptance: Given a staff profile on the desktop web app When no keyboard or pointer activity occurs for 15 minutes Then a PIN prompt covers the screen and data behind it is hidden; PIN success resumes in place.
- Rules: Biometric is not available in the browser unless the device supports WebAuthn platform authenticators, then it is optional [Spec]. On the phone, the app lock timeout is a setting: immediately, 1, 5 (default) or 15 minutes.

**IDM-LCK-006 · Must · MVP · flag: idm.app_pin · [Spec]**
The system shall limit PIN guesses and recover a forgotten PIN.
- Acceptance: Given the PIN keypad When 5 wrong PINs are entered Then the profile locks for 30 minutes (increasing to 2 hours after 10 total) and biometric is also disabled until PIN or OTP succeeds.
- Acceptance: Given "Forgot PIN" When the person verifies a fresh OTP Then a new PIN can be set and every other device's PIN-unlocked state is cleared.
- Rules: PIN is stored as a slow salted hash (Argon2id) server-side so the same PIN works on web and WhatsApp (see IDM-WAB-004); wrong-attempt counters are server-side per Person.

**IDM-LCK-007 · Should · MVP · flag: idm.app_pin · [Design]**
A person can hide balances and marks in the phone's app switcher.
- Acceptance: Given Security When "Hide balances on app switcher" is on Then fee and marks screens are blurred in recent apps and screenshots are blocked on payment and payslip screens where the OS allows.

**IDM-LCK-008 · Must · MVP · flag: idm.biometric · [Spec]**
The system shall treat biometric as a convenience over PIN and OTP, never as a standalone first factor.
- Acceptance: Given a new device When no OTP has been verified on it Then biometric cannot be used to sign in.
- Rules: With idm.biometric off the Security rows hide the biometric controls and PIN remains.

### 3.3.6 Sessions and device management

**IDM-SES-001 · Must · MVP · flag: core · [Spec]**
The system shall issue short-lived access tokens with refresh tokens and fixed lifetimes.
- Acceptance: Given a successful OTP When tokens are issued Then the access token lives 15 minutes; the refresh token lives 30 days sliding on mobile (absolute 90 days), 12 hours absolute on a browser (8 hours idle for staff profiles), and rotates on every use.
- Acceptance: Given a refresh token is used twice When the server sees the reuse Then the whole session family is revoked and the person must sign in again.
- Rules: Tokens are bound to device id; mobile refresh tokens live in the OS keychain/keystore; browser tokens use HttpOnly, Secure, SameSite cookies. Lifetimes are platform defaults; a tenant may only shorten them.

**IDM-SES-002 · Must · MVP · flag: core · [Design]**
A person can see the devices signed in and sign out of one or all of them.
- Acceptance: Given Me > Security When opened Then "Signed in on" lists "This phone · iPhone 15" (or "Pixel 8") marked "Active" and other devices with last-used time and approximate city.
- Acceptance: Given "Sign out everywhere" ("Use if you lose a phone") When the red "Sign out" is confirmed Then every session of this number on every device is revoked within 60 seconds and push tokens for those devices are removed.
- Rules: The red button "Sign out of this phone" ends only the local session of all profiles on that device. "Sign out everywhere" is available on web as well.

**IDM-SES-003 · Must · MVP · flag: core · [Spec]**
The system shall treat sign-out as sign-out of all profiles on that device.
- Acceptance: Given a device with three profiles unlocked When "Sign out of this phone" is chosen Then all three are signed out and the next open starts at "Enter your mobile number".
- Rules: Signing out of a single profile is not offered; to hide a profile the person uses the switch sheet. A profile removed by the school disappears on the next token refresh.

**IDM-SES-004 · Should · MVP · flag: core · [Spec]**
The system shall support trusted devices to reduce OTP prompts without weakening staff profiles.
- Acceptance: Given a phone where the person signed in with OTP When the refresh token is valid Then no new OTP is asked; on a browser, "Trust this computer for 30 days" is off by default for staff profiles and on-ticked only on a personal-computer confirmation.
- Rules: Shared devices (staffroom desktops, kiosks) are not trusted: sessions end at close of browser and the PIN timeout is 5 minutes (IDM-ADM-003 option).

**IDM-SES-005 · Must · MVP · flag: core · [Spec]**
The system shall register each device with a hardware-backed key.
- Acceptance: Given sign-in on a phone When the session is created Then a key pair is generated in the secure enclave/StrongBox, the public key is registered, and PIN/biometric step-up responses are signed with it.
- Rules: Rooted or jailbroken devices and failed app attestation lower trust: staff profiles and payments are refused with "This phone cannot run Dhruva One safely" [Spec].

**IDM-SES-006 · Must · MVP · flag: core · [Spec]**
The system shall revoke sessions when identity changes require it.
- Acceptance: Given a profile is deactivated, a number is changed, a role is removed or the PIN is reset When the change is saved Then the sessions and refresh tokens for the affected profile are revoked within 60 seconds and open apps show "Your access has changed. Sign in again."
- Rules: Role downgrades revoke only the changed profile; other profiles on the number keep working.

**IDM-SES-007 · Should · MVP · flag: core · [Spec]**
The system shall alert the person on unusual sign-ins.
- Acceptance: Given a sign-in from a new device, or after a "Sign out everywhere" When it succeeds Then a notice "New sign-in on <device>, <city>. Not you? Sign out everywhere." is sent to the person's other devices and, for staff, to the Tenant Administrator log.

### 3.3.7 Roles and permission scope model

**IDM-ROL-001 · Must · MVP · flag: core · [Spec]**
The system shall model every permission as capability plus scope, and evaluate it on the server for every request.
- Acceptance: Given a profile with role Class Teacher scoped to class 10-C When it requests marks of 10-B Then the server returns 403 "You do not have access to this class." and the attempt is audited.
- Rules: Capability names are stable strings (for example attendance.mark, fees.view, approvals.decide); roles are bundles of capabilities; scope levels are those in 3.4.1. Deny wins over allow.

**IDM-ROL-002 · Must · MVP · flag: core · [Design]**
The system shall provide the role catalogue in 3.3.8 and no role can reach outside its scope.
- Acceptance: Given each catalogued role When its permission matrix row is tested (Annex permission matrix) Then every allowed capability works inside scope and every other capability returns 403.
- Rules: A profile holds exactly one primary role in one campus or tenant. Someone who is both teacher and HoD holds two memberships under one profile card (see IDM-ROL-005).

**IDM-ROL-003 · Must · MVP · flag: core · [Design]**
Own-child scope shall limit parents to their linked children.
- Acceptance: Given a parent profile at DPS Gurugram When any API lists students, marks, attendance, fees or messages Then only children linked to that Person at that school are returned; other families, class lists and other children appear nowhere.
- Rules: Marks of a child are visible only to the student and the linked parents (Design: Student > Privacy). Both parents may be linked to one child; each sees the same child data.

**IDM-ROL-004 · Must · MVP · flag: core · [Design]**
Roles that carry special privacy shall be enforced as restricted capabilities.
- Acceptance: Given a counsellor's private session notes When any other role (including principal, owner and Tenant Administrator) requests them Then access is denied; only the authoring counsellor can read them (Design: Counsellor > private notes).
- Acceptance: Given a trustee When the profile opens Then only the payroll log and refund log are read-only visible.
- Rules: No teacher-observation capability exists (decision 11 Oct).

**IDM-ROL-005 · Must · MVP · flag: idm.multi_profile · [Design]**
One person can hold several roles at one school as separate memberships (teacher and Head of Maths).
- Acceptance: Given Neha Arora is Teacher (Maths) and Head of Maths at DPS Gurugram When the profile card is shown Then it reads "Teacher · Maths (10-C, 10-B, 9-C · Head of Maths)" and opens the combined staff profile; reviews and approvals appear only when the HoD membership is active.
- Rules: HoD actions are audited under the HoD role. A person cannot approve their own request in any of their roles (segregation of duties, see 3.4).

**IDM-ROL-006 · Must · MVP · flag: core · [Spec]**
The system shall support group, campus, department and class-section scopes for staff.
- Acceptance: Given the Academic Coordinator at Gurugram When cover is assigned Then only teachers and periods of Gurugram appear; at the group level only the Owner and group HR see more than one campus.
- Rules: Scope is stored on the Membership (tenant id, optional campus id, optional department id, optional class-section ids). Class-section scope for class teachers and subject teachers comes from the timetable/section assignment and updates without re-invite.

### 3.3.8 Role catalogue

Every role in the inventories is listed below. "Staff profile" means PIN/biometric-protected (IDM-LCK-003).

| Role | Typical scope | Profile type | Source of identity | Notes (source) |
|---|---|---|---|---|
| Group Owner | Tenant (group), all campuses, read-heavy | Staff | Owner invited by DhruvaOne onboarding | Does not edit campus classroom data; approves above-limit items (Design: Owner) |
| Trustee / Chairperson (standalone) | Tenant, payroll log and refund log read-only | Staff | School admin invite | Approves admin's own leave, salary, fee waivers (Design: Admin) |
| Principal | Campus | Staff | Principal named in Add a campus step 2 | Bell opens Approvals |
| Vice principal | Campus | Staff | Staff sheet and campus setup step 5 | Leadership tag set in campus setup |
| Standalone School Admin | Tenant (single school) | Staff | Onboarding | Runs the whole school day (Design: Admin) |
| Tenant Administrator (NEW, Section 4) | Tenant (or campus when delegated) | Staff | Nominated by owner / school admin | Identity, flags, roles; no default content access |
| Academic Coordinator | Campus | Staff | Staff sheet | Cover, syllabus, timetable |
| Exam Cell | Campus | Staff | Staff sheet | Papers, date sheets, report cards |
| Head of Department (HoD) | Department | Staff | Staff sheet | Approves team leave up to 2 days outside exam weeks |
| Teacher (subject) and Class Teacher | Class/section | Staff | Staff sheet | Class teacher also approves student leave |
| Counsellor | Campus, referral caseload | Staff | Staff sheet | Private notes |
| HR and payroll | Campus or group | Staff | HR system itself | Staff identity source |
| Accounts / Finance | Campus or group | Staff | Staff sheet | PIN/biometric on payments |
| Front office and admissions (CRM) | Campus | Staff | Staff sheet | Creates child links and number corrections |
| Security & IT | Campus | Staff | Staff sheet | Gate and jobs |
| Transport in-charge | Campus | Staff | Staff sheet | Fleet, routes |
| Bus attendant (English/Hindi) | Own bus and route | Staff (light) | Transport roster | Taps picked up, reached, left; WhatsApp-capable |
| Support staff (driver, guard, housekeeping) | Self only | WhatsApp or app | HR record | Payslip, leave, duty (Design: WhatsApp staff) |
| Parent / guardian | Own children at one school | Parent | Student record guardian numbers | One profile per school |
| Student, Classes 6-8 | Self | Student | Parent-created login | No payments, no messages to parents |
| Student, Classes 9-12 | Self | Student | Parent-created login or school-created at age band | No payment or admin functions |
| DhruvaOne support | Platform, break-glass | Platform | Internal | Audited, school-approved (see IDM-ADM-007) |

**IDM-ROL-007 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator role shall be able to manage identity but not read business content.
- Acceptance: Given a Tenant Administrator When the profile opens Then identity pages (people, roles, devices, sign-in audit, idm.* flags) are available; attendance, marks, fee, payroll, counselling and message content are not.
- Rules: Role defined in Section 4 (see TFC). The Tenant Administrator may assign or remove roles but not assign themselves a business role (needs the owner or school admin, SoD).

### 3.3.9 Role assignment and lifecycle

**IDM-LIF-001 · Must · MVP · flag: core · [Design]**
The system shall create staff and parent profiles from the school's imported records and invites.
- Acceptance: Given the staff sheet (Staff and leave balances) is imported When processing completes Then a "Staff accounts" count appears in onboarding ("created from the staff sheet"); no OTP is sent yet.
- Acceptance: Given the student sheet is imported When it passes validation Then parent profiles are prepared and the "Parents" invite line moves from "Invites go out once the student sheet is in" to "App and WhatsApp invites go out in Week 3".
- Rules: Principal and onboarding lead are created by the owner at "Add a campus" (name and 10-digit mobile required; invites on WhatsApp and email "when the campus is added"). Missing mobile numbers and duplicates are flagged by import validation, not silently accepted.

**IDM-LIF-002 · Must · MVP · flag: core · [Spec]**
The system shall use invite, activate, suspend and deactivate states for a profile.
- Acceptance: Given a prepared profile When the invite is sent (WhatsApp, SMS, email) Then the state is "Invited"; the first successful OTP sign-in by the number sets "Active".
- Acceptance: Given an Invited profile not accepted within 30 days When the date passes Then the invite expires, is shown as "Invite expired" to the office and can be re-sent.
- Rules: State machine in the Annex. Invite links carry a one-time token that only pre-selects the profile; they do not sign anyone in.

**IDM-LIF-003 · Must · MVP · flag: core · [Spec]**
A role can be changed, added or removed by the person with authority, with an audit record and immediate effect.
- Acceptance: Given HR records a promotion to HoD When saved Then the HoD membership is added within one minute, the person's switch sheet shows it and an audit event "role.assigned" stores who, when, old and new.
- Rules: Who may assign: HR (staff roles), Tenant Administrator (any role in tenant except Owner, Principal), Owner (Principal, Tenant Administrator), Trustee (School Admin). Self-assignment is blocked.

**IDM-LIF-004 · Must · MVP · flag: core · [Spec]**
The system shall offboard staff identity automatically when HR records an exit.
- Acceptance: Given HR starts an exit ("Start exit") When the last working day passes Then staff memberships become "Deactivated", sessions are revoked and the person's staff profile disappears from their picker.
- Acceptance: Given an exit with open clearance (for example "laptop not returned") When the last day passes Then access is still removed on the last day; clearance and final settlement continue in HR without a login.
- Rules: Access can be cut earlier by HR or Principal ("cut access now"). Authored records (attendance, marks, approvals) stay and show the former name. The person's other profiles (for example as a parent) are untouched.

**IDM-LIF-005 · Should · MVP · flag: core · [Spec]**
The system shall offer a temporary suspend for leave, investigation or lost phone without deleting the profile.
- Acceptance: Given a suspend by HR, Principal or Tenant Administrator When saved Then all sessions are revoked, sign-in shows "Your access is paused. Please contact the school office." and re-enabling restores the profile.

**IDM-LIF-006 · Must · MVP · flag: core · [Spec]**
The system shall deactivate and retain parent and student profiles when a child leaves.
- Acceptance: Given a child's status becomes Left (transfer certificate issued) When saved Then the child link is archived; if it was the parent's only child at that school the parent profile moves to "Deactivated" after 30 days (fee dues and receipts remain visible read-only during that time).
- Rules: Data retention follows Section XCT; deletion 90 days after exit with written confirmation (Design: Trust page).

**IDM-LIF-007 · Should · MVP · flag: core · [Spec]**
Staff movement between campuses of one group shall move the membership, not create a new Person.
- Acceptance: Given a teacher transfers from Gurugram to Noida When HR records it Then the Gurugram membership ends on the transfer date, a Noida membership starts and the Noida profile appears in the picker; Gurugram data stays at Gurugram.

### 3.3.10 User and profile records, parent-child linking, student and staff accounts

**IDM-REC-001 · Must · MVP · flag: core · [Spec]**
The system shall keep a Person record (one per verified mobile number) and Profile records, and show the person only their own.
- Acceptance: Given Me When opened Then the card shows name, masked number ("+91 98••• ••898 · 4 profiles"), language, and rows Switch profile, Language, Notifications, Security, Help and support, About Dhruva.
- Rules: The Person holds number, preferred language, PIN, devices; the Profile holds school, role, linked children or scope. The Person never stores school data. Display name shown inside a school is the school's record name.

**IDM-REC-002 · Must · MVP · flag: core · [Design]**
The school office shall create and maintain child-to-guardian links; parents cannot link themselves.
- Acceptance: Given a student record with guardian numbers When the office saves Then the matching parent profile shows the child; children of one school appear together (child chip, "Your children at DPS Gurugram Sec 45").
- Rules: Link fields: relation (father, mother, guardian), primary-contact flag, fee-payer flag, pickup-authorised flag, consent-holder flag. Several guardians may link one child; one guardian may link several children.

**IDM-REC-003 · Must · MVP · flag: core · [Spec]**
The system shall verify a guardian before a new link takes effect.
- Acceptance: Given the office adds or changes a guardian number When saved Then the link is "Pending" until the guardian signs in by OTP on that number, or the office confirms by recorded identity check (admission form or ID sighted) with a note; the existing primary guardian receives "A new guardian number was added for <child>" within 1 hour.
- Rules: A link to a child after admission requires two office staff or Principal approval when it grants fee-payer or pickup rights [Spec]. Persons are never merged automatically even if names match.

**IDM-REC-004 · Must · MVP · flag: core · [Spec]**
The system shall resolve a number shared by several guardians or several children correctly.
- Acceptance: Given one mobile number recorded for two children in one school When that parent signs in Then one profile lists both children together.
- Acceptance: Given one mobile number recorded as guardian of children in different schools When the person signs in Then one profile per school is listed (IDM-PRF-001).
- Rules: Two real guardians sharing one number are treated as one Person; the office is warned at entry ("This number is already linked to <relation> of <child>").

**IDM-STU-001 · Must · MVP · flag: mod.student_learning · [Design]**
A child shall have a student login only from the age band the school enables, created and controlled by a parent.
- Acceptance: Given the parent app When the parent turns on "Dhruva student app" for a child in Class 6 or above Then the toast "Student login created for <child> · details sent to you" appears; turning it off shows "<child>'s student login is switched off · the Junior pod is in your app".
- Acceptance: Given a child in Classes 1-5 (for example Arjun, Class 2) When the parent opens the app Then the child has no login and the "Junior pod" tile is shown; a younger child who has been given a login shows "Student app".
- Rules: Default bands [Spec]: Classes Nursery-5 no login (Junior pod), 6-8 and 9-12 login on parent request. Tenant may change bands (IDM-ADM-005). Student login uses the same OTP flow on a number the parent registers (the child's own number or the parent's number with a student profile). Student profiles never hold payment or messaging capabilities.

**IDM-STU-002 · Must · MVP · flag: mod.student_learning · [Spec]**
The system shall give students limited identity rights suitable for minors.
- Acceptance: Given a student profile When the Security screen opens Then biometric and PIN are optional, "Sign out everywhere" is available and the parent can also revoke the student's sessions from the parent app.
- Rules: Student leave runs two-step: the parent confirms, then the class teacher approves ("Sent to <parent> to confirm"). Only the student and linked parents see marks and attendance. No marketing messages to students; Class 6 and above get homework and results only (Design: notifications rules). Consent for under 18 is per child and held by the guardian (see IDM-ADM-007).

**IDM-STF-001 · Must · MVP · flag: core · [Design]**
Staff identity shall come from the HR record and stay in step with it.
- Acceptance: Given an employee in HR with a mobile number and employment type When the record is Active, Probation or Joins-on date reached Then the staff profile is available; Contract, Visiting and part-time staff get the same identity with scope limited to their assignment.
- Acceptance: Given HR edits a staff mobile number When saved Then the account recovery procedure in 3.3.13 runs; no change is accepted from the staff member's own app.
- Rules: The designs show "Logins and ID cards are ready" in onboarding checklists; login readiness is part of the joiner checklist (HR > Hiring and onboarding).

**IDM-STF-002 · Should · MVP · flag: core · [Spec]**
The system shall give support staff with no smartphone or no app a number-only identity.
- Acceptance: Given a driver or housekeeper in the staff sheet When the person uses WhatsApp Then identity works as in IDM-WAB-001; the app is optional.
- Rules: Staff PIN is set with HR (IDM-WAB-004).

### 3.3.11 Identity of WhatsApp users

**IDM-WAB-001 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall identify a WhatsApp sender by matching the sending number to school records, with no sign-in.
- Acceptance: Given a message from a number that matches a guardian number of one school When "Hi" is sent Then Dhruva greets by name and shows the parent menu; no OTP or password is requested.
- Acceptance: Given a staff or teacher number When "Hi" is sent Then numbers are checked against HR records and the staff or teacher bot (ch.whatsapp.staff_bot, ch.whatsapp.teacher_bot) responds.
- Rules: Only the school's verified green-tick number is used; number normalisation to E.164. The WhatsApp channel for Dhruva is Phase 1 (April to September 2027); outbound alerts and notices on WhatsApp are MVP (see Section 7).

**IDM-WAB-002 · Must · P2 · flag: ch.whatsapp.parent_bot · [Design]**
A number linked to several schools shall be asked which school is meant, and the choice remembered for 30 minutes.
- Acceptance: Given a number linked to 3 schools When "Hi" is sent Then "Hi Pooja, this number is linked to 3 schools. Which one do you mean?" appears with buttons such as "DPS Gurugram · Vivaan, Aarav", "DPS Noida · Myra", "Saraswati Vidya Niketan · Ananya".
- Acceptance: Given a choice When made Then Dhruva says "I will remember this school for the next 30 minutes. Type 'switch' to change." and keeps it for 30 minutes or until "switch".
- Rules: The school is the tenant for that chat session. Teacher and parent profiles of one number are chosen the same way and never answered together.

**IDM-WAB-003 · Must · P2 · flag: ch.whatsapp.parent_bot · [Spec]**
A number shared by one parent with several children shall show one answer per child on request.
- Acceptance: Given two children at one school When the parent asks "attendance" Then Dhruva replies with a list "Which child?" showing child first names and class, or both if the parent chooses "Both".
- Rules: Marks are sent only for the child asked about. Messages are never sent to a shared number about a child the number is not linked to.

**IDM-WAB-004 · Must · P2 · flag: ch.whatsapp.staff_bot · [Design]**
Sensitive data on WhatsApp shall need the person's 4-digit PIN.
- Acceptance: Given "My payslip" When no PIN has been entered in this chat Then "Your payslip is protected. Please enter your 4-digit PIN to open it." appears with "Enter PIN"; the sheet "Enter your PIN" says "Dhruva never asks for this PIN anywhere else." and shows "Please enter 4 digits." on error.
- Rules: PIN is entered in a WhatsApp Flow (masked), never in chat text. The PIN unlock lasts 10 minutes of chat [Spec]. Five wrong PINs lock WhatsApp payslips for 30 minutes (IDM-LCK-006). Dhruva never asks for UPI PINs, OTPs or passwords (parent footer).

**IDM-WAB-005 · Must · P2 · flag: ch.whatsapp · [Design]**
The system shall give unknown numbers a polite refusal and a way to reach the school.
- Acceptance: Given a number that matches no school record When any message arrives Then the reply asks the sender to contact the school office; no data is given and no profile or request is created.
- Rules: Reply wording is a [Spec]; the designs state only that registered numbers only work. At most 1 refusal reply per number per day to avoid spam loops. Opt-in at admission; reply STOP turns school alerts off and is honoured immediately.

**IDM-WAB-006 · Must · P2 · flag: ch.whatsapp · [Spec]**
The system shall add protection against number recycling and SIM swap on WhatsApp.
- Acceptance: Given a number was reassigned by the telecom When the school office is told or a bounce occurs Then the office can mark the number "Verify before use"; WhatsApp then requires a one-time code sent by SMS before any data is shown.
- Rules: Out-of-hours handover to humans (office, HR) is separate; identity does not extend to the human agent beyond the matched profile.

**IDM-WAB-007 · Should · P2 · flag: ch.whatsapp · [Spec]**
All WhatsApp actions shall be audited under the matched profile with channel = whatsapp.
- Acceptance: Given a photo of a register published via WhatsApp When it is saved Then the audit event shows profile, channel, message id and "Undo" availability (Design: teacher photo flow).

### 3.3.12 Privacy, consent and audit of sign-ins

**IDM-PRV-001 · Must · MVP · flag: core · [Design]**
The system shall state plainly how the number is used.
- Acceptance: Given the number screen When shown Then "Your number is only used to sign you in and to send school messages." is visible; Me > "About Dhruva" shows "How your data is used".
- Rules: No ads, no tracking, no sale of student data (Design: Trust page).

**IDM-PRV-002 · Must · MVP · flag: core · [Design]**
The system shall record parental consent per child under 18 and per purpose.
- Acceptance: Given a guardian profile When consent is requested (child student login, WhatsApp opt-in, photo use) Then each consent shows purpose, date, who gave it and is revocable in Me > Privacy.
- Rules: Consent is per child and per purpose. WhatsApp opt-in is collected at admission; reply STOP withdraws it. Withdrawal of student-login consent switches the student login off.

**IDM-PRV-003 · Must · MVP · flag: core · [Spec]**
The system shall log every identity event.
- Acceptance: Given any of sign-in, OTP request, failed OTP, lockout, profile switch, PIN set/failed, biometric toggle, session revoke, role change, link change, number change, add-request When it occurs Then an AuditEvent is written with actor, profile, tenant, channel, device, coarse IP, result and time.
- Rules: Audit is append-only and tamper-evident; OTP codes and PINs are never logged. Retention 2 years minimum for identity events [Spec]. Exportable by the school's Tenant Administrator and the Owner (audit exports for business customers).

**IDM-PRV-004 · Should · MVP · flag: core · [Spec]**
A person can see their own recent sign-in activity.
- Acceptance: Given Security When "Recent activity" is opened Then the last 30 days of sign-ins, switches and failures for their number appear with device and approximate city.

**IDM-PRV-005 · Must · P2 · flag: core · [Design]**
The system shall handle access, correction and deletion requests under the DPDP Act, routed through the school.
- Acceptance: Given a data request from a guardian When logged Then it appears for the school (data fiduciary) to approve; DhruvaOne acts as processor; the Grievance Officer address "grievance@dhruvaone.in" is shown in About Dhruva.
- Rules: Identity data held by DhruvaOne (number, devices, audit) is deleted 90 days after the last profile ends unless law requires longer.

### 3.3.13 Account recovery when the mobile number changes

**IDM-REC-005 · Must · MVP · flag: core · [Spec]**
The system shall recover access by the school updating the number, because the school's record is the account.
- Acceptance: Given a guardian or staff member has a new number When the office (parents) or HR (staff) updates the record and the new number passes OTP Then the person's profiles move to the new Person, all sessions on the old number are revoked and PIN is reset.
- Rules: The person cannot change their own number inside the app. The change request shows "Number change" with old and new masked numbers; the office confirms identity by a documented check (ID sighted or call to the old number). A notification goes to the old number by SMS and the previous device.

**IDM-REC-006 · Must · MVP · flag: core · [Spec]**
The system shall handle a lost phone or lost number in the same way.
- Acceptance: Given a lost phone with the same number When the person uses another phone and "Sign out everywhere" Then no school action is needed; if the number is also lost the office or HR starts IDM-REC-005 and may suspend the profile meanwhile (IDM-LIF-005).
- Rules: Biometric and PIN do not allow recovery; only OTP on the new number or the school's record change.

**IDM-REC-007 · Should · MVP · flag: core · [Spec]**
The system shall detect and surface duplicate or conflicting numbers.
- Acceptance: Given the same number is recorded for two staff or for a staff member and an unrelated family When the record is saved Then the office or HR sees "This number is already used by <name/role>" and must confirm (shared family phone) or correct it.

### 3.3.14 Admin controls for identity

**IDM-ADM-001 · Must · MVP · flag: core · [Spec]**
A Tenant Administrator can see and manage people, profiles and roles in their tenant.
- Acceptance: Given the Identity admin page When opened Then it lists Persons and Profiles with state, role, last sign-in, device count and filters (campus, role, state); actions are Invite, Re-send invite, Change role, Suspend, Reactivate, Deactivate, Revoke sessions.
- Rules: The page shows masked numbers; full numbers need a click that is audited. Campus-scoped delegates see only their campus.

**IDM-ADM-002 · Must · MVP · flag: core · [Spec]**
The Tenant Administrator can switch idm.* flags per tenant, campus or role, through the flag screen of Section 4 (see TFC).
- Acceptance: Given idm.biometric is turned off for role Parent When saved Then the biometric option disappears from the next sign-in or screen refresh for parent profiles and existing biometric unlocks fall back to PIN or code.
- Rules: Flags that never switch off: OTP sign-in, audit, consent (flag: core). A change takes effect within the propagation target in TFC-RUN-004 (95% within 60 seconds) and is logged.

**IDM-ADM-003 · Must · MVP · flag: idm.app_pin · [Spec]**
The Tenant Administrator can enforce PIN and biometric policy.
- Acceptance: Given policy "Require app PIN for staff profiles" (default on, cannot be turned off for payments, approvals and payslips) When enabled for parents or students Then the next sign-in asks to create a PIN before use.
- Rules: Options: require PIN for parent profiles; require biometric where the phone supports it; app lock timeout (immediately to 15 minutes); web inactivity timeout (5 to 15 minutes; default 15, Design); extra sensitive actions.

**IDM-ADM-004 · Should · MVP · flag: core · [Spec]**
The Tenant Administrator can configure sign-in policy within platform limits.
- Acceptance: Given policy options When saved Then they may set session lengths shorter than the platform default, "no trusted computers" and "no WhatsApp OTP" and these apply from the next sign-in.
- Rules: Longer lifetimes than the defaults in IDM-SES-001 are refused.

**IDM-ADM-005 · Could · P2 · flag: mod.student_learning · [Spec]**
The Tenant Administrator can change the class bands for student logins.
- Acceptance: Given the bands (default 6-12) When changed Then newly created logins follow them; existing logins are not removed without the parent's action.

**IDM-ADM-006 · Should · P3 · flag: idm.sso · [Design]**
A tenant can turn on Google or Microsoft sign-in for staff.
- Acceptance: Given idm.sso is on When a staff member signs in Then "Sign in with Google" or "Sign in with Microsoft" is offered in addition to OTP, and the mapped staff profile is found by the verified work email on the HR record.
- Rules: Shown as a website tile ("Google and Microsoft sign-in, single sign-on"); phasing unconfirmed. OTP stays available; multi-factor for staff (website) means SSO plus device or PIN step-up. Parents and students do not use SSO.

**IDM-ADM-007 · Must · MVP · flag: core · [Spec]**
The system shall support DhruvaOne support break-glass access to identity records.
- Acceptance: Given a written request from the Owner or school admin When support opens a Tenant Administrator view for 4 hours Then the access is time-boxed, shows a banner to the tenant and is audited; support cannot read business content.

### 3.3.15 Security requirements

**IDM-SEC-001 · Must · MVP · flag: core · [Spec]**
The system shall encrypt identity data in transit and at rest, hold it in an India region and keep secrets out of logs.
- Acceptance: Given a penetration test When run Then no OTP, PIN, token or full number appears in logs, analytics or crash reports; TLS 1.2+ is enforced.
- Rules: Matches the Trust page claims (India hosting, encryption, annual penetration test).

**IDM-SEC-002 · Must · MVP · flag: core · [Design]**
The OTP shall be 6 digits, the number shall be masked as "+91 98••• ••210" on screen, and no password shall exist.
- Acceptance: Given any screen showing a number When viewed Then it is masked (first 2 and last 3 digits) except in the owner's own entry field; the web design masks "98••• ••210", the app boards "98••• ••898", the switch board "98•••• 4521" (one display format is chosen: first two and last three, see Open questions).

**IDM-SEC-003 · Must · MVP · flag: core · [Spec]**
The system shall protect against automated abuse and replay.
- Acceptance: Given a captured OTP request When replayed Then it is rejected by nonce, device attestation or CAPTCHA; every sign-in API requires an app attestation or CAPTCHA token.

**IDM-SEC-004 · Must · MVP · flag: core · [Spec]**
The system shall never log a person in because of a link, a screenshot or a deep link.
- Acceptance: Given an invite or notification deep link When opened Then the app asks for sign-in or unlock first, then goes to the screen.

## 3.4 Business rules and policies

### 3.4.1 Permission scope levels
| Level | Meaning | Examples |
|---|---|---|
| Tenant | Everything in one tenant (group or standalone) | Trustee (read-only logs), Tenant Administrator (identity only), Standalone School Admin |
| Group | All campuses of one group tenant | Group Owner, group HR |
| Campus | One campus of a group, or the whole of a standalone school | Principal, Accounts, Front office, Security & IT, Counsellor |
| Department | One department's staff, plans and papers | HoD |
| Class/section | Assigned classes and sections | Class teacher, subject teacher |
| Own child | Children linked to this Person at this school | Parent |
| Self | Own records only | Student, support staff, any "Me" page |

Rules: scopes narrow, never widen. A role can only be assigned at or below the assigner's own scope. No profile ever receives scope in two tenants.

### 3.4.2 Sensitive actions that need step-up
Default list, enforced by IDM-LCK-004: fee payment and refund initiation; any Approve or Decline in Approvals; release of a salary bank file or payroll approval; opening a payslip; changing bank details; changing a mobile number or guardian link; export of student or staff lists; "Sign out everywhere"; viewing counselling notes. Step-up window 5 minutes.

### 3.4.3 Other policy rules
- **No passwords, ever.** OTP proves the number; PIN and biometric only unlock a device or step up an action.
- **Segregation of duties.** A person cannot assign, approve or deactivate their own role, leave, concession or access, in any role they hold.
- **The school's record is the account.** Names, numbers, relations and roles are changed only by the school's office, HR or Tenant Administrator, never by the person in the app.
- **Dhruva has no identity of its own.** Dhruva acts with the profile of the person asking, drafts only, and a person approves anything that changes a record or reaches a family.
- **One person, one Person.** Persons are keyed by verified mobile number; the same human with two numbers has two Persons unless a number change (IDM-REC-005) moves one to the other.
- **Minors.** Student logins exist by parent consent; students have no payment, message-to-parent or admin function.
- **Kill switch.** Flags off hide features and retain data; core items (sign-in, audit, consent) cannot be switched off.

## 3.5 Notifications and approvals raised by this section

| Event | Who is told | Channel / tier | Approval needed |
|---|---|---|---|
| New sign-in on a new device | The person (other devices); Tenant Administrator log for staff | Push, High | None |
| Sign out everywhere done | The person | Push on remaining devices, Normal | None |
| Lockout after wrong OTP or PIN | The person (screen); Tenant Administrator log | In-screen | None |
| Invite sent / invite expired | The invitee; office/HR | WhatsApp, SMS, email; Normal | None |
| Number add request | School office queue | In-app task, Normal | Office decides |
| New guardian number added | Existing primary guardian | WhatsApp or push, High | Office or Principal for fee-payer or pickup rights |
| Number change request | Office or HR; old number | In-app task; SMS to old number | Office or HR confirms identity |
| Role assigned / removed | The person; assigner's audit | Push, Normal | Assigner per IDM-LIF-003 |
| Staff offboarding done | HR, Principal, Tenant Administrator | In-app, Normal | None (HR starts the exit) |
| Flag change on idm.* | Tenant Administrator, Owner | In-app, Normal | Owner for tenant-wide security downgrades [Spec] |
| Support break-glass opened | Owner, school admin | Push, High | Written school request |

## 3.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| core | OTP sign-in, number-not-found, sessions and revocation, roles and scope, audit, consent, recovery | On, cannot be turned off | Safety and compliance items only |
| idm.web_login | Website and desktop-web sign-in | On | When off, the page shows only the app download panel; also needs ch.desktop_web for the web app |
| idm.multi_profile | Several profiles per number, picker, "Add a profile with another number", combined staff roles | On | Off = one profile per sign-in (IDM-PRF-005) |
| mod.profile_switching | Switch sheet, "All alerts", Ctrl + K switching | On | Independent of idm.multi_profile for display only |
| idm.app_pin | App PIN, staff profile lock, step-up, web re-PIN | On (staff), optional (parents) | Cannot be off for payments, approvals, payslips on any role |
| idm.biometric | Face ID / fingerprint unlock | On | Off hides toggles; PIN stays |
| idm.sso | Google/Microsoft sign-in for staff | Off | P3; extension points only |
| ch.whatsapp, ch.whatsapp.parent_bot, .teacher_bot, .staff_bot | WhatsApp identity matching and PIN flow | Per tenant | P2 for the bot; see Section 7 |
| ch.mobile_ios, ch.mobile_android, ch.desktop_web | Whether each channel can sign in | On | Channel off = sign-in on that channel refused with "Please use the app or website your school has turned on" |
| mod.student_learning | Student login creation and bands | On | See Section on student learning |

## 3.7 Non-functional requirements (identity)

- **IDM-NFR-001 · Must · MVP · flag: core · [Spec]** OTP SMS delivered to the provider within 3 seconds at p95; sign-in (verify to picker) under 1.5 seconds at p95; token refresh under 300 ms at p95.
- **IDM-NFR-002 · Must · MVP · flag: core · [Spec]** Sign-in service availability 99.9% monthly; if SMS is down the WhatsApp OTP route and a status banner are shown; existing sessions keep working.
- **IDM-NFR-003 · Must · MVP · flag: core · [Spec]** Peak load: all parents of a campus opening the app at 8:00 am. Sizing for 14 campuses in a quarter (about 3,800 new students, 296 staff on one campus) with 10 sign-ins per second sustained and 100 per second burst.
- **IDM-NFR-004 · Must · MVP · flag: core · [Spec]** Revocation (sign-out everywhere, deactivation) takes effect in 60 seconds worst case; role changes in 60 seconds.
- **IDM-NFR-005 · Should · MVP · flag: core · [Spec]** Sign-in works on the low-end Android phones and 3G; the app asks for SMS-read permission only through the OS one-tap flow, not blanket permission.
- **IDM-NFR-006 · Must · MVP · flag: core · [Spec]** Accessibility: OTP boxes work with screen readers; error text is not colour-only; Hindi and English labels for every sign-in string.
- **IDM-NFR-007 · Must · MVP · flag: core · [Spec]** Audit write is synchronous for sign-in, role and link changes; no such action succeeds if the audit write fails.

## 3.8 Open questions

1. **Check before OTP or after.** The designs show "We could not find this number" right after entering the number. That reveals whether a number is registered. Keep the design with throttling (IDM-NF-002), or send an OTP first and say "not found" only after verification? Decision for client and security review.
2. **Where is the switch?** The ProfileSwitch board puts it on the header chip; the design decision says "in Settings (gear on the notification centre)". Spec builds both (IDM-PRF-007); confirm.
3. **Web vs app login interpretation** ("not matching") is flagged unconfirmed in the design status; confirm the unregistered-number behaviour on web.
4. **One PIN or two.** App PIN (4 digits, "Required for staff pages and payments") and WhatsApp payslip PIN ("the PIN you set with HR"). Spec treats them as one account PIN; confirm, and confirm 4 digits vs 6.
5. **Mask format.** Designs show "+91 98••• ••210", "98••• ••898" and "98•••• 4521". Spec picks first two and last three digits.
6. **Parents on staff profiles.** Should a parent-only profile be allowed biometric without PIN? Spec allows it (IDM-LCK-001).
7. **Campus admin vs Tenant Administrator.** WhatsApp board shows a "Campus admin" settings card. Is it the principal's office, or a campus-delegated Tenant Administrator? Spec assumes the latter (IDM-ADM-001).
8. **Standalone School Admin vs Tenant Administrator.** Does the school admin hold both roles by default? Spec: yes at standalone schools, with the SoD rule applying to the admin's own access.
9. **Students' own numbers.** Whether Class 9-12 students may register their own number, and how a school creates logins when parents never installed the app.
10. **Non-Indian numbers** (NRI guardians) and email OTP: not designed; out of MVP.
11. **Owner identity at tenant creation.** How the first Owner or School Admin is verified (design shows only "Add a campus" invites). Spec assumes DhruvaOne onboarding with a signed order form.
12. **Phase of WhatsApp bot.** mvp-scope puts "Dhruva on WhatsApp" in Phase 1; prototypes show it now. Spec marks IDM-WAB as P2.
13. **Retention of identity audit** (2 years proposed) and deletion 90 days after exit need Legal confirmation.
14. **Who can approve a guardian link** that grants pickup rights (office vs two-person rule) and the relation to early-pickup approvals in Security & IT.

---

## Annex 3-A (engineering)

### Data entities
| Entity | Key fields | Notes |
|---|---|---|
| Person | person_id, mobile_e164 (unique), mobile_verified_at, language, pin_hash, pin_failed_count, pin_locked_until, status, created_at | Global; one per verified number. Holds no school data. |
| Profile | profile_id, person_id, tenant_id, campus_id?, kind (staff, parent, student), display_name_from_school, state, last_used_at, color_theme | Unit of access. Parent profile groups all children of one school. |
| Membership | membership_id, profile_id, role_id, scope {tenant, campus, department, section_ids}, source (hr, import, invite), starts_on, ends_on, state | One per role held; teacher + HoD = two memberships on one staff profile. |
| Role | role_id, key, capabilities[], scope_levels_allowed, is_staff, system (bool), tenant_id? | Catalogue roles are system roles; tenants may not edit capability sets in MVP. |
| Guardianship | guardian_link_id, parent_profile_id, student_id, relation, is_primary, is_fee_payer, can_pickup, consent_holder, state (pending, active, archived), verified_by, verified_at | Created by school office only. |
| StudentAccount | student_account_id, student_id, profile_id?, band, enabled_by_guardian_id, mobile_e164?, state | Exists only if parent enabled "Dhruva student app". |
| Device | device_id, person_id, platform, model_label, public_key, attestation_state, push_token, trusted_until, last_seen_at, last_city, revoked_at | One per install/browser. |
| Session | session_id, device_id, person_id, active_profile_id, refresh_family_id, issued_at, idle_expires_at, absolute_expires_at, step_up_at, state | Access token is a short JWT referencing session_id. |
| OTPChallenge | challenge_id, mobile_e164, channel (sms, whatsapp), code_hash, salt, created_at, expires_at, attempts, resends, state, ip_hash, device_id | Never stores the code in clear. |
| PinCredential | person_id, hash, algo, set_at, failed_count, locked_until | Could sit inside Person; split for key rotation. |
| Consent | consent_id, subject_student_id, given_by_person_id, purpose, text_version, given_at, withdrawn_at, channel | Per child per purpose. |
| InviteToken | invite_id, profile_id, channel, token_hash, expires_at, used_at | Preselects a profile only. |
| NumberAddRequest | request_id, mobile_hash, name, school_hint, relation, status, created_at, expires_at | From "Ask my school to add me". |
| WhatsAppBinding | wa_number, person_id, tenant_id_last_chosen, chosen_until, verify_before_use | 30-minute school memory. |
| AuditEvent | event_id, ts, tenant_id?, actor_person_id, actor_profile_id, action, target_type, target_id, channel, device_id, ip_coarse, result, reason | Append-only, hash-chained per tenant. |

### APIs
| Method + path | Purpose | Authz / role scope | Key errors |
|---|---|---|---|
| POST /auth/lookup | Optional registered-number check (throttled) | Public, attestation | 400 invalid_number, 429 rate_limited |
| POST /auth/otp/request | Send OTP (sms or whatsapp) | Public, attestation | 400 invalid_number, 404 not_registered (if lookup enabled), 429 rate_limited, 423 locked |
| POST /auth/otp/verify | Verify code, create session, return profile list | Public with challenge id | 400 invalid_code, 410 expired, 429 too_many_attempts |
| GET /auth/profiles | Profile list for the session's Person | Authenticated | 401 |
| POST /auth/switch | Switch active profile; re-issue token | Authenticated | 403 profile_not_available, 423 locked_needs_pin |
| POST /auth/refresh | Rotate refresh token | Refresh token | 401 reused_token (revokes family) |
| POST /auth/logout | End session on this device (all profiles) | Authenticated | |
| GET /auth/sessions | List devices and sessions | Authenticated (own) | |
| DELETE /auth/sessions/{id} and POST /auth/sessions/revoke-all | Revoke one / all | Own; Tenant Administrator for staff | 403 |
| POST /auth/pin/set, /auth/pin/verify, /auth/pin/reset | Set, verify, reset PIN (reset needs fresh OTP) | Authenticated | 423 pin_locked, 400 weak_pin |
| POST /auth/stepup | Challenge and verify PIN or biometric assertion | Authenticated | 401 stepup_required |
| POST /auth/devices/register | Register device key, attestation | Authenticated | 403 attestation_failed |
| POST /auth/number-add-requests | Create add request | Public, throttled | 429 |
| GET/POST /idm/people, /idm/profiles, /idm/memberships | Admin management of identity | Tenant Administrator, HR, Office (scoped) | 403, 409 conflict |
| POST /idm/profiles/{id}/invite, /suspend, /reactivate, /deactivate | Lifecycle | Per IDM-LIF-003 | 409 invalid_transition |
| POST /idm/number-changes | Start/confirm number change | Office (parents), HR (staff) | 409 number_in_use |
| POST /idm/guardianships and PATCH /idm/guardianships/{id} | Child links and verification | Office, Principal | 409, 403 two_person_required |
| POST /idm/student-accounts | Create/switch off student login | Guardian of the child | 403, 409 band_not_allowed |
| GET /idm/audit | Query and export audit events | Tenant Administrator, Owner | 403 |
| GET/PUT /idm/policy | Read/set sign-in and PIN policy | Tenant Administrator | 422 beyond_platform_limits |
| POST /wa/identify (internal) | Resolve WhatsApp number to profiles | Internal service | 404 unknown_number |
| POST /wa/pin/verify (internal) | Verify PIN from WhatsApp Flow | Internal service | 423 pin_locked |

### Events
| Event | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| auth.otp.requested | Code issued | challenge_id, channel, masked number | Audit, abuse monitor |
| auth.otp.failed / auth.otp.locked | Wrong code / limit hit | attempts, ip_hash | Audit, security alerts |
| auth.signin.succeeded | OTP verified | person_id, device_id, profile_count | Audit, notifications (new device) |
| auth.profile.switched | Active profile changed | from, to, step_up | Audit |
| auth.stepup.succeeded / failed | PIN or biometric step-up | action, method | Audit, finance, approvals |
| auth.pin.set / reset / locked | PIN change | person_id | Audit, WhatsApp |
| auth.session.revoked | Revocation | scope (one, all), reason | Push, API gateway |
| idm.profile.invited / activated / suspended / deactivated | Lifecycle change | profile_id, by | Audit, notifications, HR |
| idm.membership.assigned / removed | Role change | role, scope, by | Audit, permission cache |
| idm.guardianship.created / verified / archived | Child link change | student_id, relation | Audit, fees, transport, notices |
| idm.number.changed | Number moved | old_masked, new_masked | Audit, WhatsApp, sessions |
| idm.studentaccount.created / disabled | Student login change | student_id, guardian | Audit, student app |
| idm.consent.given / withdrawn | Consent change | purpose | Audit, channels |
| idm.flag.changed | idm.* flag edit | flag, scope, by | TFC, audit |
| hr.employee.exit_started / exit_completed (consumed) | HR exit | last_day | Identity offboarding job |

### State machines / workflows
**OTP challenge:** Created -> Sent -> (Verified | Expired | Locked | Superseded by resend | Cancelled by "Use a different number"). Verified is terminal; Locked after 5 wrong codes.

**Profile lifecycle:** Prepared (from import or office) -> Invited -> Active -> (Suspended <-> Active) -> Deactivated. Invited -> Invite expired -> Invited (re-send). Deactivated -> Archived after retention. Active -> Deactivated via exit, child left (parents, after 30 days), or admin action.

**Guardianship:** Pending -> Active (guardian OTP or office check) -> Archived (child left, guardian removed). Pending expires after 30 days.

**Session:** Created -> Active -> (Idle-expired | Absolute-expired | Revoked | Reuse-detected). Step-up is an attribute of an Active session (valid 5 minutes), not a separate session.

**Lock state per device profile:** Locked -> Unlocked (PIN or biometric) -> Locked (timeout, switch away on web, app background past app lock timeout). 5 wrong PINs: Locked-out (30 min).

**Number change:** Requested -> Identity checked -> New number OTP-verified -> Applied (sessions revoked, PIN reset) | Rejected | Expired.

**Staff offboarding:** HR exit started -> last working day -> Deactivate memberships -> revoke sessions -> exit clearance continues without login.

### Permission matrix
Legend: Y = allowed in own scope; O = own records only; R = read only; A = approve; - = not allowed.

| Capability | Owner | Principal / Admin | Tenant Admin | HR | Office / Admissions | HoD / AC / Teacher | Parent | Student | Trustee |
|---|---|---|---|---|---|---|---|---|---|
| Sign in, switch own profiles, own devices | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Set own PIN / biometric | Y | Y | Y | Y | Y | Y | Y | Y (optional) | Y |
| View people and profiles of tenant | R (group) | R (campus) | Y | Y (staff) | R (families) | - | - | - | - |
| Invite / resend invite | - | Y (staff of campus) | Y | Y (staff) | Y (parents) | - | - | - | - |
| Assign / change / remove role | A (Principal, Tenant Admin) | - | Y (not Owner, Principal) | Y (staff roles) | - | - | - | - | A (School Admin) |
| Suspend / deactivate profile | - | Y (cut access) | Y | Y | - | - | - | - | - |
| Create / edit child-guardian link | - | A (two-person) | - | - | Y | - | - | - | - |
| Change a person's mobile number | - | - | - | Y (staff) | Y (parents) | - | - | - | - |
| Create / switch off student login | - | - | - | - | - | - | Y (own child) | - | - |
| Revoke another person's sessions | - | Y (campus staff) | Y | Y (staff) | - | - | - | - | - |
| Read identity audit | R (group) | R (campus) | Y | R (staff) | - | - | O (own activity) | O | R (logs only) |
| Switch idm.* flags | A | - | Y | - | - | - | - | - | - |
| Set PIN / biometric / session policy | A | - | Y | - | - | - | - | - | - |
| Read counselling notes | - | - | - | - | - | Counsellor only | - | - | - |
| Open payslip, approve, pay | A (approvals) | Y, step-up | - | Y, step-up | - | O (payslip) | Pay own fees | - | R (logs) |

### Proposed flags
None. All flags used are in the canonical catalogue.
