import os
import shutil
import urllib.parse
import zlib
import base64

def generate_drawio_diagram():
    # Complete, fully styled Draw.io (mxGraph) XML Model
    drawio_xml = """<mxfile host="app.diagrams.net" modified="2026-11-21T23:25:00.000Z" agent="FraudShield" version="24.0.0" type="device">
  <diagram name="FraudShield System Workflow" id="fraudshield-flow">
    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="720" background="#FFFFFF" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- TITLE BANNER -->
        <mxCell id="title" value="&lt;b style='font-size: 20px;'&gt;FRAUDSHIELD: REAL-TIME PAYMENT FRAUD &amp;amp; ANOMALY DETECTION&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 13px; color: #64748B;'&gt;End-to-End System Workflow: User Ingestion, In-Memory RAM Gateway, PyTorch Focal DNN, and Tri-Tier XAI Actions&lt;/span&gt;" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;" vertex="1" parent="1">
          <mxGeometry x="150" y="20" width="900" height="50" as="geometry" />
        </mxCell>

        <!-- STAGE 1: USER INPUT -->
        <mxCell id="col1_header" value="&lt;b&gt;STEP 1: USER INPUT&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 11px;'&gt;Web &amp;amp; Mobile Interfaces&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#3B82F6;strokeWidth=2;fontColor=#1E40AF;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="40" y="90" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="box_1a" value="&lt;b style='font-size: 13px;'&gt;Live Payment Simulator&lt;/b&gt;&lt;hr style='border: 0.5px solid #93C5FD;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• Transaction Amount (₹)&lt;br&gt;• Merchant &amp;amp; Spending Category&lt;br&gt;• Off-Peak / Midnight Window&lt;br&gt;• Trusted Device Fingerprint&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#93C5FD;strokeWidth=1.5;fontColor=#1E3A8A;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="160" width="240" height="110" as="geometry" />
        </mxCell>

        <mxCell id="box_1b" value="&lt;b style='font-size: 13px;'&gt;Bank Statement Vault&lt;/b&gt;&lt;hr style='border: 0.5px solid #93C5FD;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• Monthly Statement (PDF / Excel)&lt;br&gt;• Password Protected / PIN Locked&lt;br&gt;• Any Bank Supported (SBI, HDFC, ICICI, Axis, Kotak Mahindra)&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#93C5FD;strokeWidth=1.5;fontColor=#1E3A8A;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="300" width="240" height="110" as="geometry" />
        </mxCell>

        <!-- STAGE 2: FASTAPI GATEWAY -->
        <mxCell id="col2_header" value="&lt;b&gt;STEP 2: FASTAPI GATEWAY&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 11px;'&gt;Security &amp;amp; Privacy Layer&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;strokeWidth=2;fontColor=#92400E;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="330" y="90" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="box_2a" value="&lt;b style='font-size: 13px;'&gt;In-Memory RAM Decryption&lt;/b&gt;&lt;hr style='border: 0.5px solid #FCD34D;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• Zero-Disk Storage (100% in RAM)&lt;br&gt;• Decrypted using msoffcrypto &amp;amp; pypdf&lt;br&gt;• Never saved to server hard disk&lt;br&gt;• Complete customer privacy&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FCD34D;strokeWidth=1.5;fontColor=#78350F;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="330" y="160" width="240" height="110" as="geometry" />
        </mxCell>

        <mxCell id="box_2b" value="&lt;b style='font-size: 13px;'&gt;Data Normalization Engine&lt;/b&gt;&lt;hr style='border: 0.5px solid #FCD34D;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• Fuzzy Header Scanner (100+ aliases)&lt;br&gt;• Filters disclaimers &amp;amp; branch metadata&lt;br&gt;• StandardScaler normalizes amount into 29 continuous feature inputs&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FCD34D;strokeWidth=1.5;fontColor=#78350F;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="330" y="300" width="240" height="110" as="geometry" />
        </mxCell>

        <!-- STAGE 3: PYTORCH FOCAL DNN -->
        <mxCell id="col3_header" value="&lt;b&gt;STEP 3: AI MODEL CORE&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 11px;'&gt;PyTorch Focal Neural Net&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#D1FAE5;strokeColor=#059669;strokeWidth=2;fontColor=#065F46;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="620" y="90" width="240" height="50" as="geometry" />
        </mxCell>

        <mxCell id="box_3a" value="&lt;b style='font-size: 13px;'&gt;Focal Loss Architecture&lt;/b&gt;&lt;hr style='border: 0.5px solid #6EE7B7;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• 29 Inputs (V1–V28 + Scaled Amount)&lt;br&gt;• 2 Dense Layers (64 → 32 nodes)&lt;br&gt;• Loss: FL(pt) = -(1 - pt)^γ * log(pt)&lt;br&gt;• γ = 2.0 ignores easy coffee purchases; forces AI to focus on rare fraud!&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#6EE7B7;strokeWidth=1.5;fontColor=#047857;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="620" y="160" width="240" height="115" as="geometry" />
        </mxCell>

        <mxCell id="box_3b" value="&lt;b style='font-size: 13px;'&gt;Real-Time Execution&lt;/b&gt;&lt;hr style='border: 0.5px solid #6EE7B7;'&gt;&lt;div style='text-align: left; font-size: 11px;'&gt;• Forward pass executes in &lt;b&gt;11.85 ms&lt;/b&gt;&lt;br&gt;• Well under 100ms gateway limits&lt;br&gt;• Calculates continuous fraud risk probability: &lt;b&gt;p ∈ [0.0, 1.0]&lt;/b&gt;&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#6EE7B7;strokeWidth=1.5;fontColor=#047857;align=center;verticalAlign=top;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="620" y="300" width="240" height="105" as="geometry" />
        </mxCell>

        <!-- STAGE 4: ACTION & EXPLAINABLE AI -->
        <mxCell id="col4_header" value="&lt;b&gt;STEP 4: SMART ACTION &amp;amp; XAI&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 11px;'&gt;Proportional Interventions&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#7C3AED;strokeWidth=2;fontColor=#5B21B6;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="910" y="90" width="250" height="50" as="geometry" />
        </mxCell>

        <!-- Tier 1: Approved -->
        <mxCell id="box_4a" value="&lt;b style='color: #065F46; font-size: 12px;'&gt;🟢 APPROVED (Risk &amp;lt; 30%)&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 10.5px; color: #047857;'&gt;Legitimate purchase cleared instantly without customer delay.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#10B981;strokeWidth=1.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="910" y="160" width="250" height="50" as="geometry" />
        </mxCell>

        <!-- Tier 2: Challenge -->
        <mxCell id="box_4b" value="&lt;b style='color: #92400E; font-size: 12px;'&gt;🟡 CHALLENGE (Risk 31% – 70%)&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 10.5px; color: #78350F;'&gt;Suspicious spend? Send SMS OTP instead of freezing card by mistake!&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#F59E0B;strokeWidth=1.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="910" y="225" width="250" height="55" as="geometry" />
        </mxCell>

        <!-- Tier 3: Blocked -->
        <mxCell id="box_4c" value="&lt;b style='color: #991B1B; font-size: 12px;'&gt;🔴 BLOCKED (Risk &amp;gt; 70%)&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 10.5px; color: #B91C1C;'&gt;Definite unauthorized attack blocked; card protected immediately.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF2F2;strokeColor=#EF4444;strokeWidth=1.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="910" y="295" width="250" height="50" as="geometry" />
        </mxCell>

        <!-- XAI Box -->
        <mxCell id="box_4d" value="&lt;b style='font-size: 12px; color: #1E293B;'&gt;📝 Explainable AI (XAI) Reasons&lt;/b&gt;&lt;hr style='border: 0.5px solid #CBD5E1;'&gt;&lt;div style='text-align: left; font-size: 10.5px; color: #334155;'&gt;Plain-English reasons for user &amp;amp; bank:&lt;br&gt;• &lt;i&gt;&quot;Amount is 8.4x higher than usual norm.&quot;&lt;/i&gt;&lt;br&gt;• &lt;i&gt;&quot;Made at 3:15 AM (unusual night time).&quot;&lt;/i&gt;&lt;br&gt;• &lt;i&gt;&quot;Unrecognized phone / browser device.&quot;&lt;/i&gt;&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1.5;align=center;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="910" y="360" width="250" height="95" as="geometry" />
        </mxCell>

        <!-- CONNECTING ARROWS -->
        <mxCell id="e1" edge="1" parent="1" source="box_1a" target="box_2a" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="box_1b" target="box_2a" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" edge="1" parent="1" source="box_2a" target="box_2b" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" edge="1" parent="1" source="box_2b" target="box_3a" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#D97706;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" edge="1" parent="1" source="box_3a" target="box_3b" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e6" edge="1" parent="1" source="box_3b" target="box_4a" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e7" edge="1" parent="1" source="box_3b" target="box_4b" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e8" edge="1" parent="1" source="box_3b" target="box_4c" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e9" edge="1" parent="1" source="box_4b" target="box_4d" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.5;dashed=1;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e10" edge="1" parent="1" source="box_4c" target="box_4d" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7C3AED;strokeWidth=1.5;dashed=1;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- FOOTER BADGE -->
        <mxCell id="footer" value="&lt;span style='font-size: 11px; color: #64748B;'&gt;FraudShield System Architecture • 3rd Year B.Tech CSE Capstone Project • UEM Kolkata&lt;/span&gt;" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;" vertex="1" parent="1">
          <mxGeometry x="350" y="480" width="500" height="30" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    # Save to file
    out_dir = "d:/Fraud Detection/reports/diagrams"
    os.makedirs(out_dir, exist_ok=True)
    drawio_path = os.path.join(out_dir, "FRAUDSHIELD_WORKFLOW.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_xml)
    print(f"Saved .drawio file to: {drawio_path}")

    # Copy to docs/ and artifact dir
    docs_drawio = "d:/Fraud Detection/docs/FRAUDSHIELD_WORKFLOW.drawio"
    shutil.copy(drawio_path, docs_drawio)
    
    artifact_dir = "C:/Users/praks/.gemini/antigravity/brain/32d0474b-b616-4722-999c-c63d973b6dfe"
    if os.path.exists(artifact_dir):
        shutil.copy(drawio_path, os.path.join(artifact_dir, "FRAUDSHIELD_WORKFLOW.drawio"))

    # Generate 1-Click draw.io Web Link
    # Draw.io URL schema: https://app.diagrams.net/#R<base64(raw_deflate(url_quote(xml)))>
    quoted_xml = urllib.parse.quote(drawio_xml, safe='')
    compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    deflated = compressor.compress(quoted_xml.encode('utf-8')) + compressor.flush()
    encoded = base64.b64encode(deflated).decode('utf-8')
    drawio_url = f"https://app.diagrams.net/#R{encoded}"
    
    # Save direct link into a helper HTML/markdown file
    link_md_path = "d:/Fraud Detection/docs/OPEN_IN_DIAGRAMS_NET.md"
    with open(link_md_path, "w", encoding="utf-8") as f:
        f.write(f"# 🔗 Open FraudShield Workflow in diagrams.net (Draw.io)\n\n"
                f"Click the link below to open and edit your exact workflow diagram directly in `app.diagrams.net` with 1 click:\n\n"
                f"👉 **[Click Here to Open in app.diagrams.net]({drawio_url})**\n\n"
                f"### Or open the local file:\n"
                f"1. Go to [https://app.diagrams.net/](https://app.diagrams.net/)\n"
                f"2. Click **File -> Open From -> Device**\n"
                f"3. Select `{drawio_path}`\n")
    print(f"Direct URL length: {len(drawio_url)}")
    return drawio_path, drawio_url

if __name__ == '__main__':
    generate_drawio_diagram()
