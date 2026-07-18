.PHONY: thai-glyph-candidates install-thai-candidate

thai-glyph-candidates:
	python3 -B tools/thai/generate_glyph_candidates.py

install-thai-candidate:
	@test -n "$(CANDIDATE)" || (echo "CANDIDATE is required, e.g. CANDIDATE=V03" && exit 2)
	python3 -B tools/thai/install_glyph_candidate.py $(CANDIDATE)
