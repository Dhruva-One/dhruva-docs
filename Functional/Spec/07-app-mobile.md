# 7. App - Mobile

Area code: MOB. Sources: appshell, parent, transport (bus attendant), student_mid, student_sr, platform inventories; the phone boards of every staff role; project docs mvp-scope and design-status.

Conventions used in this section
- "Phase" follows mvp-scope.md. MVP = Final MVP build (Oct to Dec 2026). P2 = the original roadmap's Phase 1 (Apr to Sep 2027). P3 = the original roadmap's Phase 2 (Oct 2027 to Mar 2028).
- "DSK-xxx" names the desktop role module in Section 6. Module codes in the table in 7.2 are assumed from the role names; reconcile them when Section 6 is final (see 7.8, Q1).
- The phone app is called "Dhruva One" (store name "Dhruva One: School App"). "The app" means both the iOS and the Android build unless a platform is named.

---

## 7.1 Purpose, scope and out-of-scope

### Purpose
The phone app is the one app for everybody who carries a phone to school life: parents, students, teachers, heads of department, coordinators, principals, owners, accounts, admissions, HR, security, transport and bus attendants, and the admin of a standalone school. It has one login (mobile number and a code, no password), one shell (sign-in, profiles, notifications, security, Dhruva) and one role home per profile that opens on what needs the person first.

Three groups of users exist only on the phone or are phone-first:
- Parents and guardians. There is no parent desktop. The parent app is the full product for a family.
- Bus attendants. The attendant app is phone only, bilingual (English and Hindi), with large buttons, safety rules and an offline queue.
- Students of Classes 6 to 8 and 9 to 12. They also have a desktop (Section 6), but the phone is their main device and some features (subject games, readiness ring, house cup sheets) are phone only.

Everyone else has the same data and the same approvals on phone and desktop. Section 6 specifies what each role can do. This section specifies how the same function behaves on the phone: the tab bar, bottom sheets, what is reduced, what works with a poor network, and what exists only on the phone.

### In scope
1. The app shell: app icon, splash, language, notification permission, biometric offer, mobile number, one-time code, choose profile, number not found, "Setting up your day", home per persona, profile and school switching, Me tab, security (Face ID or fingerprint, App PIN), sign out, lock screen, in-app banner, notification centre, notification settings.
2. The Dhruva orb on every screen and the Ask Dhruva sheet.
3. The Parent app, the Bus attendant app, the Student 6-8 and Student 9-12 phone apps in full.
4. A phone summary for every other role by reference to its DSK module (tab bars, reduced features, phone-only functions).
5. Mobile non-functional requirements: platform versions, push, deep links from notifications and WhatsApp, offline queue and sync, camera, photo and microphone flows, accessibility, localisation, update and force-update, crash and performance budgets, battery, data usage.
6. Store listing, app icon, iOS versus Android differences.

### Out of scope (covered elsewhere)
- Identity model, OTP issuing, token lifetimes at the platform level: Section 3 Identity (IDM). This section states how the phone uses them.
- Dhruva's reasoning, sources and approval rules: Section 4 AI. This section states how the phone shows them.
- WhatsApp conversations: Section 5 WhatsApp (WAB). This section covers only links from WhatsApp into the app.
- Feature flag administration: TFC. This section lists the flags it uses.
- Desktop screens and role functions: Section 6 (DSK).
- Tablet (iPad, kiosk) layouts: P3. The app installs on tablets and shows the phone layout, centred.
- GPS and RFID bus tracking: P2/P3. The MVP bus view is driven only by attendant taps.

---

## 7.2 Actors and roles

| Persona | Profile label in the picker | Phone-only? | Phone home (tab bar) | DSK module (Section 6) |
|---|---|---|---|---|
| Parent / guardian | "Parent of Navya (10-C) and Arjun (2-B)" | Yes | Home, Progress, Fees, Messages | none (no parent desktop) |
| Bus attendant | "Bus attendant, Bus 7" | Yes | Trip, Children, SOS, Me | none |
| Student 6-8 | "Student, Class 7-B" | No | Home, Schedule, Learn, Progress | DSK-STU (Student 6-8) |
| Student 9-12 | "Student, Class 10-C" | No | Home, Schedule, Learn, Progress | DSK-STU (Student 9-12) |
| Teacher | "Teacher, Maths" | No | Today, Inbox, Students, Prep, Calendar | DSK-TCH |
| Head of department | "Head of Maths" | No | Today, Reviews, Team, Progress | DSK-HOD |
| Academic coordinator | "Academic coordinator" | No | Today, Cover, Progress, Timetable | DSK-ACD |
| Exam cell | "Exam cell in-charge" | No | Today, Papers, Exam days, Marks, CBSE | DSK-EXM |
| Counsellor | "School counsellor" | No | Today, Students, Sessions, Guidance | DSK-CNS |
| Principal | "Principal" | No | Today, Calendar, Fees, Reports, Me (bell opens Approvals) | DSK-PRN |
| Group owner | "Group owner" | No | Home, Campuses, Insights, Calendar (Approvals from the Home card, Notices from "Send a notice") | DSK-OWN |
| Standalone school admin | "School admin" | No | Today, People, Money, Intake, School | DSK-ADM |
| Finance and accounts | "Accounts in-charge" | No | Home, Alerts, Reports, Bank (Approvals, Fees, Bills, Compliance as pushed screens) | DSK-FIN |
| HR and payroll | "HR and payroll" | No | Today, Requests, People, Payroll | DSK-HRP |
| Security and IT | "Security and IT in-charge" | No | Today, Jobs, Gate, Team (Systems from Today) | DSK-SEC |
| Transport in-charge | "Transport in-charge" | No | Today, Live, Safety, Messages | DSK-TRN |
| Admissions counsellor | "Admissions counsellor" | No | Today, Families, Tours, Seats | DSK-ADS |
| Trustee (standalone) | "Trustee" | Not designed on phone | Not designed; sees the payroll and refund log read-only | DSK-ADM (trustee view) |

Notes
- Staff roles all have "Me" (leave balances, apply for leave or out on duty, payslips, notices) opened from the avatar at top right (teacher, HoD, HR, security, transport, admissions) or from a tab (principal). See MOB-ME-002.
- The Teacher board shows the tab bar "Today, Inbox, Students, Prep, Calendar". The App end-to-end board shows a staff bar "Today, Inbox, Students, Prep, Me". The role board is taken as the build target; see Q2.
- Owner phone tabs are inferred from the owner inventory (Home, Campuses, Insights, Calendar); confirm in Q3.
- Roles that have no tablet or kiosk layout in the MVP: all.

---

## 7.3 Functional requirements

### 7.3.1 App icon, store presence and platform differences (MOB-STO)

**MOB-STO-001 · Must · MVP · flag: ch.mobile_ios, ch.mobile_android · [Design]**
The system shall ship one app icon, the Halo orb, on both platforms, with the name "Dhruva One" under it.
- Acceptance: Given the app is installed on iOS When the home screen is shown Then the icon is a 1024 x 1024 px source with no transparency and no pre-rounded corners, and the iOS Light, Dark and Tinted variants all exist. Given Android When the launcher shows the icon Then it is an adaptive icon 108 x 108 dp with artwork inside the 66 dp safe circle, a navy background layer, a Halo foreground layer and a monochrome layer for themed icons; a 512 x 512 Play Store icon exists.
- Rules: the status-bar and notification icon on both platforms is the one-colour Halo ring and eyes. The multi-colour ring appears only on Dhruva (icon, orb, assistant button, splash).

**MOB-STO-002 · Must · MVP · flag: ch.mobile_ios · [Design]**
The system shall publish an App Store listing that matches the store kit.
- Acceptance: Given the listing When reviewed Then it has name "Dhruva One: School App", subtitle "Parents, students and staff", category Education, age rating 4+, price Free, devices iPhone and iPad, minimum iOS 15, the 100-character keyword string from the kit, the promotional text and description from the kit, the privacy label "Data linked to you: contact info, identifiers, user content. No tracking. No third-party ads.", and five 6.7-inch screenshot cards in this order: "Learning, reimagined with AI", "Your child's school, in one calm app", "Pay fees in two taps", "See the bus coming", "Teachers: attendance in seconds".
- Rules: the first three cards are what a parent sees without scrolling; staff views come last.

**MOB-STO-003 · Must · MVP · flag: ch.mobile_android · [Design]**
The system shall publish a Google Play listing that matches the store kit.
- Acceptance: Given the listing When reviewed Then it has name "Dhruva One: School App", subtitle "Fees, bus, attendance and notices", rating "Everyone", "Contains no ads", minimum Android 8.0, the short description "Ask Dhruva, the AI assistant for your school. Fees, bus, attendance and notices.", the same full description as iOS, a 1024 x 500 feature graphic, and screenshots 1 to 4 as on iOS with card 5 the admin view "Admins: one decision at a time".
- Rules: Data safety text: "Data shared: none with third parties. Data collected: name, phone, school records. Encrypted in transit. You can ask your school to delete it."

**MOB-STO-004 · Should · MVP · flag: ch.mobile_ios, ch.mobile_android · [Spec]**
The system shall keep store text, "What's new" and screenshots versioned with each release and reviewed by product before submission.
- Acceptance: Given a release candidate When it is submitted Then the "What's new" text names the changes in plain words (the current text is "Meet Dhruva, now in the app. Ask about fees, marks and dates. Plus quiet hours and faster sign-in with Face ID." on iOS and "...fingerprint sign-in." on Android) and no claim in the listing is untrue for the build.
- Rules: store claims about languages must list only languages that are live (see MOB-SHL-003).

**MOB-STO-005 · Must · MVP · flag: core · [Design]**
The system shall apply the native look of each platform while keeping content, colours and flows identical.
- Acceptance: Given the same screen on both platforms When compared Then content, order and colours match; iOS shows its tab bar, squircle radii and 51 pt toggles; Android shows Material 3 shapes, a pill indicator on the navigation bar, Material toggles and an extended "Ask Dhruva" button.
- Rules: the full list of platform differences is in 7.4 (table 7-D).

### 7.3.2 First run (MOB-SHL)

**MOB-SHL-001 · Must · MVP · flag: core · [Design]**
The system shall open a first-run splash with the orb, the wordmark "Dhruva One" and the line "One calm app for your school".
- Acceptance: Given the app is opened for the first time When the splash shows Then two actions exist: "Get started" (primary) and a text link "I already use Dhruva One · Sign in"; both lead to the language screen on first install and to the mobile number screen when a language is already stored.
- Rules: the splash is dark navy. With "Reduce motion" on, the orb is a still pose (MOB-NFR-008).

**MOB-SHL-002 · Must · MVP · flag: core · [Design]**
The system shall show step dots at the top of the first-run flow and allow going back one step.
- Acceptance: Given the first-run flow When the person is on the language, notification, biometric or mobile number step Then the dots show position (first of four on the language step) and a back arrow returns to the previous step without losing entries.

**MOB-SHL-003 · Must · MVP · flag: ai.translation · [Design]**
The system shall ask "Choose your language" once, up front, with a note that it can be changed in Settings.
- Acceptance: Given the language screen When it opens Then it reads "You can change this any time in Settings. Dhruva replies in the language you pick." and lists six rows with native name and English name: English, हिंदी Hindi, ਪੰਜਾਬੀ Punjabi, ગુજરાતી Gujarati, मराठी Marathi, தமிழ் Tamil; one row is selected with a check; "Continue" saves it.
- Rules: [Spec] At MVP only English and Hindi are selectable; the other four rows show "Coming soon" and cannot be selected, because regional languages are Phase 1 (P2) and the notification rules confirm only English and Hindi. A tenant may hide the four rows entirely (flag ai.translation). The device language pre-selects Hindi or English when it matches; otherwise English.

**MOB-SHL-004 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall ask for notification permission once, with a reason, before the native prompt.
- Acceptance: Given the pre-permission screen When it opens Then it reads "Never miss what matters" with the line "Attendance, fees due, the bus on its way, and notes from teachers." and then the native prompt. iOS text: "“Dhruva One” Would Like to Send You Notifications. Alerts for attendance, fees, bus and messages from your school. You choose which ones in Settings." with "Don't Allow" and "Allow". Android text: "Allow Dhruva One to send you notifications?" with "Allow" and "Don't allow".
- Rules: [Spec] The pre-permission screen is shown once per install. If the person declines, the app never re-shows the native prompt on iOS (the OS blocks it); a persistent line in Notification settings explains how to turn it on (MOB-NTF-009). On Android 12 and lower there is no runtime prompt; the screen is informational and a "Continue" button replaces the native prompt.

**MOB-SHL-005 · Should · MVP · flag: idm.biometric · [Design]**
The system shall offer Face ID or fingerprint during first run and make it optional.
- Acceptance: Given the device has biometrics enrolled When the biometric step shows Then the title is "Open Dhruva with Face ID" (iOS) or "...fingerprint" (Android), the body "Skip the code next time. Your login stays on this phone only, and you can turn it off in Settings.", buttons "Turn on Face ID" or "Turn on fingerprint" and "Not now".
- Rules: [Spec] Step is skipped when no biometric is enrolled. The same offer is made again once, the first time a staff profile is opened (MOB-SEC-001).

**MOB-SHL-006 · Must · MVP · flag: core · [Spec]**
The system shall remember first-run completion and skip the splash, language and permission steps on later launches.
- Acceptance: Given first run is finished When the app is opened again Then it goes directly through the launch gate (state machine in the Annex) to the last profile.

### 7.3.3 Sign in with mobile number and code (MOB-AUT)

**MOB-AUT-001 · Must · MVP · flag: core · [Design]**
The system shall ask for the mobile number the school has on record.
- Acceptance: Given the number screen When it opens Then it reads "Enter your mobile number" with "Use the number your school has on record. We find every school and role linked to it. No passwords.", a "+91" prefix, a 10-digit field, the line "Your number is only used to sign you in and to send school messages." and a "Send code" button.
- Rules: digits only. Fewer than 10 digits shows "Enter your 10-digit mobile number". The sample chips on the board (Parent, Teacher and HoD, Owner, Unknown number) are demo shortcuts and are not shipped. There is no school search and no username.

**MOB-AUT-002 · Must · MVP · flag: core · [Design]**
The system shall ask for a 6-digit code sent by SMS and verify it.
- Acceptance: Given a code was sent When the screen "Enter the 6-digit code" shows Then it reads "Sent to +91 98••• ••898 by SMS. It expires in 10 minutes.", has six boxes, "Verify" disabled until six digits are typed, and a countdown "Resend code in 0:24". A tap on "Verify" with a correct code moves to profile choice; an incomplete code shows "Enter the 6-digit code".
- Rules: [Spec] Resend becomes available 30 seconds after the previous send (the board shows about 24 to 28 seconds; 30 is the rule). At most 5 wrong entries per code, then the code is dead and "Send a new code" is required. At most 5 sends per number per hour; after that "Too many tries. Please wait 30 minutes." Rules are owned by IDM; the phone shows the server message.

**MOB-AUT-003 · Must · MVP · flag: core · [Design]**
The system shall autofill the code from Messages on iOS and from SMS on Android.
- Acceptance: Given the code arrives by SMS When the keyboard suggestion appears Then iOS shows "From Messages 482913" and Android fills from the SMS Retriever; tapping the suggestion fills all six boxes and enables "Verify".
- Rules: [Spec] Android uses the SMS Retriever API (no SMS read permission). The SMS carries the app hash. If autofill fails the person can type the code.

**MOB-AUT-004 · Should · MVP · flag: ch.whatsapp · [Design]**
The system shall let the person receive the code on WhatsApp instead.
- Acceptance: Given the code screen When "Use WhatsApp instead" is tapped Then a code is sent to the same number on WhatsApp, the countdown restarts and the text "Sent to +91 98••• ••898 on WhatsApp." replaces "by SMS".
- Rules: only after the first resend window has passed; hidden if the tenant has ch.whatsapp off.

**MOB-AUT-005 · Must · MVP · flag: idm.multi_profile · [Design]**
The system shall show a "Choose a profile" screen when the verified number has more than one profile, and skip it when there is exactly one.
- Acceptance: Given a number with several profiles When verified Then the screen reads "Hi Neha, who are you today?" and "One login, 4 profiles on this number. Switch any time from the top of the app.", groups profiles under "DPS GROUP · DPS GURUGRAM SEC 45", "DPS GROUP · DPS NOIDA SEC 132" and "SARASWATI VIDYA NIKETAN, KARNAL" with the row text (for example "Teacher · Maths", "10-C, 10-B, 9-C · Head of Maths", "Parent of Rhea (6-A) and Veer (3-B)", "Standalone school"), a red chip with the count of new items ("2 new"), one row selected, the footer "Your own children never appear in your staff profile. Staff pages ask for your PIN or Face ID (fingerprint on Android)." and a primary button whose label follows the selection ("Continue as teacher").
- Given a number with one profile When verified Then the app goes straight to "Setting up your day".
- Rules: [Spec] The header count equals the number of profiles, not rows: Teacher and Head of Maths at one campus are two profiles that share one row only when the designs group them; the picker lists them as separate selectable profiles so the person can pick Teacher or Head of Maths explicitly (the board shows one row; see Q4). The checkbox "Open the last profile I used next time" is on by default.

