import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_system_flow(output_path="d:/Fraud Detection/reports/diagrams/SYSTEM_WORKFLOW_LANDSCAPE.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 10 x 6.8 inches - Perfect landscape ratio for Slide 9
    fig, ax = plt.subplots(figsize=(10, 6.6), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    
    # Fonts and Styling
    font_main = "DejaVu Sans"
    
    # Helper to draw rounded card
    def draw_card(x, y, w, h, bg_color, border_color, radius=2, lw=1.5):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad={radius},rounding_size=2",
            facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=2
        )
        ax.add_patch(box)
        return box

    def draw_arrow(x1, y1, x2, y2, color="#3b82f6", lw=2, style="simple"):
        arrow = patches.FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=14,
            color=color, linewidth=lw, zorder=3,
            connectionstyle="arc3,rad=0"
        )
        ax.add_patch(arrow)

    # =========================================================================
    # TITLE BANNER
    # =========================================================================
    ax.text(50, 96, "FRAUDSHIELD: END-TO-END WORKFLOW & DECISION PIPELINE", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#0f172a", family=font_main)
    ax.text(50, 92.5, "Real-Time Payment Simulation & In-Memory Bank Statement Scanner Flow", 
            ha="center", va="center", fontsize=9, color="#64748b", family=font_main)

    # =========================================================================
    # STAGE 1: USER INPUT (LEFT)
    # =========================================================================
    # Header badge
    ax.text(14, 87, "STEP 1: USER INPUT", ha="center", va="center", fontsize=10, fontweight="bold", color="#2563eb", family=font_main)
    
    # Track A: Single Transaction
    draw_card(2, 58, 24, 25, "#eff6ff", "#93c5fd", lw=1.5)
    ax.text(14, 78.5, "Live Payment Simulator", ha="center", va="center", fontsize=10, fontweight="bold", color="#1e40af", family=font_main)
    ax.text(14, 69, "• Amount (₹) & Category\n• Time (Night/Day window)\n• Trusted Device Fingerprint\n• Merchant & Channel", 
            ha="center", va="center", fontsize=8, color="#1e3a8a", family=font_main)

    # Track B: Statement Upload
    draw_card(2, 26, 24, 25, "#eff6ff", "#93c5fd", lw=1.5)
    ax.text(14, 46.5, "Bank Statement Upload", ha="center", va="center", fontsize=10, fontweight="bold", color="#1e40af", family=font_main)
    ax.text(14, 37, "• Monthly PDF or Excel\n• Encrypted / Password ZIP\n• Works with any bank\n  (SBI, HDFC, ICICI, etc.)", 
            ha="center", va="center", fontsize=8, color="#1e3a8a", family=font_main)

    # Label below inputs
    ax.text(14, 18, "Web (Next.js) or Mobile (Expo)", ha="center", va="center", fontsize=8.5, style="italic", color="#64748b", family=font_main)

    # Arrows from Step 1 to Step 2
    draw_arrow(27, 70, 36, 61, color="#2563eb")
    draw_arrow(27, 39, 36, 49, color="#2563eb")

    # =========================================================================
    # STAGE 2: FASTAPI BACKEND & PRIVACY (CENTER-LEFT)
    # =========================================================================
    ax.text(49, 87, "STEP 2: FASTAPI GATEWAY", ha="center", va="center", fontsize=10, fontweight="bold", color="#d97706", family=font_main)
    
    draw_card(37, 26, 24, 57, "#fffbeb", "#fde68a", lw=1.5)
    ax.text(49, 77, "In-Memory RAM Engine", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#92400e", family=font_main)
    
    # Bullet boxes inside Step 2
    steps_s2 = [
        ("Zero-Disk Privacy", "Files unlocked in RAM;\nNever saved to hard drive.", 64),
        ("Fuzzy Header Detection", "Maps 100+ column aliases\n(Txn Date, Dr, Debit, etc.)", 50),
        ("StandardScaler Normalization", "Scales amount & features\ninto 29 normalized inputs.", 36)
    ]
    for st_title, st_desc, pos_y in steps_s2:
        draw_card(38.5, pos_y - 4, 21, 9, "#ffffff", "#fef3c7", lw=1)
        ax.text(49, pos_y + 1.2, st_title, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#b45309", family=font_main)
        ax.text(49, pos_y - 2, st_desc, ha="center", va="center", fontsize=7.5, color="#78350f", family=font_main)

    # Arrow from Step 2 to Step 3
    draw_arrow(62, 55, 69, 55, color="#d97706")

    # =========================================================================
    # STAGE 3: PYTORCH FOCAL DNN (CENTER-RIGHT)
    # =========================================================================
    ax.text(78, 87, "STEP 3: AI MODEL", ha="center", va="center", fontsize=10, fontweight="bold", color="#059669", family=font_main)

    draw_card(70, 43, 27, 40, "#f0fdf4", "#a7f3d0", lw=1.5)
    ax.text(83.5, 78, "PyTorch Focal Neural Net", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#065f46", family=font_main)
    ax.text(83.5, 71, "• 29 Neural Inputs (V1-V28 + Amount)\n• 2 Dense Hidden Layers + Dropout\n• Loss: Focal Loss (γ = 2.0, α = 0.25)\n• Fast Inference: ~11.85 Milliseconds", 
            ha="center", va="center", fontsize=8, color="#047857", family=font_main)
    
    # Speed badge inside AI box
    draw_card(72, 47, 23, 6, "#d1fae5", "#34d399", lw=1)
    ax.text(83.5, 50, "Sub-12ms Real-Time Response", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#065f46", family=font_main)

    # Arrow from Step 3 down to Step 4 Output
    draw_arrow(83.5, 42, 83.5, 33, color="#059669")

    # =========================================================================
    # STAGE 4: DECISION & EXPLANATION (BOTTOM-RIGHT)
    # =========================================================================
    ax.text(83.5, 35, "STEP 4: SMART ACTION & EXPLANATION", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1e293b", family=font_main)

    # 3 Small Action Badges
    # Approved
    draw_card(69, 17, 8.5, 14, "#ecfdf5", "#6ee7b7", lw=1.2)
    ax.text(73.25, 27, "APPROVED", ha="center", va="center", fontsize=8, fontweight="bold", color="#065f46", family=font_main)
    ax.text(73.25, 21.5, "Risk < 30%\nInstant pass", ha="center", va="center", fontsize=7.5, color="#047857", family=font_main)

    # Challenge
    draw_card(79, 17, 9, 14, "#fffbeb", "#fcd34d", lw=1.2)
    ax.text(83.5, 27, "CHALLENGE", ha="center", va="center", fontsize=8, fontweight="bold", color="#92400e", family=font_main)
    ax.text(83.5, 21.5, "Risk 31-70%\nSend SMS OTP", ha="center", va="center", fontsize=7.5, color="#78350f", family=font_main)

    # Blocked
    draw_card(89.5, 17, 8.5, 14, "#fef2f2", "#fca5a5", lw=1.2)
    ax.text(93.75, 27, "BLOCKED", ha="center", va="center", fontsize=8, fontweight="bold", color="#991b1b", family=font_main)
    ax.text(93.75, 21.5, "Risk > 70%\nCard guarded", ha="center", va="center", fontsize=7.5, color="#b91c1c", family=font_main)

    # Explanation banner at bottom
    draw_card(69, 4, 29, 9, "#f8fafc", "#cbd5e1", lw=1)
    ax.text(83.5, 9.5, "Explainable AI (XAI) Output", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1e293b", family=font_main)
    ax.text(83.5, 6, "Plain-English reasons: High amount, midnight timing, untrusted device.", ha="center", va="center", fontsize=7, color="#475569", family=font_main)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="#ffffff")
    plt.close()
    print(f"Successfully generated landscape system workflow diagram at: {output_path}")

    # Copy to artifacts directory
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        artifact_path = os.path.join(artifact_dir, "SYSTEM_WORKFLOW_LANDSCAPE.png")
        shutil.copy(output_path, artifact_path)
        print(f"Copied to artifact directory: {artifact_path}")

if __name__ == '__main__':
    draw_system_flow()
