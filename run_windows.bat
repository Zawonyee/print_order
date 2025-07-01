@echo off
echo ========================================
echo 印刷流程数字化系统 - 启动脚本
echo ========================================

echo 安装依赖...
pip install flask flask-cors pandas openpyxl pytest pytest-cov

echo 处理订单数据...
python read_excel.py

echo 修复JSON格式...
python fix_json.py

echo 执行换版优化...
python changeover_optimization.py

echo 运行单元测试...
python -m pytest test_optimization.py --cov=changeover_optimization --cov-report=xml

echo 启动后端服务...
cd backend
start python app.py
cd ..

echo ========================================
echo 系统启动完成!
echo 访问地址: http://localhost:5000/dashboard
echo 按任意键关闭此窗口
echo ========================================

pause 