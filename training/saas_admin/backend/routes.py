from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import create_access_token, get_current_user, get_current_boss
from models import User
import schemas
import services

router = APIRouter(prefix="/api/v1", tags=["api"])

# ===== 认证相关 =====
@router.post("/auth/send-code", summary="发送验证码")
def send_verification_code(
    request: schemas.SendVerificationCodeRequest,
    db: Session = Depends(get_db)
):
    """发送短信验证码"""
    try:
        code = services.create_verification_code(db, request.phone)
        return {"message": "验证码发送成功", "code": code}  # 生产环境删除code返回
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/register", response_model=schemas.Token, summary="注册")
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """用户注册"""
    try:
        user = services.create_user(db, user_data)
        access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login", response_model=schemas.Token, summary="登录")
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录"""
    print(f"[DEBUG] 登录请求 - 手机号: {login_data.phone}, 验证码: {login_data.verification_code}")
    
    # 验证验证码
    if not services.verify_code(db, login_data.phone, login_data.verification_code):
        print(f"[DEBUG] 验证码验证失败")
        raise HTTPException(status_code=400, detail="验证码无效或已过期")
    
    print(f"[DEBUG] 验证码验证成功")
    
    # 查找用户
    user = services.get_user_by_phone(db, login_data.phone)
    if not user:
        print(f"[DEBUG] 用户不存在")
        raise HTTPException(status_code=404, detail="用户不存在，请先注册")
    
    print(f"[DEBUG] 用户找到: ID={user.id}, 手机号={user.phone}")
    
    # 修改这里：将 user.id 转为字符串
    access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone})
    print(f"[DEBUG] Token生成成功: {access_token[:50]}...")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=schemas.UserResponse, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user

# ===== 租户相关 =====
@router.post("/tenants", response_model=schemas.TenantResponse, summary="创建团队")
def create_tenant(
    tenant_data: schemas.TenantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建团队（租户）"""
    try:
        tenant = services.create_tenant(db, tenant_data, current_user.id)
        return tenant
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tenants/my", response_model=schemas.TenantResponse, summary="获取我的团队信息")
def get_my_tenant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户所属团队信息"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=404, detail="您还未加入任何团队")
    
    tenant = services.get_tenant_by_id(db, current_user.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="团队不存在")
    
    return tenant

# ===== 场景相关（老板权限） =====
@router.post("/scenes", response_model=schemas.SceneResponse, summary="创建场景")
def create_scene(
    scene_data: schemas.SceneCreate,
    current_user: User = Depends(get_current_boss),
    db: Session = Depends(get_db)
):
    """创建场景（仅老板）"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="请先创建团队")
    
    try:
        scene = services.create_scene(db, scene_data, current_user.tenant_id)
        return scene
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/scenes", response_model=List[schemas.SceneResponse], summary="获取场景列表")
def get_scenes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取团队的所有场景"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="您还未加入任何团队")
    
    scenes = services.get_scenes_by_tenant(db, current_user.tenant_id)
    return scenes

@router.put("/scenes/{scene_id}", response_model=schemas.SceneResponse, summary="更新场景")
def update_scene(
    scene_id: int,
    scene_data: schemas.SceneCreate,
    current_user: User = Depends(get_current_boss),
    db: Session = Depends(get_db)
):
    """更新场景（仅老板）"""
    try:
        scene = services.update_scene(db, scene_id, scene_data, current_user.tenant_id)
        return scene
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/scenes/{scene_id}", summary="删除场景")
def delete_scene(
    scene_id: int,
    current_user: User = Depends(get_current_boss),
    db: Session = Depends(get_db)
):
    """删除场景（仅老板）"""
    try:
        services.delete_scene(db, scene_id, current_user.tenant_id)
        return {"message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== 使用记录相关 =====
@router.post("/usage", response_model=schemas.UsageRecordResponse, summary="创建使用记录")
def create_usage(
    usage_data: schemas.UsageRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建使用记录并扣减分钟数"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="您还未加入任何团队")
    
    try:
        record = services.create_usage_record(db, usage_data, current_user.id, current_user.tenant_id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usage", response_model=List[schemas.UsageRecordResponse], summary="获取使用记录")
def get_usage_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取团队的使用记录"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="您还未加入任何团队")
    
    records = services.get_usage_records(db, current_user.tenant_id)
    return records

# ===== 充值相关 =====
@router.post("/recharge", response_model=schemas.RechargeRecordResponse, summary="创建充值记录")
def create_recharge(
    recharge_data: schemas.RechargeRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建充值记录"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="您还未加入任何团队")
    
    try:
        record = services.create_recharge_record(db, recharge_data, current_user.tenant_id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/recharge", response_model=List[schemas.RechargeRecordResponse], summary="获取充值记录")
def get_recharge_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取团队的充值记录"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="您还未加入任何团队")
    
    records = services.get_recharge_records(db, current_user.tenant_id)
    return records

# ===== 统计相关 =====
@router.get("/dashboard/stats", response_model=schemas.DashboardStats, summary="获取统计数据")
def get_dashboard_stats(
    current_user: User = Depends(get_current_boss),
    db: Session = Depends(get_db)
):
    """获取仪表盘统计数据（仅老板）"""
    from models import User, Tenant, UsageRecord
    from sqlalchemy import func
    from datetime import date
    
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="请先创建团队")
    
    tenant = services.get_tenant_by_id(db, current_user.tenant_id)
    
    # 统计团队用户数
    total_users = db.query(func.count(User.id)).filter(User.tenant_id == current_user.tenant_id).scalar()
    
    # 今日使用量
    today = date.today()
    total_usage_today = db.query(func.sum(UsageRecord.minutes_used)).filter(
        UsageRecord.tenant_id == current_user.tenant_id,
        func.date(UsageRecord.created_at) == today
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_tenants": 1,
        "total_balance": tenant.balance_minutes,
        "total_usage_today": total_usage_today
    }

