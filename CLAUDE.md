# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **content operations system** for a faceless WWII documentary YouTube channel. There is no software code — it is a strategic playbook consisting of interconnected Markdown documents and Claude slash commands that work together to produce YouTube-ready content.

## Repository Structure

| File | Purpose |
|---|---|
| `CHANNEL_STRATEGY.md` | Master strategy: niche positioning, audience targeting, competitor analysis, production stack, monetization roadmap, KPIs |
| `CONTENT_PILLARS.md` | The 6-pillar framework with 185+ video ideas organized by category and search priority |
| `SCRIPT_FRAMEWORK.md` | The 8-part documentary structure every script must follow, with narration style rules |
| `VIRAL_TITLE_FORMULAS.md` | 12 title formulas with psychological rationale, CTR ranges, and construction rules |
| `SEO_KEYWORDS.md` | Three-tier keyword system, video description template, tag strategy, and posting schedule |
| `CONTENT_CALENDAR.md` | 90-day launch calendar with specific titles, thumbnails, and pillar assignments per upload day |

### Claude Commands (`.claude/commands/`)

These are slash commands that automate the content creation workflow:

| Command | Function | Key Reference Doc |
|---|---|---|
| `/wwii-ideas` | Generate a prioritized batch of video ideas | `CONTENT_PILLARS.md` |
| `/wwii-title` | Generate 12 title variations for a topic (one per formula) | `VIRAL_TITLE_FORMULAS.md` |
| `/wwii-script` | Write a full 8-part voiceover script | `SCRIPT_FRAMEWORK.md` |
| `/wwii-thumbnail` | Generate a 3-option thumbnail design brief | `VIRAL_TITLE_FORMULAS.md` |
| `/wwii-seo` | Generate a complete publish-ready metadata package | `SEO_KEYWORDS.md` |

All commands accept a topic or title via `$ARGUMENTS`.

## Content Creation Workflow

The intended production pipeline is sequential:

```
/wwii-ideas [pillar or theme]
    → /wwii-title [chosen topic]
    → /wwii-thumbnail [chosen title]
    → /wwii-seo [chosen title]
    → /wwii-script [topic + chosen title]
```

Each step depends on output from the previous step. The script command is last because it requires a final confirmed title.

## The 6-Pillar Content Framework

All content must fit one of six pillars with specific upload ratios (per 10 videos):

| Pillar | Ratio | CPM Range |
|---|---|---|
| Famous Battles & Operations | 3/10 | $5–8 |
| Weapons & Military Technology | 2/10 | $6–10 |
| Key Leaders & Commanders | 2/10 | $5–8 |
| Strategy, Decisions & Mistakes | 1/10 | $6–9 |
| Secret Operations & Intelligence | 1/10 | $5–8 |
| Untold Stories & Forgotten Heroes | 1/10 | $4–7 |

## The 8-Part Script Structure

Every script must follow this structure exactly (see `SCRIPT_FRAMEWORK.md` for full detail):

1. **Cold Open** (0:00–0:45) — Drop into the most dramatic moment; no context yet
2. **The Promise** (0:45–1:30) — State exactly what revelation the viewer will receive
3. **Context** (1:30–3:30) — Strategic situation, 2–3 key players, stakes
4. **The Build** (3:30–6:00) — Events as Situation → Decision → Information Gap → Choice → Consequence cycles
5. **Mid-Roll Re-Hook** (6:00–6:30) — Tease what's next; never say "like and subscribe"
6. **The Climax** (6:30–10:00) — Turning point, slow down time, direct quotes, contrast technique
7. **Aftermath & Legacy** (10:00–12:30) — Strategic consequences, human cost, historian verdict, "zoom out"
8. **Closing Hook** (12:30–13:30) — Summarize revelation → universal truth → tease next video → subscribe CTA as invitation

Target word count: ~1,400 words for a 10-minute video (~130 wpm documentary pace).

## Critical Rules for Title Generation

- Optimal title length: **50–65 characters** (mobile-optimized)
- Capitalize 1–3 key words for emphasis — never the full title
- Every title must exploit the **curiosity gap**: make not clicking feel like a loss
- Include at least one power word: `REAL · Secret · Hidden · Worst · Greatest · Forgotten · Banned · Shocking · Untold · Inside`
- If CTR < 3.5% after 500 impressions → change thumbnail; after 2,000 impressions → change title + thumbnail

## Critical Rules for SEO Metadata

- Primary keyword must appear in the **first 5 words** of the title
- Description: first 2 lines are shown in search results — these must match the title's curiosity gap
- Use exactly **5 hashtags** at end of description; more than 5 reduces reach
- Chapter titles must be dramatic, never generic (bad: "Background"; good: "The Decision That Changed Everything")
- Best posting days for the history niche: **Thursday, Saturday morning, Sunday morning**

## Key Anniversary Dates (Highest-Traffic Days)

| Date | Event | Priority |
|---|---|---|
| Jun 6 | D-Day | Highest traffic day of the year for WWII channels |
| Dec 7 | Pearl Harbor | Second highest traffic day |
| May 8 | VE Day | High |
| Aug 6 | Hiroshima | High |
| Sep 1 | Invasion of Poland | Medium-High |

Always have D-Day content ready every June 6.

## Channel Positioning

The channel's differentiation is **cross-category "revelation" content** — always answering "what did you NOT know about this?" Avoid single-lane coverage (weapons-only, battles-only). Every video pairs a major event with either a moral complexity angle, a counterfactual hook, a human-scale story, or a speed-to-publish hook tied to an anniversary.

Target video length: **8–18 minutes** (sweet spot between enthusiast depth and casual viewer patience).
