import pandas as pd
import matplotlib.pyplot as plt


def load_and_preprocess_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    df['Release'] = pd.to_datetime(df['Release'])
    df['year'] = df['Release'].dt.year
    return df[(df['year'] >= 2003) & (df['year'] <= 2024)]


def calculate_cumulative_data(df):
    years = pd.Series(range(2003, 2025))
    cumulative_data = pd.DataFrame()

    for year in years:
        yearly_data = df[df['year'] <= year].groupby('Sub-Genre').agg(
            appid_count=('appid', 'count'),
            revenue_mean=('Revenue', 'mean'),
            revenue_sum=('Revenue', 'sum')
        ).reset_index()
        yearly_data['year'] = year
        cumulative_data = pd.concat([cumulative_data, yearly_data])

    return cumulative_data


def plot_corrected(cumulative_data, subgenres_to_plot):
    plt.figure(figsize=(8, 8))
    plt.grid(True, which='major', linestyle='-', alpha=0.6)

    for subgenre in subgenres_to_plot:
        data = cumulative_data[
            (cumulative_data['Sub-Genre'] == subgenre) &
            (cumulative_data['appid_count'] > 0) &
            (cumulative_data['revenue_mean'] > 0)
            ]
        if not data.empty:

            plt.plot(
                data['appid_count'],
                data['revenue_mean'],
                marker='.',
                linewidth=1,
                label=subgenre
            )

            plt.scatter(
                data['appid_count'],
                data['revenue_mean'],
                s=data['revenue_sum'] / 1e6,
                alpha=0.6,
                edgecolors='none'  # Borderless
            )

    # 严格固定坐标轴
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Number of Games')
    plt.ylabel('Average Revenue (USD)')
    plt.xlim(1, 10 ** 4)
    plt.ylim(10 ** 4, 10 ** 8)
    plt.legend(title='', loc='lower left', frameon=False)
    plt.tight_layout()
    plt.show()


def main():
    file_path = 'Steam_paid_game_stats.xlsx'
    df = load_and_preprocess_data(file_path)
    cumulative_data = calculate_cumulative_data(df)

    subgenres_to_plot = [
        'Grand Strategy',
        'Driving',
        'Turn-Based Strategy'
    ] # Choose the subgenres you want to plot

    plot_corrected(cumulative_data, subgenres_to_plot)


if __name__ == "__main__":
    main()