from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routes import router
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SaaS管理系统API",
    description="基于FastAPI的SaaS后台管理系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)


# # 静态文件服务（用于前端）
# if os.path.exists("../frontend/dist"):
#     app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

