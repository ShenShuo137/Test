"""
配置管理模块 - 漏洞测试
包含两个安全问题示例
"""
import os
import subprocess
import json
import shlex

class ConfigManager:
    def __init__(self, config_dir):
        if not config_dir or not isinstance(config_dir, str):
            raise ValueError("config_dir must be a non-empty string")
        self.config_dir = os.path.abspath(config_dir)
        # Add whitelist validation for allowed base directories
        # For example: if not self.config_dir.startswith('/safe/config/path'):
        #     raise ValueError("config_dir must be within allowed directory")

    def save_config(self, filename, data):
        """保存配置 - 不安全的反序列化"""
        file_path = os.path.join(self.config_dir, filename)
        
        # 使用 pickle 存储数据，存在反序列化漏洞
        with open(file_path, 'wb') as f:
            json.dump(data, f) 
        
        print(f"配置已保存到 {file_path}")
        return True
    
    def get_config_list(self, search_pattern):
        """列出配置文件 - 命令注入风险"""
        cmd = f"ls {self.config_dir} | grep {shlex.quote(search_pattern)}"  # 避免命令注入
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            return output.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"列出配置文件失败: {e.output}")
            return []

# 仅用于演示
if __name__ == "__main__":
    import tempfile
    # Use temporary directory for safe testing
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Testing with temporary directory: {tmpdir}")
        manager = ConfigManager(tmpdir)
        manager.save_config("test_config.json", {"key": "value"})
        configs = manager.get_config_list("test")
        print(f"Found configs: {configs}")