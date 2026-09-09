后端第一次

# 查看版本
py --version

# 创建虚拟环境
py -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装项目全部依赖
py -m pip install -r requirements.txt

# FastAPI启动后端
py -m uvicorn main:app --reload

后端第二次

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动后端
py app.py 


访问：http://127.0.0.1:5000



# 启动前端（推荐用于查看界面）

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖（首次运行需要）
npm install

# 3. 启动前端
npm run dev
```

访问：http://localhost:5173/ http://127.0.0.1:5000