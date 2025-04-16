import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# 读取 Excel 文件
file_path = 'Steam_paid_game_stats.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 确保 Revenue 列是数值类型
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

# 将 Release 列转换为日期格式
df['Release'] = pd.to_datetime(df['Release'])

# 设置图形布局（2行3列）
fig, axs = plt.subplots(2, 3, figsize=(18, 12))

# 定义时间段
years = [2013, 2015, 2017, 2019, 2021, 2023]
start_year = 1970

# 定义颜色映射
cmap = plt.get_cmap('viridis', 4)  # 使用 'viridis' 色图，设置 4 种颜色

# 遍历每个时间段生成气泡图
for i, year in enumerate(years):
    # 筛选数据
    filtered_df = df[(df['Release'] >= f'{start_year}-01-01') & (df['Release'] <= f'{year}-12-31')]

    # 按 Sub-Genre 分组
    subgenre_agg = filtered_df.groupby('Sub-Genre').agg(
        appid_count=('appid', 'count'),
        revenue_mean=('Revenue', 'mean'),
        revenue_sum=('Revenue', 'sum')
    ).reset_index()

    # 计算辅助线的值
    revenue_upper_quartile = subgenre_agg['revenue_mean'].quantile(0.75)
    appid_count_lower_quartile = subgenre_agg['appid_count'].quantile(0.25)

    # 准备聚类数据
    X = subgenre_agg[['appid_count', 'revenue_sum']]

    # K-means 聚类
    kmeans = KMeans(n_clusters=4, random_state=0)
    subgenre_agg['Cluster'] = kmeans.fit_predict(X)

    # 确保每个簇的颜色一致
    unique_clusters = np.unique(subgenre_agg['Cluster'])
    cluster_colors = {cluster: cmap(i) for i, cluster in enumerate(unique_clusters)}

    # 如果是 2013 年，手动对调绿色和黄色
    if year == 2013:
        # 对调颜色
        cluster_colors[unique_clusters[2]], cluster_colors[unique_clusters[3]] = cluster_colors[unique_clusters[3]], cluster_colors[unique_clusters[2]]

    # 选择子图（2行3列）
    ax = axs[i // 3, i % 3]

    # 绘制气泡图
    sizes = subgenre_agg['revenue_sum'] / 1e6
    scatter = ax.scatter(
        subgenre_agg['appid_count'],
        subgenre_agg['revenue_mean'],
        s=sizes,
        alpha=0.5,
        c=subgenre_agg['Cluster'].map(cluster_colors),
        edgecolors='w'
    )

    ax.set_xscale('log')
    ax.set_yscale('log')

    # 设置辅助线为蓝色
    ax.axhline(y=revenue_upper_quartile, color='blue', linestyle='--', linewidth=0.5)
    ax.axvline(x=appid_count_lower_quartile, color='blue', linestyle='--', linewidth=0.5)

    ax.grid(True, linestyle='--', linewidth=0.5)

    # 添加标签
    for j in range(len(subgenre_agg)):
        ax.annotate(
            subgenre_agg['Sub-Genre'].iloc[j],
            (subgenre_agg['appid_count'].iloc[j], subgenre_agg['revenue_mean'].iloc[j]),
            fontsize=9,
            ha='right'
        )

    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Average Revenue (Unit: $)')
    ax.set_xlim(10 ** 0, 10 ** 4)
    ax.set_ylim(10 ** 4, 10 ** 8)

    # 在右上角添加年份标注
    ax.text(0.95, 0.95, str(year), transform=ax.transAxes,
            fontsize=14, ha='right', va='top')

# 调整布局
plt.tight_layout()

# 保存图形为 PNG 文件
plt.savefig('3x2fig.png', bbox_inches='tight', dpi=300)

# 显示图形
plt.show()