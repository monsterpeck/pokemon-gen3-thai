import csv, hashlib, subprocess, unittest
from tools.thai import build_story_scope as build
class Tests(unittest.TestCase):
    def test_assembly_boundaries(self):
        from tools.thai import extract_dialogue as ex
        rows=ex.parse_assembly('A::\n.string "a\\p"\n.string "b$"\nB::\n.string "c$"\n')
        self.assertEqual([r['raw'] for r in rows],['a\\pb$','c$'])
    def test_graph_edges_and_stability(self):
        first=build.graph(); self.assertEqual(first,build.graph())
        route_nodes=[n for n in first if n['source_file']=='data/maps/Route101/scripts.inc']
        self.assertTrue(any(n['sets_flags'] for n in route_nodes))
        self.assertTrue(any(n['sets_vars'] for n in route_nodes))
    def test_explicit_exclusions(self):
        self.assertTrue(build.EXCLUDE.search('MtChimney_EventScript_SawyerRematch'))
        self.assertTrue(build.EXCLUDE.search('DeclineRide'))
    def test_optional_and_postgame_regressions(self):
        excluded=['LittlerootTown_ProfessorBirchsLab_Text_CompletedDexChoosePokemon','LittlerootTown_ProfessorBirchsLab_Text_ReceivedJohtoStarter','RustboroCity_Gym_Text_GymGuideAdvice','RustboroCity_Gym_Text_GymStatue','MauvilleCity_Text_WattsonNeedFavorTakeKey','MtChimney_EventScript_SawyerRematch','SomeTrainerPostBattle']
        self.assertTrue(all(build.exclusion({'source_label':label}) for label in excluded))
        self.assertIsNone(build.exclusion({'source_label':'RustboroCity_Gym_Text_RoxannePostBattle'}))
        self.assertIsNone(build.exclusion({'source_label':'RustboroCity_Gym_Text_ReceivedStoneBadge'}))
    def test_splits_and_repeat_bytes(self):
        subprocess.run(['python3','-B','tools/thai/build_story_scope.py'],cwd=build.ROOT,check=True)
        def rows(p):
            with p.open(encoding='utf-8-sig',newline='') as handle:
                return list(csv.DictReader(handle))
        master=rows(build.OUT/'dialogue_main_story_ordered.csv'); ids={r['id'] for r in master}
        self.assertEqual(len(ids),len(master)); self.assertTrue(all(not r['thai'] for r in master))
        self.assertEqual([int(r['global_order']) for r in master],list(range(1,len(master)+1)))
        self.assertEqual(ids,{r['id'] for p in (build.OUT/'maps').glob('*.csv') for r in rows(p)})
        self.assertEqual(ids,{r['id'] for p in (build.OUT/'chapters').glob('*.csv') for r in rows(p)})
        one={p.relative_to(build.OUT):hashlib.sha256(p.read_bytes()).digest() for p in build.OUT.rglob('*') if p.is_file()}
        subprocess.run(['python3','-B','tools/thai/build_story_scope.py'],cwd=build.ROOT,check=True)
        two={p.relative_to(build.OUT):hashlib.sha256(p.read_bytes()).digest() for p in build.OUT.rglob('*') if p.is_file()}
        self.assertEqual(one,two)
if __name__=='__main__': unittest.main()
