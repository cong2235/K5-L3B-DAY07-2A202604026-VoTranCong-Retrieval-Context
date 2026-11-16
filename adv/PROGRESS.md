# Advanced challenge - progress log (IEA Global EV Outlook 2025)

Last updated: 2026-11-16. Source and licence: see SOURCE.md.

## Done
- Document chosen and verified: 173 pages, CC BY 4.0, SHA-256 recorded (SOURCE.md).
- `scripts/adv_inspect.py` (survey), `scripts/adv_extract.py` (per-page text, TOC path, 130-dpi PNG; flags 86 "visual" pages).
- Kaggle VLM server notebook `notebooks/kaggle_vlm_server.ipynb` (Qwen2.5-VL-7B-Instruct-AWQ + vLLM + Cloudflare tunnel).
  Verified: reads images (fp16 on T4 ok); tool_choice=auto does NOT call tools, tool_choice=required does -> use force-first-search.
- `scripts/adv_caption.py`: captions the 86 visual pages (resumable). Output `adv/work/captions.jsonl`
  (backup copy: `adv/captions.jsonl`). Spot check: tables transcribed accurately (p160), complex charts NOT reliable (p22).

## Not done yet (in order)
1. Re-run truncated caption page(s) with a larger --max-tokens (p101 was cut); check the pages flagged NO_VISUAL_CONTENT
   (1, 7, 8, 9, 38, 46, 54, 105) against the page images; evaluate caption quality on a sample (>=3 tables, >=5 charts).
2. Build the index: text chunks + caption chunks (pgvector table separate from the basic lab; keep page numbers; store the
   PNG path / page region). Normalise the replacement character in the text layer (e.g. "T�rkiye").
3. Write the benchmark: dev >=15 answerable + >=3 absent; test >=24 answerable + >=6 absent. Test groups (answerable):
   tables 6, images/diagrams 5, charts 5, multi-hop 4, text 4. Fix the dev/test split BEFORE experiments. Every question needs id,
   group, question, expected answer, page + cell/row/column or figure region, unit/condition. USER MUST verify each against the PDF.
4. Agent: dense/hybrid retrieval over text+captions, optional page-image viewing tool, --force-first-search; run dev, choose a
   config, then run test once; label every test question by hand; need >=27/30 (90%) for the bonus.
5. Report + commit (never commit .env, keys, the PDF or adv/work images).

## Resuming
- The Kaggle server stops when the notebook session ends. To continue: run notebooks/kaggle_vlm_server.ipynb (GPU T4 x2,
  Internet On, secret SERVER_API_KEY attached; install cell first; do not restart after install), copy the printed
  `BASE URL`, and pass it as `--base-url`. The key is KAGGLE_LLM_API_KEY in .env (same value as the Kaggle secret).
- Re-create the page images: `python -I scripts/adv_extract.py --pdf adv/source/GlobalEVOutlook2025.pdf --out adv/work`.
- Caption script resumes automatically: `python scripts/adv_caption.py --base-url <URL> --all-visual`.

## Known risks
- 90% on test is demanding for a 7B vision model, especially charts; results will be reported honestly even if below the threshold.
- PyMuPDF `find_tables()` segfaults on this PDF.

## Caption quality check (2026-11-16, Qwen2.5-VL-7B-AWQ, 86/86 pages, compared with page images by the assistant)
Coverage: 86/86, 0 system errors, 35 min. Pages whose caption is exactly NO_VISUAL_CONTENT: 1, 7, 8, 9, 46, 105, 145, 172, 173
(46/105/145 verified on the image: plain text in shaded boxes -> correct). Pages 38 and 54 contain the string inside a real caption
(an earlier note calling them "missed" was a counting mistake).
| Page | Type | Verdict |
|---|---|---|
| 160 | table with printed numbers | accurate (every cell matches); invented "Table 1/2" labels |
| 124 | colour-coded table (green/orange/red cells) | row/column labels ok; cell contents EMPTY (the information is the colours); 15.6k chars |
| 22 | stacked bar + dots | title/legend/categories ok; values wrong |
| 137 | line chart + dots, two axes | title/legend/notes ok; values fabricated (flat ~100 table; real lithium peak ~420 in 2022, pack price falls ~100->25) |
| 101, 161 | caption cut by max_tokens and degenerate (repeated rows / empty cells) | unusable, must be re-run |
Conclusions: use captions for RETRIEVAL (titles, legends, axes, notes, printed table numbers). Do NOT trust chart values or colour
encodings; chart/heat-map questions need the page image at answer time and a stronger vision model (candidate: Gemini Flash on the
~45 chart pages), or must be limited to what is printed. Re-run 101 and 161 with a repetition guard; drop captions > 8k chars or repetitive.

