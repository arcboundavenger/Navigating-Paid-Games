import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# 读取 Excel 文件
file_path = 'Steam_paid_game_stats.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 数据处理
subgenre_agg = df.groupby('Sub-Genre').agg(
    appid_count=('appid', 'count'),
    revenue_mean=('Revenue', 'mean'),
    revenue_sum=('Revenue', 'sum')
).reset_index()

# 准备聚类数据
X = subgenre_agg[['appid_count', 'revenue_sum']]

# 使用肘部法确定最佳聚类数量
sse = []
k_values = range(2, 11)  # 测试从 2 到 10 的聚类数
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)  # 计算 SSE

# 绘制肘部法图形
plt.figure(figsize=(8, 5))
plt.plot(k_values, sse, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('SSE (Sum of Squared Errors)')
plt.xticks(k_values)
plt.grid(True)
plt.show()

# 打印 SSE 值
for k, s in zip(k_values, sse):
    print(f'Number of clusters: {k}, SSE: {s}')

# 选择最佳聚类数（可以根据肘部图的结果选择）
best_n_clusters = 4  # 根据肘部法选择的聚类数量
kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
subgenre_agg['Cluster'] = kmeans.fit_predict(X)

# 使用 viridis 色图并手动设置颜色顺序
viridis = plt.get_cmap('viridis', best_n_clusters)
custom_order = [3, 1, 0, 2]  # 这里设置你想要的顺序
colors = [viridis(i) for i in custom_order]

# 确保每个簇的颜色一致
subgenre_agg['Color'] = subgenre_agg['Cluster'].map(lambda x: colors[x])

# 绘制气泡图
plt.figure(figsize=(9, 9))
scatter = plt.scatter(
    subgenre_agg['appid_count'],
    subgenre_agg['revenue_mean'],
    s=subgenre_agg['revenue_sum'] / 1e6,
    alpha=0.5,
    c=subgenre_agg['Color'],  # 使用自定义顺序的颜色
    edgecolors='w'
)

# 添加图例
legend_labels = [f'Cluster {i}' for i in range(best_n_clusters)]
for i in range(best_n_clusters):
    plt.scatter([], [], label=legend_labels[i], color=colors[i])

plt.legend(title='Clusters')

# 设置坐标轴
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Games')
plt.ylabel('Average Revenue (Unit: $)')

# 添加辅助线
revenue_upper_quartile = subgenre_agg['revenue_mean'].quantile(0.75)
appid_count_lower_quartile = subgenre_agg['appid_count'].quantile(0.25)
plt.axhline(y=revenue_upper_quartile, color='blue', linestyle='--', linewidth=0.5)
plt.axvline(x=appid_count_lower_quartile, color='blue', linestyle='--', linewidth=0.5)

plt.grid(True, linestyle='--', linewidth=0.5)

# 添加标签
for i in range(len(subgenre_agg)):
    plt.annotate(
        subgenre_agg['Sub-Genre'].iloc[i],
        (subgenre_agg['appid_count'].iloc[i], subgenre_agg['revenue_mean'].iloc[i]),
        fontsize=9,
        ha='right'
    )

plt.xlim(10**0, 10**4)
plt.ylim(10**4, 10**8)

# 保存图形
plt.savefig('game_sub_genres_analysis.png', bbox_inches='tight')
plt.show()

# 保存聚类结果到 Excel 文件
output_file_path = 'subgenre_clustering_results.xlsx'
subgenre_agg.to_excel(output_file_path, index=False)