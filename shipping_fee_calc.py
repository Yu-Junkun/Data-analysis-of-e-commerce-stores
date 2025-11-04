#./BaiduSyncdisk/Python_Project/venv/Scripts/python.exe
# -*- coding: utf-8 -*-
'''
@File    :   shipping_fee_calc.py.py
@Time    :   2025/07/09 10:41:48
@Author  :   Junkun Yu
@Version :   1.0
@Desc    :   None
'''

import pandas as pd
import numpy as np
from math import ceil
import streamlit as st
import openpyxl
        
# 构建快递费用字典，根据快递公司、地区、公斤段、首重、续重计算
def calc_fee(row):
    """
    计算从临沂到指定地区的物流费用
    
    参数:
    weight (float): 货物重量(kg)
    express_company (str): 快递公司名称
    area (str): 目的地名称
    
    返回:
    float: 运费金额(元)
    df['收入计费重量'], df['物流'], df['地区'])
    """
    weight = row['收入计费重量']
    express_company = row['物流']
    area = row['地区']

    # 圆通、韵达的价格计算逻辑
    if express_company in ['圆通', '韵达']:
        # 整理各地区价格表（按目的地分类，每一项对应各重量区间的费用）
        # 格式：{地区: [0.01-0.5KG, 0.51-1KG, 1-2KG, 2-3KG, 3.01-5KG, 5.01-8KG, 
        #           首重(8.01-30KG), 续重(8.01-30KG), 首重(30.01+KG), 续重(30.01+KG)]}
        price_data = {
            # 第一类地区（安徽、河北、河南等）
            '安徽': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '河北': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '河南': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '湖北': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '湖南': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '江苏': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '山西': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '天津': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '浙江': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '山东': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 0.7, 3.6, 1],  # 山东续重特殊
            
            # 第二类地区（福建、广东、江西、陕西等）
            '福建': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '广东': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1, 3.6, 2.2],  # 30kg+续重2.2
            '江西': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '陕西': [2.05, 2.45, 3.3, 4.05, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '上海': [3.15, 3.35, 4.35, 4.9, 6, 9.5, 3.6, 1.2, 3.6, 2.2],  # 上海首重价格高
            
            # 第三类地区（东北三省：黑龙江、吉林、辽宁）
            '黑龙江': [2.05, 2.45, 3.45, 4.35, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            '黑龙': [2.05, 2.45, 3.45, 4.35, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            '吉林': [2.05, 2.45, 3.45, 4.35, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            '辽宁': [2.05, 2.45, 3.45, 4.35, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            
            # 第四类地区（广西、贵州、四川、重庆等）
            '广西': [2.15, 2.45, 3.45, 4.35, 9.7, 14.5, 3.6, 1.9, 3.6, 4.2],
            '贵州': [2.15, 2.45, 3.45, 4.35, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '四川': [2.15, 2.45, 3.45, 4.35, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '重庆': [2.15, 2.45, 3.45, 4.35, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            
            # 第五类地区（内蒙、宁夏、青海等）
            '内蒙': [2.15, 2.45, 3.65, 4.35, 9.7, 14, 3.6, 1.5, 3.6, 3.2],
            '内蒙古': [2.15, 2.45, 3.65, 4.35, 9.7, 14, 3.6, 1.5, 3.6, 3.2],
            '宁夏': [2.15, 2.45, 3.65, 4.35, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
            '青海': [2.15, 2.45, 3.65, 4.35, 11, 17, 3.6, 1.9, 3.6, 4.2],
            '甘肃': [5.45, 5.45, 6.65, 7.8, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
            
            # 第六类地区（云南、深圳、北京、海南）
            '云南': [2.3, 2.6, 3.6, 4.45, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '深圳': [2.35, 2.55, 3.65, 4.3, 6, 9.1, 3.6, 1, 3.6, 2.2],  # 后6数参考广东
            '北京': [3.05, 3.25, 4.25, 4.8, 6, 9.5, 3.6, 1, 3.6, 1.2],
            '海南': [5.45, 5.45, 6.65, 7.8, 11, 17, 3.6, 4.7, 3.6, 5.2],
            
            # 特殊地区（新疆、西藏）- 保持不变
            '新疆': [20, 20, 40, 60, 50, 76, 9.6, 9.6, 9.6, 11],  # 另注：20+(X-1)*20
            '西藏': [20, 20, 40, 60, 64, 99, 12.6, 12.6, 12.6, 13.5]
        }
        # ori_price_data = {
        #     # 第一类地区（安徽、河北、河南等）
        #     '安徽': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '河北': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '河南': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '湖北': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '湖南': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '江苏': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '山西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '天津': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '浙江': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
        #     '山东': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 0.7, 3.6, 1],  # 山东续重特殊
            
        #     # 第二类地区（福建、广东、江西、陕西等）
        #     '福建': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
        #     '广东': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 2.2],  # 30kg+续重2.2
        #     '江西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
        #     '陕西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
        #     '上海': [3, 3.2, 4.15, 4.55, 6, 9.5, 3.6, 1.2, 3.6, 2.2],  # 上海首重价格高
            
        #     # 第三类地区（东北三省：黑龙江、吉林、辽宁）
        #     '黑龙江': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
        #     '黑龙': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
        #     '吉林': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
        #     '辽宁': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            
        #     # 第四类地区（广西、贵州、四川、重庆等）
        #     '广西': [2, 2.3, 3.25, 4, 9.7, 14.5, 3.6, 1.9, 3.6, 4.2],
        #     '贵州': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
        #     '四川': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
        #     '重庆': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            
        #     # 第五类地区（内蒙、宁夏、青海等）
        #     '内蒙': [2, 2.3, 3.45, 4, 9.7, 14, 3.6, 1.5, 3.6, 3.2],
        #     '内蒙古': [2, 2.3, 3.45, 4, 9.7, 14, 3.6, 1.5, 3.6, 3.2],
        #     '宁夏': [2, 2.3, 3.45, 4, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
        #     '青海': [2, 2.3, 3.45, 4, 11, 17, 3.6, 1.9, 3.6, 4.2],
        #     '甘肃': [5.3, 5.3, 6.45, 7.45, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
            
        #     # 第六类地区（云南、深圳、北京、海南）
        #     '云南': [2.15, 2.45, 3.4, 4.1, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
        #     '深圳': [2.2, 2.4, 3.45, 3.95, 6, 9.1, 3.6, 1, 3.6, 2.2],  # 后6数参考广东
        #     '北京': [2.9, 3.1, 4.05, 4.45, 6, 9.5, 3.6, 1, 3.6, 1.2],
        #     '海南': [5.3, 5.3, 6.45, 7.45, 11, 17, 3.6, 4.7, 3.6, 5.2],
            
        #     # 特殊地区（新疆、西藏）
        #     '新疆': [20, 20, 40, 60, 50, 76, 9.6, 9.6, 9.6, 11],  # 另注：20+(X-1)*20
        #     '西藏': [20, 20, 40, 60, 64, 99, 12.6, 12.6, 12.6, 13.5]
        # }
        
        # 检查地区是否在价格表中
        if area not in price_data:
            return None  # 未知地区
        prices = price_data[area]
        
        # 按重量区间计算费用
        if weight <= 0.5:
            return prices[0] if prices[0] is not None else None
        elif weight <= 1:
            return prices[1] if prices[1] is not None else None
        elif weight <= 2:
            return prices[2] if prices[2] is not None else None
        elif weight <= 3:
            return prices[3] if prices[3] is not None else None
        elif weight <= 5:
            return prices[4] if prices[4] is not None else None
        elif weight <= 8:
            return prices[5] if prices[5] is not None else None
        elif weight <= 30:
            # 8.01-30kg：首重（表格中"首重 0 kg"列） + 续重 * (重量-8.01的部分)
            # 注：表格中"首重 0 kg"可能为笔误，理解为基础费+续重
            first = prices[6]
            add = prices[7]
            weight = ceil(weight)
            return first + weight * add if first is not None and add is not None else None
        elif weight > 30:
            # 30.01kg以上：首重 + 续重 * (重量-30.01的部分)
            first = prices[8]
            add = prices[9]
            weight = ceil(weight)
            return first + weight * add if first is not None and add is not None else None
        
        # 未覆盖的重量区间
        return None
     
    # 中通的价格计算逻辑
    elif express_company == '中通':
        # 根据目的地划分不同价格区间
        # 基础区域价格表(0.01-3KG固定价格)
        base_areas = {
            '安徽': [2.05, 2.45, 3.25, 3.85],
            '福建': [2.05, 2.45, 3.25, 3.85],
            '广东': [2.05, 2.45, 3.25, 3.85],
            '河北': [2.05, 2.45, 3.25, 3.85],
            '河南': [2.05, 2.45, 3.25, 3.85],
            '湖北': [2.05, 2.45, 3.25, 3.85],
            '湖南': [2.05, 2.45, 3.25, 3.85],
            '江苏': [2.05, 2.45, 3.25, 3.85],
            '江西': [2.05, 2.45, 3.25, 3.85],
            '山东': [2.05, 2.45, 3.25, 3.85],
            '山西': [2.05, 2.45, 3.25, 3.85],
            '陕西': [2.05, 2.45, 3.25, 3.85],
            '天津': [2.05, 2.45, 3.25, 3.85],
            '浙江': [2.05, 2.45, 3.25, 3.85]
        }
        
        # 东北区域价格表
        northeast_areas = {
            '黑龙江': [2.05, 2.45, 3.4, 4.15],
            '黑龙': [2.05, 2.45, 3.4, 4.15],
            '吉林': [2.05, 2.45, 3.4, 4.15],
            '辽宁': [2.05, 2.45, 3.4, 4.15]
        }
        
        # 中西部区域价格表
        central_west_areas = {
            '广西': [2.15, 2.45, 3.4, 4.15],
            '贵州': [2.15, 2.45, 3.4, 4.15],
            '四川': [2.15, 2.45, 3.4, 4.15],
            '重庆': [2.15, 2.45, 3.4, 4.15]
        }
        
        # 偏远区域价格表
        remote_areas = {
            '内蒙': [2.15, 2.45, 3.6, 4.15],
            '内蒙古': [2.15, 2.45, 3.6, 4.15],
            '宁夏': [2.15, 2.45, 3.6, 4.15],
            '青海': [2.15, 2.45, 3.6, 4.15],
            '甘肃': [5.45, 5.45, 6.6, 7.6],
            '海南': [5.45, 5.45, 6.6, 7.6]
        }
        
        # 特殊区域价格表
        special_areas = {
            '深圳': [2.35, 2.55, 3.6, 4.1],
            '北京': [3.05, 3.25, 4.2, 4.6],
            '上海': [3.15, 3.35, 4.3, 4.7],
            '云南': [2.3, 2.6, 3.55, 4.25]
        }
        
        # 查找目的地所在区域
        price_table = None
        if area in special_areas:
            price_table = special_areas[area]
            if area == '深圳':
                first_weight = 4.8
                additional_weight = 1.25
            elif area == '北京':
                first_weight = 4.8
                additional_weight = 1.45
            elif area == '上海':
                first_weight = 4.8
                additional_weight = 1.35
            else:  # 云南
                first_weight = 3.8
                additional_weight = 2.55
        elif area in base_areas:
            price_table = base_areas[area]
            first_weight = 3.8
            if area == '广东':
                additional_weight = 1.25
            elif area == '福建':
                additional_weight = 1.35
            else:
                additional_weight = 1.2
        elif area in northeast_areas:
            price_table = northeast_areas[area]
            first_weight = 3.8
            additional_weight = 1.35
        elif area in central_west_areas:
            price_table = central_west_areas[area]
            first_weight = 3.9 if area == '广西' else 3.8
            additional_weight = 2.25 if area == '广西' else 2.55
        elif area in remote_areas:
            price_table = remote_areas[area]
            if area == '甘肃':
                first_weight = 3.8
                additional_weight = 3.05
            elif area == '海南':
                first_weight = 2.65  # 海南首重未明确，假设为2.65
                additional_weight = 2.65
            else:
                first_weight = 3.8
                additional_weight = 3.25 if area == '青海' else 2.95
                # 新疆和西藏的特殊计算方式
        elif area == '新疆' or area == '西藏':
            return ceil(weight) * 22
        else:
            # 未找到的地区返回None
            return None
        
        # 根据重量计算运费
        if weight <= 0.5:
            return price_table[0]+0.2
        elif weight <= 1:
            return price_table[1]+0.2
        elif weight <= 2:
            return price_table[2]+0.2
        elif weight <= 3:
            return price_table[3]+0.4
        # elif weight <= 6:
        elif weight > 3:
            weight = ceil(weight)
            # 超过3kg的计算方式: 首重 + (重量-1)*续重，其中重量需要向上取整
            return first_weight + (weight - 1) * additional_weight
        else:
            return None
            
    elif express_company == '顺丰':
        weight = ceil(weight)
        # 按目的地分组，每组对应：[首重1KG(元), 1-3KG续重(元/KG), ＞3KG续重(元/KG)]
        area_groups = {
            # 第一组：首重8元，1-3KG续重4元，＞3KG续重5元
            'group1': ['山东', '天津', '江苏', '河北', '北京'],
            # 第二组：首重9元，1-3KG续重5元，＞3KG续重6元
            'group2': ['河南', '浙江', '安徽', '上海', '湖北', '辽宁', '福建', 
                       '江西', '山西', '广东', '湖南', '深圳'],
            # 第三组：首重11元，1-3KG续重7元，＞3KG续重8元
            'group3': ['陕西', '吉林', '四川', '重庆', '内蒙', '内蒙古', '广西', '宁夏', '贵州'],
            # 第四组：首重14元，1-3KG续重10元，＞3KG续重12元
            'group4': ['黑龙江', '黑龙', '甘肃', '青海', '云南', '海南'],
            # 第五组：首重20元，1-3KG续重12元，＞3KG续重14元
            'group5': ['新疆', '西藏']
        }
        
        # 各组价格表（与上面group1-group5对应）
        price_groups = {
            'group1': [8, 4, 5],
            'group2': [9, 5, 6],
            'group3': [11, 7, 8],
            'group4': [14, 10, 12],
            'group5': [20, 12, 14]
        }
        
        # 匹配目的地所属分组
        target_group = None
        for group, areas in area_groups.items():
            if area in areas:
                target_group = group
                break
        if not target_group:
            return None  # 未找到对应地区
        
        # 提取该组价格
        first_1kg,续重_1_3kg,续重_3kg_plus = price_groups[target_group]
        
        # 按重量计算运费
        if weight <= 1:
            # 首重1KG内（含1KG）
            return first_1kg
        elif 1 < weight <= 3:
            # 1-3KG：首重 + 超过1KG部分的续重（按1-3KG续重标准）
            return first_1kg + (weight - 1) * 续重_1_3kg
        else:
            # ＞3KG：首重 + 1-3KG部分续重 + 超过3KG部分的续重
            # 解析：1-3KG共2KG，按续重_1_3kg计算；超过3KG的部分按续重_3kg_plus计算
            #return first_1kg + 2 * 续重_1_3kg + (weight - 3) * 续重_3kg_plus
            return first_1kg + (weight - 1) * 续重_3kg_plus
    # 德邦快递的价格计算逻辑
    elif express_company == '德邦':
        # 转换后的字典（键：地区名称，值：[首重4公斤, 续重]）
        shipping_rates = {
            '北京': [7.3, 1.2],
            '天津': [6.1, 1.2],
            '河北': [6.1, 1.2],
            '山西': [6.7, 1.2],
            '内蒙古': [7.3, 1.7],
            '内蒙': [7.3, 1.7],#手动添加
            '辽宁': [7.3, 1.3],
            '吉林': [7.3, 1.7],
            '黑龙江': [7.3, 1.7],
            '上海': [7.9, 1.3],
            '江苏': [6.1, 1.2],
            '浙江': [6.7, 1.2],
            '安徽': [6.7, 1.2],
            '福建': [7.3, 1.3],
            '江西': [7.3, 1.2],
            '山东': [6.1, 0.9],
            '河南': [6.1, 1.2],
            '湖北': [7.3, 1.2],
            '湖南': [7.9, 1.2],
            '广东': [7.9, 1.7],
            '深圳': [7.9, 1.7],#手动添加
            '广西': [8.5, 1.7],
            '海南': [11.0, 2.0],
            '重庆': [7.3, 1.7],
            '四川': [7.3, 1.7],
            '贵州': [8.5, 1.7],
            '云南': [8.5, 1.7],
            '西藏': [14.6, 2.4],
            '陕西': [7.3, 1.2],
            '甘肃': [8.5, 1.7],
            '青海': [8.5, 1.7],
            '宁夏': [8.5, 1.7],
            '新疆': [14.6, 2.4]
        }
        # 计算费用
        if area in shipping_rates:
            if weight <= 4:
                return shipping_rates[area][0]
            elif weight < 20:
                return shipping_rates[area][0] + (weight - 4) * shipping_rates[area][1]
            return None
        else:
            return None  # 不支持的地区返回None
        
    elif express_company == '（中通/德邦）快运':
        price_data = {
            '北京': [18, 1.8, 1.71, 1.71],
            '天津': [18, 1.51, 1.43, 1.43],
            '安徽': [18, 1.39, 1.32, 1.32],
            '河北': [18, 1.65, 1.57, 1.57],
            '山东': [18, 1.16, 1.1, 1.1],
            '黑龙江': [18, 2.46, 2.34, 2.34],
            '黑龙': [18, 2.46, 2.34, 2.34],
            '吉林': [18, 1.96, 1.86, 1.86],
            '辽宁': [18, 1.93, 1.83, 1.83],
            '山西': [18, 1.57, 1.49, 1.49],
            '江西': [18, 1.78, 1.69, 1.69],
            '湖南': [18, 1.88, 1.79, 1.79],
            '湖北': [18, 1.76, 1.67, 1.67],
            '河南': [18, 1.42, 1.35, 1.35],
            '江苏': [18, 1.29, 1.22, 1.22],
            '上海': [18, 1.34, 1.27, 1.27],
            '浙江': [18, 1.4, 1.33, 1.33],
            '广东': [18, 1.93, 1.83, 1.83],
            '深圳': [18, 1.93, 1.83, 1.83],
            '福建': [18, 1.98, 1.88, 1.88],
            '重庆': [18, 2.25, 2.14, 2.14],
            '四川': [18, 2.12, 2.01, 2.01],
            '陕西': [18, 1.92, 1.82, 1.82],
            '内蒙': [25.0, 2.35, 2.23, 2.23],
            '内蒙古': [25.0, 2.35, 2.23, 2.23],
            '云南': [25.0, 2.6, 2.47, 2.47],
            '广西': [25.0, 2.08, 1.98, 1.98],
            '青海': [25.0, 3.48, 3.31, 3.31],
            '甘肃': [25.0, 3.07, 2.92, 2.92],
            '贵州': [25.0, 2.45, 2.33, 2.33],
            '宁夏': [25.0, 2.06, 1.96, 1.96],
            '海南': [50.0, 3.53, 3.36, 3.36],
            '西藏': [50.0, 6.16, 5.86, 5.86],
            '新疆': [50.0, 4.37, 4.16, 4.16]
        }
        # 检查地区是否在价格表中
        if area not in price_data:
            return None  # 未知地区
        prices = price_data[area]
        weight = ceil(weight)
        # 检查重量是否在该地区的价格范围内
        if weight <= 50:
            return prices[0] + (weight - 1) * prices[1]
        else:
            return prices[2] + (weight - 1) * prices[3]
    else:
        return None  # 不支持的快递公司返回None    
    
def shipping_fee_calc():
    area = st.text_input("请输入目的地省份（云南、广东、四川，例外：直辖市，深圳）")
    weight = st.number_input("请输入重量（kg）", min_value=0.00, max_value=9999.00, step=0.01, value=None)
    # express_company = st.selectbox("请选择快递公司", ("顺丰", "中通", "圆通", "韵达"))
    # 计算按钮
    if st.button("计算运费"):
        # 构造临时行数据（匹配calc_fee函数的参数要求）
        temp_row_sf = pd.Series({
            '收入计费重量': weight,
            '物流': '顺丰',
            '地区': area
        })
        temp_row_yt = pd.Series({
            '收入计费重量': weight,
            '物流': '圆通',
            '地区': area
        })
        temp_row_yd = pd.Series({
            '收入计费重量': weight,
            '物流': '韵达',
            '地区': area
        })
        temp_row_zt = pd.Series({
            '收入计费重量': weight,
            '物流': '中通',
            '地区': area
        })
        temp_row_db = pd.Series({
            '收入计费重量': weight,
            '物流': '德邦',
            '地区': area
        })
        temp_row_wt = pd.Series({
            '收入计费重量': weight,
            '物流': '（中通/德邦）快运',
            '地区': area
        })
        # 调用函数计算费用
        # 调用运费计算函数，未含快递税率6%，快运含税
        sf_fee = calc_fee(temp_row_sf)
        zt_fee = calc_fee(temp_row_zt)
        yt_fee = calc_fee(temp_row_yt)
        yd_fee = calc_fee(temp_row_yd)
        db_fee_taxed = calc_fee(temp_row_db)
        wt_fee_taxed = calc_fee(temp_row_wt)
        
        # 生成不含税费用列表，确保计算和格式化正确
        fees_without_tax = [
        f"{sf_fee:.2f}" if sf_fee is not None else None,
        f"{zt_fee:.2f}" if zt_fee is not None else None,
        f"{yt_fee:.2f}" if yt_fee is not None else None,
        f"{yd_fee:.2f}" if yd_fee is not None else None,
        f"{db_fee_taxed / 1.06:.2f}" if db_fee_taxed is not None else None,
        f"{wt_fee_taxed / 1.09:.2f}" if wt_fee_taxed is not None else None
        ]
        
        # 生成含税费用列表，确保计算和格式化正确
        tax_included_fees = [
        f"{sf_fee * 1.06:.2f}" if sf_fee is not None else None,
        f"{zt_fee * 1.06:.2f}" if zt_fee is not None else None,
        f"{yt_fee * 1.06:.2f}" if yt_fee is not None else None,
        f"{yd_fee * 1.06:.2f}" if yd_fee is not None else None,
        f"{db_fee_taxed :.2f}" if db_fee_taxed is not None else None,
        f"{wt_fee_taxed :.2f}" if wt_fee_taxed is not None else None  # 假设快运费用已经含税
        ]
        
        if sf_fee or zt_fee or yt_fee or yd_fee or db_fee_taxed or wt_fee_taxed is not None:
            st.success(f"从临沂到{area}的重量为{weight:.2f}kg的费用为: ")
            st.dataframe({
                '快递公司': ['顺丰', '中通', '圆通', '韵达', '德邦', '快运（中通/德邦）'],
                '不含税费用（元）': fees_without_tax,
                '含税费用（元）':tax_included_fees
            })
        else:
            st.error("未找到该地区或快递公司的价格表")
            
def shipping_bill_check():
    uploaded_file = st.file_uploader("请上传账单表")
    st.write("数据来源：\n\t华夏龙-杨军")
    st.write("\t文件名称样例：元更时代x月账单_received-date_version.xlsx")
    if uploaded_file is not None and uploaded_file.name.endswith('.xlsx'):
        try:
            try:
                # 直接读取文件内容，不使用临时文件
                df = pd.read_excel(uploaded_file, sheet_name='B2C明细')
            except Exception as e:
                st.error(f"错误: {str(e)}")
            # 只保留需要的列
            required_cols = ['物流单号', '映射物流公司', '省市区', '收入计费重量', '收入-快递费', '收入-操作费', '货品数量']
            df = df[required_cols]
            # workbook = pd.read_excel(uploaded_file, sheet_name='B2C明细', usecols=['物流单号', '映射物流公司', '省市区', '收入计费重量', '收入-快递费', '收入-操作费', '货品数量'])
            # 读取工作表中映射物流公司、省市区、物流单号、收入计费重量、收入-快递费列数据，合并成新dataframe
            df = workbook[:-1].copy()
            df.loc[:, '物流'] = df['映射物流公司'].str[0:2]
            # 批量删除“省市区”列中的所有空格
            df["省市区"] = df["省市区"].str.replace(" ", "", regex=False)            
            # 使用 np.where() 根据条件选择不同的值
            df.loc[:, '地区'] = np.where(
                df['省市区'].str.contains('深圳'),  # 条件：如果包含"深圳"
                '深圳',                  # 满足条件时：取第4-5个字符
                df['省市区'].str[:2]                  # 不满足条件时：取前两个字符
            )
            df.loc[:, '运费计算'] = df.apply(calc_fee, axis=1)
            # 统一对整列结果保留两位小数
            df.loc[:, '运费计算'] = df['运费计算'].round(2)
            # 计算运费差异
            df.loc[:, '运费差异'] = df['运费计算'] - df['收入-快递费']
            df.loc[:, '操作费计算'] = np.where(df['收入计费重量']<= 0.5,
                                        0.4+0.1*df['货品数量'],
                                        0.7+0.1*df['货品数量'])
            # 计算操作费差异
            df.loc[:, '操作费差异'] = df['操作费计算'] - df['收入-操作费']
            # 统一对操作费差异保留两位小数
            df.loc[:, '操作费差异'] = df['操作费差异'].round(2)
            # 筛选差异大于0.1元的行
            df_filtered1 = df[df['运费差异'] != 0]
            df_filtered2 = df[df['操作费差异'] != 0]
            # 打印筛选结果
            st.write(f"运费差异的订单有{len(df_filtered1)}条")
            st.dataframe(df_filtered1)
            st.write(f"操作费差异的订单有{len(df_filtered2)}条")
            st.dataframe(df_filtered2)
        except Exception:
            st.error("1请检查上传文件并重新上传")
    elif uploaded_file is not None:
        st.error("2请检查上传文件并重新上传")  
    else:
        st.error("3请检查上传文件并重新上传")




