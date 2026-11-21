import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_idea_focused_presentation(output_path="d:/Fraud Detection/docs/FRAUDSHIELD_FINAL_EXAM_PRESENTATION.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Modern Executive Academic Color Palette
    C_NAVY_DARK   = RGBColor(15, 23, 42)    # #0f172a - Deep Obsidian Navy
    C_NAVY_MED    = RGBColor(30, 41, 59)    # #1e293b
    C_BLUE        = RGBColor(37, 99, 235)   # #2563eb - Academic Blue
    C_EMERALD     = RGBColor(5, 150, 105)   # #059669 - Positive / Solution Green
    C_AMBER       = RGBColor(217, 119, 6)   # #d97706 - Warning / Tradeoff Amber
    C_RED         = RGBColor(225, 29, 72)   # #e11d48 - Problem Crimson
    C_SLATE_BG    = RGBColor(248, 250, 252) # #f8fafc - Light background
    C_CARD_BG     = RGBColor(255, 255, 255) # White
    C_CARD_BORDER = RGBColor(226, 232, 240) # #e2e8f0
    C_TEXT_MAIN   = RGBColor(30, 41, 59)    # #1e293b
    C_TEXT_MUTED  = RGBColor(100, 116, 139) # #64748b
    C_WHITE       = RGBColor(255, 255, 255)

    def add_header(slide, title, category="THE BIG IDEA • CONCEPTUAL & METHODOLOGICAL DEFENSE", slide_num=""):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
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
    # SLIDE 1: TITLE SLIDE - THE CORE CONCEPT
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()
    
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_BLUE
    accent.line.fill.background()

    logo_path = "d:/Fraud Detection/reports/assets/uem_logo.jpeg"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.9), Inches(0.8), height=Inches(1.2))

    tb_title = s1.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(11.5), Inches(2.6))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    
    p_badge = tf_t.paragraphs[0]
    p_badge.text = "CAPSTONE PROJECT DEFENSE • CONCEPTUAL & METHODOLOGICAL OVERVIEW"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(147, 197, 253)
    
    p_main = tf_t.add_paragraph()
    p_main.text = "FRAUDSHIELD: RETHINKING FINANCIAL FRAUD DETECTION"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_before = Pt(8)
    
    p_sub = tf_t.add_paragraph()
    p_sub.text = "An Idea-Driven Framework for Extreme Class Imbalance, Explainable Governance, and Ephemeral Privacy"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(10)

    # Info cards
    add_card(s1, Inches(0.9), Inches(5.1), Inches(5.5), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_std = s1.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(5.1), Inches(1.3))
    tfs = tb_std.text_frame
    tfs.word_wrap = True
    ps1 = tfs.paragraphs[0]
    ps1.text = "RESEARCH TEAM:"
    ps1.font.size = Pt(10)
    ps1.font.bold = True
    ps1.font.color.rgb = C_BLUE
    ps2 = tfs.add_paragraph()
    ps2.text = "Prithwiraj Rakshit & Team (B.Tech CSE)\nDepartment of Computer Science & Engineering"
    ps2.font.size = Pt(12)
    ps2.font.color.rgb = C_WHITE

    add_card(s1, Inches(6.8), Inches(5.1), Inches(5.6), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_gd = s1.shapes.add_textbox(Inches(7.0), Inches(5.25), Inches(5.2), Inches(1.3))
    tfg = tb_gd.text_frame
    tfg.word_wrap = True
    pg1 = tfg.paragraphs[0]
    pg1.text = "INSTITUTION & SUPERVISION:"
    pg1.font.size = Pt(10)
    pg1.font.bold = True
    pg1.font.color.rgb = C_EMERALD
    pg2 = tfg.add_paragraph()
    pg2.text = "University of Engineering & Management (UEM), Kolkata\nProject Guide & Faculty Supervisor"
    pg2.font.size = Pt(12)
    pg2.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: THE CORE INTELLECTUAL DILEMMA
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Real-World Dilemma: Why Fraud AI Fails Today", slide_num="02")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "1. The 'Accuracy Paradox'", C_RED)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The 577:1 Imbalance Trap:\n  In financial data, 99.83% of transactions are legitimate. Only 0.17% are fraud.\n\n• The Illusion of Success:\n  A trivial model that predicts 'Always Genuine' achieves 99.8% accuracy on paper, yet catches zero attacks.\n\n• Standard loss gradients are overwhelmed by millions of ordinary grocery purchases, blinding the AI to sophisticated attacks."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "2. The False Decline Crisis", C_AMBER)
    tb = s2.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Hidden Financial Bleed:\n  Global banks lose significantly MORE revenue to 'False Declines' (wrongly blocking real shoppers) than to actual fraud.\n\n• Customer Experience Ruin:\n  When a card is declined at a store or airport, 33% of cardholders permanently abandon that payment card.\n\n• Traditional ML achieves high recall only by spraying false alarms indiscriminately."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "3. The Black-Box Trust Gap", C_BLUE)
    tb = s2.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Probability != Decision:\n  Telling a compliance officer or user that 'Risk = 0.87' is useless without the underlying WHY.\n\n• Legal Mandate (GDPR Art. 22):\n  Financial institutions are legally forbidden from taking automated actions without a 'Right to Explanation'.\n\n• Without transparent justification, AI cannot be deployed in regulated banking."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 3: THE BIG IDEA - THE 3 FOUNDATIONAL PILLARS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Big Idea: FraudShield's Tri-Pillar Paradigm", slide_num="03")

    pillars = [
        ("Pillar I: Adaptive Attention via Focal Loss", 
         "Instead of generating fake synthetic data (SMOTE) or tuning heuristic rules, we modify the loss gradient itself. We dynamically suppress the loss of easy genuine examples so the AI is forced to learn rare, deceptive fraud patterns.", 
         C_BLUE, Inches(0.8), Inches(1.7)),
        
        ("Pillar II: Human-in-the-Loop Explainable Governance", 
         "AI should not replace human agency; it should empower it. We translate high-dimensional neural representations into transparent, plain-English reasons (Amount anomaly, time mismatch, unverified device) for instant auditability.", 
         C_EMERALD, Inches(6.8), Inches(1.7)),
        
        ("Pillar III: Ephemeral Zero-Persistence Privacy", 
         "Users should not have to surrender banking privacy to scan for anomalies. By decrypting and analyzing statements entirely in volatile RAM with zero disk writes, we guarantee complete financial data sovereignty.", 
         C_AMBER, Inches(0.8), Inches(4.4)),
        
        ("Pillar IV: Risk-Calibrated Proportional Intervention", 
         "Abandoning binary 'Approve vs Block' thinking. Real-world payments need a tiered response: Clean transactions pass instantly, ambiguous anomalies trigger step-up 2FA, and only definitive attacks are guarded.", 
         C_NAVY_DARK, Inches(6.8), Inches(4.4))
    ]

    for title, desc, col, l, t in pillars:
        add_card(s3, l, t, Inches(5.7), Inches(2.4), title, col)
        tb = s3.shapes.add_textbox(l + Inches(0.25), t + Inches(0.65), Inches(5.2), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 4: WHY EXISTING IDEAS FALL SHORT
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Conceptual Critique: Why Traditional Approaches Fail", slide_num="04")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "Flaw of Rule Engines", C_AMBER)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Static & Brittle:\n  Hardcoded if-else thresholds (e.g. 'Flag if amount > ₹50,000') fail against modern fraud.\n\n• Easy to Evade:\n  Fraud rings easily bypass rules by structuring smaller transactions (micro-smurfing).\n\n• Zero Context:\n  Cannot discern whether a midnight luxury purchase is a fraudster or a loyal customer at an international airport."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s4, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "Flaw of SMOTE Resampling", C_RED)
    tb = s4.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Fake Data Artifacts:\n  SMOTE creates synthetic fraud cases by linearly interpolating between existing points.\n\n• Boundary Contamination:\n  Synthetic points often fall squarely into genuine transaction clusters, blurring real decision boundaries.\n\n• Results in hundreds of false positives and drops Precision below acceptable banking thresholds."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s4, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "Flaw of Standard Cross-Entropy", C_BLUE)
    tb = s4.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Gradient Avalanche:\n  In standard Cross-Entropy, 99.8% easy genuine examples generate small errors that sum up into massive gradient updates.\n\n• The Shortcut Trap:\n  The neural network takes the path of least resistance: optimize exclusively for genuine transactions and ignore the 0.17% fraud.\n\n• Misses almost 29% of real attacks."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: CORE IDEA 1 - FOCAL LOSS MATHEMATICAL INTUITION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Core Idea 1: Dynamic Hard-Example Mining with Focal Loss", slide_num="05")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Conceptual Shift in Machine Learning", C_BLUE)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Human Learning Analogy:\n  Students do not master complex subjects by repeatedly reviewing questions they already answer with 100% confidence. Real learning occurs by dedicating energy to the questions they get wrong.\n\n• Standard Cross-Entropy does the opposite:\n  It spends 99.8% of its time re-verifying obvious coffee purchases.\n\n• The Focal Loss Solution (Lin et al.):\n  Instead of altering the dataset, we reshape the loss curve directly:\n\n     FL(pt) = - αt * (1 - pt)^γ * log(pt)"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Modulating Factor: How it Works", C_EMERALD)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Magic of the Modulating Factor (1 - pt)^γ:\n\n  1. When a transaction is easily identified (pt = 0.99):\n     (1 - 0.99)^2 = 0.0001 (Loss is discounted by 99.99%!)\n     Result: The model ignores obvious normal transactions.\n\n  2. When a transaction is deceptive / hard (pt = 0.30):\n     (1 - 0.30)^2 = 0.49 (Loss receives full attention!)\n     Result: Gradients focus strictly on subtle, hidden fraud.\n\n• The Impact:\n  Eliminates the need for artificial resampling (SMOTE) while automatically mining hard fraud cases during training."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 6: CORE IDEA 2 - EXPLAINABLE GOVERNANCE (XAI)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Idea 2: Explainable AI as a Human-Trust Bridge", slide_num="06")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "From Numbers to Narrative", C_EMERALD)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Cognitive Gap in Banking:\n  A bank analyst cannot contact a customer and say: 'Your transaction was declined because activation node 27 was 0.89.'\n\n• Feature Attribution Engine:\n  We translate high-dimensional latent activations into contextual human pillars:\n  - Baseline Divergence: 'Spend is 8.4x higher than personal 30-day norm.'\n  - Temporal Heuristics: 'Conducted at 03:15 AM (Off-peak threat window).'\n  - Environmental Signals: 'New browser fingerprint / Foreign IP origin.'\n\n• Compliance Ready: Directly fulfills GDPR Art. 22."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Risk-Calibrated Interventions", C_BLUE)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Moving Beyond Binary 'Block vs Allow':\n\n  🟢 Tier 1: Low Risk (0% – 30%)\n  • Immediate frictionless approval.\n  • Verified credentials, domestic merchant, habitual spending.\n\n  🟡 Tier 2: Elevated Risk (31% – 70%)\n  • Proportional Step-Up Challenge (SMS OTP / Biometric).\n  • Prevents unnecessary card freezes for genuine users traveling or making rare purchases.\n\n  🔴 Tier 3: High Threat (71% – 100%)\n  • Instant card safeguard + automated plain-language alert to user."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 7: CORE IDEA 3 - EPHEMERAL ZERO-TRUST PRIVACY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Core Idea 3: Ephemeral Zero-Persistence Privacy Architecture", slide_num="07")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Conventional Data Privacy Flaw", C_RED)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Third-Party OCR Trap:\n  Existing statement auditing services require customers to upload monthly statements to third-party cloud servers or OCR APIs.\n\n• Severe Privacy Violations:\n  Financial statements reveal account balances, home addresses, phone numbers, and complete lifestyle spending patterns.\n\n• Centralized Honey-Pots:\n  Storing customer statements in server databases creates prime targets for data breaches and regulatory fines (DPDP Act 2023)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "FraudShield's In-Memory Zero-Storage Paradigm", C_EMERALD)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• 100% Volatile RAM Execution:\n  Statements (PDF, Excel, CSV, encrypted ZIP) are streamed directly into ephemeral memory buffers. Zero bytes are written to server storage.\n\n• Smart Semantic Extraction:\n  100+ fuzzy aliases isolate transactions while stripping disclaimers, branch addresses, and metadata.\n\n• Instant Cryptographic Discard:\n  Once the neural anomaly pass completes, memory buffers are immediately purged. The server retains zero customer transaction data."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: EMPIRICAL VALIDATION OF THE IDEA (THE PROOF)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Empirical Validation: Proving the Concept with Data", slide_num="08")

    chart_path = "d:/Fraud Detection/reports/diagrams/MODEL_BENCHMARK_COMPARISON.png"
    if os.path.exists(chart_path):
        s8.shapes.add_picture(chart_path, Inches(0.8), Inches(1.65), width=Inches(7.4))

    add_card(s8, Inches(8.5), Inches(1.65), Inches(4.0), Inches(5.2), "Why the Idea Won", C_EMERALD)
    tb = s8.shapes.add_textbox(Inches(8.7), Inches(2.2), Inches(3.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Theoretical Hypothesis Confirmed:\n\n1. Logistic Regression Failed:\n  Triggered 1,487 false alarms because it lacks dynamic weight focusing.\n\n2. Standard BCE DNN Failed:\n  Overwhelmed by genuine class; missed 29% of real fraud.\n\n3. SMOTE + RF Stumbled:\n  Synthetic artifacts degraded Precision to 78%.\n\n4. Proposed Focal DNN Triumph:\n  • 84.4% F1-Score\n  • 87.1% PR-AUC\n  • Only 9 false alarms across 56,864 test transactions!"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 9: SYSTEM EMBODIMENT - HOW THE IDEA MANIFESTS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "System Embodiment: Translating the Concept to Reality", slide_num="09")

    uml_path = "d:/Fraud Detection/reports/diagrams/FRAUDSHIELD_UML_ACTIVITY_DIAGRAM.png"
    if os.path.exists(uml_path):
        s9.shapes.add_picture(uml_path, Inches(0.8), Inches(1.65), width=Inches(7.2))

    add_card(s9, Inches(8.3), Inches(1.65), Inches(4.2), Inches(5.2), "The Living System", C_BLUE)
    tb = s9.shapes.add_textbox(Inches(8.5), Inches(2.2), Inches(3.8), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Real-Time Gateway:\n  Sub-12ms response time allows the AI to sit directly on the authorization pipeline of online payment gateways.\n\n• Universal Consumer Access:\n  Web & mobile interfaces enable cardholders to audit whole statements with 1 tap.\n\n• Frictionless User Experience:\n  Focal Loss cuts false alarms by 99.4% compared to baseline regression, preserving customer trust while guarding assets."
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 10: SOCIETAL VISION & FUTURE SCOPE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "The Broader Vision: Societal Impact & Future Scope", slide_num="10")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Core Conceptual Contributions", C_EMERALD)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Solved the Imbalance Dilemma Mathematically:\n   Proved that adaptive loss modulation (Focal Loss) outperforms synthetic data manipulation (SMOTE).\n\n2. Rebuilt User & Regulator Trust:\n   Pioneered plain-language XAI to replace cryptic probabilities with human accountability.\n\n3. Pioneered Zero-Knowledge Privacy:\n   Proved that financial auditing does not require persistent server-side customer data collection."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Next Frontier: Federated Graph AI", C_BLUE)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Graph Neural Networks (GNNs):\n  Moving from individual transaction inspection to relational graph mining to catch distributed money-mule rings across accounts.\n\n• Cross-Institutional Federated Learning:\n  Enabling competing banks (SBI, HDFC, ICICI) to collaboratively train global fraud weights without exposing sensitive customer records to one another.\n\nThank you!\nWe welcome questions on our methodology & findings."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    saved_path = output_path
    try:
        prs.save(output_path)
        print(f"Successfully generated idea-focused presentation at: {output_path}")
    except PermissionError:
        saved_path = output_path.replace(".pptx", "_v2.pptx")
        prs.save(saved_path)
        print(f"Note: Original was locked by PowerPoint. Saved to: {saved_path}")
    
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        artifact_pptx = os.path.join(artifact_dir, os.path.basename(saved_path))
        shutil.copy(saved_path, artifact_pptx)
        print(f"Copied to artifact directory: {artifact_pptx}")

if __name__ == '__main__':
    build_idea_focused_presentation()
