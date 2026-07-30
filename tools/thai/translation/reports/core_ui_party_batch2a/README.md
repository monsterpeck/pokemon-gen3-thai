# Phase 5 Batch 2A — Party Menu

Source checkpoint: `fe8ba3510` on `work/core-ui-inventory`.

## Applied translations

- Direct Party labels/actions: 26/26.
- Revised after semantic review: `ABLE`, `NOT ABLE`, `LEARNED`, and `STORE`.
- Deferred stat terms: 9 unchanged.
- Cross-screen symbols requiring broader runtime QA: 2.

## Automated QA

- Source definitions matched exactly: 26/26.
- Thai precompose shaper: passed.
- Width checks: 26/26 passed.
- Widest translation: `gText_NotAble` at 58 px.
- Tightest margin: `gText_NotAble` with 6 px remaining.
- Normal ROM build: passed.
- Source SHA-256: `e0a3af0439dfbd3863d728b28885eb35e45b46f0072d160ff7182550d9fcbfd7`.
- ROM SHA-256: `8cadd3344b72fc456fed82fe431957780fb4e43c0a4338aaa9636f11110b6f61`.

## Status

All 26 entries are `translated_pending_qa`. Runtime visual evidence is required before any entry is changed to `proof_passed`.

## Shaper verification

```text
Map format       : pokemon-gen3-thai-precompose-full-v1
Glyph count      : 761
Atlas size       : [256, 768]
Start-game       : เ | ริ่ | ม | เ | ก | ม | ส์
Total advance    : 40
RESULT: PRECOMPOSE SHAPER CHECK PASSED
```
