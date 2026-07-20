# แผนงาน Pokémon Emerald ภาษาไทย

อัปเดตสถานะจากงานล่าสุด เพื่อใช้ต่อเมื่อ Codex พร้อม

## 1. เป้าหมายของโครงการ

สร้าง Pokémon Emerald ภาษาไทยโดยดำเนินงานตามลำดับนี้:

1. จัดฐานข้อมูลบทพูดเนื้อเรื่องหลักให้ครบและเรียงตามเหตุการณ์
2. แปลบทพูดเป็นภาษาไทย พร้อม Glossary และ Translation Memory
3. ตรวจคำแปลทีละแผนที่และ Chapter
4. Inject คำแปลกลับเข้า Source
5. Build ROM และทดสอบในเกม
6. กลับมาแก้คุณภาพฟอนต์และระบบชื่อโปเกมอนใน Runtime

นโยบายชื่อโปเกมอนของโครงการ:

> ใช้ชื่อภาษาไทยที่ถอดเสียงจากชื่อญี่ปุ่นตามไฟล์อ้างอิง

ตัวอย่าง:

- BULBASAUR → フシギダネ → ฟุชิกิดาเนะ
- CHARMANDER → ヒトカゲ → ฮิโตคาเงะ
- TREECKO → キモリ → คิโมริ

---

## 2. สถานะงานที่เสร็จแล้ว

### 2.1 ระบบข้อความภาษาไทย

ทำระบบ Build-time Thai shaping แล้ว:

- Unicode Thai source
- HarfBuzz shaping ตอน Build
- Compact shaped glyph IDs
- Positioned glyph commands
- Runtime renderer สำหรับ Thai positioned glyphs

ระบบคำสั่งและการฝัง Font เข้า ROM ทำงานแล้ว แต่คุณภาพการแสดงผลตัวอักษรบางตัว เช่น `ร` และ `ส` ยังไม่สมบูรณ์ใน Emulator

สถานะ:

> พักงานฟอนต์ไว้ก่อน เพื่อไม่ให้วนแก้ปัญหาเดิมโดยไม่มีหลักฐานใหม่

### 2.2 การดึงบทพูด

สร้างเครื่องมือดึงข้อความจาก Source แล้ว ครอบคลุม:

- Assembly `.string`
- C strings
- Control codes
- Placeholders
- Source labels
- Source lines
- Script references

### 2.3 ฐานข้อมูลเนื้อเรื่องหลัก

ตรวจ Scope และลำดับเหตุการณ์เรียบร้อยแล้ว:

- บทพูดเนื้อเรื่องหลัก: 261 รายการ
- เหตุการณ์หลัก: 45 เหตุการณ์
- Optional/Postgame ที่ถอดออก: 173 รายการ
- Map-period files: 43 ไฟล์
- Chapter files: 12 ไฟล์
- Global order: 1–261 ต่อเนื่อง
- ID ไม่ซ้ำ
- ทุกแถวเชื่อมกับ Event
- ไม่มี Mandatory sequence ที่ Missing
- Generation ซ้ำแล้วได้ไฟล์ Byte-identical
- Thai fields ยังว่างทั้งหมด
- Translation status ยังเป็น `untranslated`

ไฟล์หลัก:

```text
tools/thai/translation/story_order/
├── dialogue_main_story_ordered.csv
├── story_events.csv
├── dialogue_event_links.csv
├── scope_audit.csv
├── coverage_report.md
├── scope_corrections_report.md
├── script_graph.json
├── maps/
└── chapters/
```

### 2.4 ไฟล์ชื่อโปเกมอน

ไฟล์อ้างอิงมี 412 แถว:

- Active species names: 386 รายการ
- System reserved: 26 รายการ
- `LOCKED_GLOSSARY`: 75 รายการ
- `TRANSLATED_DRAFT`: 310 รายการ
- `NEEDS_REVIEW_GLOSSARY_CHANGE`: 1 รายการ

ชื่อไทยทั้งหมดอิงชื่อญี่ปุ่น

ข้อจำกัดที่ยังค้าง:

- ยังต้องสร้าง English species name → Internal species ID → Japanese → Thai cross-reference
- ชื่อไทยยาวเกิน Fixed entry 6 bytes
- Runtime species-name table ยังต้องใช้ Pointer Hook หรือ Relocation ในภายหลัง

### 2.5 Prompt แปล

มี Prompt สำหรับแปลเนื้อเรื่องหลัก 261 รายการแล้ว และมีฉบับปรับปรุงที่เพิ่มนโยบายชื่อโปเกมอนอิงภาษาญี่ปุ่น

---

## 3. งานเตรียมก่อน Codex พร้อม

### 3.1 เก็บ Checkpoint ของฐานข้อมูลเนื้อเรื่อง

รันใน Ubuntu/WSL Terminal:

```bash
cd ~/dev/projects/pokeemerald || exit 1

git status --short
git diff --check
make check-story-scope
make test-story-scope
```

