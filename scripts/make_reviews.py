"""Turn the test traces + hand labels into the files starter/agent_metrics.py needs, and aggregate them.

Labels (LABELS below) were read against the chunk text of the book (the cited chunks and the gold evidence) and written by the
AI assistant as a DRAFT; the student must confirm them against the original book before submission (see report).
Rules used:
- grounded answer 0/1/2 (BENCHMARK.md): 0 wrong or no supporting evidence in the context (including a refusal of an answerable
  question), 1 partly right, 2 right and sufficient.
- citation support: True only if the cited chunk is in the context AND contains what the sentence it is attached to claims;
  garbled ids and citations in refusals are False.
- context grade 0/1/2: 0 no evidence, 1 evidence present but a needed point is missing, 2 evidence and source (chunk id and page) complete.
- status and citations are re-derived from the stored answer text with src.agent.parse_answer (fixes: "[INSUFFICIENT_EVIDENCE" and
  garbled citation ids); trace files in results/ are not modified.
Usage: python scripts/make_reviews.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'starter'))
from agent_metrics import aggregate  # noqa: E402
from src.agent import parse_answer  # noqa: E402

P = 'B:openstax-pds:'
RUNS = {'C1': 'results/test-agent-C1-rerankrrf-k5-force1', 'BASE': 'results/test-agent-BASE-dense-k3-b800-auto'}
# qid: (grounded 0/1/2 or None, supported citation ids, context grade or None, abstention_correct or None, reason)
LABELS = {
 'C1': {
  'H01': (2, ['p119:0'], 2, None, 'Khớp đáp án; p119:0 chứa đúng câu về dữ liệu phi số.'),
  'H02': (2, [], 2, None, 'Đúng (giá trị giữa; vị trí (n+1)/2 có ở p118:2, nằm trong context) nhưng citation p118:0 không chứa phần vị trí.'),
  'H03': (2, ['p123:0'], 2, None, 'Đúng và được p123:0 hỗ trợ.'),
  'H04': (2, ['p136:1', 'p132:1'], 2, None, 'Ví dụ y học (p136:1) và hiệu chỉnh xác suất theo thông tin mới (p132:1) đều được hỗ trợ.'),
  'H05': (2, [], 2, None, 'Định nghĩa và ví dụ quầy thanh toán đúng (p142:1); ví dụ tai nạn giao lộ nằm ở p142:0 (có trong context), không phải p142:1 được trích.'),
  'H06': (1, [], 2, None, 'Phần làm sạch đúng (trùng lặp, thiếu, định dạng) nhưng sai khi nói làm sạch bao gồm tích hợp và biến đổi dữ liệu: đó là các bước riêng ở p86:2.'),
  'H07': (2, ['p98:0'], 2, None, 'Đúng; câu về diễn giải cho học máy có trong p98:0.'),
  'H08': (2, ['p97:0'], 2, None, 'Đúng; "readability" và ví dụ có trong p97:0.'),
  'H09': (2, ['p128:0'], 2, None, 'Cận trên 1,159,375 và kết luận ngoại lệ đúng.'),
  'H10': (2, ['p129:0'], 2, None, 'Kết luận -2 độ lệch chuẩn dưới trung bình đúng; ký hiệu công thức bị mất trong text layer của sách.'),
  'H11': (2, ['p146:0'], 2, None, '99,7% đúng.'),
  'H12': (2, ['p75:0'], 2, None, 'Trùng gần nguyên văn p75:0.'),
  'H13': (2, ['p145:0', 'p148:1'], 2, None, 'Diện tích bên phải (p145:0) và norm.cdf rồi lấy 1 trừ (p148:1) đều được hỗ trợ.'),
  'X-T01': (None, [], None, True, 'Đã tìm, từ chối, không thêm khẳng định.'),
  'X-T02': (None, [], None, False, 'Trả lời bằng kiến thức ngoài sách, không citation, rồi mới nói passages không nêu: không đạt.'),
  'X-T03': (None, [], None, True, 'Đã tìm, từ chối, không thêm khẳng định.'),
 },
 'BASE': {
  'H01': (0, [], 0, None, 'Context không có đoạn về mode; citation p118:2 nói về vị trí trung vị (không hỗ trợ).'),
  'H02': (0, [], 0, None, 'Từ chối câu có đáp án; context không có evidence (800 ký tự chỉ vừa một chunk).'),
  'H03': (0, [], 0, None, 'Không tìm kiếm, citation p95:1 không có trong context và nói về tokenization.'),
  'H04': (1, ['p136:1'], 1, None, 'Ví dụ y học đúng nhưng thiếu ý hiệu chỉnh xác suất theo thông tin mới.'),
  'H05': (0, [], 0, None, 'Từ chối câu có đáp án (không tìm kiếm).'),
  'H06': (2, ['p86:1'], 2, None, 'Context có p86:1 chứa cùng nội dung (đoạn thay thế hợp lệ); chunk gold p84 không có trong context nên chỉ số tự động tính trượt.'),
  'H07': (2, [], 2, None, 'Nội dung đúng và evidence có trong context nhưng ID citation viết sai (không hợp lệ).'),
  'H08': (0, [], 0, None, 'Từ chối câu có đáp án (không tìm kiếm).'),
  'H09': (2, ['p128:0'], 2, None, 'Đúng và được p128:0 hỗ trợ.'),
  'H10': (0, [], 0, None, 'Từ chối câu có đáp án (không tìm kiếm).'),
  'H11': (0, [], 0, None, 'Từ chối câu có đáp án (không tìm kiếm).'),
  'H12': (2, [], 2, None, 'Nội dung đúng (trùng p75:0) nhưng ID citation viết sai (không hợp lệ).'),
  'H13': (0, [], 0, None, 'Từ chối câu có đáp án (không tìm kiếm).'),
  'X-T01': (None, [], None, True, 'Đã tìm và từ chối.'),
  'X-T02': (None, [], None, True, 'Từ chối nhưng KHÔNG gọi search (từ chối không có căn cứ tìm kiếm).'),
  'X-T03': (None, [], None, True, 'Đã tìm và từ chối.'),
 },
}


def main():
    out = ROOT / 'results' / 'test-review'
    out.mkdir(parents=True, exist_ok=True)
    qs = {q['id']: q for q in json.loads((ROOT / 'data/converted/questions.json').read_text(encoding='utf-8'))}
    cases = [{'id': q, 'split': 'test', 'answerable': q in qs} for q in LABELS['C1']]
    (out / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=1), encoding='utf-8')
    summary = {}
    for run, path in RUNS.items():
        traces = json.loads((ROOT / path / 'traces.json').read_text(encoding='utf-8'))
        conv, reviews, ctx = [], [], {'0': 0, '1': 0, '2': 0}
        for t in traces:
            status, cited, valid = parse_answer(t['answer'], t['context_ids'])
            g, sup, cg, abst, reason = LABELS[run][t['query_id']]
            events = [{**e, 'event': 'search'} for e in t['events']]
            conv.append({'query_id': t['query_id'], 'status': status, 'events': events, 'citations': cited,
                         'citations_in_context': valid, 'status_original': t['status']})
            full = [P + x for x in sup]
            r = {'query_id': t['query_id'],
                 'citation_support': [status == 'answered' and (c in full) and (c in valid) for c in cited], 'reason': reason}
            if g is not None:
                r['answer_grade'] = g
                r['context_grade'] = cg
                ctx[str(cg)] += 1
            else:
                r['abstention_correct'] = abst
            reviews.append(r)
        (out / f'traces_{run}.json').write_text(json.dumps(conv, ensure_ascii=False, indent=1), encoding='utf-8')
        (out / f'reviews_{run}.json').write_text(json.dumps(reviews, ensure_ascii=False, indent=1), encoding='utf-8')
        agg = aggregate(cases, conv, reviews)
        agg['context_grade_counts'] = ctx
        agg['context_grade_mean'] = round((ctx['1'] + 2 * ctx['2']) / sum(ctx.values()), 2)
        agg['status_corrected'] = [c['query_id'] for c in conv if c['status'] != c['status_original']]
        summary[run] = agg
        (out / f'summary_{run}.json').write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
