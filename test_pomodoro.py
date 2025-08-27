#!/usr/bin/env python3
"""
ポモドーロタイマー - テストスイート
Step 2: 進捗表示機能のテスト
"""

import unittest
import sys
import os

# テスト対象のモジュールをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import PomodoroTimer


class TestPomodoroProgressDisplay(unittest.TestCase):
    """進捗表示機能のテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.timer = PomodoroTimer()
    
    def test_initial_progress_values(self):
        """初期進捗値のテスト（仮置きデータ）"""
        # 要件: 値はフロントエンドで仮置き
        self.assertEqual(self.timer.completion_count, 2, "初期完了回数は2回（仮置き）")
        self.assertEqual(self.timer.total_focus_time, 90, "初期集中時間は90分（仮置き）")
    
    def test_timer_completion_increments_progress(self):
        """タイマー完了時の進捗加算テスト"""
        # 初期値を記録
        initial_completion = self.timer.completion_count
        initial_focus_time = self.timer.total_focus_time
        
        # タイマー完了処理を実行
        self.timer.timer_completed()
        
        # 要件: タイマーが0になったら加算
        self.assertEqual(
            self.timer.completion_count, 
            initial_completion + 1, 
            "完了回数が1増加する"
        )
        self.assertEqual(
            self.timer.total_focus_time, 
            initial_focus_time + 25, 
            "集中時間が25分増加する"
        )
    
    def test_multiple_timer_completions(self):
        """複数回のタイマー完了テスト"""
        initial_completion = self.timer.completion_count
        initial_focus_time = self.timer.total_focus_time
        
        # 3回タイマー完了を実行
        for _ in range(3):
            self.timer.timer_completed()
        
        # 3回分の加算確認
        self.assertEqual(
            self.timer.completion_count, 
            initial_completion + 3, 
            "完了回数が3増加する"
        )
        self.assertEqual(
            self.timer.total_focus_time, 
            initial_focus_time + 75,  # 25 * 3
            "集中時間が75分増加する"
        )
    
    def test_timer_reset_preserves_progress(self):
        """タイマーリセット時に進捗が保持されるテスト"""
        # 進捗を一度更新
        self.timer.timer_completed()
        progress_after_completion = self.timer.completion_count
        focus_time_after_completion = self.timer.total_focus_time
        
        # タイマーリセット
        self.timer.reset_timer()
        
        # 進捗データは保持される
        self.assertEqual(
            self.timer.completion_count, 
            progress_after_completion, 
            "リセット後も完了回数は保持される"
        )
        self.assertEqual(
            self.timer.total_focus_time, 
            focus_time_after_completion, 
            "リセット後も集中時間は保持される"
        )
        
        # タイマー時間はリセットされる
        self.assertEqual(
            self.timer.current_time, 
            self.timer.demo_duration, 
            "タイマー時間はリセットされる"
        )


class TestPomodoroTimerBasicFunctionality(unittest.TestCase):
    """タイマーの基本機能テスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.timer = PomodoroTimer()
    
    def test_timer_initialization(self):
        """タイマー初期化テスト"""
        self.assertFalse(self.timer.is_running, "初期状態でタイマーは停止中")
        self.assertEqual(self.timer.current_time, self.timer.demo_duration, "初期時間が正しく設定される")
    
    def test_timer_start_stop(self):
        """タイマー開始・停止テスト"""
        # 開始
        result = self.timer.start_timer()
        self.assertTrue(result, "タイマー開始が成功する")
        self.assertTrue(self.timer.is_running, "タイマーが実行中になる")
        
        # 停止
        result = self.timer.stop_timer()
        self.assertTrue(result, "タイマー停止が成功する")
        self.assertFalse(self.timer.is_running, "タイマーが停止中になる")
    
    def test_timer_reset(self):
        """タイマーリセットテスト"""
        # 時間を変更
        self.timer.current_time = 5
        
        # リセット
        self.timer.reset_timer()
        
        # 初期時間に戻る
        self.assertEqual(self.timer.current_time, self.timer.demo_duration, "時間が初期値にリセットされる")
        self.assertFalse(self.timer.is_running, "タイマーが停止状態になる")


def run_tests():
    """テスト実行"""
    print("🧪 ポモドーロタイマー - Step 2: 進捗表示機能テスト")
    print("=" * 60)
    
    # テストスイート作成
    suite = unittest.TestSuite()
    
    # 進捗表示機能のテスト
    suite.addTest(unittest.makeSuite(TestPomodoroProgressDisplay))
    
    # タイマー基本機能のテスト
    suite.addTest(unittest.makeSuite(TestPomodoroTimerBasicFunctionality))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 結果表示
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ すべてのテストが成功しました！")
        print("✓ 進捗表示UI機能")
        print("✓ 仮置きデータ設定")
        print("✓ タイマー完了時の加算処理")
        print("✓ 基本的なタイマー機能")
    else:
        print("❌ テストに失敗がありました")
        for failure in result.failures:
            print(f"  FAIL: {failure[0]}")
        for error in result.errors:
            print(f"  ERROR: {error[0]}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)