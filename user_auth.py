"""
配置管理模块 - 漏洞测试
包含两个安全问题示例
"""

import os
import pickle
import subprocess
import json

# 导入保护：防止在生产环境中导入
if os.getenv("APP_ENV") == "production":
    raise ImportError("user_auth 模块仅用于测试，禁止在生产环境中导入")

class ConfigManager:
    def __init__(self, config_dir):
        if not os.path.exists(config_dir) or not os.path.isdir(config_dir):
            raise ValueError(f"Invalid config directory: {config_dir}")
        self.config_dir = os.path.abspath(config_dir)
    def save_config(self, filename, data):
        """保存配置 - 不安全的反序列化"""
        file_path = os.path.join(self.config_dir, filename)
        
        # 使用 pickle 存储数据，存在反序列化漏洞
        with open(file_path, 'wb') as f:
            with open(file_path, 'w') as f:
                json.dump(data, f)  # 使用JSON进行安全序列化
            
        
        print(f"配置已保存到 {file_path}")
        return True
    
    def get_config_list(self, search_pattern):
        """列出配置文件 - 命令注入风险"""
        cmd = f"ls {self.config_dir} | grep {search_pattern}"  # ❌ 命令注入风险
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            return output.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"列出配置文件失败: {e.output}")
            return []

# 仅用于演示
if __name__ == "__main__":
    manager = ConfigManager("/etc/app/configs")
    manager.save_config("test_config.pkl", {"key": "value"})
    manager.get_config_list("test")