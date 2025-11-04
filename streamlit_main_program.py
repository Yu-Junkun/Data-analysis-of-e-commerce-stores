# -*- coding: utf-8 -*-
'''
@File    :   streamlit_main_program.py
@Time    :   2025/04/02 10:50:36
@Author  :   Junkun Yu
@Version :   1.0
@Desc    :   None
'''

import streamlit as st
from shipping_fee_calc import *

# 创建边栏
# 选择直播平台
st.set_page_config(layout="wide")
with st.sidebar:
    selected_tab = st.radio("选择功能", ["快递运费", "华夏龙账单核对"])
     
if selected_tab == '快递运费':
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

