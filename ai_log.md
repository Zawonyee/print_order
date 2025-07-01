# AI 使用记录

## 记录1：Excel数据解析

**问题**：如何将复杂的Excel印刷订单表格转换为结构化JSON格式？

**为何这样问**：Excel文件结构复杂，直接使用pandas读取会遇到标题行不在第一行、列名不规范等问题，需要AI协助处理这些边缘情况。

**AI回答**：
```python
import pandas as pd
import json
import re

# 读取Excel文件
try:
    # 直接读取Excel文件
    df_raw = pd.read_excel('内文印刷明细总表.xlsx')
    
    # 找到真正的标题行
    for i, row in df_raw.iterrows():
        if '产品序号' in str(row.values):
            header_row = i
            break
    
    # 重新读取Excel，使用找到的标题行
    df = pd.read_excel('内文印刷明细总表.xlsx', header=header_row)
    
    # 清洗数据
    orders_list = []
    for i, row in df.iterrows():
        # 跳过空行或者标题行
        if pd.isna(row.iloc[0]) or isinstance(row.iloc[0], str) and '产品序号' in row.iloc[0]:
            continue
            
        try:
            # 获取必要字段
            order_id = row.iloc[0]
            product_name = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            printing_method = row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else ""
            delivery_date = row.iloc[15] if len(row) > 15 and pd.notna(row.iloc[15]) else ""
            
            # 创建订单字典
            order_dict = {
                'order_id': str(int(order_id)) if isinstance(order_id, (int, float)) else str(order_id),
                'product_name': str(product_name),
                'printing_method': str(printing_method),
                'delivery_date': str(delivery_date)
            }
            
            orders_list.append(order_dict)
            
        except Exception as e:
            print(f"处理行 {i} 时出错: {e}")
            continue
    
    # 保存为JSON文件
    with open('parsed_orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders_list, f, ensure_ascii=False, indent=2)
```

## 记录2：换版优化排产

**问题**：如何实现"相同印刷方式"订单的合并排产逻辑，以减少换版次数？

**为何这样问**：需要一个高效的算法来分析订单数据，按照印刷方式进行分组，并计算优化前后的换版次数与减少比例。

**AI回答**：
```python
from collections import defaultdict

def group_by_printing_method(orders):
    """根据印刷方式分组订单"""
    method_groups = defaultdict(list)
    
    for order in orders:
        printing_method = order.get('printing_method', '').strip()
        if printing_method:
            method_groups[printing_method].append(order)
    
    return method_groups

def optimize_changeovers(orders):
    """优化换版次数"""
    # 按印刷方式分组
    method_groups = group_by_printing_method(orders)
    
    # 计算优化前的换版次数（每个订单一次换版）
    changeover_before = len(orders)
    
    # 优化后的订单列表
    optimized_orders = []
    changeover_after = 0
    
    # 对每种印刷方式内的订单进行排序和合并
    for method, method_orders in method_groups.items():
        # 按交货日期排序
        method_orders.sort(key=lambda x: x.get('delivery_date', ''))
        
        # 添加到优化后的订单列表
        optimized_orders.extend(method_orders)
        
        # 每种印刷方式只需要一次换版
        changeover_after += 1
    
    # 计算减少的百分比
    if changeover_before > 0:
        reduction_pct = (changeover_before - changeover_after) / changeover_before
    else:
        reduction_pct = 0
    
    return {
        'optimized_orders': optimized_orders,
        'changeover_before': changeover_before,
        'changeover_after': changeover_after,
        'changeover_reduction_pct': round(reduction_pct, 2)
    }
```

## 记录3：响应式手机端看板

**问题**：如何创建一个响应式的手机端网页看板，支持实时查看订单状态、排产顺序和预警信息？

**为何这样问**：需要设计一个在移动设备上表现良好的界面，同时能够动态展示和更新订单数据，以及生成相关的预警信息。

**AI回答**：
```html
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="metrics-card">
                <h5><i class="bi bi-graph-up"></i> 换版优化指标</h5>
                <div class="row mt-3">
                    <div class="col">
                        <p class="mb-1">优化前换版次数</p>
                        <h4 id="changeover-before">-</h4>
                    </div>
                    <div class="col">
                        <p class="mb-1">优化后换版次数</p>
                        <h4 id="changeover-after">-</h4>
                    </div>
                    <div class="col">
                        <p class="mb-1">减少比例</p>
                        <h4 id="reduction-pct">-</h4>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <h5 class="mb-3"><i class="bi bi-list-check"></i> 优化后排产顺序</h5>
    <div id="orders-container">
        <!-- 订单卡片将在这里动态添加 -->
    </div>
    
    <script>
        // 显示订单列表
        function displayOrders(orders) {
            // 按印刷方式分组
            const ordersByMethod = {};
            orders.forEach(order => {
                const method = order.printing_method || '未指定';
                if (!ordersByMethod[method]) {
                    ordersByMethod[method] = [];
                }
                ordersByMethod[method].push(order);
            });
            
            // 为每个印刷方式创建一个部分
            Object.keys(ordersByMethod).forEach(method => {
                const methodOrders = ordersByMethod[method];
                
                // 创建印刷方式标题和订单卡片
                // ...
            });
        }
        
        // 生成预警信息
        function generateWarnings() {
            // 查找今日交付的订单
            const today = new Date();
            const todayOrders = allOrders.filter(order => {
                const dueDate = parseDueDate(order.delivery_date);
                return dueDate && dueDate.toDateString() === today.toDateString();
            });
            
            if (todayOrders.length > 0) {
                // 创建预警信息
                // ...
            }
        }
    </script>
</div>
```

## 记录4：后端API服务设计

**问题**：如何设计一个支持数据上传、处理和查询的RESTful API后端？

**为何这样问**：需要一个功能完善的后端服务来支持前端看板的数据需求，包括文件上传、数据处理、优化结果和指标的查询等。

**AI回答**：
```python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import pandas as pd
import sys

# 添加父目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from changeover_optimization import optimize_changeovers, load_orders, load_devices

app = Flask(__name__)
CORS(app)  # 启用跨域请求

@app.route('/')
def index():
    return jsonify({"message": "印刷流程数字化系统API服务"})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = load_orders(ORDERS_FILE)
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimized_orders', methods=['GET'])
def get_optimized_orders():
    try:
        orders = load_orders(ORDERS_FILE)
        optimization_result = optimize_changeovers(orders)
        return jsonify(optimization_result['optimized_orders'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件上传"}), 400
        
    # 文件处理逻辑
    # ...
    
    return jsonify({
        "message": "文件上传并处理成功",
        "orders_count": len(orders),
        "metrics": metrics
    })
``` 