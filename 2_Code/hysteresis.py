# -*- coding: utf-8 -*-
"""
磁滞回线模拟模块
"""
import numpy as np
from ising_model import IsingModel
from monte_carlo import MetropolisMonteCarlo


def simulate_hysteresis_loop(size, temperature, h_min=-2.0, h_max=2.0, num_h=50,
                              thermal_steps=100, measure_steps=50):
    """
    模拟磁滞回线
    
    参数:
        size: 晶格尺寸
        temperature: 温度 T
        h_min: 最小磁场
        h_max: 最大磁场
        num_h: 磁场点数量
        thermal_steps: 每个磁场的热平衡步数
        measure_steps: 每个磁场的测量步数
        
    返回:
        磁场列表, 磁化强度列表
    """
    # 初始化模型（从全向上开始）
    model = IsingModel(size, J=1.0, h=h_max)
    mc = MetropolisMonteCarlo(model, temperature)
    
    # 磁场路径：从h_max降到h_min，再回到h_max
    h_sequence = np.concatenate([np.linspace(h_max, h_min, num_h), 
                                np.linspace(h_min, h_max, num_h)])
    
    m_list = []
    h_list = []
    
    for h in h_sequence:
        # 更新外磁场
        model.h = h
        
        # 弛豫到平衡
        for _ in range(thermal_steps):
            for _ in range(size**2):
                mc.single_spin_flip()
                
        # 测量平均磁化强度
        m_avg = 0.0
        for _ in range(measure_steps):
            for _ in range(size**2):
                mc.single_spin_flip()
            m_avg += model.calculate_magnetization()
        m_avg /= measure_steps
        
        m_list.append(m_avg)
        h_list.append(h)
        print(f"磁场 h = {h:.3f}, 磁化强度 m = {m_avg:.3f}")
        
    return h_list, m_list


def analyze_hysteresis(h_list, m_list, num_h):
    """
    分析磁滞回线，计算剩余磁化和矫顽场
    
    参数:
        h_list: 磁场序列
        m_list: 磁化强度序列
        num_h: 单向磁场点数
        
    返回:
        剩余磁化, 矫顽场
    """
    # 下降段和上升段
    descending_h = h_list[:num_h]
    descending_m = m_list[:num_h]
    ascending_h = h_list[num_h:]
    ascending_m = m_list[num_h:]
    
    # 剩余磁化（h=0时的磁化强度）
    def find_m_at_h(h_target, h_arr, m_arr):
        idx = np.argmin(np.abs(h_arr - h_target))
        return m_arr[idx]
    
    m_rem_desc = find_m_at_h(0.0, descending_h, descending_m)
    m_rem_asc = find_m_at_h(0.0, ascending_h, ascending_m)
    
    # 矫顽场（m=0时的磁场）
    def find_h_at_m(m_target, h_arr, m_arr):
        idx = np.argmin(np.abs(m_arr - m_target))
        return h_arr[idx]
    
    h_c_desc = find_h_at_m(0.0, descending_h, descending_m)
    h_c_asc = find_h_at_m(0.0, ascending_h, ascending_m)
    
    return np.mean([abs(m_rem_desc), abs(m_rem_asc)]), np.mean([abs(h_c_desc), abs(h_c_asc)])
