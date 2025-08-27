import time


class PomodoroProgressDemo:
    def __init__(self):
        # 進捗データ（仮置きの値）
        self.completion_count = 2  # 今日の完了回数（仮置き）
        self.total_focus_time = 90  # 集中時間（分）（仮置き）
    
    def display_progress(self):
        """進捗表示UI"""
        print("\n" + "="*50)
        print("           今日の進捗表示")
        print("="*50)
        print(f"📊 完了回数: {self.completion_count} 回")
        print(f"⏱️  集中時間: {self.total_focus_time} 分")
        print("="*50)
    
    def timer_demo(self, duration=3):
        """タイマーのデモ（短時間版）"""
        print(f"\n🍅 ポモドーロタイマー開始！（{duration}秒デモ）")
        
        for remaining in range(duration, 0, -1):
            minutes = remaining // 60
            seconds = remaining % 60
            print(f"\r⏰ タイマー: {minutes:02d}:{seconds:02d}", end="", flush=True)
            time.sleep(1)
        
        print("\r⏰ タイマー: 00:00")
        return self.timer_completed()
    
    def timer_completed(self):
        """タイマー完了時の処理（フロント側で加算）"""
        print("\n\n🎉 ポモドーロ完了！")
        
        # 旧値を保存
        old_completion = self.completion_count
        old_focus_time = self.total_focus_time
        
        # 進捗を更新（要件：タイマーが0になったら加算）
        self.completion_count += 1
        self.total_focus_time += 25  # 25分追加
        
        print("\n📈 進捗が更新されました：")
        print(f"   完了回数: {old_completion} → {self.completion_count} 回 (+1)")
        print(f"   集中時間: {old_focus_time} → {self.total_focus_time} 分 (+25)")
        
        return True
    
    def run_demo(self):
        """デモ実行"""
        print("🍅 ポモドーロタイマー - Step 2: 進捗表示の追加")
        print("✨ 要件実装確認:")
        print("   1. 今日の完了回数・集中時間の表示欄をUIに追加（値はフロントエンドで仮置き）")
        print("   2. タイマーが0になったら「完了回数」「集中時間」をフロント側で加算")
        
        # 初期状態の進捗表示
        print("\n📋 初期状態（仮置きデータ）:")
        self.display_progress()
        
        input("\nEnterキーでタイマーデモを開始...")
        
        # タイマー実行とカウント更新のデモ
        self.timer_demo(3)  # 3秒デモ
        
        # 更新後の進捗表示
        print("\n📋 更新後の進捗:")
        self.display_progress()
        
        print("\n✅ 実装完了確認:")
        print("   ✓ 進捗表示UI追加済み")
        print("   ✓ 仮置きデータ設定済み")
        print("   ✓ タイマー完了時の加算処理実装済み")


def main():
    demo = PomodoroProgressDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()