**MOB-AUT-006 · Must · MVP · flag: core · [Design]**
The system shall show a clear dead end when the number is not on any school's record.
- Acceptance: Given an unknown number When the code is verified (or when the number is submitted, per IDM) Then the screen reads "We could not find this number", "+91 90000 12345 is not on any school's record yet. Ask your school office to add it, or try the number you gave at admission.", with buttons "Try another number" and "Ask my school to add me".
- Rules: [Spec] To avoid revealing which numbers exist, the app always sends the code first and shows this screen after verification fails to match a record (IDM decides). Inline form of the older prototype ("This number is not registered with any school. Ask your school office to add it, then try again.") is retired.

**MOB-AUT-007 · Should · MVP · flag: core · [Spec]**
The system shall send an "add me" request when "Ask my school to add me" is tapped.
- Acceptance: Given the number-not-found screen When "Ask my school to add me" is tapped Then a short form asks for name, role (parent, student, staff), and "School name or city" (free text, no list), and on "Send" shows "Request sent. The school office will add your number and we will message you." and creates an AddMeRequest (Annex).
- Rules: if the app was installed from a school invite link, the school is attached and the request goes to that school's office; otherwise it goes to the DhruvaOne support queue, which forwards it. The design does not draw this action (Q5). The person is told by SMS when the number is added. At most 3 requests per number per day.

**MOB-AUT-008 · Must · MVP · flag: core · [Design]**
The system shall show "Setting up your day" while the chosen profile loads.
- Acceptance: Given a profile was chosen When loading Then the orb with a rainbow progress bar, a greeting by time of day and name ("Good morning, Ms. Arora") and a one-line summary ("Setting up your day at DPS Gurugram Sec 45: 6 classes and 1 cover.") appear, then the profile home.
- Rules: [Spec] The summary line is built from the profile's real counts (classes and covers for a teacher; children for a parent; buses for transport). If loading passes 8 seconds the line becomes "Still setting up..." and a "Try again" appears after 20 seconds; if cached data exists the home opens from the cache with a "Last updated 7:52 am" strip.

**MOB-AUT-009 · Must · MVP · flag: core · [Spec]**
The system shall keep the person signed in with a refreshable session and end it only on sign-out, revocation, or long inactivity.
- Acceptance: Given a signed-in phone When the app is idle 30 days (parent, student, attendant) or 14 days (other staff) Then the next launch asks for a new code. Given an admin or the person revokes the device (MOB-SEC-006) Then the next request returns "Signed out" and the app returns to the number screen.
- Rules: access token 15 minutes, refresh token rolling; values are Spec assumptions and owned by IDM. Tokens are stored in the iOS Keychain and the Android Keystore.

**MOB-AUT-010 · Must · MVP · flag: core · [Spec]**
The system shall handle a new phone, a changed number and a lost phone without support help.
- Acceptance: Given a new phone When the same number is entered Then a new code is required, biometrics and PIN are set up again, and the old phone stays signed in until revoked. Given a lost phone When "Sign out everywhere" is used on another device or the school office revokes the number Then all sessions end and push tokens are deleted. Given a number change at the school office Then the old number stops working at once.
- Rules: the design does not draw device change, session expiry or biometric failure (Q6); these are Spec.

### 7.3.4 Profiles and school switching (MOB-PRF)

**MOB-PRF-001 · Must · MVP · flag: mod.profile_switching · [Design]**
The system shall model a profile as one school (or campus) plus one role, linked to the number, and show the current profile in a chip at the top of every home screen.
- Acceptance: Given the profile home When it opens Then a chip shows the school short name and role detail ("DPS Gurugram · Parent · 2 children"), a bell shows the count of items needing attention in the other profiles, and nothing from another profile is visible.
- Rules: children in one school stay together in one parent profile (linked by the school office). A child at another campus or school is another profile. A teacher and a parent profile never mix; the staff profile hides the person's own children and the parent profile hides class data.

**MOB-PRF-002 · Must · MVP · flag: mod.profile_switching · [Design]**
The system shall open a "Switch profile" sheet from the profile chip.
- Acceptance: Given the chip is tapped When the sheet opens Then it reads "Switch profile" with "One login for every role and school linked to your phone number.", the phone number, one row per profile (school, role tag, children or classes, a red "needs you" line, a check on the current one, "Active" or "in use"), and a dashed button "+ Add a profile with another number". Tapping outside closes it; tapping the current profile just closes it.
- Rules: order is active profile first, then other campuses and schools by number of new items. Where the Me tab also offers "Switch profile" it opens the same sheet. The design status doc places switching in Settings (gear on the notification centre) while the profile board places it at the top; both entry points exist (MOB-ME-001, Q7).

**MOB-PRF-003 · Must · MVP · flag: mod.profile_switching · [Design]**
The system shall switch profile without signing out and show a short hand-over.
- Acceptance: Given another profile is tapped When the switch runs Then the sheet closes, a hand-over screen shows two avatars and an arrow with "Switching to DPS Noida Sec 132. Parent of Rhea and Veer. Your teacher profile stays signed in and one tap away.", then the new home appears in that profile's colours, menu and data with the toast "Switched to DPS Noida Sec 132 · Parent".
- Rules: [Spec] Switch completes within 1.5 seconds on a warm cache. Caches are namespaced per profile; nothing from the old profile is left in memory or on screen. Each profile keeps its own colours (group campuses share the look; a standalone school has its own colours).

**MOB-PRF-004 · Must · MVP · flag: idm.app_pin · [Design]**
The system shall require PIN or biometrics when switching to a staff profile.
- Acceptance: Given a staff profile is selected When the switch starts Then the lock screen "Unlock your teacher profile" shows "Staff profiles are protected, so a child with your phone cannot open your class data.", a four-dot PIN keypad, "Use Face ID" (or fingerprint) and "Cancel"; a right PIN or biometric opens the profile with the toast "Unlocked · Teacher at DPS Gurugram".
- Rules: see MOB-SEC-002 for the lock rules.

**MOB-PRF-005 · Should · MVP · flag: mod.profile_switching · [Design]**
The system shall show "All alerts" across profiles from the bell.
- Acceptance: Given the bell is tapped When "All alerts" opens Then each alert is labelled "<SCHOOL> · <ROLE>" with its text and time; tapping one jumps to that profile (asking for the PIN if it is a locked staff profile); "Close" dismisses.
- Rules: the bell's accessibility label is "<n> items need you in your other profiles".

**MOB-PRF-006 · Should · MVP · flag: mod.profile_switching · [Design]**
The system shall let a person add a profile with another number.
- Acceptance: Given "+ Add a profile with another number" is tapped Then the message "Add a profile: enter a different number and verify it with an OTP" leads to the number and code screens; after verification the new number's profiles join this phone's profile list as a second identity.
- Rules: [Spec] A phone may hold at most 3 numbers. Profiles from different numbers are shown in separate groups in the sheet; sign-out affects all.

**MOB-PRF-007 · Must · MVP · flag: mod.profile_switching · [Design]**
The system shall reopen on the last profile used.
- Acceptance: Given the checkbox "Open the last profile I used next time" is on When the app is reopened Then the last profile loads (after biometric or PIN if it is staff or if Face ID is on).
- Rules: when off, the app shows "Choose a profile" at each cold start.

**MOB-PRF-008 · Could · P2 · flag: mod.profile_switching · [Design]**
The system shall accept links that open a specific profile (see MOB-NFR-006).
- Acceptance: Given a link names a tenant and role When opened Then the app switches to the matching profile (with unlock if needed) before showing the target screen.

### 7.3.5 Security on the phone (MOB-SEC)

**MOB-SEC-001 · Should · MVP · flag: idm.biometric · [Design]**
The system shall let the person turn "Open with Face ID" (or fingerprint) on and off.
- Acceptance: Given Me > Security When the toggle "Open with Face ID" (iOS) or "Open with fingerprint" (Android) is on Then the app asks for the biometric on every cold start and every return after the lock delay; the toggle's help text is "Skip the code on this phone".
- Rules: "Your login stays on this phone only": the biometric never leaves the device; the app stores only a Keychain or Keystore key bound to biometric enrolment. [Spec] If the biometric set changes on the device (new face or fingerprint), the key is invalidated and the app asks for the PIN, then re-enables.

**MOB-SEC-002 · Must · MVP · flag: idm.app_pin · [Design]**
The system shall require an App PIN for staff pages and for payments.
- Acceptance: Given a staff profile or a finance payment action When the profile opens or the action is requested Then a PIN (or biometric if on) is asked even if already signed in; the row in Security reads "App PIN · Required for staff pages and payments" with a "Change" action.
- Rules: [Spec] PIN is 4 digits (the prototype shows four dots). Set on first staff-profile open with confirm entry. Stored as a salted hash in the Keychain or Keystore, never sent to the server in clear. Auto-lock: staff profiles lock after 2 minutes in the background and on every profile switch; finance payments ask for PIN or biometric on each payment confirmation. Parents are locked only if "Open with Face ID" is on, after 1 minute in the background.

**MOB-SEC-003 · Must · MVP · flag: idm.app_pin · [Spec]**
The system shall limit PIN attempts and give a recovery path.
- Acceptance: Given wrong PIN entries When the 5th wrong entry occurs Then entry locks for 30 seconds, doubling at each further 5 wrong tries up to 15 minutes; after 10 wrong tries the profile is signed out and a new code is needed. "Forgot PIN" starts a new code and then asks for a new PIN.
- Rules: the design does not draw PIN set-up and reset (Q6). A biometric failure falls back to the PIN after 3 attempts.

**MOB-SEC-004 · Should · MVP · flag: core · [Design]**
The system shall offer "Hide balances on app switcher".
- Acceptance: Given the toggle is on When the app goes to the recent-apps view Then fee and marks screens are blurred ("Blur fees and marks in recent apps").
- Rules: [Spec] On Android the payment, PIN and payslip screens use FLAG_SECURE (no screenshots) regardless of the toggle. On iOS a blur view covers the window on resign-active.

**MOB-SEC-005 · Must · MVP · flag: core · [Design]**
The system shall show Me > Security with the exact rows of the design.
- Acceptance: Given Me > Security When opened Then rows appear in this order: "Open with Face ID" toggle, "App PIN" with "Change", "Hide balances on app switcher" toggle, "Signed in on" ("This phone · iPhone 15" or "Pixel 8", "Active"), "Sign out everywhere" ("Use if you lose a phone", red "Sign out"), and the footer "Staff and finance pages ask for your PIN or Face ID (fingerprint) before opening, even when you are already signed in."

**MOB-SEC-006 · Must · MVP · flag: core · [Design]**
The system shall list the devices signed in and allow "Sign out everywhere".
- Acceptance: Given "Sign out everywhere" is tapped and confirmed When it succeeds Then every other session is revoked, every push token other than this phone's is deleted, and the "Signed in on" list shows only this phone.
- Rules: [Spec] The list shows device model, platform, last seen and city or "Active". Each other device has a "Sign out" action.

**MOB-SEC-007 · Must · MVP · flag: core · [Design]**
The system shall sign out of the phone with a confirmation sheet.
- Acceptance: Given the red button "Sign out of this phone" is tapped When the bottom sheet "Sign out of Dhruva One?" opens Then it reads "You will be signed out of all 4 profiles on this phone. Your school data stays safe. Next time you will need a new code." with a red "Sign out" and an outline "Stay signed in".
- Rules: [Spec] Sign-out deletes the local database, the offline queue (after warning "3 items have not been sent yet. Sign out anyway?" if the queue is not empty), cached files, tokens, the push token on the server and the PIN.

**MOB-SEC-008 · Must · MVP · flag: core · [Spec]**
The system shall keep local data encrypted and minimal.
- Acceptance: Given the app stores data on the phone When inspected on a rooted or jailbroken device Then the local database and files are encrypted with a key held in the Keychain or Keystore; staff caches are cleared when a staff profile is locked for more than 24 hours; no school data is written to shared storage or logs.
- Rules: TLS 1.2 or higher for all traffic; certificate pinning for the API host (Should). Clipboard use for the OTP only.

### 7.3.6 Notifications on the phone (MOB-NTF)

**MOB-NTF-001 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall deliver notifications in three tiers.
- Acceptance: Given an event When it is delivered Then Urgent breaks quiet hours and repeats once after 5 minutes if unopened; High shows a banner in school hours and waits overnight; Normal is silent and grouped.
- Rules: iOS marks Urgent as Time Sensitive only; Android uses channels Safety, Fees, Bus, School updates and Messages, each mutable in system settings. [Spec] A sixth channel "Work" carries staff task alerts (cover, attendance not marked, approvals) so staff can mute them without muting Safety.

**MOB-NTF-002 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall show short, named lock-screen cards with the child's name.
- Acceptance: Given the lock-screen cards of the design When shown Then they read "Bus 7 is 10 minutes away" with "Sector 45 stop · Navya's pickup, now", "Navya reached school" with "Marked present at 7:52 am by Ms. Kavya Reddy", and "October fee due Fri 16 Oct" with "Rs 80,200 for Navya and Arjun. Pay by UPI."; Android adds the channel in the header ("Dhruva One · Bus", "Attendance", "Fees").
- Rules: [Spec] Respect the OS preview setting. Sensitive staff content (salary amount, approval amounts) shows generic text on the lock screen ("Salary credited · payslip ready") until the profile is unlocked. Only the app's own active profile names are used in text.

**MOB-NTF-003 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall show tap-to-act banners inside the app.
- Acceptance: Given the person is in the app When a High notification arrives in school hours Then a banner appears at the top (example "Principal · Ms. Mehra: 3 sections have not marked attendance. Remind teachers?") with action buttons "Remind" and "Later" on Android and tap-to-open on iOS.
- Rules: [Spec] Banner stays 8 seconds unless touched; "Remind" performs the action once and shows a toast; banners never cover the SOS countdown, PIN screen or a payment.

**MOB-NTF-004 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall open the matching screen when a notification is tapped.
- Acceptance: Given a notification is tapped When the app opens Then the screen from the catalogue opens (Attendance, Message teacher, Pay, Live map, Approve or refuse, Mark, Timetable, Leave, Today, Job, Payslip, Results), after unlock and profile switch where needed.
- Rules: see MOB-NFR-006 for links.

**MOB-NTF-005 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall provide a notification centre.
- Acceptance: Given the bell or Inbox is opened When "Notifications" shows Then the title carries the unread count ("5 unread"), a gear opens settings, filter chips read "All", "Unread · 5", "Fees", "Bus", "Messages", "School", a "TODAY" group shows with "Mark all read", then earlier items. Each card has icon, title, sender or detail, time and at most one action ("Pay now", "Track bus", "Remind").
- Rules: tapping an item marks it read and decrements the count; "School" covers attendance, notices and exam items; "Unread · N" recalculates. [Spec] Read state syncs across the person's devices; the list keeps 60 days, then items are removed from the phone (the record stays for audit).

**MOB-NTF-006 · Must · MVP · flag: mod.fees · [Design]**
The system shall let "Pay now" on a fee card complete in place.
- Acceptance: Given the card "October fee due Fri 16 Oct" When "Pay now" is tapped and payment succeeds Then the card reads "Paid Rs 14,600 by UPI. Receipt sent here and on WhatsApp." with the toast "Paid Rs 14,600 · receipt sent" and the unread count falls.
- Rules: the payment steps are those of MOB-PARF-002. "Track bus" opens the live bus map.

**MOB-NTF-007 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall have a notification settings screen with "WHAT YOU GET" toggles.
- Acceptance: Given Notifications settings When opened Then section "WHAT YOU GET" lists for parents "Fees and receipts" (Reminders and payment receipts), "Attendance" (When your child reaches school or is absent), "Bus and pickups" (Live bus alerts and early pickup requests), "Teacher messages" (Notes and homework from teachers), "Exams and results" (Date sheets, admit cards and results), "School notices" (Holidays, meetings and circulars); each is a toggle.
- Rules: [Spec] Staff see role topics (for example for teachers "Attendance not marked", "Cover", "Leave and duty decisions", "Messages"; for principal and owner "Decisions waiting", "Safety incidents", "Attendance down"; for finance "Approvals", "Bank and Tally"); students from Class 6 see only "Homework and notes" and "Results" and cannot receive anything promotional. The topic list per role is in the Annex permission matrix.

