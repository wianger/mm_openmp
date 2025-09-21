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

# 分离串行和并行算法
serial_algorithms = ["1d_array", "baseline", "blocking", "loop_interchange"]
parallel_algorithms = [
    "omp_1d_array",
    "omp_blocking",
    "omp_loop_interchange",
    "omp_naive",
]

# 创建颜色映射
colors_serial = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
colors_parallel = ["#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]

# 创建图形
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# 绘制串行算法性能
for i, algo in enumerate(serial_algorithms):
    algo_data = data[data["algorithm_type"] == algo]
    ax1.loglog(
        algo_data["N"],
        algo_data["GFLOPS/s"],
        marker="o",
        markersize=6,
        linewidth=2,
        color=colors_serial[i],
        label=algo,
    )

# 绘制并行算法性能
for i, algo in enumerate(parallel_algorithms):
    algo_data = data[data["algorithm_type"] == algo]
    ax2.loglog(
        algo_data["N"],
        algo_data["GFLOPS/s"],
        marker="s",
        markersize=6,
        linewidth=2,
        color=colors_parallel[i],
        label=algo.replace("omp_", ""),
    )

# 设置轴标签和标题
ax1.set_ylabel("GFLOPS/s", fontsize=12)
ax2.set_ylabel("GFLOPS/s", fontsize=12)
ax2.set_xlabel("Matrix Size (N)", fontsize=12)
ax1.set_title("Serial Algorithms Performance", fontsize=14, pad=15)
ax2.set_title("Parallel (OpenMP) Algorithms Performance", fontsize=14, pad=15)

# 设置网格
ax1.grid(True, which="both", linestyle="--", alpha=0.4)
ax2.grid(True, which="both", linestyle="--", alpha=0.4)

# 添加图例
ax1.legend(frameon=True, fancybox=True, shadow=True, ncol=2)
ax2.legend(frameon=True, fancybox=True, shadow=True, ncol=2)

# 设置x轴刻度
n_values = sorted(data["N"].unique())
ax1.set_xticks(n_values)
ax2.set_xticks(n_values)
ax1.get_xaxis().set_major_formatter(ScalarFormatter())
ax2.get_xaxis().set_major_formatter(ScalarFormatter())

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig("matrix_multiplication_performance.png")
plt.savefig("matrix_multiplication_performance.pdf")

plt.show()

# 创建性能提升对比图
fig, ax = plt.subplots(1, 1, figsize=(8, 6))

# 计算相对于baseline的性能提升
baseline_data = data[data["algorithm_type"] == "baseline"].set_index("N")["GFLOPS/s"]
parallel_baseline = data[data["algorithm_type"] == "omp_naive"].set_index("N")[
    "GFLOPS/s"
]

# 选择要展示的算法
algorithms_to_show = ["loop_interchange", "omp_loop_interchange", "omp_naive"]
colors = ["#2ca02c", "#e377c2", "#7f7f7f"]
labels = ["Loop Interchange (Serial)", "Loop Interchange (OpenMP)", "Naive (OpenMP)"]

for i, algo in enumerate(algorithms_to_show):
    algo_data = data[data["algorithm_type"] == algo].set_index("N")["GFLOPS/s"]
    if algo.startswith("omp"):
        speedup = algo_data / parallel_baseline
    else:
        speedup = algo_data / baseline_data
    ax.semilogx(
        speedup.index,
        speedup,
        marker="o",
        markersize=6,
        linewidth=2,
        color=colors[i],
        label=labels[i],
    )

ax.set_xlabel("Matrix Size (N)", fontsize=12)
ax.set_ylabel("Speedup Ratio", fontsize=12)
ax.set_title("Performance Speedup Relative to Baseline", fontsize=14, pad=15)
ax.grid(True, which="both", linestyle="--", alpha=0.4)
ax.legend(frameon=True, fancybox=True, shadow=True)

# 设置x轴刻度
ax.set_xticks(n_values)
ax.get_xaxis().set_major_formatter(ScalarFormatter())

plt.tight_layout()
plt.savefig("performance_speedup.png")
plt.savefig("performance_speedup.pdf")
plt.show()

# 创建执行时间热图
# 准备数据
time_data = data.pivot(index="N", columns="algorithm_type", values="time(s)")

# 计算对数尺度下的执行时间（便于可视化）
log_time_data = np.log10(time_data)

# 创建热图
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
im = ax.imshow(log_time_data, cmap="viridis_r", aspect="auto")

# 设置标签
ax.set_xticks(np.arange(len(time_data.columns)))
ax.set_yticks(np.arange(len(time_data.index)))
ax.set_xticklabels(time_data.columns, rotation=45, ha="right")
ax.set_yticklabels(time_data.index)

# 添加颜色条
cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label("log10(Execution Time (s))", rotation=270, labelpad=20)

# 添加数值标注
for i in range(len(time_data.index)):
    for j in range(len(time_data.columns)):
        text = ax.text(
            j,
            i,
            f"{time_data.iloc[i, j]:.2e}",
            ha="center",
            va="center",
            color="w",
            fontsize=7,
        )

ax.set_title("Execution Time by Algorithm and Matrix Size", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("execution_time_heatmap.png")
plt.savefig("execution_time_heatmap.pdf")
plt.show()
