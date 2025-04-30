from ortools.sat.python import cp_model

# ---- モデル定義 ----
model = cp_model.CpModel()
days      = range(7)          # 1週間
employees = ["Alice", "Bob", "Carol"]
shifts    = ["Early", "Late"]

x = {}  # x[(e,d,s)] = 0/1
for e in employees:
    for d in days:
        for s in shifts:
            x[(e,d,s)] = model.NewBoolVar(f"{e}_{d}_{s}")

# 1) 各日×シフトに1人だけ割り当て
for d in days:
    for s in shifts:
        model.AddExactlyOne(x[(e,d,s)] for e in employees)

# 2) 従業員は1日1シフトまで
for e in employees:
    for d in days:
        model.AddAtMostOne(x[(e,d,s)] for s in shifts)

# 3) 目的：均等に働く (= 最多勤務日数を最小化)
work_days = [model.NewIntVar(0, len(days), f"work_{e}") for e in employees]
for idx, e in enumerate(employees):
    model.Add(work_days[idx] == sum(x[(e,d,s)] for d in days for s in shifts))
max_work = model.NewIntVar(0, len(days), "max_work")
for wd in work_days:
    model.Add(wd <= max_work)
model.Minimize(max_work)

# ---- ソルバー実行 ----
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10
status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    for d in days:
        print(f"Day {d}: ", end="")
        for s in shifts:
            e = next(e for e in employees if solver.Value(x[(e,d,s)]))
            print(f"{s}:{e} ", end="")
        print()
