# EQ Legends Item Reference

A living reference of community-recommended items in **EverQuest Legends** (launched
2026-07-28) — what each item does and how to get it. Rendered to a single screen HTML
page with a live filter.

## Files

| File | Role |
|---|---|
| `eqlegends-recommended-items.md` | **Source of truth.** Edit this and nothing else. |
| `rebuild.py` | Regenerates the HTML from the markdown. |
| `eqlegends-recommended-items.html` | Generated, but **committed** — it's the deployable artifact. Dark EQ-tooltip theme, live filter, mobile cards. |
| `README.md` | Repo landing page. Hand-written — not generated. |
| `LICENSE` | MIT — covers the code. |
| `LICENSE-DOCS.md` | CC BY 4.0 — covers the reference content. |

Rebuild with:

```bash
python3 rebuild.py eqlegends-recommended-items.md
```

`rebuild.py` is standard-library only — no third-party packages and no external binaries, so
there's nothing to install.

**If a dependency ever does show up, work in a virtual environment** — never install into the
system Python:

```bash
python3 -m venv .venv
```

Activate with `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1`
(Windows PowerShell). `.venv/` is already gitignored.

Don't hand-edit the .html — it gets overwritten. The .html is tracked in git so it can be
dropped straight onto a static host, so **rebuild and commit it in the same commit as any
markdown edit**, or the deployed page drifts from the source. It's fully self-contained
except for the Google Fonts link in `<head>`; without network access the page falls back to
system serif/mono and still works.

## License

Split, because the two halves of this repo are different kinds of work:

- **Code** (`rebuild.py`) — MIT. See [LICENSE](LICENSE).
- **Content** (`eqlegends-recommended-items.md` and the generated HTML) — CC BY 4.0. See
  [LICENSE-DOCS.md](LICENSE-DOCS.md).

The CC BY attribution line is rendered into the page footer by `build_screen_html()`, so it
travels with the deployed HTML. If you change the footer, keep the license link — attribution
is the one condition CC BY imposes.

Note that CC BY covers the editorial work, not the underlying facts, and not passages
inherited from the upstream sources listed below. `LICENSE-DOCS.md` spells this out.

## Markdown conventions the renderer depends on

The parser in `rebuild.py` is deliberately small and will silently produce wrong output if
these break:

- **Tables are for items only, and have exactly three columns**: `Item | Description | How to
  Obtain`. Don't add a table for anything else — put mechanics, thresholds, and comparisons in
  prose or a `- ` list. The parser hard-codes three cells per row, so a two-column table
  renders a mismatched `<thead>`, and *every* table row counts toward the "N items" figure in
  the filter bar, so a four-row mechanics table silently inflates the item count by four.
- `## ` headings become numbered sections and nav links. `### ` are subheadings inside a
  section and get no nav entry.
- The **first paragraph** after the H1 becomes the page lede; the **second** becomes the
  sources line. Don't add a third paragraph before the first `## `.
- Supported inline markup: `**bold**`, `*italic*`, `` `code` ``, `[text](url)`. Nothing
  else — no images, no nested lists, no footnotes.
- `---` horizontal rules are dropped from the HTML.

The HTML filter indexes all three cells of every row, so zone names, mob names, and effect
names in any column are searchable. Write them out in full rather than abbreviating.

## Editorial standards

This is a reference someone reads while playing, so:

- **Attribute confidence.** Distinguish wiki-documented facts from "community reports say."
  The game is new and a lot of circulating information is inherited from classic EQ (1999)
  rather than verified in EQL.
- **Prefer specifics over adjectives.** Coordinates, drop percentages, level ranges, and
  placeholder mechanics are the useful part. "Really good item" is not.
- **Flag contradictions rather than resolving them silently.** Where the wiki and the
  community farm lists disagree, say so and name both.
- Keep the Caveats section at the bottom current — it dates the whole document.

## Source hierarchy

