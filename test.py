"""
用户管理系统 - 包含多种代码质量问题的测试文件
用于验证智能代码审查工具的检测能力
"""

import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText


class UserManager:
    """
    用户管理类
    警告：此代码包含故意设计的安全漏洞和代码质量问题，仅用于教学演示！
    """
    
    def __init__(self):
        # 🔴 问题1: 硬编码数据库凭证 (CWE-798)
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "Admin@123456"  # 硬编码密码
        self.db_name = "user_db"
        
        # 🔴 问题2: 硬编码API密钥
        self.api_key = "sk-1234567890abcdef1234567890abcdef"
        
        # 🔴 问题3: 硬编码邮箱密码
        self.email_password = "MyEmailPass123"
        
        self.connection = self._connect_db()
    
    def _connect_db(self):
        """连接数据库"""
        conn = sqlite3.connect(f"{self.db_name}.db")
        return conn
    
    # ==================== 认证相关方法 ====================
    
    def login(self, username, password):
        """
        用户登录
        🔴 问题4: SQL注入漏洞 (CWE-89) - Critical
        """
        # 直接拼接SQL，未使用参数化查询
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        cursor = self.connection.cursor()
        result = cursor.execute(query).fetchall()
        
        if result:
            return {"status": "success", "user": result[0]}
        else:
            return {"status": "failed"}
    
    def register(self, username, password, email):
        """
        用户注册
        🔴 问题5: SQL注入漏洞 (CWE-89)
        """
        # 同样的SQL注入问题
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
        return {"status": "success", "message": "User registered"}
    
    def authenticate_user(self, token):
        """
        验证用户token
        🔴 问题6: SQL注入漏洞
        """
        query = f"SELECT * FROM users WHERE token='{token}'"
        cursor = self.connection.cursor()
        return cursor.execute(query).fetchone()
    
    def reset_password(self, username, new_password):
        """
        重置密码
        🔴 问题7: SQL注入 + 明文存储密码
        """
        query = f"UPDATE users SET password='{new_password}' WHERE username='{username}'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
    
    # ==================== 通知相关方法 ====================
    
    def send_welcome_email(self, user_email, username):
        """
        发送欢迎邮件
        🔴 问题8: XSS漏洞 (CWE-79) - 如果用于Web
        """
        # 未转义用户输入，直接插入HTML
        html_content = f"""
        <html>
            <body>
                <h1>Welcome {username}!</h1>
                <p>Your email is: {user_email}</p>
            </body>
        </html>
        """
        
        # 发送邮件的代码（简化版）
        msg = MIMEText(html_content, 'html')
        msg['Subject'] = 'Welcome!'
        msg['From'] = 'admin@example.com'
        msg['To'] = user_email
        
        # 实际不会真的发送
        return html_content
    
    def display_user_profile(self, user_input):
        """
        显示用户资料
        🔴 问题9: XSS漏洞 (CWE-79)
        """
        # 未对用户输入进行HTML转义
        html = f"<div class='profile'><h2>{user_input}</h2></div>"
        return html
    
    def send_notification(self, user_id, message):
        """
        发送通知
        🔴 问题10: XSS漏洞
        """
        # 从数据库获取用户信息（含SQL注入风险）
        query = f"SELECT email FROM users WHERE id={user_id}"
        cursor = self.connection.cursor()
        result = cursor.execute(query).fetchone()
        
        if result:
            email = result[0]
            # 未转义message
            html_message = f"<p>Notification: {message}</p>"
            # 发送邮件...
            return html_message
    
    # ==================== 计算相关方法 ====================
    
    def calculate_user_discount(self, user_type, amount):
        """
        计算用户折扣
        🔴 问题11: 代码重复 (与calculate_user_tax类似)
        """
        if user_type == "VIP":
            discount = amount * 0.2
        elif user_type == "Premium":
            discount = amount * 0.15
        elif user_type == "Regular":
            discount = amount * 0.1
        elif user_type == "New":
            discount = amount * 0.05
        else:
            discount = 0
        
        final_amount = amount - discount
        return final_amount
    
    def calculate_user_tax(self, user_type, amount):
        """
        计算用户税费
        🔴 问题12: 代码重复 (逻辑与calculate_user_discount几乎相同)
        """
        if user_type == "VIP":
            tax = amount * 0.15
        elif user_type == "Premium":
            tax = amount * 0.18
        elif user_type == "Regular":
            tax = amount * 0.20
        elif user_type == "New":
            tax = amount * 0.22
        else:
            tax = amount * 0.25
        
        final_amount = amount + tax
        return final_amount
    
    def calculate_shipping_fee(self, user_type, distance):
        """
        计算运费
        🔴 问题13: 重复的条件判断模式
        """
        if user_type == "VIP":
            fee = distance * 0.5
        elif user_type == "Premium":
            fee = distance * 0.7
        elif user_type == "Regular":
            fee = distance * 1.0
        elif user_type == "New":
            fee = distance * 1.2
        else:
            fee = distance * 1.5
        
        return fee
    
    # ==================== 报表相关方法 ====================
    
    def generate_user_report(self, user_id):
        """
        生成用户报表
        🔴 问题14: SQL注入 + 过长方法 + 高复杂度
        """
        # SQL注入风险
        query = f"SELECT * FROM users WHERE id={user_id}"
        cursor = self.connection.cursor()
        user_data = cursor.execute(query).fetchone()
        
        if not user_data:
            return None
        
        # 复杂的报表生成逻辑（圈复杂度高）
        report = {}
        
        if user_data[3] == "VIP":
            report['level'] = 'VIP'
            report['discount'] = 20
            if user_data[4] > 10000:
                report['bonus'] = 'Gold Badge'
                if user_data[5] > 50:
                    report['extra'] = 'Free Shipping'
                else:
                    report['extra'] = 'Priority Support'
            else:
                report['bonus'] = 'Silver Badge'
        elif user_data[3] == "Premium":
            report['level'] = 'Premium'
            report['discount'] = 15
            if user_data[4] > 5000:
                report['bonus'] = 'Silver Badge'
            else:
                report['bonus'] = 'Bronze Badge'
        else:
            report['level'] = 'Regular'
            report['discount'] = 10
        
        # 更多复杂的判断...
        if user_data[6] == True:
            report['verified'] = 'Yes'
            if user_data[7] > 100:
                report['trust_score'] = 'High'
            else:
                report['trust_score'] = 'Medium'
        else:
            report['verified'] = 'No'
            report['trust_score'] = 'Low'
        
        return report
    
    def export_users_to_csv(self, filename):
        """
        导出用户到CSV
        🔴 问题15: 路径遍历漏洞 (CWE-22)
        """
        # 未验证filename，可能导致路径遍历
        query = "SELECT * FROM users"
        cursor = self.connection.cursor()
        users = cursor.execute(query).fetchall()
        
        # 直接使用用户提供的文件名
        with open(filename, 'w') as f:
            for user in users:
                f.write(str(user) + '\n')
    
    # ==================== 管理相关方法 ====================
    
    def delete_user(self, user_id):
        """
        删除用户
        🔴 问题16: SQL注入
        """
        query = f"DELETE FROM users WHERE id={user_id}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
    
    def search_users(self, keyword):
        """
        搜索用户
        🔴 问题17: SQL注入
        """
        # LIKE查询也存在注入风险
        query = f"SELECT * FROM users WHERE username LIKE '%{keyword}%'"
        cursor = self.connection.cursor()
        return cursor.execute(query).fetchall()
    
    def update_user_role(self, username, new_role):
        """
        更新用户角色
        🔴 问题18: SQL注入 + 权限控制缺失
        """
        query = f"UPDATE users SET role='{new_role}' WHERE username='{username}'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
    
    # ==================== 统计相关方法 ====================
    
    def get_user_statistics(self):
        """
        获取用户统计
        🔴 问题19: 方法过长 + 复杂度高
        """
        stats = {}
        
        # 统计总用户数
        cursor = self.connection.cursor()
        total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        stats['total'] = total_users
        
        # 统计各类型用户
        vip_count = cursor.execute("SELECT COUNT(*) FROM users WHERE type='VIP'").fetchone()[0]
        premium_count = cursor.execute("SELECT COUNT(*) FROM users WHERE type='Premium'").fetchone()[0]
        regular_count = cursor.execute("SELECT COUNT(*) FROM users WHERE type='Regular'").fetchone()[0]
        
        stats['vip'] = vip_count
        stats['premium'] = premium_count
        stats['regular'] = regular_count
        
        # 计算百分比
        if total_users > 0:
            stats['vip_percent'] = (vip_count / total_users) * 100
            stats['premium_percent'] = (premium_count / total_users) * 100
            stats['regular_percent'] = (regular_count / total_users) * 100
        
        # 统计活跃用户
        active_users = cursor.execute("SELECT COUNT(*) FROM users WHERE active=1").fetchone()[0]
        stats['active'] = active_users
        
        if total_users > 0:
            stats['active_rate'] = (active_users / total_users) * 100
        
        return stats


# 🔴 问题20: 在模块级别执行危险操作
if __name__ == "__main__":
    # 创建实例时就暴露了凭证
    manager = UserManager()
    
    # 测试用例（演示如何被攻击）
    # 攻击示例1: SQL注入
    malicious_input = "admin' OR '1'='1"
    result = manager.login(malicious_input, "anything")
    print(result)
    
    # 攻击示例2: XSS
    xss_payload = "<script>alert('XSS')</script>"
    html = manager.display_user_profile(xss_payload)
    print(html)