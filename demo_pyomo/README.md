# Pyomo 运输问题演示

## 问题简介

运输问题是运筹学中最经典的优化问题之一：

- **3个产地** (云南, 贵州, 四川): 每个产地有固定供给量
- **4个销地** (合肥, 北京, 上海, 天津): 每个销地有固定需求量
- **单位运输成本**: 从每个产地到每个销地的单位运费不同

## 数学模型

```
集合: 
1. 产地集合 s_origins, index = o
2. 销地集合 s_destinations, index = d

参数
1. 单位运输成本 p_cost[o, d]
2. 产地供应量 p_supply[o]
3. 销地需求量 p_demand[d]

决策变量
1. v_volumn[o, d], domain 大于等于 0
2. v_slack[o, d],  >= 0 , 未滿足的需求

约束条件
1. 供给约束：Σ v_volumn[o, d] ≤ p_supply[o]  每个产地发货量不大于产地供给量
2. 需求约束：Σ v_volumn[o, d] + v_slack[o, d] = demand[d]  每个销地收货量，尽可能满足需求，不超过需求。 贵的也要，但是不会多买


目标函数: min Σ p_cost[o, d] * v_volumn[o, d] + Σ v_slack[o, d] * 1000   (最小化总运输成本)

```