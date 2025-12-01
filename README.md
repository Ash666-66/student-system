# 🎓 学生选课系统 (Student Course Selection System)

一个基于 Django 的现代化学生选课管理系统，提供完整的选课流程、用户管理和权限控制功能。

## ✨ 功能特色

### 👥 用户管理
- **多角色支持**: 管理员、教师、学生三种用户类型
- **完整注册流程**: 用户注册 → 档案完善 → 权限分配
- **安全认证**: 基于 Django 的安全用户认证系统
- **个人档案管理**: 完善的学生和教师档案信息

### 📚 课程管理
- **课程信息管理**: 创建、编辑、删除课程信息
- **课程班次管理**: 灵活的课程班次配置
- **容量控制**: 自动管理课程名额和选课人数
- **学期管理**: 支持多学期课程管理

### 📝 选课功能
- **在线选课**: 学生可浏览和选择感兴趣的课程
- **选课审核**: 教师和管理员可审核选课申请
- **状态跟踪**: 实时跟踪选课状态（待审核、已通过、已拒绝）
- **退课功能**: 支持学生退课申请

### 📊 成绩管理
- **成绩录入**: 教师可为学生录入课程成绩
- **成绩查看**: 学生可查看自己的课程成绩
- **成绩统计**: 自动计算平均分和通过率

### 📢 公告系统
- **系统公告**: 管理员可发布系统级公告
- **课程公告**: 教师可发布课程相关公告
- **公告管理**: 支持公告的启用/禁用控制

## 🏗️ 技术架构

### 后端技术栈
- **Framework**: Django 4.2+
- **Database**: SQLite (可扩展至 PostgreSQL/MySQL)
- **Authentication**: Django 内置认证系统
- **ORM**: Django ORM

### 前端技术栈
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Charts**: Chart.js
- **CSS**: 自定义响应式设计

### 开发工具
- **Package Manager**: uv (现代 Python 包管理器)
- **Code Formatter**: Black + Ruff
- **Version Control**: Git
- **Development Server**: Django 开发服务器

## 📋 数据库设计

系统包含 7 个主要数据表：

1. **User** (扩展用户表)
   - 基础用户信息 + 用户类型 + 联系方式

2. **StudentProfile** (学生档案表)
   - 学号、姓名、性别、出生日期、年级、专业、班级

3. **TeacherProfile** (教师档案表)
   - 教师编号、姓名、性别、出生日期、院系、职称

4. **Course** (课程表)
   - 课程代码、课程名称、描述、学分、课时、学期、学年

5. **CourseClass** (课程班次表)
   - 班次代码、授课教师、教室、上课时间、最大人数

6. **Enrollment** (选课记录表)
   - 学生、课程班次、选课状态、选课时间、审核时间、成绩

7. **Announcement** (公告表)
   - 公告标题、内容、发布者、关联课程班次、状态

## 🚀 快速开始

### 环境要求
- Python 3.8+
- uv (推荐) 或 pip
- Git

### 使用 uv (推荐)

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/student-system.git
   cd student-system
   ```

2. **安装依赖**
   ```bash
   uv sync
   ```

3. **激活虚拟环境**
   ```bash
   uv shell
   ```

4. **数据库迁移**
   ```bash
   uv run python manage.py migrate
   ```

5. **创建超级管理员**
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **启动开发服务器**
   ```bash
   uv run python manage.py runserver
   ```

### 使用 pip (传统方式)

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/student-system.git
   cd student-system
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **后续步骤同上**

### 访问应用
- **前端应用**: http://127.0.0.1:8000/
- **管理后台**: http://127.0.0.1:8000/admin/

## 👥 用户角色权限

### 🛡️ 管理员 (Admin)
- 用户管理：查看、编辑所有用户信息
- 课程管理：创建、编辑、删除课程和班次
- 选课管理：审核所有选课申请
- 系统管理：发布公告、查看统计数据
- 权限控制：管理用户权限和访问控制

### 👨‍🏫 教师 (Teacher)
- 课程管理：查看和管理自己负责的课程班次
- 选课审核：审核学生选课申请
- 成绩录入：为学生录入和修改成绩
- 公告发布：发布课程相关公告
- 数据查看：查看选课统计和学生信息

### 👨‍🎓 学生 (Student)
- 课程浏览：查看可选课程和课程详情
- 在线选课：选择感兴趣的课程班次
- 选课管理：查看选课状态，申请退课
- 成绩查看：查看已选课程的成绩
- 档案管理：维护个人信息

## 🔧 开发指南

### 代码规范
项目使用 **Ruff** 和 **Black** 进行代码格式化和检查：

```bash
# 格式化代码
uv run ruff format .

