"""
Opportunity OS - MCP Tools Module
This module encapsulates the core logic for querying career opportunities.
It is designed to be highly extensible so it can easily be connected to live 
APIs (e.g., GitHub API, Devpost API, LinkedIn Jobs, etc.) or external databases.
"""

import sys

# Curated dataset of opportunities categorized by type and domain
OPPORTUNITIES_DB = {
    "hackathons": [
        # Technology
        {
            "name": "OpenAI DevDay Hackathon",
            "domain": "Technology",
            "match_score": "98/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "High alignment with cutting-edge AI development skills and prompt engineering.",
            "skills_required": "Python, API Integration, Large Language Models",
            "preparation_time": "2-3 weeks",
            "next_action": "Read the OpenAI API docs and sign up on Devpost."
        },
        {
            "name": "Global Web3 Hackfest",
            "domain": "Technology",
            "match_score": "88/100",
            "priority": "Medium",
            "difficulty": "Intermediate",
            "why_matches": "Excellent match for decentralized systems and full-stack engineering interests.",
            "skills_required": "Solidity, React, Node.js, Web3.js",
            "preparation_time": "1-2 weeks",
            "next_action": "Review basic Solidity syntax and smart contract deployment guides."
        },
        # Mechanical
        {
            "name": "Aerospace Design Sprint",
            "domain": "Mechanical",
            "match_score": "92/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Direct application of aerospace structural design and CAD modeling skills.",
            "skills_required": "CAD, SolidWorks, Aerodynamics, FEA",
            "preparation_time": "3 weeks",
            "next_action": "Form a team and review fuselage modeling case studies."
        },
        # Medical
        {
            "name": "BioTech Future Hack",
            "domain": "Medical",
            "match_score": "90/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Bridges medical research with hardware prototyping and clinical analysis.",
            "skills_required": "Bio-informatics, Medical Devices, Python, Data Analytics",
            "preparation_time": "2 weeks",
            "next_action": "Research current trends in non-invasive patient monitoring."
        },
        # Business
        {
            "name": "Venture Capital Case Crack",
            "domain": "Business",
            "match_score": "94/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Fits business analytics, financial modeling, and venture valuation skills.",
            "skills_required": "Financial Modeling, Market Research, Pitch Deck Design",
            "preparation_time": "1 week",
            "next_action": "Download case files from the competition portal."
        },
        # Design
        {
            "name": "Adobe Creative Jam",
            "domain": "Design",
            "match_score": "96/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Perfect for showcases in interactive UI/UX and motion graphics.",
            "skills_required": "Figma, Adobe XD, Prototyping, Visual Design",
            "preparation_time": "1 week",
            "next_action": "Review the design brief and create a Figma design system kit."
        },
        # Research
        {
            "name": "Quantum Computing Ideas Lab",
            "domain": "Research",
            "match_score": "95/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Targets theoretical physics and algorithms research.",
            "skills_required": "Qiskit, Python, Quantum Mechanics, Scientific Writing",
            "preparation_time": "4 weeks",
            "next_action": "Draft a short abstract on quantum error mitigation strategies."
        },
        # Law
        {
            "name": "AI Policy & Legal Tech Hackathon",
            "domain": "Law",
            "match_score": "93/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Bridges emerging AI regulations, ethics, and legal frameworks.",
            "skills_required": "Legal Analysis, Policy Writing, AI Ethics",
            "preparation_time": "2 weeks",
            "next_action": "Read the EU AI Act and drafting templates."
        },
        # Entrepreneurship
        {
            "name": "Techstars Startup Weekend",
            "domain": "Entrepreneurship",
            "match_score": "97/100",
            "priority": "Critical",
            "difficulty": "Intermediate",
            "why_matches": "Rapid validation of business ideas, pitch training, and networking.",
            "skills_required": "Business Development, Pitching, Agile MVP Building",
            "preparation_time": "3-5 days",
            "next_action": "Draft a 60-second elevator pitch and secure your ticket."
        }
    ],
    "internships": [
        # Technology
        {
            "name": "Google AI Residency",
            "domain": "Technology",
            "match_score": "97/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Ideal for students pursuing machine learning engineering and research.",
            "skills_required": "PyTorch, TensorFlow, Python, Algorithm Design",
            "preparation_time": "4-6 weeks",
            "next_action": "Solve LeetCode medium questions and update your AI project portfolio."
        },
        {
            "name": "Stripe Software Engineering Intern",
            "domain": "Technology",
            "match_score": "91/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Focuses on robust API design, backend architecture, and clean code.",
            "skills_required": "Ruby on Rails, Go, API Design, System Architecture",
            "preparation_time": "3 weeks",
            "next_action": "Practice system design fundamentals and REST API mockups."
        },
        # Mechanical
        {
            "name": "Tesla CAD & Hardware Intern",
            "domain": "Mechanical",
            "match_score": "95/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Focuses on high-performance mechanical systems and design for manufacturing (DFM).",
            "skills_required": "SolidWorks, GD&T, Finite Element Analysis (FEA)",
            "preparation_time": "4 weeks",
            "next_action": "Prepare CAD assembly files highlighting DFM principles for interview review."
        },
        # Medical
        {
            "name": "Mayo Clinic Bio-Medical Analyst",
            "domain": "Medical",
            "match_score": "93/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Involves processing healthcare data models and analyzing clinical trials.",
            "skills_required": "Python, Biostatistics, Clinical Standards, SQL",
            "preparation_time": "2 weeks",
            "next_action": "Review HIPAA guidelines and medical data structures."
        },
        # Business
        {
            "name": "McKinsey Business Analyst Intern",
            "domain": "Business",
            "match_score": "95/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "High focus on case interview strategies, business growth analysis, and communication.",
            "skills_required": "Structured Problem Solving, Case Interviews, Tableau, Excel",
            "preparation_time": "4 weeks",
            "next_action": "Read Victor Cheng's 'Case Interview' and do 10 interactive case mocks."
        },
        # Design
        {
            "name": "Apple Product Design Intern",
            "domain": "Design",
            "match_score": "98/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Opportunity to work with premium, minimalist user interfaces and hardware designs.",
            "skills_required": "UX Research, Interaction Design, Figma, 3D Prototyping",
            "preparation_time": "4-6 weeks",
            "next_action": "Refine top 3 case studies in your portfolio with emphasis on design iteration."
        },
        # Research
        {
            "name": "CERN Technical Student (Computing/Physics)",
            "domain": "Research",
            "match_score": "96/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Conduct research on large-scale physics data analytics.",
            "skills_required": "C++, Python, High Performance Computing, Data Processing",
            "preparation_time": "4 weeks",
            "next_action": "Submit your university transcript and letters of recommendation."
        },
        # Law
        {
            "name": "IP Law Legal Intern at Baker McKenzie",
            "domain": "Law",
            "match_score": "92/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Deep dive into patent, trademark, and tech copyright legal processes.",
            "skills_required": "Intellectual Property Law, Research, Case Writing",
            "preparation_time": "3 weeks",
            "next_action": "Write an analysis of recent IP legal decisions in software patents."
        },
        # Entrepreneurship
        {
            "name": "Y Combinator Founder in Residence / Intern",
            "domain": "Entrepreneurship",
            "match_score": "96/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Direct exposure to venture-backed startups and growth strategies.",
            "skills_required": "Growth Hacking, Product Strategy, Customer Development",
            "preparation_time": "2 weeks",
            "next_action": "Submit a video explaining your startup project and market validation."
        }
    ],
    "open_source": [
        # Technology
        {
            "name": "Google Summer of Code (GSoC) - Python Software Foundation",
            "domain": "Technology",
            "match_score": "95/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Invaluable program for contributing to core Python packages (like Django, Pandas).",
            "skills_required": "Git, Python, Open Source Collaboration, Testing",
            "preparation_time": "3 weeks",
            "next_action": "Find PSF sub-organizations on GSoC portal and make initial issue contributions."
        },
        {
            "name": "Linux Kernel Development Program",
            "domain": "Technology",
            "match_score": "87/100",
            "priority": "Medium",
            "difficulty": "Advanced",
            "why_matches": "Excellent for low-level systems programming and operating systems interests.",
            "skills_required": "C, Bash, Git, Operating Systems Architecture",
            "preparation_time": "4 weeks",
            "next_action": "Subscribe to the LKML (Linux Kernel Mailing List) and read kernel patch docs."
        },
        # Mechanical
        {
            "name": "FreeCAD Core Contributions",
            "domain": "Mechanical",
            "match_score": "90/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Develop new features for the largest open source CAD design suites.",
            "skills_required": "C++, Python, Qt, CAD Concepts",
            "preparation_time": "2 weeks",
            "next_action": "Set up the local build environment for FreeCAD and check open issues."
        },
        # Medical
        {
            "name": "OpenEMR Healthcare Platform Contributions",
            "domain": "Medical",
            "match_score": "89/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Help improve medical health record management used worldwide.",
            "skills_required": "PHP, Javascript, MySQL, Health Standards",
            "preparation_time": "2 weeks",
            "next_action": "Check OpenEMR GitHub repository for beginner-friendly issues."
        },
        # Business
        {
            "name": "ERPNext Open Source ERP Contributions",
            "domain": "Business",
            "match_score": "92/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Bridges enterprise software architecture with business processes.",
            "skills_required": "Python, Frappe Framework, SQL, Business Logic",
            "preparation_time": "1-2 weeks",
            "next_action": "Run ERPNext locally using Docker and study the asset management module."
        },
        # Design
        {
            "name": "Penpot Design System UI contributions",
            "domain": "Design",
            "match_score": "94/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Help build Penpot, the first open-source, collaborative design tool.",
            "skills_required": "ClojureScript, CSS/SVG, UI Design, SVG Layouts",
            "preparation_time": "2 weeks",
            "next_action": "Join Penpot community forum and contribute to design system updates."
        },
        # Research
        {
            "name": "SymPy (Symbolic Math Library) Contributions",
            "domain": "Research",
            "match_score": "94/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Perfect for mathematical and algorithmic programming contributions.",
            "skills_required": "Python, Abstract Algebra, Calculus, Numerical Methods",
            "preparation_time": "2 weeks",
            "next_action": "Submit a pull request solving a calculus solver issue on GitHub."
        },
        # Law
        {
            "name": "Stanford CodeX Legal Schema Project",
            "domain": "Law",
            "match_score": "91/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Contribute to building standard machine-readable legal schemas.",
            "skills_required": "JSON-LD, XML, Legal Knowledge, Knowledge Representation",
            "preparation_time": "2 weeks",
            "next_action": "Review current draft schemas on Stanford Legal Tech GitHub."
        },
        # Entrepreneurship
        {
            "name": "Odoo CRM Enterprise App Modules",
            "domain": "Entrepreneurship",
            "match_score": "93/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Design business apps for Odoo, the modular open-source ERP system.",
            "skills_required": "Python, XML, PostgreSQL, Product Management",
            "preparation_time": "1-2 weeks",
            "next_action": "Build and publish a free community utility module on Odoo app store."
        }
    ],
    "competitions": [
        # Technology
        {
            "name": "Kaggle Grand Challenge",
            "domain": "Technology",
            "match_score": "96/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Provides premium testing ground for advanced model architecture tuning.",
            "skills_required": "Python, Pandas, PyTorch, Feature Engineering",
            "preparation_time": "3-4 weeks",
            "next_action": "Download the active competition dataset and set up a baseline notebook."
        },
        {
            "name": "Imagine Cup by Microsoft",
            "domain": "Technology",
            "match_score": "90/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Great showcase for cloud-based social impact projects using AI.",
            "skills_required": "Azure, Software Architecture, Project Pitching",
            "preparation_time": "4 weeks",
            "next_action": "Draft a 3-page executive summary of your technology solution."
        },
        # Mechanical
        {
            "name": "Formula SAE Design Competition",
            "domain": "Mechanical",
            "match_score": "96/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Requires intensive vehicle dynamics simulation, materials analysis, and fabrication design.",
            "skills_required": "CAD modeling, ANSYS FEA, Chassis Design, Welding/Machining",
            "preparation_time": "6-12 months",
            "next_action": "Coordinate with the team on structural suspension node analysis reports."
        },
        # Medical
        {
            "name": "MIT HealthHacks",
            "domain": "Medical",
            "match_score": "92/100",
            "priority": "High",
            "difficulty": "Intermediate",
            "why_matches": "Solves real healthcare challenges presented by hospital clinicians.",
            "skills_required": "Rapid Prototyping, Clinical Workflow, UX/UI, Bio-sensing",
            "preparation_time": "1 week",
            "next_action": "Apply to participate as an individual or team lead."
        },
        # Business
        {
            "name": "Hult Prize Startup Challenge",
            "domain": "Business",
            "match_score": "95/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Solve global social impact problems through innovative enterprise models.",
            "skills_required": "Social Entrepreneurship, Pitching, Business Strategy",
            "preparation_time": "4 weeks",
            "next_action": "Analyze current global Hult Prize themes and register your team."
        },
        # Design
        {
            "name": "Red Dot Design Award Competition",
            "domain": "Design",
            "match_score": "97/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Prestige standard recognition for high quality industrial or interface product design.",
            "skills_required": "Product Rendering, Industrial Design, Graphic Design",
            "preparation_time": "6 weeks",
            "next_action": "Create rendering sheets and write-ups highlighting manufacturing viability."
        },
        # Research
        {
            "name": "Falling Walls Lab Research Competition",
            "domain": "Research",
            "match_score": "94/100",
            "priority": "High",
            "difficulty": "Advanced",
            "why_matches": "Pitch breakthrough research in 3 minutes to a global scientific jury.",
            "skills_required": "Public Speaking, Slide Presentation, Scientific Synthesis",
            "preparation_time": "3 weeks",
            "next_action": "Prepare your 3-minute pitch outline and submit your entry video."
        },
        # Law
        {
            "name": "Jessup International Law Moot Court",
            "domain": "Law",
            "match_score": "96/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "Highly rigorous simulated dispute before the International Court of Justice.",
            "skills_required": "Oral Advocacy, Public International Law, Legal Drafting",
            "preparation_time": "3-6 months",
            "next_action": "Begin drafting the applicant and respondent memorials."
        },
        # Entrepreneurship
        {
            "name": "Rice Business Plan Competition",
            "domain": "Entrepreneurship",
            "match_score": "97/100",
            "priority": "Critical",
            "difficulty": "Advanced",
            "why_matches": "World's richest graduate student startup business plan competition.",
            "skills_required": "Financial Projections, Venture Pitching, Due Diligence",
            "preparation_time": "8 weeks",
            "next_action": "Upload business plan drafts and request university certification."
        }
    ]
}


