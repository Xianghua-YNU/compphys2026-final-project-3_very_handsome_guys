# Ising模型期末设计项目结构

## 项目文件说明

### 核心代码模块

| 文件名 | 功能描述 |
|--------|----------|
| `ising_model.py` | Ising模型类，包含自旋操作、能量计算、热力学量计算 |
| `monte_carlo.py` | Metropolis和Wolff蒙特卡洛算法实现 |
| `hysteresis.py` | 磁滞回线模拟与分析 |
| `visualization.py` | 可视化模块，包含所有绘图函数 |
| `main.py` | 主程序，整合所有功能并运行完整模拟 |

### 其他文件

| 文件名 | 功能描述 |
|--------|----------|
| `DEMO.ipynb` | Jupyter Notebook演示文件 |
| `requirements.txt` | Python依赖包列表 |
| `README.md` | 开题报告 |
| `PROJECT_STRUCTURE.md` | 本文件，项目结构说明 |

## 快速开始

### 环境配置

```bash
pip install -r requirements.txt
```

### 运行完整模拟

```bash
python main.py
```

### 使用Notebook演示

```bash
jupyter notebook DEMO.ipynb
```

## 主要功能

### 1. 相变曲线模拟
- 温度扫描：T ∈ [1.5, 3.5]
- 计算磁化强度、比热、磁化率
- 自动识别临界点 Tc ≈ 2.27

### 2. 磁滞回线模拟
- 磁场扫描：h ∈ [-2.0, 2.0]
- 计算剩余磁化和矫顽场
- 观察回线形状与温度的关系

### 3. 有限尺寸效应
- 对比不同晶格尺寸（16×16, 32×32, 64×64）
- 分析有限尺寸标度行为

### 4. 可视化功能
- 自旋构型快照
- 热力学量曲线
- 磁滞回线图
- 多尺寸对比图

## 模块使用示例

### 基本使用

```python
from ising_model import IsingModel
from monte_carlo import MetropolisMonteCarlo

# 初始化模型
model = IsingModel(size=32, J=1.0, h=0.0)
mc = MetropolisMonteCarlo(model, temperature=2.0)

# 运行模拟
energy_list, magnetization_list = mc.run_simulation(
    thermal_steps=200, measure_steps=100
)

# 计算热力学量
m_avg = np.mean(np.abs(magnetization_list))
c = model.calculate_specific_heat(energy_list, 2.0)
chi = model.calculate_susceptibility(magnetization_list, 2.0)
```

### 磁滞回线

```python
from hysteresis import simulate_hysteresis_loop

h_list, m_list = simulate_hysteresis_loop(
    size=32, temperature=1.5,
    h_min=-2.0, h_max=2.0, num_h=40
)
```

## 进阶功能

### Wolff算法（集群更新）

```python
from monte_carlo import WolffMonteCarlo

mc_wolff = WolffMonteCarlo(model, temperature=2.27)
# 临界区域模拟速度更快！
```

### 自定义初始条件

```python
model = IsingModel(size=32)
model.spins = model.initialize_spins(random=True)  # 随机初始化
```

## 物理意义

| 物理量 | 符号 | 公式 |
|--------|------|------|
| 磁化强度 | $m$ | $\langle |\sum s_i/N| \rangle$ |
| 比热 | $C$ | $(\langle E^2 \rangle - \langle E \rangle^2)/(N T^2)$ |
| 磁化率 | $\chi$ | $(\langle m^2 \rangle - \langle m \rangle^2)/(N T)$ |

## 参考文献

1. Plischke, M., & Bergersen, B. (2006). *Equilibrium statistical physics*. World Scientific.
2. Newman, M. E. J., & Barkema, G. T. (1999). *Monte Carlo methods in statistical physics*. Oxford University Press.
3. Onsager, L. (1944). Crystal statistics. I. *Physical Review*, 65, 117.
4. Wolff, U. (1989). Collective Monte Carlo updating. *Physical Review Letters*, 62, 361.
