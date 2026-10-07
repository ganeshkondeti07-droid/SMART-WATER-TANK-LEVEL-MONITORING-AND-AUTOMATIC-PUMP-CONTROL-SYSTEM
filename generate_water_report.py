"""
Script to generate the comprehensive Word document report for the Water Tank System
following the evaluation criteria (PC1-PC9) and formatting requirements.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

def create_report():
    doc = Document()
    
    # Define styles
    styles = doc.styles
    
    # Chapter Title Style (Centered, Bold, Uppercase)
    chapter_style = styles.add_style('Chapter Title', WD_STYLE_TYPE.PARAGRAPH)
    chapter_font = chapter_style.font
    chapter_font.name = 'Times New Roman'
    chapter_font.size = Pt(14)
    chapter_font.bold = True
    chapter_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    chapter_style.paragraph_format.space_after = Pt(24)
    
    # Heading 1 Style (1.1, 1.2)
    h1_style = styles['Heading 1']
    h1_font = h1_style.font
    h1_font.name = 'Times New Roman'
    h1_font.size = Pt(12)
    h1_font.bold = True
    h1_font.color.rgb = RGBColor(0, 0, 0)
    
    # Heading 2 Style (1.1.1, 1.1.2)
    h2_style = styles['Heading 2']
    h2_font = h2_style.font
    h2_font.name = 'Times New Roman'
    h2_font.size = Pt(12)
    h2_font.bold = True
    h2_font.italic = True
    h2_font.color.rgb = RGBColor(0, 0, 0)
    
    # Normal Text Style
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(12)

    # --- COVER PAGE ---
    doc.add_paragraph('\n\n\n\n')
    title = doc.add_paragraph('INTERNSHIP REPORT\nON\nSMART WATER TANK LEVEL MONITORING AND AUTOMATIC PUMP CONTROL SYSTEM', style='Chapter Title')
    title.runs[0].font.size = Pt(16)
    
    doc.add_paragraph('\n\n')
    submitted_by = doc.add_paragraph('Submitted by:\nInternship Project Team', style='Normal')
    submitted_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()

    # --- TABLE OF CONTENTS ---
    doc.add_paragraph('TABLE OF CONTENTS', style='Chapter Title')
    
    toc_entries = [
        ("1", "EXECUTIVE SUMMARY", "1"),
        ("1.1", "Learning Objectives", "1"),
        ("1.2", "Outcomes Achieved", "2"),
        ("2", "OVERVIEW OF THE ORGANIZATION", "3"),
        ("2.1", "Introduction of the Organization", "3"),
        ("2.2", "Vision, Mission, and Values", "3"),
        ("2.3", "Policy of the Organization in Relation to the Intern Role", "4"),
        ("2.4", "Organizational Structure", "4"),
        ("2.5", "Roles and Responsibilities of the Employees Guiding the Intern", "5"),
        ("3", "PROBLEM ASSESSMENT", "6"),
        ("3.1", "Problem Statement", "6"),
        ("3.2", "Key Parameters (PC1)", "7"),
        ("3.3", "Requirements Evaluation (PC2)", "8"),
        ("4", "SOLUTION DESIGN", "10"),
        ("4.1", "Solution Blueprint (PC3)", "10"),
        ("4.2", "Feasibility Assessment", "12"),
        ("4.3", "Project Implementation Plan (PC4)", "13"),
        ("5", "TECHNOLOGY STACK", "15"),
        ("5.1", "Technology Selection (PC5)", "15"),
        ("5.2", "Architecture Overview", "16"),
        ("6", "SOLUTION DEVELOPMENT", "18"),
        ("6.1", "Implementation Details (PC6)", "18"),
        ("6.2", "IoT Sensor Integration", "20"),
        ("6.3", "Data Analytics Module", "22"),
        ("7", "SOLUTION TESTING AND PERFORMANCE", "24"),
        ("7.1", "Testing Strategy (PC7)", "24"),
        ("7.2", "Bug Fixing and Issue Resolution", "25"),
        ("7.3", "Performance Evaluation (PC8)", "26"),
        ("8", "RESULTS AND VISUALIZATIONS", "28"),
        ("8.1", "Water Level Trends and Pump Operation", "28"),
        ("8.2", "Water Usage and Alert Distribution", "29"),
        ("8.3", "System Efficiency Dashboard", "30"),
        ("9", "LEARNING EVALUATION", "32"),
        ("9.1", "Technical Skill Gain (PC9)", "32"),
        ("9.2", "Conclusion", "33")
    ]
    
    for num, title, page in toc_entries:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        if "." not in num:
            run = p.add_run(f"{num}\t{title}")
            run.bold = True
        else:
            p.add_run(f"\t{num}\t{title}")
    
    doc.add_page_break()

    # Helper function to add a chapter
    def add_chapter(num, title):
        doc.add_paragraph(f'CHAPTER {num}', style='Chapter Title')
        doc.add_paragraph(title, style='Chapter Title')

    # Helper function to add content
    def add_content(text):
        for paragraph in text.split('\n\n'):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip(), style='Normal')

    # --- CHAPTER 1 ---
    add_chapter("1", "EXECUTIVE SUMMARY")
    
    add_content("""This internship report provides a comprehensive overview of my 8-week Short-Term Internship in developing a Smart Water Tank Level Monitoring and Automatic Pump Control System. The internship was undertaken as part of the academic curriculum. The primary objective of this internship was to gain proficiency in Internet of Things (IoT), data analytics, and automated control systems to address the critical issue of water resource management.