เมื่อผลผ่าน ให้ Commit เฉพาะฐานข้อมูลและเครื่องมือ Scope ก่อนเริ่มงานแปล

ตัวอย่าง:

```bash
cd ~/dev/projects/pokeemerald || exit 1

git add   Makefile   tools/thai/extract_dialogue.py   tools/thai/validate_story_scope.py   tools/thai/tests/test_dialogue_extraction.py   tools/thai/tests/test_story_scope_and_chronology.py   tools/thai/translation/story_order

git commit -m "Finalize mandatory Emerald story dialogue scope"
```

ก่อน Commit ให้ตรวจว่าไม่มี Probe หรือไฟล์ทดลองฟอนต์ที่ไม่ต้องการปะปนอยู่

### 3.2 วางไฟล์ชื่อโปเกมอนในโปรเจกต์

ตำแหน่งเป้าหมาย:

```text
tools/thai/translation/reference/species_names_th.csv
```

สร้างโฟลเดอร์:

```bash
cd ~/dev/projects/pokeemerald || exit 1
mkdir -p tools/thai/translation/reference
```

จากนั้นดาวน์โหลดไฟล์ CSV จาก ChatGPT และคัดลอกเข้าโฟลเดอร์ดังกล่าว โดยเปลี่ยนชื่อเป็น:

```text
species_names_th.csv
```

ตรวจไฟล์:

```bash
cd ~/dev/projects/pokeemerald || exit 1

python3 - <<'PY'
import csv
from pathlib import Path

path = Path("tools/thai/translation/reference/species_names_th.csv")

with path.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

print("rows:", len(rows))
print("headers:", list(rows[0]) if rows else [])
print("reserved:", sum(r["status"] == "SYSTEM_RESERVED" for r in rows))
print("locked:", sum(r["status"] == "LOCKED_GLOSSARY" for r in rows))
print("draft:", sum(r["status"] == "TRANSLATED_DRAFT" for r in rows))
print(
    "review:",
    sum(r["status"] == "NEEDS_REVIEW_GLOSSARY_CHANGE" for r in rows),
)
PY
```

ค่าที่คาดหวัง:

```text
rows: 412
reserved: 26
locked: 75
draft: 310
review: 1
```

### 3.3 ตรวจว่าโฟลเดอร์ Translation ยังไม่ถูกสร้างแบบค้างครึ่ง

```bash
cd ~/dev/projects/pokeemerald || exit 1

find tools/thai/translation/story_order/translation   -maxdepth 3 -type f 2>/dev/null | sort
```

ก่อนเริ่มรอบจริงควรไม่มี Partial Batch จากรอบที่ Codex หยุด

หากมีไฟล์ Partial ห้ามลบทันที ให้ย้ายออกไปสำรองก่อน:

```bash
cd ~/dev/projects/pokeemerald || exit 1

if [ -d tools/thai/translation/story_order/translation ]; then
    mv       tools/thai/translation/story_order/translation       tools/thai/translation/story_order/translation_before_full_run
fi
```

ทำเฉพาะเมื่อยืนยันว่าเป็นไฟล์ค้างและยังไม่ได้ตรวจรับ

---

## 4. งานถัดไปเมื่อ Codex พร้อม

### Phase A — ตรวจ Reference และสร้าง Species Cross-reference

เป้าหมาย:

- อ่าน `species_names_th.csv`
- อ่าน English species table ใน pokeemerald
- เชื่อมด้วย Internal Species ID
- สร้างตารางตรวจสอบ English → Japanese → Thai
- ไม่แก้ Source เกม
- ไม่แปลบทพูด

ผลลัพธ์แนะนำ:

```text
tools/thai/translation/reference/
├── species_names_th.csv
├── species_names_cross_reference.csv
└── species_names_cross_reference_report.md
```

เกณฑ์ผ่าน:

- Active species ทุกตัวมี English mapping หนึ่งรายการ
- ไม่มี Species ID ซ้ำ
- Reserved rows ไม่ถูกนำไปใช้
- ชื่อไทยตรงกับ `translation_th`
- Index 80 ถูกทำเครื่องหมาย Review

Phase นี้เป็นงานขนาดเล็กกว่า Full translation และเหมาะสำหรับใช้ตรวจระบบก่อน

### Phase B — แปลเนื้อเรื่องหลัก 261 รายการ

ใช้ Prompt:

```text
codex_prompt_translate_emerald_main_story_261_with_japanese_species_names.md
```

ผลลัพธ์หลัก:

```text
tools/thai/translation/story_order/translation/
├── dialogue_main_story_thai.csv
├── glossary.csv
├── translation_memory.csv
├── speaker_style_guide.csv
├── main_story_length_review.csv
├── translation_progress.json
├── main_story_translation_report.md
├── batches/
├── maps/
├── chapters/
└── reviews/
```

เกณฑ์ผ่าน:

