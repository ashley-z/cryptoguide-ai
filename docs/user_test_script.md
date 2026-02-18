# CryptoGuide AI — User Testing Script

## Overview

**Objective:** Validate that CryptoGuide AI reduces protocol research time by 90% (5 hours → 30 minutes) with high user satisfaction.

**Participants:** 5 users
- 3 "Crypto-Curious Professionals" (familiar with finance, new to DeFi)
- 2 "DeFi Power Users" (active DeFi users across multiple protocols)

**Duration:** ~25 minutes per session

---

## Pre-Session Setup

1. Ensure backend is running: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
2. Ensure frontend is running: `cd frontend && npm run dev`
3. Open http://localhost:5173 in a clean browser tab
4. Prepare a stopwatch for timed tasks
5. Have the post-session survey ready

---

## Introduction Script (2 min)

> *"Thanks for helping me test CryptoGuide AI! This is an AI-powered research assistant that helps you understand DeFi protocols like Aave, Compound, and Uniswap. I'm going to give you a few tasks and ask you to think aloud as you work through them. There are no wrong answers — I'm testing the product, not you."*

---

## Timed Tasks

### Task 1: Single Protocol Query (Target: <2 min)

**Instruction to participant:**
> *"Using this tool, find out what collateral requirements Aave has for USDC lending."*

**What to observe:**
- [ ] Did they select the correct protocol (Aave)?
- [ ] Did they phrase the question clearly?
- [ ] Did they read the sources/citations?
- [ ] Time to complete: _____ seconds
- [ ] Any confusion or hesitation?

**Notes:** _______________________________________________

---

### Task 2: Comparison Mode (Target: <3 min)

**Instruction to participant:**
> *"Now, compare how liquidation penalties work in Aave vs Compound."*

**What to observe:**
- [ ] Did they discover the Compare button?
- [ ] Did they select the correct protocols?
- [ ] Did they understand the comparison answer?
- [ ] Did they notice protocol badges on sources?
- [ ] Time to complete: _____ seconds
- [ ] Any confusion or hesitation?

**Notes:** _______________________________________________

---

### Task 3: Concept Explanation (Target: <2 min)

**Instruction to participant:**
> *"Switch to Uniswap and ask the tool to explain how concentrated liquidity works in simple terms."*

**What to observe:**
- [ ] Did they switch protocols correctly?
- [ ] Did they exit compare mode (if active)?
- [ ] Was the explanation understandable to them?
- [ ] Did they expand any source cards?
- [ ] Time to complete: _____ seconds
- [ ] Any confusion or hesitation?

**Notes:** _______________________________________________

---

## Post-Session Survey

### Quantitative (1-5 scale)

| Question | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| How helpful was CryptoGuide AI? | | | | | |
| How much do you trust the AI's answers? | | | | | |
| How likely are you to use this again? | | | | | |
| How easy was it to use? | | | | | |
| How professional does the UI look? | | | | | |

### Qualitative

1. What was the most useful feature?
2. What was the most confusing part?
3. What would you change or add?
4. Would you prefer this over reading documentation directly? Why?
5. Any other thoughts?

---

## Success Criteria

- [ ] **4/5 users** complete all tasks in <30 minutes total
- [ ] **4/5 users** rate helpfulness ≥4/5
- [ ] **Collect 10+** qualitative insights for iteration
- [ ] Identify top 3-5 issues for immediate fixes

---

## Post-Testing Action Items

| Priority | Issue | Fix |
|---|---|---|
| P0 | ___________________ | ___________________ |
| P1 | ___________________ | ___________________ |
| P2 | ___________________ | ___________________ |
| P3 | ___________________ | ___________________ |
| P4 | ___________________ | ___________________ |
