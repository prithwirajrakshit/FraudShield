import os
import matplotlib
# Use non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch

# Set cache dir to avoid permission warnings
os.environ['MPLCONFIGDIR'] = os.path.abspath('d:/Fraud Detection/.matplotlib_cache')
os.makedirs('d:/Fraud Detection/.matplotlib_cache', exist_ok=True)

def draw_uml_diagram(theme="light", output_path="uml_activity.png"):
    # Dimensions in inches (large canvas for ultra-sharp clarity)
    fig_w, fig_h = 17, 22
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    
    # Theme color definitions
    if theme == "light":
        bg_color = "#FFFFFF"
        text_main = "#0F172A"
        text_muted = "#475569"
        border_box = "#CBD5E1"
        track1_bg = "#F0F9FF"
        track1_border = "#0284C7"
        track1_header = "#0369A1"
        track2_bg = "#F8FAFC"
        track2_border = "#0D9488"
        track2_header = "#0F766E"
        node_bg = "#FFFFFF"
        node_border = "#64748B"
        diamond_bg = "#FEF3C7"
        diamond_border = "#D97706"
        diamond_text = "#92400E"
        arrow_color = "#334155"
        green_bg = "#ECFDF5"
        green_border = "#10B981"
        green_text = "#047857"
        amber_bg = "#FFFBEB"
        amber_border = "#F59E0B"
        amber_text = "#B45309"
        red_bg = "#FFF1F2"
        red_border = "#F43F5E"
        red_text = "#BE123C"
    else:
        bg_color = "#0B0F19"
        text_main = "#F8FAFC"
        text_muted = "#94A3B8"
        border_box = "#334155"
        track1_bg = "#082F49"
        track1_border = "#38BDF8"
        track1_header = "#7DD3FC"
        track2_bg = "#042F2E"
        track2_border = "#2DD4BF"
        track2_header = "#5EEAD4"
        node_bg = "#1E293B"
        node_border = "#475569"
        diamond_bg = "#451A03"
        diamond_border = "#F59E0B"
        diamond_text = "#FDE68A"
        arrow_color = "#94A3B8"
        green_bg = "#064E3B"
        green_border = "#34D399"
        green_text = "#A7F3D0"
        amber_bg = "#78350F"
        amber_border = "#FBBF24"
        amber_text = "#FDE68A"
        red_bg = "#881337"
        red_border = "#FB7185"
        red_text = "#FECDD3"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Helper: draw node
    def draw_box(x, y, w, h, text, subtext="", bg=node_bg, border=node_border, text_c=text_main, sub_c=text_muted, rx=1.2):
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={rx}",
            facecolor=bg, edgecolor=border, linewidth=1.5, zorder=3
        )
        ax.add_patch(box)
        if subtext:
            ax.text(x, y + 0.35, text, ha="center", va="center", fontsize=9, fontweight="bold", color=text_c, zorder=4, family="sans-serif")
            ax.text(x, y - 0.45, subtext, ha="center", va="center", fontsize=7.5, color=sub_c, zorder=4, family="sans-serif")
        else:
            ax.text(x, y, text, ha="center", va="center", fontsize=9, fontweight="bold", color=text_c, zorder=4, family="sans-serif")

    # Helper: draw diamond (decision)
    def draw_diamond(x, y, w, h, text, bg=diamond_bg, border=diamond_border, text_c=diamond_text):
        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        poly = Polygon(pts, facecolor=bg, edgecolor=border, linewidth=1.5, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha="center", va="center", fontsize=8, fontweight="bold", color=text_c, zorder=4, family="sans-serif")

    # Helper: draw arrow
    def draw_arrow(x1, y1, x2, y2, label="", label_pos=(0, 0), rad=0.0):
        arr = FancyArrowPatch(
            (x1, y1), (x2, y2),
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>", mutation_scale=11,
            color=arrow_color, linewidth=1.4, zorder=2
        )
        ax.add_patch(arr)
        if label:
            lx = (x1 + x2) / 2 + label_pos[0]
            ly = (y1 + y2) / 2 + label_pos[1]
            ax.text(lx, ly, label, ha="center", va="center", fontsize=7.5, fontweight="bold",
                    color=arrow_color, bbox=dict(boxstyle="round,pad=0.15", facecolor=bg_color, edgecolor="none", alpha=0.9), zorder=5)

    # ==========================================
    # HEADER / TITLE
    # ==========================================
    ax.text(50, 98.2, "FRAUDSHIELD: END-TO-END SYSTEM UML ACTIVITY DIAGRAM",
            ha="center", va="center", fontsize=15, fontweight="heavy", color=text_main, family="sans-serif")
    ax.text(50, 96.6, "Universal Multi-Platform Financial Cybersecurity & Real-Time Fraud Telemetry Architecture",
            ha="center", va="center", fontsize=9, color=text_muted, family="sans-serif")

    # ==========================================
    # START NODE
    # ==========================================
    c_start = Circle((50, 93.8), 1.0, facecolor="#0284C7" if theme == "light" else "#38BDF8", edgecolor=border_box, linewidth=1.2, zorder=4)
    ax.add_patch(c_start)
    ax.text(50, 93.8, "●", ha="center", va="center", fontsize=12, color="#FFFFFF", fontweight="bold")
    ax.text(50, 95.0, "App Initialized", ha="center", va="center", fontsize=8, fontweight="bold", color=text_muted)

    # Initial Decision Diamond
    draw_diamond(50, 89.6, 18, 3.8, "User Selects Gateway Mode")
    draw_arrow(50, 92.8, 50, 91.5)

    # ==========================================
    # SWIMLANE 1: TRACK 1 (LIVE GUARD) - LEFT
    # ==========================================
    swim1 = FancyBboxPatch((3, 9), 44, 76.5, boxstyle="round,pad=0.5,rounding_size=1.5",
                           facecolor=track1_bg, edgecolor=track1_border, linewidth=1.5, linestyle="--", alpha=0.45, zorder=1)
    ax.add_patch(swim1)
    ax.text(25, 84.0, "TRACK 1: REAL-TIME PAYMENT GUARD (LIVE GUARD)",
            ha="center", va="center", fontsize=10, fontweight="heavy", color=track1_header, family="sans-serif")

    draw_arrow(41, 89.6, 25, 81.2, label="Single Transaction", label_pos=(-1, 1.2), rad=0.15)

    draw_box(25, 79.5, 34, 3.0, "1. User Enters Payment Parameters", "Amount (₹), Merchant Category, Channel, Time, Device")
    draw_arrow(25, 78.0, 25, 74.8)

    draw_box(25, 73.2, 34, 2.8, "2. Client-Side Input Validation", "Ensure Amount > ₹0, Set Fallback Safeguards")
    draw_arrow(25, 71.8, 25, 68.4)

    draw_box(25, 66.8, 34, 3.0, "3. Asynchronous API POST Request", "Endpoint: /api/check-transaction (FastAPI Gateway)")
    draw_arrow(25, 65.3, 25, 62.0)

    draw_box(25, 60.4, 34, 3.0, "4. Feature Mapping & Scaling", "FeatureMapper projects inputs -> 29 continuous PCA features")
    draw_arrow(25, 58.9, 25, 55.6)

    draw_box(25, 54.0, 34, 3.0, "5. PyTorch Focal DNN Inference", "Computes raw logit z -> Sigmoid -> Fraud Probability p in [0, 1]")
    draw_arrow(25, 52.5, 25, 49.3)

    # Risk Tier Decision Diamond
    draw_diamond(25, 47.0, 24, 4.2, "Evaluate Risk Score (p)")

    # 3 Branches: Approved, Challenged, Blocked
    draw_box(11, 38.5, 13, 3.2, "APPROVED", "p < 30% (Cleared Safe)", bg=green_bg, border=green_border, text_c=green_text)
    draw_box(25, 38.5, 13, 3.2, "CHALLENGE", "30% <= p < 70% (2FA OTP)", bg=amber_bg, border=amber_border, text_c=amber_text)
    draw_box(39, 38.5, 13, 3.2, "BLOCKED", "p >= 70% (High Threat)", bg=red_bg, border=red_border, text_c=red_text)

    draw_arrow(18, 45.6, 11, 40.2, label="Low Risk", label_pos=(-1.8, 0.4), rad=0.1)
    draw_arrow(25, 44.9, 25, 40.2, label="Medium", label_pos=(1.8, 0.2))
    draw_arrow(32, 45.6, 39, 40.2, label="Severe", label_pos=(1.8, 0.4), rad=-0.1)

    # Re-converge to XAI
    draw_box(25, 28.5, 36, 3.2, "6. GDPR Article 22 Explainable AI (XAI)", "Synthesizes human reasons: Spending z-score, nocturnal hours, device trust")
    draw_arrow(11, 36.8, 20, 30.2, rad=-0.1)
    draw_arrow(25, 36.8, 25, 30.2)
    draw_arrow(39, 36.8, 30, 30.2, rad=0.1)

    draw_box(25, 20.0, 36, 3.0, "7. Render Live Security Telemetry UI", "Updates SVG Circular Risk Gauge, Tier Badges & Action Steps")
    draw_arrow(25, 26.8, 25, 21.6)

    # ==========================================
    # SWIMLANE 2: TRACK 2 (STATEMENT VAULT) - RIGHT
    # ==========================================
    swim2 = FancyBboxPatch((53, 9), 44, 76.5, boxstyle="round,pad=0.5,rounding_size=1.5",
                           facecolor=track2_bg, edgecolor=track2_border, linewidth=1.5, linestyle="--", alpha=0.45, zorder=1)
    ax.add_patch(swim2)
    ax.text(75, 84.0, "TRACK 2: UNIVERSAL STATEMENT SCANNER (VAULT)",
            ha="center", va="center", fontsize=10, fontweight="heavy", color=track2_header, family="sans-serif")

    draw_arrow(59, 89.6, 75, 81.2, label="Bank Statement", label_pos=(1, 1.2), rad=-0.15)

    draw_box(75, 79.5, 34, 3.0, "1. User Selects Bank Statement File", "Supports: Excel (.xlsx), CSV, PDF, or encrypted ZIP")
    draw_arrow(75, 78.0, 75, 74.8)

    draw_box(75, 73.2, 34, 2.8, "2. Native Multipart Upload Streaming", "Endpoint: /api/scan-statement (Streams file into RAM)")
    draw_arrow(75, 71.8, 75, 68.6)

    # Encryption Check Diamond
    draw_diamond(75, 66.5, 22, 3.8, "Is File Password-Protected?")

    # Branch: Protected without password -> Modal
    draw_box(92, 59.5, 14, 2.8, "Password Popup", "Prompts for DOB / PIN", bg=amber_bg, border=amber_border, text_c=amber_text)
    draw_arrow(86, 66.5, 92, 61.0, label="Yes, No PIN", label_pos=(2.2, 0.4), rad=-0.15)
    draw_arrow(92, 58.0, 78, 71.8, label="User submits PIN", label_pos=(2.5, -2.5), rad=-0.4)

    # Branch: Decrypt in RAM
    draw_box(65, 59.5, 18, 3.0, "In-Memory RAM Decryption", "msoffcrypto / pypdf / pyzipper (Zero disk writes)")
    draw_arrow(69, 64.6, 65, 61.1, label="Yes, With PIN", label_pos=(-2.2, 0.4), rad=0.1)

    # Decryption check diamond
    draw_diamond(65, 52.8, 16, 3.2, "Password Valid?")
    draw_arrow(65, 58.0, 65, 54.5)

    # If wrong password -> show error popup
    draw_box(86, 52.8, 13, 2.6, "Wrong PIN Alert", "Shows bank hints (DDMMYYYY)", bg=red_bg, border=red_border, text_c=red_text)
    draw_arrow(73, 52.8, 79.5, 52.8, label="Incorrect", label_pos=(0, 0.5))
    draw_arrow(86, 54.2, 80, 71.8, label="User Retries", label_pos=(3, -3.5), rad=-0.45)

    # If correct or unencrypted -> Continue to parsing
    draw_box(75, 43.5, 34, 3.2, "3. Candidate Header Scoring Engine", "Scans first 50 rows, scores 100+ fuzzy aliases (Date, Debit, Cr, Bal)")
    draw_arrow(75, 64.6, 75, 45.2, label="No (Plain File)", label_pos=(-2.5, 4.0))
    draw_arrow(65, 51.2, 72, 45.2, label="Correct PIN", label_pos=(-2.0, 0.4), rad=0.15)

    draw_box(75, 35.5, 34, 3.0, "4. Data Normalization & Hygiene", "Word-boundary regex filters noise, totals, and calendar dates")
    draw_arrow(75, 41.8, 75, 37.1)

    draw_box(75, 27.5, 34, 3.0, "5. Micro-Batch DNN Inference", "PyTorch Focal DNN scores all statement transactions in parallel")
    draw_arrow(75, 33.9, 75, 29.1)

    draw_box(75, 20.0, 36, 3.0, "6. Render Audit Telemetry Dashboard", "Displays KPI summary (Approved, Challenged, Blocked) & row feed")
    draw_arrow(75, 25.9, 75, 21.6)

    # ==========================================
    # FINAL CONVERGENCE & END NODE
    # ==========================================
    # Convergence point
    draw_arrow(25, 18.4, 46.5, 6.2, rad=0.2)
    draw_arrow(75, 18.4, 53.5, 6.2, rad=-0.2)

    # End Bullseye Circle (outer ring + solid inner circle)
    c_outer = Circle((50, 5.0), 1.4, facecolor="none", edgecolor=border_box, linewidth=2.0, zorder=4)
    c_inner = Circle((50, 5.0), 0.8, facecolor="#0284C7" if theme == "light" else "#38BDF8", edgecolor="none", zorder=5)
    ax.add_patch(c_outer)
    ax.add_patch(c_inner)
    ax.text(50, 2.5, "Workflow Completed (Awaiting Next Action)", ha="center", va="center", fontsize=8.5, fontweight="bold", color=text_muted)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=bg_color)
    plt.close()
    print(f"Successfully generated {output_path}")

if __name__ == '__main__':
    diagrams_dir = os.path.join(os.path.dirname(__file__), "diagrams")
    os.makedirs(diagrams_dir, exist_ok=True)
    light_path = os.path.join(diagrams_dir, "FRAUDSHIELD_UML_ACTIVITY_DIAGRAM.png")
    dark_path = os.path.join(diagrams_dir, "FRAUDSHIELD_UML_ACTIVITY_DARK.png")

    # 1. Clean Academic Light Theme (Perfect for reports, viva printouts, and guides)
    draw_uml_diagram(theme="light", output_path=light_path)
    
    # 2. Sleek Dark Cyber Theme (Perfect for presentations and dark slides)
    draw_uml_diagram(theme="dark", output_path=dark_path)
    
    # Also copy to artifacts directory for web download
    import shutil
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        shutil.copy(light_path, os.path.join(artifact_dir, "FRAUDSHIELD_UML_ACTIVITY_DIAGRAM.png"))
        shutil.copy(dark_path, os.path.join(artifact_dir, "FRAUDSHIELD_UML_ACTIVITY_DARK.png"))

