#./BaiduSyncdisk/Python_Project/venv/Scripts/python.exe
# -*- coding: utf-8 -*-
'''
@File    :   erp_fee_check.py
@Time    :   2025/07/09 10:41:48
@Author  :   Junkun Yu
@Version :   1.0
@Desc    :   None
'''

import pandas
from math import ceil
import streamlit as st

# 打开特定路径工作簿，工作表
# def worksheet():
#     workbook = pandas.read_excel('./20250709_104148.xlsx')
#     worksheet = workbook['B2C明细']
#     # 读取工作表中“重量”列数据
#     weight_list = worksheet['重量'].tolist()
#     return weight_list
        
# 构建快递费用字典，根据快递公司、地区、公斤段、首重、续重计算
def calc_fee(weight, express_company, area):
    """
    计算从临沂到指定地区的物流费用
    
    参数:
    weight (float): 货物重量(kg)
    express_company (str): 快递公司名称
    area (str): 目的地名称
    
    返回:
    float: 运费金额(元)
    """
    
    # 中通的价格计算逻辑
    if express_company == '中通':
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
        
        # 新疆和西藏的特殊计算方式
        if area == '新疆' or area == '西藏':
            return ceil(weight) * 22
        
        # 查找目的地所在区域
        price_table = None
        if area in base_areas:
            price_table = base_areas[area]
            first_weight = 3.8
            additional_weight = 1.2
        elif area in northeast_areas:
            price_table = northeast_areas[area]
            first_weight = 3.8
            additional_weight = 1.35
        elif area in central_west_areas:
            price_table = central_west_areas[area]
            first_weight = 3.8
            additional_weight = 2.25 if area == '广西' else 2.55
        elif area in remote_areas:
            price_table = remote_areas[area]
            if area == '甘肃':
                first_weight = 3.8
                additional_weight = 3.05
            elif area == '海南':
                first_weight = 3.8  # 海南首重未明确，假设为3.8
                additional_weight = 2.65
            else:
                first_weight = 3.8
                additional_weight = 2.95 if area in ['内蒙', '宁夏'] else 3.25
        elif area in special_areas:
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
        else:
            # 未找到的地区返回None
            return None
        
        # 根据重量计算运费
        if weight <= 0.5:
            return price_table[0]
        elif weight <= 1:
            return price_table[1]
        elif weight <= 2:
            return price_table[2]
        elif weight <= 3:
            return price_table[3]
        else:
            weight = ceil(weight)
            # 超过3kg的计算方式: 首重 + (重量-1)*续重，其中重量需要向上取整
            return first_weight + (weight - 1) * additional_weight
    
    # 圆通、韵达的价格计算逻辑
    elif express_company in ['圆通', '韵达']:
        # 整理各地区价格表（按目的地分类，每一项对应各重量区间的费用）
        # 格式：{地区: [0.01-0.5KG, 0.51-1KG, 1-2KG, 2-3KG, 3.01-5KG, 5.01-8KG, 
        #           首重(8.01-30KG), 续重(8.01-30KG), 首重(30.01+KG), 续重(30.01+KG)]}
        price_data = {
            # 第一类地区（安徽、河北、河南等）
            '安徽': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '河北': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '河南': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '湖北': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '湖南': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '江苏': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '山西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '天津': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '浙江': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '山东': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 0.7, 3.6, 1],  # 山东续重特殊
            
            # 第二类地区（福建、广东、江西、陕西等）
            '福建': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '广东': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 2.2],  # 30kg+续重2.2
            '江西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '陕西': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1.2, 3.6, 2.2],
            '上海': [3, 3.2, 4.15, 4.55, 6, 9.5, 3.6, 1.2, 3.6, 2.2],  # 上海首重价格高
            
            # 第三类地区（东北三省：黑龙江、吉林、辽宁）
            '黑龙': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            '吉林': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            '辽宁': [1.9, 2.3, 3.25, 4, 6, 9.1, 3.6, 1.5, 3.6, 3.2],
            
            # 第四类地区（广西、贵州、四川、重庆等）
            '广西': [2, 2.3, 3.25, 4, 9.7, 14.5, 3.6, 1.9, 3.6, 4.2],
            '贵州': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '四川': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '重庆': [2, 2.3, 3.25, 4, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            
            # 第五类地区（内蒙、宁夏、青海等）
            '内蒙': [2, 2.3, 3.45, 4, 9.7, 14, 3.6, 1.5, 3.6, 3.2],
            '宁夏': [2, 2.3, 3.45, 4, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
            '青海': [2, 2.3, 3.45, 4, 11, 17, 3.6, 1.9, 3.6, 4.2],
            '甘肃': [5.3, 5.3, 6.45, 7.45, 11, 16.5, 3.6, 1.9, 3.6, 4.2],
            
            # 第六类地区（云南、深圳、北京、海南）
            '云南': [2.15, 2.45, 3.4, 4.1, 9.7, 14, 3.6, 1.9, 3.6, 5.2],
            '深圳': [2.2, 2.4, 3.45, 3.95, None, None, None, None, None, None],  # 仅到3.95kg
            '北京': [2.9, 3.1, 4.05, 4.45, 6, 9.5, 3.6, 1, 3.6, 1.2],
            '海南': [5.3, 5.3, 6.45, 7.45, 11, 17, 3.6, 4.7, 3.6, 5.2],
            
            # 特殊地区（新疆、西藏）
            '新疆': [None, None, None, None, None, None, 9.6, 9.6, 9.6, 11],  # 另注：20+(X-1)*20
            '西藏': [None, None, None, None, 64, 99, 12.6, 12.6, 12.6, 13.5]
        }
        
        # 检查地区是否在价格表中
        if area not in price_data:
            return None  # 未知地区
        prices = price_data[area]
        
        # 特殊处理：深圳仅支持到3.95kg，且3.01-5kg有单独公式
        if area == '深圳':
            if weight <= 0.5:
                return prices[0]
            elif 0.5 < weight <= 1:
                return prices[1]
            elif 1 < weight <= 2:
                return prices[2]
            elif 2 < weight <= 3:
                return prices[3]
            elif 3 < weight <= 5:
                # 公式：4.6 + (X-1)*1.05（X为重量）
                return 4.6 + (weight - 1) * 1.05
            else:
                return None  # 深圳5kg以上未明确
        
        # 特殊处理：新疆的基础公式（20+(X-1)*20）
        if area == '新疆' and weight <= 8:
            return 20 + (weight - 1) * 20
        
        # 按重量区间计算费用
        if weight <= 0.5:
            return prices[0] if prices[0] is not None else None
        elif 0.5 < weight <= 1:
            return prices[1] if prices[1] is not None else None
        elif 1 < weight <= 2:
            return prices[2] if prices[2] is not None else None
        elif 2 < weight <= 3:
            return prices[3] if prices[3] is not None else None
        elif 3 < weight <= 5:
            return prices[4] if prices[4] is not None else None
        elif 5 < weight <= 8:
            return prices[5] if prices[5] is not None else None
        elif 8 < weight <= 30:
            # 8.01-30kg：首重（表格中"首重 0 kg"列） + 续重 * (重量-8.01的部分)
            # 注：表格中"首重 0 kg"可能为笔误，理解为基础费+续重
            first = prices[6]
            add = prices[7]
            return first + weight * add if first is not None and add is not None else None
        elif weight > 30:
            # 30.01kg以上：首重 + 续重 * (重量-30.01的部分)
            first = prices[8]
            add = prices[9]
            return first + weight * add if first is not None and add is not None else None
        
        # 未覆盖的重量区间
        return None
    if express_company == '顺丰':
        # 按目的地分组，每组对应：[首重1KG(元), 1-3KG续重(元/KG), ＞3KG续重(元/KG)]
        area_groups = {
            # 第一组：首重8元，1-3KG续重4元，＞3KG续重5元
            'group1': ['山东', '天津', '江苏', '河北', '北京'],
            # 第二组：首重9元，1-3KG续重5元，＞3KG续重6元
            'group2': ['河南', '浙江', '安徽', '上海', '湖北', '辽宁', '福建', 
                       '江西', '山西', '广东', '湖南', '深圳'],
            # 第三组：首重11元，1-3KG续重7元，＞3KG续重8元
            'group3': ['陕西', '吉林', '四川', '重庆', '内蒙', '广西', '宁夏', '贵州'],
            # 第四组：首重14元，1-3KG续重10元，＞3KG续重12元
            'group4': ['黑龙江', '甘肃', '青海', '云南', '海南'],
            # 第五组：首重20元，1-3KG续重12元，＞3KG续重14元
            'group5': ['新疆', '西藏']
        }
        
        # 各组价格表（与上面group1-group5对应）
        price_groups = {
            'group1': (8, 4, 5),
            'group2': (9, 5, 6),
            'group3': (11, 7, 8),
            'group4': (14, 10, 12),
            'group5': (20, 12, 14)
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
    
    # ---------------------- 圆通/韵达计算逻辑（沿用之前） ----------------------
    elif express_company in ['圆通', '韵达']:
        # 价格数据表（与之前一致，省略重复代码，直接调用核心计算逻辑）
        price_data = {
            # 第一类地区（示例，完整数据见之前的定义）
            '安徽': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 1, 3.6, 1.2],
            '山东': [1.9, 2.3, 3.1, 3.7, 6, 9.1, 3.6, 0.7, 3.6, 1],
            # ...（其他地区数据省略，保持不变）
            '新疆': [None, None, None, None, None, None, 9.6, 9.6, 9.6, 11],
            '西藏': [None, None, None, None, 64, 99, 12.6, 12.6, 12.6, 13.5]
        }
        
        # 检查地区是否存在
        if area not in price_data:
            return None
        prices = price_data[area]
        
        # 按重量区间计算（逻辑同之前，仅简化展示）
        if weight <= 0.5:
            return prices[0] if prices[0] is not None else None
        elif 0.5 < weight <= 1:
            return prices[1] if prices[1] is not None else None
        elif 1 < weight <= 2:
            return prices[2] if prices[2] is not None else None
        elif 2 < weight <= 3:
            return prices[3] if prices[3] is not None else None
        elif 3 < weight <= 5:
            return prices[4] if prices[4] is not None else None
        elif 5 < weight <= 8:
            return prices[5] if prices[5] is not None else None
        elif 8 < weight <= 30:
            return prices[6] + (weight - 8) * prices[7] if all(prices[6:8]) else None
        elif weight > 30:
            return prices[8] + (weight - 30) * prices[9] if all(prices[8:10]) else None
        else:
            return None
    
    # 其他快递公司的逻辑可以在这里继续添加
    else:
        return None  # 不支持的快递公司返回None    

# 创建边栏
with st.sidebar:
    selected_tab = st.radio("选择功能", ["运费计算", "开发中"])
    
if selected_tab == "运费计算":
    st.title("运费计算")
    # 用户输入目的地与重量段
    area = st.text_input("请输入目的地省份（例外：直辖市，深圳）")
    weight = st.number_input("请输入重量（kg）", min_value=0， max_value=50, step=2，value=None)
    # express_company = st.selectbox("请选择快递公司", ("顺丰", "中通", "圆通", "韵达"))
    # 计算按钮
    if st.button("计算运费"):
        # 调用运费计算函数
        sf_fee = calc_fee(weight, '顺丰', area)
        zt_fee = calc_fee(weight, '中通', area)
        yt_fee = calc_fee(weight, '圆通', area)
        yd_fee = calc_fee(weight, '韵达', area)
        if sf_fee or zt_fee or yt_fee or yd_fee is not None:
            st.success(f"从临沂到{area}的重量为{weight}kg的费用为: ")
            st.dataframe({
                '快递公司': ['顺丰', '中通', '圆通', '韵达'],
                '费用（元/kg）': [sf_fee, zt_fee, yt_fee, yd_fee]
            })
        else:
            st.error("未找到该地区或快递公司的价格表")
    else:
        st.error("请输入正确的重量")
    
    st.divider()
    
# if __name__ == '__main__':
#     option_select = str(input("请选择功能：\n1. 计算费用\n2. 退出\n"))
#     if option_select == '1':
#         while True:
#             # 示例重量和目的地
#             #express_company = input("请输入快递公司（如：顺丰、圆通、韵达、申通、中通）：")
#             weight = float(input("请输入重量（kg）："))  # 单位：kg
#             area = input("请输入目的地（如：北京、上海、广州、深圳等）：")
        
#             # 调用函数计算费用
            
#             sf_fee = calc_fee(weight, '顺丰', area)
#             zt_fee = calc_fee(weight, '中通', area)
#             yt_fee = calc_fee(weight, '圆通', area)
#             yd_fee = calc_fee(weight, '韵达', area)
            
#             if sf_fee or zt_fee or yt_fee or yd_fee is not None:
#                 print(f"从临沂到{area}的重量为{weight}kg的费用为: \n顺丰：{sf_fee}元 \n中通：{zt_fee}元 \n圆通：{yt_fee}元 \n韵达：{yd_fee}元")
#             else:
#                 print("未找到该地区或快递公司的价格表")
    
    
    
    
    
    
