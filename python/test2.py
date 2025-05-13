from collections import defaultdict

# 時間ごとの必要作業量
required_work = {
    9:  20, 10: 40, 11: 90, 12: 160, 13: 130, 14: 100, 15: 70,
    16: 80, 17: 60, 18: 190, 19: 150, 20: 130, 21: 70
}

# スタッフ情報
staff = {
    "A": {"efficiency": 60, "available": list(range(9, 14))},
    "B": {"efficiency": 25, "available": list(range(10, 17))},
    "C": {"efficiency": 41, "available": list(range(9, 13))},
    "D": {"efficiency": 37, "available": list(range(9, 13))},
    "E": {"efficiency": 10, "available": list(range(12, 20))},
    "F": {"efficiency": 39, "available": list(range(11, 14))},
    "G": {"efficiency": 51, "available": list(range(9, 14))},
    "H": {"efficiency": 29, "available": list(range(10, 22))},
    "I": {"efficiency": 12, "available": list(range(9, 13))},
    "J": {"efficiency": 30, "available": list(range(15, 19))},
    "K": {"efficiency": 21, "available": list(range(12, 16))},
    "L": {"efficiency": 10, "available": list(range(18, 23))},
    "M": {"efficiency": 25, "available": list(range(13, 20))},
    "N": {"efficiency": 22, "available": list(range(18, 23))},
    "O": {"efficiency": 18, "available": list(range(11, 18))},
    "P": {"efficiency": 38, "available": list(range(18, 23))},
    "Q": {"efficiency": 11, "available": list(range(9, 12))},
    "R": {"efficiency": 58, "available": list(range(11, 14))},
    "S": {"efficiency": 49, "available": list(range(11, 18))},
    "T": {"efficiency": 14, "available": list(range(9, 18))},
    "U": {"efficiency": 39, "available": list(range(13, 20))},
    "V": {"efficiency": 40, "available": list(range(18, 23))},
    "W": {"efficiency": 25, "available": list(range(11, 17))},
    "X": {"efficiency": 18, "available": list(range(9, 18))},
    "Y": {"efficiency": 11, "available": list(range(10, 20))},
    "Z": {"efficiency": 32, "available": list(range(18, 23))}
}

# ブロック抽出（3時間以上の連続勤務）
def extract_shift_blocks(staff, required_hours):
    blocks = []
    for name, info in staff.items():
        available = sorted(set(info["available"]) & set(required_hours))
        eff = info["efficiency"]
        i = 0
        while i < len(available):
            j = i
            while j + 1 < len(available) and available[j + 1] == available[j] + 1:
                j += 1
            segment = available[i:j+1]
            if len(segment) >= 3:
                for k in range(len(segment) - 2):
                    for l in range(k + 3, len(segment) + 1):
                        block = {
                            "staff": name,
                            "hours": segment[k:l],
                            "efficiency": eff
                        }
                        blocks.append(block)
            i = j + 1
    return blocks

# ブロックのスコア（どれだけ効くか）
def block_score(block, work):
    return sum(min(work.get(h, 0), block["efficiency"]) for h in block["hours"])

# メイン関数
def assign_shifts(required_work, staff):
    required_hours = list(required_work.keys())
    work_left = required_work.copy()
    assigned_staff = set()
    result = []

    blocks = extract_shift_blocks(staff, required_hours)

    while any(work_left[h] > 0 for h in work_left):
        best_block = None
        best_score = 0

        for block in blocks:
            if block["staff"] in assigned_staff:
                continue
            score = block_score(block, work_left)
            if score > best_score:
                best_score = score
                best_block = block

        if best_block is None:
            print("残作業が割り当て不能です")
            break

        for h in best_block["hours"]:
            work_left[h] = max(0, work_left[h] - best_block["efficiency"])

        assigned_staff.add(best_block["staff"])
        result.append(best_block)

    return result, work_left

# 実行
schedule, remaining = assign_shifts(required_work, staff)

# 結果表示
print("=== シフト表 ===")
for entry in schedule:
    print(f'{entry["staff"]}: {entry["hours"][0]}時〜{entry["hours"][-1]+1}時（効率 {entry["efficiency"]}）')

print("\n=== 残作業量 ===")
for h in sorted(remaining):
    print(f"{h}時: {remaining[h]}")
