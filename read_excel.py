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
    
    # 打印列名
    print("列名:")
    print(df.columns.tolist())
    
    # 清洗数据
    orders_list = []
    for i, row in df.iterrows():
        # 跳过空行或者标题行
        if pd.isna(row.iloc[0]) or isinstance(row.iloc[0], str) and '产品序号' in row.iloc[0]:
            continue
            
        try:
            # 尝试获取订单编号
            order_id = row.iloc[0]
            if pd.isna(order_id):
                continue
                
            # 忽略非数字的订单编号行
            if not (isinstance(order_id, int) or isinstance(order_id, float) or 
                   (isinstance(order_id, str) and re.match(r'^\d+$', order_id))):
                continue
                
            # 获取产品名称
            product_name = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            # 获取印刷方式
            printing_method = row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else ""
            
            # 获取交货日期
            delivery_date = row.iloc[15] if len(row) > 15 and pd.notna(row.iloc[15]) else ""
            
            # 创建订单字典
            order_dict = {
                'order_id': str(int(order_id)) if isinstance(order_id, (int, float)) else str(order_id),
                'product_name': str(product_name),
                'printing_method': str(printing_method),
                'delivery_date': str(delivery_date)
            }
            
            orders_list.append(order_dict)
            print(f"处理订单: {order_dict}")
            
        except Exception as e:
            print(f"处理行 {i} 时出错: {e}")
            continue
    
    # 保存为JSON文件
    with open('parsed_orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders_list, f, ensure_ascii=False, indent=2)
    
    print(f"\nJSON文件已保存为 parsed_orders.json，共处理 {len(orders_list)} 条记录")
    
except Exception as e:
    print(f"读取文件出错: {e}") 