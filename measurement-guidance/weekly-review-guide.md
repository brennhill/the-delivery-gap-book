# The Weekly Review (15 Minutes)

If you do nothing else from this toolkit, do this meeting. The cadence is more important than the sophistication of the metrics.

---

## The Setup

**Who:** Engineering manager, tech lead, one rotating IC. Three people. Not more. More people means more opinions, longer discussions, and meetings that creep past 15 minutes.

**When:** Same time every week. Non-negotiable. If it moves around, it dies within a month. Put it on the calendar as recurring with no end date.

**Duration:** 15 minutes maximum. Set a timer. If it's longer than 15 minutes, you're solving problems in the meeting instead of identifying them for after.

---

## What to Look At

Whatever metrics you have. Seriously.

If you have a DORA dashboard, look at that. If you have Swarmia or LinearB, look at that. If you have nothing but GitHub and a CI pipeline, look at:

- PRs merged this week
- CI failures this week
- Any incidents or rollbacks

That's enough to start. The meeting is more important than the metrics.

As your measurement matures, you can add more signals. But don't wait for perfect measurement to start the habit.

---

## The Three Questions

Every week, answer these three questions. Write the answers down somewhere your team can see them (a shared doc, a Slack channel, whatever sticks).

### 1. Are things better, worse, or the same as last week?

Not better or worse against a benchmark. Not better or worse against another team. Better or worse than **last week, for this team**.

If you don't know, say "same" and move on. The point is to establish a trend over weeks and months, not to judge any single week.

### 2. What was the most expensive PR this week?

"Expensive" means whatever cost your team the most effort or caused the most problems:

- The PR that required the most review rounds
- The PR that caused an incident after merge
- The PR that took the longest from open to merge
- The PR that was the hardest to review

Pick one. Discuss it for two minutes. Not to blame anyone — to understand what made it expensive and whether the pattern is recurring.

### 3. What one thing do we change for next week?

One thing. Not three. Not five. One concrete change that you can actually check on next week.

Examples:
- "PRs over 400 lines get split before review"
- "We add a lint rule for that error class that keeps recurring"
- "We require a test for any PR that touches the payments module"

If last week's change helped, keep it. If it didn't, drop it and try something else.

---

## What This Is NOT

**Not a standup.** You're not going around the room asking what everyone did yesterday.

**Not a retrospective.** You're not processing feelings about the sprint. Retros are valuable — this is not one.

**Not a metrics review.** You're not staring at a dashboard for 15 minutes while someone narrates charts. You look at the numbers for 2 minutes, then you talk about what they mean.

**Not a performance review.** No individual names. No "who wrote that bad PR." The unit of analysis is the team, the PR, or the process — never the person.

---

## Why This Works

The weekly review works because it creates a **feedback loop with a one-week cycle time**. Most teams have no feedback loop shorter than a quarterly retro or an annual performance review. By then, the details are gone and the problems have compounded.

One week is short enough to remember what happened. Short enough to try a change and see if it helped. Short enough that "better than last week" is a meaningful comparison.

The discipline is in the cadence, not the analysis. Show up, look at the numbers, ask the three questions, pick one thing to change. Repeat. The compounding effect over months is where the real value appears.

---

## Getting Started

1. Pick a time slot this week
2. Invite your tech lead and one IC
3. Pull up your GitHub PR list and CI dashboard
4. Ask the three questions
5. Write down your one change
6. Do it again next week
