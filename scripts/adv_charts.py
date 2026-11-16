"""Rebuild the numbers of a vector bar / stacked-bar chart from the PDF geometry (no vision model).

Idea: every bar is a filled rectangle; its height times the axis scale is the value. The scale comes from a linear fit of the
numeric y-axis tick labels (text positions); the series name comes from the legend swatch of the same fill colour; the
category comes from the x-axis label nearest to the bar. Grouped bars share a category; a stacked segment's value is its height.

Usage: python -I scripts/adv_charts.py --pdf adv/source/GlobalEVOutlook2025.pdf --work adv/work --element p039_e1 [--json out.json]
Limitations (prototype): vertical bars on a linear axis, single-token category labels. Always check the output against the page.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import pymupdf

NUM = re.compile(r'^[−\-]?\d+([.,]\d+)?%?$')


def words_in(page, rect):
    return [(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text('words', clip=rect)]


def merge_numeric_ticks(words, x_max):
    """Group number tokens left of the plot on the same line ("1" "200" -> 1200)."""
    rows = defaultdict(list)
    for x0, y0, x1, y1, t in words:
        if x1 <= x_max and NUM.match(t):
            rows[round((y0 + y1) / 2)].append((x0, y0, x1, y1, t))
    ticks = []
    for _, ws in rows.items():
        ws.sort()
        txt = ''.join(w[4] for w in ws).replace('−', '-').replace(',', '.').rstrip('%')
        yc = sum((w[1] + w[3]) / 2 for w in ws) / len(ws)
        try:
            ticks.append((yc, float(txt)))
        except ValueError:
            pass
    return ticks


def fit_axis(ticks):
    """value = a * y + b by least squares on (y centre, value)."""
    n = len(ticks)
    sy = sum(t[0] for t in ticks)
    sv = sum(t[1] for t in ticks)
    syy = sum(t[0] ** 2 for t in ticks)
    syv = sum(t[0] * t[1] for t in ticks)
    a = (n * syv - sy * sv) / (n * syy - sy ** 2)
    b = (sv - a * sy) / n
    resid = max(abs(a * y + b - v) for y, v in ticks)
    return a, b, resid


def extract_bars(page, bbox):
    rect = pymupdf.Rect(bbox)
    series = defaultdict(list)           # fill colour -> bar rects
    swatches = {}                         # fill colour -> legend swatch rect
    for dr in page.get_drawings():
        fill = dr.get('fill')
        if not fill or not rect.contains(dr['rect']):
            continue
        color = tuple(round(c, 2) for c in fill)
        for it in dr['items']:
            if it[0] != 're':
                continue
            r = it[1]
            if r.width <= 8 and r.height <= 8:
                swatches[color] = r
            elif r.width < 60 and r.height > 0.2 and r.width > 3:   # a bar (the grey shading / rules are wide or thin)
                series[color].append(r)
    series = {c: v for c, v in series.items() if len(v) >= 2}
    if not series:
        raise ValueError('no bar series found')
    allbars = [r for v in series.values() for r in v]
    baseline = max(r.y1 for r in allbars)
    left = min(r.x0 for r in allbars)
    words = words_in(page, rect)
    ticks = merge_numeric_ticks([w for w in words if w[3] < baseline + 2], left - 1)
    if len(ticks) < 3:
        raise ValueError('not enough numeric y-axis ticks')
    a, b, resid = fit_axis(ticks)
    # category labels: words just below the baseline
    cats = []
    for x0, y0, x1, y1, t in sorted(words):
        if baseline < y0 < baseline + 14 and not (swatches and any(abs(y0 - s.y0) < 6 for s in swatches.values())):
            cats.append(((x0 + x1) / 2, t))
    merged = []
    for xc, t in cats:
        if merged and xc - merged[-1][0] < 3:
            merged[-1] = ((merged[-1][0] + xc) / 2, merged[-1][1] + ' ' + t)
        else:
            merged.append((xc, t))
    # legend names: words to the right of each swatch on the same line
    names = {}
    for color, s in swatches.items():
        line = sorted(w for w in words if abs((w[1] + w[3]) / 2 - (s.y0 + s.y1) / 2) < 5 and w[0] >= s.x1 - 1)
        label, last = [], s.x1
        for w in line:
            if w[0] - last > 8 and label:
                break
            label.append(w[4])
            last = w[2]
        names[color] = ' '.join(label)
    out = []
    for color, bars in series.items():
        for r in bars:
            xc = (r.x0 + r.x1) / 2
            cat = min(merged, key=lambda c: abs(c[0] - xc))[1] if merged else ''
            value = (a * (r.y0) + b) - (a * (r.y1) + b)      # height in axis units (a is negative, so use the difference)
            out.append({'category': cat, 'series': names.get(color, str(color)), 'color': list(color),
                        'value': round(abs(value), 1), 'bar_height_pt': round(r.height, 2)})
    return {'axis_fit_max_residual': round(resid, 3), 'units_per_pt': round(abs(a), 3), 'baseline_y': round(baseline, 1),
            'legend': {str(list(k)): v for k, v in names.items()}, 'categories': [c[1] for c in merged], 'bars': out}


def _fit_pairs(pairs):
    """Least squares v = a*c + b on (coordinate, value) pairs."""
    n = len(pairs)
    sc, sv = sum(c for c, _ in pairs), sum(v for _, v in pairs)
    scc, scv = sum(c * c for c, _ in pairs), sum(c * v for c, v in pairs)
    a = (n * scv - sc * sv) / (n * scc - sc ** 2)
    b = (sv - a * sc) / n
    return a, b, max(abs(a * c + b - v) for c, v in pairs)


def extract_lines(page, bbox):
    """Line + dot chart with a numeric x axis (years) and a left and/or right numeric y axis."""
    rect = pymupdf.Rect(bbox)
    words = words_in(page, rect)
    grid = [d for d in page.get_drawings() if rect.contains(d['rect']) and d.get('color') == (0.88, 0.88, 0.88)
            or (rect.contains(d['rect']) and d.get('color') and all(abs(c - 0.88) < 0.02 for c in d['color']))]
    if not grid:
        raise ValueError('no grid lines found')
    pl, pr = min(g['rect'].x0 for g in grid), max(g['rect'].x1 for g in grid)
    pt, pb = min(g['rect'].y0 for g in grid), max(g['rect'].y1 for g in grid)
    for d in page.get_drawings():   # the zero line / x axis is a black stroke spanning the plot width: it is the true bottom
        r = d['rect']
        if rect.contains(r) and r.height < 1 and r.width >= 0.9 * (pr - pl) and d.get('color') and sum(d['color']) < 0.3:
            pb = max(pb, r.y1)
    # ticks: left axis (x1 <= pl), right axis (x0 >= pr), x axis years (below the plot)
    def numeric(ws):
        rows = defaultdict(list)
        for x0, y0, x1, y1, t in ws:
            if NUM.match(t):
                rows[round((y0 + y1) / 2)].append((x0, y0, x1, y1, t))
        out = []
        for ws2 in rows.values():
            ws2.sort()
            try:
                out.append(((sum((w[1] + w[3]) / 2 for w in ws2) / len(ws2)), float(''.join(w[4] for w in ws2).replace(',', '.'))))
            except ValueError:
                pass
        return out
    inplot = [w for w in words if pt - 8 <= (w[1] + w[3]) / 2 <= pb + 3]
    # tick labels sit right next to the plot edge; a rotated axis title ("Index (1 Jan. 2017 = 100)") is further away
    left = numeric([w for w in inplot if pl - 22 <= w[2] <= pl + 1])
    right = numeric([w for w in inplot if pr - 1 <= w[0] <= pr + 22])
    xt = [((w[0] + w[2]) / 2, float(w[4])) for w in words if w[1] > pb + 3 and re.fullmatch(r'(19|20)\d\d', w[4]) and w[1] < pb + 20]
    if len(left) < 3 or len(xt) < 3:
        raise ValueError('axis ticks not found')
    ax = {'left': _fit_pairs(left)}
    if len(right) >= 3:
        ax['right'] = _fit_pairs(right)
    xa, xb, xres = _fit_pairs(xt)
    # legend: short single-segment strokes (lines) and tiny filled circles (dots)
    legend = []
    for d in page.get_drawings():
        r = d['rect']
        if not rect.contains(r) or r.y0 < pb + 8:
            continue
        if d.get('color') and len(d['items']) == 1 and d['items'][0][0] == 'l' and 8 < r.width < 40 and r.height < 1:
            legend.append(('line', tuple(round(c, 2) for c in d['color']), r))
        elif d.get('fill') and d['items'] and d['items'][0][0] == 'c' and r.width < 8:
            legend.append(('dot', tuple(round(c, 2) for c in d['fill']), r))
    names = {}
    for kind, color, r in legend:
        line = sorted(w for w in words if abs((w[1] + w[3]) / 2 - (r.y0 + r.y1) / 2) < 5 and w[0] >= r.x1 - 1)
        label, last = [], r.x1
        for w in line:
            if w[0] - last > 8 and label:
                break
            label.append(w[4])
            last = w[2]
        names[(kind, color)] = ' '.join(label)
    series = []
    for d in page.get_drawings():
        r = d['rect']
        if not rect.contains(r) or r.y0 >= pb + 3:
            continue
        if d.get('color') and not d.get('fill') and len(d['items']) >= 10 and all(it[0] == 'l' for it in d['items']):
            color = tuple(round(c, 2) for c in d['color'])
            if ('line', color) not in names:   # axis ticks and other unlabeled strokes are not data series
                continue
            name = names[('line', color)]
            axis = 'right' if '(right)' in name and 'right' in ax else 'left'
            pts = [d['items'][0][1]] + [it[2] for it in d['items']]
            a, b, _ = ax[axis]
            series.append({'series': name, 'kind': 'line', 'axis': axis,
                           'points': [(round(xa * p.x + xb, 2), round(a * p.y + b, 1)) for p in pts]})
    dots = defaultdict(set)
    for d in page.get_drawings():
        r = d['rect']
        if rect.contains(r) and d.get('fill') and d['items'] and d['items'][0][0] == 'c' and r.width < 9 and r.y0 < pb:
            color = tuple(round(c, 2) for c in d['fill'])
            name = names.get(('dot', color), str(color))
            axis = 'right' if '(right)' in name and 'right' in ax else 'left'
            a, b, _ = ax[axis]
            dots[(name, axis)].add((round(xa * (r.x0 + r.x1) / 2 + xb, 2), round(a * (r.y0 + r.y1) / 2 + b, 1)))
    for (name, axis), pts in dots.items():
        series.append({'series': name, 'kind': 'dots', 'axis': axis, 'points': sorted(pts)})
    return {'axes_fit_max_residual': {k: round(v[2], 3) for k, v in ax.items()}, 'x_fit_residual': round(xres, 3),
            'series': series}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True, type=Path)
    ap.add_argument('--work', required=True, type=Path)
    ap.add_argument('--element', required=True)
    ap.add_argument('--json', type=Path)
    a = ap.parse_args()
    els = {e['element_id']: e for e in map(json.loads, (a.work / 'elements.jsonl').read_text(encoding='utf-8').splitlines())}
    e = els[a.element]
    page = pymupdf.open(a.pdf)[e['page'] - 1]
    try:
        res = extract_bars(page, e['bbox'])
    except ValueError:
        res = extract_lines(page, e['bbox'])
        res['element_id'], res['title'] = a.element, e['title']
        if a.json:
            a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
        print(res['title'][:100], '| residuals', res['axes_fit_max_residual'], res['x_fit_residual'])
        for s_ in res['series']:
            vals = [v for _, v in s_['points']]
            hi = max(s_['points'], key=lambda p: p[1])
            lo = min(s_['points'], key=lambda p: p[1])
            print(f"{s_['series']!r} [{s_['kind']}, {s_['axis']} axis] n={len(vals)} first={s_['points'][0]} last={s_['points'][-1]} "
                  f"max={hi} min={lo}")
        return
    res['element_id'] = a.element
    res['title'] = e['title']
    if a.json:
        a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(res['title'][:100])
    print('axis fit residual', res['axis_fit_max_residual'], '| units/pt', res['units_per_pt'], '| legend', res['legend'])
    table = defaultdict(dict)
    for b in res['bars']:
        table[b['category']][b['series']] = b['value']
    series = sorted({b['series'] for b in res['bars']})
    print('category | ' + ' | '.join(series))
    for c in res['categories']:
        print(c, '|', ' | '.join(str(table[c].get(s, '')) for s in series))


if __name__ == '__main__':
    main()