1. [EQL Wiki](https://eqlwiki.com) — item stat blocks, quest walkthroughs. Explicitly in
   BETA; some "no longer drops" flags are inherited from classic EQ and may be wrong.
2. [EQ Legends Tools](https://eqlegendstools.com) — searchable clicky/focus/proc database,
   curated and updated on a stated bi-weekly cadence. **Renders its tables client-side, so
   fetching the URL returns nothing** — this one needs a human with a browser.
3. [EverQuest Guides farm list](https://www.everquestguides.com) — the best community
   camp-by-camp source; beta-era, so treat drop locations as strong leads.
4. [EQProgression](https://www.eqprogression.com/legends/exaltations/) — mechanics-focused,
   decent on Exaltation rules.
5. In-game general chat, the EQL Discord, and reddit — freshest, least verified. Note that
   reddit can't be fetched by Claude Code's web tools; a human has to read it.

**Two traps when sourcing:**

- **`eqlegends.wiki` and `everquestlegends.wiki` are not the tier-1 wiki.** Only `eqlwiki.com`
  is. The other two look like content farms recycling each other — three sites agreeing is
  one source, not three.
- **Searches for legacy items return classic EQ (1999), not EQL,** at the top of the results:
  Project 1999, Allakhazam, Project Quarm, usenet. The `eqlwiki` pages themselves inherit
  some of these notes. The phrase **"on Live"** is the reliable tell that a note is about
  classic EQ.

## Open questions to resolve

- **Journeyman's Boots — does Drelzna drop them in EQL?** Narrowed but not closed (checked
  2026-08-01). The `eqlwiki` **item** page lists Drops From → Najena → Drelzna with no "no
  longer drops" flag; the **Drelzna** page lists them at 20% rare *and* carries a "made a
  quest on October 13, 1999 on Live" note. So the wiki contradicts itself, and the note is
  classic-EQ inheritance rather than an EQL claim. Drelzna is level 25 in Najena at
  `(-35, -222)`, necromancer placeholder in the middle room, ~18.5–19 min respawn — so this
  is cheap to settle: camp her and watch. The doc flags both routes rather than picking.
- **Manastone — has anyone actually camped An Evil Eye?** This is what's left of the legacy
  item question (see Resolved). The wiki still lists the drop source and says only "no
  confirmed sightings," so the item may simply be rare and under-reported rather than removed.
  One person reporting a clear result either way closes it.
- **Guise of the Deceiver — is there any route to it?** The wiki documents no source at all:
  not dropped, not sold, no quest, not crafted. Either it's genuinely unobtainable in EQL or
  the page is incomplete. Also **its class restriction is contested** — wiki says BRD/ROG,
  community describes the all-class pre-nerf version.
- **Does the Rubicite regen really work from any slot?** The community claim is that its
  HP Regen 6 works from any slot once extracted, but the
  [Exaltations page](https://eqlwiki.com/Exaltations) says an Exaltation keeps its source
  item's slot restriction — and the breastplate is CHEST. Both are in the doc, flagged as
  disagreeing.
- **Footman's Blade — does this item exist in EQL under this name?** The wiki 404s on it
  (checked 2026-08-01). A search summary claimed it was renamed to *The Baron's Blade*, but
  the [Patch Notes](https://eqlwiki.com/Patch_Notes) do not mention any such rename and the
  Baron's Blade page doesn't reference a former name — so that claim is unsupported and was
  not written into the doc. Complicating it, the doc describes a level-15 mob while Baron
  Telyx V\`Zher is a named boss, so they're probably different items. Someone needs to look
  in-game or find the right wiki page.
- **Ignite proc damage — needs one parse against a non-fire mob.** Narrowed (2026-08-01). The
  wiki lists Ignite at **38 (L8) to 46 (L16)**, resist type Fire, capping at L16 — so the
  circulating "~8 a hit" figure conflicts with the documented value by ~5x. The single parse
  behind it was a Lord Nagafen kill: a fire proc into a level-55 fire dragon. Caveat on the
  explanation — the wiki does *not* document Nagafen's fire resistance, and the "fire and magic
  resists mean everything" line on his page refers to the *player's* resists against Lava
  Breath. So resist-on-target is a hypothesis, and one that leans on classic-EQ intuition,
  which is the exact trap flagged above. Any ordinary mob parse settles it.

### Resolved

- **Full name audit — all 39 items checked against the wiki** (2026-08-01). Findings, because
  the *rate* matters more than the individual fixes: **7 item names wrong, 6 mob names wrong,
  2 zones wrong, 6 stat blocks wrong**, across roughly a third of the document. One entry was
  wholly fabricated (see below). Everything is now the wiki's spelling. **Standing rule from
  this: verify the name against `eqlwiki.com` before adding any row.** A misspelled item or mob
  sends a reader hunting something that doesn't exist and looks like a dead camp, which is
  worse than omitting the row. Where a community detail survives without wiki support — the
  Slave Trammels +2 behaviour, the Kitchen Toolbelt's ~20% scaling, various spawn percentages —
  it is now labelled as community-only in the row rather than stated flatly.
- **"Rune Totem Staff off Kerak Splitpaw" doesn't exist** (2026-08-01). Removed. Five checks
  all came back empty: item page 404, mob page 404, no Kerak among the named mobs on the
  Splitpaw Lair page, no staff in Verishe Mal Executioner's loot table, and no site-search hit
  for either name. The only genuine detail was the Executioner — **Verishe Mal Executioner**,
  L42, `(1171, 113)`. Replaced with the **Gnoll Hide Tome** (Rosch Val L'Vlor, Splitpaw Lair),
  which is documented. **The lesson is the one worth keeping:** that row named a plausible item
  and a plausible mob, sat unremarked among correct entries, and was fabricated end to end. A
  row being specific is not evidence it is true — the two other rows still resting on nothing
  but community reports are Footman's Blade and the Guise camp details.
- **Legacy item status — the items don't share one status** (2026-08-01). The old question
  assumed a single "no longer drops" flag applied to all three. It doesn't: **Guise of the
  Deceiver** has no documented source of any kind, while **Manastone** has only "no confirmed
  sightings" with its source still listed. The doc had flattened them into one phrase and
  stated the Manastone case more strongly than the source supports. Both remaining cases are
  tracked as narrower questions above. The third item, **Fungus Covered Great Staff**, was
  removed from the doc entirely — its source zone is Out of Era (see below).
  **Correction worth recording:** an earlier pass claimed the Fungus staff's "No Longer Drops"
  flag could not be explained by unimplemented content, on the grounds that Old Sebilis "is
  implemented, Kunark era." That was a misreading of **"Out of Era,"** which means the opposite
  of what it looks like — the zone is *not* accessible. So pending content is in fact the most
  likely explanation for that flag.
- **Exaltation extraction threshold** (2026-08-01). It's per *effect type*, not one number,
  which is why sources appeared to disagree: **Focus +1, Click +2, Worn +3, Proc +4**, per
  the [Exaltations page](https://eqlwiki.com/Exaltations). Also documented there: an
  Exaltation keeps its source item's slot restriction, and the destination item's usable
  classes narrow to the overlap. Wiki-documented, not yet in-game verified.

## Context

Game mechanics that shape which items matter, for anyone picking this up cold:

- **Scope: Classic era plus the Planes. Nothing else is in the game.** EQL launched
  2026-07-28 with Classic content; the [News page](https://eqlwiki.com/News) says to "assume
  that Kunark and Velious content will not be present immediately." On the
  [Zones page](https://eqlwiki.com/Zones), those expansions are listed under
  **"Out of Era."** **That label means not currently accessible** — it reads like "available
  but off-era" and it is not. Kunark and Velious *item* pages look entirely normal, with
  stats and named drop sources, so the item page alone will happily lead you to farm a zone
  you cannot enter. **Before adding any item, check its zone's era.** Confirmed Out of Era so
  far: Lake of Ill Omen, Warsliks Woods, Old Sebilis (Kunark), Iceclad Ocean (Velious).
  The Hole is *not* — it's Odus, and playable.
- **Quests carry their own era flag, independent of their zones.** **All class epics are Out of
  Era** ([Class Epic Quest List](https://eqlwiki.com/Class_Epic_Quest_List) is headed "Epic
  Quests Era: Out of Era"). The Paladin epic is the instructive case: every zone it touches is
  Classic, and the quest is still gated. So checking zone eras is *not sufficient* — open the
  quest page and look for its own flag. This also catches quests that don't look epic but sit
  under that umbrella, e.g. **The Sword of Nobility**, the Ghoulbane quest route. Confirmed in
  era: the Journeyman's Boots quest, Lynuga's Gem Collection.

- Characters run **up to three simultaneous classes**; an item is usable if any of the three
  qualifies. This is why class restrictions matter less than in classic EQ.
- **Exaltation:** level an item, extract its click/proc/focus effect, socket it into a
  different item. Makes otherwise-mediocre items valuable as donors. Both donor and
  destination must share a class with your build or the mote is lost.
- **Difficulty tiers** (D0–D4) don't change loot tables, they change merge value:
  D0=1, D1=2, D2=4, D3=8, D4=16 points toward +10.
