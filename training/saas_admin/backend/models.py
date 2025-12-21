from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    """角色枚举"""
    BOSS = "boss"  # 老板
    EMPLOYEE = "employee"  # 员工

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(11), unique=True, index=True, nullable=False, comment="手机号")
    password = Column(String(255), nullable=True, comment="密码（可选）")
    nickname = Column(String(50), nullable=True, comment="昵称")
    role = Column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE, comment="角色")
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True, comment="所属租户ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    tenant = relationship("Tenant", back_populates="users")
    usage_records = relationship("UsageRecord", back_populates="user")

class Tenant(Base):
    """租户表（企业/团队）"""
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="团队名称")
    invite_code = Column(String(20), unique=True, index=True, nullable=False, comment="邀请码")
    balance_minutes = Column(Float, default=0, comment="剩余分钟数")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    users = relationship("User", back_populates="tenant")
    scenes = relationship("Scene", back_populates="tenant")
    usage_records = relationship("UsageRecord", back_populates="tenant")
    recharge_records = relationship("RechargeRecord", back_populates="tenant")

class Scene(Base):
    """场景表（业务渠道场景）"""
    __tablename__ = "scenes"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, comment="所属租户")
    name = Column(String(100), nullable=False, comment="场景名称")
    description = Column(Text, nullable=True, comment="场景描述")
    prompt_template = Column(Text, nullable=False, comment="Prompt模板")
    variables = Column(Text, nullable=True, comment="变量定义(JSON格式)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    tenant = relationship("Tenant", back_populates="scenes")

class UsageRecord(Base):
    """使用记录表"""
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, comment="租户ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    minutes_used = Column(Float, nullable=False, comment="使用分钟数")
    description = Column(String(255), nullable=True, comment="使用说明")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    tenant = relationship("Tenant", back_populates="usage_records")
    user = relationship("User", back_populates="usage_records")

class RechargeRecord(Base):
    """充值记录表"""
    __tablename__ = "recharge_records"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, comment="租户ID")
    minutes = Column(Float, nullable=False, comment="充值分钟数")
    amount = Column(Float, nullable=False, comment="充值金额")
    status = Column(String(20), default="pending", comment="状态: pending/completed")
    payment_screenshot = Column(String(255), nullable=True, comment="支付截图路径")
    admin_note = Column(Text, nullable=True, comment="管理员备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    confirmed_at = Column(DateTime, nullable=True, comment="确认时间")
    
    # 关系
    tenant = relationship("Tenant", back_populates="recharge_records")

class VerificationCode(Base):
    """验证码表"""
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(11), nullable=False, index=True, comment="手机号")
    code = Column(String(6), nullable=False, comment="验证码")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    expires_at = Column(DateTime, nullable=False, comment="过期时间")
    used = Column(Integer, default=0, comment="是否已使用: 0未使用, 1已使用")

