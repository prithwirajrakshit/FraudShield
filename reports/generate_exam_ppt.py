import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="d:/Fraud Detection/docs/FRAUDSHIELD_FINAL_EXAM_PRESENTATION.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Color Palette - Modern Executive Academic
    C_NAVY_DARK  = RGBColor(15, 23, 42)    # #0f172a
    C_NAVY_MED   = RGBColor(30, 41, 59)    # #1e293b
    C_BLUE       = RGBColor(37, 99, 235)   # #2563eb
    C_EMERALD    = RGBColor(5, 150, 105)   # #059669
    C_AMBER      = RGBColor(217, 119, 6)   # #d97706
    C_RED        = RGBColor(225, 29, 72)   # #e11d48
    C_SLATE_BG   = RGBColor(248, 250, 252) # #f8fafc
    C_CARD_BG    = RGBColor(255, 255, 255) # White
    C_CARD_BORDER= RGBColor(226, 232, 240) # #e2e8f0
    C_TEXT_MAIN  = RGBColor(30, 41, 59)    # #1e293b
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
    C_WHITE      = RGBColor(255, 255, 255)

    def add_header(slide, title, category="FRAUDSHIELD • B.TECH CAPSTONE PROJECT DEFENSE", slide_num=""):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE
        
        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK
        
        # Slide number
        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.5))
            ntf = num_box.text_frame
            np = ntf.paragraphs[0]
            np.text = f"{slide_num} / 10"
            np.alignment = PP_ALIGN.RIGHT
            np.font.size = Pt(11)
            np.font.bold = True
            np.font.color.rgb = C_TEXT_MUTED

    def add_card(slide, left, top, width, height, title="", title_color=C_BLUE, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
        return shape

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background full fill
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()
    
    # Accent top border
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_BLUE
    accent.line.fill.background()

    # Logo
    logo_path = "d:/Fraud Detection/reports/assets/uem_logo.jpeg"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.9), Inches(0.8), height=Inches(1.2))

    # Title text box
    tb_title = s1.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(11.5), Inches(2.5))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    
    p_badge = tf_t.paragraphs[0]
    p_badge.text = "FINAL YEAR CAPSTONE PROJECT DEFENSE • ACADEMIC YEAR 2026-27"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(147, 197, 253) # Light Blue
    
    p_main = tf_t.add_paragraph()
    p_main.text = "FRAUDSHIELD: REAL-TIME FINANCIAL FRAUD &\nANOMALY DETECTION SYSTEM"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_before = Pt(8)
    
    p_sub = tf_t.add_paragraph()
    p_sub.text = "Powered by Deep Focal Loss Neural Networks, Explainable AI (XAI), and Universal Statement Scanning"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(10)

    # Info footer cards
    # Left Card: Student
    add_card(s1, Inches(0.9), Inches(5.1), Inches(5.5), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_std = s1.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(5.1), Inches(1.3))
    tfs = tb_std.text_frame
    tfs.word_wrap = True
    ps1 = tfs.paragraphs[0]
    ps1.text = "SUBMITTED BY:"
    ps1.font.size = Pt(10)
    ps1.font.bold = True
    ps1.font.color.rgb = C_BLUE
    ps2 = tfs.add_paragraph()
    ps2.text = "Prithwiraj Rakshit & Team (B.Tech CSE)\nEnrollment: UEM Kolkata | Department of CSE"
    ps2.font.size = Pt(12)
    ps2.font.color.rgb = C_WHITE

    # Right Card: Guide & Dept
    add_card(s1, Inches(6.8), Inches(5.1), Inches(5.6), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_gd = s1.shapes.add_textbox(Inches(7.0), Inches(5.25), Inches(5.2), Inches(1.3))
    tfg = tb_gd.text_frame
    tfg.word_wrap = True
    pg1 = tfg.paragraphs[0]
    pg1.text = "UNDER THE SUPERVISION OF:"
    pg1.font.size = Pt(10)
    pg1.font.bold = True
    pg1.font.color.rgb = C_EMERALD
    pg2 = tfg.add_paragraph()
    pg2.text = "Project Guide / Supervisor\nUniversity of Engineering & Management (UEM), Kolkata"
    pg2.font.size = Pt(12)
    pg2.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Motivation & The 3 Critical Industry Challenges", slide_num="02")

    # Card 1: Class Imbalance
    add_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "1. Extreme Class Imbalance", C_RED)
    tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "• Fraud Rate is only ~0.17% (577:1 ratio).\n\n• The Accuracy Paradox: A naive model that classifies 100% of transactions as 'Genuine' scores 99.8% accuracy on paper, but catches 0 real frauds.\n\n• Standard Cross-Entropy loss gets overwhelmed by millions of easy genuine transactions."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MAIN

    # Card 2: Black Box
    add_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "2. The Black-Box AI Dilemma", C_AMBER)
    tb_c2 = s2.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "• Complex Neural Networks produce opaque probability numbers without justification.\n\n• High Customer Friction: Blocking legitimate credit cards with no explanation causes frustration & churn.\n\n• Regulatory Non-Compliance: GDPR (Article 22) mandates the 'Right to Explanation' for automated financial decisions."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MAIN

    # Card 3: Inconsistent Bank Formats
    add_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "3. Inconsistent Bank Formats", C_BLUE)
    tb_c3 = s2.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf3 = tb_c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "• Fragmented Schemas: SBI, HDFC, ICICI, and Axis all use different column names, date styles, and summary footers.\n\n• Password Protection: Many statements are encrypted PDFs or Excel files.\n\n• Data Privacy Risk: Third-party OCR web services compromise sensitive banking details."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 3: OBJECTIVES & SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Project Objectives & Technical Scope", slide_num="03")

    # 4 Pillar Cards
    pillars = [
        ("Deep Focal Loss Network", "Design and train a custom PyTorch Deep Neural Network that addresses extreme class imbalance dynamically without synthesizing distorted fake data (SMOTE).", C_BLUE, Inches(0.8), Inches(1.7)),
        ("Explainable AI (XAI) Engine", "Convert latent multi-dimensional feature activations into clear, human-intelligible justifications (e.g. abnormal amount multiplier, night-time hours, untrusted device).", C_EMERALD, Inches(6.8), Inches(1.7)),
        ("Universal Privacy Scanner", "Build an in-memory statement engine with 100+ fuzzy column aliases capable of parsing encrypted PDFs, Excel, CSV, and locked ZIPs with zero server disk storage.", C_AMBER, Inches(0.8), Inches(4.4)),
        ("Real-Time Full-Stack Delivery", "Develop sub-15ms FastAPI backend, interactive Next.js 16 Web Dashboard, and cross-platform React Native (Expo) Mobile App for real-world deployment.", C_NAVY_DARK, Inches(6.8), Inches(4.4))
    ]

    for title, desc, col, l, t in pillars:
        add_card(s3, l, t, Inches(5.7), Inches(2.4), title, col)
        tb = s3.shapes.add_textbox(l + Inches(0.25), t + Inches(0.65), Inches(5.2), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 4: END-TO-END SYSTEM ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "End-to-End System Architecture & Dataflow", slide_num="04")

    # Architecture diagram on left
    uml_path = "d:/Fraud Detection/reports/diagrams/FRAUDSHIELD_UML_ACTIVITY_DIAGRAM.png"
    if os.path.exists(uml_path):
        s4.shapes.add_picture(uml_path, Inches(0.8), Inches(1.65), width=Inches(7.2))
    
    # 3-Tier explanation card on right
    add_card(s4, Inches(8.3), Inches(1.65), Inches(4.2), Inches(5.2), "Key Architectural Flow", C_BLUE)
    tb_arc = s4.shapes.add_textbox(Inches(8.5), Inches(2.2), Inches(3.8), Inches(4.4))
    tfa = tb_arc.text_frame
    tfa.word_wrap = True
    p = tfa.paragraphs[0]
    p.text = "1. Client Ingestion Layer:\n• Next.js Web UI & React Native Mobile App capture live transactions or statement files.\n\n2. Security & Gateway Layer:\n• FastAPI validates payloads, decrypts locked PDFs ephemerally in RAM (zero-disk logging).\n\n3. Machine Learning Inference:\n• StandardScaler normalizes inputs.\n• PyTorch Focal DNN computes risk score in <12 milliseconds.\n\n4. Tri-Tier Decision & XAI:\n• 0-30%: Approved (Instant pass)\n• 31-70%: Challenged (SMS 2FA)\n• 71-100%: Blocked (Card guarded)"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: CORE INNOVATION 1 - DEEP FOCAL LOSS DNN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Core Technical Innovation: Deep Focal Neural Network", slide_num="05")

    # Left: Mathematical Foundation
    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Why Standard Loss Fails vs. Focal Loss", C_BLUE)
    tb_m = s5.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tfm = tb_m.text_frame
    tfm.word_wrap = True
    p = tfm.paragraphs[0]
    p.text = "• Binary Cross-Entropy (BCE) Loss:\n  Loss = - [ y * log(p) + (1-y) * log(1-p) ]\n  Problem: Millions of easy genuine transactions dominate total gradient updates, causing the model to neglect rare fraud.\n\n• Proposed Focal Loss Formulation (Lin et al.):\n  FL(pt) = - αt * (1 - pt)^γ * log(pt)\n\n• Key Parameters:\n  - γ = 2.0 (Focusing Parameter): Dynamically reduces loss for well-classified examples (pt > 0.5), focusing model exclusively on hard-to-classify fraudulent transactions.\n  - α = 0.25 (Class Balance Weight): Re-weights minority fraud class."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # Right: Network Architecture
    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Custom PyTorch Neural Architecture", C_EMERALD)
    tb_net = s5.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tfn = tb_net.text_frame
    tfn.word_wrap = True
    p = tfn.paragraphs[0]
    p.text = "• Input Layer: 29 PCA & numerical features (V1–V28 + Normalized Amount).\n\n• Hidden Layer 1: Linear(29 → 64) + LeakyReLU(0.1)\n  - Batch Normalization stabilizes internal covariate shift.\n  - Dropout (p=0.3) prevents overfitting to majority class.\n\n• Hidden Layer 2: Linear(64 → 32) + LeakyReLU(0.1)\n  - Dropout (p=0.2).\n\n• Output Layer: Linear(32 → 1) + Sigmoid Activation\n  - Outputs continuous fraud risk probability: p ∈ [0.0, 1.0].\n\n• Optimizer: Adam (lr = 0.001, Weight Decay = 1e-4)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 6: CORE INNOVATION 2 - XAI & STATEMENT SCANNER
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Technical Innovation: Explainable AI & Universal Scanner", slide_num="06")

    # Left: XAI Engine
    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Explainable AI (XAI) Engine", C_EMERALD)
    tb_xai = s6.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tfx = tb_xai.text_frame
    tfx.word_wrap = True
    p = tfx.paragraphs[0]
    p.text = "• Translates Complex Vectors into Plain English:\n  Neural probability numbers are decomposed into actionable risk factors for users and compliance auditors:\n\n• Primary Trigger Factors:\n  - Amount Anomaly: 'Transaction is 8.4x higher than cardholder's historical 30-day average.'\n  - Temporal Heuristics: 'Conducted during high-risk off-peak hours (03:15 AM).'\n  - Geolocation Vector: 'Cross-border merchant location mismatch.'\n  - Device Security: 'Unrecognized browser/mobile device fingerprint.'\n\n• GDPR Article 22 Compliance: Every flagged alert provides actionable advice for the customer."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # Right: Statement Scanner
    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Universal Bank Statement Parser", C_BLUE)
    tb_sc = s6.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tfc = tb_sc.text_frame
    tfc.word_wrap = True
    p = tfc.paragraphs[0]
    p.text = "• 100+ Fuzzy Header Aliases:\n  Dynamically maps non-standard column headers across SBI, HDFC, ICICI, Axis, PNB, Kotak, etc. (e.g. 'Txn Date', 'Value Dt', 'Dr', 'Debit Amount', 'Withdrawal').\n\n• Zero-Persistence In-Memory Decryption:\n  Password-protected PDFs & Excel files are unlocked in volatile RAM via msoffcrypto & pypdf. No personal customer data is stored on disk.\n\n• Smart Noise Slicing:\n  Filters out metadata disclaimers, branch details, and summary footers to extract clean transaction rows accurately."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 7: EXPERIMENTAL SETUP & DATASETS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Experimental Setup & Evaluation Methodology", slide_num="07")

    # 3 Stat Metric Boxes
    metrics = [
        ("284,807", "Total Transactions Evaluated", "ULB Credit Card Benchmark", Inches(0.8)),
        ("577 : 1", "Class Imbalance Ratio", "Only 492 Fraud Cases (0.17%)", Inches(4.8)),
        ("56,864", "Strict Out-of-Sample Test Set", "95 True Fraud Cases in Test", Inches(8.8))
    ]
    for val, lbl, sub, left in metrics:
        add_card(s7, left, Inches(1.7), Inches(3.7), Inches(1.4), "", bg_color=C_SLATE_BG)
        tb = s7.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(1.2))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = C_BLUE
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_DARK
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_TEXT_MUTED

    # Bottom Explanation Cards
    add_card(s7, Inches(0.8), Inches(3.4), Inches(5.7), Inches(3.5), "Dataset Preprocessing Pipeline", C_BLUE)
    tb_dp = s7.shapes.add_textbox(Inches(1.0), Inches(3.9), Inches(5.3), Inches(2.8))
    tfd = tb_dp.text_frame
    tfd.word_wrap = True
    p = tfd.paragraphs[0]
    p.text = "• Feature Normalization: Robust StandardScaler applied to transaction Amount to eliminate extreme spending outliers.\n• Stratified Splitting: 80% Training (228,061 rows) / 20% Testing (56,864 rows) maintaining exact fraud class ratios.\n• Secondary Validation: IEEE-CIS Fraud Benchmark (590,540 real transactions) verified generalization."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s7, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.5), "Why We Rejected Standard Accuracy", C_AMBER)
    tb_wa = s7.shapes.add_textbox(Inches(7.0), Inches(3.9), Inches(5.3), Inches(2.8))
    tfw = tb_wa.text_frame
    tfw.word_wrap = True
    p = tfw.paragraphs[0]
    p.text = "• Accuracy & ROC-AUC are Misleading:\n  With 56,769 genuine test samples, even 1,000 false alarms yield a False Positive Rate of only 1.7%, artificially inflating ROC-AUC to > 0.95.\n\n• Required Academic Metrics:\n  - Precision: Minimizes false alarms for legitimate users.\n  - Recall: Catches actual fraudulent transactions.\n  - PR-AUC & F1-Score: Harmonic evaluation on imbalanced data."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: RESULT ANALYSIS & BENCHMARK COMPARISON
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Result Analysis: Benchmark Performance Comparison", slide_num="08")

    # Embed generated Grouped Bar Chart on Left
    chart_path = "d:/Fraud Detection/reports/diagrams/MODEL_BENCHMARK_COMPARISON.png"
    if os.path.exists(chart_path):
        s8.shapes.add_picture(chart_path, Inches(0.8), Inches(1.65), width=Inches(7.4))

    # Right: Results Summary & Table Highlights
    add_card(s8, Inches(8.5), Inches(1.65), Inches(4.0), Inches(5.2), "Key Findings (Table 5.3)", C_EMERALD)
    tb_res = s8.shapes.add_textbox(Inches(8.7), Inches(2.2), Inches(3.6), Inches(4.5))
    tfr = tb_res.text_frame
    tfr.word_wrap = True
    p = tfr.paragraphs[0]
    p.text = "• Proposed Focal DNN vs. Baselines:\n\n1. Logistic Regression: 59.6% F1\n  - High recall (87%) but disastrous 5.3% precision (1,487 false alarms!).\n\n2. Standard DNN (BCE): 72.9% F1\n  - Suffers from class imbalance; misses 29% of real fraud transactions.\n\n3. SMOTE + Random Forest: 78.8% F1\n  - Synthetic data generation blurs decision boundaries.\n\n4. Proposed Focal DNN: 84.4% F1\n  - Highest Precision: 86.4%\n  - High Recall: 82.5%\n  - Superior PR-AUC: 87.1%\n  - Only 9 False Alarms out of 56,864 test transactions!"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 9: FULL-STACK CROSS-PLATFORM IMPLEMENTATION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Full-Stack Deployment & Cross-Platform Interfaces", slide_num="09")

    # 3 Cards: Backend, Web, Mobile
    add_card(s9, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "FastAPI Microservice", C_BLUE)
    tb_b = s9.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tfb = tb_b.text_frame
    tfb.word_wrap = True
    p = tfb.paragraphs[0]
    p.text = "• Lightning Fast: Average inference latency of 11.85 ms per transaction.\n\n• Endpoints:\n  - POST /api/check-transaction\n  - POST /api/scan-statement\n  - GET /api/health\n\n• In-Memory Stream Processing: Handles multi-page statements via streaming multipart buffers with zero disk writes."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s9, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "Next.js 16 Web Dashboard", C_NAVY_DARK)
    tb_w = s9.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tfw = tb_w.text_frame
    tfw.word_wrap = True
    p = tfw.paragraphs[0]
    p.text = "• Modern Tech Stack: Built with React, Next.js 16 (Turbopack), and Tailwind CSS.\n\n• Interactive Simulator: Test single transactions with configurable amount, channel, time, and merchant.\n\n• Animated Risk Gauge: Dynamic SVG radial threat meter with instant color response (Green / Amber / Red)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s9, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "React Native Mobile App", C_EMERALD)
    tb_mob = s9.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tfm = tb_mob.text_frame
    tfm.word_wrap = True
    p = tfm.paragraphs[0]
    p.text = "• Native Cross-Platform: Runs on Android & iOS via Expo SDK 58.\n\n• WinterCG Multipart Upload: Robust Uint8Array binary stream buffer satisfies modern mobile engines without crashes.\n\n• Statement Vault: Instant in-app audit of monthly bank statements with high-risk row highlighting."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion, Societal Impact & Future Scope", slide_num="10")

    # Conclusion Card
    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Conclusion & Achievements", C_EMERALD)
    tb_con = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tfc = tb_con.text_frame
    tfc.word_wrap = True
    p = tfc.paragraphs[0]
    p.text = "• Solved Extreme Imbalance: Focal Loss forces gradient updates on rare fraud cases without generating synthetic data artifacts.\n\n• Superior Results: 84.4% F1-score, 87.1% PR-AUC, and only 9 false positives across 56,864 test transactions.\n\n• Regulatory Compliance: Full GDPR Article 22 compliance through human-readable XAI justifications.\n\n• Production Ready: Cross-platform web and mobile apps operating with sub-15ms real-time latency."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # Future Scope Card
    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Future Scope & Q&A", C_BLUE)
    tb_fut = s10.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tff = tb_fut.text_frame
    tff.word_wrap = True
    p = tff.paragraphs[0]
    p.text = "1. Graph Neural Networks (GNNs):\n• Incorporate spatial-temporal transaction graphs to uncover coordinated money-mule syndicates.\n\n2. Privacy-Preserving Federated Learning:\n• Enable collaborative cross-bank fraud model training across institutions (SBI, HDFC, ICICI) without sharing raw cardholder records.\n\n3. Edge Deployment:\n• Quantize neural weights to ONNX/TensorRT for microsecond edge verification on POS terminals.\n\nThank you!\nQuestions & Feedback Welcome."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # Save presentation
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")
    
    # Copy to artifacts directory for chat download
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        artifact_pptx = os.path.join(artifact_dir, "FRAUDSHIELD_FINAL_EXAM_PRESENTATION.pptx")
        shutil.copy(output_path, artifact_pptx)
        print(f"Copied to artifact directory: {artifact_pptx}")

if __name__ == '__main__':
    build_presentation()
