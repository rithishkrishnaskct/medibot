"""
Script to create sample medical PDF documents for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_sample_medical_pdf():
    """Create a sample medical PDF with drug information"""
    
    # Ensure pdfs directory exists
    os.makedirs("pdfs", exist_ok=True)
    
    # Create PDF
    doc = SimpleDocTemplate("pdfs/sample_drug_info.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
    )
    
    # Content
    content = []
    
    # Title
    content.append(Paragraph("ADALIMUMAB (HUMIRA®) - Prescribing Information", title_style))
    content.append(Spacer(1, 12))
    
    # Description
    content.append(Paragraph("DESCRIPTION", heading_style))
    content.append(Paragraph(
        "HUMIRA® (adalimumab) is a recombinant human IgG1 monoclonal antibody specific for human tumor necrosis factor (TNF). "
        "Adalimumab is produced by recombinant DNA technology in a mammalian cell expression system and is purified by a process "
        "that includes specific viral inactivation and removal steps.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Indications
    content.append(Paragraph("INDICATIONS AND USAGE", heading_style))
    content.append(Paragraph(
        "HUMIRA is indicated for the treatment of adults with moderately to severely active rheumatoid arthritis. "
        "HUMIRA can be used alone or in combination with methotrexate or other non-biologic disease-modifying antirheumatic drugs (DMARDs).",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Dosage
    content.append(Paragraph("DOSAGE AND ADMINISTRATION", heading_style))
    content.append(Paragraph(
        "The recommended dose of HUMIRA for adult patients with rheumatoid arthritis is 40 mg administered every other week "
        "by subcutaneous injection. Methotrexate should be continued during treatment with HUMIRA.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Contraindications
    content.append(Paragraph("CONTRAINDICATIONS", heading_style))
    content.append(Paragraph(
        "HUMIRA is contraindicated in patients with known hypersensitivity to adalimumab or any of its components. "
        "HUMIRA should not be given concurrently with live vaccines. HUMIRA is contraindicated in patients with an active infection.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Warnings
    content.append(Paragraph("WARNINGS AND PRECAUTIONS", heading_style))
    content.append(Paragraph(
        "Increased risk of serious infections that may lead to hospitalization or death. Most patients who developed these "
        "infections were taking concomitant immunosuppressants such as methotrexate or corticosteroids. "
        "Lymphoma and other malignancies have been reported in patients treated with TNF blockers.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Adverse Reactions
    content.append(Paragraph("ADVERSE REACTIONS", heading_style))
    content.append(Paragraph(
        "The most common adverse reactions (≥10%) in HUMIRA clinical trials were: injection site reactions, "
        "upper respiratory infections, headache, and rash. Serious adverse reactions include serious infections, "
        "neurological events, and hematological events.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Drug Interactions
    content.append(Paragraph("DRUG INTERACTIONS", heading_style))
    content.append(Paragraph(
        "Live vaccines should not be given concurrently with HUMIRA. No data are available on the secondary transmission "
        "of infection by live vaccines in patients receiving HUMIRA. Concomitant use of HUMIRA with other biologic DMARDs "
        "or targeted synthetic DMARDs is not recommended.",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(content)
    print("Sample medical PDF created: pdfs/sample_drug_info.pdf")

def create_second_sample_pdf():
    """Create another sample medical PDF"""
    
    doc = SimpleDocTemplate("pdfs/medication_safety_guide.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
    )
    
    content = []
    
    # Title
    content.append(Paragraph("MEDICATION SAFETY GUIDE - BIOLOGICS", title_style))
    content.append(Spacer(1, 12))
    
    # General Safety
    content.append(Paragraph("GENERAL SAFETY INFORMATION", heading_style))
    content.append(Paragraph(
        "Biologic medications require special handling and administration. Patients should be monitored regularly "
        "for signs of infection, changes in blood counts, and liver function. All patients should receive appropriate "
        "vaccinations before starting biologic therapy.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Storage
    content.append(Paragraph("STORAGE AND HANDLING", heading_style))
    content.append(Paragraph(
        "Store in refrigerator at 36°F to 46°F (2°C to 8°C). Do not freeze or shake. "
        "Protect from light. Allow to reach room temperature before injection. "
        "Use within 14 days if stored at room temperature.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Administration
    content.append(Paragraph("ADMINISTRATION GUIDELINES", heading_style))
    content.append(Paragraph(
        "Rotate injection sites (thigh, abdomen, upper arm). Clean injection site with alcohol. "
        "Inject subcutaneously at 45-90 degree angle. Do not inject into areas where skin is tender, "
        "bruised, red, or hard.",
        styles['Normal']
    ))
    content.append(Spacer(1, 12))
    
    # Monitoring
    content.append(Paragraph("PATIENT MONITORING", heading_style))
    content.append(Paragraph(
        "Regular blood tests are required to monitor: Complete blood count (CBC), liver function tests, "
        "and signs of infection. Patients should report fever, flu-like symptoms, or unusual fatigue immediately. "
        "Annual tuberculosis screening is recommended.",
        styles['Normal']
    ))
    
    doc.build(content)
    print("Second sample medical PDF created: pdfs/medication_safety_guide.pdf")

if __name__ == "__main__":
    try:
        create_sample_medical_pdf()
        create_second_sample_pdf()
        print("Sample PDFs created successfully!")
    except ImportError:
        print("reportlab not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        create_sample_medical_pdf()
        create_second_sample_pdf()
        print("Sample PDFs created successfully!")
    except Exception as e:
        print(f"Error creating sample PDFs: {e}")
        print("You can manually add PDF files to the pdfs/ directory instead.")