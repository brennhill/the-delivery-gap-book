# Feature Workflow Sample — Toolkit V2 Redesign

> This is the full `/feature` conversation that produced `toolkit-v2-redesign.md`. Preserved as an example of the four-phase feature definition process.

---

## Phase 1: Intent

### Question 1: What problem does this solve?

**AI:** Not "what does the tool do" — what problem goes away when this exists?

**User:** Engineering leaders are trying to apply AI because executives are forcing them to. They do not have established best practices and are being pushed to apply this stuff and "have results." (Linked: andrewmurphy.io — "If You Thought the Speed of Writing Code Was Your Problem, You Have Bigger Problems")

I'm trying to give them a plug and play toolkit to make this happen and push back where needed.

**AI:** That's a dashboard. "Guaranteed to help" is a curated playbook with enforcement. Let me restate:

The problem: engineering leaders under pressure to adopt AI have no plug-and-play system that gives them the best odds of success — the right metrics, the right gates, the right processes — without requiring months of custom instrumentation or expensive SaaS.

**User:** Yes.

---

### Question 2: How will we know it worked?

**AI:** What existing metric moves when this tool succeeds?

**User:** I think a few things:
1. Just having an AI policy to begin with is associated with success. They should have one with enough reasoning that they can defend it.
2. They have "best practice" stuff installed/done by default. Utilities, gates, etc. It doesn't have to be perfect, but it needs to be something they can just go with if they have nothing.
3. Ideally some reporting - but the struggle with reporting is that it is very dependent on their whole ecosystem. So ideally some playbooks for common ecosystems.

**AI (pushback):** Those are outputs, not metrics. "They have an AI policy" — how do you know it's a good policy? "They have gates installed" — how do you know the gates are catching anything?

Proposed success criteria at two levels:

**Level 1 — Adoption:** AI policy exists, gates installed, review cadence started.

**Level 2 — Impact:** Machine catch rate > 0% via CI reporting. With the caveat: this is a floor check, not a full picture.

**User:** Both are success criteria independently. But rework rate and rubber stamp rate make me hesitate. After EXTENSIVE looking there's no "magic" way to measure these without tooling across their whole ecosystem. The only thing we can measure is baseline machine catch rates from CI, and even that is ecosystem specific.

Ideally we have instructions on how to hook into CI/CD. A reporting template for GitHub Actions might work. If they use GitHub Actions, here's how to see how many issues were caught in CI. It still hides issues caught locally, but it tells you if ANYTHING is getting caught.

**AI:** Honest success criteria:

Level 1 — what the tool guarantees. Level 2 — what the tool enables if they wire up reporting. The gap between Level 1 and Level 2 is where consulting lives.

**User:** Consulting or let's be honest: these are supposed to be smart and experienced people. They need guidance not a parent.

---

### Question 3: What is out of scope?

**User:** It should not try to provide plug and play for all ecosystems. That's a product line, not a tools repo for a book.

**AI (probing):** What else? Should it detect AI code? Measure individual productivity? Provide ongoing monitoring? Replace commercial tools? Work for non-GitHub repos?

**User:**
- It shouldn't try to "replace" commercial tools. But it should direct people to the best possible open source or other tools they can install, right now, for free. We should also be honest about where commercial tools are potentially better.
- It should work for non-GitHub repos, because we're not going to ship any custom tooling that requires more than git.

---

### Question 4: What must NOT happen?

**User:** I think the biggest risk is false confidence.

**AI (pushback):** I can think of more:

- **Gate theater** — they install Tier 0 gates that catch only formatting issues, report "we have automated verification." Meanwhile real defects sail through.
- **Process overhead that kills velocity without improving quality**
- **Cargo-culting the success stories**

**User:**
- Cargo cult: not a risk because we don't have that much to offer them.
- Process overhead: acceptable risk. Adults held to adult standards.
- Gate theater: real risk. Deserves VERY LOUD language in-repo and during install.
- False confidence: warnings all the way. No repo will solve fundamental competence and honesty issues.

---

### Question 5: Pre-mortem findings

**AI:** Six months from now. This tool exists, teams tried it. It failed. Why?

**User:** Possible thesis is wrong, possible that the gates aren't good enough and they just abandon AI, possible something better comes out.

**AI (pushback):**

- "Thesis is wrong" — which part?
- "Gates aren't good enough" — the tool working correctly but being perceived as evidence that AI is the problem.
- "Something better comes out" — real risk, can't design against.

Additional failure modes:
- **Time-to-first-value too high** — leader opens repo, sees 16 chapters, closes tab.
- **Doesn't match their stack**
- **Weekly review never sticks**

