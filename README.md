# 印刷流程数字化系统

基于Python和Flask的印刷订单管理和排产优化系统，提供移动端友好的实时看板。

## 功能

- **订单解析**：Excel订单数据转换为结构化JSON
- **换版优化**：自动合并相同印刷方式的订单，减少换版次数
- **实时看板**：移动端响应式界面，显示订单状态和预警信息

## 系统要求

- Python 3.6+
- 依赖包：flask, flask-cors, pandas, openpyxl

## 快速启动

```bash
# 赋予执行权限（Linux/Mac）
chmod +x run.sh

# 启动系统
./run.sh
```

## 访问地址

- **看板界面**: http://localhost:5000/dashboard
- **API接口**: http://localhost:5000/api
- **健康检查**: http://localhost:5000/health

## 项目结构

- `backend/app.py` - 后端API服务
- `frontend/` - 前端看板界面
- `parsed_orders.json` - 结构化订单数据
- `metrics.json` - 系统性能指标
- `changeover_optimization.py` - 换版优化算法 