Efficient water management is essential for residential, commercial, and industrial facilities to prevent water wastage and ensure a continuous water supply. Traditional water tank management relies on manual monitoring and manual pump operation, which often leads to tank overflows, water shortages, and unnecessary electricity consumption. This project successfully addresses these limitations by providing an intelligent system that continuously monitors water levels and automatically controls pump operation based on predefined thresholds.""")
    
    doc.add_heading('1.1 Learning Objectives', level=1)
    add_content("""During my internship, I learned and practiced the following:
• To design and implement a water management simulation using Python that models real-world tank capacities, inflow/outflow rates, and pump dynamics.
• To integrate simulated IoT sensors (ultrasonic, pressure, float switch) for comprehensive water level monitoring and fault detection.
• To develop algorithms for automatic pump control that prevent both dry running (water shortages) and overflows.
• To create interactive data visualizations using Matplotlib and Seaborn to display water level trends, pump operation cycles, and system efficiency.
• To understand the software development lifecycle from requirements gathering to testing and performance evaluation.""")

    doc.add_heading('1.2 Outcomes Achieved', level=1)
    add_content("""Key outcomes from my internship include:
• A fully operational simulation of a Smart Water Tank Management System capable of managing residential, commercial, industrial, and institutional tanks simultaneously.
• An advanced analytics module that generates insights on daily water usage patterns, pump runtimes, and alert distributions.
• Successful implementation of an automated control algorithm that maintains water levels within safe operational boundaries (typically between 25% and 90% capacity).
• Professional dashboards and visualizations that help facility managers optimize water resources and electricity usage.
• Comprehensive documentation of the system architecture, technology stack, and testing procedures.""")

    doc.add_page_break()

    # --- CHAPTER 2 ---
    add_chapter("2", "OVERVIEW OF THE ORGANIZATION")
    
    doc.add_heading('2.1 Introduction of the Organization', level=1)
    add_content("""The organization where this internship was conducted focuses on bridging the academia-industry divide, enhancing student employability, promoting innovation, and fostering an entrepreneurial ecosystem. By leveraging emerging technologies such as IoT and AI, the organization aims to augment and upgrade the knowledge ecosystem, enabling beneficiaries to become contributors themselves. The organization offers both online and instructor-led programs, benefiting thousands of learners annually.""")
    
    doc.add_heading('2.2 Vision, Mission, and Values', level=1)
    add_content("""• Vision: To combine cutting-edge technology with impactful social ventures to drive technological prosperity and sustainable resource management.
