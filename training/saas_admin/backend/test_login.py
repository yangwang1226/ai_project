"""
测试脚本 - 用于测试登录功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
from models import User, Tenant, VerificationCode
from services import create_verification_code, verify_code, create_user
from schemas import UserCreate
from datetime import datetime

# 创建数据库表
print("创建数据库表...")
Base.metadata.create_all(bind=engine)
print("✓ 数据库表创建成功")

# 创建数据库会话
db = SessionLocal()

try:
    # 测试手机号
    test_phone = "13800138000"
    
    # 1. 清理旧数据
    print(f"\n清理测试用户 {test_phone} 的旧数据...")
    db.query(User).filter(User.phone == test_phone).delete()
    db.query(VerificationCode).filter(VerificationCode.phone == test_phone).delete()
    db.commit()
    print("✓ 清理完成")
    
    # 2. 创建验证码
    print(f"\n为 {test_phone} 创建验证码...")
    code = create_verification_code(db, test_phone)
    print(f"✓ 验证码创建成功: {code}")
    
    # 3. 验证验证码
    print(f"\n验证验证码 {code}...")
    is_valid = verify_code(db, test_phone, code)
    print(f"✓ 验证码验证: {'通过' if is_valid else '失败'}")
    
    # 4. 重新生成验证码（因为上一步验证后已使用）
    print(f"\n重新生成验证码...")
    code = create_verification_code(db, test_phone)
    print(f"✓ 新验证码: {code}")
    
    # 5. 创建测试用户
    print(f"\n创建测试用户...")
    user_data = UserCreate(
        phone=test_phone,
        nickname="测试用户",
        verification_code=code,
        invite_code=None
    )
    user = create_user(db, user_data)
    print(f"✓ 用户创建成功: ID={user.id}, 手机号={user.phone}, 角色={user.role}")
    
    # 6. 查询所有用户
    print("\n当前所有用户:")
    users = db.query(User).all()
    for u in users:
        print(f"  - ID: {u.id}, 手机号: {u.phone}, 昵称: {u.nickname}, 角色: {u.role}, 租户ID: {u.tenant_id}")
    
    # 7. 生成新验证码用于登录测试
    print(f"\n生成登录测试验证码...")
    login_code = create_verification_code(db, test_phone)
    print(f"✓ 登录验证码: {login_code}")
    
    print("\n" + "="*50)
    print("测试完成！")
    print("="*50)
    print(f"\n📱 测试登录信息:")
    print(f"手机号: {test_phone}")
    print(f"验证码: {login_code}")
    print("\n你可以使用上面的信息在前端进行登录测试")
    
except Exception as e:
    print(f"\n❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

