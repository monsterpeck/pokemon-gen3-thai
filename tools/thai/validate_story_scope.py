#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'tools/thai/translation/story_order'
def read(path):
    if not path.read_bytes().startswith(b'\xef\xbb\xbf'): raise ValueError(f'{path}: missing BOM')
    return list(csv.DictReader(path.open(encoding='utf-8-sig',newline='')))
def main():
    try:
        ordered=read(OUT/'dialogue_main_story_ordered.csv'); events=read(OUT/'story_events.csv'); links=read(OUT/'dialogue_event_links.csv'); audit=read(OUT/'scope_audit.csv'); master={r['id']:r for r in read(OUT.parent/'dialogue_master.csv')}; ids=[r['id'] for r in ordered]
        audit_by_id={r['dialogue_id']:r for r in audit}
        assert [int(r['global_order']) for r in ordered]==list(range(1,len(ordered)+1))
        assert all(audit_by_id[r['id']]['mandatory']=='yes' and audit_by_id[r['id']]['final_category']=='main_story' for r in ordered)
        assert all(r['mandatory_path']=='yes' and r['scope_decision']=='main_story' for r in links)
        forbidden={'LittlerootTown_ProfessorBirchsLab_Text_CompletedDexChoosePokemon','LittlerootTown_ProfessorBirchsLab_Text_ReceivedJohtoStarter','RustboroCity_Gym_Text_GymGuideAdvice','RustboroCity_Gym_Text_GymStatue','MauvilleCity_Text_WattsonNeedFavorTakeKey'}
        assert not forbidden.intersection(r['source_label'] for r in ordered)
        assert not any(r['final_category'] in {'optional_npc','optional_interaction','optional_sidequest','postgame','optional_reward','sign','trainer'} and r['dialogue_id'] in ids for r in audit)
        assert len(ids)==len(set(ids)); assert set(ids)=={r['dialogue_id'] for r in links}
        assert all(r['event_id'] and r['script_label'] for r in ordered)
        assert all(not r['thai'] and r['translation_status']=='untranslated' for r in ordered)
        assert all(master[r['id']]['english_raw']==r['english_raw'] for r in ordered)
        assert not any('Rematch' in r['script_label'] or 'Decline' in r['script_label'] for r in ordered)
        map_ids=[r['id'] for p in (OUT/'maps').glob('*.csv') for r in read(p)]; chapter_ids=[r['id'] for p in (OUT/'chapters').glob('*.csv') for r in read(p)]
        assert sorted(map_ids)==sorted(ids)==sorted(chapter_ids); assert len(events)==45
        assert json.loads((OUT/'script_graph.json').read_text())['nodes']; assert audit
        assert not any(': missing' in line for line in (OUT/'coverage_report.md').read_text().splitlines())
    except (AssertionError,ValueError,KeyError,FileNotFoundError) as error:
        print(f'story scope validation failed: {error}',file=sys.stderr); return 1
    print(f'story scope validation passed ({len(ordered)} rows, {len(events)} events)'); return 0
if __name__=='__main__': raise SystemExit(main())
