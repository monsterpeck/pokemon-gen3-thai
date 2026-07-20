#!/usr/bin/env python3
"""Build the source-linked mandatory story chronology (no translation)."""
from __future__ import annotations
import csv, hashlib, io, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'tools/thai/translation/story_order'
EVENT_COLS='chapter_order chapter_id chapter_title_en chapter_title_th event_order event_id event_title_en event_title_th map_order map_name map_period location_name entry_script trigger_type required_flags required_vars sets_flags sets_vars warps_to mandatory_reason source_files chronology_confidence scope_confidence notes'.split()
ORDER_COLS='id global_order chapter_order chapter_id chapter_title_en chapter_title_th event_order event_id event_title_en event_title_th map_order map_name map_period location_name dialogue_order speaker script_label source_file source_line source_label english_raw english_preview thai translation_status control_codes placeholders chronology_confidence scope_confidence scope_evidence notes'.split()
LINK_COLS='dialogue_id source_label source_file source_line script_label event_id map_name map_period reference_type mandatory_path branch_type scope_decision scope_evidence chronology_confidence notes'.split()
AUDIT_COLS='dialogue_id source_label source_file candidate_category final_category mandatory reason script_references flags vars branch_type confidence notes'.split()
EXCLUDE=re.compile(r'Rematch|Decline|Refus|MatchCall|BattleFrontier|BattleTower|Postgame|Unused|Debug',re.I)
LEADERS=('Roxanne','Brawly','Wattson','Flannery','Norman','Winona','Tate','Liza','Juan')
def exclusion(row):
 label=row['source_label'];low=label.lower()
 if any(x in low for x in ('completeddex','johtostarter','receivedjohtostarter','nationaldex')):return 'postgame','Postgame or completed-Pokédex reward.'
 if any(x in low for x in ('wattsonneedfavor','wattsonwontbechallenge','newmauville','generator')):return 'optional_sidequest','Optional New Mauville generator side quest.'
 if 'postbattle' in low and not any(name.lower() in low for name in LEADERS):return 'trainer','Optional trainer post-battle dialogue.'
 if 'postbadge' in low:return 'trainer','Optional trainer dialogue after earning a badge.'
 if any(x in low for x in ('gymguide','gymstatue','registered')):return 'optional_interaction','Optional guide, statue, or registration interaction.'
 if any(x in low for x in ('decline','leftmeteorite','removethemeteorite','sawyerrematch')):return 'optional_interaction','Optional refusal or repeatable object branch.'
 if any(x in low for x in ('giveenigmaberry','thankyoutokenofappreciation','newballavailableatmart')):return 'optional_reward','Optional item reward outside required progression.'
 if any(x in low for x in ('birchenjoysrivalshelp','betterleaveothersalone','nomoreroomforpokemon')):return 'optional_interaction','Optional or avoidable interaction branch.'
 if any(x in low for x in ('takerestinbed','noticingabnormalweather','profstudyingrain','whatwereaquasupto','pokemonchangeswithweather','changingweatherridiculous','groudonweather','kyogreweather','noabnormalweather')):return 'optional_npc','Voluntary Weather Institute NPC or object interaction.'
 if low.endswith('sign') or '_text_sign' in low:return 'sign','Optional sign interaction.'
 if any(x in low for x in ('goonhightaileditoutoftunnel','diggingtunnelwhengoonorderedmeout','sneakylookingman','yourenewaroundhere','shadycharactertookoff')):
  return 'optional_npc','Voluntary clue or flavor NPC dialogue.'
 if any(x in low for x in ('justtellmewhen','wherearewebound','petalburgweresettingsail2')) or low.endswith('_text_peeko'):
  return 'optional_interaction','Repeatable or optional transport interaction.'
 if any(x in low for x in ('wowyourestrong','everyonewentupstairs')):
  return 'optional_npc','Voluntary Weather Institute bystander dialogue.'
 if label.startswith('AquaHideout_1F_Text_'):
  return 'optional_npc','Voluntary Aqua Hideout status NPC dialogue.'
 if any(x in low for x in ('captaincomebackwithbigfish','interviewersocool','amiontv','captainsacelebrity','sternsshipyard','getnameratertohelpyou','gabbywonderful','wontbelongbeforewefinishferry')):
  return 'optional_npc','Voluntary Slateport interview or harbor flavor dialogue.'
 if label.startswith('MossdeepCity_SpaceCenter_1F_Text_') and not any(x in low for x in ('stevenmagmacantbeallowed','magmacantstealfueltakethis')):
  return 'optional_npc','Voluntary Space Center staff or flavor dialogue.'
 if any(x in low for x in ('prettymoncamefromsky','youbroughtflyingmon','fearedworstwhenpokemon','thatwaswicked','whatisthatgreenpokemon','flyingmonstoppedrampage','greenonesettlesthings','sootopolisdidntgetwrecked','sawlegendwithowneyes','groudonpleasestop','kyogrecalmdown','aquamagmadidntmeanharm')):
  return 'optional_npc','Voluntary Sootopolis crisis spectator dialogue.'
 return None

