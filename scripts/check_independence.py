"""Kiểm độ độc lập của lượt gán: đếm box trùng tọa độ giữa các thành viên trên ảnh chung.

    python scripts/check_independence.py

Hai người vẽ tay độc lập gần như không bao giờ ra cùng tọa độ box. Tỉ lệ box trùng cao
cho thấy nhãn được sao chép từ một nguồn chung, khi đó IAA không đo được đồng thuận thật.
Ghi submission/qc/independence_check.md. Script do nhóm thêm, không thuộc starter repo.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = ROOT / "submission" / "labels"
OUT = ROOT / "submission" / "qc" / "independence_check.md"


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    names = {c["id"]: c["name"] for c in data["categories"]}
    files = {i["id"]: Path(i["file_name"]).name for i in data["images"]}
    boxes: dict[str, list] = {name: [] for name in files.values()}
    attrs = Counter()
    for a in data["annotations"]:
        boxes[files[a["image_id"]]].append((names[a["category_id"]], tuple(round(v, 1) for v in a["bbox"])))
        at = a.get("attributes", {})
        attrs[(str(at.get("occluded_level")), str(at.get("truncated")))] += 1
    return {"boxes": boxes, "attrs": attrs, "n": len(data["annotations"])}


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    members = {p.stem: load(p) for p in sorted(LABELS.glob("[0-9][0-9][0-9].json"))}
    lines = ["# Kiểm độ độc lập của lượt gán", "",
             "Box trùng = cùng ảnh, cùng tọa độ [x, y, w, h] làm tròn 0.1 px (không xét lớp).", "",
             "| Cặp | Ảnh chung | Box của A trên ảnh chung | Box trùng tọa độ | Tỉ lệ |", "|---|---|---|---|---|"]
    for a, b in combinations(members, 2):
        common = set(members[a]["boxes"]) & set(members[b]["boxes"])
        total = same = 0
        for image in common:
            bb = Counter(box for _, box in members[b]["boxes"][image])
            for _, box in members[a]["boxes"][image]:
                total += 1
                if bb[box] > 0:
                    same += 1
                    bb[box] -= 1
        rate = f"{same / total:.0%}" if total else "N/A"
        lines.append(f"| {a}–{b} | {len(common)} | {total} | {same} | {rate} |")
    lines += ["", "## Thuộc tính (occluded_level, truncated)", "",
              "| Thành viên | Tổng box | Phân bố |", "|---|---|---|"]
    for m, d in members.items():
        dist = ", ".join(f"{k[0]}/{k[1]}: {v}" for k, v in d["attrs"].most_common())
        lines.append(f"| {m} | {d['n']} | {dist} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nĐã ghi {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
