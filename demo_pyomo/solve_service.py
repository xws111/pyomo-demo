import pandas as pd
from pyomo.core import ConcreteModel, Set, Param, Var
from pyomo.environ import *

from demo_pyomo.entities import ModelData, Site


def get_model_data():
    """
    返回 Pyomo 優化模型的測試數據集
    示例：運輸問題
    - 3个产地（云南、贵州、四川）供给产品
    - 4个销地（合肥、北京、上海、天津）需求产品
    - 目標：最小化運輸成本 + 懲罰未滿足需求
    """
    # 产地集合
    s_origins = ['云南', '贵州', '四川']
    # 销地集合
    s_destinations = ['合肥', '北京', '上海', '天津']
    # 产地供应量
    p_supply = {'云南': 100, '贵州': 150, '四川': 120}
    # 销地需求量
    p_demand = {'合肥': 80, '北京': 90, '上海': 110, '天津': 70}
    # 单位运输成本 [产地, 销地]
    p_cost = {
        ('云南', '合肥'): 10, ('云南', '北京'): 15, ('云南', '上海'): 12, ('云南', '天津'): 8,
        ('贵州', '合肥'): 8, ('贵州', '北京'): 10, ('贵州', '上海'): 14, ('贵州', '天津'): 11,
        ('四川', '合肥'): 13, ('四川', '北京'): 12, ('四川', '上海'): 9, ('四川', '天津'): 10,
    }

    data = {
        'origins': s_origins,
        'destinations': s_destinations,
        'supply': p_supply,
        'demand': p_demand,
        'cost': p_cost,
    }
    return data


def define_sets(model, data):
    model.s_origins = Set(initialize=[o.code for o in data.origins])
    model.s_destinations = Set(initialize=[d.code for d in data.destinations])


def define_parameters(model, data):
    model.p_supply = Param(model.s_origins, initialize=data.supply)
    model.p_demand = Param(model.s_destinations, initialize=data.demand)
    model.p_cost = Param(model.s_origins, model.s_destinations, initialize=data.cost)


def define_variable(model):
    model.v_volume = Var(model.s_origins, model.s_destinations, domain=NonNegativeReals)
    model.v_slack = Var(model.s_destinations, domain=NonNegativeReals)


def define_constraint(model, data):
    # 1. 產地出發的所有流量，小於等於產地生產量
    def supply_constraint(model, o):
        return sum(model.v_volume[o, d] for d in model.s_destinations) <= data.supply[o]

    model.supply_constraint = Constraint(model.s_origins, rule=supply_constraint)

    # 2. 到目的地的所有流量 + 鬆弛變量 等於目的地的需求量

    def demand_constraint(model, d):
        return sum(model.v_volume[o, d] for o in model.s_origins) + model.v_slack[d] == data.demand[d]

    model.demand_constraint = Constraint(model.s_destinations, rule=demand_constraint)


def define_obj(model):
    model.obj = Objective(
        expr=sum(model.p_cost[o, d] * model.v_volume[o, d]
                 for o in model.s_origins for d in model.s_destinations) + sum(
            model.v_slack[d] for d in model.s_destinations) * 1000
    )


def create_model(data: ModelData) -> ConcreteModel:
    model = ConcreteModel()
    # 1. 定義集合
    define_sets(model, data)
    # 2. 定義參數
    define_parameters(model, data)
    # 3. 定義決策變量
    define_variable(model)
    # 4. 定義約束條件
    define_constraint(model, data)
    # 5. 定義目標函數
    define_obj(model)
    return model


def solve_model(model: ConcreteModel):
    solver = SolverFactory("cplex")
    solver.solve(model, tee=True)


def post_result(model: ConcreteModel):
    print("\n=== 優化結果 ===")
    print(f"\n目標函數值: {model.obj()}")

    print("\n--- 運輸量 ---")
    for o in model.s_origins:
        for d in model.s_destinations:
            vol = model.v_volume[o, d].value
            if vol and vol > 0:
                print(f"  {o} -> {d}: {vol}")

    if hasattr(model, 'v_slack'):
        print("\n--- 未滿足需求 ---")
        for d in model.s_destinations:
            slack = model.v_slack[d].value
            if slack and slack > 0:
                print(f"  {d}: 未滿足 {slack}")


def get_model_data_from_excel(path: str) -> ModelData:
    raw_data = pd.read_excel(path, sheet_name=None)

    origins = [Site(**row) for _, row in raw_data['origins'].iterrows()]
    destinations = [Site(**row) for _, row in raw_data['destinations'].iterrows()]
    supply = raw_data['supply'].set_index('Code')['Value'].to_dict()
    demand = raw_data['demand'].set_index('Code')['Value'].to_dict()
    cost = raw_data['cost'].set_index(['origin', 'destination'])['cost'].to_dict()


    return ModelData(
            origins=origins,
            destinations=destinations,
            supply=supply,
            demand=demand,
            cost=cost,
        )


def solve_opt():
    # # 1. 拿模型數據
    # data = get_model_data()
    # for key, value in data.items():
    #     print(key, value)
    # 1. 从 excel 拿数据
    data = get_model_data_from_excel("data/ModelData.xlsx")

    # 2. 創建模型
    model = create_model(data)
    # 3. 求解模型
    solve_model(model)
    # 4. 輸出結果
    post_result(model)
