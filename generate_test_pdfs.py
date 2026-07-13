from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename, pages_content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for content in pages_content:
        textobject = c.beginText()
        textobject.setTextOrigin(50, height - 50)
        textobject.setFont("Helvetica", 12)
        
        lines = content.split('\n')
        for line in lines:
            textobject.textLine(line)
            
        c.drawText(textobject)
        c.showPage()
        
    c.save()
    print(f"Created {filename}")

def main():
    # Test PDF 1: 1 page, simple PII
    content1 = [
        "Confidential Document - Internal Use Only",
        "",
        "Employee Profile:",
        "Name: John Smith",
        "Email: john.smith@example.com",
        "Phone: +1-555-123-4567",
        "SSN: 123-45-6789",
        "Date of Birth: 05-12-1980",
        "",
        "End of document."
    ]
    
    # Test PDF 2: 2 pages, complex PII, Indian context
    content2_page1 = [
        "Draft Red Herring Prospectus",
        "",
        "The Promoters of this company are:",
        "1. KUSHAL SUBBAYYA HEGDE",
        "2. Anjali Sharma",
        "",
        "Registered Office:",
        "TechNova Solutions Private Limited",
        "123 Innovation Drive, Mumbai, Maharashtra, India",
        "",
        "Company Details:",
        "PAN: ABCDE1234F",
        "IP Address: 192.168.1.100",
    ]
    
    content2_page2 = [
        "Financial Information",
        "",
        "Payment Details:",
        "Credit Card: 1234-5678-9012-3456 (Valid Luhn)",
        "Credit Card: 4532 1522 9311 0214",
        "",
        "Contact the Lead Manager:",
        "Nuvama Wealth Management Limited",
        "Telephone: +91 22 4009",
        "4400"
    ]
    
    # Test PDF 3: 3 pages, Edge cases and false positive testing
    content3_page1 = [
        "Legal Framework and Definitions",
        "",
        "In this document, capitalized terms have specific meanings.",
        "The Offer comprises a Fresh Issue and an Offer for Sale.",
        "The Board of Directors have approved this.",
        "Bidders must submit their ASBA Forms to the SCSBs.",
        "",
        "We are regulated by SEBI and RBI under the Companies Act."
    ]
    
    content3_page2 = [
        "List of Intermediaries",
        "",
        "Registrar of Companies (ROC)",
        "National Stock Exchange (NSE)",
        "Bombay Stock Exchange (BSE)",
        "",
        "Auditors:",
        "Deloitte Haskins & Sells LLP",
        "Legal Counsel:",
        "Cyril Amarchand Mangaldas"
    ]
    
    content3_page3 = [
        "Additional Contacts",
        "",
        "Some generic text with a date that shouldn't be tagged as DOB: 15-08-1947",
        "Born on: 12/10/1990",
        "DOB: 11-11-1985",
        "",
        "A stray long number that is not a phone or CC: 1234567890123",
        "Another string: 9876543210987654",
        "A proper phone number: (022) 2345-6789",
    ]

    create_pdf("test_simple.pdf", ["\n".join(content1)])
    create_pdf("test_indian_context.pdf", ["\n".join(content2_page1), "\n".join(content2_page2)])
    create_pdf("test_edge_cases.pdf", ["\n".join(content3_page1), "\n".join(content3_page2), "\n".join(content3_page3)])

if __name__ == "__main__":
    main()
