# -*- coding: utf-8 -*-
'''
@File    :   st_dy_xhs_live_data_upload.py
@Time    :   2025/04/02 10:50:36
@Author  :   Junkun Yu
@Version :   1.0
@Desc    :   None
'''

import streamlit as st
from shipping_fee_calc import calc_fee
from live_data_function import *
from shipping_fee_calc import *

# 创建边栏
# 选择直播平台
st.set_page_config(layout="wide")
with st.sidebar:
    selected_tab = st.radio("选择功能", ["抖音直播", "小红书直播", "直播综合", "快递运费", "华夏龙账单核对"])
    
if selected_tab == "抖音直播":
    st.title("抖音直播数据分析数据导入")
    st.write("本程序用于\n\t1. 将抖音直播数据分析数据导入到 MySQL 数据库中。\n\t2. 计算指标并上传到飞书。")
    st.divider()
    douyin_order_data_import()
    st.divider()
    douyin_live_data_import()
    st.divider()
    douyin_live_promotion_data_import()
    st.divider()
    douyin_calculate_and_upload_to_feishu()
    st.divider()
    
elif selected_tab == "小红书直播":
    st.title("小红书直播数据分析数据导入")
    st.write("本程序用于\n\t1. 将小红书直播数据分析数据导入到 MySQL 数据库中。\n\t2. 计算指标并上传到飞书。")
    st.divider()
    xhs_live_data_import()
    st.divider()
    xhs_order_data_import()
    st.divider()
    xhs_live_order_data_import()
    st.divider()
    xhs_promotion_data_import()
    st.divider()
    xhs_calculate_and_upload_to_feishu()
    st.divider()
    
elif selected_tab == '直播综合':
    st.title("抖音&小红书直播数据分析数据导入")
    st.write("本程序用于\n\t1. 辅助分析抖音&小红书直播订单ROI。")
    st.divider()
    multi_calculate_and_upload_to_feishu()
    st.divider()
    
elif selected_tab == '快递运费':
    st.title("华夏龙云仓快递物流费用计算")
    st.write("本程序用于\n\t1. 各地区常规运费计算。")
    st.divider()
    shipping_fee_calc()
    st.divider()
    
elif selected_tab == '华夏龙账单核对':
    st.title("华夏龙云仓快递物流费用核对")
    st.write("本程序用于\n\t1. 华夏龙账单快递、快运费用核对。")
    st.divider()
    shipping_bill_check()
    st.divider()