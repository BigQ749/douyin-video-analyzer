"""基础测试：验证各模块能否正常导入"""
import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestImports(unittest.TestCase):
    """测试依赖能否导入"""
    
    def test_faster_whisper(self):
        """faster-whisper 可用"""
        from faster_whisper import WhisperModel
        self.assertTrue(WhisperModel)
    
    def test_playwright(self):
        """playwright 可用"""
        from playwright.sync_api import sync_playwright
        self.assertTrue(sync_playwright)
    
    def test_yaml(self):
        """yaml 可用"""
        import yaml
        self.assertTrue(yaml)
    
    def test_ffmpeg(self):
        """ffmpeg 可用"""
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
