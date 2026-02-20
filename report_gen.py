try:
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
except Exception:
    canvas = None
    colors = None

import os

def generate_forensic_report(case_data: dict, out_path: str):
    """Generate a minimal forensic PDF report (2026-branded).

    case_data should contain at least: id, type, summary
    """
    if canvas is None:
        # reportlab not installed — write a placeholder text file
        with open(out_path.replace('.pdf', '.txt'), 'w') as f:
            f.write(f"SENTIENT SYNC // ACTIVE DEFENSE REPORT 2026\n")
            f.write(f"INCIDENT ID: {case_data.get('id')}\n")
            f.write(f"TYPE: {case_data.get('type')}\n")
            f.write(f"DATE: February 20, 2026\n")
            f.write('\n')
            f.write(case_data.get('summary', 'No summary provided'))
        return out_path.replace('.pdf', '.txt')

    # Create PDF
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    c = canvas.Canvas(out_path, pagesize=(612, 792))

    # Header - 2026 Active Monitoring
    c.setFillColor(colors.black)
    c.rect(0, 750, 612, 50, fill=1)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.green)
    c.drawString(50, 770, "SENTIENT SYNC // ACTIVE DEFENSE REPORT 2026")

    # Body Content
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 720, f"INCIDENT ID: {case_data.get('id')}")
    c.setFont("Helvetica", 9)
    c.drawString(50, 705, f"DATE: February 20, 2026")

    # 2026 Compliance Section
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 670, "REGULATORY FRAMEWORK ALIGNMENT:")
    c.setFont("Helvetica", 9)
    c.drawString(70, 655, f"• NIST CSF 2.0 (2026 Update): [DETECT]")
    c.drawString(70, 640, f"• OWASP AGI/LLM Top 10 (2026): [{case_data.get('type')}]")

    # Summary
    c.setFont("Helvetica", 9)
    text = c.beginText(50, 610)
    text.textLines(case_data.get('summary', 'No summary'))
    c.drawText(text)

    c.showPage()
    c.save()
    return out_path


if __name__ == "__main__":
    sample = {
        'id': 'CASE-20260220-001',
        'type': 'AUTO_FLAGGED',
        'summary': 'This is a sample forensic report generated on Feb 20, 2026.'
    }
    out = generate_forensic_report(sample, 'forensic_reports/sample_report_2026.pdf')
    print(f"Report generated: {out}")
