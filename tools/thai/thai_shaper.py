#!/usr/bin/env python3
"""Host-side reference model for the metadata-driven Thai renderer."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
METADATA = HERE / "font/thai_glyph_metadata.csv"
BASE_METRICS = HERE / "font/thai_base_metrics.csv"


@dataclass(frozen=True)
class Event:
    char: str
    glyph_id: int | None
    glyph_class: str
    x: int
    y: int
    advance: int
    component: str = ""


def load_metadata():
    with METADATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["char"]: {**row, "glyph_id": int(row["glyph_id"], 0),
                           "advance": int(row["advance"]),
                           "mark_x": int(row["mark_x"]),
                           "mark_y": int(row["mark_y"]),
                           "second_level_y": int(row["second_level_y"])} for row in rows}


def load_base_metrics():
    with BASE_METRICS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {int(row["glyph_id"], 0): {key: value if key == "shape_group" else int(value, 0)
            for key, value in row.items()} for row in rows}


def shape(text: str) -> list[Event]:
    metadata, metrics = load_metadata(), load_base_metrics()
    events: list[Event] = []
    cursor = 0
    base = None
    upper = False
    for char in text:
        row = metadata.get(char)
        if row is None:
            events.append(Event(char, None, "NON_THAI", cursor, 0, 0))
            base, upper = None, False
            continue
        cls, advance = row["class"], row["advance"]
        if cls in {"BASE", "LEADING_VOWEL", "SPACING_VOWEL", "PUNCTUATION"}:
            events.append(Event(char, row["glyph_id"], cls, cursor, 0, advance))
            cursor += advance
            base = row if cls == "BASE" else None
            upper = False
            continue
        if cls == "SARA_AM":
            if base:
                metric = metrics[base["glyph_id"]]
                events.append(Event("ํ", int(row["component_id"], 0), "NIKHAHIT",
                                    metric["upper_x"] + row["mark_x"],
                                    metric["upper_y"] + row["mark_y"], 0, "nikhahit"))
            events.append(Event("า", 0x11C, "SPACING_VOWEL", cursor, 0, advance, "sara_aa"))
            cursor += advance
            base, upper = None, False
            continue
        if base:
            metric = metrics[base["glyph_id"]]
            if cls == "LOWER_VOWEL":
                x, y = metric["lower_x"], metric["lower_y"]
            elif cls in {"TONE", "THAN_THAKHAT"}:
                x, y = metric["tone_x"], metric["tone_y"] + (row["second_level_y"] if upper else 0)
            else:
                x, y = metric["upper_x"], metric["upper_y"]
            x += row["mark_x"]
            y += row["mark_y"]
            if cls == "UPPER_VOWEL":
                upper = True
            events.append(Event(char, row["glyph_id"], cls, x, y, 0))
        else:
            events.append(Event(char, row["glyph_id"], cls, cursor, 0, 4))
    return events


def logical_width(text: str) -> int:
    return sum(event.advance for event in shape(text))
