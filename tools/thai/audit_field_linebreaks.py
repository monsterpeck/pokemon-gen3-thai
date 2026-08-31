from pathlib import Path
import csv, ctypes, json, re

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / 'tools/thai/font/thai_precompose_glyph_map.json'
IDMAP = {int(e['target_index']): e['name'] for e in json.loads(MAP.read_text(encoding='utf-8'))['glyphs']}
NUM = re.compile(r'\{(\d+)\}')
THAI = re.compile(r'[\u0E00-\u0E7F]')
PROTECTED_TERMS = set()
for rel, col in [('tools/thai/translation/glossary.csv', 1), ('tools/thai/translation/story_order/translation/glossary.csv', 2)]:
    with (ROOT / rel).open(encoding='utf-8', newline='') as handle:
        for row in csv.reader(handle):
            if len(row) > col:
                term = row[col].strip()
                if len(term) >= 2 and THAI.search(term) and not re.search(r'\s', term):
                    PROTECTED_TERMS.add(term)

lib = ctypes.CDLL('libthai.so.0')
lib.th_brk.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_size_t]
lib.th_brk.restype = ctypes.c_int

def thai_breaks(text):
    # libthai expects TIS-620. Preserve one-byte positions for non-TIS symbols
    # (ellipsis, smart quotes, placeholders) by substituting an ASCII marker.
    raw = b''.join(
        ch.encode('tis-620') if ord(ch) < 128 or '\u0e00' <= ch <= '\u0e7f' else b'X'
        for ch in text
    )
    out = (ctypes.c_int * (len(raw) + 2))()
    n = lib.th_brk(raw, out, len(out))
    return {int(out[i]) for i in range(n)}
def parse_numeric(body, pos):
    vals = []
    p = pos
    for _ in range(8):
        m = NUM.match(body, p)
        if not m:
            return None
        vals.append(int(m.group(1)))
        p = m.end()
    if vals[0] == 252 and vals[1] == 25:
        gid = vals[2] | (vals[3] << 8)
        if gid in IDMAP:
            return IDMAP[gid], p
    return None

def decode_body(body):
    out = []
    i = 0
    while i < len(body):
        rec = parse_numeric(body, i) if body.startswith('{', i) else None
        if rec:
            cluster, i = rec
            out.append(cluster)
            continue
        if body.startswith('\\n', i): out.append('\n'); i += 2; continue
        if body.startswith('\\l', i): out.append('\n'); i += 2; continue
        if body.startswith('\\p', i): out.append('\f'); i += 2; continue
        if body.startswith('\\', i) and i + 1 < len(body):
            out.append(body[i+1]); i += 2; continue
        if body.startswith('{', i):
            end = body.find('}', i + 1)
            if end >= 0:
                out.append('¤')
                i = end + 1
                continue
        out.append(body[i])
        i += 1
    return ''.join(out)

def break_violations(text):
    found = []
    for page in text.split('\f'):
        lines = page.split('\n')
        if len(lines) < 2:
            continue
        flat = ''.join(lines)
        legal = thai_breaks(flat)
        pos = 0
        for left, right in zip(lines, lines[1:]):
            pos += len(left)
            protected = None
            for term in PROTECTED_TERMS:
                start = flat.rfind(term, 0, pos + len(term))
                if start >= 0 and start < pos < start + len(term):
                    protected = term
                    break
            prev = flat[pos - 1] if pos else ''
            nxt = flat[pos] if pos < len(flat) else ''
            if protected is not None:
                found.append(('PROTECTED_TERM', left[-18:], right[:18], protected))
            elif THAI.match(prev) and THAI.match(nxt) and pos not in legal:
                found.append(('MID_WORD', left[-18:], right[:18], ''))
            if nxt and nxt in '?!.,ๆ':
                found.append(('ORPHAN_PUNCT', left[-18:], right[:18], ''))
    return found
# libthai does not know every Pokémon proper noun / loanword. These labels were
# manually reviewed once and their existing break is intentional and readable.
ALLOWED_LABELS = {
    'DewfordTown_Text_GymSign',
    'DewfordTown_Gym_Text_ReceivedKnuckleBadge',
    'FortreeCity_Text_GymSign',
    'FortreeCity_Gym_Text_ReceivedFeatherBadge',
    'JaggedPass_Text_EthanDefeat',
    'LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge',
    'LilycoveCity_PokemonTrainerFanClub_Text_MyFavoriteTrainerIsBrawly',
    'LittlerootTown_Text_SwitchShoesWithRunningShoes',
    'RivalsHouse_2F_Text_BrendanWhoAreYou',
    'MauvilleCity_Text_GymSign',
    'MauvilleCity_Gym_Text_ReceivedDynamoBadge',
    'MauvilleCity_PokemonCenter_1F_Text_MyDataUpdatedFromRecordCorner',
    'MossdeepCity_Text_GymSign',
    'MossdeepCity_House2_Text_PokemonCarriesMailBackAndForth',
    'PacifidlogTown_Text_FastRunningCurrent',
    'PetalburgCity_Gym_Text_ReceivedBalanceBadge',
    'Route101_Text_TakeTiredPokemonToPokeCenter',
    'Route110_TrickHouseEnd_Text_LeavingOnJourney',
    'RustboroCity_Gym_Text_ReceivedStoneBadge',
    'RustboroCity_House2_Text_RoxanneKnowsALot',
    'SootopolisCity_Text_GymSign',
    'SootopolisCity_Text_AwakenedPokemonClash',
}

files = sorted((ROOT / 'data/maps').rglob('*.inc')) + [ROOT / 'data/event_scripts.s']
checked = 0
violations = []
for path in files:
    label = '<unknown>'
    for lineno, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
        stripped = line.strip()
        if stripped.endswith(':') and not stripped.startswith('.'):
            label = stripped[:-1]
        if '.string ' not in line or '"' not in line:
            continue
        first = line.find('"')
        last = line.rfind('"')
        if last <= first:
            continue
        body = line[first+1:last]
        if '{252}{25}' not in body or ('\\n' not in body and '\\l' not in body):
            continue
        checked += 1
        text = decode_body(body)
        for kind, left, right, detail in break_violations(text):
            violations.append((str(path.relative_to(ROOT)), lineno, label, kind, left, right, detail, text))

ALLOWED_PROTECTED_TERM_BREAKS = {('FortreeCity_Text_GymSign', 'ฮิวะมากิยิม')}
def is_allowed(row):
    _path, _lineno, label, kind, _left, _right, detail, _text = row
    if kind == 'PROTECTED_TERM':
        return (label, detail) in ALLOWED_PROTECTED_TERM_BREAKS
    return label in ALLOWED_LABELS

allowed = [row for row in violations if is_allowed(row)]
actionable = [row for row in violations if not is_allowed(row)]
print(
    f'FIELD_LINEBREAK_GATE checked={checked} raw={len(violations)} '
    f'allowed={len(allowed)} actionable={len(actionable)}'
)
if actionable:
    for path, lineno, label, kind, left, right, detail, _text in actionable:
        suffix = f' term={detail!r}' if detail else ''
        print(f'{kind} {path}:{lineno} {label} :: {left!r} | {right!r}{suffix}')
    print('RESULT: FAIL')
    raise SystemExit(1)
print('RESULT: PASS')
