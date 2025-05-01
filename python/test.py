# tkと書けばtkinter(標準ライブラリ)の機能が使える
import tkinter as tk
# 日付と時刻に関するライブラリ
import datetime


# GUIの操作画面をつくるクラス
class MainApp(tk.Frame): 
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # ウィンドウ設定
        master.geometry("700x500") # ウィンドウの大きさ指定
        master.title("Sample") # タイトル

        self.make_widgets()

    # ウィジェットの入れ子
    def make_widgets(self):
        # 内部フレーム1
        set_frame = tk.Frame(self)
        set_frame.pack(side=tk.LEFT)

        # 管理者用設定
        pass_comment=tk.Label(set_frame,text="パスワード")
        pass_comment.pack()
        write_pass=tk.Entry(set_frame)
        write_pass.pack()
        adm_set = tk.Button(set_frame, text="管理者用画面",command=self.adm_window)
        adm_set.pack(anchor=tk.W)
        
        """
        カレンダーを作る
        """
        # 内部フレーム2
        frame2 = tk.Frame(self)
        frame2.pack(side=tk.LEFT)

        # 内部フレーム2の内部フレーム
        cal_text = tk.Frame(frame2)
        cal_text.pack()
        cal_week = tk.Frame(frame2)
        cal_week.pack()
        cal1 = tk.Frame(frame2)
        cal1.pack()
        cal2 = tk.Frame(frame2)
        cal2.pack()
        cal3 = tk.Frame(frame2)
        cal3.pack()
        cal4 = tk.Frame(frame2)
        cal4.pack()
        cal5 = tk.Frame(frame2)
        cal5.pack()     
        
        # カレンダー
        label_c1 = tk.Label(cal_text,text="スケジュール")
        label_c1.pack()
        # 年月
        now = datetime.datetime.now() # 今日の日付等を取得
        back_month = tk.Button(cal_text,text="<")
        back_month.pack(side="left")
        label_year = tk.Label(cal_text,text=now.year)
        label_year.pack(side="left")
        label_c2 = tk.Label(cal_text,text="/")
        label_c2.pack(side="left")
        label_month = tk.Label(cal_text,text=now.month)
        label_month.pack(side="left")
        after_month = tk.Button(cal_text,text=">")
        after_month.pack(side="left")
        # 曜日
        #weeks=['日','月','火','水','木','金','土']
        #for week in weeks:
         #   days = tk.Label(cal_week,text=week)
          #  days.pack(side="left",ipadx=25)
            
        # 日付の記載されたボタンを作る
        j=0
        for i in range(7):
            days = tk.Button(cal1,text=i+1+j*7,width=5,height=3,command=self.new_window)
            days.pack(side="left")
        j=j+1
        for i in range(7):
            days = tk.Button(cal2,text=i+1+j*7,width=5,height=3,command=self.new_window)
            days.pack(side="left")
        j=j+1
        for i in range(7):
            days = tk.Button(cal3,text=i+1+j*7,width=5,height=3,command=self.new_window)
            days.pack(side="left")
        j=j+1
        for i in range(7):
            days = tk.Button(cal4,text=i+1+j*7,width=5,height=3,command=self.new_window)
            days.pack(side="left")
        j=j+1
        if now.month==2:
            if now.year%400==0:
                for i in range(1):
                    days = tk.Button(cal5,text=i+1+j*7,width=5,height=3,command=self.new_window)
                    days.pack(side="left")
                for i in range(7-1):
                    days = tk.Button(cal5,text=i+1,width=5,height=3,bg="gray",command=self.new_window)
                    days.pack(side="left")
            elif now.year%100!=0&now.year%4==0:
                for i in range(1):
                    days = tk.Button(cal5,text=i+1+j*7,width=5,height=3,command=self.new_window)
                    days.pack(side="left")
                for i in range(7-1):
                    days = tk.Button(cal5,text=i+1,width=5,height=3,bg="gray",command=self.new_window)
                    days.pack(side="left")
        elif now.month==4|now.month==6|now.month==9|now.month==11:
            for i in range(2):
                days = tk.Button(cal5,text=i+1+j*7,width=5,height=3,command=self.new_window)
                days.pack(side="left")
            for i in range(7-2):
                days = tk.Button(cal5,text=i+1,width=5,height=3,bg="gray",command=self.new_window)
                days.pack(side="left")
        else:
            for i in range(3):
                days = tk.Button(cal5,text=i+1+j*7,width=5,height=3,command=self.new_window)
                days.pack(side="left")
            for i in range(7-3):
                days = tk.Button(cal5,text=i+1,width=5,height=3,bg="gray",command=self.new_window)
                days.pack(side="left")

    # 記入or確認画面
    def new_window(self):
        new=tk.Toplevel(root)
        new.geometry("300x400")
        # 前面に表示
        new.transient(root)
        # 他ウィンドウへのアクセス禁止
        new.grab_set()

        # 戻るボタン
        new_back=tk.Button(new,text="<戻る",command=new.destroy)
        new_back.pack(anchor=tk.W)

        # コマ(仮に3時間毎のシフトとする, 修正すること)
        comment_label=tk.Label(new,text="※仮に3時間毎のシフトとする")# 削除すること
        comment_label.pack()# 削除すること
        shift_button=tk.Button(new,text="9:00~12:00",width=15,height=2)
        shift_button.pack()
        shift_button=tk.Button(new,text="12:00~15:00",width=15,height=2)
        shift_button.pack()
        shift_button=tk.Button(new,text="15:00~18:00",width=15,height=2)
        shift_button.pack()
        shift_button=tk.Button(new,text="18:00~21:00",width=15,height=2)
        shift_button.pack()

        # 登録番号、名前など個人を識別する文字列
        who_label=tk.Label(new,text="登録番号を半角で入力")
        who_label.pack()
        # 入力スペース

        # 登録ボタン
        new_shift=tk.Button(new,text="登録",width=7,bg="lightgreen")
        new_shift.pack(side="left")
        # キャンセルボタン
        cancel_shift=tk.Button(new,text="キャンセル",width=7,bg="pink")
        cancel_shift.pack(side="left")

    # ファイル読み込み
    #def read_file(self):
    # 記録
    #def write_file(self):

    # 店舗設定制御
    #

    # 年月の<>ボタン制御
    #

    """
    シフト日時について
    """
    # 登録ボタン制御
    #

    # キャンセルボタン制御
    #
    
    """
    人員整理について
    """
    # 管理ボタン制御
    #

    """
    管理者画面
    """
    def adm_window(self):
        new=tk.Toplevel(root)
        new.geometry("300x400")
        # 設定
        label_set1 = tk.Label(new, text="設定")
        label_set1.pack()
        
        # テキスト
        label_set2 = tk.Label(new, text="要素を選択")
        label_set2.pack()

        # チェックボックスの状態を格納する変数
        check1 = tk.BooleanVar()
        check2 = tk.BooleanVar()
        check3 = tk.BooleanVar()
        check4 = tk.BooleanVar()
        check5 = tk.BooleanVar()

        """
        集客に関わる要素を選択する
        """
        # チェックボックス
        check_box1 = tk.Checkbutton(new,text="天気",variable=check1)
        check_box1.pack()
        
        check_box2 = tk.Checkbutton(new,text="？？",variable=check2)
        check_box2.pack()

        check_box3 = tk.Checkbutton(new,text="？？",variable=check3)
        check_box3.pack()

        check_box4 = tk.Checkbutton(new,text="？？",variable=check4)
        check_box4.pack()

        check_box5 = tk.Checkbutton(new,text="？？",variable=check5)
        check_box5.pack()

        # 決定ボタン
        decide = tk.Button(new,text="決定")
        decide.pack()

        
# イベントループ
if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(master=root)
    root.mainloop()
    
