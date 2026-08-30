import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import sqlite3

def get_module_names():
    """Extract module names from database.py"""
    # Since we can't directly import database.py without running it, we'll parse the file
    # Alternatively, we can connect to the database and query the modules table
    # Let's do the database approach for robustness

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM modules")
    modules = cursor.fetchall()
    conn.close()
    return [module[0] for module in modules]

def create_pdf_for_module(module_name, output_dir):
    """Create a PDF summary for a given module"""
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the PDF file path
    safe_module_name = module_name.replace("/", "-").replace("\\", "-")
    pdf_path = os.path.join(output_dir, f"resume - {safe_module_name}.pdf")

    # Create the PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    story.append(Paragraph(f"Resume - {module_name}", title_style))
    story.append(Spacer(1, 20))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 12))
    exec_summary = f"""
    This document provides a comprehensive summary of the {module_name} module.
    It covers the essential concepts, key learning objectives, and practical applications
    that students need to master in this subject area. The summary is designed to serve
    as a quick reference guide for review and study purposes.
    """
    story.append(Paragraph(exec_summary.strip(), styles['Normal']))
    story.append(Spacer(1, 20))

    # Key Concepts
    story.append(Paragraph("Key Concepts", styles['Heading2']))
    story.append(Spacer(1, 12))
    key_concepts = [
        f"Fundamental principles of {module_name}",
        f"Core theories and models in {module_name}",
        f"Key terminology and definitions",
        f"Important formulas and calculations (where applicable)",
        f"Critical thinking approaches specific to {module_name}"
    ]
    for concept in key_concepts:
        story.append(Paragraph(f"• {concept}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Practical Applications
    story.append(Paragraph("Practical Applications", styles['Heading2']))
    story.append(Spacer(1, 12))
    practical_apps = f"""
    The {module_name} module emphasizes real-world applications that prepare students
    for professional practice. Through case studies, simulations, and hands-on projects,
    learners develop the ability to apply theoretical knowledge to solve practical problems
    encountered in the field. Key application areas include:
    """
    story.append(Paragraph(practical_apps.strip(), styles['Normal']))
    story.append(Spacer(1, 12))

    apps_list = [
        f"Industry-standard practices in {module_name}",
        f"Problem-solving scenarios relevant to {module_name}",
        f"Tools and technologies used in {module_name} profession",
        f"Ethical considerations and best practices",
        f"Integration with related disciplines"
    ]
    for app in apps_list:
        story.append(Paragraph(f"• {app}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Visual Diagrams (Placeholder)
    story.append(Paragraph("Visual Diagrams", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Note: Visual diagrams would be included here in the final version.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Create a simple placeholder diagram (a rectangle with text)
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics import renderPDF

    drawing = Drawing(400, 200)
    rect = Rect(0, 0, 400, 200)
    rect.fillColor = colors.lightgrey
    rect.strokeColor = colors.black
    rect.strokeWidth = 1
    drawing.add(rect)

    label = String(200, 100, f"Diagram Placeholder\n{module_name}", textAnchor='middle')
    label.fontSize = 14
    label.fillColor = colors.darkblue
    drawing.add(label)

    story.append(drawing)
    story.append(Spacer(1, 30))

    # Build the PDF
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

def main():
    """Main function to generate PDFs for all modules"""
    # Get module names from database
    module_names = get_module_names()
    print(f"Found {len(module_names)} modules: {module_names}")

    # Define output directory
    output_dir = "2_Resumes_Modules"

    # Generate PDF for each module
    for module_name in module_names:
        create_pdf_for_module(module_name, output_dir)

    print(f"\nAll PDFs generated in '{output_dir}' directory.")

if __name__ == "__main__":
    main()