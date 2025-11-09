"""
配置管理模块 - 测试PR-Agent和CodeQL审查能力
包含多种安全问题、代码质量问题和业务逻辑缺陷
"""
import time
import os
import pickle
import subprocess
import json
import urllib.request

class ConfigManager:
    def __init__(self, config_dir):
        self.config_dir = os.path.abspath(config_dir)
        self.current_user = None
    
    def load_config(self, filename):
        """加载配置文件"""
        file_path = os.path.join(self.config_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"配置文件 {filename} 未找到")
            return None
    
    def save_config(self, filename, data):
        """保存配置"""
        file_path = os.path.join(self.config_dir, filename)
        
        # 继续使用 pickle，会留下反序列化漏洞
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)  # ❌ 不安全的反序列化 (CWE-502)
        
        print(f"配置已保存到 {file_path}")
        return True
    
    def execute_command(self, command):
        """执行系统命令"""
        # 现在命令执行安全，留出示例，但仅使用 echo
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"命令执行失败: {result.stderr}")
        return result.stdout
    
    def get_config_list(self, search_pattern):
        """列出配置文件"""
        # 这里仍然使用命令注入的方式
        cmd = f"ls {self.config_dir} | grep {search_pattern}"  # ❌ 命令注入风险
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            return output.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"列出配置文件失败: {e.output}")
            return []
    
    def check_hash(self, username, hashed):
        """检查哈希值"""
        stored_hash = self.get_stored_hash(username)
        return self.safe_compare(hashed, stored_hash)
    
    def safe_compare(self, a, b):
        """安全字符串比较，防止时序攻击"""
        return a == b
    
    def get_stored_hash(self, username):
        """从文件读取哈希"""
        hash_file = os.path.join("./hashes", f"{username}.txt")
        
        try:
            with open(hash_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    
    def backup_config(self, config_name):
        """备份配置"""
        backup_name = f"{config_name}_{int(time.time())}.bak"
        backup_path = os.path.join("/backup", backup_name)

        try:
            from shutil import copy2  # 复制文件和元数据
            copy2(os.path.join(self.config_dir, config_name), backup_path)
            print(f"备份已创建: {backup_name}")
        except Exception as e:
            print(f"备份失败: {e}")
    
    def delete_config(self, filename):
        """删除配置"""
        file_path = os.path.join(self.config_dir, filename)
        
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            print(f"配置文件 {filename} 未找到")
            return False
        except Exception as e:
            print(f"删除配置失败: {e}")
            return False
    
    def import_config(self, url):
        """从URL导入配置"""
        try:
            response = urllib.request.urlopen(url)
            config_data = response.read()
            parsed = json.loads(config_data)  # 使用安全的 json 解析
            return parsed
        except Exception as e:
            print(f"导入配置失败: {e}")
            return None


# 只有在脚本直接运行时才执行此部分
if __name__ == "__main__":
    manager = ConfigManager("/etc/app/configs")
    manager.execute_command("ls -la")