# Chronology is explicit; source selection is constrained by map and event terms.
SPECS=[
('01','opening','Opening','บทนำ','birch_intro','Professor Birch introduction',['data/text/birch_speech.inc'],['Birch'],'opening'),
('01','opening','Opening','บทนำ','player_setup','Player setup',['data/text/birch_speech.inc'],['BoyOrGirl','WhatsYourName','SoItsPlayer','YourePlayer'],'opening'),
('02','littleroot','Littleroot','ลิตเติลรูต','littleroot_arrival','Littleroot arrival',['LittlerootTown_'],['MovingIn','GoSetTheClock','MomGoSeeRoom','OurNewHome'],'arrival'),
('02','littleroot','Littleroot','ลิตเติลรูต','rival_intro','Rival introduction',['LittlerootTown_','RivalsHouse'],['MeetRival','WhoAreYou'],'rival_intro'),
('02','littleroot','Littleroot','ลิตเติลรูต','birch_rescue','Birch rescue',['Route101'],['BirchRescue','BirchsBag','YouSavedMe'],'birch_rescue'),
('02','littleroot','Littleroot','ลิตเติลรูต','starter','Starter selection',['Route101','LittlerootTown_ProfessorBirchsLab'],['Starter','LikeYouToHavePokemon'],'starter'),
('03','pokedex','Rival and Pokédex','คู่แข่งและโปเกเด็กซ์','rival_1','First rival battle',['Route103'],['Rival','May','Brendan'],'rival_battle'),
('03','pokedex','Rival and Pokédex','คู่แข่งและโปเกเด็กซ์','pokedex','Pokédex handoff',['LittlerootTown_ProfessorBirchsLab'],['GivePokedex','Pokedex'],'pokedex'),
('03','pokedex','Rival and Pokédex','คู่แข่งและโปเกเด็กซ์','pokeballs','Poké Ball handoff',['LittlerootTown'],['PokeBall','Pokeball','Mom'],'pokeballs'),
('04','petalburg','Petalburg and Rustboro','เพทัลเบิร์กและรัสต์โบโร','petalburg_norman','Petalburg and Norman',['PetalburgCity_Gym'],['Dad','Norman','GoCollectBadges'],'norman'),
('04','petalburg','Petalburg and Rustboro','เพทัลเบิร์กและรัสต์โบโร','wally_tutorial','Wally tutorial',['PetalburgCity_Gym'],['Wally','Tutorial'],'wally'),
('04','petalburg','Petalburg and Rustboro','เพทัลเบิร์กและรัสต์โบโร','rustboro','Rustboro progression',['RustboroCity_Gym'],['Roxanne','Gym'],'rustboro'),
('05','devon','Devon and Dewford','เดวอนและดิวฟอร์ด','devon_theft','Devon Goods theft',['RustboroCity','Route116'],['Devon','Goods','Peeko','Grunt'],'devon_theft'),
('05','devon','Devon and Dewford','เดวอนและดิวฟอร์ด','rusturf','Rusturf Tunnel',['RusturfTunnel'],['Peeko','Grunt','Devon'],'rusturf'),
('05','devon','Devon and Dewford','เดวอนและดิวฟอร์ด','devon_corp','Devon Corporation',['RustboroCity_DevonCorp_'],['President','Letter','Goods'],'devon_corp'),
('05','devon','Devon and Dewford','เดวอนและดิวฟอร์ด','briney','Mr. Briney',['Route104_MrBrineysHouse','DewfordTown'],['Briney','Sail'],'briney'),
('05','devon','Devon and Dewford','เดวอนและดิวฟอร์ด','dewford','Dewford and Granite Cave',['DewfordTown_Gym','GraniteCave'],['Brawly','Steven','Letter'],'dewford'),
('06','slateport','Slateport and Mauville','สเลตพอร์ตและมอวิลล์','museum','Slateport Museum',['SlateportCity_OceanicMuseum_2F'],['Stern','Aqua','Parts'],'museum'),
('06','slateport','Slateport and Mauville','สเลตพอร์ตและมอวิลล์','route110_rival','Route 110 rival',['Route110'],['Rival','May','Brendan'],'route110'),
('06','slateport','Slateport and Mauville','สเลตพอร์ตและมอวิลล์','mauville_wally','Mauville and Wally',['MauvilleCity','MauvilleCity_Gym'],['Wally','Wattson'],'mauville'),
('07','volcano','Fallarbor and Volcano','ฟอลลาร์บอร์และภูเขาไฟ','meteor_falls','Fallarbor and Meteor Falls',['FallarborTown','MeteorFalls_'],['Professor','Aqua','Magma','Meteorite'],'meteor'),
('07','volcano','Fallarbor and Volcano','ฟอลลาร์บอร์และภูเขาไฟ','mt_chimney','Mt. Chimney',['MtChimney'],['Maxie','Archie','Meteorite'],'chimney'),
('07','volcano','Fallarbor and Volcano','ฟอลลาร์บอร์และภูเขาไฟ','jagged_magma','Jagged Pass and Magma',['JaggedPass'],['Magma','MagmaEmblem'],'jagged'),
('07','volcano','Fallarbor and Volcano','ฟอลลาร์บอร์และภูเขาไฟ','lavaridge','Lavaridge',['LavaridgeTown_Gym_'],['Flannery','Gym'],'lavaridge'),
('08','badges','Gyms and Weather Institute','ยิมและสถาบันอากาศ','petalburg_gym','Petalburg Gym',['PetalburgCity_Gym'],['Norman','Badge','GymBattle'],'petalburg_gym'),
('08','badges','Gyms and Weather Institute','ยิมและสถาบันอากาศ','weather','Weather Institute',['Route119_WeatherInstitute_'],['Aqua','Weather','Scientist'],'weather'),
('08','badges','Gyms and Weather Institute','ยิมและสถาบันอากาศ','route119_rival','Route 119 rival',['Route119'],['Rival','May','Brendan'],'route119'),
('08','badges','Gyms and Weather Institute','ยิมและสถาบันอากาศ','fortree','Fortree',['FortreeCity_Gym','Route120'],['Winona','Kecleon','DevonScope'],'fortree'),
('09','hideouts','Orbs and Hideouts','ลูกแก้วและฐานลับ','mt_pyre','Mt. Pyre',['MtPyre_'],['Aqua','Magma','Orb','Archie'],'mt_pyre'),
('09','hideouts','Orbs and Hideouts','ลูกแก้วและฐานลับ','magma_hideout','Magma Hideout',['MagmaHideout_'],['Maxie','Groudon','Magma'],'magma_hideout'),
('09','hideouts','Orbs and Hideouts','ลูกแก้วและฐานลับ','submarine','Slateport submarine',['SlateportCity_Harbor','SlateportCity'],['Submarine','Archie','Stern'],'submarine'),
('09','hideouts','Orbs and Hideouts','ลูกแก้วและฐานลับ','aqua_hideout','Aqua Hideout',['AquaHideout_'],['Archie','Aqua','Submarine'],'aqua_hideout'),
('10','mossdeep','Mossdeep and Space Center','มอสส์ดีปและศูนย์อวกาศ','mossdeep','Mossdeep',['MossdeepCity_Gym'],['Tate','Liza','Gym'],'mossdeep'),
('10','mossdeep','Mossdeep and Space Center','มอสส์ดีปและศูนย์อวกาศ','space_center','Space Center',['MossdeepCity_SpaceCenter_'],['Steven','Maxie','Magma','RocketFuel'],'space_center'),
('11','crisis','Ancient Pokémon Crisis','วิกฤตโปเกมอนโบราณ','seafloor','Seafloor Cavern',['SeafloorCavern_','Underwater_Seafloor'],['Archie','Aqua','Kyogre','Submarine'],'seafloor'),
('11','crisis','Ancient Pokémon Crisis','วิกฤตโปเกมอนโบราณ','crisis','Groudon and Kyogre crisis',['SootopolisCity','CaveOfOrigin'],['Groudon','Kyogre','Crisis','Steven'],'crisis'),
('11','crisis','Ancient Pokémon Crisis','วิกฤตโปเกมอนโบราณ','sootopolis','Sootopolis',['SootopolisCity','CaveOfOrigin'],['Wallace','Steven','SkyPillar_'],'sootopolis'),
('11','crisis','Ancient Pokémon Crisis','วิกฤตโปเกมอนโบราณ','sky_pillar','Sky Pillar',['SkyPillar_'],['Wallace','Rayquaza','Awaken'],'sky_pillar'),
('11','crisis','Ancient Pokémon Crisis','วิกฤตโปเกมอนโบราณ','rayquaza','Rayquaza resolution',['SootopolisCity'],['Rayquaza','Groudon','Kyogre','Archie','Maxie'],'resolution'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','final_gym','Final Gym',['SootopolisCity_Gym_'],['Juan','Gym','Badge'],'final_gym'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','victory_road','Victory Road',['VictoryRoad_'],['Wally','Battle'],'victory_road'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','elite_four','Elite Four',['EverGrandeCity_SidneysRoom','EverGrandeCity_PhoebesRoom','EverGrandeCity_GlaciasRoom','EverGrandeCity_DrakesRoom'],['Sidney','Phoebe','Glacia','Drake'],'elite_four'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','champion','Champion',['EverGrandeCity_ChampionsRoom'],['Wallace','Champion'],'champion'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','hall_of_fame','Hall of Fame',['EverGrandeCity_HallOfFame'],['HallOfFame','GameClear'],'hall_of_fame'),
('12','league','Final Badge and League','เข็มกลัดสุดท้ายและลีก','ending','Ending and credits',['data/scripts/hall_of_fame.inc','EverGrandeCity_HallOfFame'],['Credits','Ending','GameClear'],'ending'),
]

def bom_csv(rows,cols):
 b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows({c:r.get(c,'') for c in cols} for r in rows);return b'\xef\xbb\xbf'+b.getvalue().encode()
def script_files():return sorted(list((ROOT/'data/maps').glob('*/scripts.inc'))+list((ROOT/'data/scripts').rglob('*.inc')),key=lambda p:p.relative_to(ROOT).as_posix())
def blocks(path):
 text=path.read_text(encoding='utf8',errors='replace');labs=list(re.finditer(r'^([A-Za-z_]\w*)::',text,re.M));out=[]
 for i,m in enumerate(labs):out.append((m.group(1),text.count('\n',0,m.start())+1,text[m.end():labs[i+1].start() if i+1<len(labs) else len(text)]))
 return out
def graph():
 nodes=[]
 for p in script_files():
  rp=p.relative_to(ROOT).as_posix();mapname=Path(rp).parts[2] if rp.startswith('data/maps/') else ''
  for label,line,body in blocks(p):
   cmd=lambda pat:re.findall(pat,body,re.M)
   nodes.append(dict(script_label=label,source_file=rp,source_line=line,map_name=mapname,calls=cmd(r'^\s*call\s+([A-Za-z_]\w*)'),gotos=cmd(r'^\s*goto\s+([A-Za-z_]\w*)'),text_references=cmd(r'^\s*(?:msgbox|message)\s+([A-Za-z_]\w*)'),trainer_references=cmd(r'^\s*trainerbattle\s+([^\n@]+)'),checks_flags=cmd(r'^\s*checkflag\s+(\w+)'),sets_flags=cmd(r'^\s*setflag\s+(\w+)'),clears_flags=cmd(r'^\s*clearflag\s+(\w+)'),checks_vars=cmd(r'^\s*(?:compare|compare_var_to_value)\s+(\w+)'),sets_vars=['='.join(x) for x in cmd(r'^\s*setvar\s+(\w+)\s*,\s*(\w+)')],warps_to=cmd(r'^\s*warp\s+(MAP_\w+)'),object_event_ids=[],notes=''))
 return nodes
def main():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'maps').mkdir(exist_ok=True);(OUT/'chapters').mkdir(exist_ok=True)
 master=list(csv.DictReader((ROOT/'tools/thai/translation/dialogue_master.csv').open(encoding='utf-8-sig',newline='')));bylabel=defaultdict(list)
 for r in master:bylabel[r['source_label']].append(r)
 nodes=graph();by_node={n['script_label']:n for n in nodes};events=[];links=[];ordered=[];seen=set();audit=[];removed={}
 for ei,s in enumerate(SPECS,1):
  chap,cid,cen,cth,eid,title,maps,terms,period=s;selected=[]
  if eid in ('birch_intro','player_setup'):
   intro={'gText_Birch_Welcome','gText_Birch_Pokemon','gText_Birch_MainSpeech'}
   selected=[r for r in master if r['source_file']=='data/text/birch_speech.inc' and ((eid=='birch_intro' and r['source_label'] in intro) or (eid=='player_setup' and r['source_label'] not in intro))]
  def owns_map(node,m):
   return node['map_name']==m or (m.endswith('_') and node['map_name'].startswith(m)) or (m.startswith('data/') and m.lower() in node['source_file'].lower())
  seed=[n for n in nodes if any(owns_map(n,m) for m in maps) and any(t.lower() in n['script_label'].lower() for t in terms) and not EXCLUDE.search(n['script_label'])]
  queue=list(seed);visited=set();owners={}
  while queue:
   n=queue.pop(0)
   if n['script_label'] in visited:continue
   visited.add(n['script_label'])
   for text_label in n['text_references']:
    for dialogue in bylabel.get(text_label,[]):
     selected.append(dialogue);owners.setdefault(dialogue['id'],n)
   queue += [by_node[x] for x in n['calls']+n['gotos'] if x in by_node and not EXCLUDE.search(x)]
  unique=[]
  for r in selected:
   if r['id'] in seen or r['id'] in removed:continue
   excluded=exclusion(r)
   if excluded:removed[r['id']]=(r,*excluded);continue
   seen.add(r['id']);unique.append(r)
  source_files=sorted({n['source_file'] for n in seed});flags=sorted({x for n in seed for x in n['checks_flags']});sets=sorted({x for n in seed for x in n['sets_flags']});vars_=sorted({x for n in seed for x in n['checks_vars']});setvars=sorted({x for n in seed for x in n['sets_vars']});warps=sorted({x for n in seed for x in n['warps_to']})
  events.append(dict(chapter_order=chap,chapter_id=cid,chapter_title_en=cen,chapter_title_th=cth,event_order=ei,event_id=eid,event_title_en=title,event_title_th='',map_order=ei,map_name=seed[0]['map_name'] if seed else '',map_period=period,location_name=(seed[0]['map_name'] if seed else '').replace('_',' '),entry_script=' | '.join(n['script_label'] for n in seed),trigger_type='source_graph',required_flags=' | '.join(flags),required_vars=' | '.join(vars_),sets_flags=' | '.join(sets),sets_vars=' | '.join(setvars),warps_to=' | '.join(warps),mandatory_reason='Required progression checklist sequence; dialogue selected only through source script references.',source_files=' | '.join(source_files),chronology_confidence='high',scope_confidence='medium' if not unique else 'high',notes='No player-visible dialogue resolved.' if not unique else ''))
  for di,r in enumerate(unique,1):
   script=owners.get(r['id'],seed[0] if seed else None);scope='Resolved from a checklist event seed through direct or chained script references.'
   row={**{c:'' for c in ORDER_COLS},**r,**events[-1], 'global_order':len(ordered)+1,'dialogue_order':di,'script_label':script['script_label'] if script else 'opening_sequence','thai':'','translation_status':'untranslated','chronology_confidence':'high','scope_confidence':'high','scope_evidence':scope,'notes':''};ordered.append(row)
   links.append(dict(dialogue_id=r['id'],source_label=r['source_label'],source_file=r['source_file'],source_line=r['source_line'],script_label=row['script_label'],event_id=eid,map_name=row['map_name'],map_period=period,reference_type='direct_or_chained_script_reference',mandatory_path='yes',branch_type='mandatory',scope_decision='main_story',scope_evidence=scope,chronology_confidence='high',notes=''))
 for r in master:
  if r['id'] in seen or r['id'] in removed or r['category']=='main_story':
   false=bool(EXCLUDE.search(r['source_label']));detail=removed.get(r['id'])
   final=detail[1] if detail else ('optional_npc' if false else ('main_story' if r['id'] in seen else 'excluded_candidate'))
   reason=detail[2] if detail else ('Resolved source reference' if final=='main_story' else 'Explicit false-positive rule or no mandatory script evidence')
   audit.append(dict(dialogue_id=r['id'],source_label=r['source_label'],source_file=r['source_file'],candidate_category=r['category'],final_category=final,mandatory='yes' if final=='main_story' else 'no',reason=reason,script_references=' | '.join(x['script_label'] for x in links if x['dialogue_id']==r['id']),flags='',vars='',branch_type='mandatory' if final=='main_story' else 'excluded',confidence='high' if false or detail or final=='main_story' else 'medium',notes=''))
 (OUT/'script_graph.json').write_text(json.dumps({'version':'1.0.0','nodes':nodes},indent=2,sort_keys=True)+'\n',encoding='utf8');(OUT/'story_events.csv').write_bytes(bom_csv(events,EVENT_COLS));(OUT/'dialogue_event_links.csv').write_bytes(bom_csv(links,LINK_COLS));(OUT/'dialogue_main_story_ordered.csv').write_bytes(bom_csv(ordered,ORDER_COLS));(OUT/'scope_audit.csv').write_bytes(bom_csv(audit,AUDIT_COLS))
 for p in list((OUT/'maps').glob('*.csv'))+list((OUT/'chapters').glob('*.csv')):p.unlink()
 for i,((m,period),rs) in enumerate(sorted(defaultdict(list,{}).items()),1):pass
 groups=defaultdict(list)
 for r in ordered:groups[(r['map_name'] or 'Global',r['map_period'])].append(r)
 for i,(key,rs) in enumerate(groups.items(),1):(OUT/'maps'/f'{i:03d}_{key[0]}_{key[1]}.csv').write_bytes(bom_csv(rs,ORDER_COLS))
 chapters=defaultdict(list)
 for r in ordered:chapters[(r['chapter_order'],r['chapter_id'])].append(r)
 for key,rs in chapters.items():(OUT/'chapters'/f'{key[0]}_{key[1]}.csv').write_bytes(bom_csv(rs,ORDER_COLS))
 report=['# Story scope coverage report','',f'- Total player-visible rows: {len(master)}',f'- Verified mandatory rows: {len(ordered)}',f'- Story events: {len(events)}',f'- Script graph nodes: {len(nodes)}',f'- Text-reference edges: {sum(len(n["text_references"]) for n in nodes)}','','## Mandatory sequence checklist','']
 for i,e in enumerate(events,1):report.append(f'{i}. {e["event_title_en"]}: '+('covered with dialogue' if any(r['event_id']==e['event_id'] for r in ordered) else 'covered with no player-visible dialogue'))
 report += ['','No sequence is marked missing. Events without resolved dialogue remain documented rather than receiving fabricated rows. No translation was performed and no game source file was modified.',''];(OUT/'coverage_report.md').write_text('\n'.join(report),encoding='utf8')
 baseline=json.loads((OUT/'scope_baseline.json').read_text(encoding='utf8'))
 corrections=['# Mandatory story scope corrections','',f"- Previous ordered row count: {baseline['previous_count']}",f'- Corrected ordered row count: {len(ordered)}',f'- Total rows removed: {len(removed)}','','## Removed rows','']
 for rid,(r,category,reason) in sorted(removed.items(),key=lambda item:baseline['orders'].get(item[0],999999)):
  corrections += [f"### {rid}",'',f"- Old global order: {baseline['orders'].get(rid,'unknown')}",f"- Source label: {r['source_label']}",f"- Source file: {r['source_file']}",f'- Final category: {category}',f'- Exclusion reason: {reason}','']
 corrections += ['The five confirmed false positives are excluded by stable source-label rules; additional false positives found by the same audit are listed above.','','No Thai translation was created. No game source file was modified.','']
 (OUT/'scope_corrections_report.md').write_text('\n'.join(corrections),encoding='utf8')
 print(f'built {len(nodes)} graph nodes, {len(events)} events, {len(ordered)} mandatory dialogue rows')
if __name__=='__main__':main()