- 261 แถวครบ
- Global order 1–261
- Thai ไม่ว่างทุกแถว
- Status = `draft_review`
- Placeholder และ Control code ไม่เปลี่ยน
- Glossary ไม่มี English key ซ้ำ
- ชื่อโปเกมอนใช้จาก CSV เท่านั้น
- Map และ Chapter splits รวมกันตรงกับ Master
- Tests และ Validator ผ่าน

### Phase C — Human Review

ตรวจตามลำดับ:

1. `main_story_translation_report.md`
2. `glossary.csv`
3. `reviews/main_story_translation_review.md`
4. `main_story_length_review.csv`
5. `dialogue_main_story_thai.csv`

หัวข้อที่ต้องตรวจ:

- ชื่อคน
- ชื่อโปเกมอน
- ชื่อเมืองและสถานที่
- Team Aqua / Team Magma
- คำเรียกตำแหน่ง
- สรรพนามและบุคลิกตัวละคร
- ประโยคยาว
- Control codes
- Placeholder
- สำนวนที่แปลตรงตัวเกินไป

สถานะ Glossary:

- `locked` = ห้ามเปลี่ยนโดยไม่อนุมัติ
- `draft` = ใช้เป็นคำหลักชั่วคราว
- `review` = ต้องตัดสินใจก่อน Inject

### Phase D — Inject กลับเข้า Source

ทำหลัง Human Review ผ่านเท่านั้น

เป้าหมาย:

- สร้าง Injector จาก Stable ID และ Source label
- สำรอง English source
- Inject เฉพาะรายการที่อนุมัติ
- รักษา Control codes และ Placeholders
- ตรวจ Source diff
- ยังไม่แตะข้อความ Optional/NPC

ต้องมี Dry-run report ก่อนเขียนจริง

### Phase E — Build ROM และทดสอบ

หลัง Inject:

- Build ROM
- ทดสอบฉากเปิดเกม
- ทดสอบเปลี่ยนหน้า
- ทดสอบ Placeholder
- ทดสอบข้อความหลายบรรทัด
- ทดสอบบทพูดชื่อโปเกมอน
- ทดสอบ Save/Load
- ตรวจ Regression ภาษาอังกฤษส่วนที่ยังไม่แปล

### Phase F — กลับมาแก้ฟอนต์

งานค้าง:

- ตัวฐานบางตัว เช่น `ร` และ `ส` แสดงไม่สมบูรณ์
- ต้องตรวจจากหลักฐาน Runtime ใหม่ ไม่วนปรับ Bitmap แบบเดิม
- ทดสอบด้วยข้อความจริงจาก Batch ที่แปลแล้ว
- แก้เฉพาะเมื่อมี Reproduction ที่สั้นและชัดเจน

### Phase G — Species Name Runtime Hook

งานค้าง:

- ตารางชื่อโปเกมอนเดิมจำกัด 6 bytes
- ชื่อไทยทั้งหมดเกิน Fixed entry ปัจจุบัน
- ต้องออกแบบ Pointer Hook หรือ Relocation
- ต้องรองรับชื่อใน:
  - Party
  - Battle
  - Pokédex
  - Summary
  - PC
  - Script placeholders

แยกงานนี้ออกจากการแปล Dialogue เพื่อไม่ให้สองระบบรบกวนกัน

---

## 5. ลำดับความสำคัญ

### พร้อมทำทันทีโดยไม่ใช้ Codex มาก

1. ดาวน์โหลดและวาง `species_names_th.csv`
2. ตรวจจำนวนแถวและสถานะ
3. Commit Story Scope checkpoint
4. ตรวจว่าไม่มี Partial translation
5. เก็บ Prompt ฉบับล่าสุดไว้

### ทำเมื่อ Codex quota พร้อม

1. Species cross-reference
2. Full translation 261 rows
3. Validation และ Review files
4. Human review
5. Injection tool
6. ROM build

### ยังไม่ทำตอนนี้

- แก้ฟอนต์ `ร` และ `ส` ต่อ
- Inject ชื่อโปเกมอนลง Fixed table
- Build ROM ก่อนตรวจคำแปล
- แปล Optional NPC ทั้งหมด
- แปล Menu/Battle/Item text

---

## 6. Definition of Done สำหรับ Milestone แปลเนื้อเรื่อง

Milestone นี้ถือว่าเสร็จเมื่อ:

- บทพูด 261 รายการมีคำแปลไทยครบ
- Glossary ครบและไม่มีคำสะกดสลับ
- ชื่อโปเกมอนอิงภาษาญี่ปุ่นตาม CSV
- Translation Memory ถูกสร้าง
- Speaker Style Guide ถูกสร้าง
- Control codes และ Placeholders ผ่าน Validator
- Map และ Chapter review ครบ
- รายการ `review` ถูกตรวจโดยมนุษย์
- ยังไม่ได้ Inject หรือ Build ROM โดยไม่ได้รับอนุมัติ
