import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter, LogFormatter
import matplotlib.font_manager as fm

# 解决字体问题
try:
    # 尝试设置Times New Roman字体
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
except:
    # 如果失败，使用系统默认serif字体
    plt.rcParams["font.family"] = "serif"
    print("Times New Roman not found, using default serif font")

# 设置科学期刊风格
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.rcParams["figure.titlesize"] = 16
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["savefig.pad_inches"] = 0.1
plt.rcParams["mathtext.fontset"] = "stix"

# 读取数据
data = pd.read_csv("./result/result.csv")

algorithms = [
    "1d_array",
    "baseline",
    "blocking",
    "loop_interchange",
    "omp_1d_array",
    "omp_blocking",
    "omp_loop_interchange",
    "omp_naive",
    "openblas",
]

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
]

# 创建图形
n_values = sorted(data["N"].unique())
fig, ax = plt.subplots(1, 1)

# 绘制串行算法性能
for i, algo in enumerate(algorithms):
    algo_data = data[data["algorithm_type"] == algo]
    ax.loglog(
        algo_data["N"],
        algo_data["GFLOPS/s"],
        marker="o",
        markersize=6,
        linewidth=2,
        color=colors[i],
        label=algo,
    )
ax.set_ylabel("GFLOPS/s", fontsize=12)
ax.set_title("Algorithms Performance", fontsize=14, pad=15)
ax.grid(True, which="both", linestyle="--", alpha=0.4)
ax.legend(
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    frameon=True,
    fancybox=True,
    shadow=True,
)
ax.set_xticks(n_values)
ax.get_xaxis().set_major_formatter(ScalarFormatter())
plt.savefig("./result/algorithms_performance.png")
plt.savefig("./result/algorithms_performance.pdf")
