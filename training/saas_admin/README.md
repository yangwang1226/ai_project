# SaaS管理系统

一个功能完整的SaaS后台管理系统，包含用户管理、团队协作、场景配置、计费系统等功能。

## 功能特性

根据需求表实现的核心功能：

### ✅ 核心功能（Must Have）

- **用户模块**
  - 手机号注册登录
  - 短信验证码验证
  - JWT身份认证

- **租户模块**
  - 企业/团队概念
  - 唯一邀请码生成
  - 团队成员管理

- **权限模块**
  - 老板角色：完全权限
  - 员工角色：受限权限
  - 基于角色的访问控制

- **业务模块**
  - 自定义渠道场景
  - Prompt模板配置
  - 支持变量替换（一个简单的变量，插入Prompt变量）

- **计费模块**
  - 按分钟数计费
  - 类库分钟数扣减机制
  - 每次调用扣减和记录

- **支付模块**
  - 充值页面
  - 客服微信二维码展示
  - 页面放客服信息二维码 -> 你支付动态

- **合规模块**
  - 用户协议
  - 隐私政策
  - 秒杀入口

- **客服模块**
  - 页面右下角客服入口
  - 客服联系信息展示

## 技术栈

### 后端
- FastAPI - 现代化的Python Web框架
- SQLAlchemy - ORM数据库工具
- JWT - 身份认证
- Pydantic - 数据验证
- SQLite - 数据库（可替换为MySQL/PostgreSQL）

### 前端
- Vue 3 - 渐进式JavaScript框架
- Element Plus - UI组件库
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP客户端
- Vite - 构建工具

## 项目结构

```
saas_admin/
├── backend/                 # 后端代码
│   ├── main.py             # 应用入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic模式
│   ├── auth.py             # 认证相关
│   ├── services.py         # 业务逻辑
│   ├── routes.py           # API路由
│   ├── requirements.txt    # Python依赖
│   └── .env.example        # 环境变量示例
│
└── frontend/               # 前端代码
    ├── src/
    │   ├── views/          # 页面组件
    │   │   ├── Login.vue
    │   │   ├── Register.vue
    │   │   ├── Dashboard.vue
    │   │   ├── Scenes.vue
    │   │   ├── Usage.vue
    │   │   ├── Recharge.vue
    │   │   ├── Team.vue
    │   │   ├── Terms.vue
    │   │   └── Privacy.vue
    │   ├── layouts/        # 布局组件
    │   ├── components/     # 通用组件
    │   ├── stores/         # 状态管理
    │   ├── router/         # 路由配置
    │   ├── utils/          # 工具函数
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    ├── vite.config.js
    └── index.html
```

## 快速开始

### 后端启动

1. 进入后端目录并安装依赖：
```bash
cd saas_admin/backend
pip install -r requirements.txt
```

2. 复制环境变量文件：
```bash
cp .env.example .env
```

3. 修改 `.env` 文件，配置必要的参数（如密钥、数据库等）

4. 启动后端服务：
```bash
python main.py
```

后端API服务将运行在 `http://localhost:8000`

API文档地址：`http://localhost:8000/docs`

### 前端启动

1. 进入前端目录并安装依赖：
```bash
cd saas_admin/frontend
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

前端应用将运行在 `http://localhost:3000`

### 生产部署

1. 构建前端：
```bash
cd saas_admin/frontend
npm run build
```

2. 启动后端（生产模式）：
```bash
cd saas_admin/backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 数据库模型

### 用户表 (users)
- 手机号、昵称
- 角色（老板/员工）
- 所属租户

### 租户表 (tenants)
- 团队名称
- 邀请码
- 余额分钟数

### 场景表 (scenes)
- 场景名称、描述
- Prompt模板
- 变量定义

### 使用记录表 (usage_records)
- 用户ID、租户ID
- 使用分钟数
- 使用时间

### 充值记录表 (recharge_records)
- 充值分钟数、金额
- 状态（待确认/已完成）
- 确认时间

### 验证码表 (verification_codes)
- 手机号
- 验证码
- 过期时间

## API接口

### 认证相关
- `POST /api/v1/auth/send-code` - 发送验证码
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户信息

### 租户相关
- `POST /api/v1/tenants` - 创建团队
- `GET /api/v1/tenants/my` - 获取我的团队

### 场景相关
- `POST /api/v1/scenes` - 创建场景（老板）
- `GET /api/v1/scenes` - 获取场景列表
- `PUT /api/v1/scenes/{id}` - 更新场景（老板）
- `DELETE /api/v1/scenes/{id}` - 删除场景（老板）

### 使用记录相关
- `POST /api/v1/usage` - 创建使用记录
- `GET /api/v1/usage` - 获取使用记录

### 充值相关
- `POST /api/v1/recharge` - 创建充值记录
- `GET /api/v1/recharge` - 获取充值记录

### 统计相关
- `GET /api/v1/dashboard/stats` - 获取仪表盘统计（老板）

## 权限说明

### 老板（Boss）
- 可以访问数据看板
- 可以创建/编辑/删除场景
- 可以查看团队所有数据
- 可以管理团队成员

### 员工（Employee）
- 可以查看场景列表
- 可以查看使用记录
- 可以进行充值
- 权限受限

## 安全特性

- JWT身份认证
- 密码加密存储（bcrypt）
- 短信验证码验证
- 基于角色的访问控制
- CORS跨域保护
- SQL注入防护

## 开发建议

1. **短信服务**：当前使用模拟短信，生产环境需要接入阿里云短信服务
2. **支付功能**：当前使用客服人工确认，可以接入支付宝/微信支付API
3. **数据库**：开发环境使用SQLite，生产环境建议使用MySQL或PostgreSQL
4. **密钥管理**：务必修改 `.env` 中的 `SECRET_KEY`
5. **日志系统**：建议添加完善的日志记录
6. **监控告警**：建议添加系统监控和告警机制

## 后续优化方向

- [ ] 添加数据导出功能
- [ ] 添加数据可视化图表
- [ ] 支持多语言国际化
- [ ] 添加API限流功能
- [ ] 完善单元测试
- [ ] 添加Docker部署支持
- [ ] 性能优化和缓存

## 许可证

MIT License

## 联系方式

如有问题，请通过以下方式联系：
- 邮箱：support@example.com
- 客服微信：见系统内客服二维码