# 代码检查
uv run ruff check .

# 自动修复
uv run ruff check --fix .
```

### 数据库迁移
```bash
# 创建迁移文件
uv run python manage.py makemigrations

# 应用迁移
uv run python manage.py migrate
```

### 测试
```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=.
```

### 静态文件管理
```bash
# 收集静态文件（生产环境）
uv run python manage.py collectstatic
```

## 📁 项目结构

```
student_system/
├── student_system/           # 项目配置目录
│   ├── settings.py         # Django 设置
│   ├── urls.py           # 主 URL 配置
│   ├── wsgi.py          # WSGI 配置
│   └── asgi.py          # ASGI 配置
├── users/                 # 用户管理应用
│   ├── models.py         # 用户模型
│   ├── views.py         # 用户视图
│   ├── forms.py         # 用户表单
│   ├── admin.py         # 管理后台配置
│   └── urls.py         # URL 配置
├── courses/              # 课程管理应用
│   ├── models.py         # 课程模型
│   ├── views.py         # 课程视图
│   ├── forms.py         # 课程表单
│   ├── admin.py         # 管理后台配置
│   └── urls.py         # URL 配置
├── templates/            # 模板文件
│   ├── base.html       # 基础模板
│   ├── users/          # 用户相关模板
│   ├── courses/        # 课程相关模板
│   ├── admin/          # 管理员模板
│   ├── teacher/        # 教师模板
│   └── student/        # 学生模板
├── static/              # 静态文件
│   ├── css/           # CSS 样式
│   ├── js/            # JavaScript 文件
│   └── images/        # 图片文件
├── pyproject.toml        # 项目配置 (uv)
├── requirements.txt      # 生产依赖
├── requirements-dev.txt  # 开发依赖
├── .gitignore          # Git 忽略文件
├── README.md           # 项目说明
└── manage.py           # Django 管理脚本
```

## 🔒 安全特性

- **密码安全**: 使用 Django 内置的密码哈希
- **CSRF 保护**: 启用 CSRF 令牌验证
- **权限控制**: 基于角色的访问控制 (RBAC)
- **输入验证**: 表单数据验证和清理
- **SQL 注入防护**: Django ORM 自动防护
- **XSS 防护**: 模板自动转义用户输入

## 📈 性能优化

- **数据库优化**: 合理的查询优化和索引
- **静态文件优化**: 静态文件压缩和缓存
- **分页功能**: 大数据集的分页显示
- **缓存支持**: 可扩展的缓存机制
- **异步支持**: 为未来的异步处理做准备

## 🚀 部署指南

### 生产环境要求
- Python 3.8+
- PostgreSQL/MySQL 数据库
- Redis (缓存和会话存储)
- Nginx (反向代理)
- Gunicorn/uWSGI (WSGI 服务器)

### 部署步骤
1. 配置环境变量
2. 安装生产依赖
3. 收集静态文件
4. 配置数据库连接
5. 配置 Web 服务器
6. 设置 SSL 证书

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目主页: https://github.com/yourusername/student-system
- 问题反馈: https://github.com/yourusername/student-system/issues
- 邮箱: admin@school.edu

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

⭐ 如果这个项目对你有帮助，请给它一个星标！