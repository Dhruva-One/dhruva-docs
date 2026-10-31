# dhruva-docs

Product and technical documentation for **DhruvaOne**, a school ERP with the Dhruva AI assistant, built for Indian school groups and standalone schools. This repository is where decisions are written down. The code repositories link to it and build to it.

| | |
|---|---|
| Owner | DhruvaOne product and engineering |
| Current spec | Functional specification **v1.1** (908 requirements); all decisions in section 10.2 confirmed by the client on 31 October 2026 |
| Cloud decision | AWS: Mumbai (ap-south-1) primary, Hyderabad (ap-south-2) recovery |
| Pilot | DPS Gurugram Sec 45 from 5 January 2027; all 14 DPS campuses by 31 March 2027 |

## What is in here

| Document | What it answers | Read it when |
|---|---|---|
| [Functional specification](Functional/DhruvaOne-Functional-Spec.md) | What the product must do: every requirement with acceptance criteria, plus engineering annexes (data, APIs, events, permissions) | You build, test or sign off a feature |
| [Functional overview (PDF)](Functional/DhruvaOne_Functional_Overview.pdf) | What every screen in the designs shows, role by role (214 pages) | You need the designed labels, flows or screens |
| [Repositories and technology stack](Technology/DhruvaOne%20Repositories%20and%20Technology%20Stack.md) | Which repositories exist, the stack in each, and why | You start a new service or pick a library |
| [Technical architecture](Technology/DhruvaOne-Technical-Architecture.md) | How the system carries the load: workload model, capacity per phase, data tier, scaling, resilience | You size, scale or change infrastructure |
| [Deployment strategy](Technology/Deployment-Strategy.md) | Where and how it runs: AWS against Google Cloud, cost by phase including AI models, environments, release process and rollout | You deploy, budget or revisit the cloud choice |

## How the functional spec is organised

The master copy is one file, `Functional/DhruvaOne-Functional-Spec.md`. `Functional/spec/` holds the same text split by section for easier reading and review; when you change the combined file, update the matching split file in the same pull request. The code reads only the combined file.

| Section | Area | Code |
|---|---|---|
| 1 to 2 | Conventions, platform overview, and API and event conventions (2.5) | |
| 3 | Identity management | IDM |
| 4 | Tenant administration and feature control | TFC |
| 5 | AI: the Dhruva assistant | AI |
| 6 | App, desktop | DSK |
| 7 | App, mobile | MOB |
| 8 | WhatsApp | WAB |
| 9 | Cross-cutting platform | XCT |
| 10 | Release phasing and decisions | |
| 11 | Website | WEB |
| Appendices | A: feature flag registry · B: glossary · C: design gaps | |

Every requirement is one block with an ID, priority, phase, feature flag and source tag:

```
**IDM-OTP-001 · Must · MVP · flag: core · [Design]**
A person can start sign-in by entering the mobile number the school has on record ...
- Acceptance: Given ... When ... Then ...
```

- **Phases:**
  - **MVP:** built Oct–Dec 2026, live Jan–Mar 2027.
  - **P2:** Apr–Sep 2027.
  - **P3:** Oct 2027 – Mar 2028.
- **Source tags:**
  - `[Design]`: the behaviour is in the prototypes.
  - `[Spec]`: added by the spec, beyond the designs.
- **Engineering annexes:** every section ends with one, covering data entities, APIs, events, state machines and the permission matrix. APIs follow section 2.5: public paths under `/v1`, service calls under `/internal/v1`, and each API defined once by the section that owns it.

## How the code uses these documents

The repositories live in the [Dhruva-One](https://github.com/Dhruva-One) organisation: `dhruva-platform`, `dhruva-ai`, `dhruva-apps`, `dhruva-site`, `dhruva-whatsapp`, `dhruva-connectors` and `dhruva-infra`.

`dhruva-platform` reads the functional spec directly. Its `tools/spec-sync/sync.py` turns the spec into a catalog of requirements, APIs, events and flags. A CI test fails if a requirement has no owner or an API stops answering. To check the spec still parses after you edit it, run from a sibling checkout of `dhruva-platform`:

```bash
npm run spec:check     # reads ../dhruva-docs/Functional/DhruvaOne-Functional-Spec.md
npm run spec:sync      # regenerates the catalog after a spec change; commit the result in dhruva-platform
```

## Changing a document

1. **Branch and pull request:** work on a branch and open a pull request. One topic per pull request.
2. **Spec changes keep the format:**
   - Keep the requirement header exactly as above; the parser depends on it.
   - New requirements take the next free number in their module. Never reuse an ID.
   - A new API or event goes into the annex of the section that owns it (section 2.5).
3. **Decisions:** record a changed decision as a new numbered row in section 10.2, with the sections it touches. Raise anything still open in 10.3 or the section's open questions.
4. **Version line:** update the document's version and date at the top of the spec when the change is more than a typo.
5. **Check:** run `npm run spec:check` in `dhruva-platform` before asking for review.

Keep writing plain: short sentences, exact labels from the designs, numbers with units. Sample names and figures in the spec are sample data.

## Status and open items

**Settled:**
- All 25 decisions in spec section 10.2.
- The website is static for the MVP, with a content management system chosen in 2027.
- AWS is the cloud.

**Still open with the client:**
- Where website requests go after the Platform console: a CRM tool or the console only (spec section 11, Q1).
- Legal sign-off on the website's privacy notice, terms, data processing agreement and Trust page claims.

**Still open with engineering** (see the deployment strategy):
- Confirm AWS Mumbai prices.
- Confirm which AI models run with inference inside India.
- Run the AI model evaluation.
- Decide region-loss recovery: a disaster allowance, or an earlier warm standby.

**Repository housekeeping:**
- The `Import AI cards to project` workflow runs `import_cards.py` with `cards.json`. Neither file is in the repository, so the workflow fails until they are restored or the workflow is deleted.

## Licence

[MIT](LICENSE).
