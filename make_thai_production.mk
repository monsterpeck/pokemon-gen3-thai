.PHONY: thai-production-font check-thai-production-font thai-production-proof

THAI_PRODUCTION_PYTHON := PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B

thai-production-font:
	$(THAI_PRODUCTION_PYTHON) tools/thai/shape_thai_production.py --build-font --check

check-thai-production-font: build/assets/graphics/fonts/thai_shaped.png.latfont
	$(THAI_PRODUCTION_PYTHON) tools/thai/shape_thai_production.py --check
	$(THAI_PRODUCTION_PYTHON) tools/thai/thai_production_artifacts.py

thai-production-proof:
	$(THAI_PRODUCTION_PYTHON) tools/thai/render_thai_proof.py
	$(THAI_PRODUCTION_PYTHON) tools/thai/compare_proof_production.py
	$(THAI_PRODUCTION_PYTHON) tools/thai/thai_production_artifacts.py
