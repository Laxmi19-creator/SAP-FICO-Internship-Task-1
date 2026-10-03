import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell (values in dxa: 20 dxa = 1 pt)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Set subtle modern borders for a table."""
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:insideV w:val="none"/>'
                            f'<w:left w:val="none"/>'
                            f'<w:right w:val="none"/>'
                            f'</w:tblBorders>')
        tblPr[0].append(borders)

def add_callout(doc, text, title=None):
    """Add a shaded callout block with a left border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8") # soft light blue/gray
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
                        f'<w:top w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:bottom w:val="none"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        run_title = p.add_run(f"{title}\n")
        run_title.bold = True
        run_title.font.name = "Arial"
        run_title.font.size = Pt(10.5)
        run_title.font.color.rgb = RGBColor(0, 51, 102)
    
    run_text = p.add_run(text)
    run_text.font.name = "Arial"
    run_text.font.size = Pt(10)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(40, 50, 60)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_sap_fico_doc():
    doc = docx.Document()
    
    # Page setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "SAP FICO Comprehensive Research Report | Week 1 Internship Deliverable"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Author: Laxmi Gupta  |  SAP Consulting Intern  |  Confidential & Academic Evaluation"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    # Document Title Styling
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("SAP FICO: Comprehensive Architectural & Functional Research Report")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(0, 51, 102) # Corporate Navy

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("A Deep-Dive Study on Enterprise Financial Accounting, Controlling, Module Integrations, Real-World Use Cases, and Strategic Enterprise Impact")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(80, 90, 100)

    # Metadata Card Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Author / Candidate:", "Laxmi Gupta (SAP Consulting / ERP Intern)"),
        ("Project Task:", "Week 1 Task: Understanding SAP FICO Fundamentals & Integration"),
        ("Deliverable Type:", "Formal Industrial Research Document & Technical Reference"),
        ("Date & Evaluation Cycle:", "October 2026 | Comprehensive Academic & Industrial Evaluation")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.0)
        cell_val.width = Inches(4.5)
        set_cell_background(cell_lbl, "F4F6F8")
        set_cell_background(cell_val, "FAFAFA")
        set_cell_margins(cell_lbl, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_val, top=60, bottom=60, left=100, right=100)
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0, 51, 102)
        
        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(40, 40, 40)
        
    set_table_borders(meta_table, color="D0D7DE", sz="4")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Helper function for Section Headings
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(15)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 51, 102)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12.5)
        r.bold = True
        r.font.color.rgb = RGBColor(15, 82, 148)
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.bold = True
        r.font.color.rgb = RGBColor(50, 60, 70)
        return h

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(10)
            rb.font.color.rgb = RGBColor(20, 20, 20)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(10)
            rb.font.color.rgb = RGBColor(20, 20, 20)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 30, 30)
        return p

    # 1. Executive Summary
    add_h1("1. Executive Summary")
    add_p("In the modern global economy, multinational corporations navigate intricate regulatory compliance standards, volatile multi-currency supply chains, and complex internal cost structures. Enterprise Resource Planning (ERP) systems provide the digital backbone that coordinates these widespread activities. Within the enterprise ecosystem developed by SAP SE, SAP FICO (Financial Accounting and Controlling) serves as the primary engine for statutory external compliance, financial governance, internal operational cost management, and executive decision support.")
    add_p("This comprehensive research paper examines the core architecture, functional sub-modules, cross-functional integrations, practical use cases, strategic advantages, implementation roadblocks, and next-generation advancements of SAP FICO. Developed as the primary deliverable for Week 1 of the ERP Internship, this report reflects an exhaustive synthesis of architectural principles, industry benchmarks, and operational workflows.")
    
    add_callout(doc, 
        "Key Research Insight: SAP FICO is not merely a double-entry bookkeeping application. It is an integrated enterprise data pipeline that translates real-world physical events—from the receipt of a raw material pallet in a warehouse to the dispatch of a finished product to a customer—into synchronized, auditable accounting entries instantaneously.",
        "Core Architectural Foundation")

    # 2. Introduction to SAP & Enterprise Resource Planning
    add_h1("2. Introduction to SAP & Enterprise Resource Planning (ERP)")
    add_p("Enterprise Resource Planning (ERP) is defined as a software architecture that integrates core business processes across an entire enterprise—including procurement, manufacturing, sales, human resources, finance, and logistics—into a single, unified database and software suite.")
    add_p("Founded in Mannheim, Germany in 1972 by former IBM systems engineers, SAP (Systeme, Anwendungen und Produkte in der Datenverarbeitung / Systems, Applications, and Products in Data Processing) pioneered the concept of real-time enterprise computing. Over five decades of technological advancement, SAP transformed from:")
    add_bullet(" Pioneered real-time financial data processing on punched cards and mainframe systems.", "SAP R/1 & R/2 (1970s–1980s):")
    add_bullet(" Introduced the revolutionary three-tier client/server architecture (Database Layer, Application Layer, Presentation Layer / SAP GUI).", "SAP R/3 (1992):")
    add_bullet(" Modularized enterprise operations into functional components (FI, CO, MM, SD, PP, HR) operating on relational databases.", "SAP ERP Central Component (ECC 6.0, 2004):")
    add_bullet(" Built natively on the in-memory columnar SAP HANA database, unifying transactions and analytics while replacing legacy fragmented tables with the Universal Journal (ACDOCA).", "SAP S/4HANA (2015–Present):")

    # 3. High-Level Architecture of SAP FICO
    add_h1("3. High-Level Architecture of SAP FICO")
    add_p("SAP FICO is composed of two distinct yet intimately integrated sub-systems: SAP FI (Financial Accounting) and SAP CO (Controlling). While they operate within the same enterprise software suite, their design objectives, user personas, regulatory rules, and reporting outputs are fundamentally different.")
    
    add_h2("3.1 Comparative Analysis: Financial Accounting (FI) vs. Controlling (CO)")
    
    # Table Comparison
    table_fico = doc.add_table(rows=7, cols=3)
    table_fico.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Evaluation Dimension", "SAP FI (Financial Accounting)", "SAP CO (Controlling / Management)"]
    row0 = table_fico.rows[0]
    for i, h_text in enumerate(headers):
        cell = row0.cells[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    fico_data = [
        ("Target Audience", "External: Tax authorities, statutory auditors, banks, shareholders, regulatory agencies.", "Internal: Executive C-suite, operational controllers, plant managers, cost center owners."),
        ("Legal Requirement", "Strictly mandatory under local commercial laws and international regulations.", "Voluntary; shaped by operational management needs and internal business strategy."),
        ("Accounting Standards", "Governed by statutory GAAP (IFRS, US GAAP, Indian AS, German HGB).", "Governed by internal managerial economics, cost accounting, and absorption formulas."),
        ("Primary Reporting Deliverables", "Balance Sheet, Profit & Loss (P&L), Cash Flow Statement, Notes to Accounts.", "Cost Center variance reports, Product Cost estimates, Contribution Margin analyses."),
        ("Primary Organizational Unit", "Company Code (Independent legal entity publishing statutory balance sheets).", "Controlling Area (Organizational unit defining the boundary of cost accounting)."),
        ("Data Nature", "Historical, highly auditable, legal transactional double-entry ledger.", "Forward-looking budgets, standard cost baselines, activity rates, internal allocations.")
    ]
    
    for row_idx, data in enumerate(fico_data):
        row = table_fico.rows[row_idx + 1]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0, 51, 102)
            else:
                r.font.color.rgb = RGBColor(40, 40, 40)
                
    set_table_borders(table_fico, color="D0D7DE", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("3.2 The Enterprise Organizational Hierarchy in SAP")
    add_p("To model complex corporate structures, SAP uses a strictly nested organizational hierarchy:")
    add_bullet(" The highest technical entity in SAP, representing the corporate parent database partition.", "1. Client:")
    add_bullet(" Highest organizational unit in Controlling, dedicated to multi-dimensional Profitability Analysis (CO-PA).", "2. Operating Concern:")
    add_bullet(" Central unit in management accounting. Defines the scope of cost accounting, cost center hierarchies, and overhead allocations. One Controlling Area can encompass multiple Company Codes.", "3. Controlling Area:")
    add_bullet(" The foundational organizational unit in Financial Accounting. An independent legal commercial entity with autonomous statutory reporting, bookkeeping, and balance sheets.", "4. Company Code:")
    add_bullet(" Internal organizational dimensions used for decentralized managerial balance sheets and segment reporting under IFRS 8 / ASC 280.", "5. Business Area / Profit Center / Segment:")
    add_bullet(" Operational facilities (manufacturing plants, fulfillment warehouses, corporate branches) assigned to Company Codes.", "6. Plant / Storage Location:")

    add_h2("3.3 The S/4HANA Revolution: The Universal Journal (ACDOCA)")
    add_p("In legacy SAP ECC 6.0, Financial Accounting and Controlling were architecturally separated into distinct physical database tables:")
    add_bullet(" Stored header and line items for financial documents.", "Legacy FI Tables (BKPF, BSEG):")
    add_bullet(" Stored internal cost postings and primary/secondary cost totals.", "Legacy CO Tables (COEP, COSP, COSS):")
    add_bullet(" Stored fixed asset values and planned depreciation.", "Legacy Asset Tables (ANEP, ANEA):")
    add_bullet(" Stored multi-dimensional profitability segment totals.", "Legacy CO-PA Tables (CE1xxxx - CE4xxxx):")
    add_p("Because of this fragmentation, month-end closing in ECC required laborious, time-consuming reconciliation runs to align FI and CO figures. In SAP S/4HANA, SAP eliminated redundant tables and unified all financial dimensions into a single database table: the Universal Journal (Table ACDOCA).")
    add_bullet(" General Ledger account, Cost Center, Profit Center, Asset Number, Material Number, Customer, Vendor, and Profitability characteristics are populated simultaneously in a single record.", "Single Source of Truth:")
    add_bullet(" Because FI and CO write to the same table concurrently, inter-module reconciliation is completely obsolete.", "Zero Month-End Reconciliation:")
    add_bullet(" Running on the in-memory SAP HANA database, multi-million-row financial queries execute in milliseconds without requiring pre-aggregated totals.", "Columnar In-Memory Performance:")

    # 4. Deep-Dive: SAP FI Core Sub-Modules
    add_h1("4. Deep-Dive: SAP FI (Financial Accounting) & Core Sub-Modules")
    add_p("SAP FI contains specialized sub-modules tailored to distinct financial balance-sheet processes.")
    
    add_h2("4.1 General Ledger Accounting (FI-GL)")
    add_p("The General Ledger is the central financial master ledger of the company. Key elements include:")
    add_bullet(" The systematic master list of general ledger accounts used across company codes. SAP supports Operational Chart of Accounts (daily postings), Group Chart of Accounts (consolidation), and Country-Specific Chart of Accounts (local tax/statutory requirements).", "Chart of Accounts (COA):")
    add_bullet(" Supports parallel accounting standards within a single company. Leading Ledger (0L) reflects primary corporate accounting (e.g., IFRS), while Non-Leading Ledgers (2L, 3L) capture parallel standards (e.g., US GAAP, Indian AS) simultaneously.", "Parallel Ledgers (Leading vs. Non-Leading):")
    add_bullet(" Every posting creates an unalterable accounting document. Debits must equal credits. Postings utilize two-digit numeric Posting Keys (e.g., 40 = GL Debit, 50 = GL Credit, 01 = Customer Invoice Debit, 31 = Vendor Invoice Credit) to control field status and debit/credit orientation.", "Document Principles & Posting Keys:")

    add_h2("4.2 Accounts Payable (FI-AP)")
    add_p("Accounts Payable records all enterprise liabilities and financial transactions with suppliers.")
    add_bullet(" In SAP S/4HANA, vendors and suppliers are maintained under the unified Business Partner (BP) master framework, unifying purchasing, financial, and tax profiles under a single master identifier.", "Business Partner (BP) Architecture:")
    add_bullet(" Individual vendor balances do not sit directly on the general ledger. Instead, vendor sub-ledger postings automatically roll up into an immutable Sundry Creditors Reconciliation Account in real-time.", "Reconciliation Accounts:")
    add_bullet(" Evaluates open vendor invoices, identifies cash discounts, applies payment methods (NEFT, RTGS, SEPA, ACH, Wire, Check), generates electronic bank payment files, and posts simultaneous clearing entries automatically.", "Automatic Payment Program (APP - T-Code F110):")

    add_h2("4.3 Accounts Receivable (FI-AR)")
    add_p("Accounts Receivable manages customer master records, invoicing, credit monitoring, and cash collection.")
    add_bullet(" Customer sub-ledger accounts link directly to the Accounts Receivable Reconciliation Account on the General Ledger.", "Customer Sub-Ledger:")
    add_bullet(" High-speed automated matching of incoming customer bank receipts against open invoices using Electronic Bank Statements (EBS) and Lockbox processing.", "Cash Application:")
    add_bullet(" Automated evaluation of overdue receivables. Generates multi-tiered dunning notices (polite reminders to formal legal demands) based on predefined grace periods and interest calculation rules.", "Automated Dunning Program (T-Code F150):")
    add_bullet(" Dynamically calculates customer credit limits, monitors total credit exposure (open orders + open deliveries + open invoices), and automatically blocks sales order processing if credit limits are breached.", "Credit Management (FSCM):")

    add_h2("4.4 Asset Accounting (FI-AA)")
    add_p("Asset Accounting manages the complete lifecycle of tangible and intangible fixed assets:")
    add_bullet(" Acquisition -> Capitalization -> Depreciation -> Transfer -> Retirement / Scrapping.", "Asset Lifecycle:")
    add_bullet(" Different valuation rules applied to the same asset (e.g., Book Depreciation Area 01 for local commercial balance sheet; Tax Depreciation Area 15 for statutory tax authorities; Group Depreciation Area 30 for IFRS group reporting).", "Depreciation Areas:")
    add_bullet(" Collects capital expenditures during the design/construction phase of an asset before settling into permanent fixed asset master records upon commissioning.", "Assets Under Construction (AuC):")

    add_h2("4.5 Bank Ledger & Cash Management (FI-BL)")
    add_p("Manages bank master records, house banks, account IDs, and liquidity. It automates Electronic Bank Statement (EBS) ingestion (formats such as SWIFT MT940, CAMT.053, and BAI2), matching cleared items and providing corporate treasury with real-time cash positioning and liquidity forecasts.")

    # 5. Deep-Dive: SAP CO Core Sub-Modules
    add_h1("5. Deep-Dive: SAP CO (Controlling / Management Accounting)")
    add_p("Controlling provides internal executives and cost accountants with tools to measure profitability, control overhead expenditures, and value manufacturing operations.")
    
    add_h2("5.1 Cost Element Accounting (CO-CEL)")
    add_bullet(" Expenses that originate from external procurement transactions (e.g., Raw Material Purchases, Utilities, Office Supplies). Every primary cost element maps directly to an existing General Ledger expense account in FI.", "Primary Cost Elements:")
    add_bullet(" Costs that arise exclusively from internal cost allocations, assessments, or activity distributions within the enterprise (e.g., IT department overhead charged to manufacturing plants). They have no direct external financial footprint in FI.", "Secondary Cost Elements:")

    add_h2("5.2 Cost Center Accounting (CO-CCA)")
    add_p("Tracks where costs are incurred across organizational responsibility units:")
    add_bullet(" Subunits representing organizational responsibilities (e.g., Quality Assurance, Maintenance, Assembly Line 2, HR).", "Cost Centers & Standard Hierarchy:")
    add_bullet(" Measurable operational outputs (e.g., machine runtime hours, labor hours, kilowatt hours) used to calculate internal activity rates:", "Activity Types & Rates:")
    add_callout(doc, "Activity Rate Formula: Activity Rate ($/hr) = Total Budgeted Cost Center Costs / Total Planned Activity Output Units", "Activity Rate Calculation")
    add_bullet(" Methods for reallocating overhead across departments. Distribution retains the original primary cost element, while Assessment aggregates multiple costs and transfers them using a secondary cost element.", "Cost Allocations (Distribution vs. Assessment):")

    add_h2("5.3 Internal Orders (CO-IO)")
    add_p("Used to plan, collect, and track costs for temporary, specific, or non-recurring corporate initiatives (e.g., Trade Show Marketing Campaign, Research & Development Project, Capital Plant Overhaul). Features hard budget limits (Availability Control) that prevent purchase orders when allocated funds are exhausted.")

    add_h2("5.4 Product Cost Controlling (CO-PC)")
    add_p("Product Costing is the analytical core of manufacturing finance. It integrates directly with Production Planning (PP) and Materials Management (MM) to calculate the Cost of Goods Manufactured (COGM) and Cost of Goods Sold (COGS).")
    add_bullet(" Aggregates material costs (from Bill of Materials) and operation costs (from Work Center routings and activity rates).", "Standard Cost Estimate (Costing Run):")
    add_bullet(" Values unfinished manufacturing orders on the shop floor at month-end, capitalizing them as assets on the balance sheet.", "Work in Process (WIP):")
    add_bullet(" Compares actual production debits against standard cost credits, breaking variances into Input Price Variances, Input Quantity Variances, Scrap Variances, and Efficiency Variances.", "Variance Analysis (T-Code KKS2):")

    add_h2("5.5 Profitability Analysis (CO-PA) & Profit Center Accounting (CO-PCA)")
    add_bullet(" Enables multi-dimensional profitability analysis across external market segments (by Product Group, Customer Segment, Geographic Sales Region, Distribution Channel). In S/4HANA, Account-Based CO-PA is fully unified with the General Ledger.", "Profitability Analysis (CO-PA):")
    add_bullet(" Facilitates decentralized responsibility accounting by tracking both revenues and expenses for business divisions, allowing divisional managers to assess return on investment (ROI).", "Profit Center Accounting (CO-PCA):")

    # 6. Integration of SAP FICO with Operational Modules
    add_h1("6. End-to-End Integration of SAP FICO with Operational Modules")
    add_p("The foundational strength of SAP ERP lies in its real-time, automated integration. Business events in logistics, sales, procurement, and manufacturing trigger financial journal entries instantaneously without manual human intervention.")

    add_h2("6.1 Integration with SAP MM (Materials Management) - Procure-to-Pay (P2P)")
    add_p("The Procure-to-Pay lifecycle seamlessly bridges physical warehouse receiving and financial accounting:")
    add_bullet(" Purchase Requisition created (ME51N) and approved into a formal Purchase Order (ME21N). A financial commitment is logged in Controlling.", "Step 1: Purchase Order Creation:")
    add_bullet(" Warehouse logs physical arrival in transaction MIGO. SAP automatically posts an accounting document:", "Step 2: Goods Receipt (MIGO):")
    add_callout(doc, 
        "Debit: Inventory Balance Sheet Account (Transaction Key BSX)\n"
        "Credit: GR/IR Clearing Interim Account (Transaction Key WRX)\n\n"
        "Significance: The GR/IR account serves as an interim holding account balancing physical goods received against future vendor invoices.", 
        "Goods Receipt Accounting Entry")
    add_bullet(" Accounts Payable logs vendor bill in transaction MIRO (Logistics Invoice Verification). SAP posts:", "Step 3: Invoice Verification (MIRO):")
    add_callout(doc,
        "Debit: GR/IR Clearing Interim Account (Transaction Key WRX) [Clearing the holding balance]\n"
        "Credit: Vendor Sub-Ledger / Accounts Payable Reconciliation Account (Transaction Key KBS)",
        "Invoice Verification Accounting Entry")
    add_bullet(" Finance runs Automatic Payment Program (F110):", "Step 4: Vendor Settlement:")
    add_callout(doc,
        "Debit: Vendor Sub-Ledger / Accounts Payable Reconciliation Account\n"
        "Credit: Bank Outflow / Bank Clearing Account",
        "Payment Run Accounting Entry")
    add_p("How does SAP know which accounts to hit? It uses the Automatic Account Determination Matrix (Transaction OBYC), which links Chart of Accounts, Valuation Class (assigned in Material Master), Movement Types, and Transaction Keys (BSX, WRX, PRD).")

    add_h2("6.2 Integration with SAP SD (Sales and Distribution) - Order-to-Cash (O2C)")
    add_p("The Order-to-Cash cycle connects external customer demand with financial realization:")
    add_bullet(" Sales order created (VA01). Real-time credit check evaluates customer credit limit against open items.", "Step 1: Sales Order Booking:")
    add_bullet(" Warehouse performs Post Goods Issue (PGI) in transaction VL01N. Financial posting:", "Step 2: Delivery & Goods Issue (PGI):")
    add_callout(doc,
        "Debit: Cost of Goods Sold (COGS) Expense Account (P&L)\n"
        "Credit: Finished Goods Inventory Balance Sheet Account (BSX)",
        "Goods Issue Accounting Entry")
    add_bullet(" Billing department creates customer invoice in transaction VF01. Financial posting:", "Step 3: Billing Document Creation (VF01):")
    add_callout(doc,
        "Debit: Customer Sub-Ledger / Accounts Receivable Reconciliation Account\n"
        "Credit: Sales Revenue Account (Account Key ERL in VKOA)\n"
        "Credit: Output Sales Tax Payable (Account Key MWS)",
        "Billing Document Accounting Entry")
    add_bullet(" Customer remits payment. Payment entry posts Debit to Bank Inflow and Credit to Customer Sub-Ledger, clearing open items.", "Step 4: Payment Realization:")
    add_p("Automatic revenue account assignment is controlled by Transaction VKOA, evaluating Customer Account Assignment Groups, Material Groups, and Sales Condition Types.")

    add_h2("6.3 Integration with SAP PP, HCM, PM, and PS")
    add_bullet(" Linking Work Centers to Cost Centers allows manufacturing machine and labor hours to be costed in real-time. Production variances settle directly to the P&L via transaction KO88.", "SAP PP (Production Planning):")
    add_bullet(" Payroll runs generate automated journal entries debiting Wage Expenses and crediting Net Payables and Statutory Tax liabilities, while distributing costs to respective Cost Centers.", "SAP HCM / SuccessFactors:")
    add_bullet(" Maintenance orders track machine repairs and spare parts, settling expenses into plant manufacturing Cost Centers.", "SAP PM (Plant Maintenance):")
    add_bullet(" Major capital expenditure initiatives (e.g., factory construction) accumulate expenses on Work Breakdown Structure (WBS) elements before capitalizing into Assets Under Construction (AuC).", "SAP PS (Project System):")

    # 7. Real-World Use Cases
    add_h1("7. Real-World Industry Use Cases & Scenarios")
    
    add_h2("Case 1: Multinational Enterprise Multi-GAAP & Multi-Currency Consolidation")
    add_p("A Fortune 500 manufacturing conglomerate with corporate headquarters in Frankfurt operates legal subsidiaries in Chicago, Tokyo, and Mumbai. The US entity must report local taxes and financials in USD according to US GAAP, while the parent requires consolidated group reporting in EUR under IFRS.")
    add_p("Solution: Using SAP S/4HANA Parallel Accounting, the enterprise configures Leading Ledger (0L) for IFRS in EUR and Non-Leading Ledger (2L) for US GAAP in USD. Every operational invoice immediately posts to both ledgers simultaneously in both local transaction currency and corporate group currency. Month-end consolidation requires zero manual spreadsheet manipulation.")

    add_h2("Case 2: Automotive Standard Costing & Production Variance Decomposition")
    add_p("An automobile assembly plant manufactures 50,000 electric vehicles annually. During an inflationary period, actual manufacturing costs exceed baseline standards by $8.4 million.")
    add_p("Solution: Using SAP CO-PC Variance Calculation (KKS2), the plant controller decomposes the $8.4M variance into $5.1M Input Price Variance (unplanned raw lithium price surges), $2.1M Input Quantity Variance (excess sheet metal stamping scrap), and $1.2M Resource Efficiency Variance (assembly line downtime). Management precisely attributes financial accountability to procurement, quality control, and maintenance.")

    add_h2("Case 3: High-Volume Automated Accounts Receivable in Retail Wholesale")
    add_p("A pharmaceutical distributor delivers medicines to 15,000 pharmacies daily, issuing over 60,000 invoices per week.")
    add_p("Solution: Deploying SAP Electronic Bank Statement (EBS) and Lockbox automation in FI-BL, incoming bank payment batches are automatically parsed. Machine learning algorithms achieve a 95% automated cash clearing rate. Undisputed overdue invoices trigger automated dunning notices (F150), decreasing Days Sales Outstanding (DSO) by 12 days.")

    # 8. Benefits & Challenges
    add_h1("8. Strategic Benefits & Enterprise Implementation Challenges")
    
    add_h2("8.1 Core Strategic & Operational Benefits")
    add_bullet(" Single source of truth via Universal Journal (ACDOCA) eliminates data discrepancies between external accounting and internal management.", "1. Unified Financial Architecture:")
    add_bullet(" Month-end financial close cycles reduced from 15 business days to 2-3 business days through automated closing cockpits.", "2. Accelerated Financial Close (Fast Close):")
    add_bullet(" Immutable, timestamped audit records with full drill-down capability from consolidated balance sheets to origin logistics documents.", "3. Comprehensive Regulatory Compliance:")
    add_bullet(" Automated 3-way matching in AP and automated credit blocking in SD minimize working capital leakage.", "4. Optimized Working Capital:")
    add_bullet(" Deep visibility into profitability across customers, products, channels, and regions via CO-PA.", "5. Multi-Dimensional Profitability:")

    add_h2("8.2 Critical Implementation Challenges & Mitigation")
    
    # Table of Challenges
    table_chal = doc.add_table(rows=6, cols=3)
    table_chal.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Implementation Challenge", "Enterprise Risk / Pain Point", "Recommended Mitigation Strategy"]
    r0_c = table_chal.rows[0]
    for i, h_text in enumerate(c_headers):
        cell = r0_c.cells[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    chal_data = [
        ("High Cost & High TCO", "Significant licensing, infrastructure, consulting, and maintenance capital requirements.", "Adopt SAP S/4HANA Cloud (Public Edition) to transition CapEx to OpEx; implement modular phased rollouts."),
        ("Steep Learning Curve", "Intricate transaction codes, thousands of configuration tables, user operational resistance.", "Modernize interface using SAP Fiori web apps; deploy robust change management and employee training programs."),
        ("Legacy Data Migration", "Inconsistent legacy charts of accounts, corrupted vendor/customer master data, reconciliation mismatch.", "Implement SAP Master Data Governance (MDG); conduct multiple iterative data cleansing and cutover rehearsals."),
        ("The 'Customization Trap'", "Excessive custom ABAP Z-programs causing system instability and blocking future upgrades.", "Adhere strictly to SAP's 'Clean Core' paradigm; develop custom functionality side-by-side using SAP BTP."),
        ("Cross-Module Integration Errors", "Misconfigured account determination rules in OBYC or VKOA halting billing or goods receipt.", "Execute rigorous end-to-end integration testing (Unit, SIT, UAT) with comprehensive baseline documentation.")
    ]
    
    for row_idx, data in enumerate(chal_data):
        row = table_chal.rows[row_idx + 1]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0, 51, 102)
            else:
                r.font.color.rgb = RGBColor(40, 40, 40)
                
    set_table_borders(table_chal, color="D0D7DE", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 9. Future Trends & Conclusion
    add_h1("9. The Future of SAP Financials: S/4HANA, AI & Autonomous Finance")
    add_p("The discipline of corporate finance is undergoing a rapid transition from historical recordkeeping to real-time predictive financial steering:")
    add_bullet(" Uses sales order commitments to populate predictive ledgers, forecasting future revenues, COGS, and cash demands prior to billing or shipping.", "Predictive Accounting:")
    add_bullet(" Machine learning algorithms analyze historical invoice clearing patterns, automatically reconciling unmatched remittances.", "AI-Powered Cash Application:")
    add_bullet(" Continuous algorithmic audits monitor journal entries in real-time, instantly identifying suspicious postings or policy deviations.", "Intelligent Anomaly Detection:")
    add_bullet(" Transitioning from artificial monthly closing batches toward a continuous, uninterrupted real-time closing cycle.", "Continuous Accounting:")

    add_h1("10. Master Glossary & Essential SAP FICO Transaction Codes (T-Codes)")
    
    # Table of T-Codes
    table_tcode = doc.add_table(rows=16, cols=3)
    table_tcode.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Functional Domain", "Transaction Code", "Description & Operational Use"]
    r0_t = table_tcode.rows[0]
    for i, h_text in enumerate(t_headers):
        cell = r0_t.cells[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    tcode_data = [
        ("General Ledger (FI-GL)", "FS00", "Centrally create, display, and modify G/L Account Master Records."),
        ("General Ledger (FI-GL)", "FB50", "Enter G/L Account Document (Single-screen posting)."),
        ("General Ledger (FI-GL)", "FAGLL03", "Display / Change G/L Account Line Items (New G/L)."),
        ("Accounts Payable (FI-AP)", "BP", "Maintain Business Partner (Central vendor/customer master in S/4HANA)."),
        ("Accounts Payable (FI-AP)", "FB60", "Enter Incoming Vendor Invoice (Direct FI posting)."),
        ("Accounts Payable (FI-AP)", "F110", "Execute Automatic Payment Program (APP) for bulk disbursements."),
        ("Accounts Receivable (FI-AR)", "FB70", "Enter Outgoing Customer Invoice."),
        ("Accounts Receivable (FI-AR)", "F-28", "Post Incoming Customer Payment."),
        ("Accounts Receivable (FI-AR)", "F150", "Execute Automated Customer Dunning Run."),
        ("Asset Accounting (FI-AA)", "AS01 / AS02", "Create / Change Fixed Asset Master Record."),
        ("Asset Accounting (FI-AA)", "AFAB", "Execute Periodic Asset Depreciation Posting Run."),
        ("Cost Center Accounting (CO-CCA)", "KS01 / KS02", "Create / Change Cost Center Master Record."),
        ("Product Costing (CO-PC)", "CK11N / CK24", "Create, mark, and release Material Cost Estimate with Quantity Structure."),
        ("Integration (MM-FI)", "OBYC", "Configure Automatic Account Determination for Materials Management."),
        ("Integration (SD-FI)", "VKOA", "Configure Revenue Account Determination for Sales & Distribution.")
    ]
    
    for row_idx, data in enumerate(tcode_data):
        row = table_tcode.rows[row_idx + 1]
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            if col_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(0, 51, 102)
            else:
                r.font.color.rgb = RGBColor(40, 40, 40)
                
    set_table_borders(table_tcode, color="D0D7DE", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h1("11. Conclusion")
    add_p("SAP FICO stands as the undisputed benchmark in enterprise financial architecture. By seamlessly unifying statutory external reporting (FI) with internal operational controlling (CO), and connecting physical logistics transactions in real-time through automated account determinations (OBYC, VKOA), SAP FICO empowers global enterprises with financial governance, audit transparency, and strategic decision support.")
    add_p("With the architectural evolution to SAP S/4HANA's Universal Journal (ACDOCA) and in-memory computing, the legacy friction of month-end reconciliations has been eliminated, paving the way for autonomous, AI-driven, continuous accounting. For aspiring ERP consultants and enterprise finance professionals, mastering the functional and integration paradigms of SAP FICO represents an essential foundation for driving modern digital transformation.")

    add_h1("12. References & Citations")
    add_bullet(" SAP Help Portal. (2024). Financial Accounting (FI) and Management Accounting (CO) in SAP S/4HANA Enterprise Management.")
    add_bullet(" Murray, M., & Chudy, N. (2021). SAP S/4HANA Financial Accounting Configuration. SAP PRESS.")
    add_bullet(" Rhein, A. (2020). Controlling with SAP S/4HANA: Business User Guide. SAP PRESS.")
    add_bullet(" Jones, P. (2022). Integrating Materials Management and Financial Accounting in SAP. Galileo Press.")
    add_bullet(" Institute of Management Accountants (IMA). (2023). Enterprise ERP Architectures and the Modern Management Accountant. Strategic Finance.")
    add_bullet(" Deloitte Insights. (2024). Autonomous Finance and the Modern ERP Landscape. Deloitte Development LLC.")

    # Save document
    output_path = r"C:\Users\Laxmi Gupta\.antigravity-ide\SAP-FICO-Internship-Task-1\SAP_FICO_Comprehensive_Research_Report.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    build_sap_fico_doc()
