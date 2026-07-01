# -*- coding: utf-8 -*-
"""
Ising模型核心模块
包含二维Ising模型的基本操作
"""
import numpy as np  # 导入NumPy库，用于数组运算


class IsingModel:
    """二维Ising模型类"""
    
    def __init__(self, size, J=1.0, h=0.0):
        """
        初始化Ising模型
        
        参数:
            size: 晶格尺寸 (size × size)
            J: 交换相互作用常数，J>0为铁磁
            h: 外磁场强度
        """
        self.size = size  # 保存晶格边长
        self.J = J  # 保存交换相互作用常数J
        self.h = h  # 保存外磁场强度h
        self.spins = self.initialize_spins()  # 初始化自旋晶格
        
    def initialize_spins(self, random=False):
        """
        初始化自旋晶格
        
        参数:
            random: 是否随机初始化，False则全为+1
        """
        if random:  # 如果选择随机初始化
            # 从[-1, 1]中随机选择，生成size×size的数组
            return np.random.choice([-1, 1], size=(self.size, self.size))
        else:  # 如果选择全向上
            # 生成size×size的全1数组，数据类型为int
            return np.ones((self.size, self.size), dtype=int)
        
    def calculate_energy(self):
        """计算系统的总能量"""
        energy = 0.0  # 初始化能量为0
        # 遍历晶格中的每个自旋
        for i in range(self.size):  # 遍历每一行
            for j in range(self.size):  # 遍历每一列
                # 计算该自旋的4个最近邻（使用周期性边界条件）
                neighbors = self.spins[(i+1)%self.size, j] + \
                           self.spins[(i-1)%self.size, j] + \
                           self.spins[i, (j+1)%self.size] + \
                           self.spins[i, (j-1)%self.size]  # 下、上、右、左四个邻居
                # 哈密顿量 H = -JΣs_i s_j - hΣs_i
                energy -= self.J * self.spins[i, j] * neighbors  # 交换相互作用项
                energy -= self.h * self.spins[i, j]  # 外磁场项
        # 由于每对相互作用被计算了两次，所以除以2
        return energy / 2.0  # 避免双重计数
        
    def calculate_magnetization(self):
        """计算系统的平均磁化强度"""
        return np.mean(self.spins)  # 计算自旋数组的平均值 m = (Σs_i)/N
        
    def calculate_specific_heat(self, energy_list, temperature):
        """
        计算比热
        
        参数:
            energy_list: 能量时间序列
            temperature: 温度 T
        """
        mean_energy = np.mean(energy_list)  # 计算能量的平均值 <E>
        mean_energy_sq = np.mean(np.array(energy_list)**2)  # 计算能量平方的平均值 <E²>
        N = self.size ** 2  # 总自旋数 N = size × size
        # 比热公式：C = (<E²> - <E>²) / (k_B T² N)
        return (mean_energy_sq - mean_energy**2) / (temperature**2 * N)
        
    def calculate_susceptibility(self, magnetization_list, temperature):
        """
        计算磁化率
        
        参数:
            magnetization_list: 磁化强度时间序列
            temperature: 温度 T
        """
        mean_mag = np.mean(magnetization_list)  # 计算磁化强度的平均值 <m>
        mean_mag_sq = np.mean(np.array(magnetization_list)**2)  # 计算磁化强度平方的平均值 <m²>
        N = self.size ** 2  # 总自旋数 N = size × size
        # 磁化率公式：χ = (<m²> - <m>²) / (k_B T N)
        return (mean_mag_sq - mean_mag**2) / (temperature * N)
