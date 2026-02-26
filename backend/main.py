from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from pyqubo import Array, Constraint
import neal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定（Viteからアクセス可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========
# 入力スキーマ
# ==========
class GroupInput(BaseModel):
    A: int
    B: int
    C: int
    D: int
    E: int
    F: int
    G: int
    H: int
    I: int


@app.post("/optimize")
def optimize_route(data: GroupInput):

    groups = data.dict()

    base_times = {
        "3F": [20, 25, 30],
        "2F": [15, 20, 25],
        "1F": [5, 10, 15]
    }

    alpha = 0.2

    # ==========
    # ルート構築
    # ==========
    route_options = {}

    for g, pop in groups.items():
        if g in "GHI":
            floor = "3F"
        elif g in "DEF":
            floor = "2F"
        else:
            floor = "1F"

        for idx in range(3):
            calc_time = base_times[floor][idx] + pop * alpha

            if floor == "3F":
                edges = [f"Stair_{idx+1}_3-2", f"Stair_{idx+1}_2-1", f"Exit_{idx+1}"]
            elif floor == "2F":
                edges = [f"Stair_{idx+1}_2-1", f"Exit_{idx+1}"]
            else:
                edges = [f"Exit_{idx+1}"]

            route_options[(g, idx)] = {
                "edges": edges,
                "time": calc_time
            }

    # ==========
    # QUBO構築
    # ==========
    x = {}
    for g in groups:
        for idx in range(3):
            x[(g, idx)] = Array.create(f'x_{g}_{idx}', shape=1, vartype='BINARY')[0]

    H_select = sum(
        Constraint((sum(x[(g, i)] for i in range(3)) - 1)**2,
                   label=f"one-hot_{g}")
        for g in groups
    )

    H_time = sum(
        route_options[(g, idx)]["time"] * groups[g] * x[(g, idx)]
        for (g, idx) in route_options
    )

    all_edges = set(e for data in route_options.values() for e in data["edges"])

    H_congestion = 0
    for e in all_edges:
        total_load = sum(
            groups[g] * x[(g, idx)]
            for (g, idx), data in route_options.items()
            if e in data["edges"]
        )
        H_congestion += (total_load - 0.5)**2

    A, B, C = 10**6, 1, 10
    H = A * H_select + B * H_time + C * H_congestion

    model = H.compile()
    qubo, offset = model.to_qubo()

    sampler = neal.SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(qubo, num_reads=30)
    decoded = model.decode_sampleset(sampleset)[0]

    # ==========
    # 結果整形
    # ==========
    result = {}
    edge_load = {e: 0 for e in all_edges}

    for g in groups:
        for idx in range(3):
            var_name = f"x_{g}_{idx}[0]"
            if decoded.sample[var_name] == 1:
                route = route_options[(g, idx)]
                result[g] = route["edges"]

                for e in route["edges"]:
                    edge_load[e] += groups[g]

    return {
        "routes": result,
        "edge_load": edge_load
    }