### Re-run of p101 and p161 (--max-tokens 4000 --frequency-penalty 0.2) - checked against the images
Both now end normally (finish=stop, no repetition loops); old versions kept in adv/captions_replaced.jsonl.
- p161: first table 8 of 9 rows match the image exactly (diesel/BEV/FCEV x US/EU/China), but the "China" fuel-cell row is garbage
  ("(estimated)" repeated; true values 0.16 / 0.15 / 4.5% / 4.1% / 11.6 / 14.0); the SECOND table on the page (unladen weight of a
  tractor-trailer) is missing; the notes are corrupted by invented LaTeX ("\text{years}", "percentage %"). -> page-level captions
  miss elements when a page holds more than one; use per-element crops.
- p101: title and notes ok; line-chart and scatter values are wrong (e.g. real US line rises 15->32, caption says 15->23; Norway
  line is the grey one 15->33, caption says 4->8). -> chart values still unreliable.
Next improvement (also required by ADVANCED.md: keep the page region / crop of tables, figures, charts): detect each element's
region (title block to its credit line) and caption each crop separately; store crop path + bbox + page.

## Element-level pipeline (2026-11-16)
- `scripts/adv_crops.py`: 91 elements on 83 pages (71 figures, 20 tables) found from the blue title/bottom rules; 6 pages use a
  flagged whole-page fallback (79, 80, 106, 125, 126, 171); 7 elements lack a bottom rule (end at the last "Source(s):" block or the
  page footer). Output: adv/work/crops/*.png + adv/work/elements.jsonl (bbox in PDF points, title, kind, exact text layer).
- `scripts/adv_caption_elements.py`: per-crop VLM caption with the text layer as authority (adv/work/element_captions.jsonl).
  Test on 3 elements: p161_e1 all 9 rows and notes correct (was broken at page level); p137_e1 qualitative only, no invented values;
  p161_e2 (two-level header) still collapses the BEV/FCEV columns -> index the raw text layer as well.

## Vector chart data extraction (no VLM) - scripts/adv_charts.py (2026-11-16)
The IEA charts are vector drawings: bars are filled rectangles, lines are stroke paths, dots are small circles; axis tick labels
and legend text carry coordinates. The script fits the axis scale from tick labels (least squares) and reads values from geometry.
- p039_e1 (stacked bars, 3 series x 13 years): axis fit residual 0.0; values match the page image (e.g. electric cars 78 (2015) ->
  785 (2024) -> 1130 (2027); ICE 1389 in 2015).
- p137_e1 (4 lines + dots, two y axes): residuals 0.0 on left, right and x axes; lithium carbonate peaks ~420.7 near 2022.75, cobalt ~259
  near 2018.25, battery-pack dots 99.8 (2015) -> 24.6 (2024). The page-level VLM caption had invented a flat ~100 table here.
- Coverage on the 66 figure elements (adv/charts_auto.json): 33 parse with a sane axis fit (30 bar-type, 3 line-type); 33 fail
  (mostly: no numeric y-axis ticks found, horizontal/percentage axes, maps, other chart types).
  "Sane fit" is NOT proof of correctness (category/legend mapping and rotated labels are unchecked; e.g. p022 stacked bars + dots).
  Every chart used in the benchmark must be verified against the page image by hand.
Plan: put the extracted tables into the index as chart-data chunks; write chart questions only from verified charts; keep the VLM
caption as the qualitative fallback; document unparsed charts as a limitation.

## Index built and loaded (2026-11-16)
- Element captions: 91/91 (0 system errors; p077_e1 hit the token limit, 8.9k chars - to be re-run).
- `scripts/adv_index.py`: 796 chunks = 517 text + 156 caption + 118 layer (exact PDF text of the crop) + 5 chartdata (verified charts in
  adv/verified_charts.json: p039_e1, p137_e1); covers 172/173 pages (page 1 = cover). Loaded into pgvector table `adv_chunks`
  (e5-small, 384 dims). Copies: adv/index_chunks.json, adv/elements.jsonl, adv/element_captions.jsonl.
- Dense smoke test (top-4): p160 table and p137 line chart queries hit the right page at rank 1; a p039 bar-chart query and a p033
  diagram query did NOT surface the element chunks in the top 4 (text chunks of nearby pages win) -> candidates for hybrid / rerank.
- Non-chart "image/diagram" material is thin: p033 bubble-flow diagram (labels printed), p147 Sankey (qualitative), p107, p040;
  only ~10 pages carry embedded images (cover, logo, trucks). Plan: keep them for the test group "images/diagrams" and state the limit.
- Next: write benchmark (dev >=15+3, test >=24+6, groups tables 6 / images 5 / charts 5 / multi-hop 4 / text 4) from the verified
  structured data; user verifies every item on the PDF. Then agent + dev runs + one test run + hand labels + report.
