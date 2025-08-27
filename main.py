#!/usr/bin/env python3
"""
ポモドーロタイマー - メインアプリケーション
Step 2: 進捗表示の追加
"""

import time
import threading
from datetime import datetime


class PomodoroTimer:
    """ポモドーロタイマーのメインクラス"""
    
    def __init__(self):
        # タイマー設定
        self.pomodoro_duration = 25 * 60  # 25分（実際の設定）
        self.demo_duration = 10  # デモ用短縮版
        self.current_time = self.demo_duration
        self.is_running = False
        
        # 進捗データ（フロントエンド仮置き値）
        self.completion_count = 2  # 今日の完了回数（仮置き）
        self.total_focus_time = 90  # 集中時間（分）（仮置き）
        
        # タイマー制御
        self.timer_thread = None
        self.should_stop = False
    
    def display_progress_ui(self):
        """今日の完了回数・集中時間の表示欄（UI）"""
        print("\n" + "="*60)
        print("                  📊 今日の進捗")
        print("="*60)
        print(f"🏆 完了回数: {self.completion_count} 回")
        print(f"⏱️  集中時間: {self.total_focus_time} 分")
        print(f"📅 日付: {datetime.now().strftime('%Y年%m月%d日')}")
        print("="*60)
    
    def display_timer(self):
        """タイマー表示"""
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        print(f"\r🍅 ポモドーロタイマー: {minutes:02d}:{seconds:02d}", end="", flush=True)
    
    def start_timer(self):
        """タイマー開始"""
        if self.is_running:
            print("\n⚠️  タイマーは既に実行中です")
            return False
        
        self.is_running = True
        self.should_stop = False
        print(f"\n🍅 ポモドーロタイマー開始！（{self.current_time}秒）")
        
        # タイマーを別スレッドで実行
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()
        return True
    
    def stop_timer(self):
        """タイマー停止"""
        if not self.is_running:
            return False
        
        self.should_stop = True
        self.is_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        print("\n⏸️  タイマーを停止しました")
        return True
    
    def reset_timer(self):
        """タイマーリセット"""
        self.stop_timer()
        self.current_time = self.demo_duration
        print(f"\n🔄 タイマーをリセットしました（{self.current_time}秒）")
    
    def run_timer(self):
        """タイマー実行（別スレッド）"""
        while self.is_running and self.current_time > 0 and not self.should_stop:
            self.display_timer()
            time.sleep(1)
            if not self.should_stop:
                self.current_time -= 1
        
        if self.current_time <= 0 and not self.should_stop:
            # タイマーが0になった時の処理
            self.timer_completed()
        
        self.is_running = False
    
    def timer_completed(self):
        """
        タイマー完了時の処理
        要件: タイマーが0になったら「完了回数」「集中時間」をフロント側で加算
        """
        print("\n\n🎉 ポモドーロ完了おめでとうございます！")
        
        # 旧値を記録
        old_completion = self.completion_count
        old_focus_time = self.total_focus_time
        
        # フロント側で進捗を加算
        self.completion_count += 1
        self.total_focus_time += 25  # 25分のポモドーロセッション
        
        print("\n📈 進捗更新:")
        print(f"   完了回数: {old_completion} → {self.completion_count} 回 (+1)")
        print(f"   集中時間: {old_focus_time} → {self.total_focus_time} 分 (+25)")
        
        # タイマーをリセット
        self.current_time = self.demo_duration
        
        # 更新された進捗表示
        self.display_progress_ui()
    
    def run_interactive_mode(self):
        """インタラクティブモード"""
        print("🍅 ポモドーロタイマー - Step 2: 進捗表示機能")
        print("=" * 60)
        print("実装機能:")
        print("✓ 今日の完了回数・集中時間の表示欄をUIに追加")
        print("✓ タイマーが0になったら進捗をフロント側で加算")
        print("=" * 60)
        
        # 初期進捗表示（仮置きデータ）
        self.display_progress_ui()
        
        print("\nコマンド:")
        print("  start  - タイマー開始")
        print("  stop   - タイマー停止") 
        print("  reset  - タイマーリセット")
        print("  status - 進捗表示")
        print("  quit   - 終了")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command in ['start', 's']:
                    self.start_timer()
                elif command in ['stop']:
                    self.stop_timer()
                elif command in ['reset', 'r']:
                    self.reset_timer()
                elif command in ['status', 'progress', 'p']:
                    self.display_progress_ui()
                elif command in ['quit', 'q', 'exit']:
                    self.stop_timer()
                    print("👋 ポモドーロタイマーを終了します")
                    break
                elif command == '':
                    continue
                else:
                    print("❌ 無効なコマンド: start/stop/reset/status/quit")
            
            except KeyboardInterrupt:
                self.stop_timer()
                print("\n\n👋 ポモドーロタイマーを終了します")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")


def main():
    """メインエントリーポイント"""
    timer = PomodoroTimer()
    timer.run_interactive_mode()


if __name__ == "__main__":
    main()