**MOB-NTF-008 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall give quiet hours and keep safety alerts on.
- Acceptance: Given Notifications settings When quiet hours are on Then the row "Quiet hours" reads "9 pm to 7 am · only safety alerts and overdue fees get through" (the app-flow board shows 6 am; the rule is 7 am), and "Safety alerts always on" (Bus breakdown, early closure, emergencies) is shown on and locked; tapping a locked toggle shows "Safety alerts can't be turned off".
- Rules: [Spec] Parents can change the start and end time; staff default is the same. The Urgent tier (early pickup by someone new, gate incidents, SOS) passes quiet hours and cannot be disabled. The design's "overdue fees" exception is kept for parents only.

**MOB-NTF-009 · Must · MVP · flag: ch.mobile_push · [Design]**
The system shall show how alerts reach the person and what happens when push is off.
- Acceptance: Given Notifications settings When opened Then section "HOW IT REACHES YOU" shows "App notification" (Always on), "WhatsApp copy" (Fees and attendance in English or Hindi, on), "SMS if the app is offline" (Only for bus and safety alerts, off); a locked "SMS for gate safety" (Always on) appears for parents.
- Rules: [Spec] If the system permission is denied the screen shows at the top "Notifications are off for Dhruva One. Turn them on in Settings." with a button that opens the system settings page. In that state fee and early-pickup alerts go to WhatsApp immediately instead of after 30 minutes.

**MOB-NTF-010 · Must · MVP · flag: ch.whatsapp · [Design]**
The system shall fall back to WhatsApp for fee and pickup alerts that are not opened within 30 minutes.
- Acceptance: Given a fee or early pickup push is sent When 30 minutes pass without the push being opened or the card being read in the app Then the same alert is sent on WhatsApp once, in the person's language.
- Rules: SMS is used for gate safety only. No marketing messages are ever sent through the app.

**MOB-NTF-011 · Must · MVP · flag: core · [Design]**
The system shall never send promotional notifications and shall let the school control who can send notices.
- Acceptance: Given any push When classified Then it has a transactional category from the catalogue; a category "promotion" does not exist. Students from Class 6 receive only homework and results.

**MOB-NTF-012 · Should · MVP · flag: ch.mobile_push · [Spec]**
The system shall keep a per-device badge that equals the unread count of the active profile.
- Acceptance: Given a profile is active When the unread count changes Then the app icon badge shows that count; at sign-out or on lock of a staff profile the badge is cleared.

### 7.3.7 Dhruva orb and Ask Dhruva sheet (MOB-DHR)

**MOB-DHR-001 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall show the Dhruva orb on every screen of every profile and open the chat sheet from it.
- Acceptance: Given any screen after sign-in When rendered Then the orb sits at the bottom right, above the tab bar, and a tap opens the Ask Dhruva sheet; on Android the control is the extended button "Ask Dhruva".
- Rules: the orb is the one colourful thing on every screen. [Spec] It is hidden on sign-in, PIN and lock screens, the SOS countdown, the timed past paper and any payment confirmation. With ai.assistant_chat off, it is hidden and nothing else changes.

**MOB-DHR-002 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall show the Ask Dhruva sheet with suggestions first, then free text.
- Acceptance: Given the sheet opens When idle Then the header reads "Dhruva · Your school's AI assistant · online" (Android top bar: "online · replies in Hindi or English"), a greeting for the profile ("Hello Mr. Reddy. Ask me about Navya or Arjun: marks, fees, notices or the week ahead."), suggestion chips (for example "Homework due", "Bus status", "Fee receipt") and an "Ask anything..." input.
- Rules: while working the status reads "Checking your records..."; every answer ends with a source line (for example "Fee invoices", "Marks and attendance", "School calendar and notices"). The suggestions are role-specific (examples per role in the Annex).

**MOB-DHR-003 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall return answer cards with real actions, not only text.
- Acceptance: Given a question such as "When is the parent-teacher meeting?" When answered Then the reply is "Saturday 17 Oct, 9 am to 12 pm. Ms. Kavya Reddy has a free slot at 10:20 am." with buttons "Book 10:20 am" and "Other times"; "Why is October's fee Rs 14,600?" returns a break-up card (Tuition, Transport, Late fee, Total) with "Pay now" and "Download invoice".
- Rules: an action that changes a record or reaches a family opens the normal confirmation of that function; Dhruva never completes it silently.

**MOB-DHR-004 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall give a role-safe fallback for questions outside the records.
- Acceptance: Given a question Dhruva cannot answer When asked by a parent Then the reply is "I answer questions about your children's school day, marks, fees and notices, from the school's records."; for a student "I help you plan revision and give hints. I won't do your homework for you, but I'll help you get there."; for a bus attendant "I can help with your stops, children and who can pick them up. Speak or type in Hindi or English."

**MOB-DHR-005 · Should · MVP · flag: ai.voice_input · [Design]**
The system shall accept spoken questions in Hindi or English.
- Acceptance: Given the mic is tapped for the first time When the system prompt is accepted Then the orb shows its Listening state (tall eyes, violet pulse) and the question appears as text before it is sent; the person can edit it.
- Rules: see MOB-DEV-003 for the microphone flow. Without ai.voice_input the mic is hidden and typing works.

**MOB-DHR-006 · Must · MVP · flag: ai.assistant_chat · [Design]**
The system shall show Dhruva's six states on the orb.
- Acceptance: Given the orb When in each state Then Idle breathes slowly and blinks every 4 seconds; Listening has tall eyes and a violet pulse; Thinking spins the ring and glances up and right; Done shows smiling eyes for 2 seconds after a task; Needs you shows an amber ring and pulse for urgent items only (overdue fees, safety); Quiet hours dims the ring with closed eyes and no sound or buzz.
- Rules: with "Reduce motion" every state is a still pose and the ring does not spin.

**MOB-DHR-007 · Must · MVP · flag: ai.assistant_chat · [Spec]**
The system shall say plainly when Dhruva cannot answer because the phone is offline.
- Acceptance: Given no network When the sheet opens Then it shows "You are offline. Dhruva answers from live school records, so it needs the internet." and the input is disabled; earlier answers in the thread remain readable.

### 7.3.8 Me tab (MOB-ME)

