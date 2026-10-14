import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

def generate_figures():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    summary_csv = RESULTS_DIR / "metrics_summary.csv"
    if not summary_csv.exists():
        print("No metrics_summary.csv found.")
        return

    df = pd.read_csv(summary_csv)
    
    # Configure style
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({"font.sans-serif": "Arial", "font.size": 11})

    # Figure 1: Retrieval Quality Metrics (P@5, Recall@5, F1@5)
    plt.figure(figsize=(9, 5))
    metrics_subset = ["Precision@5", "Recall@5", "F1@5"]
    melted = df.melt(id_vars=["Model"], value_vars=metrics_subset, var_name="Metric", value_name="Score")
    ax = sns.barplot(data=melted, x="Metric", y="Score", hue="Model", palette=["#3b82f6", "#10b981", "#8b5cf6"])
    plt.title("Information Retrieval Quality Comparison (NFCorpus Benchmark)", fontsize=13, weight="bold", pad=12)
    plt.ylabel("Score (0.0 - 1.0)")
    plt.ylim(0, 0.40)
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f"{h:.3f}", (p.get_x() + p.get_width() / 2., h + 0.008), ha='center', va='bottom', fontsize=9)
    plt.legend(title="Retrieval Model", loc="upper left")
    plt.tight_layout()
    fig1_path = FIGURES_DIR / "retrieval_quality.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[OK] Saved {fig1_path}")

    # Figure 2: Ranking Quality Metrics (MRR & nDCG@10)
    plt.figure(figsize=(8, 5))
    ranking_metrics = ["MRR", "nDCG@10"]
    melted_rank = df.melt(id_vars=["Model"], value_vars=ranking_metrics, var_name="Metric", value_name="Score")
    ax2 = sns.barplot(data=melted_rank, x="Metric", y="Score", hue="Model", palette=["#3b82f6", "#10b981", "#8b5cf6"])
    plt.title("Ranking Quality Comparison: MRR & nDCG@10", fontsize=13, weight="bold", pad=12)
    plt.ylabel("Score (0.0 - 1.0)")
    plt.ylim(0, 0.65)
    for p in ax2.patches:
        h = p.get_height()
        if h > 0:
            ax2.annotate(f"{h:.3f}", (p.get_x() + p.get_width() / 2., h + 0.01), ha='center', va='bottom', fontsize=9)
    plt.legend(title="Retrieval Model", loc="upper left")
    plt.tight_layout()
    fig2_path = FIGURES_DIR / "ranking_quality.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[OK] Saved {fig2_path}")

    # Figure 3: Latency Comparison (Mean vs Median Latency in ms)
    plt.figure(figsize=(8, 5))
    latency_metrics = ["Mean Latency (ms)", "Median Latency (ms)"]
    melted_lat = df.melt(id_vars=["Model"], value_vars=latency_metrics, var_name="Latency Metric", value_name="Time (ms)")
    ax3 = sns.barplot(data=melted_lat, x="Model", y="Time (ms)", hue="Latency Metric", palette=["#f59e0b", "#ef4444"])
    plt.title("Computational Query Latency Comparison", fontsize=13, weight="bold", pad=12)
    plt.ylabel("Latency per Query (Milliseconds)")
    plt.xticks(rotation=15)
    for p in ax3.patches:
        h = p.get_height()
        if h > 0:
            ax3.annotate(f"{h:.1f}ms", (p.get_x() + p.get_width() / 2., h + 0.8), ha='center', va='bottom', fontsize=9)
    plt.legend(title="Metric", loc="upper left")
    plt.tight_layout()
    fig3_path = FIGURES_DIR / "latency_comparison.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[OK] Saved {fig3_path}")

    # Figure 4: Error Category Breakdown
    error_csv = RESULTS_DIR / "error_analysis.csv"
    if error_csv.exists():
        err_df = pd.read_csv(error_csv)
        counts = err_df["error_category"].value_counts()
        plt.figure(figsize=(9, 5))
        ax4 = sns.barplot(x=counts.values, y=counts.index, palette="mako")
        plt.title("Failure & Error Category Distribution Across Evaluated Queries", fontsize=12, weight="bold", pad=12)
        plt.xlabel("Number of Failure Cases")
        for p in ax4.patches:
            w = p.get_width()
            ax4.annotate(f"{int(w)}", (w + 1, p.get_y() + p.get_height() / 2.), va='center', fontsize=10)
        plt.tight_layout()
        fig4_path = FIGURES_DIR / "error_categories.png"
        plt.savefig(fig4_path, dpi=300)
        plt.close()
        print(f"[OK] Saved {fig4_path}")

    print("\n[SUCCESS] All academic figures rendered to results/figures/!")

if __name__ == "__main__":
    generate_figures()
