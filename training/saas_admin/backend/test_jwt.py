from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

# 使用相同的配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-please-change-in-production")
ALGORITHM = "HS256"

print("="*60)
print("JWT测试")
print("="*60)

# 测试数据
test_data = {"sub": 1, "phone": "13800138000"}

# 创建Token
print(f"\n1. 创建Token")
print(f"   数据: {test_data}")
print(f"   SECRET_KEY: {SECRET_KEY[:20]}...")
print(f"   ALGORITHM: {ALGORITHM}")

expire = datetime.utcnow() + timedelta(minutes=30)
to_encode = test_data.copy()
to_encode.update({"exp": expire})

try:
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"   ✓ Token生成成功")
    print(f"   Token: {token[:80]}...")
except Exception as e:
    print(f"   ✗ Token生成失败: {e}")
    exit(1)

# 验证Token
print(f"\n2. 验证Token")
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"   ✓ Token验证成功")
    print(f"   解码数据: {payload}")
    
    user_id = payload.get("sub")
    phone = payload.get("phone")
    print(f"   user_id: {user_id}")
    print(f"   phone: {phone}")
except JWTError as e:
    print(f"   ✗ Token验证失败: {e}")
except Exception as e:
    print(f"   ✗ 未知错误: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)