"""Build a UT report .xlsx from a YAML (or JSON) case file.

Format follows the team's standard UT sheets: layout, styles, and case numbering, plus sections
(Phần A / Phần B), NG -> OK, and the date format.
Rows 1-5 hold Branch / Redmine / the OK rule, the 2-row header starts at row 6, data at row 8.

Usage: python build_report.py <input.yaml> <output.xlsx>
"""
import json
import subprocess
import sys
from collections import Counter
from datetime import date

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RESULTS = ["OK", "NG", "NA", "NT", "NG -> OK"]
RESULT_ALIASES = {"Pending": "NT"}  # old YAML files used Pending; the team dropdown has NT (Not Tested)
OK_RULE = "※ OK khi đồng nhất giữa hệ mới và hệ cũ, nếu trường hợp khác thì note lý do"
FONT = "Times New Roman"
SIZE = 10
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
GROUP_FILL = PatternFill("solid", fgColor="DDEBF7")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")
SECTION_FILL = PatternFill("solid", fgColor="FFFF00")
HEADER_FONT = Font(name=FONT, size=SIZE, bold=True, color="FFFFFF")
BOLD_FONT = Font(name=FONT, size=SIZE, bold=True, color="000000")
BODY_FONT = Font(name=FONT, size=SIZE)
THIN = Side(style="thin", color="000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WIDTHS = {"A": 6, "B": 26, "C": 48, "D": 42, "E": 42, "F": 17.15, "G": 16.57, "H": 20, "I": 40}
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
CENTER_TOP = Alignment(horizontal="center", vertical="top", wrap_text=True)
LEFT_TOP = Alignment(horizontal="left", vertical="top", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
DATE_FORMAT = "d/m/yyyy"
HEADER_ROW = 6  # first header row when the first table has no section title

LAYERS = ["FE", "BE", "FE+BE"]
LAYER_COLORS = {"FE": "CFE2F3", "BE": "FCE5CD", "FE+BE": "EAD1DC"}


def git_user():
    try:
        return subprocess.run(["git", "config", "user.name"], capture_output=True,
                              text=True, check=False).stdout.strip()
    except OSError:
        return ""


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def text(obj, key):
    """A text field is a string (YAML block) or a list of lines; both become one cell with line breaks."""
    v = obj.get(key)
    if v is None:
        return ""
    return "\n".join(map(str, v)) if isinstance(v, list) else str(v)


def parse_date(raw, where):
    if not raw:
        return None
    if isinstance(raw, date):  # YAML reads 2026-10-19 as a date
        return raw
    try:
        return date.fromisoformat(raw)
    except ValueError:
        fail(f"{where}: date '{raw}' is not YYYY-MM-DD")


def top_block(ws, ncol, branch, redmine):
    """Rows 1-5: bordered white cells, Branch / Redmine with the link in column C, the red OK rule."""
    for r in range(1, 6):
        ws.row_dimensions[r].height = 18.75
        for col in range(1, ncol + 1):
            c = ws.cell(row=r, column=col)
            c.font, c.fill, c.alignment, c.border = BOLD_FONT, WHITE_FILL, CENTER, BORDER
    for r, label, value in ((2, "Branch", branch), (3, "Redmine", redmine)):
        ws.cell(row=r, column=2, value=label).alignment = LEFT
        c = ws.cell(row=r, column=3, value=value or None)
        c.alignment = LEFT
        if r == 3:
            c.font = Font(name=FONT, size=SIZE, color="000000")
    c = ws.cell(row=5, column=2, value=OK_RULE)
    c.font = Font(name=FONT, size=SIZE, bold=True, color="FF0000")
    c.alignment = Alignment(horizontal="left", vertical="center")


def header(ws, row, with_layer):
    ws.merge_cells(start_row=row, end_row=row, start_column=1, end_column=3)
    ws.merge_cells(start_row=row, end_row=row, start_column=4, end_column=5)
    ws.cell(row=row, column=1, value="Case")
    ws.cell(row=row, column=4, value="Mong đợi")
    for col, label in enumerate(["#", "Nhóm", "Trường hợp", "Hệ cũ", "Hệ mới"], 1):
        ws.cell(row=row + 1, column=col, value=label)
    labels = ["Ngày test", "Kết quả", "Tester (Dev)", "Note/Lý do"] + (["Lỗi ở (FE/BE)"] if with_layer else [])
    for col, label in enumerate(labels, 6):
        ws.merge_cells(start_row=row, end_row=row + 1, start_column=col, end_column=col)
        ws.cell(row=row, column=col, value=label)
    for r in (row, row + 1):
        ws.row_dimensions[r].height = 19.5
        for col in range(1, len(labels) + 6):
            c = ws.cell(row=r, column=col)
            c.fill, c.font, c.alignment, c.border = HEADER_FILL, HEADER_FONT, CENTER, BORDER


def body_cell(ws, row, col, value):
    c = ws.cell(row=row, column=col, value=value)
    c.border = BORDER
    if col in (1, 2):  # # / Nhóm: bold on light blue, merged per group
        c.font, c.fill, c.alignment = BOLD_FONT, GROUP_FILL, CENTER
    else:
        c.font = BODY_FONT
        c.alignment = CENTER_TOP if col in (6, 7, 8, 10) else LEFT_TOP
    if col == 6:
        c.number_format = DATE_FORMAT
    return c


def write_groups(ws, row, groups, ctx):
    """Write one table body. Returns the next free row."""
    gi = 0
    for gi, g in enumerate(groups, 1):
        if not g.get("name"):
            fail(f"{ctx['where']} group {gi}: missing 'name'")
        name = text(g, "name")
        cases = g.get("cases") or [{"_placeholder": True, "note": g.get("note", "")}]
        start = row
        real = 0
        for ci, c in enumerate(cases, 1):
            where = f"{ctx['where']} group {gi} case {ci}"
            result = c.get("result", "") or ""
            result = RESULT_ALIASES.get(result, result)
            if result and result not in RESULTS:
                fail(f"{where}: result '{result}' not in {RESULTS}")
            d = parse_date(c.get("date"), where)
            tester = c.get("tester") or (ctx["tester"] if d else "")
            layer = c.get("layer") or None
            if layer and layer not in LAYERS:
                fail(f"{where}: layer '{layer}' not in {LAYERS}")
            case_text = text(c, "case")
            is_case = bool(c) and not c.get("_placeholder")
            if is_case:
                real += 1
                if ctx["numbering"] and case_text:
                    case_text = f"{gi}.{real}  {case_text}"
            values = [gi, name, case_text, text(c, "legacy"), text(c, "new"),
                      d, result or None, tester, text(c, "note")] + ([layer] if ctx["with_layer"] else [])
            for col, v in enumerate(values, 1):
                body_cell(ws, row, col, v)
            if layer:
                ws.cell(row=row, column=10).fill = PatternFill("solid", fgColor=LAYER_COLORS[layer])
            if is_case:
                ctx["n_cases"] += 1
                ctx["counts"][result or "(trống)"] += 1
            row += 1
        if row - 1 > start:
            ws.merge_cells(start_row=start, end_row=row - 1, start_column=1, end_column=1)
            ws.merge_cells(start_row=start, end_row=row - 1, start_column=2, end_column=2)

    for _ in range(int(ctx["extra_rows"])):
        gi += 1
        for col in range(1, ctx["ncol"] + 1):
            body_cell(ws, row, col, gi if col == 1 else None)
        ws.row_dimensions[row].height = 30
        row += 1
    return row


def build_sheet(wb, spec, defaults, idx):
    title = str(spec.get("name") or spec.get("sheet") or defaults.get("sheet") or "UT")[:31]
    ws = wb.active if idx == 0 else wb.create_sheet()
    ws.title = title
    sections = spec.get("sections")
    if sections is None:
        if not isinstance(spec.get("groups"), list) or not spec["groups"]:
            fail(f"sheet '{title}': 'groups' (or 'sections') must be a non-empty list")
        sections = [{"groups": spec["groups"]}]
    all_cases = [c for s in sections for g in (s.get("groups") or []) for c in (g.get("cases") or [])]
    # Optional column J: where an NG is fixed (case key `layer`: FE / BE / FE+BE). Only added when a case sets it.
    with_layer = any(c.get("layer") for c in all_cases)
    ncol = 10 if with_layer else 9
    for col, w in WIDTHS.items():
        ws.column_dimensions[col].width = w
    if with_layer:
        ws.column_dimensions["J"].width = 12
    top_block(ws, ncol, spec.get("branch", defaults.get("branch")), spec.get("redmine", defaults.get("redmine")))

    ctx = {"where": f"sheet '{title}'", "tester": defaults["tester"], "with_layer": with_layer, "ncol": ncol,
           "numbering": spec.get("numbering", defaults.get("numbering", True)),
           "extra_rows": spec.get("extra_rows", defaults.get("extra_rows", 0)),
           "counts": Counter(), "n_cases": 0}
    ranges = []
    row = HEADER_ROW
    for si, s in enumerate(sections):
        if s.get("title"):  # section title row on yellow, as in CD2011 (Phần A / Phần B)
            if si == 0:
                row += 1
            c = ws.cell(row=row, column=1, value=text(s, "title"))
            c.font, c.fill, c.alignment = BOLD_FONT, SECTION_FILL, Alignment(horizontal="left", vertical="center")
            row += 1
        header(ws, row, with_layer)
        start = row + 2
        ctx["where"] = f"sheet '{title}' section {si + 1}"
        row = write_groups(ws, start, s.get("groups") or [], ctx)
        ranges.append((start, row - 1))
        row += 3  # blank rows before the next section title

    dv = DataValidation(type="list", formula1='"' + ",".join(RESULTS) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    for a, b in ranges:
        dv.add(f"G{a}:G{b}")
    if with_layer:
        dv_layer = DataValidation(type="list", formula1='"' + ",".join(LAYERS) + '"', allow_blank=True)
        ws.add_data_validation(dv_layer)
        for a, b in ranges:
            dv_layer.add(f"J{a}:J{b}")
    if len(ranges) == 1:  # one table: keep the header and #/Nhóm/Trường hợp in view
        ws.freeze_panes = f"D{ranges[0][0]}"
        # Filter buttons on the lower header row, so Kết quả (column G) can be filtered.
        ws.auto_filter.ref = f"A{ranges[0][0] - 1}:{get_column_letter(ncol)}{ranges[0][1]}"
    return title, ctx


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        fail("usage: build_report.py <input.yaml> <output.xlsx>")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = yaml.safe_load(f) if sys.argv[1].endswith((".yaml", ".yml")) else json.load(f)
    defaults = dict(data)
    defaults["tester"] = data.get("tester") or git_user()
    sheets = data.get("sheets") or [data]  # one-sheet files keep `groups` at the top level
    if not isinstance(sheets, list):
        fail("'sheets' must be a list")

    wb = Workbook()
    report = [build_sheet(wb, spec, defaults, i) for i, spec in enumerate(sheets)]
    wb.save(sys.argv[2])
    print(f"Saved {sys.argv[2]}")
    for title, ctx in report:
        print(f"Sheet {title}  Cases: {ctx['n_cases']}")
        for k in RESULTS + ["(trống)"]:
            if ctx["counts"][k]:
                print(f"  {k}: {ctx['counts'][k]}")


if __name__ == "__main__":
    main()
