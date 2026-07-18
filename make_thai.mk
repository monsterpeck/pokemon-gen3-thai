include make_thai_production.mk
.PHONY: thai-noto-font check-thai-noto-font thai-noto-proof test-thai-shaped-text

thai-noto-font:
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/rasterize_noto_thai.py
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/extract_noto_thai_metrics.py
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/shape_thai_production.py --build-font --check

check-thai-noto-font:
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B -m unittest tools.thai.tests.test_noto_font_engineering -v

thai-noto-proof:
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/render_thai_proof.py
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/compare_proof_production.py
.PHONY: thai-review-sheet check-thai-review-sheet import-thai-review-sheet test-thai-menu test-thai-renderer check-thai-combining

thai-review-sheet:
	python3 -B tools/thai/export_review_sheet.py

check-thai-review-sheet:
	python3 -B tools/thai/import_review_sheet.py --check

import-thai-review-sheet:
	python3 -B tools/thai/import_review_sheet.py
	python3 -B tools/thai/build_thai_font.py
	python3 -B tools/thai/validate_thai_font.py

test-thai-renderer:
	python3 -B tools/thai/validate_combining_renderer.py
	python3 -B -m unittest discover -s tools/thai/tests -p "test_combining*.py"

test-thai-menu:
	python3 -B tools/thai/validate_combining_renderer.py
	python3 -B -m unittest discover -s tools/thai/tests -p "test_combining*.py"

check-thai-combining:
	python3 -B tools/thai/validate_combining_renderer.py

test-thai-shaped-text: build/assets/graphics/fonts/thai_shaped.png.latfont
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B -m unittest tools.thai.tests.test_build_time_shaping -v
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/shape_thai_production.py --check
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/runtime_glyph_trace.py
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/thai_production_artifacts.py
	PYTHONPATH=tools/thai/cache/python:tools/thai python3 -B tools/thai/build_time_shaping_report.py