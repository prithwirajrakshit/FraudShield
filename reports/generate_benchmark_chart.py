import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

def generate_benchmark_chart(output_path="d:/Fraud Detection/reports/diagrams/MODEL_BENCHMARK_COMPARISON.png"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Benchmark Data (from Table 5.3 in UEM Project Report)
    models = [
        "Logistic\nRegression",
        "Isolation\nForest",
        "Random\nForest",
        "Standard DNN\n(Binary Cross-Entropy)",
        "SMOTE +\nRandom Forest",
        "Proposed\nFocal DNN"
    ]
    
    precision = [0.612, 0.320, 0.882, 0.745, 0.781, 0.864]
    recall    = [0.581, 0.449, 0.735, 0.714, 0.796, 0.825]
    f1_score  = [0.596, 0.374, 0.802, 0.729, 0.788, 0.844]
    pr_auc    = [0.624, 0.312, 0.814, 0.751, 0.801, 0.871]
    
    # Dimensions & Bar Positions
    n_models = len(models)
    x = np.arange(n_models)
    bar_width = 0.18
    
    # Set Matplotlib Styling
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#cbd5e1'
    plt.rcParams['axes.linewidth'] = 1.2
    
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300, facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Professional academic color palette
    c_precision = '#2563eb' # Blue
    c_recall    = '#d97706' # Amber / Dark Yellow
    c_f1        = '#059669' # Emerald Green
    c_prauc     = '#7c3aed' # Purple
    
    # Plot Grouped Bars
    b1 = ax.bar(x - 1.5 * bar_width, precision, bar_width, label='Precision (Low False Alarms)', color=c_precision, edgecolor='white', linewidth=1, alpha=0.92)
    b2 = ax.bar(x - 0.5 * bar_width, recall,    bar_width, label='Recall (Fraud Capture Rate)',  color=c_recall,    edgecolor='white', linewidth=1, alpha=0.92)
    b3 = ax.bar(x + 0.5 * bar_width, f1_score,  bar_width, label='F1-Score (Balanced Accuracy)', color=c_f1,        edgecolor='white', linewidth=1, alpha=0.92)
    b4 = ax.bar(x + 1.5 * bar_width, pr_auc,    bar_width, label='PR-AUC (Precision-Recall Area)', color=c_prauc,  edgecolor='white', linewidth=1, alpha=0.92)
    
    # Highlight the Proposed Focal DNN with an elegant background box
    highlight_rect = plt.Rectangle((5 - 0.44, 0), 0.88, 1.05, 
                                   facecolor='#ecfdf5', edgecolor='#10b981', 
                                   linestyle='--', linewidth=1.5, zorder=0, alpha=0.6)
    ax.add_patch(highlight_rect)
    
    # Add Badge above Proposed Model
    ax.text(5, 0.94, '★ PROPOSED BEST\nF1: 84.4% | PR-AUC: 87.1%', 
            ha='center', va='center', fontsize=9.5, fontweight='bold', 
            color='#065f46',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#d1fae5', edgecolor='#059669', linewidth=1.2))
    
    # Add Value Labels on Top of Bars for the Proposed Focal DNN
    for bar, val in zip([b1[5], b2[5], b3[5], b4[5]], [0.864, 0.825, 0.844, 0.871]):
        height = bar.get_height()
        ax.annotate(f'{val:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),  # 4 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1e293b')
        
    # Also add F1 label for Random Forest (strongest baseline)
    ax.annotate(f'0.802',
                xy=(b3[2].get_x() + b3[2].get_width() / 2, b3[2].get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8, fontweight='semibold', color='#334155')

    # Styling Axes and Labels
    ax.set_ylabel('Score Metric (0.0 to 1.0)', fontsize=12, fontweight='bold', color='#1e293b', labelpad=10)
    ax.set_title('Figure 5.1: Comparative Performance Benchmark of Fraud Detection Models on Imbalanced Data\n(Evaluated on Test Partition: 56,864 Samples, 577:1 Class Imbalance Ratio)', 
                 fontsize=13, fontweight='bold', color='#0f172a', pad=18)
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10.5, fontweight='semibold', color='#1e293b')
    ax.set_ylim(0, 1.08)
    
    # Y-axis Gridlines
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#94a3b8')
    ax.set_axisbelow(True)
    
    # Legend Styling
    legend = ax.legend(loc='upper left', frameon=True, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=10, ncol=2)
    legend.get_title().set_fontweight('bold')
    
    # Explanatory annotation note at bottom
    plt.figtext(0.5, 0.015, 
                "Key Insight: Standard Accuracy is misleading on 577:1 imbalance. Proposed Focal DNN dynamically penalizes easy genuine transactions, achieving superior F1 (0.844) & PR-AUC (0.871).", 
                ha="center", fontsize=9.5, style="italic", color="#475569")
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    plt.close()
    print(f"Successfully generated high-resolution benchmark chart at: {output_path}")

    # Copy to artifacts directory so user can preview and download in chat
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        artifact_path = os.path.join(artifact_dir, "MODEL_BENCHMARK_COMPARISON.png")
        shutil.copy(output_path, artifact_path)
        print(f"Copied to artifact path: {artifact_path}")

if __name__ == '__main__':
    generate_benchmark_chart()