def _filter_opportunities(category: str, domain: str) -> list:
    """
    Helper function to filter opportunities by category and domain.
    Matches the domain case-insensitively.
    """
    category_list = OPPORTUNITIES_DB.get(category.lower(), [])
    if not category_list:
        return []

    # Clean domain string
    domain_clean = domain.strip().lower()

    # Filter opportunities
    filtered = [
        item for item in category_list 
        if item.get("domain", "").lower() == domain_clean
    ]

    # If nothing specific was found or domain is generic, return a sample of high-impact opportunities
    if not filtered:
        # Fallback to general high-impact items for that category
        filtered = category_list[:3]

    return filtered


def search_hackathons(domain: str) -> list:
    """
    Searches for hackathons related to a specific domain.
    """
    print(f"DEBUG (mcp/tools): search_hackathons called for domain: {domain}", file=sys.stderr)
    return _filter_opportunities("hackathons", domain)


def search_internships(domain: str) -> list:
    """
    Searches for internships related to a specific domain.
    """
    print(f"DEBUG (mcp/tools): search_internships called for domain: {domain}", file=sys.stderr)
    return _filter_opportunities("internships", domain)


def search_open_source(domain: str) -> list:
    """
    Searches for open source programs or projects related to a specific domain.
    """
    print(f"DEBUG (mcp/tools): search_open_source called for domain: {domain}", file=sys.stderr)
    return _filter_opportunities("open_source", domain)


def search_competitions(domain: str) -> list:
    """
    Searches for competitions or tournaments related to a specific domain.
    """
    print(f"DEBUG (mcp/tools): search_competitions called for domain: {domain}", file=sys.stderr)
    return _filter_opportunities("competitions", domain)
