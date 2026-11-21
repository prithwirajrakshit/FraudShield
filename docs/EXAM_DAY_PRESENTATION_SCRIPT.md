# 🎓 Student Presentation Notes & Viva Cheat Sheet
### Simple, Easy-to-Explain Script for 3rd Year B.Tech Defense
**Project Name**: FraudShield: Smart Payment Fraud Detection  
**File**: `docs/FRAUDSHIELD_FINAL_EXAM_PRESENTATION_student.pptx` (Exact 10 Slides)

---

## 💡 How to Speak on Exam Day
- Speak simply and naturally. Do not sound like you memorized a textbook.
- Keep each slide to **30–45 seconds**.
- Whenever examiners ask a question, answer in 1 or 2 clear sentences.

---

## 📑 Slide-by-Slide Speaking Script

### 🟢 Slide 1: Title Slide (Introduction)
- **What to Say**:
  > *"Good morning respected sir/ma'am. We are 3rd-year Computer Science students from UEM Kolkata. Today, we are presenting our project: **FraudShield - Smart Payment Fraud Detection**. Our goal was to build a system that catches real credit card fraud fast, without blocking genuine customers by mistake."*

---

### 🟢 Slide 2: Why We Chose This Project (The Problem)
- **What to Say**:
  > *"When banks use machine learning for fraud, they face three major headaches:*
  > 1. ***The 99% Accuracy Trap***: *In real credit card data, 99.8% of payments are normal and only 0.2% are fraud. If an AI model just marks everything as 'Normal', it gets a 99.8% accuracy score on paper, but in reality, it caught zero frauds!*
  > 2. ***False Alarms***: *Basic models try to catch fraud by blocking too many transactions. Real customers get their cards declined at stores or airports, which is very embarrassing and frustrating.*
  > 3. ***The Black Box Problem***: *Normal models just say '87% Risk', but cannot explain WHY the payment was blocked."*

---

### 🟢 Slide 3: What We Built (Our 4 Goals)
- **What to Say**:
  > *"To solve these 3 problems, our team built 4 things:*
  > - ***1. Smarter Model***: *We used 'Focal Loss' so the AI focuses on rare fraud cases instead of getting lazy on normal ones.*
  > - ***2. Plain-English Reasons***: *Instead of showing a random percentage, the system tells the user the exact reason (like high amount or late-night purchase).*
  > - ***3. Bank Statement Scanner***: *A tool to upload and scan full monthly PDF or Excel statements safely.*
  > - ***4. Working Demo***: *A fast backend running in 11 milliseconds, a web dashboard, and a mobile app."*

---

### 🟢 Slide 4: Why Old Methods Don't Work Well
- **What to Say**:
  > *"Before building our model, we checked why standard solutions fail:*
  > - ***Rule Systems Fail***: *Simple rules like 'block if amount is above ₹50,000' are too rigid. Fraudsters just make smaller transfers like ₹5,000 to bypass them.*
  > - ***SMOTE (Fake Data) Fails***: *Generating fake fraud data points confuses the AI because fake points overlap with normal purchases, creating lots of false alarms.*
  > - ***Standard Neural Networks Fail***: *Because 99% of training examples are easy grocery purchases, the neural network only learns to predict normal payments."*

---

### 🟢 Slide 5: Our Core Idea: Focal Loss (Focus on Mistakes)
- **What to Say**:
  > *"Here is the main idea of our project: Think of how we students study for exams. We don't spend hours re-reading chapter 1 that we already know 100%. We spend our time practicing the hard questions we keep getting wrong!*  
  > *Focal Loss does the exact same thing for AI:*
  > - *If a transaction is obviously normal, the loss penalty is reduced by **99.9%**. The AI ignores it.*
  > - *If a transaction is suspicious or tricky, the AI gets the full penalty and pays complete attention to learn from its mistake!*  
  > *This way, we don't need any fake data. The AI learns directly from real data."*
- **If the Guide asks**: *"What is the gamma ($\gamma$) parameter?"*
  - **Your Answer**: *"Sir, gamma controls how much to ignore the easy cases. We set it to 2, which reduces the penalty on easy normal transactions so the model focuses strictly on fraud."*

---

### 🟢 Slide 6: Making the AI Explain Itself (Explainable AI)
- **What to Say**:
  > *"Next, we made the system explain its decisions in simple words. If a transaction is flagged, our system shows 3 simple points:*
  > 1. *'Amount is 8 times higher than your normal spending.'*
  > 2. *'Made at 3:15 AM (unusual late-night hour).'*
  > 3. *'Unrecognized device or phone.'*  
  > *We also use a fair 3-level system: Safe payments are approved instantly; suspicious payments trigger an SMS OTP challenge instead of immediately freezing the card; only high-risk attacks are blocked."*

---

### 🟢 Slide 7: Bank Statement Scanner (Privacy First)
- **What to Say**:
  > *"We also built a Bank Statement Scanner. Most online PDF tools make you upload files to their cloud servers, which exposes your private bank balance and salary details.*  
  > *In our system:*
  > - *It automatically detects columns across any bank like SBI, HDFC, or ICICI (mapping 'Txn Date', 'Dr', 'Debit', etc.).*
  > - *Everything runs in computer memory (RAM). Once the scan finishes, the file is immediately deleted.*
  > - *Nothing is saved on our server hard drive, keeping customer data 100% private."*

---

### 🟢 Slide 8: Results: How Our Model Performed (The Test)
- **What to Say**:
  > *(Point to the bar chart)*  
  > *"We tested our model on 56,864 real European credit card transactions:*
  > - ***Logistic Regression*** *blocked 1,487 innocent users by mistake!*
  > - ***Standard Neural Network*** *missed 29% of real fraud.*
  > - ***Our Focal Loss Model*** *achieved an **84.4% F1-score**, and caused only **9 false alarms** out of 56,000 transactions!*  
  > *This proves our idea worked: tuning the loss function is much better than creating fake data."*

---

### 🟢 Slide 9: How The Whole System Works (Live Flow)
- **What to Say**:
  > *(Point to the flowchart)*  
  > *"Here is how a transaction flows through the system in real life:*
  > 1. *User submits a payment or uploads a statement.*
  > 2. *Our Python backend loads the numbers in RAM.*
  > 3. *The neural network checks the fraud score in just 11 milliseconds.*
  > 4. *The user immediately sees the color gauge (Green, Yellow, or Red) along with the reasons and clear advice."*

---

### 🟢 Slide 10: Conclusion & What's Next
- **What to Say**:
  > *"To conclude, we built a working, fast fraud detection system that catches real fraud without annoying genuine customers.*  
  > *In the future, we want to add **Graph Neural Networks** to detect organized gangs who transfer money across multiple bank accounts, and test with more Indian banks.*  
  > *Thank you sir! We would love to answer your questions."*

---

## 🎯 3 Quick Tips for Exam Day:
1. **Never say 99.9% accuracy is enough** — explain that accuracy is misleading when 99.8% of the data is normal.
2. **Remember the number 9** — our model had only 9 false alarms out of 56,000 transactions, compared to 1,487 in older models.
3. **Be confident and relaxed** — keep your answers short and practical.
