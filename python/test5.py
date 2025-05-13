from collections import defaultdict

# 時間ごとの必要作業量
required_work = {
    9:  20, 10: 40, 11: 90, 12: 160, 13: 130, 14: 100, 15: 70,
    16: 80, 17: 60, 18: 190, 19: 100, 20: 130, 21: 70
}
""" 
#時間ごとの必要作業量（ユーザ入力版）
required_work = {}
print("各時間帯の作業量を入力してください（数値を入力）")

for hour in range(9, 22):  # 9時〜21時
    while True:
        try:
            value = int(input(f"{hour}時の作業量: "))
            required_work[hour] = value
            break
        except ValueError:
            print("無効な入力です。数字を入力してください。")

print("\n入力された作業量:")
for hour, amount in required_work.items():
    print(f"{hour}時: {amount}")
 """
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

"""
#スタッフ勤務時間帯情報、（ユーザ入力版）
 # 効率だけ先に固定して定義
efficiency_dict = {
    "A": 60, "B": 25, "C": 41, "D": 37, "E": 10, "F": 39, "G": 51,
    "H": 29, "I": 12, "J": 30, "K": 21, "L": 10, "M": 25, "N": 22,
    "O": 18, "P": 38, "Q": 11, "R": 58, "S": 49, "T": 14, "U": 39,
    "V": 40, "W": 25, "X": 18, "Y": 11, "Z": 32
}

staff = {}

print("各スタッフの勤務可能時間帯を入力してください（例：9-14）。効率は自動設定されます。\n")

for name in efficiency_dict:
    print(f"\n{name}さんの情報:")
    efficiency = efficiency_dict[name]

    while True:
        time_input = input(f"  勤務可能時間（例：9-14）: ")
        if '-' in time_input:
            try:
                start_str, end_str = time_input.split('-')
                start, end = int(start_str), int(end_str)
                if 0 <= start < end <= 24:
                    available = list(range(start, end))
                    break
                else:
                    print("  時間は 0〜24 の範囲で、開始 < 終了 にしてください。")
            except ValueError:
                print("  無効な形式です。数字で例のように入力してください（例：9-14）")
        else:
            print("  無効な形式です。ハイフン（-）で区切ってください（例：9-14）")

    staff[name] = {
        "efficiency": efficiency,
        "available": available
    }

print("\n最終的なスタッフ情報:")
for name, data in staff.items():
    print(f"{name}: 効率={data['efficiency']}, 勤務可能={data['available']}")
 """
# 相性が悪いペア（同じ時間帯で勤務させたくない）
# ユーザー入力から相性の悪いペアを読み込む
def input_bad_pairs():
    pair_input = input("相性の悪いペアを『A,B;F,G;R,S』のように入力してください。いない場合はEnterを押してください: ")
    pairs = []
    for part in pair_input.strip().split(';'):
        if ',' in part:
            a, b = part.split(',')
            pairs.append((a.strip(), b.strip()))
    return pairs

# 使用例
bad_pairs = input_bad_pairs()
print("登録された相性の悪いペア:", bad_pairs)


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
                max_block_length = 6  # 最大6時間までの連続勤務
                for k in range(len(segment) - 2):
                    for l in range(k + 3, min(k + max_block_length + 1, len(segment) + 1)):
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


# メイン関数（中央休憩対応付き）
def assign_shifts(required_work, staff, bad_pairs):
    required_hours = list(required_work.keys())
    work_left = required_work.copy()
    assigned_staff = set()
    result = []
    breaks = []

    blocks = extract_shift_blocks(staff, required_hours)

    while any(work_left[h] > 0 for h in work_left):
        best_block = None
        best_score = 0

        for block in blocks:
            if block["staff"] in assigned_staff:
                continue

            # 相性チェック：すでに配置されたスタッフと時間が重なるか？
            overlap_conflict = False
            for existing in result:
                if (block["staff"], existing["staff"]) in bad_pairs or \
                   (existing["staff"], block["staff"]) in bad_pairs:
                    # 同じ時間帯に重なってる時間がある？
                    if any(h in existing["hours"] for h in block["hours"]):
                        overlap_conflict = True
                        break

            if overlap_conflict:
                continue  # 相性悪い人と時間がかぶるならスキップ

            score = block_score(block, work_left)
            if score > best_score:
                best_score = score
                best_block = block


        if best_block is None:
            print("残作業が割り当て不能です")
            break

        hours = best_block["hours"]
        staff_name = best_block["staff"]
        efficiency = best_block["efficiency"]

        # 6時間以上勤務の場合は中央に休憩時間を入れる
        if len(hours) >= 6:
            mid_index = len(hours) // 2
            break_hour = hours[mid_index]
            work_hours = hours[:mid_index] + hours[mid_index+1:]
            breaks.append({"staff": staff_name, "break": break_hour})
        else:
            work_hours = hours

        for h in work_hours:
            work_left[h] = max(0, work_left[h] - efficiency)

        assigned_staff.add(staff_name)
        result.append({
            "staff": staff_name,
            "hours": work_hours,
            "efficiency": efficiency
        })

    return result, work_left, breaks



# 実行
schedule, remaining, breaks = assign_shifts(required_work, staff, bad_pairs)

# 結果表示
print("=== シフト表 ===")
for entry in schedule:
    start = entry["hours"][0]
    end = entry["hours"][-1] + 1
    print(f'{entry["staff"]}: {start}時〜{end}時（効率 {entry["efficiency"]}）　勤務時間：{end - start}時間')

print("\n=== 休憩 ===")
for b in breaks:
    print(f'{b["staff"]}: {b["break"]}時〜{b["break"] + 1}時 休憩')

print("\n=== 残作業量 ===")
for h in sorted(remaining):
    print(f"{h}時: {remaining[h]}")
