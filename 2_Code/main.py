# -*- coding: utf-8 -*-
"""
主程序：Ising模型相变与磁滞回线模拟
"""
import numpy as np
import matplotlib.pyplot as plt
from ising_model import IsingModel
from monte_carlo import MetropolisMonteCarlo, WolffMonteCarlo
from hysteresis import simulate_hysteresis_loop, analyze_hysteresis
from visualization import (plot_spin_configuration, plot_phase_transition, 
                        plot_hysteresis_loop, plot_size_comparison)


def task1_phase_transition():
    """任务1：相变曲线模拟"""
    print("="*60)
    print("任务1：二维Ising模型相变模拟")
    print("="*60)
    
    size = 32
    T_list = np.linspace(1.5, 3.5, 21)
    thermal_steps = 200
    measure_steps = 100
    
    m_avg_list = []
    c_list = []
    chi_list = []
    
    for T in T_list:
        print(f"温度 T = {T:.2f}")
        model = IsingModel(size)
        mc = MetropolisMonteCarlo(model, T)
        energy_list, magnetization_list = mc.run_simulation(thermal_steps, measure_steps)
        
        m_avg = np.mean(np.abs(magnetization_list))
        c = model.calculate_specific_heat(energy_list, T)
        chi = model.calculate_susceptibility(magnetization_list, T)
        
        m_avg_list.append(m_avg)
        c_list.append(c)
        chi_list.append(chi)
    
    # 绘制相变曲线
    fig = plot_phase_transition(T_list, m_avg_list, c_list, chi_list)
    fig.savefig('phase_transition.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return T_list, m_avg_list, c_list, chi_list


def task2_hysteresis():
    """任务2：磁滞回线模拟"""
    print("\n" + "="*60)
    print("任务2：磁滞回线模拟")
    print("="*60)
    
    size = 32
    T = 1.5  # T < Tc
    print(f"温度 T = {T}")
    
    h_list, m_list = simulate_hysteresis_loop(size, T, h_min=-2.0, h_max=2.0, 
                                                num_h=40, thermal_steps=150, measure_steps=80)
    
    m_rem, h_c = analyze_hysteresis(h_list, m_list, num_h=40)
    print(f"\n剩余磁化 m_rem = {m_rem:.3f}")
    print(f"矫顽场 h_c = {h_c:.3f}")
    
    # 绘制磁滞回线
    fig = plot_hysteresis_loop(h_list, m_list, num_h=40, T=T, m_rem=m_rem, h_c=h_c)
    fig.savefig('hysteresis_loop.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return h_list, m_list


def task3_spin_visualization():
    """任务3：不同温度下的自旋构型"""
    print("\n" + "="*60)
    print("任务3：自旋构型可视化")
    print("="*60)
    
    size = 64
    T_values = [1.0, 2.2, 3.0]
    thermal_steps = 300
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, T in enumerate(T_values):
        model = IsingModel(size)
        mc = MetropolisMonteCarlo(model, T)
        mc.thermalize(thermal_steps)
        
        ax = plot_spin_configuration(model.spins, ax=axes[i], title=f'自旋构型 (T={T})')
    
    plt.savefig('spin_configurations.png', dpi=300, bbox_inches='tight')
    plt.show()


def task4_size_effect():
    """任务4：有限尺寸效应"""
    print("\n" + "="*60)
    print("任务4：有限尺寸效应分析")
    print("="*60)
    
    sizes = [16, 32, 64]
    T_list = np.linspace(1.5, 3.5, 15)
    thermal_steps = 200
    measure_steps = 100
    
    results = {size: [] for size in sizes}
    
    for size in sizes:
        print(f"尺寸 N = {size}x{size}")
        m_values = []
        for T in T_list:
            model = IsingModel(size)
            mc = MetropolisMonteCarlo(model, T)
            energy_list, magnetization_list = mc.run_simulation(thermal_steps, measure_steps)
            m_values.append(np.mean(np.abs(magnetization_list)))
        results[size] = m_values
    
    # 绘制尺寸对比
    fig = plot_size_comparison(T_list, results, quantity='m')
    fig.savefig('size_effect.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """主程序主函数"""
    print("Ising模型相变与磁滞回线模拟")
    print("="*60)
    
    # 运行任务
    task1_phase_transition()
    task2_hysteresis()
    task3_spin_visualization()
    task4_size_effect()
    
    print("\n" + "="*60)
    print("所有任务完成！")
    print("生成的图像已保存为PNG文件。")
    print("="*60)


if __name__ == "__main__":
    main()
