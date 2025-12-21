from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import User, Tenant, Scene, UsageRecord, RechargeRecord, VerificationCode, RoleEnum
from schemas import UserCreate, TenantCreate, SceneCreate, UsageRecordCreate, RechargeRecordCreate
from auth import get_password_hash
import random
import string

# ===== 验证码服务 =====
def generate_verification_code() -> str:
    """生成6位数字验证码"""
    return ''.join(random.choices(string.digits, k=6))

def create_verification_code(db: Session, phone: str) -> str:
    """创建并存储验证码"""
    code = generate_verification_code()
    expires_at = datetime.now() + timedelta(minutes=5)
    
    # 删除该手机号的旧验证码
    db.query(VerificationCode).filter(VerificationCode.phone == phone).delete()
    
    verification = VerificationCode(
        phone=phone,
        code=code,
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()
    
    # TODO: 这里应该调用阿里云短信服务发送验证码
    print(f"[模拟发送短信] 手机号: {phone}, 验证码: {code}")
    
    return code

def verify_code(db: Session, phone: str, code: str) -> bool:
    """验证验证码"""
    # 开发环境：如果验证码是 "888888"，直接通过（用于测试）
    if code == "888888":
        return True
    
    verification = db.query(VerificationCode).filter(
        VerificationCode.phone == phone,
        VerificationCode.code == code,
        VerificationCode.used == 0,
        VerificationCode.expires_at > datetime.now()
    ).first()
    
    if verification:
        verification.used = 1
        db.commit()
        return True
    return False

# ===== 用户服务 =====
def get_user_by_phone(db: Session, phone: str):
    """通过手机号获取用户"""
    return db.query(User).filter(User.phone == phone).first()

def create_user(db: Session, user_data: UserCreate) -> User:
    """创建用户"""
    # 验证验证码
    if not verify_code(db, user_data.phone, user_data.verification_code):
        raise ValueError("验证码无效或已过期")
    
    # 检查用户是否已存在
    existing_user = get_user_by_phone(db, user_data.phone)
    if existing_user:
        raise ValueError("该手机号已注册")
    
    # 处理邀请码
    tenant_id = None
    role = RoleEnum.BOSS  # 默认老板
    if user_data.invite_code:
        tenant = db.query(Tenant).filter(Tenant.invite_code == user_data.invite_code).first()
        if not tenant:
            raise ValueError("邀请码无效")
        tenant_id = tenant.id
        role = RoleEnum.EMPLOYEE  # 通过邀请码加入的是员工
    
    user = User(
        phone=user_data.phone,
        nickname=user_data.nickname,
        role=role,
        tenant_id=tenant_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ===== 租户服务 =====
def generate_invite_code() -> str:
    """生成唯一邀请码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_tenant(db: Session, tenant_data: TenantCreate, user_id: int) -> Tenant:
    """创建租户（团队）"""
    # 检查用户是否已有租户
    user = db.query(User).filter(User.id == user_id).first()
    if user.tenant_id:
        raise ValueError("您已加入一个团队")
    
    # 生成唯一邀请码
    invite_code = generate_invite_code()
    while db.query(Tenant).filter(Tenant.invite_code == invite_code).first():
        invite_code = generate_invite_code()
    
    tenant = Tenant(
        name=tenant_data.name,
        invite_code=invite_code,
        balance_minutes=0
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    # 将用户关联到租户
    user.tenant_id = tenant.id
    user.role = RoleEnum.BOSS
    db.commit()
    
    return tenant

def get_tenant_by_id(db: Session, tenant_id: int):
    """获取租户信息"""
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

# ===== 场景服务 =====
def create_scene(db: Session, scene_data: SceneCreate, tenant_id: int) -> Scene:
    """创建场景"""
    scene = Scene(
        tenant_id=tenant_id,
        name=scene_data.name,
        description=scene_data.description,
        prompt_template=scene_data.prompt_template,
        variables=scene_data.variables
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene

def get_scenes_by_tenant(db: Session, tenant_id: int):
    """获取租户的所有场景"""
    return db.query(Scene).filter(Scene.tenant_id == tenant_id).all()

def update_scene(db: Session, scene_id: int, scene_data: SceneCreate, tenant_id: int):
    """更新场景"""
    scene = db.query(Scene).filter(Scene.id == scene_id, Scene.tenant_id == tenant_id).first()
    if not scene:
        raise ValueError("场景不存在或无权限")
    
    scene.name = scene_data.name
    scene.description = scene_data.description
    scene.prompt_template = scene_data.prompt_template
    scene.variables = scene_data.variables
    db.commit()
    db.refresh(scene)
    return scene

def delete_scene(db: Session, scene_id: int, tenant_id: int):
    """删除场景"""
    scene = db.query(Scene).filter(Scene.id == scene_id, Scene.tenant_id == tenant_id).first()
    if not scene:
        raise ValueError("场景不存在或无权限")
    db.delete(scene)
    db.commit()

# ===== 使用记录服务 =====
def create_usage_record(db: Session, usage_data: UsageRecordCreate, user_id: int, tenant_id: int):
    """创建使用记录并扣减分钟数"""
    tenant = get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise ValueError("租户不存在")
    
    if tenant.balance_minutes < usage_data.minutes_used:
        raise ValueError("余额不足")
    
    # 扣减分钟数
    tenant.balance_minutes -= usage_data.minutes_used
    
    # 创建使用记录
    record = UsageRecord(
        tenant_id=tenant_id,
        user_id=user_id,
        minutes_used=usage_data.minutes_used,
        description=usage_data.description
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_usage_records(db: Session, tenant_id: int, limit: int = 50):
    """获取使用记录"""
    return db.query(UsageRecord).filter(
        UsageRecord.tenant_id == tenant_id
    ).order_by(UsageRecord.created_at.desc()).limit(limit).all()

# ===== 充值服务 =====
def create_recharge_record(db: Session, recharge_data: RechargeRecordCreate, tenant_id: int):
    """创建充值记录"""
    record = RechargeRecord(
        tenant_id=tenant_id,
        minutes=recharge_data.minutes,
        amount=recharge_data.amount,
        status="pending"
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_recharge_records(db: Session, tenant_id: int):
    """获取充值记录"""
    return db.query(RechargeRecord).filter(
        RechargeRecord.tenant_id == tenant_id
    ).order_by(RechargeRecord.created_at.desc()).all()

def confirm_recharge(db: Session, record_id: int, admin_note: str = None):
    """确认充值（仅管理员）"""
    record = db.query(RechargeRecord).filter(RechargeRecord.id == record_id).first()
    if not record:
        raise ValueError("充值记录不存在")
    
    if record.status == "completed":
        raise ValueError("该充值记录已处理")
    
    # 更新租户余额
    tenant = get_tenant_by_id(db, record.tenant_id)
    tenant.balance_minutes += record.minutes
    
    # 更新充值记录
    record.status = "completed"
    record.confirmed_at = datetime.now()
    record.admin_note = admin_note
    
    db.commit()
    return record

