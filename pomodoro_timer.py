import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("ポモドーロタイマー")
        self.root.geometry("400x300")
        
        # タイマー設定（秒）
        self.pomodoro_duration = 25 * 60  # 25分
        self.current_time = self.pomodoro_duration
        self.is_running = False
        self.timer_job = None
        
        # 進捗データ（仮置きの値）
        self.completion_count = 2  # 今日の完了回数（仮置き）
        self.total_focus_time = 90  # 集中時間（分）（仮置き）
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """UIの設定"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 進捗表示エリア
        progress_frame = ttk.LabelFrame(main_frame, text="今日の進捗", padding="10")
        progress_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 完了回数表示
        ttk.Label(progress_frame, text="完了回数:").grid(row=0, column=0, sticky=tk.W)
        self.completion_label = ttk.Label(progress_frame, text="", font=("Arial", 12, "bold"))
        self.completion_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 集中時間表示
        ttk.Label(progress_frame, text="集中時間:").grid(row=1, column=0, sticky=tk.W)
        self.focus_time_label = ttk.Label(progress_frame, text="", font=("Arial", 12, "bold"))
        self.focus_time_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # タイマー表示
        self.timer_label = ttk.Label(main_frame, text="", font=("Arial", 24, "bold"))
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=20)
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 開始/停止ボタン
        self.start_stop_button = ttk.Button(button_frame, text="開始", command=self.toggle_timer)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # リセットボタン
        self.reset_button = ttk.Button(button_frame, text="リセット", command=self.reset_timer)
        self.reset_button.grid(row=0, column=1)
        
        # グリッドの重み設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def update_display(self):
        """表示の更新"""
        # 進捗表示の更新
        self.completion_label.config(text=f"{self.completion_count} 回")
        self.focus_time_label.config(text=f"{self.total_focus_time} 分")
        
        # タイマー表示の更新
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def toggle_timer(self):
        """タイマーの開始/停止切り替え"""
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """タイマー開始"""
        self.is_running = True
        self.start_stop_button.config(text="停止")
        self.run_timer()
    
    def stop_timer(self):
        """タイマー停止"""
        self.is_running = False
        self.start_stop_button.config(text="開始")
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
    
    def reset_timer(self):
        """タイマーリセット"""
        self.stop_timer()
        self.current_time = self.pomodoro_duration
        self.update_display()
    
    def run_timer(self):
        """タイマー実行"""
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            self.update_display()
            self.timer_job = self.root.after(1000, self.run_timer)
        elif self.current_time <= 0:
            # タイマーが0になった時の処理
            self.timer_completed()
    
    def timer_completed(self):
        """タイマー完了時の処理"""
        self.is_running = False
        self.start_stop_button.config(text="開始")
        
        # 進捗を更新
        self.completion_count += 1
        self.total_focus_time += 25  # 25分追加
        
        # 表示を更新
        self.update_display()
        
        # タイマーをリセット
        self.current_time = self.pomodoro_duration
        self.update_display()
        
        # 完了メッセージ
        print("ポモドーロ完了！進捗が更新されました。")


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()