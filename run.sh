#!/bin/bash

# 显示标题
echo "========================================"
echo "印刷流程数字化系统 - 启动脚本"
echo "========================================"

# 安装依赖
echo "安装依赖..."
pip install flask flask-cors pandas openpyxl pytest pytest-cov

# 运行数据处理
echo "处理订单数据..."
python read_excel.py

# 修复JSON格式问题
echo "修复JSON格式..."
python fix_json.py

# 运行换版优化
echo "执行换版优化..."
python changeover_optimization.py

# 运行单元测试并生成覆盖率报告
echo "运行单元测试..."
python -m pytest test_optimization.py --cov=changeover_optimization --cov-report=xml

# 启动后端服务
echo "启动后端服务..."
cd backend
python app.py &
SERVER_PID=$!
cd ..

# 等待服务启动
echo "等待服务启动..."
sleep 3

echo "========================================"
echo "系统启动完成!"
echo "访问地址: http://localhost:5000/dashboard"
echo "按 Ctrl+C 停止服务"
echo "========================================"

# 等待用户中断
wait $SERVER_PID 