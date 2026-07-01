# -*- coding: utf-8 -*-
"""
可视化模块
包含各种绘图函数
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def plot_spin_configuration(spins, ax=None, title="自旋构型"):
    """
    绘制自旋构型
    
    参数:
        spins: 二维自旋数组
        ax: matplotlib轴对象
        title: 标题
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(spins, cmap='seismic', vmin=-1, vmax=1, interpolation='nearest')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


def plot_phase_transition(T_list, m_list, c_list, chi_list, T_c=2.269):
    """
    绘制相变曲线
    
    参数:
        T_list: 温度列表
        m_list: 磁化强度列表
        c_list: 比热列表
        chi_list: 磁化率列表
        T_c: 理论临界点
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # 磁化强度
    axes[0].plot(T_list, np.abs(m_list), 'o-', label='$|m|$', linewidth=2)
    axes[0].axvline(x=T_c, color='r', linestyle='--', label='$T_c$')
    axes[0].set_xlabel('温度 T', fontsize=14)
    axes[0].set_ylabel('磁化强度 $|m|$', fontsize=14)
    axes[0].legend(fontsize=12)
    axes[0].grid(True, alpha=0.3)
    
    # 比热
    axes[1].plot(T_list, c_list, 's-', label='$C$', linewidth=2)
    axes[1].axvline(x=T_c, color='r', linestyle='--', label='$T_c$')
    axes[1].set_xlabel('温度 T', fontsize=14)
    axes[1].set_ylabel('比热 C', fontsize=14)
    axes[1].legend(fontsize=12)
    axes[1].grid(True, alpha=0.3)
    
    # 磁化率
    axes[2].plot(T_list, chi_list, '^-', label=r'$\chi$', linewidth=2)
    axes[2].axvline(x=T_c, color='r', linestyle='--', label=r'$T_c$')
    axes[2].set_xlabel('温度 T', fontsize=14)
    axes[2].set_ylabel('磁化率 $\chi$', fontsize=14)
    axes[2].legend(fontsize=12)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_hysteresis_loop(h_list, m_list, num_h, T, m_rem=None, h_c=None):
    """
    绘制磁滞回线
    
    参数:
        h_list: 磁场列表
        m_list: 磁化强度列表
        num_h: 单向磁场点数
        T: 温度
        m_rem: 剩余磁化
        h_c: 矫顽场
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 绘制下降段和上升段
    ax.plot(h_list[:num_h], m_list[:num_h], 'o-', label='下降段', markersize=4, linewidth=1.5)
    ax.plot(h_list[num_h:], m_list[num_h:], 's-', label='上升段', markersize=4, linewidth=1.5)
    
    # 标注剩余磁化和矫顽场
    if m_rem is not None:
        ax.axhline(y=m_rem, color='g', linestyle=':', alpha=0.7)
        ax.axhline(y=-m_rem, color='g', linestyle=':', alpha=0.7)
    if h_c is not None:
        ax.axvline(x=h_c, color='orange', linestyle=':', alpha=0.7)
        ax.axvline(x=-h_c, color='orange', linestyle=':', alpha=0.7)
    
    ax.set_xlabel('外磁场 h', fontsize=14)
    ax.set_ylabel('磁化强度 m', fontsize=14)
    ax.set_title(f'Ising模型磁滞回线 (T={T})', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig


def plot_size_comparison(T_list, results_dict, quantity='m'):
    """
    绘制不同尺寸的对比曲线
    
    参数:
        T_list: 温度列表
        results_dict: 结果字典 {size: value_list}
        quantity: 物理量 'm', 'c', 或 'chi'
    """
    labels = {'m': '磁化强度', 'c': '比热', 'chi': '磁化率'}
    ylabels = {'m': '$|m|$', 'c': '$C$', 'chi': '$\chi$'}
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    markers = ['o', 's', '^', 'd', 'v']
    for i, (size, values) in enumerate(results_dict.items()):
        ax.plot(T_list, values, marker=markers[i%len(markers)], label=f'$N={size}\\times{size}$', linewidth=2, markersize=6)
    
    ax.axvline(x=2.269, color='r', linestyle='--', label='$T_c$')
    ax.set_xlabel('温度 T', fontsize=14)
    ax.set_ylabel(ylabels[quantity], fontsize=14)
    ax.set_title(f'不同尺寸下的{labels[quantity]}', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
