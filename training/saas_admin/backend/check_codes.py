# 创建文件：saas_admin/backend/check_codes.py
from database import SessionLocal
from models import VerificationCode
from datetime import datetime

db = SessionLocal()
codes = db.query(VerificationCode).filter(
    VerificationCode.expires_at > datetime.now()
).all()

print("当前有效的验证码：")
for c in codes:
    print(f"手机号: {c.phone}, 验证码: {c.code}, 已使用: {c.used}, 过期时间: {c.expires_at}")

db.close()