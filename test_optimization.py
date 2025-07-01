import unittest
import json
import os
from changeover_optimization import optimize_changeovers, group_by_printing_method

class TestOptimization(unittest.TestCase):
    def setUp(self):
        # 测试用订单数据
        self.test_orders = [
            {"order_id": "1", "product_name": "测试产品1", "printing_method": "小全开双彩", "delivery_date": "6.10"},
            {"order_id": "2", "product_name": "测试产品2", "printing_method": "小全开双彩", "delivery_date": "6.15"},
            {"order_id": "3", "product_name": "测试产品3", "printing_method": "对开双彩", "delivery_date": "6.12"},
            {"order_id": "4", "product_name": "测试产品4", "printing_method": "对开双彩", "delivery_date": "6.20"},
            {"order_id": "5", "product_name": "测试产品5", "printing_method": "小全开双单", "delivery_date": "6.18"}
        ]
        
    def test_group_by_printing_method(self):
        """测试按印刷方式分组"""
        groups = group_by_printing_method(self.test_orders)
        
        # 验证分组结果
        self.assertEqual(len(groups), 3)  # 应该有3种印刷方式
        self.assertEqual(len(groups["小全开双彩"]), 2)  # 小全开双彩有2个订单
        self.assertEqual(len(groups["对开双彩"]), 2)  # 对开双彩有2个订单
        self.assertEqual(len(groups["小全开双单"]), 1)  # 小全开双单有1个订单
        
    def test_optimize_changeovers(self):
        """测试换版优化"""
        result = optimize_changeovers(self.test_orders)
        
        # 验证结果
        self.assertEqual(result["changeover_before"], 5)  # 优化前5个订单需要5次换版
        self.assertEqual(result["changeover_after"], 3)  # 优化后只需要3次换版（按印刷方式分组）
        self.assertEqual(result["changeover_reduction_pct"], 0.4)  # 减少40%
        
        # 验证优化后订单的顺序
        optimized_orders = result["optimized_orders"]
        self.assertEqual(len(optimized_orders), 5)  # 总数应该不变
        
        # 验证相同印刷方式的订单在一起
        methods = [order["printing_method"] for order in optimized_orders]
        method_groups = []
        current_method = None
        
        for method in methods:
            if method != current_method:
                current_method = method
                method_groups.append(method)
                
        self.assertEqual(len(method_groups), 3)  # 应该只有3个换版点
        
    def test_integration_with_real_data(self):
        """测试与实际数据文件集成"""
        # 跳过测试，如果没有对应文件
        if not os.path.exists('parsed_orders.json'):
            self.skipTest("parsed_orders.json not found")
            
        try:
            # 加载真实数据
            with open('parsed_orders.json', 'r', encoding='utf-8') as f:
                real_orders = json.load(f)
                
            # 运行优化
            result = optimize_changeovers(real_orders)
            
            # 基本验证
            self.assertGreater(result["changeover_before"], 0)
            self.assertGreater(result["changeover_after"], 0)
            self.assertLessEqual(result["changeover_after"], result["changeover_before"])
            self.assertGreaterEqual(result["changeover_reduction_pct"], 0)
            self.assertLessEqual(result["changeover_reduction_pct"], 1)
            
        except Exception as e:
            self.fail(f"Integration test failed: {str(e)}")
            
if __name__ == '__main__':
    unittest.main() 