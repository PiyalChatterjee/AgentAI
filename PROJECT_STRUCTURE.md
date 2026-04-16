# AgentAI Project Structure

## Overview
21-day AI Engineer Core Track using interactive learning with OpenAI/Azure OpenAI APIs.

---

## Folder Organization

### 📁 `day_01/` — Day 1: OpenAI API & System Prompts
**Status:** ✅ Complete

**Files:**
- `DAY_01_NOTES.md` — Comprehensive learning notes (Q1-Q4 + Activities A1-A6)
- `day1_chatbot.py` — 3-prompt comparison chatbot (Friendly Teacher, Technical Expert, Product Manager)
- `day1_results.json` — Saved API responses from chatbot run
- `token_utils.py` — Token counter utility with cost estimation & offline fallback

**Key Concepts Covered:**
- Q1: How the OpenAI API works
- Q2: System prompts and their structure
- Q3: How to structure an API call in Python
- Q4: Tokenization and cost management

**How to run:**
```bash
cd day_01
python day1_chatbot.py friendly_teacher
python token_utils.py -t "Your text here" -p 0.0001
```

---

### 📁 `day_XX/` — Future Days (Day 2+)
Placeholder for upcoming days. Each day will follow the same pattern:
- `DAY_XX_NOTES.md` — Concept questions and activities
- Day-specific scripts and outputs
- Results/artifact files

---

### 📁 `docs/` — Documentation & Planning
**Contains:**
- `COURSE_DAILY_SCHEDULE.md` — Overall 21-day schedule and roadmap
- `ROADMAP_AI_AGENTIC.md` — Detailed learning objectives and project goals
- `DAILY_CHECKIN_TEMPLATE.md` — Daily progress metrics and reflections

**Purpose:** High-level course structure, planning, and progress tracking (not day-specific).

---

### 📁 `shared/` — Shared Utilities & Config
**For future use:** Common utilities, helper functions, or configurations shared across multiple days.

**Examples (future):**
- `utils/` — Shared Python utilities
- `.env` (root-level, shared) — Azure OpenAI credentials

---

### 🔧 Root Level Files
- `.env` — Azure OpenAI API credentials & configuration
- `.venv/` — Python virtual environment
- `.git/` — Git repository
- `README.md` — Project overview
- `lab1.py` — Legacy/reference lab file
- `DAY_01_PLAN.md` — Initial day plan (reference)

---

## Navigation Examples

**View Day 1 learning notes:**
```
open day_01/DAY_01_NOTES.md
```

**Run Day 1 chatbot:**
```bash
cd day_01
python day1_chatbot.py friendly_teacher
```

**Check course schedule:**
```
open docs/COURSE_DAILY_SCHEDULE.md
```

**See daily progress:**
```
open docs/DAILY_CHECKIN_TEMPLATE.md
```

---

## Git Status
Commit: Day 1 Complete (hash: 23e1bff)  
All files tracked and organized by folder.

---

## Next Steps
- Day 2: Model Comparison & Architecture (when ready)
- Add Day 2 folder with similar structure
- Maintain docs/ folder for course-level planning
