.PHONY: thai-review-sheet check-thai-review-sheet import-thai-review-sheet test-thai-menu

thai-review-sheet:
	python3 -B tools/thai/export_review_sheet.py

check-thai-review-sheet:
	python3 -B tools/thai/import_review_sheet.py --check

import-thai-review-sheet:
	python3 -B tools/thai/import_review_sheet.py
	python3 -B tools/thai/build_thai_font.py
	python3 -B tools/thai/validate_thai_font.py

test-thai-menu:
	python3 -B tools/thai/test_thai_menu.py