**MOB-ME-001 · Must · MVP · flag: core · [Design]**
The system shall provide a Me screen with the rows of the design.
- Acceptance: Given Me opens When rendered Then the profile card reads "Ms. Neha Arora, +91 98••• ••898 · 4 profiles"; rows are "Switch profile" (Teacher at DPS Gurugram · now), "Language" (English), "Notifications" (Quiet hours 9 pm to 6 am as drawn; the live value is the person's own hours), "Security" (Face ID and PIN; Fingerprint and PIN on Android), "Help and support" (Chat with Dhruva or call the school office), "About Dhruva" (How your data is used); a red "Sign out of this phone"; footer "Dhruva One 2.4 · Privacy · Terms" with the real version.
- Rules: [Spec] "Help and support" opens Ask Dhruva with the help topic and a "Call the school office" button that dials the tenant's office number.

**MOB-ME-002 · Must · MVP · flag: mod.hr_leave · [Design]**
The system shall give every staff role a staff "Me" with leave, payslips and notices, by reference to the desktop.
- Acceptance: Given a staff profile When Me opens Then it shows leave balances (for example Casual 6 of 12, Earned 19 of 30, Sick 9 of 10), "Apply for leave" and "Out on duty" with Type, From, To, Reason and "In charge while you are away", payslips with "Download PDF" and "Email to me", and notices from the owner, principal, HoD and HR with unread dots and "Confirm" where needed.
- Rules: same as the staff Me page in DSK (each role module). Phone specifics: payslip detail opens behind the PIN (MOB-SEC-002); PDF is saved to the app's share sheet, not to the gallery. Routing notes are role-specific and shown on the form (for example "Goes to Dr. Anjali Desai, HoD. Mrs. Rekha Sinha arranges cover for your classes.").

**MOB-ME-003 · Must · MVP · flag: ai.translation · [Design]**
The system shall let the person change language in Me > Language.
- Acceptance: Given Language is tapped When "English" or "हिन्दी" is chosen Then the app interface, Dhruva's replies and notification text switch within one second without sign-out; numbers and dates keep their format in both languages.
- Rules: see MOB-NFR-009.

**MOB-ME-004 · Should · MVP · flag: core · [Design]**
The system shall provide "About Dhruva · How your data is used".
- Acceptance: Given the row is tapped Then a page states what Dhruva reads, that it shows sources, that it never changes a record or messages a family without a person's approval, and links to Privacy and Terms.

### 7.3.9 Parent app (MOB-PAR)

The parent app is phone only. The bottom bar has four tabs: Home, Progress, Fees, Messages. Leave, PTM, Notices, Bus, Calendar, Junior pod and message threads are pushed screens with a "Home" back link. The child chip (for example "Navya ›") is on every screen. The notification centre and settings open from the bell in the top bar (Q8).

#### Home

**MOB-PARH-001 · Must · MVP · flag: core · [Design]**
The parent can open a Home that shows one child at a time with today's status and three headline numbers.
- Acceptance: Given the parent opens Home When it loads Then it shows "Good morning, Mr. Reddy", the date, a child card (photo, name, "Class 10-C · Roll 20", a chip such as "Present today" with "Marked 8:04 am by Ms. Neha Arora", a bus line "Bus 7 reached school at 7:40 am ›"), three tiles ("94% attendance", "84% unit test 3", "2 homework due"), the focus card, four tiles, a "Coming up" strip and the orb.
- Rules: the bus line shows only for a child who uses transport; for a parent-collected child it reads "You drop and pick up · gate pass 2-B-11" and is not tappable. Tiles jump to Progress > Attendance or Marks. Class 2 shows descriptive grades, not marks.

**MOB-PARH-002 · Must · MVP · flag: ai.focus_card · [Design]**
The parent can work through "N things need you today" one at a time.
- Acceptance: Given there are open items When Home loads Then the heading reads "4 things need you today" with dots, buttons by type ("Confirm" for a child's leave request, "Pay", "Book", "Read"), "Later ›" to skip to the next, "Not now" on the leave item in the See-all view, and "See all 4" which switches to a list (the link becomes "One at a time"). When all are done the heading reads "Nothing needs you today".
- Rules: the list is built from live conditions: leave waiting for the parent, any unpaid fee, no PTM slot booked for the child, consent pending, a notice asking "I have read this". Tapping "Confirm" shows "Confirmed · sent to Ms. Neha Arora" and the item leaves. Without ai.focus_card the same list is shown in a fixed order without Dhruva's ranking.

**MOB-PARH-003 · Must · MVP · flag: mod.calendar_ptm · [Design]**
The parent can reach Leave, PTM slot, Notices and a fourth tile from Home.
- Acceptance: Given the four tiles When shown Then they are "Leave", "PTM slot", "Notices" (red count = items awaiting a response) and one of "Report card" (age 11 and over), "Junior pod" (no student login) or "Student app" (young child with a login, toast "Navya uses her own Dhruva student app · you see the same homework and marks here").
- Rules: "Coming up" opens the calendar (MOB-PARC-001).

#### Kids switching

**MOB-PARK-001 · Must · MVP · flag: mod.profile_switching · [Design]**
The parent can switch between children of the same school from the child chip on any screen.
- Acceptance: Given the chip or the small avatar is tapped When the sheet "Your children at DPS Gurugram Sec 45" opens Then it lists each child with class and class teacher ("Navya Reddy · Class 10-C · Ms. Neha Arora", "Showing" on the current one); tapping one closes the sheet, shows "Now showing Arjun" and re-scopes every number, task and tile.
- Rules: fees can show both children together (MOB-PARF-003). The Messages office thread is shared across children.

**MOB-PARK-002 · Should · MVP · flag: mod.student_learning · [Design]**
The parent can switch a child's "Dhruva student app" on or off.
- Acceptance: Given the toggle "Dhruva student app" When switched on Then a student login is created and the toast "Student login created for Arjun · details sent to you" appears; when switched off, "Arjun's student login is switched off · the Junior pod is in your app"; a child without login shows "No student login · uses the Junior pod in your app".
- Rules: [Spec] The toggle is offered only for Class 1 and above and only when the school has enabled student logins; student sign-in credential is Q9.

**MOB-PARK-003 · Should · MVP · flag: mod.profile_switching · [Design]**
The parent can see other profiles on the same number from the kids sheet.
- Acceptance: Given the sheet When it shows "OTHER PROFILES ON THIS NUMBER" Then it lists DPS Noida Sec 132 (Parent · Ishaan 4-A, "1 new"), Saraswati Vidya Niketan, Karnal (Parent · Diya 3-A, "3 new") and a staff profile ("Teacher · Maths · PIN or Face ID, 1 new") and the footnote "Children at this school show together. A child at another campus or school, and your teacher profile, are separate profiles on the same login."

**MOB-PARK-004 · Should · MVP · flag: core · [Design]**
The parent can ask to add a child.
- Acceptance: Given "Add child" is tapped When the form opens Then it asks "Enter your child's admission number" and states "the school office verifies it"; on send the request shows as "Waiting for the school office".
- Rules: the child appears only after the school office links it.

#### Progress

**MOB-PARP-001 · Must · MVP · flag: mod.marks_results · [Design]**
The parent can view Progress as Attendance, Marks or Report card with a one-line Dhruva insight.
- Acceptance: Given Progress opens When shown Then a three-way switch "Attendance | Marks | Report card" appears under the child chip with an insight such as "Doing well overall. Watch Social science: 29/40, below the class average of 31. 2 homework due this week."; for a child on track "Arjun is on track. Nothing needs you in Progress today. 1 homework due this week."
- Rules: Marks is the default. Marks and the child's student app show the same numbers. Without ai.focus_card or ai.assistant_chat the insight line is hidden.

**MOB-PARP-002 · Must · MVP · flag: mod.marks_results · [Design]**
The parent can read marks, change since the last test and homework for the week.
- Acceptance: Given Marks When shown Then "Unit test 3 · out of 40" shows a bar per subject with change ("Maths 31/40 ▲ 4 since last test", "Social science 29/40 ▼ 2") and "Homework · this week" lists subject, title, teacher comment and a chip ("Returned · 8/10", "Handed in", "Due Sat 10 Oct · Not started yet"). For Class 2 the heading is "Term 1 so far · descriptive grades (Class 2)" with a grade and a comment per area.

**MOB-PARP-003 · Must · MVP · flag: mod.attendance · [Design]**
The parent can read attendance and apply for leave from it.
- Acceptance: Given Attendance When shown Then it has the big percentage ("94%", "64 of 68 school days"), a month calendar with present, holiday, weekend and future shading, an "Absent:" list with reasons and a button "Apply for leave" that opens the leave form.

**MOB-PARP-004 · Must · MVP · flag: mod.report_cards · [Design]**
The parent can read and download the report card.
- Acceptance: Given Report card When shown Then the headline ("Promoted to Class 10 · 87.4% overall"), the summary lines ("Strongest: Information technology (94)", "Needs practice: Maths (81)", "Improved in 6 of 6 subjects since Term 1"), the formal card (school, student, class and roll, session, subject table, co-scholastic grades, attendance days, class-teacher remark) and "Download report card (PDF)" with the toast "Report card PDF downloaded · signed by the principal" appear; a footer states the publish date of the next card.
- Rules: [Spec] The PDF opens in the system viewer and share sheet; it is not saved to the photo gallery. The last published card is shown until the new one is published. The sample shows last session's card while Term 1 of 2026-27 is unpublished (Q10 notes the date mismatch in the sample).

#### Fees and payments

**MOB-PARF-001 · Must · MVP · flag: mod.fees · [Design]**
The parent can see what is due, tick what to pay and see a countdown.
- Acceptance: Given Fees opens When shown Then the headline reads "₹80,200 due for Navya · tick what you want to pay", a card "Due in 6 days · ₹80,200 for Navya · by Thu 15 Oct" (turns red at 3 days or fewer), tickable line items with notes ("Tuition · Oct–Dec ₹71,200", "Transport · Bus 7, Sector 46 · Oct–Dec ₹8,400 · You opted for school transport", "Science practical file and lab ₹600 · Asked by the school on 5 Oct"), method pills "UPI | Card | Net banking" and a pay button whose label follows the ticked total ("Pay ₹80,200"), greyed when nothing is ticked.
- Rules: partial payment is possible by unticking lines. A sibling discount shows as a note ("Sibling discount 10% applied (− ₹3,680)"). Consent-linked fees appear only after consent (MOB-PARN-002).

**MOB-PARF-002 · Must · MVP · flag: mod.fees · [Spec]**
The system shall take the payment through the school's gateway and confirm it on the server.
- Acceptance: Given "Pay" is tapped When the method is UPI Then the app opens the person's UPI app through an intent (Android) or UPI app link (iOS); for Card and Net banking it opens the gateway's hosted page in an in-app secure browser (Custom Tabs on Android, SFSafariViewController on iOS). When the person returns Then the screen shows "Confirming your payment..." until the server confirms (up to 90 seconds), then the success state below or "We could not confirm this payment yet. If money was taken it will be matched within 30 minutes. Check Payment history." with no second charge.
- Rules: card numbers never touch the app. A payment request carries an idempotency key; a double tap makes one payment. Pay is disabled offline with "Connect to the internet to pay". The designs show the three methods as selectors only (no gateway screens drawn).

**MOB-PARF-003 · Must · MVP · flag: mod.fees · [Design]**
The parent can pay for siblings together.
- Acceptance: Given the sibling line "Arjun also has ₹37,650 due · pay together" When tapped Then the list shows both children with each line tagged by name ("Showing both children") and the button reads "Pay ₹1,17,850".

**MOB-PARF-004 · Must · MVP · flag: mod.fees · [Design]**
The parent shall see a clear state and a receipt after payment.
- Acceptance: Given payment succeeds Then the toast "Paid ₹1,17,850 · receipt in the app and on WhatsApp" appears, paid lines disappear, the screen shows "✓ Nothing due right now" (or "All paid for Navya"), and a history row is added with a receipt number (series RV-xxxxx).
- Rules: the receipt arrives in the app, as PDF and on WhatsApp.

**MOB-PARF-005 · Must · MVP · flag: mod.fees · [Design]**
The parent can open any past payment as a receipt.
- Acceptance: Given "Payment history · tap for receipt" with "Paid this session" total When a row is tapped Then the receipt sheet shows school and campus, "PAID", amount, item, receipt number, date, "Paid by" ("UPI · GPay"), student with class and admission number, "Sample receipt · computer-generated, no signature needed" (live copy: "Computer-generated, no signature needed"), "Download PDF" (toast "Receipt RV-08812 saved as PDF") and "Send on WhatsApp" (toast "Receipt sent to you on WhatsApp").

**MOB-PARF-006 · Should · MVP · flag: mod.fees · [Design]**
The parent can ask for a reminder before the due date.
- Acceptance: Given the toggle "Remind me 2 days before" When switched on Then it reads "Reminder on · 2 days before" with the toast "Done · we will remind you on WhatsApp 2 days before"; off shows "Reminder removed".

#### Messages

**MOB-PARM-001 · Must · MVP · flag: mod.parent_messaging · [Design]**
The parent can see conversations for the selected child and start a new one by topic.
- Acceptance: Given Messages opens When shown Then conversations (teacher, coordinator, school office) list with last message and time and the note "Teachers reply on school days between 8 am and 5 pm."; "+ New message" opens "What is it about? Dhruva sends it to the right person for Navya" with four topics: "A question about marks or homework" (goes to the class teacher), "Attendance or a sick day" (class teacher), "Study pace or extra help" (academic coordinator), "Fees, bus or certificates" (school office); "Or choose a teacher by name" lists class teacher, subject teachers, coordinator and "School office · Fees, transport and certificates".
- Rules: threads are per child except school-office and notices-type threads, which are shared. Routing by topic is Dhruva's (flag ai.reply_drafts is for teacher drafts; routing itself uses the fixed table in Section 6).

**MOB-PARM-002 · Must · MVP · flag: mod.parent_messaging · [Design]**
The parent can read and send in a thread with a stated reply time.
- Acceptance: Given a thread When open Then its header shows name, role and "about Navya", the line "Usually replies within 3 hours on school days · not after 7 pm or on Sundays" (coordinator and principal: "Usually replies within a school day"), message bubbles, a text box and "Send"; a new thread opens with "Hello, how can I help you with Navya?".
- Rules: messages carry the child's name. [Spec] Sends made offline are queued and show "Waiting to send" with a clock icon until delivered (MOB-OFF-006). Attachments are not designed; not in MVP. The 3.5-second auto-reply of the prototype is not a product behaviour.

#### Leave request

**MOB-PARL-001 · Must · MVP · flag: mod.attendance · [Design]**
The parent can send a leave request for a child.
- Acceptance: Given the Leave form When opened Then it has child chip, From and To, reason pills ("Unwell", "Family function", "Doctor's appointment", "Travel", "Other"), optional details, the routing note "Goes to Ms. Neha Arora, class teacher. Bus 7 is told not to wait. Homework for those days stays in the app.", a button that steps "Pick the dates" to "Pick a reason" to "Send for Navya · Wed 21 Oct – Thu 22 Oct", and a list of past requests. Send shows "Sent to Ms. Neha Arora", the row "With class teacher" (amber), then "Approved" (green) with the toast "Leave approved by Ms. Neha Arora".
- Rules: To defaults to From. An end before the start shows "The end date is before the start date". The day counter excludes Sundays ("2 school days"). The bus attendant is told not to wait for a child on the bus for those days. A request raised in the student app arrives as the Home task "Navya asked for leave" with "Confirm" before the teacher sees it.

#### PTM slot

**MOB-PART-001 · Must · MVP · flag: mod.calendar_ptm · [Design]**
The parent can book a PTM slot with the class teacher.
- Acceptance: Given "PTM · Sat 31 Oct" When opened Then the class teacher shows ("Ms. Neha Arora · class teacher"), twelve 10-minute slots 9:00 to 10:50 with taken slots crossed out, mode pills "In person | Video call" and "Subject teachers (optional)". The button reads "Pick a time", then "Block 10:30 with Ms. Neha". After blocking, the toast "Slot blocked · reminder the evening before" and the card "✓ Your slot is blocked · Sat 31 Oct · 10:30 · Ms. Neha Arora · Room 204" (or "video call (link in the app)") with "Add to calendar" and "Release slot".
- Rules: one class-teacher slot per child; taken slots cannot be picked; each subject teacher has a "Book 10:40" follow-on slot ("Also booked: Ms. Kavya Reddy at 10:40 am"); the Home task "Book a PTM slot" disappears once booked. [Spec] If a slot is taken between viewing and tapping the app shows "That slot was just taken. Please pick another." and refreshes the grid. "Add to calendar" asks for write-only calendar permission (iOS) or opens the system add-event screen (Android) and shows "Added to your phone calendar". Reminder uses a push the evening before.

#### Notices and consent

**MOB-PARN-001 · Must · MVP · flag: mod.notices · [Design]**
The parent can read notices for the selected child and the family.
- Acceptance: Given Notices When opened Then filter pills "All | School | Class and teacher" appear above a feed ("Term 1 exams: timings and rules", "Diwali break: Sat 7 – Wed 11 Nov", "Revision notes shared", "Bus routes 7 and 12: revised pickup times", "PTM on Saturday 31 Oct"); a notice that needs acknowledgement shows "I have read this" with the toast "Confirmed · the school can see you read it".
- Rules: the Home tile badge counts notices awaiting a response. Read receipts are visible to the school.

**MOB-PARN-002 · Must · MVP · flag: mod.notices · [Design]**
The parent can give or refuse consent on a notice.
- Acceptance: Given a consent notice (zoo trip, ₹450, consent by Mon 19 Oct) When "Give consent" is tapped Then the toast "Consent given · ₹450 added to Arjun's fees" appears and the fee shows on Fees; "No" shows "Noted · Mrs. Malhotra is told" and "You said no · Arjun stays in school that day".

#### Bus tracker

**MOB-PARB-001 · Must · MVP · flag: mod.bus_live · [Design]**
The parent can follow the bus for a child who uses transport.
- Acceptance: Given the bus line is tapped When the screen opens Then it reads "Bus 7 · Route Sector 47 – Sohna Road · Navya's stop: Sector 46 market" with a switch "Morning · to school | Afternoon · home", a status card, a stop-by-stop timeline with times, and contacts. Morning shows "Reached school · Morning trip done · Bus 7 reached school at 7:40 am · on time" and "Boarded · tapped by Mrs. Geeta Devi · 7:21 am". Afternoon shows "On the way home · Live", "3 stops away · arriving about 2:22 pm" and "Navya gets off here · only to you or her mother"; at the last stop "Navya is home · Handed to you at Sector 46 market · 2:22 pm" with "Handed to Mr. Srinivas Reddy · code checked".
- Rules: updates come from the attendant's tap at each stop (no GPS), so the screen says "Updated at <time>" and never shows a moving dot between stops. [Spec] The screen refreshes on push and every 30 seconds while open. The sample link "Preview: move the bus on ›" is a design aid and is not shipped.

**MOB-PARB-002 · Should · MVP · flag: mod.bus_live · [Design]**
The parent can ask to be alerted one stop before drop.
- Acceptance: Given "Alert me 1 stop before" When tapped Then the toast "We'll notify you when Bus 7 leaves Sector 46 market" appears and the button reads "You'll be alerted 1 stop before"; tapping again shows "Alert off".

**MOB-PARB-003 · Must · MVP · flag: mod.bus_live · [Design]**
The parent can call the attendant and the transport desk from the bus screen.
- Acceptance: Given contacts show "Mrs. Geeta Devi · bus attendant, Driver: Mr. Suresh Yadav · HR 26 CK 4471" and "School transport desk · 7 am – 4 pm on school days" When "Call" is tapped Then the phone dialer opens with the number; no number is shown on screen before the tap.

**MOB-PARB-004 · Must · MVP · flag: mod.security_gate · [Design]**
The parent shall be able to approve or refuse an early pickup by someone new.
- Acceptance: Given the Urgent notification "Kiara 3-B: pickup by uncle. Is this OK?" When tapped Then a screen shows the person, the time and two buttons "Approve" and "Refuse"; the result is sent to security and the class teacher at once.
- Rules: [Spec] Approve requires biometric or PIN if enabled. The request is Urgent and repeats once after 5 minutes. If not answered the gate keeps the child and calls the parent (decision belongs to DSK-SEC). A person unlisted on the authorised list is never approved by the attendant (see MOB-BUS-008).

#### Calendar and Junior pod

**MOB-PARC-001 · Should · MVP · flag: mod.calendar_ptm · [Design]**
The parent can read the school calendar for the selected child.
- Acceptance: Given "Calendar ›" is tapped Then "School calendar · Navya and Arjun · session 2026–27" shows a "Month | Whole year" switch, filter pills "All | Exams | Holidays | PTMs | Events", a month grid with coloured dots, a list for the month, and for a tapped date that day's events; the year view lists 12 months with counts ("Session 2026–27 · 39 dates · tap a month") and a "Coming up" list. Entries are per child where relevant.

**MOB-PARJ-001 · Should · MVP · flag: mod.student_learning · [Design]**
The parent can open a parent-led Junior pod for a child without a student login.
- Acceptance: Given the tile "Junior pod" When opened Then "Hi Arjun! Let's read and play with Papa today" shows a star count, tiles "Story time", "Number pop", "Word builder", and the parent card "12 of 20 minutes today · together mode" and "No chat, no ads, nothing to buy. Activities follow Arjun's class."; finishing a story shows "Story finished · +3 stars for Arjun".
- Rules: 20-minute daily time budget; "Read it to me" reads in English or Hindi; no chat and no purchases.

#### Parent report card, offline and push summary

**MOB-PARO-001 · Should · MVP · flag: ch.mobile_offline · [Spec]**
The parent app shall stay readable offline for what was last loaded.
- Acceptance: Given the network drops When the parent opens a screen visited in the last 24 hours Then data shows with a strip "Last updated 7:52 am · Offline"; Pay, Send, Book and Confirm are disabled with "Connect to the internet to <do this>" except messages and leave requests, which queue (MOB-OFF-006).
- Rules: general read-only offline cache for the parent is a P2 feature on the roadmap ("offline mode and multi-child parents"); the MVP guarantees only the last-loaded Home, Fees due list, receipts already opened and the bus screen's last state.

### 7.3.10 Bus attendant app (MOB-BUS)

The attendant app is phone only. Header on every screen: "BUS ATTENDANT", language toggle "हिंदी" (becomes "English"), tabs "Morning" and "Afternoon", the bus and trip title and the status "● Online · saves on the phone if the network drops". Bottom tabs: "Trip", "Children", "SOS", "Me". All text, stop names and relation labels have a Hindi version. An attendant sees only her own bus and children.

**MOB-BUS-001 · Must · MVP · flag: mod.transport · [Design]**
The attendant can switch the whole app between English and Hindi at any time.
- Acceptance: Given the toggle "हिंदी" is tapped When switched Then every label, stop name, button, toast and relation label changes to Hindi (for example "अगला स्टॉप", "बच्चा आ गया") and the toggle reads "English"; the choice is remembered.
- Rules: the first-run language screen defaults an attendant to Hindi when the device language is Hindi ("Hindi first"). Parent-facing messages sent on the attendant's taps use the parent's language, not the attendant's.

**MOB-BUS-002 · Must · MVP · flag: mod.transport · [Spec]**
The attendant shall start the trip with one tap, with a clear state.
- Acceptance: Given the morning pickup is due When the attendant opens Trip Then a large "Start trip" button shows the bus, route, number of children and first stop; tapping it records the start time and tells the transport in-charge; if the attendant has not tapped by 10 minutes after the due time the in-charge's Today shows "Bus 21 hasn't started".
- Rules: the Start step is implied by the transport desk screens ("hasn't tapped Start") but is not drawn on the attendant board (Q11). A spare or cover attendant sees the bus after the in-charge assigns cover.

**MOB-BUS-003 · Must · MVP · flag: mod.transport · [Design]**
The attendant can see the trip status and the next stop.
- Acceptance: Given the arrive state When shown Then it reads "Bus 7 · Morning pickup", "31 / 42 on the bus" with a progress bar, "Stop 9 / 12", a card "Next stop · Sector 46 market · 5 children · due 7:21" with "🔊 Read aloud" and "📍 Reached stop", the list "Coming up" (stop, number of children, time) and a button "🆘 SOS and help".
- Rules: "Read aloud" speaks "Next stop: Sector 46 market" through text-to-speech in the chosen language. Buttons are at least 56 dp high and one-handed.

**MOB-BUS-004 · Must · MVP · flag: mod.transport · [Design]**
The attendant can tap "Reached stop", which tells the parents at that stop.
- Acceptance: Given "Reached stop" is tapped When saved Then the toast "Parents told the bus is at Sector 46 market" appears, the live board for the in-charge updates and parents at the stop receive "Bus 7 is at Sector 46 market".
- Rules: one "Reached stop" per stop per trip; a second tap is ignored. The tap time is the phone's time stamped at the moment of the tap (see MOB-OFF-003).

**MOB-BUS-005 · Must · MVP · flag: mod.transport · [Design]**
The attendant can mark each child "On the bus" or "Not here" at the stop.
- Acceptance: Given "At the stop · Sector 46 market · Parents get a message the moment you tap" When shown Then one card per child (photo, name, class) has two big buttons "✓ On the bus" and "✗ Not here"; "✓ On the bus" shows "✓ On the bus · parent told" with the toast "Aarav's parents: 'On Bus 7 at 7:21'" and the count rises; "✗ Not here" shows "✗ Not here · parent called" with the toast "Calling Navya's parent · waiting 1 minute" and then two buttons "Child came" (back to on the bus) and "Leave without" (toast "Navya left at the stop · Mr. Bhatt and the parent are told"). A child who is absent (leave approved or told the school) shows "Absent today · parent told the school" with "Undo". Any marked row has "Undo".
- Rules: "Not here" opens the dialler for the parent's number only on the attendant's tap on the call action; the app does not auto-dial.

**MOB-BUS-006 · Must · MVP · flag: mod.transport · [Design]**
The attendant shall not be able to leave a stop until every child at it is marked.
- Acceptance: Given at least one child at the stop is unmarked When the attendant looks at "Leave stop →" Then it is dimmed with the hint "Tap every child before you leave"; it enables when every child has a state.
- Rules: the same rule applies to afternoon stops (MOB-BUS-008).

**MOB-BUS-007 · Must · MVP · flag: mod.transport · [Design]**
The attendant can close the morning trip with the empty-bus check.
- Acceptance: Given the last stop is done When "Reached school" is tapped Then the toast "School told: Bus 7 arrived · 31 children" appears and the step "Check the bus is empty" shows "Walk to the back. Every child must be off before the trip can close." with three tick boxes "I walked to the last seat", "I checked under every seat", "No bags or children left"; "Bus is empty · close the trip" shows "Tick all three checks first" if incomplete, and "Trip closed · bus checked empty at 7:43 am" on success with a summary "All 31 children at school · bus checked empty".
- Rules: an optional handover note to the in-charge offers pills "All fine", "Bus needs cleaning", "Seat or window damaged", "A child felt unwell", "Roads were slow"; "Tap at least one" if none; send shows "Note sent to Mr. Bhatt".

**MOB-BUS-008 · Must · MVP · flag: mod.transport · [Design]**
The attendant can hand over each child in the afternoon only to a person on the list or to a parent code.
- Acceptance: Given "Bus 7 · Afternoon drop", "8 on the bus · 33 of 41 handed over" When at a stop Then the guidance "Hand each child only to someone on their list, or check the parent's code." shows with the people on the list and relation (for example "Mrs. Neelam Singh, Mother"); tapping a name hands over (toast "Tara handed to Mrs. Neelam Singh · parents told", row "✓ Handed to ..."); "🔢 Parent's code" opens code entry and shows "Code matched · handed over"; "Walks home alone · Parent's written consent on file" appears for such a child.
- Rules: if no one is there, "No one is here" keeps the child on the bus with "Mr. Bhatt and <child>'s parent told · child stays on the bus" and the row "⚠ Stays on the bus · Mr. Bhatt and the parent are told". An unlisted person is never accepted without a code. Every handover is logged with the time and the person.

**MOB-BUS-009 · Must · MVP · flag: mod.transport · [Design]**
The attendant shall close the afternoon trip only after every child is accounted for.
- Acceptance: Given the last afternoon stop When the trip ends Then the screen reads "All handed over · back to the depot" or "<n> child still on the bus · go back to school", then the empty-bus ticks and the summary "Every child handed to a known adult · bus checked empty" or "1 child stayed on the bus and is back at school with Mr. Bhatt · bus checked empty".

**MOB-BUS-010 · Must · MVP · flag: mod.transport · [Design]**
The attendant can see the children list for the bus with live status.
- Acceptance: Given "Children" When opened Then "Bus 7 children · 31 / 42 on the bus · check each face against the photo" lists photo, name, class and a chip "To pick up" (grey), "On the bus" (teal), "Not here" (red) or "Absent" (amber), updated from stop taps; the footer notes children picked up at earlier stops that are not shown.
- Rules: each chip also carries text so colour is never the only signal.

**MOB-BUS-011 · Must · MVP · flag: core · [Design]**
The attendant can send an SOS with location.
- Acceptance: Given the "SOS" tab When opened Then it reads "Need help? Mr. Vinod Bhatt · transport in-charge" with a big red "SOS · emergency" ("Tap: your location goes to Mr. Bhatt and the principal"); tapping starts a 3-2-1 countdown ("Sending SOS in 3") with "Cancel" (toast "SOS cancelled"); after it, "🚨 Help is coming · stay with the children" and "Location sent at 2:31 pm to Mr. Bhatt, the principal and the driver's phone. Mr. Bhatt will call you within 2 minutes." with "I'm safe now · close SOS".
- Rules: [Spec] SOS is never disabled by a tenant flag. The first SOS use asks "While using the app" location permission with a reason (MOB-DEV-004); if denied, SOS is sent without location and says "Location not shared". If the app has no network, SOS is not silently queued: it shows "Not sent yet. Call Mr. Bhatt" with a large call button and prepares an SMS to the in-charge and the principal with the bus number, time and last known stop; the app also retries the data send for 5 minutes. SOS events are never merged or deleted by sync.

**MOB-BUS-012 · Must · MVP · flag: mod.transport · [Design]**
The attendant can send quick help messages to the in-charge.
- Acceptance: Given "Or tell Mr. Bhatt" When one of "Running late", "Child unwell", "Child not at stop", "Something else" is tapped Then the toast "Mr. Vinod Bhatt told · he will call you" appears and the button is ticked; "Child unwell" first asks "Which child is unwell?" with the riders and then tells "<child>'s parent, the school nurse and Mr. Bhatt"; "📞 Call Mr. Vinod Bhatt" dials.

**MOB-BUS-013 · Should · MVP · flag: ai.voice_input · [Design]**
The attendant can ask Dhruva about the trip by voice or text in Hindi or English.
- Acceptance: Given the orb When "Who is absent today?" is asked Then the answer is "Diya Sharma 1-B at Sector 46 market, mother told the school at 6:10 am"; "What time is the next stop?" gives "Sector 46 market 7:21, then Huda market 7:25, school 7:40"; "Can someone else pick up Riya?" gives "only people on her authorised list; Mr. Vinod Bansal is not on it yet".
- Rules: see MOB-DHR-004 for the fallback.

**MOB-BUS-014 · Must · MVP · flag: mod.hr_leave · [Design]**
The attendant can use Me for leave, payslip and notices.
- Acceptance: Given Me When opened Then it shows "Mrs. Geeta Devi · Bus attendant, Bus 7 · DPS Gurugram Sec 45 · Emp ID DPSG-S-0261", leave balances (Casual 9 of 12, Earned 11 of 30, Sick 10 of 10), "Apply for leave or out on duty", the history, "In charge" (spare attendants), the routing note "Goes to Mr. Vinod Bhatt. A spare attendant rides Bus 7 while you are away" (over 2 days also to the principal), payslips and "Notices · 3".

**MOB-BUS-015 · Must · MVP · flag: ch.mobile_offline · [Design]**
The attendant app shall keep working without network and show its state.
- Acceptance: Given the network drops When the attendant taps Then the status reads "● Offline · saves on the phone" (Hindi equivalent), taps are accepted and shown with a clock icon "Waiting to send", and on reconnection they sync in order and the clock becomes a tick; a counter shows "3 not sent yet".
- Rules: full rules in MOB-OFF-001 to MOB-OFF-005. Parents are told at sync time with the real tap time ("On Bus 7 at 7:21"). The stop and child lists for the trip are downloaded when the trip is opened and kept until it closes.

### 7.3.11 Student phone app, Classes 6 to 8 (MOB-STM)

Same as the desktop student module (DSK-STU, Student 6-8) for data and rules: homework, notes, ask a teacher, marks, attendance, holistic progress, leave. This section adds what is different on the phone. Tab bar: Home, Schedule, Learn, Progress; the header shows a house chip ("HOUSE Raman") and the avatar (initials) that opens the profile and leave. Marks and attendance are visible only to the student and parents.

**MOB-STM-001 · Must · MVP · flag: mod.student_learning · [Design]**
The student can open a Home that shows a level, three daily quests and a warm-up quiz.
- Acceptance: Given Home opens When shown Then the greeting "Hi Myra!" and "3 quests and a warm-up quiz today", a level card ("Level 7 · Explorer", "260 XP to Level 8 · Navigator", "12-day streak", "1,240 / 1,500 XP"), the focus card "3 THINGS NEED YOU · 1 OF 3" with "Start homework" or "Start" and "Later ›", the "Brain boost · Science" quiz, "Term 1 · your subjects" cards, and tiles "Raman · 2nd · 45 points behind Tagore" and "Badges · 2 of 6 earned". When all quests are done the card reads "All 3 quests done · streak saved! Come back tomorrow for new ones."
- Rules: quests are chosen by Dhruva only from work the teachers set (flag ai.focus_card for ranking; without it the quests are the open homework and new notes in date order). XP is awarded on first correct answers only; a retry round gives no extra points. 10 XP gives 1 house point.

**MOB-STM-002 · Should · MVP · flag: mod.student_learning · [Design]**
The student can play a five-question warm-up quiz and a subject game.
- Acceptance: Given the quiz When answered Then a right answer shows "Correct! +10 XP" and a wrong one "Not quite · see why below" with a one-line reason; the summary reads "Full marks! 5 of 5" with "+50 XP · Quiz champ +1" or "N of 5 right"; "Try again" gives "New round · practice only, no extra points". A subject card opens a sheet ("Exam Tue 13 · in 4 days · Maths · Maths whiz badge · 1 of 3 · Getting there", "PRACTISE THIS NEXT: Integers and fractions") with "Play a 5-question game" and "See a 1-page summary"; the game shows "Pop! +10 XP" or "Oops · the right one is green" and ends with "Perfect round!", "Great round!" or "Good try!"; 4 or more right moves the whiz badge.

**MOB-STM-003 · Should · MVP · flag: mod.student_learning · [Design]**
The student can see the house cup and badges as sheets.
- Acceptance: Given the tile "Raman · 2nd" is tapped Then "House cup" lists the four houses with points and "You gave Raman 45 points this week · every 10 XP you earn = 1 house point"; "Badges" lists six badges with progress and what feeds them (Homework hero 9 of 10, Quiz champ 1 of 3, Note ninja 6 of 10, Curious mind, Perfect week, Bookworm 3 of 5).
- Rules: house standing is public across houses; personal marks are not.

**MOB-STM-004 · Must · MVP · flag: mod.timetable · [Design]**
The student can see the day and week timetable and the school calendar from Schedule.
- Acceptance: Given Schedule When opened Then a switch "Timetable | School calendar" shows; the timetable has "Day | Week" with weekday pills, eight periods with subject colour dot and teacher, a "NEXT" tag on today's next class and a "Break" row; the calendar has "Month | Whole year" and filters "All | Exams | Holidays | Events | PTMs".

**MOB-STM-005 · Must · MVP · flag: mod.homework · [Design]**
The student can open homework from Learn and submit it by photo, file or typing.
- Acceptance: Given a "To do" item When opened Then the sheet shows teacher, due date, status and "How do you want to submit?" with "Photo of my notebook", "Upload a file", "Type my answer" and "Submit"; Submit without a choice shows "Pick how you want to submit"; success shows "Submitted on time · +30 XP", the chip becomes "Submitted", and the Learn badge falls. A "Returned" item shows marks and feedback.
- Rules: the camera flow is MOB-DEV-002: up to 5 photos per homework, compressed to at most 1.5 MB each; offline photo uploads queue ("Waiting to send"). The design shows "Submitted on time" with no late rule (Q12).

**MOB-STM-006 · Should · MVP · flag: mod.student_learning · [Design]**
The student can read notes and save them for offline reading.
- Acceptance: Given Learn > Notes When a note is opened Then key points show with "Shown: the first part of the sheet · open the full PDF for everything", "Save offline" (toast "Saved for offline reading") and "Practise 8 questions from this sheet"; opening clears "NEW" and counts toward the Note ninja badge.
- Rules: [Spec] Offline notes are stored encrypted in the app, removed after 30 days or at sign-out, with a limit of 50 MB.

**MOB-STM-007 · Must · MVP · flag: mod.student_learning · [Design]**
The student can ask a teacher, with a hint first.
- Acceptance: Given Learn > Ask When a subject is chosen and a question typed Then "Dhruva's hint · A nudge, not the answer" shows with "Got it now" (toast "Great! +5 XP for working it out") and "Still stuck? Ask Ms. Ritu Sharma" (toast "Sent to Ms. Ritu Sharma · you'll get a reply here"); an empty question shows "Type your question first".
- Rules: the teacher sees the question only after the student taps "Still stuck?". Teacher routing is by subject. Hint requires ai.assistant_chat; with it off, "Ask" goes straight to the teacher with the label "Ask Ms. Ritu Sharma".

**MOB-STM-008 · Must · MVP · flag: mod.marks_results · [Design]**
The student can read marks, attendance and the holistic progress card from Progress.
- Acceptance: Given Progress When opened Then Marks shows "Unit test 3 · out of 40 · 83% overall" with a bar per subject and the thin grey line for the last test; Attendance shows "97% · 66 of 68 school days this term", a month calendar and "Absent: 14 Aug (fever), 3 Sep (fever)"; Holistic shows six domains with four-step levels (Beginner, Progressing, Proficient, Advanced), activities, teacher remark and "In my own words" with "Save my reflection" (toast "Saved · your class teacher sees it on your progress card").
- Rules: footnote "Only you and your parents see your marks."

**MOB-STM-009 · Must · MVP · flag: mod.attendance · [Design]**
The student can apply for leave, which the parent confirms first.
- Acceptance: Given the avatar is tapped When "Apply for leave" is used Then the form shows From, To, reasons ("Unwell", "Family function", "Doctor's appointment", "Other"), the route note "Mrs. Ritu Kapoor confirms it in the parent app, then Ms. Pallavi Shah (class teacher) approves. Your teachers see it, and homework due those days moves."; send shows "Sent to Mrs. Ritu Kapoor to confirm", the row "Parent confirmed · with class teacher", then "Leave approved by Ms. Pallavi Shah".
- Rules: Sundays are not counted; an end before the start shows "The end date is before the start date".

**MOB-STM-010 · Must · MVP · flag: core · [Spec]**
The student app shall never expose messaging to anyone outside the school and shall send only homework and results notifications.
- Acceptance: Given a student profile When notification settings open Then only "Homework and notes" and "Results" and quiet hours exist; there is no free chat with other students and no external link that leaves the app without a parent gate.

### 7.3.12 Student phone app, Classes 9 to 12 (MOB-STS)

Same as DSK-STU (Student 9-12). Tab bar: Home, Schedule, Learn, Progress; header house chip ("HOUSE Tagore") and avatar that opens the profile and leave. No XP or levels; "study points" and a readiness score replace them.

**MOB-STS-001 · Must · MVP · flag: mod.student_learning · [Design]**
The student can open an Exam Mode Home with countdown, first-paper line, readiness ring and streak.
- Acceptance: Given Home opens in exam season When shown Then a dark card reads "3 days to Term 1", "Maths first · Mon 12 Oct, 8:30 am · Hall B, seat 14", a ring "77% ready" with "How? ⓘ", "9-day streak" and "2,150 pts"; below the focus card "3 THINGS NEED YOU · 1 OF 3" (homework first, then plan tasks with "Mark as done" and toast "Nice work · +20 study points"), "Brain boost · Maths", "Your subjects · tap one to revise" with a ring per exam, and tiles "Tagore · 1st · 45 points ahead" and "Achievements · 3 of 6 earned".
- Rules: outside exam season the card is replaced by the normal Home. Exam seat shows only after the exam cell publishes seating.

**MOB-STS-002 · Must · MVP · flag: ai.focus_card · [Design]**
The student can see how the readiness score is worked out.
- Acceptance: Given "How? ⓘ" is tapped When the sheet "How your 77% is worked out" opens Then it states "For each subject, Dhruva averages two numbers: Revised, the share of Term 1 topics you have studied and ticked off, and Practice, your average score in practice sets and class tests over the last 30 days. Your overall readiness is the average of all five subjects.", a table of Revised, Practice and Ready per subject, the tip "Fastest way up: Social science · Map work: rivers. One 30-minute revision there adds about 2% to your overall." and "Got it".
- Rules: readiness is the mean of Revised and Practice per subject, then the mean across five subjects.

**MOB-STS-003 · Should · MVP · flag: mod.student_learning · [Design]**
The student can open a subject sheet and start a short revision or practice.
- Acceptance: Given a subject card When opened Then the sheet reads "Exam Mon 12 · in 3 days · Maths · Revised 72% · Practice score 68%" with two bars, "DHRUVA SUGGESTS: Quadratic word problems" and buttons "Start a 10-minute revision" (toast "Dhruva made a 10-minute revision on Quadratic word problems · +20 points when done") and "Practise 5 questions".
- Rules: without ai.focus_card the suggestion line is hidden and the buttons open the linked teacher note and a teacher-set practice set.

**MOB-STS-004 · Could · P2 · flag: mod.student_learning · [Design]**
The student can take a timed past-paper practice.
- Acceptance: Given the board screen When opened Then it shows "Timed practice · past board questions · Quadratic equations", a 15:00 countdown (red under two minutes), question buttons 1 to 6, "Question 1 of 6 · 1 mark", "Next question" and "‹ Back", "0 of 6 answered" and "Pause and leave" (toast "Practice paused · your answers are saved"); time up submits automatically; the result shows a score ring, "Finished in m:ss of 15:00", "+30 study points · Board ready +1" and a per-question review.
- Rules: the plan item "Maths · 10 past board questions (timed)" is the intended entry but the design has no linking button (Q13), so the entry is P2. The orb is hidden during the timed paper (MOB-DHR-001). The paper stays on screen if the app goes to background for under 60 seconds; answers are saved locally every answer.

**MOB-STS-005 · Must · MVP · flag: mod.homework · [Design]**
The student can submit homework by photo, file or typing and see Dhruva's pre-check.
- Acceptance: Given Learn > Homework When a "To do" item is submitted Then the toast "Submitted to Ms. Neha Arora" shows (no XP in this app) and the chip becomes "Submitted"; a returned item shows "Checked by Dhruva, returned by Ms. Neha Arora" with marks and feedback.
- Rules: same capture rules as MOB-STM-005.

**MOB-STS-006 · Must · MVP · flag: mod.marks_results · [Design]**
The student can read marks, attendance and holistic progress.
- Acceptance: Given Progress When opened Then Marks shows "Unit test 3 · out of 40 · 84% overall" (these equal the numbers the parent sees); Attendance shows "94% · 64 of 68 school days this term"; Holistic shows Co-scholastic (A or B grades), Life skills (A or B), Career ("Interested in Science with Maths (PCM). Career session with Ms. Ritika Bhalla, counsellor, on Thu 22 Oct."), activities, remark and "In my own words" ("My goal for Term 1, and how I will reach it") with "Save my reflection".

**MOB-STS-007 · Should · MVP · flag: mod.student_learning · [Design]**
The student can ask a teacher with a hint first and keep a doubts list.
- Acceptance: Given Learn > Ask When the hint is shown Then "Got it now" saves the question and shows "Saved to your doubts list" (no XP); "Still stuck? Ask Ms. Neha Arora" sends it ("Sent to Ms. Neha Arora · you'll get a reply here").

**MOB-STS-008 · Should · MVP · flag: mod.student_learning · [Design]**
The student can see house cup and achievements.
- Acceptance: Given "Tagore · 1st · 45 points ahead" is tapped Then the house cup lists four houses and "You gave Tagore 38 points this week · every 10 study points = 1 house point"; "Achievements" lists Board ready 2 of 5, Problem solver 14 of 20, Steady scholar 9 of 14, Doubt clearer, Full month, Top 10%.

**MOB-STS-009 · Must · MVP · flag: mod.attendance · [Design]**
The student can apply for leave, which the parent confirms first.
- Acceptance: As MOB-STM-009, with the route note "Mr. Srinivas Reddy confirms it in the parent app, then Ms. Neha Arora (class teacher) approves." The same request appears on the parent's Home as "Navya asked for leave · Wed 21 – Thu 22 Oct".

**MOB-STS-010 · Must · MVP · flag: mod.timetable · [Design]**
The student can see the timetable and the calendar, including class-specific entries.
- Acceptance: Given Schedule When opened Then it matches MOB-STM-004 for Class 10-C with eight periods and calendar entries such as "Career talk · choosing streams", "Pre-board 1 · Class 10 · 7–15 Dec" and "CBSE board exams begin · Class 10".

### 7.3.13 Phone apps of the other roles (MOB-STF)

Each staff role has a phone app that reads and writes the same data as its desktop module. The rule for this section: the phone app does the same function as the desktop, in a narrower layout, on fewer tabs, with the same approvals and audit. The table gives the phone summary. "Reduced on phone" means the function exists in the DSK module but is not on the phone or is simplified; the phone shows "That section is on the desktop" (HR: "Exits are on the desktop") when a link would lead there.

**Table 7-A. Phone summary by role**

| Role (DSK module) | Tabs on phone | Same as desktop | Reduced or desktop-only | Phone-only |
|---|---|---|---|---|
| Teacher (DSK-TCH) | Today, Inbox, Students, Prep, Calendar; Me from avatar | Attendance, marks (type or photo), homework check, paper, notes, lesson plan, remedial, leave, payslips | Large tables (paper step 2, plan details, roster) are easier on desktop; Timetable page is "Week ›" link | "Switch profile" sheet from the header; "Prep" tile grid with a "Recently" list |
| HoD (DSK-HOD) | Today, Reviews, Team, Progress | Leave, plan and paper review, team, results, homework | Progress shows Results and Homework only; "My classes" is a toggle on Today and says "The full teacher screens are on the desktop" | Calendar as a link from "Coming up" |
| Academic coordinator (DSK-ACD) | Today, Cover, Progress, Timetable | Cover, plan reminders, outcomes, timetable | "+ Notice to teachers" and Ask Dhruva header button are not on phone | Parent queries from the Today card |
| Exam cell (DSK-EXM) | Today, Papers, Exam days, Marks, CBSE | Papers, seating and duties, date sheets, marks checks, CBSE | "+ Notice about exams" and "Term 1 at a glance" are desktop | none |
| Counsellor (DSK-CNS) | Today, Students, Sessions, Guidance | Referrals, sessions, private notes, guidance | Header "+ Book a session" is desktop | Notes stay private and need PIN |
| Principal (DSK-PRN) | Today, Calendar, Fees, Reports, Me; bell = Approvals | Attendance by class and department, absence watch, fee defaulters, approvals, notices | Desktop has separate Attendance, Absence watch, Approvals, Notices items; setup journey is desktop | Pushed pages from Today cards |
| Group owner (DSK-OWN) | Home, Campuses, Insights, Calendar | Approvals, campus scorecard, attendance, admissions, reports, notices, calendar | Onboarding and Add a campus are desktop only | Insights tab with chips Attendance, Admissions, Reports; "+ Event" on calendar |
| Standalone admin (DSK-ADM) | Today, People, Money, Intake, School; Me from avatar | Attendance and cover, leave, fees, salary, admissions, notices, timetable and exams | "Coming up" panel not on phone | "Intake" label for admissions |
| Finance (DSK-FIN) | Home, Alerts, Reports, Bank | Approvals, bank matching, bill approval, fees, compliance, month-end steps | Voucher entry, ledger setup, month lock, Tally mapping, vendors, inventory, requisition quotes: desktop only ("That section is on the desktop") | Alerts tab with drill-down sheets |
| HR (DSK-HRP) | Today, Requests, People, Payroll; hiring from Today | Corrections and leave issues, people, payroll run steps | Exits, payroll setup, "Today's attendance", KPI tiles, employee Attendance calendar: desktop | Pager dots on the focus card |
| Security and IT (DSK-SEC) | Today, Jobs, Gate, Team; Systems from Today | Jobs, gate, systems, roster | none | Systems as a screen from "Systems: 4 of 6 working" |
| Transport in-charge (DSK-TRN) | Today, Live, Safety, Messages | Emergency banner, live board, safety checks, parent messages | Routes and students, Fleet, Transport fees, Reports, "+ Update parents": desktop | Bus detail as a bottom sheet |
| Admissions (DSK-ADS) | Today, Families, Tours, Seats | Families, tours, seats | Campaigns, Reports, board view, family tabs, "Fee paid" button: desktop | Family as a bottom sheet with call and WhatsApp |

**MOB-STF-001 · Must · MVP · flag: core · [Design]**
Each staff role can open its phone home on the one-at-a-time Dhruva-prepared list.
- Acceptance: Given a staff profile opens When Home or Today loads Then a focus card "N THINGS NEED YOU · 1 OF N" shows with the role's primary action and "Later ›", a "See all N for today · 0 done" link, tab badges that fall as items are done, and the orb.
- Rules: contents per role are in the DSK module; with ai.focus_card off the list is shown in fixed order (see Section 4).

**MOB-STF-002 · Must · MVP · flag: core · [Design]**
The staff phone shall show "That section is on the desktop" for desktop-only sections instead of a dead end.
- Acceptance: Given a staff tap leads to a desktop-only section (Table 7-A) When tapped Then a toast or sheet says "That section is on the desktop" (HR: "Exits are on the desktop") and, where useful, offers "Send me the link" which sends a web link to the person's own number by SMS.
- Rules: [Spec] "Send me the link" uses idm.web_login and asks for sign-in with the code on the web.

**MOB-STF-003 · Must · MVP · flag: mod.attendance · [Design]**
The teacher can take attendance on the phone in two taps with everyone present by default.
- Acceptance: Given "10-C · P1 · 38 students · Tap a name to mark absent; tap again to undo" When a name is tapped Then the tile turns red "Absent" and the button reads "Submit · 35 present, 3 absent"; a student with an approved leave or a parent's note is pre-marked; a repeat absence shows "Kabir Joshi is absent again (5 of the last 7 days)..." with a note that Dhruva will tell the coordinator.
- Rules: parents of absent children are told on WhatsApp after submit. On phone the register is a large-tile grid; in poor network the register submits through the offline queue (MOB-OFF-002) and shows "Saved on this phone · will send when online". Undo is available for 10 minutes after submit while online.

**MOB-STF-004 · Must · MVP · flag: ai.marks_from_photo · [Design]**
The teacher can enter marks by photographing the mark sheet or by typing.
- Acceptance: Given "Snap the mark sheet" When a photo is taken Then the list of students fills and a toast reads "Dhruva read 36 marks from the photo · 2 need a look"; rows over the maximum or blank are amber with fix chips ("13", "20", "Absent", "0"); a summary updates live ("14.6 Average of 20"); "Type the marks instead" works the same with Dhruva's checks.
- Rules: camera flow in MOB-DEV-002. Marks are never published automatically: the teacher presses the share action (to parents today or after HoD check). With ai.marks_from_photo off the photo button is hidden and typing is unchanged. Photo reading is a prototype in the designs (Q14).

**MOB-STF-005 · Must · MVP · flag: mod.fees · [Design]**
Finance and principal payment-type actions shall ask for PIN or biometric on each confirmation.
- Acceptance: Given an approval or payment in DSK-FIN or DSK-PRN (for example "Schedule transfer", bill or concession approval) When confirmed Then the PIN or biometric prompt shows regardless of the unlock state and the action is logged with the person, time and device.

**MOB-STF-006 · Must · MVP · flag: mod.approvals · [Design]**
The principal and owner can approve or decline from the phone and be told it was recorded.
- Acceptance: Given the bell (principal) or the Home card (owner) When "Approve" is tapped Then the toast "Approved · requester notified" appears, the counter drops and the decision is logged; "Decline" asks for a one-line reason (owner copy: "Decline").
- Rules: approval limits are those in Section 6 (for example concessions above ₹25,000 go to the owner); the phone shows the limit line on each card.

**MOB-STF-007 · Must · MVP · flag: mod.transport · [Design]**
The transport in-charge can handle an emergency from the phone with one tap.
- Acceptance: Given Bus 14 breaks down When the emergency card shows Then "Send spare bus and tell parents" sends the Dhruva-written English and Hindi message to the families after the in-charge checks it, and "Call bus" dials the attendant; the card then reads "Bus 14 handled · spare Bus 25 reaches the children at 7:31 am · parents told".
- Rules: the message reaches families only after the in-charge taps (Dhruva prepares, a person approves).

**MOB-STF-008 · Must · MVP · flag: mod.security_gate · [Design]**
The security in-charge shall receive Urgent notifications for gate incidents and open the job in one tap.
- Acceptance: Given "Unknown man near Gate 2" When it arrives Then it is an Urgent notification (breaks quiet hours) and a tap opens the Job with the assign suggestion.

**MOB-STF-009 · Should · MVP · flag: mod.cover · [Design]**
The teacher can accept or swap a cover assignment from the notification.
- Acceptance: Given "Cover: 8-B, period 4 / Room 12 · Ms. Rekha Yadav is absent" When the notification is shown on Android Then action buttons "Accept" and "Swap" are present; on iOS a tap opens the Timetable with the same two actions.

### 7.3.14 Offline and poor network (MOB-OFF)

**MOB-OFF-001 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall keep a durable offline queue on the phone for attendance submissions and bus taps.
- Acceptance: Given the network is lost or the API is not reachable (3 failed attempts in 10 seconds) When a teacher submits attendance or an attendant taps Then an OfflineQueueItem is saved in the encrypted local database before the screen confirms, the screen shows "Saved on this phone · will send when online", and the item survives app kill, phone restart and a 7-day gap.
- Rules: queued types at MVP: attendance register submission, attendance undo, bus trip start, stop reached, child boarding state (on the bus, not here, left at the stop, child came, absent), handover (person or code), "no one is here", empty-bus check, trip close, handover note, help messages. SOS is not queued (MOB-BUS-011). Payments, approvals, fee actions and any message that reaches a family from a staff member are never queued; they need a live connection.

**MOB-OFF-002 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall sync the queue automatically, in order, with retries.
- Acceptance: Given queued items exist When the network returns or the app is foregrounded or every 60 seconds with network Then items are sent in creation order per trip or per class-period, in batches of at most 50, each with a client_event_id; a success marks the item "synced" and shows a tick; a network failure retries with backoff 5 s, 15 s, 60 s, then every 5 minutes; a server rejection moves the item to "Needs a look".
- Rules: the sync is a single batch endpoint (Annex). The user sees a counter "3 not sent yet" on the attendant status line and on the teacher's Today card; a sync button "Send now" exists.

**MOB-OFF-003 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall record the real time of each action and send that time with the item.
- Acceptance: Given an action is taken offline When synced later Then the item carries device_time (ISO 8601 with offset) and a monotonic sequence number; the server stores received_at and device_time and uses device_time for the log, the live board and parent text ("On Bus 7 at 7:21").
- Rules: if device_time differs from server time by more than 10 minutes the server flags the clock skew, uses its own receive time minus the measured offset where the device reported it, and shows the event as "time estimated" to the in-charge.

**MOB-OFF-004 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall apply conflict rules that never lose a safety event.
- Acceptance: Given two conflicting items When synced Then these rules apply: (a) Duplicate client_event_id is accepted once and acknowledged again (idempotent). (b) Bus taps are an append-only log; the current state of a child is the latest by device_time; a later "Undo" supersedes an earlier tap; stop and trip lifecycle events are never dropped. (c) An attendance submission for a class-period that the server already holds from another device or person is not overwritten: it is stored as "Needs a look" and the teacher sees "Attendance for 10-C P1 was already marked by Ms. Tanvi Chawla. Review the difference." with "Keep theirs" or "Use mine". (d) An attendance undo that arrives after the parents were told is applied and a correction is sent. (e) A handover recorded for a child already marked handed over at that stop by another device is kept in the log and shown to the in-charge as a "double record".
- Rules: no queued item is ever deleted silently. Items that stay "Needs a look" for 24 hours are shown to the role's supervisor (attendance: coordinator; bus: transport in-charge).

**MOB-OFF-005 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall not tell parents stale facts as if they were live.
- Acceptance: Given a queued bus tap is synced more than 15 minutes after device_time When the parent notification is made Then the text carries the recorded time ("Navya was on Bus 7 at 7:21 am") and is sent as Normal tier, not "Bus 7 is at your stop"; "Reached stop" taps older than 15 minutes do not trigger "bus is here" alerts.

**MOB-OFF-006 · Should · MVP · flag: ch.mobile_offline · [Spec]**
The system shall queue parent messages and leave requests as drafts that send when online.
- Acceptance: Given a parent sends a message or a leave request offline When the item is created Then it shows "Waiting to send" and sends on reconnection within 24 hours; after 24 hours the item turns into a draft with "Not sent. Tap to send."
- Rules: parent payments, PTM bookings and consent are not queued.

**MOB-OFF-007 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall show the connectivity state and a last-updated time on read screens.
- Acceptance: Given the phone is offline When any data screen shows cached data Then a strip reads "Offline · Last updated 7:52 am"; when the API is slow (over 5 seconds) a "Slow network" strip appears with a "Try again" action; no screen shows an empty state that could be mistaken for "no data" when the cause is no network.

**MOB-OFF-008 · Should · P2 · flag: ch.mobile_offline · [Design]**
The system shall extend offline reading to every role (roadmap "offline mode and multi-child parents").
- Acceptance: Given P2 Then the last 7 days of timetable, rosters, notes the person saved, and receipts are readable offline for every role, with the rules of MOB-OFF-007.

**MOB-OFF-009 · Must · MVP · flag: ch.mobile_offline · [Spec]**
The system shall protect the offline queue and caches at sign-out and device events.
- Acceptance: Given sign-out with a non-empty queue When confirmed Then the queue is sent first if online; if offline the person is warned and can cancel. Given a revoked device Then items are discarded and the server logs "device revoked with 2 unsynced items".

### 7.3.15 Camera, photos, microphone and location (MOB-DEV)

**MOB-DEV-001 · Must · MVP · flag: core · [Spec]**
The system shall ask for each device permission only when the feature needs it, with a reason screen first.
- Acceptance: Given the person taps a feature that needs a permission for the first time When no permission has been asked Then a reason sheet explains in one sentence and offers "Continue" and "Not now"; "Continue" opens the system prompt. If "Not now" or denied, the feature shows a clear state and a manual alternative.
- Rules: permissions used: notifications, camera, photos (picker), microphone, location (while using), calendar write (PTM), contacts: none, phone dialler (intent, no permission), biometrics. Each is in Table 7-B in the Annex.

**MOB-DEV-002 · Must · MVP · flag: ai.marks_from_photo · [Spec]**
The system shall provide a camera capture flow for marks, homework, notes and registers with a denied-permission path.
- Acceptance: Given "Snap the mark sheet" (teacher), "Photo of my notebook" (student) or "notes from a photo" (teacher) is tapped When camera permission is granted Then a camera screen opens with a framing guide for a page, a flash toggle, a retake and "Use photo"; up to 5 pages for homework, 1 to 3 for marks, up to 6 for notes. If permission is denied Then the reason sheet shows "Camera is off for Dhruva One. You can turn it on in Settings or choose a photo from your gallery." with "Open Settings" and "Choose from gallery".
- Rules: the gallery uses the system photo picker (PHPicker on iOS, Android Photo Picker), which needs no full-library permission. Photos are resized to a long side of 2048 px and compressed to at most 1.5 MB, EXIF location stripped, uploaded over an encrypted channel and deleted from the phone's app storage after upload. A photo taken offline is queued as "Waiting for network · Dhruva will read it when you are online" and manual typing remains available. Marks photos are kept by the school as source evidence for the retention period in Section 4.

**MOB-DEV-003 · Should · MVP · flag: ai.voice_input · [Spec]**
The system shall ask for microphone access only when the mic is tapped.
- Acceptance: Given the mic in Ask Dhruva is tapped for the first time When the reason sheet "Dhruva listens only while you hold or tap the mic" is accepted and the system prompt allowed Then the Listening state starts; denied shows "Microphone is off. Type your question instead, or turn it on in Settings." with "Open Settings".
- Rules: audio is sent for transcription only while the mic is active, is not stored after the transcript is produced, and is limited to 60 seconds per question. Hindi and English are supported (MOB-NFR-009).

**MOB-DEV-004 · Must · MVP · flag: core · [Spec]**
The system shall ask for precise location "while using the app" for the bus attendant's SOS only.
- Acceptance: Given the attendant opens Trip the first time When the reason sheet says "Your location is shared only if you press SOS" is accepted Then the system prompt for "While using the app" appears; later SOS reads one location fix; no background location is used at MVP.
- Rules: parents, students and other staff are never asked for location. GPS tracking of buses is P2/P3 and will need its own flow.

**MOB-DEV-005 · Should · MVP · flag: mod.calendar_ptm · [Spec]**
The system shall use write-only calendar access for "Add to calendar".
- Acceptance: Given "Add to calendar" is tapped on iOS When permission is not given Then the system asks for write-only access; on Android the app opens the system "add event" screen and needs no permission.

---

## 7.4 Business rules and policies

1. One number, many profiles. A profile is a school (or campus) plus a role. Children in one school are one profile. Another campus, another school, and a staff role are separate profiles. They never mix on screen or in data.
2. Staff pages are protected by a PIN or biometric on every unlock, and payments and finance approvals ask again each time.
3. Safety alerts, early pickup requests and SMS for gate safety can never be turned off by a parent. Quiet hours hold everything else.
4. No marketing, ever. Students from Class 6 get homework and results only.
5. Dhruva prepares; a person approves. Nothing that changes a record or reaches a family is sent by the app without a person's tap. Dhruva's answers show their source.
6. The bus view is driven by attendant taps; it does not show a moving dot. A child is handed over only to a listed person or with a parent code; otherwise the child stays on the bus.
7. Marks and fees are visible to the child's parents and, for marks, the child's own student app. Class 6 and above students never see fees.
8. The app never stores a card number, a PIN in clear, or a biometric.
9. If the phone is offline, safety facts are recorded and never dropped; money and approvals are never queued.
10. Language is English or Hindi at MVP, chosen once and changed in Me > Language. Numbers and dates keep one format.
11. Quiet hours default to 9 pm to 7 am (the app-flow board shows 6 am; the notification catalogue says 7 am; the catalogue wins).
12. Only transactional notifications exist. The school sets who can send notices.

**Table 7-D. iOS versus Android**

| Topic | iOS | Android |
|---|---|---|
| Minimum version | iOS 15 | Android 8.0 (API 26) |
| Biometric | Face ID, Touch ID | Fingerprint, face (class 3 only) via BiometricPrompt |
| Notification permission | Native prompt "Don't Allow / Allow" | Android 13+ runtime prompt "Allow / Don't allow"; 8 to 12 no prompt |
| Urgent handling | Time Sensitive interruption level | Channel "Safety" with high importance and its own sound |
| Channels | Not used | Safety, Fees, Bus, School updates, Messages, Work |
| Banner actions | Tap opens the app | Buttons "Remind", "Later"; lock-screen buttons "Track", "Mute today", "Pay now", "Remind me", "Accept", "Swap", "Mark now" |
| OTP autofill | Keyboard suggestion "From Messages" | SMS Retriever; chip "from SMS" |
| UPI | UPI app links | UPI intents |
| In-app browser for card and net banking | SFSafariViewController | Chrome Custom Tabs |
| Icon | Squircle mask by system; Light, Dark, Tinted | Adaptive circle or squircle; themed monochrome |
| Controls | 51 pt toggles, tab bar | Material 3 toggles, pill nav indicator, extended "Ask Dhruva" button |
| App switcher privacy | Blur on resign-active | Blur plus FLAG_SECURE on payment, PIN and payslip |
| Calendar | Write-only access | System add-event intent |
| Back | Swipe back and back arrow | System back gesture and bar |
| Device row in Security | "This phone · iPhone 15" | "This phone · Pixel 8" |
| Lock-screen card header | App name | App name with channel ("Dhruva One · Bus") |
| Deep link scheme | Universal Links | App Links |
| Store | App Store, TestFlight for pilot | Google Play, internal testing for pilot |

---

## 7.5 Notifications and approvals raised by this section

| Event | Who gets it | Tier | Tap opens | Approval needed |
|---|---|---|---|---|
| Child marked present | Parent | Normal | Attendance | none |
| Child absent, not marked by 9 am | Parent | High | Message teacher | none |
| Fee due in 7 days, then overdue | Parent | Normal (overdue passes quiet hours) | Pay | none |
| Bus 10 minutes away or late | Parent | High | Live map | none |
| "On Bus 7 at 7:21" (attendant tap) | Parent | High | Bus screen | none |
| Early pickup by someone new | Parent | Urgent | Approve or refuse | Parent decides |
| Leave request raised by student | Parent | High | Home task "Confirm" | Parent confirms; teacher approves |
| Leave decided | Parent, student, staff | Normal | Leave | none |
| Class attendance not marked | Teacher | Normal | Mark | none |
| Cover assigned | Teacher | High | Timetable | Accept or swap |
| Decision waiting | Principal, owner, admin, finance | Normal | Today or Approvals | The approver |
| Safety incident or unknown person | Principal, security | Urgent | Job | none |
| SOS from bus attendant | Transport in-charge, principal, driver | Urgent | SOS detail with location | none |
| Salary credited | Staff | Normal (generic text on lock screen) | Payslip | none |
| Results published | Parent, student | Normal | Results | none |
| Add-me request | School office | Normal | People | School office adds or declines |
| Offline item "Needs a look" for 24 hours | Coordinator or transport in-charge | Normal | Review | Supervisor decides |
| Force-update available | Person on old version | in-app | Store | none |

---

## 7.6 Feature switches in this section

| Flag key | What it controls | Default | Notes |
|---|---|---|---|
| ch.mobile_ios | The iOS app for the tenant | On | Off blocks sign-in on iOS and shows "Your school has not turned on the app for this phone." |
| ch.mobile_android | The Android app for the tenant | On | Same as above |
| mod.profile_switching | Profile chip, switch sheet, alerts across profiles | On | Off keeps one profile per sign-in |
| idm.biometric | Face ID or fingerprint unlock | On | Off hides the toggle and offer |
| idm.app_pin | App PIN for staff pages and payments | On | Cannot be turned off for staff and finance roles in production (TFC) |
| idm.multi_profile | Choose a profile at sign-in | On | Off: the first profile opens |
| ai.assistant_chat | Orb and Ask Dhruva | On | Off hides the orb |
| ai.focus_card | One-at-a-time Dhruva list and insight lines | On | Off shows fixed lists |
| ai.voice_input | Mic in Ask Dhruva and attendant voice | Off until Hindi voice is tested | |
| ai.marks_from_photo | Marks photo capture | On for teachers | Off hides the photo button |
| ai.translation | Hindi and English choice | On | Off locks the app to the tenant's language |
| ai.reply_drafts | Dhruva's drafts for teacher replies | On | Does not affect parent topic routing |
| mod.fees | Fees tab, pay, receipts | On | |
| mod.bus_live | Parent bus tracker | On | |
| mod.transport | Attendant app and transport desk phone | On | |
| mod.parent_messaging | Parent Messages | On | |
| mod.calendar_ptm | PTM booking, calendar | On | |
| mod.student_learning | Quests, house cup, Junior pod, readiness | On | |
| mod.notices | Notices and consent | On | |
| mod.attendance | Attendance, leave | On | |
| mod.homework | Homework submit | On | |
| mod.marks_results | Marks and results | On | |
| mod.report_cards | Report card | On | |
| mod.security_gate | Early pickup approval | On | |
| mod.hr_leave | Staff Me leave | On | |
| mod.approvals | Approvals on phone | On | |
| mod.cover | Cover action on phone | On | |
| mod.timetable | Timetable on phone | On | |
| ch.whatsapp | WhatsApp OTP and fallback | On | |
| ch.mobile_push | Push notifications and notification settings | On | See Proposed flags |
| ch.mobile_offline | Offline queue for attendance and bus taps | On | Cannot be turned off for transport while mod.transport is on (safety) |
| core | Sign-in, SOS, consent, notification centre read access, audit | always on | |

---

## 7.7 Non-functional requirements (specific to the phone)

**MOB-NFR-001 · Must · MVP · flag: core · [Design]**
The system shall support iOS 15 and later and Android 8.0 and later.
- Acceptance: Given a device on those versions When the app is installed Then it runs without crash on the test matrix (Spec assumption: the latest two major OS versions plus the minimum, on at least 6 devices per platform, including a 3 GB RAM Android phone and a small-screen iPhone SE).
- Rules: the minimums come from the store listings. Targets (Spec assumptions): iOS built with the latest SDK, deployment target 15; Android compileSdk and targetSdk at the latest required by Google Play, minSdk 26. Support for an OS version ends 12 months after it falls below 5% of active devices, announced one release ahead.

**MOB-NFR-002 · Must · MVP · flag: ch.mobile_push · [Spec]**
The system shall deliver push through APNs on iOS and FCM on Android with a server-side fan-out.
- Acceptance: Given a notification event When sent Then it is queued by the Notification Service, resolved to the person's active devices and profiles, and sent to APNs or FCM; Urgent targets delivery within 10 seconds at the 95th percentile, High within 30 seconds, Normal within 2 minutes; invalid tokens (APNs 410, FCM UNREGISTERED) are deleted.
- Rules: push payloads carry an id, type, profile, deep link and a short title and body; sensitive text is not in the payload for staff topics (the app fetches it after unlock). Push to a revoked or signed-out device is never sent. Silent pushes refresh the unread count and the bus screen only.

**MOB-NFR-003 · Must · MVP · flag: ch.mobile_push · [Spec]**
The system shall register devices and push tokens safely.
- Acceptance: Given the app starts after sign-in When the push token is available Then it registers (device id, platform, OS version, app version, locale, token) for the active session; a token change is re-registered at next launch; at sign-out the token is deleted.
- Rules: one token per install; at most 5 active devices per number; the 6th sign-in asks the person to sign out one.

**MOB-NFR-004 · Must · MVP · flag: core · [Spec]**
The system shall open the right screen from notifications and WhatsApp links in under 2 seconds on a warm start.
- Acceptance: Given a notification tap or link When the app is running Then the target opens within 2 seconds; when cold it opens within 4 seconds on a mid-range Android device.

**MOB-NFR-005 · Must · MVP · flag: core · [Spec]**
The system shall resolve a link in this order: signed in, right profile, unlocked, then screen.
- Acceptance: Given a link opens and the person is signed out Then the sign-in runs and then the target opens; if the target belongs to another profile the app switches (asking for the PIN if staff); if the target is not allowed for the person it opens that profile's Home with "You do not have access to this item."

**MOB-NFR-006 · Must · MVP · flag: ch.whatsapp · [Spec]**
The system shall support HTTPS links from notifications and WhatsApp that open the app when installed and a web or store page when not.
- Acceptance: Given a WhatsApp message contains "https://app.dhruvaone.in/l/pay/<token>" When tapped on a phone with the app Then the app opens on the pay screen of the profile named in the token (Universal Links on iOS, App Links on Android); when not installed Then the page shows the "Get the app" store buttons and, for a pay link, a web payment fallback if the tenant offers it.
- Rules: links carry a signed, single-purpose token that expires (pay 48 hours, track 6 hours, receipt 30 days, other 7 days); the token holds the target and profile hint only, never personal data; opening a link does not sign anyone in. The domain is a Spec assumption.

**MOB-NFR-007 · Must · MVP · flag: core · [Spec]**
The system shall support force update and soft update by version policy.
- Acceptance: Given the app starts When the server reports min_supported above the installed version Then a blocking screen "Update Dhruva One. This version is no longer supported." shows with "Update" opening the store; if recommended is above the installed version a dismissible banner "A new version is ready" shows at most once per day and at most 3 times per version.
- Rules: the attendant app never force-updates during an open trip: the screen waits until the trip closes (or SOS is closed). The policy also lists a blocked-versions list for security fixes. Force update is not a tenant flag; it is controlled by DhruvaOne releases. A release is staged 5%, 25%, 100% over 7 days.

**MOB-NFR-008 · Must · MVP · flag: core · [Design]**
The system shall be accessible.
- Acceptance: Given VoiceOver or TalkBack is on When every screen is traversed Then every control has a spoken label and role, order follows reading order, toasts are announced, status chips are read as text ("Absent", "On the bus"), and sheets trap focus. Touch targets are at least 44 x 44 pt (iOS) and 48 x 48 dp (Android), and the attendant's main buttons at least 56 dp. Text scales to 200% without clipping of primary actions. Contrast meets WCAG 2.1 AA (4.5:1 for text). Colour is never the only signal. "Reduce motion" turns the orb and all animations to still poses and no spinning.
- Rules: the designs state the reduce-motion rule only; the rest is Spec.

**MOB-NFR-009 · Must · MVP · flag: ai.translation · [Design]**
The system shall be fully localised in English and Hindi at MVP.
- Acceptance: Given the language is Hindi When any screen, error, toast, notification or Dhruva answer shows Then it is in Hindi (Devanagari) with Indian numerals formatted as the English numerals in both languages (₹1,17,850, dates as "Fri 9 Oct"); fonts include Devanagari (Outfit and Plus Jakarta Sans are Latin; a Devanagari companion such as Noto Sans Devanagari is a Spec assumption); layout does not clip with Hindi text that is up to 30% longer.
- Rules: Punjabi, Gujarati, Marathi and Tamil are P2. Notifications are sent in the person's chosen language. Names and school names stay as entered. Right-to-left layouts are not needed at MVP.

**MOB-NFR-010 · Must · MVP · flag: core · [Spec]**
The system shall meet crash and performance budgets.
- Acceptance: Given the release metrics When measured over 28 days Then crash-free sessions are at least 99.5%, ANR rate is below 0.47% (Google threshold), cold start to usable Home is at most 2.5 seconds at the 75th percentile on a mid-range Android device (4 GB RAM) and 1.5 seconds on iPhone 12, warm start at most 1 second, tab switch at most 300 ms with cached data, API p95 at most 800 ms for read calls, scroll at 60 fps with under 5% slow frames. Download size at most 60 MB; installed size at most 150 MB before caches.
- Rules: Crash and performance reports go to the engineering team's reporting tool; personal data is not in reports. A release that breaches the crash budget on the staged roll-out is paused.

**MOB-NFR-011 · Should · MVP · flag: core · [Spec]**
The system shall be gentle on battery.
- Acceptance: Given a normal day When measured Then background work is limited to push handling and the offline-queue sync; there is no continuous location, no periodic polling in the background, foreground polling only on the bus tracker (every 30 s) and the attendant live status; the app uses under 3% battery per hour in the foreground in test.
- Rules: the animated orb uses a lightweight animation and stops when the app is in the background or "Reduce motion" is on.

**MOB-NFR-012 · Should · MVP · flag: core · [Spec]**
The system shall limit mobile data use, because many parents are on prepaid plans.
- Acceptance: Given a typical day Then the parent app uses under 5 MB; Home loads in under 150 KB; images are served as thumbnails sized to the screen; the report card PDF and receipts are fetched only on tap; no video autoplays. A "Data saver" switch in Me is a Could (P2) that stops image previews.

**MOB-NFR-013 · Must · MVP · flag: core · [Spec]**
The system shall keep phone traffic secure.
- Acceptance: Given any request Then it uses TLS 1.2 or higher; the API host is pinned (Should); the app rejects invalid certificates; tokens never appear in URLs or logs; the app blocks use on jailbroken or rooted devices only for staff profiles that hold finance or HR data, with a warning, not a block, for others (Could).

**MOB-NFR-014 · Must · MVP · flag: core · [Spec]**
The system shall use portrait layout on phones and show the phone layout centred on tablets.
- Acceptance: Given an iPad or Android tablet When the app runs Then the phone layout shows centred at a maximum width of 480 pt; iPad and kiosk views are P3.

---

## 7.8 Open questions

- Q1. The DSK module codes in 7.2 (DSK-TCH etc.) are assumed. Confirm with Section 6.
- Q2. Teacher tab bar: the Teacher board shows "Today, Inbox, Students, Prep, Calendar"; the app-flow board shows "Today, Inbox, Students, Prep, Me"; the profile board shows "Today, Classes, Marks, Dhruva"; mvp-scope says "Today, Classes, Make, Me". Which is final?
- Q3. Owner phone tab bar is inferred (Home, Campuses, Insights, Calendar). Confirm.
- Q4. Teacher and Head of Maths: one row or two in the profile picker? The picker text says "4 profiles" and draws three rows.
- Q5. What does "Ask my school to add me" send, and to whom, when the school is unknown? (Spec default in MOB-AUT-007.)
- Q6. Not drawn: biometric failure, session expiry, device change, PIN set-up and reset. Spec defaults in MOB-AUT-009, MOB-AUT-010, MOB-SEC-003.
- Q7. Where is "Switch school" for a person? Top chip (profile board) or Settings gear on the notification centre (design status). Spec supports both.
- Q8. The Final Parent board has four tabs and no Inbox; the Halo design shows Home, Learn, Dhruva, Pay, Inbox; the inbox board shows Home, Learn, Pay, Inbox. Spec: the notification centre opens from the bell; confirm the final parent tab bar and whether Dhruva is a floating orb or a centre tab.
- Q9. How does a student sign in? The design says "Student login created for Arjun · details sent to you" but does not say the credential. Spec default: a student profile on a number the parent nominates.
- Q10. Sample inconsistency: Term 1 report card is announced for Sat 31 Oct on the Progress tab but results are Fri 30 Oct in the calendar and notices.
- Q11. The attendant board has no "Start trip" screen although the in-charge screens refer to "tapped Start". Spec default in MOB-BUS-002.
- Q12. Late homework rule: the student toast always says "Submitted on time".
- Q13. The timed past-paper has no visible entry in the design.
- Q14. Photo reading is a prototype only and the marks and learning plans publish without teacher review in the designs; confirm with the client (design-status Open list). This spec requires an explicit teacher share tap.
- Q15. Language list: six languages in the picker versus two in the rules. Spec: only English and Hindi are selectable at MVP.
- Q16. Quiet hours: 9 pm to 6 am versus 9 pm to 7 am. Spec: 7 am.
- Q17. Is there a trustee phone view? The inventory lists the trustee but shows no phone board.
- Q18. SMS fallback for bus and safety alerts when the app is offline: the cost and the opt-in are not defined.
- Q19. Whether the early pickup approval needs biometric or PIN when the parent has neither set.

---

## Annex 7-A (engineering)

### Data entities

| Entity | Key fields | Notes |
|---|---|---|
| Device | device_id (uuid, generated at install), person_id, platform (ios, android), os_version, device_model, app_version, build, locale, timezone, created_at, last_seen_at, last_ip_city, status (active, revoked, signed_out), biometric_enrolled (bool), pin_set (bool) | One row per install per number. "Signed in on" list reads this. Max 5 active per number |
| PushToken | token_id, device_id, provider (apns, fcm), token (hashed index plus encrypted value), registered_at, last_ok_at, invalid_at, environment (prod, sandbox), permission_state (granted, denied, not_asked, provisional) | One active token per device. Deleted at sign-out and on provider invalid response |
| NotificationPreference | person_id, profile_id, topic_key, enabled, quiet_start, quiet_end, quiet_enabled, language, whatsapp_copy (bool), sms_offline (bool), updated_at | Per profile. Locked topics (safety, early pickup, gate SMS) are rows with locked=true and cannot be set false |
| OfflineQueueItem (phone) | local_id, client_event_id (uuid), type, payload (json), profile_id, entity_ref (class_period, trip_id), device_time, sequence_no, created_at, attempts, last_error, state (queued, sending, synced, needs_look, failed_final) | Stored in the encrypted local DB. Mirrored on the server as SyncReceipt |
| SyncReceipt | client_event_id, device_id, received_at, device_time, applied (bool), result (applied, duplicate, conflict, rejected), conflict_ref | Server-side idempotency ledger; kept 90 days |
| Notification (inbox item) | notification_id, person_id, profile_id, event_type, tier, topic, title, body, deep_link, created_at, read_at, action_state | 60 days on phone; permanent record elsewhere for audit |
| DeepLinkToken | token, purpose (pay, track, receipt, notice, other), target, profile_hint, expires_at, used_at | Signed; single-purpose |
| AppVersionPolicy | platform, min_supported, recommended, blocked_versions[], message_en, message_hi, updated_at | Read at launch |
| AddMeRequest | request_id, mobile (hashed), name, role, school_text, tenant_hint, status (new, matched, added, declined), created_at | Routed to the school office or support |
| AppSession | session_id, device_id, person_id, issued_at, last_refresh_at, expires_at, revoked_at | Refresh tokens rotate |
| TripEvent (bus) | event_id, client_event_id, trip_id, bus_id, type (start, stop_reached, child_state, handover, no_one_here, empty_check, close, note, help), child_id, stop_id, actor_id, device_time, received_at, time_estimated (bool) | Append-only |
| SosEvent | sos_id, trip_id, actor_id, triggered_at, lat, lng, accuracy_m, delivery_state, closed_at | Never queued silently; audit retained |

### APIs

| Method and path | Purpose | Authz and role scope | Key errors |
|---|---|---|---|
| POST /v1/auth/otp/send | Send a code (SMS or WhatsApp) | none (rate limited) | 429 TOO_MANY_REQUESTS; 400 INVALID_NUMBER |
| POST /v1/auth/otp/verify | Verify the code and return session and profile list | none | 400 CODE_WRONG; 410 CODE_EXPIRED; 423 LOCKED |
| POST /v1/auth/refresh | Refresh the access token | refresh token | 401 SESSION_REVOKED |
| POST /v1/auth/logout | Sign out this device | session | none |
| POST /v1/auth/logout-all | Sign out other devices | session | none |
| GET /v1/me/profiles | List profiles for the number with counts of new items | session | 401 |
| POST /v1/me/profiles/{id}/switch | Make a profile active; returns a profile-scoped token | session | 403 PROFILE_NOT_LINKED; 423 PROFILE_LOCKED |
| POST /v1/me/pin | Set or change the App PIN (hash and salt wrapped by device key) | session | 400 WEAK_PIN |
| POST /v1/me/pin/verify | Server check after 5 local failures (rate limit) | session | 429 |
| GET /v1/devices | List signed-in devices | session | none |
| POST /v1/devices | Register or update a device | session | 409 TOO_MANY_DEVICES |
| DELETE /v1/devices/{id} | Revoke a device | session | 404 |
| PUT /v1/devices/{id}/push-token | Register or replace the push token | session, same device | 400 BAD_TOKEN |
| DELETE /v1/devices/{id}/push-token | Remove the token | session | none |
| GET /v1/notifications?profile=&filter=&cursor= | Inbox list with unread count | session, profile scope | 403 |
| POST /v1/notifications/{id}/read | Mark read | session | none |
| POST /v1/notifications/read-all | Mark all read | session | none |
| GET /v1/notification-preferences | Read settings for the profile | session | none |
| PUT /v1/notification-preferences | Save settings | session | 422 LOCKED_TOPIC |
| POST /v1/push/send (internal) | Notification Service fan-out to APNs/FCM | service | 202 ACCEPTED |
| POST /v1/sync/batch | Send up to 50 queued items | session, role must match item types | 207 MULTI_STATUS with per-item result (applied, duplicate, conflict, rejected) |
| GET /v1/sync/state?since= | Pull changes since a cursor for cached screens | session | none |
| POST /v1/sos | Raise an SOS with optional location | attendant, session | 503 retry; client falls back to SMS |
| GET /v1/app/version-policy?platform=&build= | Version policy | none | none |
| GET /v1/links/resolve?t=<token> | Resolve a deep-link token | none (token is the credential) | 410 LINK_EXPIRED; 404 |
| POST /v1/uploads/photo | Upload a captured photo (multipart) | session | 413 TOO_LARGE; 415 BAD_TYPE |
| POST /v1/add-me | Create an add-me request | none (rate limited) | 429 |
| POST /v1/payments/intent | Create a payment intent for ticked lines (idempotency key) | parent | 409 ALREADY_PAID; 422 NOTHING_TICKED |
| GET /v1/payments/{id} | Poll payment status | parent | 404 |

### Events

| Event name | Emitted when | Payload highlights | Consumers |
|---|---|---|---|
| device.registered | Device first registered | device_id, platform, app_version | Audit, Notification Service |
| device.revoked | Sign-out everywhere, revoke, lost phone | device_id, reason, unsynced_items | Audit, Notification Service, IDM |
| push.token.registered / push.token.invalidated | Token set or provider returns invalid | token_id, provider | Notification Service |
| notification.sent | Push accepted by APNs/FCM | notification_id, tier, device_id | Analytics |
| notification.opened | App opens from a push | notification_id, time_to_open | Fallback timer (WhatsApp after 30 minutes), analytics |
| notification.fallback.whatsapp | 30 minutes without open for fee or pickup | notification_id, template | WhatsApp channel |
| auth.otp.verified / auth.profile.switched | Verified; profile changed | person_id, profile_id | Audit, IDM |
| auth.pin.locked | 10 wrong PIN tries | profile_id | Audit |
| sync.batch.received | Batch posted | count, device_id | Sync service |
| sync.item.applied / sync.item.conflict | Per item result | client_event_id, type, conflict_ref | Teacher and transport views, supervisors |
| attendance.submitted | Attendance applied (live or synced) | class_period, device_time, source (live, queue) | Parent alerts, coordinator, principal |
| bus.child.boarded / bus.stop.reached / bus.handover / bus.trip.closed | Attendant taps applied | trip_id, child_id, device_time, time_estimated | Parent app, transport live board, headcount check |
| bus.sos.raised | SOS applied | sos_id, location | Transport in-charge, principal, driver |
| app.version.blocked | Blocked version attempts to start | build | Release team |
| link.opened | Deep link resolved | purpose, result | Analytics |
| photo.uploaded | Photo stored | purpose (marks, homework, notes), count | AI (marks from photo), homework |

### State machines and workflows

**App launch and auth gate**

| State | Entry | Next states |
|---|---|---|
| Cold start | App process starts | VersionCheck |
| VersionCheck | Read policy (cached if no network) | ForceUpdate (below min), FirstRun (no install record), SessionCheck |
| ForceUpdate | Blocking screen | exits only by store update (deferred while a bus trip is open) |
| FirstRun | Splash, language, notifications, biometric offer | SignIn |
| SignIn | Number and code | ProfilePicker (more than one profile), Setup (one), NumberNotFound |
| NumberNotFound | Dead end | SignIn, AddMe |
| SessionCheck | Tokens present and valid | SignedOut (invalid or revoked), Locked (staff or biometric on), Setup |
| Locked | PIN or biometric prompt | Setup (success), Locked (retry with limits), SignedOut (10 failures) |
| ProfilePicker | Shown if last-profile checkbox is off or no last profile | Setup |
| Setup ("Setting up your day") | Load profile home | Home, SetupError (retry, cached home) |
| Home | Role home | ProfileSwitching, Locked (after background delay), SignedOut |
| ProfileSwitching | Hand-over screen | Locked (staff) then Home, or Home |
| SignedOut | Tokens and local data wiped | SignIn |

**Offline sync (per OfflineQueueItem)**

| From | Event | To |
|---|---|---|
| (new) | User action while offline or API unreachable | queued |
| queued | Network up, foreground, 60 s timer | sending |
| sending | 2xx applied or duplicate | synced |
| sending | network failure | queued (attempts + 1, backoff) |
| sending | server conflict | needs_look |
| sending | server rejection (permission, validation) | failed_final (supervisor told) |
| needs_look | User chooses Keep theirs or Use mine, or supervisor resolves | synced |
| queued | Sign-out confirmed with items | discarded (logged) |

**Notification delivery**: event -> tier -> preference check (topic, quiet hours; Urgent bypasses) -> push to devices -> if fee or pickup and not opened in 30 minutes (or permission denied) -> WhatsApp -> for gate safety, SMS.

**Permission prompt (each OS permission)**: not asked -> reason sheet -> system prompt -> granted or denied -> if denied, feature shows its manual alternative and "Open Settings".

### Table 7-B. OS permissions

| Permission | Used by | When asked | If denied |
|---|---|---|---|
| Notifications | All | Pre-permission screen at first run | Notification settings shows "off" notice; WhatsApp fallback applies at once |
| Camera | Marks from photo, homework photo, notes photo | First tap on a camera action | Gallery picker and typing |
| Photos | Same | Picker needs none | none |
| Microphone | Ask Dhruva voice, attendant voice | First tap on mic | Typing |
| Location (while using) | Attendant SOS only | First Trip open | SOS sends without location |
| Calendar (write-only) | PTM "Add to calendar" | On tap (iOS) | Share the event as text |
| Biometrics | Unlock | Offer at first run and first staff profile | PIN |

### Permission matrix (capability x persona)

Y = yes, N = no, R = read only, P = needs PIN or biometric each time.

| Capability | Parent | Student | Attendant | Teacher | HoD / AC / Exam / Counsellor | Principal | Owner | Finance | Others (HR, Sec, Transport, Admissions, Admin) |
|---|---|---|---|---|---|---|---|---|---|
| Sign in with number and code | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Multi-profile picker | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Staff profile PIN | N | N | N | Y | Y | Y | Y | Y | Y |
| Payment or finance approval | Y (own children, biometric if on) | N | N | N | N | P (approvals) | P | P | P (admin: fees) |
| Orb and Ask Dhruva | Y | Y (hints) | Y (voice, Hindi) | Y | Y | Y | Y | Y | Y |
| Notification centre and settings | Y | Y (homework, results) | Y | Y | Y | Y | Y | Y | Y |
| Locked safety alerts | Y | N/A | Y | N/A | N/A | Y (Urgent) | Y | N/A | Security: Y |
| Take attendance (queue allowed) | N | N | Bus taps only | Y | N | N | N | N | N |
| Camera for marks or homework | N | Y (homework) | N | Y | Exam: marks R | N | N | N | N |
| Offline queue | Messages and leave only | Homework photos | Y | Y | N | N | N | N | N |
| SOS | N | N | Y | N | N | R (receives) | N | N | Transport and security R |
| Sign out everywhere | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| View other children's data | N | N | Only own bus list | Own classes | Own scope | Campus | Group | Campus finance | Role scope |

Notification topics by role (for MOB-NTF-007): Parent: fees, attendance, bus and pickups, teacher messages, exams and results, school notices. Student: homework and notes, results. Attendant: trip changes, help replies, notices, leave decisions. Teacher: attendance not marked, cover, leave and duty decisions, messages, notices. Coordinator and HoD: reviews, cover, leave to review. Principal and owner: decisions waiting, safety incidents, attendance and fee alerts. Finance: approvals, bank and Tally issues. HR: requests, payroll steps. Security: jobs, gate. Transport: emergencies, late buses, messages, safety checks.

Suggested starter questions for Ask Dhruva by persona: Parent: "How is Navya doing before the exams?", "What do I need to pay this month?", "What is happening at school next week?". Student: "What should I revise first?", "What homework is due?". Attendant: "Who is absent today?", "What time is the next stop?", "Can someone else pick up Riya?". Principal and owner: "Why is Gurugram attendance low?", "Which campuses are behind on onboarding?". Transport: "Which buses are late most often?", "Is transport paying for itself?", "Which buses have seats free?".

### Proposed flags

| Flag | Controls | Default | Reason |
|---|---|---|---|
| ch.mobile_push | Push notifications and the notification settings screen | On | The catalogue has channel flags but no switch for push itself; a tenant that wants WhatsApp only needs one |
| ch.mobile_offline | Offline queue and Saved-on-this-phone behaviour for attendance, bus and messages | On | Allows a tenant or release to disable queueing while debugging; transport safety rules keep it on while mod.transport is on |