**User:**
- Thesis: the measurement thought could be wrong or superseded. DORA has been enhanced. Many tools are valuable on their own though.
- Gates: exactly. They give up. A lot of people hate AI and are looking for reasons.
- Upfront work: I want this to be easy. Not an implementation guide. An install script or something.
- Stack mismatch: real but open source. Can't solve for free.
- Weekly review: out of scope. Horse->water->drink problem.

---

## Phase 2: Behavioral Spec

### Level 1: Stories

**AI:** Walk me through what the leader experiences today when this problem happens.

**User:** They put something on OKRs to "ship with AI" to show they take it seriously and sort it out later. Then they tell their team to do it and give them a success story. The team runs around building stuff with AI to look good. Maybe managers try to figure out the chaos.

**AI:** So a quarter later they have "95% AI adoption" and a pipeline that's the same or worse. The VP asks "why is velocity flat?" and the leader has no answer.

Now walk me through what you want them to experience instead.

**User:** Ideally they push back that adoption itself is not a great metric. They look for "how do I get results from AI," land on the book/repo, and install my suggestions. And ideally those suggestions don't suck. And then the tooling gives them data to show not only that they are succeeding but some actionable findings.

---

### Level 2: Mechanism

**AI:** Why will this approach work? What if the leader installs everything and gates catch nothing?

**User:** I think that's impossible/improbable to the point of absurdity given the blog post I linked and everything else in the industry.

**AI:** What about the other direction — gates catch tons of issues and the team revolts?

**User:** I think both, but I can't resolve it from here. That's its own try->fail->refine loop.

---

### Level 3: States and Transitions

Four states identified:
1. **Nothing** — no policy, no gates, no AI process
2. **Installed** — policy exists, Tier 0 gates blocking in CI, context files in repo
3. **Running** — weekly review happening, gates catching things, leader has data
4. **Wired up** — CI reporting connected, ecosystem connectors for deeper metrics

---

### Level 4: Error Cases

- **Conflicting existing setup:** AI detects what exists and fills gaps, asks before changing.
- **Unknown language/stack:** Prompt the user to do a web search for the best tools, warn it's a search not curated, build config together.
- **Bad CI config:** Save all AI-generated configs for rollback. Test safely — AI asks the user how. Human helps AI be safe.
- **Multi-repo orgs:** Per-repo. Leaders can delegate.
- **AI policy template legally dangerous:** Prompt for regulatory requirements, disclaimer to have legal review.

---

## Phase 3: Design Conversation

### Codebase Findings

The toolkit today is 44 markdown files, 5 Python scripts, and 1 installable package. It's a reference library — a menu when the user needs a meal.

| What the user wants | What exists today |
|---|---|
| "Install and go" | Read 44 markdown files |
| Interactive setup | Nothing |
| AI policy to present to leadership | Blank rollout memo template |
| Gates in CI after one command | Gate recommendations, no CI configs |
| Curated "install these" | Lists of 10-20 options per tier per language |

### Approach Decision

**B+C: Opinionated quick-start guides + AI-guided setup.**

The markdown guides are the source of truth. The CLAUDE.md / AGENTS.md file instructs the AI to read these guides and apply them interactively. The AI is the install experience. No custom CLI to build.

Plus: doing C means they can say "we're using AI! see!" — the setup process itself is AI-assisted.

---

## Phase 4: Implementation Design

### Key Decisions

- **Kill `delivery-metrics/` entirely.** Unvetted measurement scripts create false confidence. Replace with `measurement-guidance/` pointing to established DORA tools.
- **Kill the measurement scripts.** rework-detector, cost-calculator, spec-coverage, defect-escape-rate, change-fail-rate. All dead. These heavily overlap with DORA — direct users to established tools.
- **Trim by-language pages.** From 13+ tools per tier to 3-4 opinionated picks with "last verified" dates.
- **Quick-starts describe what should be in place, not copy-paste configs.** V1 says what Tier 0 includes. Tested workflow files are a future improvement.
- **CLAUDE.md is the entry point.** AGENTS.md is a symlink.
- **Scorecard: kill.** Just say weekly review of basic stuff. "Better than last week" is as good as it gets — no benchmarks, we tried, the data isn't there.
- **Multi-pass review tool:** Ship V1 with Claude, package as skill or alternatives later.

### Blind Spots Caught

- **Tool recommendation rot:** "Last verified" dates, AI checks tool existence before recommending.
- **Multi-pass review requires API key:** Disclose upfront, list alternatives.
- **Existing codebase with thousands of warnings:** Guidance on baselining (only new violations block).
- **CLAUDE.md must not authorize arbitrary commands.** Generate configs, human reviews and applies.

---

> "All fair. Let me write the spec."

*Spec written to `Delivery-Gap-Toolkit/specs/toolkit-v2-redesign.md`*
