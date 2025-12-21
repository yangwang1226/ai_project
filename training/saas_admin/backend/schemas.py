from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models import RoleEnum

# ===== 用户相关 =====
class UserBase(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    nickname: Optional[str] = None

class UserCreate(UserBase):
    verification_code: str = Field(..., min_length=6, max_length=6, description="验证码")
    invite_code: Optional[str] = Field(None, description="邀请码")

class UserLogin(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)
    verification_code: str = Field(..., min_length=6, max_length=6)

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    tenant_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SendVerificationCodeRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)

# ===== 租户相关 =====
class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int
    invite_code: str
    balance_minutes: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== 场景相关 =====
class SceneBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    prompt_template: str = Field(..., min_length=1)
    variables: Optional[str] = None

class SceneCreate(SceneBase):
    pass

class SceneUpdate(SceneBase):
    pass

class SceneResponse(SceneBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ===== 使用记录相关 =====
class UsageRecordCreate(BaseModel):
    minutes_used: float = Field(..., gt=0)
    description: Optional[str] = None

class UsageRecordResponse(BaseModel):
    id: int
    tenant_id: int
    user_id: int
    minutes_used: float
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== 充值记录相关 =====
class RechargeRecordCreate(BaseModel):
    minutes: float = Field(..., gt=0, description="充值分钟数")
    amount: float = Field(..., gt=0, description="充值金额")

class RechargeRecordResponse(BaseModel):
    id: int
    tenant_id: int
    minutes: float
    amount: float
    status: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class RechargeRecordConfirm(BaseModel):
    record_id: int
    admin_note: Optional[str] = None

# ===== Token相关 =====
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    phone: Optional[str] = None

# ===== 统计相关 =====
class DashboardStats(BaseModel):
    total_users: int
    total_tenants: int
    total_balance: float
    total_usage_today: float

