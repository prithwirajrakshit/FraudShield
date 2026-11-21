import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_student_presentation(output_path="d:/Fraud Detection/docs/FRAUDSHIELD_FINAL_EXAM_PRESENTATION.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Clean & Simple Color Palette
    C_NAVY_DARK   = RGBColor(15, 23, 42)    # #0f172a
    C_NAVY_MED    = RGBColor(30, 41, 59)    # #1e293b
    C_BLUE        = RGBColor(37, 99, 235)   # #2563eb
    C_EMERALD     = RGBColor(16, 185, 129)  # #10b981
    C_AMBER       = RGBColor(245, 158, 11)  # #f59e0b
    C_RED         = RGBColor(239, 68, 68)   # #ef4444
    C_SLATE_BG    = RGBColor(248, 250, 252) # #f8fafc
    C_CARD_BG     = RGBColor(255, 255, 255) # White
    C_CARD_BORDER = RGBColor(226, 232, 240) # #e2e8f0
    C_TEXT_MAIN   = RGBColor(30, 41, 59)    # #1e293b
    C_TEXT_MUTED  = RGBColor(100, 116, 139) # #64748b
    C_WHITE       = RGBColor(255, 255, 255)

    def add_header(slide, title, category="3RD YEAR B.TECH CSE PROJECT PRESENTATION", slide_num=""):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE
        
        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK
        
        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.5))
            ntf = num_box.text_frame
            np = ntf.paragraphs[0]
            np.text = f"{slide_num} / 10"
            np.alignment = PP_ALIGN.RIGHT
            np.font.size = Pt(12)
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
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
        return shape

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
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
    p_badge.text = "B.TECH 3RD YEAR PROJECT DEFENSE • COMPUTER SCIENCE & ENGINEERING"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(147, 197, 253)
    
    p_main = tf_t.add_paragraph()
    p_main.text = "FRAUDSHIELD: SMART PAYMENT FRAUD DETECTION"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_before = Pt(8)
    
    p_sub = tf_t.add_paragraph()
    p_sub.text = "Catching Real Fraud Quickly Without Annoying Genuine Cardholders"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(10)

    # Info cards
    add_card(s1, Inches(0.9), Inches(5.1), Inches(5.5), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_std = s1.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(5.1), Inches(1.3))
    tfs = tb_std.text_frame
    tfs.word_wrap = True
    ps1 = tfs.paragraphs[0]
    ps1.text = "PRESENTED BY:"
    ps1.font.size = Pt(10)
    ps1.font.bold = True
    ps1.font.color.rgb = C_BLUE
    ps2 = tfs.add_paragraph()
    ps2.text = "Prithwiraj Rakshit & Team\n3rd Year B.Tech CSE | UEM Kolkata"
    ps2.font.size = Pt(12)
    ps2.font.color.rgb = C_WHITE

    add_card(s1, Inches(6.8), Inches(5.1), Inches(5.6), Inches(1.6), "", bg_color=C_NAVY_MED, border_color=RGBColor(51, 65, 85))
    tb_gd = s1.shapes.add_textbox(Inches(7.0), Inches(5.25), Inches(5.2), Inches(1.3))
    tfg = tb_gd.text_frame
    tfg.word_wrap = True
    pg1 = tfg.paragraphs[0]
    pg1.text = "GUIDED BY:"
    pg1.font.size = Pt(10)
    pg1.font.bold = True
    pg1.font.color.rgb = C_EMERALD
    pg2 = tfg.add_paragraph()
    pg2.text = "Project Supervisor / Faculty Guide\nDepartment of Computer Science & Engineering"
    pg2.font.size = Pt(12)
    pg2.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: WHY WE CHOSE THIS PROJECT (THE PROBLEM)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Real-World Problem: Why Fraud Detection Is Hard", slide_num="02")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "1. The 99% Accuracy Trap", C_RED)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• In credit card data, 99.8% of transactions are normal purchases, and only 0.2% are fraud.\n\n• If an AI model just marks EVERYTHING as 'Normal', it gets a 99.8% score on paper!\n\n• But in reality, it caught ZERO frauds. Standard models get lazy because normal examples are everywhere."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "2. Annoying False Alarms", C_AMBER)
    tb = s2.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Basic models try to catch fraud by blocking too many transactions.\n\n• Result: Real users get their cards declined at a restaurant, movie, or airport.\n\n• Studies show that 33% of people stop using their card completely after a single embarrassing false decline."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "3. The 'Black Box' Issue", C_BLUE)
    tb = s2.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Normal AI models only output a number like '87% Risk'.\n\n• They don't tell the user or the bank manager WHY it was blocked.\n\n• Banking laws require banks to give a clear reason if an automated system blocks someone's money."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 3: WHAT WE BUILT (OUR 4 MAIN GOALS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "What We Built: Our 4 Main Goals", slide_num="03")

    goals = [
        ("Goal 1: A Smarter AI Model (Focal Loss)", 
         "Instead of normal models that get confused by imbalanced data, we used 'Focal Loss' to make our AI focus strictly on difficult fraud cases.", 
         C_BLUE, Inches(0.8), Inches(1.7)),
        
        ("Goal 2: Plain-English Explanations (XAI)", 
         "Instead of just showing a percentage, our system explains the exact reason: like 'unusually high amount', 'late night purchase', or 'new device'.", 
         C_EMERALD, Inches(6.8), Inches(1.7)),
        
        ("Goal 3: Universal Bank Statement Scanner", 
         "Users can upload full monthly statements from any bank (SBI, HDFC, ICICI, etc.) in Excel or PDF, even if it is password-locked.", 
         C_AMBER, Inches(0.8), Inches(4.4)),
        
        ("Goal 4: Complete Working Demo (Web & Mobile)", 
         "We created a fast Python backend (runs in 11ms), a web dashboard to test transactions, and a mobile app to scan statements on a phone.", 
         C_NAVY_DARK, Inches(6.8), Inches(4.4))
    ]

    for title, desc, col, l, t in goals:
        add_card(s3, l, t, Inches(5.7), Inches(2.4), title, col)
        tb = s3.shapes.add_textbox(l + Inches(0.25), t + Inches(0.65), Inches(5.2), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 4: WHY OLD METHODS DON'T WORK WELL
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Why Existing Methods Fail in Practice", slide_num="04")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1), "1. Simple If-Else Rules", C_AMBER)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Basic rules like 'Flag if spend > ₹50,000' are very easy to bypass.\n\n• Fraudsters simply split stolen money into multiple small transfers of ₹5,000.\n\n• At the same time, it flags genuine people shopping during holiday festivals."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s4, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1), "2. Generating Fake Data (SMOTE)", C_RED)
    tb = s4.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• A common trick in college projects is SMOTE (creating fake fraud data points to balance the dataset).\n\n• But fake data often overlaps with real normal transactions.\n\n• The AI gets confused, resulting in hundreds of false alarms for normal users."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s4, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), "3. Standard Neural Networks", C_BLUE)
    tb = s4.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Normal deep learning treats every transaction with equal importance.\n\n• Millions of easy tea & grocery transactions overwhelm the network during training.\n\n• It ends up missing up to 29% of real fraud attacks."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: OUR CORE IDEA: FOCAL LOSS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Our Solution: Focal Loss (Making AI Focus on Mistakes)", slide_num="05")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Simple Student Analogy", C_BLUE)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• When students prepare for exams, they don't waste hours re-reading chapter 1 that they already know 100%.\n\n• Good students spend their time practicing the hard problems they keep getting wrong!\n\n• Normal AI does the opposite: it spends all its time checking obvious coffee and grocery payments.\n\n• Our idea: Use Focal Loss to tell the AI: 'Ignore the easy stuff, spend your energy learning the tricky fraud patterns!'"
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "How the Math Helps (In Simple Words)", C_EMERALD)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• The Focal Loss Formula:\n  Loss = -(1 - p)^γ * log(p)\n\n• For an Easy Transaction (p = 0.99):\n  (1 - 0.99)^2 = 0.0001\n  The AI cuts the penalty by 99.99%! It basically ignores it.\n\n• For a Hard / Suspicious Transaction (p = 0.30):\n  (1 - 0.30)^2 = 0.49\n  The AI pays full attention to learn from its mistake!\n\n• Big Benefit: No fake data needed. The AI learns directly from real data."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 6: EXPLAINABLE AI (XAI)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Giving Plain-English Reasons (Explainable AI)", slide_num="06")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Why Numbers Alone Don't Work", C_EMERALD)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• If a customer calls bank support, the agent cannot say: 'Sorry, mathematical node 28 had a value of 0.88.'\n\n• That makes no sense to a real person!\n\n• Our Explainable AI module converts internal numbers into 3 simple checks:\n  1. Amount: '8 times higher than cardholder's usual spending.'\n  2. Time: 'Made at 3:15 AM (unusual late-night hour).'\n  3. Device: 'Unrecognized phone or browser.'"
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "A Fair 3-Step Action System", C_BLUE)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Instead of only 'Yes' or 'No', we use 3 smart levels:\n\n  🟢 Green (0% - 30% Risk): APPROVED\n  • Normal grocery/shopping transaction passes instantly.\n\n  🟡 Yellow (31% - 70% Risk): CHALLENGE (OTP)\n  • Unusual purchase? Don't block the card! Just send an SMS OTP to confirm it's really the user.\n\n  🔴 Red (71% - 100% Risk): BLOCKED\n  • Definite unauthorized attack blocked to protect money."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 7: BANK STATEMENT SCANNER
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Scanning Bank Statements Safely (Privacy First)", slide_num="07")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "The Problem With Online Scanners", C_RED)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Most online statement tools ask users to upload PDF statements to cloud websites.\n\n• Bank statements contain home addresses, account balances, salary details, and daily habits.\n\n• Storing statements on cloud servers creates a big privacy risk if the server gets hacked."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Our In-Memory Privacy Solution", C_EMERALD)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Works With Any Bank:\n  Different banks use different headers ('Txn Date', 'Value Dt', 'Dr', 'Debit'). Our code automatically maps 100+ aliases.\n\n• In-Memory Only (Zero Disk Storage):\n  The file is unlocked and scanned directly in RAM. Once the fraud score is calculated, the file is immediately wiped.\n\n• Zero data is saved on our server hard drive."
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: RESULTS & COMPARISON (THE TEST)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Results: How Our Model Performed on Real Data", slide_num="08")

    chart_path = "d:/Fraud Detection/reports/diagrams/MODEL_BENCHMARK_COMPARISON.png"
    if os.path.exists(chart_path):
        s8.shapes.add_picture(chart_path, Inches(0.8), Inches(1.65), width=Inches(7.4))

    add_card(s8, Inches(8.5), Inches(1.65), Inches(4.0), Inches(5.2), "Key Takeaways", C_EMERALD)
    tb = s8.shapes.add_textbox(Inches(8.7), Inches(2.2), Inches(3.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Tested on 56,864 Real Transactions:\n\n1. Logistic Regression Failed:\n  Triggered 1,487 false alarms! Annoyed 1,487 real customers.\n\n2. Standard Neural Network:\n  Missed 29% of real fraud.\n\n3. Fake Data (SMOTE + RF):\n  Only 78% precision due to fake points.\n\n4. Our Focal Loss Model:\n  • 84.4% F1-Score\n  • 86.4% Precision\n  • Only 9 false alarms in total!"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 9: HOW THE COMPLETE SYSTEM WORKS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "How The Whole System Works (User Journey)", slide_num="09")

    uml_path = "d:/Fraud Detection/reports/diagrams/FRAUDSHIELD_UML_ACTIVITY_DIAGRAM.png"
    if os.path.exists(uml_path):
        s9.shapes.add_picture(uml_path, Inches(0.8), Inches(1.65), width=Inches(7.2))

    add_card(s9, Inches(8.3), Inches(1.65), Inches(4.2), Inches(5.2), "The 4 Quick Steps", C_BLUE)
    tb = s9.shapes.add_textbox(Inches(8.5), Inches(2.2), Inches(3.8), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. User Input:\n• User tests a transaction or uploads a bank statement (Web or Mobile).\n\n2. Memory Processing:\n• Python backend reads numbers in RAM; no files saved to disk.\n\n3. Instant AI Check:\n• Neural network runs in 11 milliseconds.\n\n4. Smart Output:\n• Shows colorful risk gauge + plain-English reasons + clear action (Approve / OTP / Block)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE WORK
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion & What We Can Build Next", slide_num="10")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "What We Achieved in This Project", C_EMERALD)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Solved Imbalance Without Fake Data:\n  Focal Loss makes the AI pay attention to rare fraud naturally.\n\n• High Accuracy With Low False Alarms:\n  Caught over 82% of frauds while causing only 9 false alarms across 56,000 checks.\n\n• Made AI Explainable:\n  Gives clear reasons instead of confusing percentage numbers.\n\n• Safe Bank Statement Scanner:\n  Works with any bank file while protecting user privacy."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MAIN

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "What We Can Add in the Future", C_BLUE)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Graph Networks (GNNs):\n• Connect transactions between accounts to catch organized fraud groups who move money across multiple bank accounts.\n\n2. Cross-Bank Learning:\n• Let different banks (SBI, HDFC, ICICI) share fraud knowledge together without having to share personal customer data.\n\nThank you!\nWe are happy to answer any questions."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MAIN

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    saved_path = output_path
    try:
        prs.save(output_path)
        print(f"Successfully generated student presentation at: {output_path}")
    except PermissionError:
        saved_path = output_path.replace(".pptx", "_student.pptx")
        prs.save(saved_path)
        print(f"Note: Saved to student version at: {saved_path}")
        
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        artifact_pptx = os.path.join(artifact_dir, os.path.basename(saved_path))
        shutil.copy(saved_path, artifact_pptx)
        print(f"Copied to artifact directory: {artifact_pptx}")

if __name__ == '__main__':
    build_student_presentation()
