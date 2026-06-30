# -*- coding: utf-8 -*-
"""
蒙特卡洛算法模块
包含Metropolis算法和Wolff算法
"""
import numpy as np  # 导入NumPy库，用于数值计算
from ising_model import IsingModel  # 从ising_model模块导入IsingModel类


class MetropolisMonteCarlo:
    """Metropolis蒙特卡洛模拟类"""
    
    def __init__(self, model, temperature):
        """
        初始化Metropolis模拟器
        
        参数:
            model: IsingModel实例
            temperature: 温度 T
        """
        self.model = model  # 保存Ising模型实例
        self.beta = 1.0 / temperature  # 计算β = 1/(k_B T)，这里k_B=1
        self.temperature = temperature  # 保存温度值
        
    def single_spin_flip(self):
        """执行一次单自旋翻转"""
        # 随机选择一个自旋的位置i, j
        i = np.random.randint(0, self.model.size)  # 在0~size-1之间随机选择行索引
        j = np.random.randint(0, self.model.size)  # 在0~size-1之间随机选择列索引
        
        # 计算翻转(i,j)处自旋的能量差
        delta_E = self.calculate_energy_diff(i, j)  # 调用能量差计算函数
        
        # Metropolis接受/拒绝判定
        if delta_E <= 0 or np.random.random() < np.exp(-self.beta * delta_E):
            # 如果能量差<=0（翻转后能量降低），直接接受
            # 或者以概率exp(-βΔE)接受（即使能量升高）
            self.model.spins[i, j] *= -1  # 翻转该自旋
            
    def calculate_energy_diff(self, i, j):
        """计算翻转(i,j)处自旋的能量差"""
        s = self.model.spins[i, j]  # 获取(i,j)处的自旋值（+1或-1）
        # 计算4个最近邻自旋的和（使用周期性边界条件）
        neighbors = self.model.spins[(i+1)%self.model.size, j] + \
                   self.model.spins[(i-1)%self.model.size, j] + \
                   self.model.spins[i, (j+1)%self.model.size] + \
                   self.model.spins[i, (j-1)%self.model.size]  # 下、上、右、左四个邻居
        # 能量差公式：ΔE = 2JsΣ邻居 + 2hs
        delta_E = 2 * self.model.J * s * neighbors + 2 * self.model.h * s
        return delta_E
        
    def thermalize(self, steps):
        """热平衡化：让系统弛豫到平衡态"""
        for _ in range(steps):  # 循环thermal_steps次
            for _ in range(self.model.size**2):  # 每个时间步扫描整个晶格
                self.single_spin_flip()  # 执行一次自旋翻转
                
    def run_simulation(self, thermal_steps, measure_steps):
        """
        运行完整模拟
        
        参数:
            thermal_steps: 热平衡步数
            measure_steps: 测量步数
            
        返回:
            能量列表、磁化强度列表
        """
        # 热平衡阶段：先让系统达到平衡
        self.thermalize(thermal_steps)
        
        # 初始化存储测量结果的列表
        energy_list = []  # 存储每个测量步的能量
        magnetization_list = []  # 存储每个测量步的磁化强度
        
        # 测量阶段
        for _ in range(measure_steps):  # 循环measure_steps次
            # 每次测量前先弛豫
            for _ in range(self.model.size**2):  # 扫描整个晶格
                self.single_spin_flip()  # 执行自旋翻转
            # 测量当前能量和磁化强度并保存
            energy_list.append(self.model.calculate_energy())  # 计算并记录能量
            magnetization_list.append(self.model.calculate_magnetization())  # 计算并记录磁化
            
        return energy_list, magnetization_list  # 返回测量结果
    
    def update_temperature(self, temperature):
        """更新温度参数"""
        self.temperature = temperature  # 更新温度值
        self.beta = 1.0 / temperature  # 重新计算β = 1/T


class WolffMonteCarlo:
    """Wolff集群更新算法（进阶）"""
    
    def __init__(self, model, temperature):
        self.model = model  # 保存Ising模型实例
        self.beta = 1.0 / temperature  # 计算β = 1/T
        self.temperature = temperature  # 保存温度值
        # 计算添加邻居到集群的概率 p_add = 1 - exp(-2βJ)
        self.p_add = 1 - np.exp(-2 * self.beta * model.J)
        
    def cluster_update(self):
        """执行一次Wolff集群更新"""
        # 随机选择集群生长的起始点
        i, j = np.random.randint(0, self.model.size), np.random.randint(0, self.model.size)
        seed_spin = self.model.spins[i, j]  # 获取起始点的自旋值
        cluster = {(i, j)}  # 初始化集群集合，包含起始点
        stack = [(i, j)]  # 使用栈（LIFO）来实现深度优先搜索
        
        # 生长集群（使用深度优先搜索）
        while stack:  # 当栈不为空时继续
            x, y = stack.pop()  # 从栈中取出一个位置
            # 遍历四个最近邻方向：下、上、右、左
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                # 计算邻居位置，使用周期性边界
                nx, ny = (x+dx)%self.model.size, (y+dy)%self.model.size
                # 检查邻居是否还没加入集群，并且和起始自旋方向相同
                if (nx, ny) not in cluster and self.model.spins[nx, ny] == seed_spin:
                    # 以概率p_add添加到集群
                    if np.random.random() < self.p_add:
                        cluster.add((nx, ny))  # 将邻居加入集群
                        stack.append((nx, ny))  # 将邻居压入栈中继续生长
        
        # 翻转集群中的所有自旋
        for (x, y) in cluster:  # 遍历集群中的每个位置
            self.model.spins[x, y] *= -1  # 翻转自旋
            
    def thermalize(self, steps):
        """热平衡化"""
        for _ in range(steps):  # 循环steps次
            self.cluster_update()  # 每次执行一次集群更新
            
    def run_simulation(self, thermal_steps, measure_steps):
        """运行模拟"""
        self.thermalize(thermal_steps)  # 热平衡
        energy_list = []  # 初始化能量列表
        magnetization_list = []  # 初始化磁化列表
        
        for _ in range(measure_steps):  # 测量阶段
            self.cluster_update()  # 执行集群更新
            energy_list.append(self.model.calculate_energy())  # 记录能量
            magnetization_list.append(self.model.calculate_magnetization())  # 记录磁化
            
        return energy_list, magnetization_list  # 返回结果