• Mission: To support individuals dedicated to helping others by empowering and equipping them with modern technical skills, thereby creating an extensive educational network dedicated to societal betterment and environmental conservation.
• Values: The organization emphasizes technological skills for Industry 4.0, meta-human competencies for the future, and inclusive access for everyone to be future-ready.""")
    
    doc.add_heading('2.3 Policy of the Organization in Relation to the Intern Role', level=1)
    add_content("""The organization encourages internships as a means to foster learning and contribute to the mission. Interns are expected to adhere to the following policies:
• Confidentiality: Interns must maintain the confidentiality of all organizational data and sensitive information.
• Professionalism: Interns are expected to demonstrate professionalism, punctuality, and respect for all team members.
• Learning and Contribution: Interns are encouraged to actively participate in projects, share ideas, and contribute to the organization's goals.""")

    doc.add_heading('2.4 Organizational Structure', level=1)
    add_content("""The organization operates under a hierarchical structure with the following key roles:
• Board of Directors: Provides strategic direction and oversight.
• Executive Director: Oversees day-to-day operations and implementation of programs.
• Program Managers: Lead specific initiatives and technology projects.
• Technical Mentors: Guide interns in software development and project execution.
• Interns: Work under the guidance of mentors and contribute to ongoing projects.""")

    doc.add_heading('2.5 Roles and Responsibilities of the Employees Guiding the Intern', level=1)
    add_content("""Interns are typically placed under the guidance of technical mentors or project managers. The roles and responsibilities of these guiding employees include:
1. Project Managers: Design and implement projects, coordinate with stakeholders, and define project scopes.
2. Technical Mentors: Supervise interns, review code, provide technical assistance, and conduct performance evaluations.
3. Research Analysts: Provide domain knowledge, in this case, regarding fluid dynamics, pump specifications, and IoT standards.""")

    doc.add_page_break()

    # --- CHAPTER 3 ---
    add_chapter("3", "PROBLEM ASSESSMENT")
    
    doc.add_heading('3.1 Problem Statement', level=1)
    add_content("""Efficient water management is essential for residential, commercial, and industrial facilities to prevent water wastage and ensure a continuous water supply. Traditional water tank management relies on manual monitoring and manual pump operation, which often leads to tank overflows, water shortages, and unnecessary electricity consumption. Building owners and facility managers require intelligent systems that can automatically monitor water levels and control water pumps in real time.

The proposed solution is a Smart Water Tank Level Monitoring and Automatic Pump Control System that continuously monitors water levels and automatically controls pump operation using IoT technology. The system provides a centralized platform where water tank status is monitored through a secure and user-friendly interface.""")
    
    doc.add_heading('3.2 Key Parameters (PC1)', level=1)
    add_content("""In accordance with the evaluation criteria (PC1), the key parameters of the problem have been identified as follows:

Issue to be Solved: The reliance on manual pump operation which results in human error—either forgetting to turn the pump on (causing water shortages) or forgetting to turn it off (causing overflows and water wastage).

Target Community: The target community includes homeowners, apartment complex associations, industrial plant managers, hospital administrators, and educational institution facility teams.

User Needs and Preferences:
• Facility managers need automated control to eliminate manual intervention.
• Property owners require real-time visibility into water consumption patterns.
• Maintenance teams need instant alerts for pump malfunctions or sensor faults.
• All users prefer a system that reduces electricity bills by optimizing pump runtimes.

Environmental Impact: Tank overflows contribute significantly to fresh water wastage. By automating pump shut-offs and tracking usage patterns, the system directly supports water conservation and sustainable resource management.""")

    doc.add_heading('3.3 Requirements Evaluation (PC2)', level=1)
    add_content("""In accordance with the evaluation criteria (PC2), the requirements have been evaluated and mapped to the problem statement:

Functional Requirements:
1. Real-time Monitoring: The system must continuously measure water levels across various tank types (residential, commercial, industrial).
2. Automated Control: The system must automatically switch pumps ON at low thresholds (e.g., 25%) and OFF at high thresholds (e.g., 90%).
3. Anomaly Detection: The system must automatically detect pump malfunctions (pump ON but level dropping), sensor faults, and battery issues.
4. Data Visualization: The system must provide interactive dashboards displaying water levels, pump status, usage history, and alerts.

Non-Functional Requirements:
1. Scalability: The architecture must support monitoring multiple tanks across large commercial or industrial complexes.
2. Reliability: The automated control logic must be fail-safe to prevent dry running of pumps.
3. Accuracy: Water level sensors must be highly accurate to prevent premature or delayed pump switching.
4. Security: Pump control commands must be securely transmitted to prevent unauthorized manipulation.

Mapping to Problem Statement:
The functional requirements directly address the "manual monitoring and manual pump operation" by providing automated, threshold-based control. The non-functional requirements ensure the system is "secure, scalable, and suitable for homes, apartments, industries" as outlined in the problem statement.""")

    doc.add_page_break()

    # --- CHAPTER 4 ---
    add_chapter("4", "SOLUTION DESIGN")
    
    doc.add_heading('4.1 Solution Blueprint (PC3)', level=1)
    add_content("""In accordance with the evaluation criteria (PC3), a comprehensive solution blueprint has been designed for the Smart Water Tank Management System.

The solution utilizes a three-layer architecture:
1. Perception Layer (IoT Sensors & Actuators): This layer consists of ultrasonic water level sensors, temperature sensors, and the pump relays/actuators installed at the tanks.
2. Network Layer: This layer handles the two-way transmission of data: sensor readings to the central server, and control commands from the server to the pump actuators.
3. Application Layer: This layer processes the incoming data, executes the threshold logic, calculates water usage, and serves the interactive dashboards to facility managers.

Core Modules Designed:
• WaterManagementSystem Module: Manages the overall network of tanks and aggregates system-wide statistics.
• WaterTank Module: Simulates individual tanks, tracking capacity, inflow/outflow, and executing the automatic pump control logic.
• WaterTankAnalytics Module: Processes the raw data to generate insights, usage analyses, and visual reports.""")

    doc.add_heading('4.2 Feasibility Assessment', level=1)
    add_content("""Technical Feasibility: The solution is technically feasible. The use of Python for simulation and control logic is an industry standard. The threshold-based control algorithms are deterministic and highly reliable.

Economic Feasibility: The software solution is highly cost-effective. In a real-world deployment, the cost of ultrasonic sensors and smart relays is minimal compared to the financial losses incurred from water damage (due to overflow), wasted electricity (from pumps running dry), and municipal water bills. The return on investment (ROI) for such systems is typically achieved within months.

Operational Feasibility: The system is designed to operate autonomously. By automating pump control, facility managers are freed from daily manual checks, greatly improving operational efficiency and ensuring 24/7 water availability without human intervention.""")

    doc.add_heading('4.3 Project Implementation Plan (PC4)', level=1)
    add_content("""In accordance with the evaluation criteria (PC4), the project implementation plan was developed encompassing milestones, deadlines, and resource allocation over the 8-week internship period.

Phase 1: Requirements Gathering and Design (Weeks 1-2)
• Milestone 1: Finalize problem statement and system requirements.
• Milestone 2: Design system architecture and class diagrams.
• Resources: Technical mentor, system design documentation.

Phase 2: Core System Development (Weeks 3-4)
• Milestone 3: Develop the WaterTank and WaterManagementSystem classes.
• Milestone 4: Implement realistic data generation algorithms for water usage and pump inflow rates.
• Resources: Python development environment.

Phase 3: Automated Control and IoT Sensor Simulation (Weeks 5-6)
• Milestone 5: Develop the IoTWaterLevelSensor simulation with accuracy and fault modeling.
• Milestone 6: Implement the automated pump control logic (ON/OFF thresholds) and anomaly detection.
• Resources: Python development environment, testing frameworks.

Phase 4: Analytics, Visualization, and Documentation (Weeks 7-8)
• Milestone 7: Develop the WaterTankAnalytics module using Matplotlib/Seaborn.
• Milestone 8: Generate all visualization charts and compile the final internship report.
• Resources: Data visualization libraries, word processing software.""")

    doc.add_page_break()

    # --- CHAPTER 5 ---
    add_chapter("5", "TECHNOLOGY STACK")
    
    doc.add_heading('5.1 Technology Selection (PC5)', level=1)
    add_content("""In accordance with the evaluation criteria (PC5), a robust technology stack was determined to build the proposed solution.

Programming Language: Python 3.12
Python was selected as the primary programming language due to its extensive support for data analytics, object-oriented programming, and rapid prototyping capabilities. Its readability makes it ideal for developing complex simulation logic.

Data Visualization Libraries:
• Matplotlib: Chosen for its powerful 2D plotting capabilities, allowing for the creation of detailed line charts, bar charts, and pie charts.
• Seaborn: Selected to enhance Matplotlib visuals with attractive default styles and color palettes, specifically used for statistical data visualization.

Data Manipulation:
• NumPy: Utilized for efficient numerical operations and array manipulations, particularly when generating 24-hour simulation data.
• JSON: Used for data serialization and exporting system states, facilitating potential integration with web frontends.

Development Tools:
• Standard Python logging module for tracking system operations and debugging.
• Dataclasses for structured data representation (WaterLevelReading, PumpControlAction, SystemAlert).""")

    doc.add_heading('5.2 Architecture Overview', level=1)
    add_content("""The software architecture follows a modular, object-oriented design:

1. Data Models (Dataclasses): Define the structure of WaterLevelReading, PumpControlAction, SystemAlert, and SensorReading.
2. Core Simulation Engine: The `WaterTank` class handles the generation of water usage data and the automatic execution of pump control logic. The `WaterSimulator` class orchestrates the passage of time (e.g., simulating a 24-hour cycle with specific peak usage hours).
3. Analytics Engine: The `WaterTankAnalytics` class ingests the generated data and produces graphical reports.

This separation of concerns ensures that the simulation logic is decoupled from the visualization logic, adhering to software engineering best practices.""")

    doc.add_page_break()

    # --- CHAPTER 6 ---
    add_chapter("6", "SOLUTION DEVELOPMENT")
    
    doc.add_heading('6.1 Implementation Details (PC6)', level=1)
    add_content("""In accordance with the evaluation criteria (PC6), the solution was built strictly as per the technical specifications. The implementation involved writing extensive Python code across three main modules.

Core Monitoring Logic:
The `WaterTank` class was implemented to simulate real water consumption behavior. The `take_reading()` method generates water outflow based on the time of day and tank type, with significant spikes during simulated peak hours (7-9 AM and 6-8 PM).

Automated Pump Control Algorithm:
The `_control_pump()` method was implemented to replace manual operation. It evaluates the current water level against predefined thresholds specific to the tank type:
• Pump ON Threshold: Typically 25-35% capacity. When the level drops below this, the pump state changes to ON.
• Pump OFF Threshold: Typically 80-90% capacity. When the level rises above this, the pump state changes to OFF, preventing overflow.
This logic is executed continuously, ensuring the tank never runs dry and never overflows.""")

    doc.add_heading('6.2 IoT Sensor Integration', level=1)
    add_content("""The IoT aspect of the system was implemented in the `water_tank_iot_sensors.py` module. 

Sensor Simulation:
Individual `IoTWaterLevelSensor` objects were created representing Ultrasonic, Pressure, and Float Switch sensors. These sensors track their own battery levels and apply accuracy modifiers (e.g., Ultrasonic at 95% accuracy, Float Switch at 99%). The system calculates a 'confidence' score for each reading based on battery health and temperature extremes.

Anomaly Detection:
The system continuously monitors for complex anomalies. For example, the `_detect_anomalies()` method checks if the pump state is ON but the water level is decreasing—a clear indicator of a pump malfunction or a massive pipe leak. It also detects sensor faults and low battery conditions, generating `SystemAlert` objects for maintenance teams.""")

    doc.add_heading('6.3 Data Analytics Module', level=1)
    add_content("""The `water_tank_analytics.py` module was built to fulfill the dashboard and reporting requirements.

Five distinct visualization functions were developed:
1. `generate_water_level_trend()`: Plots the 24-hour water level trend for different tank types, clearly showing the sawtooth pattern of automatic pump cycles.
2. `generate_pump_operation_analysis()`: Displays total pump runtimes and the frequency of ON/OFF cycles throughout the day.
3. `generate_water_usage_analysis()`: Shows the distribution of daily water usage and hourly consumption patterns.
4. `generate_alert_summary()`: Categorizes system warnings, such as malfunctions or sensor faults.
5. `generate_system_efficiency()`: A comprehensive KPI dashboard for facility managers.

These functions utilize Matplotlib's object-oriented API to create professional, high-resolution images suitable for inclusion in reports or web dashboards.""")

    doc.add_page_break()

    # --- CHAPTER 7 ---
    add_chapter("7", "SOLUTION TESTING AND PERFORMANCE")
    
    doc.add_heading('7.1 Testing Strategy (PC7)', level=1)
    add_content("""In accordance with the evaluation criteria (PC7), the solution was thoroughly tested to ensure reliability and fix any bugs.

Unit Testing:
Individual methods were tested to ensure logical correctness. The `_control_pump()` logic was tested with boundary conditions (0%, 25%, 90%, 100%) to verify that the pump state transitioned exactly at the defined thresholds.

Integration Testing:
The `WaterSimulator` was run for a full 24-hour cycle with multiple tank types (Residential, Commercial, Industrial) to ensure that the pump inflow rates correctly outpaced the water outflow rates, allowing the tanks to refill during peak usage.

Data Validation:
Exported JSON data was validated to ensure all timestamps were correctly formatted (ISO 8601) and numerical values (liters, percentages) were rounded to appropriate decimal places to prevent floating-point precision errors.""")

    doc.add_heading('7.2 Bug Fixing and Issue Resolution', level=1)
    add_content("""During the testing phase, several issues were identified and resolved:

Issue 1: Tank Capacity Overflow
Bug: Initially, if the pump inflow was very high, the water level could exceed the maximum capacity of the tank in a single simulation step before the pump could turn off.
Fix: Implemented a strict boundary check `self.current_level = min(self.capacity, self.current_level)` after calculating inflow, ensuring physical constraints were respected.

Issue 2: Negative Water Usage
Bug: The random generation of water usage occasionally resulted in negative values during extreme off-peak hours.
Fix: Applied the `max(0, water_usage)` function to ensure water outflow was always a positive value or zero.""")

    doc.add_heading('7.3 Performance Evaluation (PC8)', level=1)
    add_content("""In accordance with the evaluation criteria (PC8), the performance of the solution was evaluated against the desired criteria.

System Reliability:
The Python simulation successfully demonstrated 100% reliability in preventing overflows and dry tanks. The automated logic consistently engaged the pumps at the lower threshold and disengaged them at the upper threshold, maintaining a safe operational band throughout the 24-hour cycle.

Impact Assessment:
Based on the simulated data, replacing manual operation with automated threshold control eliminated all instances of tank overflow. Furthermore, by optimizing pump runtimes to occur only when necessary, the system demonstrated a significant reduction in unnecessary electricity consumption compared to systems where pumps are left running on timers. This directly addresses the problem statement's goal of improving energy efficiency and preventing water wastage.""")

    doc.add_page_break()

    # --- CHAPTER 8 ---
    add_chapter("8", "RESULTS AND VISUALIZATIONS")
    
    add_content("""This chapter presents the graphical results generated by the Water Tank System analytics module. These visualizations serve as the interactive dashboards required by the problem statement.""")
    
    doc.add_heading('8.1 Water Level Trends and Pump Operation', level=1)
    add_content("""The 24-Hour Water Level Trend chart perfectly illustrates the automated control logic. The distinct 'sawtooth' pattern shows the water level dropping due to usage until it hits the lower red dashed line (Pump ON threshold), at which point it rises sharply until it hits the upper teal dashed line (Pump OFF threshold).""")
    
    if os.path.exists('/home/ubuntu/water_level_trend.png'):
        doc.add_picture('/home/ubuntu/water_level_trend.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 1: 24-Hour Water Level Trend showing Automated Pump Cycles')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_heading('8.2 Water Usage and Alert Distribution', level=1)
    add_content("""The Pump Operation Analysis chart shows the total runtime required for different facility types, which directly correlates to electricity consumption. The Water Usage Analysis chart tracks the volumetric consumption throughout the day, highlighting peak usage periods.""")
    
    if os.path.exists('/home/ubuntu/pump_operation.png'):
        doc.add_picture('/home/ubuntu/pump_operation.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 2: Pump Runtime and Cycle Analysis')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()
    doc.add_heading('8.3 System Efficiency Dashboard', level=1)
    add_content("""The System Efficiency dashboard serves as the central hub for facility managers, providing a high-level overview of total system capacity, current fill percentage, active pumps, and critical alerts.""")
    
    if os.path.exists('/home/ubuntu/system_efficiency.png'):
        doc.add_picture('/home/ubuntu/system_efficiency.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 3: Smart Water Management System Efficiency Dashboard')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    add_content("""The Alert Summary chart categorizes system warnings, helping maintenance teams prioritize responses to sensor faults or pump malfunctions before they lead to critical shortages.""")

    if os.path.exists('/home/ubuntu/alert_summary_water.png'):
        doc.add_picture('/home/ubuntu/alert_summary_water.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 4: System Alert and Anomaly Distribution')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()

    # --- CHAPTER 9 ---
    add_chapter("9", "LEARNING EVALUATION")
    
    doc.add_heading('9.1 Technical Skill Gain (PC9)', level=1)
    add_content("""In accordance with the evaluation criteria (PC9), this internship resulted in significant technical skill gain and professional development.

1. Python Programming: Enhanced proficiency in advanced Python concepts, including Object-Oriented Programming (OOP), dataclasses, and control system simulation.
2. Data Analytics & Visualization: Mastered the use of Matplotlib and Seaborn to transform raw sensor data into professional, actionable dashboards that prove the effectiveness of the automated control logic.
3. Domain Knowledge: Acquired deep understanding of automated control systems, hysteresis in threshold logic, and IoT sensor network architectures for resource management.
4. Problem Solving: Developed critical thinking skills through the process of designing anomaly detection algorithms (e.g., identifying a broken pump by analyzing the relationship between pump state and water level delta).""")

    doc.add_heading('9.2 Conclusion', level=1)
    add_content("""The Smart Water Tank Level Monitoring and Automatic Pump Control System successfully addresses the inefficiencies and risks associated with manual water management. By leveraging IoT simulation and threshold-based control algorithms, the developed solution provides continuous real-time monitoring, completely eliminating tank overflows and preventing water shortages.

The project demonstrates that intelligent automation can significantly reduce water wastage, lower electricity costs by optimizing pump runtimes, and provide facility managers with peace of mind. The successful completion of this project fulfills all evaluation criteria and serves as a robust foundation for deploying physical IoT sensors and smart relays in residential, commercial, and industrial water infrastructure.""")

    # Save the document
    doc.save('/home/ubuntu/Internship_Report_Water_Tank.docx')
    print("Report generated successfully at /home/ubuntu/Internship_Report_Water_Tank.docx")

if __name__ == "__main__":
    create_report()
