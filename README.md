# EverQuest Legends — Community-Recommended Items

A living reference of **39 items** worth chasing in [EverQuest Legends](https://eqlwiki.com),
covering what each one does and how to get it. The markdown source is rendered to a
self-contained HTML page with a live filter over item names, zones, mobs, and effects.

> **This is launch-week knowledge, not settled fact.** EQL launched July 28, 2026. Drop
> rates, camps, and stat blocks are still being verified — treat locations as starting
> points. Contradictions between sources are flagged in the document rather than silently
> resolved.

**Everything listed is reachable today.** EQL launched with Classic-era content and the
Planes; Kunark, Velious, and all class epic quests are flagged "Out of Era" on the wiki, which
means not yet accessible. Items sourced from that content have been removed rather than listed
with a caveat, because their wiki pages look entirely normal and will happily send you to farm
a zone you can't enter.

## What's in it

| Section | Covers |
|---|---|
| Why people chase these | The Exaltation system and difficulty-tier merge math |
| The Big Ones | Classic legacy items — Manastone, Guise, Journeyman's Boots |
| Best Clickies and Focus Effects | Effects worth carrying to 50, plus utility clicks |
| Early Armor | Low-level pieces worth a detour |
| Weapons | Procs, damage, and donor candidates |
| Instant-Clicky Tricks | Timing and cast-time exploits |
| Caveats | What's contested, what was verified, and as of when |

## Reading it

The generated page — `eqlegends-recommended-items.html` — is committed to this repo and has
no build step or external dependencies. Clone and open it in a browser, or download it from
the file view. Press <kbd>/</kbd> to jump to the filter; it searches all three columns, so a
zone or mob name finds every item that drops there.

The markdown renders fine on GitHub too, if you just want to read it in place:
[eqlegends-recommended-items.md](eqlegends-recommended-items.md).

## Rebuilding

`rebuild.py` is standard-library only — no dependencies, nothing to install. Any Python 3
will do:

```bash
python3 rebuild.py eqlegends-recommended-items.md
```

Edit **`eqlegends-recommended-items.md` and nothing else.** The HTML is generated, but it's
tracked in git as the deployable artifact — so rebuild and commit it in the same commit as
any markdown change, or the published page drifts from the source.

The parser is deliberately small and will silently produce wrong output if you break its
assumptions — three-column tables, `## ` for sections, a limited set of inline markup. See
[CLAUDE.md](CLAUDE.md) for the full conventions, the editorial standards, and the source
hierarchy.

## Contributing

The most useful contribution is **verification**. Several claims rest on a single data point
or on classic-EQ information that may not hold in EQL. The open questions are tracked in
[CLAUDE.md](CLAUDE.md) — currently the two competing sources for Journeyman's Boots, the
status of the "no longer drops" legacy items, the real Exaltation extraction threshold, and
the Ignite proc damage.

When you add something, attribute its confidence. "Wiki-documented" and "community reports
say" are different claims and the document keeps them apart.

## License

Split, because this repo is two kinds of work:

- **Code** (`rebuild.py`) — [MIT](LICENSE).
- **Content** (the markdown and the generated HTML) — [CC BY 4.0](LICENSE-DOCS.md).

CC BY covers the editorial work — selection, organization, wording, verification notes. It
does not extend to the underlying facts, which aren't copyrightable, or to passages inherited
from the upstream sources. [LICENSE-DOCS.md](LICENSE-DOCS.md) has the details.

## Sources

In rough order of how much weight they carry:

1. [EQL Wiki](https://eqlwiki.com) — stat blocks and quest walkthroughs. Explicitly in beta.
2. [EQ Legends Tools](https://eqlegendstools.com) — searchable clicky/focus/proc database.
3. [EverQuest Guides farm list](https://www.everquestguides.com) — camp-by-camp, beta-era.
4. In-game general chat and the EQL Discord — freshest, least verified.

---

Unofficial fan reference. Not affiliated with or endorsed by the publisher of EverQuest
Legends; all game names and content belong to their respective owners.
