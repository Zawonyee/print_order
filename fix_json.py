#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import os
import pandas as pd
import traceback

def fix_chinese_quotes(text):
    """将中文引号转换为标准英文引号"""
    # 替换中文双引号为英文双引号
    text = text.replace('"', '"')  # 左双引号
    text = text.replace('"', '"')  # 右双引号
    # 替换中文单引号为英文单引号
    text = text.replace(''', "'")  # 左单引号
    text = text.replace(''', "'")  # 右单引号
    return text

def recreate_orders_from_excel():
    """直接从Excel文件重新创建订单数据"""
    try:
        print("尝试从Excel直接重新创建订单数据...")
        excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '内文印刷明细总表.xlsx')
        
        if not os.path.exists(excel_path):
            print(f"Excel文件不存在: {excel_path}")
            return None
            
        # 读取Excel文件
        df = pd.read_excel(excel_path)
        print(f"成功读取Excel文件，共 {len(df)} 行")
        
        # 处理Excel数据
        orders = []
        for i, row in df.iterrows():
            if i > 0:  # 跳过标题行
                try:
                    order_id = str(i)
                    
                    # 安全获取单元格值
                    def safe_get_cell(row, idx, default=""):
                        if idx < len(row) and pd.notna(row.iloc[idx]):
                            val = str(row.iloc[idx]).strip()
                            # 替换中文引号为英文引号
                            val = val.replace('"', '"').replace('"', '"')
                            val = val.replace(''', "'").replace(''', "'")
                            return val
                        return default
                    
                    product_name = safe_get_cell(row, 1)
                    printing_method = safe_get_cell(row, 5)
                    delivery_date = safe_get_cell(row, 15)
                    
                    if product_name:
                        order = {
                            "order_id": order_id,
                            "product_name": product_name,
                            "printing_method": printing_method,
                            "delivery_date": delivery_date
                        }
                        orders.append(order)
                except Exception as e:
                    print(f"处理第 {i+1} 行时出错: {e}")
                    continue
                    
        print(f"从Excel提取了 {len(orders)} 条订单数据")
        return orders
    except Exception as e:
        print(f"从Excel重建订单数据时出错: {e}")
        traceback.print_exc()
        return None

def fix_json_file(file_path):
    """修复JSON文件中的中文引号和编码问题"""
    try:
        # 读取原始JSON内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"正在修复文件: {file_path}")
        
        # 检查是否有乱码的迹象
        has_non_ascii = False
        try:
            for char in content:
                if ord(char) > 127:
                    has_non_ascii = True
                    break
        except:
            has_non_ascii = True
            
        if has_non_ascii:
            print("检测到可能的编码问题，尝试重新从Excel创建订单数据...")
            orders = recreate_orders_from_excel()
            if orders:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                print(f"已用重建的数据替换 {file_path}")
                return True
        
        # 尝试解析JSON
        try:
            data = json.loads(content)
            print("JSON文件格式正确，检查内容中的编码问题...")
            
            # 检查是否有中文乱码
            has_encoding_issues = False
            new_data = []
            
            for item in data:
                if isinstance(item, dict):
                    new_item = {}
                    for key, value in item.items():
                        if isinstance(value, str):
                            # 检查是否有可能的乱码
                            try:
                                if re.search(r'[\u4e00-\u9fff]', value) and len(value) > 0:
                                    has_encoding_issues = True
                            except:
                                has_encoding_issues = True
                    new_data.append(item)
            
            if has_encoding_issues:
                print("检测到中文编码问题，尝试重新从Excel创建订单数据...")
                orders = recreate_orders_from_excel()
                if orders:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(orders, f, ensure_ascii=False, indent=2)
                    print(f"已用重建的数据替换 {file_path}")
                    return True
            else:
                print("未检测到明显的编码问题")
                return True
                
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print("JSON格式错误，尝试从Excel重建数据...")
            
            orders = recreate_orders_from_excel()
            if orders:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                print(f"已用重建的数据替换 {file_path}")
                return True
            else:
                print("无法从Excel重建数据，尝试其他修复方法...")
        
        # 如果上面的方法都失败了，尝试更激进的修复
        print("尝试修复JSON格式问题...")
        
        # 修复所有可能的中文引号问题
        fixed_content = fix_chinese_quotes(content)
        if fixed_content != content:
            print("已修复中文引号问题")
            content = fixed_content

        # 修复常见的JSON格式问题
        content = re.sub(r',\s*}', '}', content)  # 移除对象末尾多余的逗号
        content = re.sub(r',\s*]', ']', content)  # 移除数组末尾多余的逗号
        
        # 保存修复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"已保存修复后的文件: {file_path}")
            
        # 验证修复后的JSON
        try:
            json.loads(content)
            print("验证通过：修复后的JSON格式正确")
            return True
        except json.JSONDecodeError as e:
            print(f"修复后JSON仍然存在问题，最后尝试从Excel重建...")
            orders = recreate_orders_from_excel()
            if orders:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                print(f"已用重建的数据替换 {file_path}")
                return True
            else:
                print("所有修复方法都失败，请手动检查数据")
                return False
            
    except Exception as e:
        print(f"处理文件时出错: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 修复parsed_orders.json文件
    print("=" * 50)
    print("修复JSON文件中的编码和格式问题")
    print("=" * 50)
    
    file_path = 'parsed_orders.json'
    success = fix_json_file(file_path)
    
    if success:
        print("\n修复成功！请重新启动系统查看效果。")
    else:
        print("\n修复失败，请手动检查JSON文件。") 