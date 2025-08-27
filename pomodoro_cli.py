import time
import threading
from datetime import datetime


class PomodoroTimer:
    def __init__(self):
        # タイマー設定（秒）
        self.pomodoro_duration = 25 * 60  # 25分（実際のアプリ用）
        self.demo_duration = 5  # デモ用に5秒
        self.current_time = self.demo_duration  # デモ用
        self.is_running = False
        
        # 進捗データ（仮置きの値）
        self.completion_count = 2  # 今日の完了回数（仮置き）
        self.total_focus_time = 90  # 集中時間（分）（仮置き）
        
        self.timer_thread = None
        self.should_stop = False
    
    def display_progress(self):
        """進捗表示"""
        print("\n" + "="*40)
        print("          今日の進捗")
        print("="*40)
        print(f"完了回数: {self.completion_count} 回")
        print(f"集中時間: {self.total_focus_time} 分")
        print("="*40)
    
    def display_timer(self):
        """タイマー表示"""
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        print(f"\rタイマー: {minutes:02d}:{seconds:02d}", end="", flush=True)
    
    def start_timer(self):
        """タイマー開始"""
        if self.is_running:
            print("\nタイマーは既に実行中です")
            return
        
        self.is_running = True
        self.should_stop = False
        print(f"\nポモドーロタイマー開始！（{self.current_time}秒 - デモ用）")
        
        # タイマーを別スレッドで実行
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()
    
    def stop_timer(self):
        """タイマー停止"""
        if not self.is_running:
            print("\nタイマーは実行されていません")
            return
        
        self.should_stop = True
        self.is_running = False
        print("\nタイマーを停止しました")
    
    def reset_timer(self):
        """タイマーリセット"""
        self.stop_timer()
        self.current_time = self.demo_duration  # デモ用
        print(f"\nタイマーをリセットしました（{self.current_time}秒）")
    
    def run_timer(self):
        """タイマー実行（別スレッド）"""
        while self.is_running and self.current_time > 0 and not self.should_stop:
            self.display_timer()
            time.sleep(1)
            self.current_time -= 1
        
        if self.current_time <= 0 and not self.should_stop:
            # タイマーが0になった時の処理
            self.timer_completed()
        
        self.is_running = False
    
    def timer_completed(self):
        """タイマー完了時の処理"""
        print("\n\n🎉 ポモドーロ完了！")
        
        # 進捗を更新（フロント側で加算）
        self.completion_count += 1
        self.total_focus_time += 25  # 25分追加
        
        print("進捗が更新されました：")
        print(f"  完了回数: {self.completion_count - 1} → {self.completion_count} 回")
        print(f"  集中時間: {self.total_focus_time - 25} → {self.total_focus_time} 分")
        
        # タイマーをリセット
        self.current_time = self.demo_duration  # デモ用
        
        # 更新された進捗を表示
        self.display_progress()
    
    def run_interactive(self):
        """インタラクティブモード"""
        print("ポモドーロタイマー - Step 2: 進捗表示の追加")
        print("コマンド: start(開始), stop(停止), reset(リセット), progress(進捗表示), quit(終了)")
        
        # 初期進捗表示
        self.display_progress()
        
        while True:
            try:
                command = input("\nコマンドを入力: ").strip().lower()
                
                if command in ['start', 's']:
                    self.start_timer()
                elif command in ['stop']:
                    self.stop_timer()
                elif command in ['reset', 'r']:
                    self.reset_timer()
                elif command in ['progress', 'p']:
                    self.display_progress()
                elif command in ['quit', 'q', 'exit']:
                    self.stop_timer()
                    print("ポモドーロタイマーを終了します")
                    break
                else:
                    print("無効なコマンドです。start/stop/reset/progress/quit を使用してください")
            
            except KeyboardInterrupt:
                self.stop_timer()
                print("\n\nポモドーロタイマーを終了します")
                break


def main():
    timer = PomodoroTimer()
    timer.run_interactive()


if __name__ == "__main__":
    main()