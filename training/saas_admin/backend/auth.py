from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from database import get_db
from models import User
import schemas

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-please-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建JWT访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> schemas.TokenData:
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")  # 现在是字符串
        phone: str = payload.get("phone")
        
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭证"
            )
        
        # 将字符串转回整数
        user_id = int(user_id_str)
        return schemas.TokenData(user_id=user_id, phone=phone)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    print(f"[DEBUG] get_current_user 被调用")
    print(f"[DEBUG] credentials: {credentials}")
    
    token = credentials.credentials
    print(f"[DEBUG] 提取的token: {token[:50]}...")
    
    token_data = verify_token(token)
    print(f"[DEBUG] Token验证成功, user_id: {token_data.user_id}")
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    print(f"[DEBUG] 数据库查询结果: {user}")
    
    if user is None:
        print(f"[DEBUG] 用户不存在")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    print(f"[DEBUG] 返回用户: ID={user.id}, phone={user.phone}")
    return user

 

def get_current_boss(current_user: User = Depends(get_current_user)) -> User:
    """获取当前老板用户（权限检查）"""
    if current_user.role != "boss":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有老板可以执行此操作"
        )
    return current_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """密码哈希"""
    return pwd_context.hash(password)

