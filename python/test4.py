import tkinter as tk
from tkinter import messagebox
import datetime
import calendar
import json
import os
import csv

CONFIG_FILE = "config.json"
HISTORY_FILE = "daily_schedule.json"
TABLE_DIR = os.path.join(os.path.dirname(__file__),"table")#csvファイルを格納するディレクトリ
#あらかじめtableディレクトリを作成しておいて下さい。

DEFAULT_CONFIG = {#初期値
    "staff": ["佐藤", "鈴木", "高橋", "田中", "伊藤"],
    "stations": ["レジ", "品出し", "清掃", "案内"],
    "business_hours": {"start": 9, "end": 22}
}

class MainApp(tk.Frame):
    def __init__(self, master):#メインウィンドウの定義
        super().__init__(master)
        self.master = master
        self.pack()
        self.load_settings()
        self.history = self.load_history()
        today = datetime.date.today()
        self.year, self.month = today.year, today.month
        master.geometry("700x500")
        master.title("シフト管理")
        self.create_widgets()
        self.build_calendar()

    def load_settings(self):#ファイル読取の準備
        if os.path.exists(CONFIG_FILE):
            self.config = json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))#config.jsonを読取モードで開く
        else:
            self.config = DEFAULT_CONFIG.copy()
            json.dump(self.config, open(CONFIG_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)#config.jsonを書き込みモードで開く
        self.staffs = list(self.config.get('staff', DEFAULT_CONFIG['staff']))
        self.stations = list(self.config.get('stations', DEFAULT_CONFIG['stations']))
        bh = self.config.get('business_hours', DEFAULT_CONFIG['business_hours'])
        self.bh_start = bh.get('start', 9)#初期値
        self.bh_end = bh.get('end', 22)#初期値
        self.TIME_CHOICES = []
        for h in range(self.bh_start, self.bh_end):
            for m in (0, 30):
                self.TIME_CHOICES.append(f"{h:02d}:{m:02d}")
        self.TIME_CHOICES.append(f"{self.bh_end:02d}:00")

    def save_config(self):#config.jsonを書き込みモードで開く
        json.dump(self.config, open(CONFIG_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    def load_history(self):#daily_schedule.jsonを読取モードで開く
        if os.path.exists(HISTORY_FILE):
            return json.load(open(HISTORY_FILE, 'r', encoding='utf-8'))
        return {}

    def create_widgets(self):#トップ画面
        menu = tk.Frame(self)#メニュー
        menu.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Button(menu, text="管理者画面", command=self.open_admin).pack(fill=tk.X, pady=2)
        self.cal_frame = tk.Frame(self)
        self.cal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        nav = tk.Frame(self.cal_frame)#カレンダー
        nav.pack()
        tk.Button(nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.lbl_year = tk.Label(nav, text=self.year)
        self.lbl_year.pack(side=tk.LEFT)
        tk.Label(nav, text=" / ").pack(side=tk.LEFT)
        self.lbl_month = tk.Label(nav, text=self.month)
        self.lbl_month.pack(side=tk.LEFT)
        tk.Button(nav, text=">", command=self.next_month).pack(side=tk.LEFT)
        wk = tk.Frame(self.cal_frame)
        wk.pack()
        for d in ['日','月','火','水','木','金','土']:
            tk.Label(wk, text=d, width=4).pack(side=tk.LEFT)#曜日を表示
        self.rows = []
        for _ in range(6):
            row = tk.Frame(self.cal_frame)
            row.pack()
            self.rows.append(row)

    def build_calendar(self):#カレンダーをつくる
        self.lbl_year.config(text=self.year)
        self.lbl_month.config(text=self.month)
        for row in self.rows:
            for w in row.winfo_children():
                w.destroy()
        cal = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(cal):
            for day in week:
                frame = self.rows[r]
                if day:
                    tk.Button(frame, text=str(day), width=4, 
                                  command=lambda d=day: self.open_day(d)).pack(side=tk.LEFT)
                else:
                    tk.Button(frame, text="", width=4, state=tk.DISABLED).pack(side=tk.LEFT)

    def prev_month(self):#<ボタンを押したとき、ひと月戻る
        if self.month == 1:
            self.year -= 1; self.month = 12
        else:
            self.month -= 1
        self.build_calendar()

    def next_month(self):#>ボタンを押したとき、ひと月進む
        if self.month == 12:
            self.year += 1; self.month = 1
        else:
            self.month += 1
        self.build_calendar()

    def open_admin(self):#管理者画面の設計
        dlg = tk.Toplevel(self.master)
        dlg.title("管理者設定")
        dlg.geometry("350x600")
        dlg.transient(self.master)
        dlg.grab_set()
        bh = self.config.get('business_hours', DEFAULT_CONFIG['business_hours'])
        frame_bh = tk.LabelFrame(dlg, text="営業時間設定(時)")#営業時間管理
        frame_bh.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(frame_bh, text="開始:").pack(side=tk.LEFT)
        v_start = tk.IntVar(value=bh.get('start'))
        tk.Spinbox(frame_bh, from_=0, to=23, textvariable=v_start, width=5).pack(side=tk.LEFT)
        tk.Label(frame_bh, text="終了:").pack(side=tk.LEFT)
        v_end = tk.IntVar(value=bh.get('end'))
        tk.Spinbox(frame_bh, from_=1, to=24, textvariable=v_end, width=5).pack(side=tk.LEFT)
        frame_st = tk.LabelFrame(dlg, text="役職(持ち場)設定")#役職管理
        frame_st.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        lb_st = tk.Listbox(frame_st); lb_st.pack(fill=tk.BOTH, expand=True)
        for s in self.stations: lb_st.insert(tk.END, s)
        ent_st = tk.Entry(frame_st); ent_st.pack(fill=tk.X, padx=5, pady=2)
        def add_st():
            v = ent_st.get().strip()
            if v and v not in self.stations:
                self.stations.append(v); lb_st.insert(tk.END, v); ent_st.delete(0, tk.END)
        def del_st():
            sel = lb_st.curselection()
            if sel:
                idx = sel[0]; lb_st.delete(idx); self.stations.pop(idx)
        tk.Button(frame_st, text="追加", command=add_st).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_st, text="削除", command=del_st).pack(side=tk.LEFT)
        frame_sf = tk.LabelFrame(dlg, text="スタッフ設定")#スタッフ管理
        frame_sf.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        lb_sf = tk.Listbox(frame_sf); lb_sf.pack(fill=tk.BOTH, expand=True)
        for n in self.staffs: lb_sf.insert(tk.END, n)
        ent_sf = tk.Entry(frame_sf); ent_sf.pack(fill=tk.X, padx=5, pady=2)
        def add_sf():
            v = ent_sf.get().strip()
            if v and v not in self.staffs:
                self.staffs.append(v); lb_sf.insert(tk.END, v); ent_sf.delete(0, tk.END)
                self.config['staff'] = self.staffs; self.save_config()
        def del_sf():
            sel = lb_sf.curselection()
            if sel:
                idx = sel[0]; lb_sf.delete(idx); self.staffs.pop(idx);
                self.config['staff'] = self.staffs; self.save_config()
        tk.Button(frame_sf, text="追加", command=add_sf).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_sf, text="削除", command=del_sf).pack(side=tk.LEFT)
        def save_admin():#設定を保存する
            self.config['business_hours'] = {'start': v_start.get(), 'end': v_end.get()}
            self.config['stations'] = self.stations; self.config['staff'] = self.staffs
            self.save_config(); messagebox.showinfo("保存", "設定を保存しました。")
            dlg.destroy(); self.load_settings(); self.build_calendar()
        tk.Button(dlg, text="保存", command=save_admin).pack(pady=10)

    def open_day(self, day):#シフト作成画面の作成
        date = f"{self.year:04d}-{self.month:02d}-{day:02d}"
        dlg = tk.Toplevel(self.master)#他ウィンドウへのアクセスを禁止
        dlg.title(date + " シフト作成"); dlg.geometry("400x500"); dlg.transient(self.master); dlg.grab_set()
        tk.Label(dlg, text="出勤スタッフ", font=(None,12,'bold')).pack(pady=5)
        vars_sf = []; frame_s = tk.Frame(dlg); frame_s.pack(padx=10, fill=tk.X)
        for n in self.staffs:
            v = tk.BooleanVar(); tk.Checkbutton(frame_s, text=n, variable=v).pack(anchor=tk.W); vars_sf.append((n, v))
        frame_t = tk.Frame(dlg); frame_t.pack(fill=tk.BOTH, expand=True, pady=10)
        entries = []
        btn1 = tk.Button(dlg, text="確定"); btn2 = tk.Button(dlg, text="シフト作成"); btn2.pack_forget()
        def confirm():
            for w in frame_t.winfo_children(): w.destroy(); entries.clear()
            sel = [n for n,v in vars_sf if v.get()]
            if not sel: messagebox.showwarning("エラー", "スタッフ選択してください"); return #エラーメッセージ
            for idx,n in enumerate(sel):
                f = tk.Frame(frame_t); f.pack(fill=tk.X, pady=2)
                tk.Label(f, text=n, width=8).pack(side=tk.LEFT)
                vs = tk.StringVar(value=self.TIME_CHOICES[0]); tk.OptionMenu(f, vs, *self.TIME_CHOICES).pack(side=tk.LEFT, padx=5)
                ve = tk.StringVar(value=self.TIME_CHOICES[-1]); tk.OptionMenu(f, ve, *self.TIME_CHOICES).pack(side=tk.LEFT, padx=5)
                entries.append((n, vs, ve))
            btn2.pack(pady=10); btn1.config(state=tk.DISABLED)
        btn1.config(command=confirm); btn1.pack(pady=5); btn2.config(command=lambda: self.create_shift(date, entries, dlg))

    def create_shift(self, date, entries, dlg):#スタッフ/時間の表が表示され、csvファイルで保存される。
        sched = []
        TABLE_FILE = os.path.join(TABLE_DIR,date+".csv")
        FILE = open(TABLE_FILE,"w",encoding="utf-8")#table\<date>.csvを書き込みモードで開く
        for idx, (n, vs, ve) in enumerate(entries):
            st = datetime.datetime.strptime(vs.get(), "%H:%M")
            ed = datetime.datetime.strptime(ve.get(), "%H:%M")
            blocks = []
            current = st
            while current + datetime.timedelta(hours=1) <= ed:
                bs = current.strftime("%H:%M"); be = (current + datetime.timedelta(hours=1)).strftime("%H:%M")
                blocks.append({"staff": n, "start": bs, "end": be, "station": None}); current += datetime.timedelta(hours=1)
            if len(blocks) > 6:#スタッフの休憩時間を確保
                earliest = 2; latest = len(blocks) - 2
                if latest < earliest: pos = earliest
                else: pos = earliest + (idx % (latest - earliest + 1))
                br = blocks.pop(pos); blocks.insert(pos, {"staff": n, "start": br['start'], "end": br['end'], "station": "休憩"})
            ct = 0
            for blk in blocks:
                if blk['station'] == "休憩": sched.append(blk)
                else:
                    stn = self.stations[(idx + ct) % len(self.stations)]; blk['station'] = stn; sched.append(blk); ct += 1
        self.history[date] = sched
        json.dump(self.history, open(HISTORY_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)#daily_schedule.jsonを書き込みモードで開く
        dlg.destroy()
        res = tk.Toplevel(self.master); res.title(date + " シフト一覧")#他ウィンドウへのアクセスを禁止
        timeslots = [f"{h:02d}:00-{h+1:02d}:00" for h in range(self.bh_start, self.bh_end)]
        tk.Label(res, text="スタッフ/時間", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
        FILE.write(date)
        FILE.write("\n")
        FILE.write("スタッフ/時間,")
        for j, ts in enumerate(timeslots, 1):#時間を<00:00-00:00>の形式で表示、書き込み
            tk.Label(res, text=ts, borderwidth=1, relief="solid").grid(row=0, column=j, sticky="nsew")
            FILE.write(ts)
            FILE.write(",")
        FILE.write("\n")
        staff_list = list({rec['staff'] for rec in sched})#スタッフ名を表示、書き込み
        for i, stf in enumerate(staff_list, 1):
            tk.Label(res, text=stf, borderwidth=1, relief="solid").grid(row=i, column=0, sticky="nsew")
            FILE.write(stf)
            FILE.write(",")
            for j, ts in enumerate(timeslots, 1):#時間・スタッフ毎の役職を表示、書き込み
                bs, be = ts.split('-'); val = ""
                for rec in sched:
                    if rec['staff'] == stf and rec['start'] == bs and rec['end'] == be: val = rec['station']; break
                tk.Label(res, text=val, borderwidth=1, relief="solid").grid(row=i, column=j, sticky="nsew")
                FILE.write(val)
                FILE.write(",")
            FILE.write("\n")
        FILE.close()#table\<date>.csvを閉じる
        for c in range(len(timeslots) + 1): res.grid_columnconfigure(c, weight=1)
        for r in range(len(staff_list) + 1): res.grid_rowconfigure(r, weight=1)
        break_button=tk.Button(res, text="閉じる", command=res.destroy).grid(row=len(staff_list) + 1, column=0, columnspan=len(timeslots) + 1, pady=5)

if __name__ == '__main__':#MainAppのインスタンス生成
    root = tk.Tk()
    app=MainApp(root)
    root.mainloop()
