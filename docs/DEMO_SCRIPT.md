# 90-Second Demo Script — CarbonVerifier

Setup before stepping up:
- Slide deck open in browser fullscreen at `docs/deck/index.html`
- Streamlit app running: `uv run streamlit run app.py` → `http://localhost:8501`
- Browser tab pre-loaded with the dashboard, **VCS-981 Cikel** selected

The cadence: **6 slides + 2 live-app moments**, totalling ~90 seconds. Slide jumps are keyboard `1`–`8`; advance with `→`.

---

## [SLIDE 1 — TITLE] · 0:00–0:08 · 8s

> *"This is CarbonVerifier — a satellite-verified audit tool for the voluntary carbon credit market."*

**Action:** Pause one beat on the title screen. Let the dot pulse.

---

## [SLIDE 2 — THE PROBLEM] · 0:08–0:23 · 15s

> *"In 2023, journalists exposed that 90%+ of Verra's Amazon rainforest carbon credits were phantom. Microsoft, Disney, Shell, Salesforce — all bought them. The voluntary carbon market is two billion dollars a year. There has been no good way for buyers to know if what they bought is real."*

**Action:** Hold on the four stats grid for the closing line.

---

## [SLIDE 3 — THE PIPELINE] · 0:23–0:33 · 10s

> *"Four steps. Boundary. Satellite. Analysis. Claude. Generative AI is the central reasoning layer — not a chatbot wrapper."*

**Action:** Trace the four cards left-to-right with your hand or cursor as you say the four words.

---

## [LIVE APP — Map + KPI strip] · 0:33–0:52 · 19s

**Switch to Streamlit tab.** Project should already be VCS-981 Cikel.

> *"Pick a project. Cikel Brazilian Amazon, Verra ID 981. Microsoft is the named buyer. Twenty-thousand hectares of forest in 2000."*

**Action:** Point to the FOREST 2000 KPI cell.

> *"Eight thousand three hundred sixty-seven hectares lost during the credit-issuance period. Thirty-nine point nine percent."*

**Action:** Point to POST-START LOSS, then to the CRITICAL pill in ADDITIONALITY VERDICT.

> *"Negative additionality. The project area lost more forest than nearby unprotected land. Now watch the satellite."*

**Action:** Click the **TIME-LAPSE** tab. Let the GIF play one cycle (~7 seconds).

---

## [SLIDE 5 — THREE VOICES] · 0:52–1:12 · 20s

**Switch back to the slide deck. Press `5`.**

> *"Same satellite evidence. Three Claude reports. Same numbers, three audiences."*

**Action:** Trace the three cards left-to-right.

> *"For Microsoft's sustainability lead — a 1-page brief with risk rating and recommended action: write down, do not retire."*
>
> *"For an investigative journalist — a 600-word narrative, naming only the buyers in the data, citing every number to its satellite source."*
>
> *"For a Verra compliance auditor — a regulatory brief flagging Standard 3.4 additionality with a recommended credit-invalidation."*

---

## [SLIDE 6 — TWO MORE CASES] · 1:12–1:25 · 13s

**Press `6`.**

> *"Two more cases. ADPML — the forest is still standing, but Verra suspended the project for land-grabbing. Satellites verify cover; they can't verify consent. Cordillera Azul — only zero-point-six percent loss, but the park was already legally protected. The credits exist more in the baseline than in reality."*

**Action:** Touch each case card as you describe it. End on Cordillera Azul.

---

## [SLIDE 7 — THESIS] · 1:25–1:32 · 7s

**Press `7`.**

> *"Generative AI as accountability infrastructure for the largest greenwashing market on earth. Built in four days. Public repo."*

---

## Total: 1:32 (~92 seconds)

Trim points if running long:
- Drop slide 6 (case studies) → saves 13s, lands at 79s
- Drop the time-lapse cycle on the live app → saves 7s, lands at 85s

Stretch points if running short:
- Add a click into the **BRIEFS** tab to show the actual Sonnet 4.6 executive report rendering inside the dashboard → adds 10–15s

---

## Click cheat-sheet for the live segment

1. `Cmd+Tab` → Streamlit
2. App opens on **MAP** tab — VCS-981 selected — KPI strip visible
3. Click **TIME-LAPSE** tab — GIF auto-plays
4. `Cmd+Tab` → slide deck → press `5`

---

## Recovery if the live app is laggy

Skip the live segment. Slides 4 and 5 already show the KPI strip and the report quotes. The deck stands on its own at ~70 seconds.
