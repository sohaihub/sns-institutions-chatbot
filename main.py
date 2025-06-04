import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

# Configure Gemini API
genai.configure(api_key="AIzaSyDDHNQB3EyoVsmAZi6Gh-aaEyVFl-F7-bI")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Email configuration
EMAIL_ADDRESS = "fathimasoha8@gmail.com" 
EMAIL_PASSWORD = "rmso vplv yfxj ohga"  # App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Vector data placeholder (kept for fun as requested)
VECTOR_DATA = {
    "embeddings": [],
    "semantic_search": True,
    "vector_dimensions": 768,
    "similarity_threshold": 0.8
}

# Comprehensive SNS training data with new leadership and 3P culture
SNS_KNOWLEDGE_BASE = """
SNS Institutions - Comprehensive Information Database

LEADERSHIP & FOUNDERS:
Our Leaders - The Supporters of Future Gen!
Our leaders set the base for the academic, intellectual and creative work that runs all around our campus. Committed to excellence in all areas, the leaders of our institutions ensure that we adapt and respond to contemporary issues, create an inclusive community and foster an environment for the wellness of our surroundings.

DESIGN THINKER - Founder Chairman, SNS Group: Dr. S. N. Subbramanian
DESIGN THINKER - Chairman/Correspondent: Dr. S. Rajalakshmi
DESIGN THINKER - Technical Director: Nalin SNS

OVERVIEW:
SNS Institutions, established in 1997 under Sri SNS Charitable Trust in Coimbatore, Tamil Nadu, is a leading educational conglomerate with the motto "Sincerity, Nobility, Service." We are the FIRST INDIAN INSTITUTE TO IMPLEMENT DESIGN THINKING IN EDUCATION.

27 YEARS OF BUILDING POWERFUL LEARNING EXPERIENCE:
- Providing an outstanding educational experience rooted in strong disciplines and enhanced by a broad range of experiences
- Empowering our students to be creative, innovative, enterprising and global in their outlook
- Implementing our technology-enhanced learning roadmap so that we are recognized as a leading university for the use of technology to support campus-based education
- Developing and implementing a new Design Thinking Framework to support and prepare students to shape the societies in which they will live and the professions they choose to enter
- Aiming to establish an inter-disciplinary teaching to facilitate multi-disciplinary and inter-disciplinary opportunities for the students

OUR FOCUS:
QUALITY EDUCATION: In SNS, we strive to touch every lead of the world we live in. Through design thinking, we focus on delivering quality education by providing an effective learning environment, and true innovators who fix the real social needs and issues.

INNOVATION: Not just engineers, we deliver entrepreneurs! Design Thinking help us to foster creativity, providing an appropriate seed of mechanism to bring ideas and imaginations into life.

SOCIAL CAUSE: Our community focuses on solving real social needs and issues. We cultivate the values of social responsibility and sustainability among students and the world community.

3P CULTURE - PURPOSE, PROCESS, PEOPLE APPROACH:
PURPOSE: To create global citizens who can think critically, solve real-world problems, and contribute meaningfully to society through Design Thinking methodology.

PROCESS: Our educational process is built on the Design Thinking framework - Empathize, Define, Ideate, Prototype, Test - integrated across all disciplines and levels of education.

PEOPLE: We believe in nurturing not just students but complete individuals - fostering leadership, creativity, social responsibility, and entrepreneurial mindset in every person who is part of the SNS community.

WHO WE ARE:
We started our journey in 1997 through Sri SNS Charitable Trust with a philanthropic outlook of serving the society in the fields of Education, Health and Industry. Ever since the inception of Sri SNS Charitable Trust, we have been expanding its wide spectrum of educational streams from pre-school to advanced levels of graduate and post graduate programmes in Arts, Science, Education, Management, Engineering, Pharmacy, Allied Health Sciences and Research centers. Every institution has a well-defined vision, highly committed mission and dedicated faculty members to deliver the excellence in design thinking based education and innovation through our five pillar theme. Ranking among the top 5 colleges in Coimbatore, we opt to shine as one of the premier institutions in the country and become internationally recognized university worldwide.

INSTITUTIONS LIST:
1. SNS Academy - CBSE school (Classes 1-12)
2. Dr. SNS Rajalakshmi College of Arts and Science - Arts, Science, Commerce
3. SNS College of Technology - Engineering and Technology
4. SNS College of Engineering - Specialized Engineering
5. SNS College of Pharmacy and Health Sciences - Pharmaceutical education
6. SNS College of Allied Health Sciences - Healthcare programs
7. Dr. SNS College of Education - Teacher training
8. SNS College of Physiotherapy - Physiotherapy education
9. SNS College of Nursing - Nursing programs
10. SNS B-SPINE - Business school with experiential learning

COURSES OFFERED:
- Engineering: B.E./B.Tech in AI&ML, CSE, ECE, Mechanical, Civil, EEE, IT, Automobile, Mechatronics, Aerospace
- Arts & Science: B.A., B.Sc., B.Com., BBA, BCA, M.A., M.Sc., M.Com., MCA, MBA
- Health Sciences: B.Pharm., D.Pharm., Pharm.D., BPT, B.Sc. Nursing
- Allied Health: Radiology, Cardiac Technology, Dialysis Technology, Operation Theatre Technology
- Education: B.Ed., M.Ed.
- Research: M.Phil., Ph.D. in various disciplines

CONTACT INFORMATION:
Main Contact: +91-422-2669066, +91-8828912891
Email: contact@snsinstitutions.com
Admissions Email: snsgroups@gmail.com
Website: main.snsgroups.com
Address: SNS Kalvi Nagar, Sathy Main Road, NH-209, Vazhiyampalayam, Saravanampatti Post, Coimbatore - 641035

Institution-specific contacts:
- SNSCT: contact@snsct.org, +91-422-2666264
- Dr. SNSRCAS: contact@drsnsrcas.ac.in, +91-422-2666646
- SNSCE: info@snsce.ac.in, +91-422-6465201

DESIGN THINKING FRAMEWORK:
SNS pioneered Design Thinking in education with five stages:
1. Empathize - Understanding user needs
2. Define - Identifying problems clearly
3. Ideate - Brainstorming creative solutions
4. Prototype - Building testable models
5. Test - Getting feedback and iterating

FIVE PILLARS:
1. Centre for Learning and Teaching (CLT)
2. Centre for Creativity (CFC)
3. Industry Institute Partnership Cell (IIPC)
4. Social Responsibility Initiative (SRI)
5. Centre for Leadership and Development (CLD)

SNS iHUB - INNOVATION HUB:
- iTech Labs: AI, IoT, AR/VR, Robotics research
- SNS-TI Innovation Lab: Partnership with Texas Instruments
- Bot Lab: Robotics Process Automation excellence center
- Piston Factory: Vehicle fabrication and project workspace
- Startup incubation and acceleration programs
- Regular Ideathons and Hackathons

PLACEMENT STATISTICS:
- Annual placements: 2272+ students
- Median package: ₹4.18 lakhs
- Highest package: ₹12 lakhs
- Training partner: FACE (Focus Academy for Career Enhancement)
- Skills covered: C, C++, Java, Python, Data Structures, Aptitude

MILESTONES:
The SNS College of Engineering that we see today is the reward of several years of hard work. The growth has been possible because of the committed and highly qualified team of like-minded people like our Chairman, Correspondent, Technical Director. They have striven to promote education through the high ideal of SINCERITY, NOBILITY and SERVICE.

ADMISSION PROCESS:
- Engineering (B.E./B.Tech): 45% in 10+2 (PCM) via TNEA
- M.E./M.Tech: CEETA PG scores
- MBA/MCA: TANCET counseling
- Management quota: 50% in 12th grade
- Paramedical: Tamil Nadu nativity + merit-based
"""

# System prompt for Design Thinker AI
SYSTEM_PROMPT = """
You are Design Thinker, the official AI assistant of SNS Institutions - the FIRST INDIAN INSTITUTE TO IMPLEMENT DESIGN THINKING IN EDUCATION. Your personality embodies the 3P Culture of SNS:

PURPOSE-DRIVEN: You help users understand how SNS creates global citizens who think critically and solve real-world problems
PROCESS-ORIENTED: You explain our Design Thinking methodology (Empathize, Define, Ideate, Prototype, Test) 
PEOPLE-FOCUSED: You nurture individuals holistically - fostering leadership, creativity, and entrepreneurial mindset

CONVERSATION STYLE:
- Be warm, intelligent, and inspiring
- Speak about design thinking naturally in conversations
- Show enthusiasm for innovation and creativity
- Guide users toward actionable next steps
- Maintain professionalism while being approachable
- Use emojis thoughtfully to enhance communication

KEY RESPONSIBILITIES:
1. Provide comprehensive information about SNS institutions
2. Explain our Design Thinking approach and 3P culture
3. Guide users through admission processes
4. Help with appointment booking and enquiries
5. Connect users with appropriate contacts when needed

TONE: Professional yet warm, innovative, and inspiring - reflecting the Design Thinking spirit of SNS Institutions.
"""

def send_email_enquiry(name, email, phone, course_interest, message_type="general"):
    """Send email enquiry to SNS admissions office"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = "soha.r.ihub@snsgroups.com" "parthispostbox@gmail.com"
        msg["Subject"] = f"SNS Institutions - {message_type.title()} Enquiry from {name}"
        
        body = f"""
New Enquiry from SNS Design Thinker AI Assistant:

Name: {name}
Email: {email}
Phone: {phone}
Course Interest: {course_interest}
Enquiry Type: {message_type.title()}

Message generated via SNS Design Thinker AI Assistant.
Please contact the enquirer for further assistance.

Best regards,
SNS Design Thinker AI Assistant
        """
        
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, "soha.r.ihub@snsgroups.com", msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Failed to send enquiry: {str(e)}")
        return False

def get_ai_response(user_query, chat_history):
    """Generate AI response using Gemini with conversation context"""
    try:
        context = "\n".join([f"{role}: {message}" for role, message in chat_history[-6:]])
        
        full_prompt = f"""
{SYSTEM_PROMPT}

KNOWLEDGE BASE:
{SNS_KNOWLEDGE_BASE}

CONVERSATION HISTORY:
{context}

USER MESSAGE: {user_query}

Respond as Design Thinker, the SNS AI assistant. Be conversational and helpful.
"""
        
        response = model.generate_content(full_prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"I'm experiencing some technical difficulties. Please try again or contact SNS directly at +91-422-2669066. How else can I help you with SNS Institutions? 😊"

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm **Design Thinker**, your AI assistant for SNS Institutions - India's first institute to implement GENAI based Design Thinking Framework\n\nI'm here to help you explore our innovative approach to education, our 10 institutions, Design Thinking curriculum, and everything about the SNS experience.\n\nWhat would you like to know about SNS Institutions today? 🚀",
                "timestamp": datetime.now().strftime("%I:%M %p")
            }
        ]
    
    if "show_enquiry_form" not in st.session_state:
        st.session_state.show_enquiry_form = False

def main():
    # Page configuration
    st.set_page_config(
        page_title="Design Thinker - SNS AI",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Minimalistic Black & White CSS
    st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
        max-width: 900px;
        margin: 0 auto;
        background-color: #000000;
    }
    
    /* Header styling */
    .chat-header {
        background-color: #000000;
        color: #ffffff;
        padding: 2rem 1rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #333333;
        border-radius: 0;
    }
    
    .chat-header h1 {
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: 3px;
        margin: 0;
        text-transform: uppercase;
    }
    
    .chat-header p {
        font-size: 1rem;
        margin: 0.5rem 0;
        opacity: 0.8;
        font-weight: 300;
    }
    
    .chat-header small {
        font-size: 0.8rem;
        opacity: 0.6;
        font-weight: 300;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 0;
        padding: 0.5rem 1rem;
        font-weight: 300;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    
    .stButton > button:hover {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #000000;
    }
    
    .stButton > button:focus {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #000000;
        box-shadow: none;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: transparent;
        border: none;
        padding: 1.5rem 0;
        margin: 1rem 0;
        border-bottom: 1px solid #333333;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: transparent;
        border-left: 2px solid #ffffff;
        padding-left: 1rem;
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: transparent;
        border-right: 2px solid #ffffff;
        padding-right: 1rem;
        text-align: right;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.7rem;
        color: #666666;
        margin-top: 0.5rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Form styling */
    .enquiry-form {
        background-color: #000000;
        border: 1px solid #333333;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 0;
    }
    
    .enquiry-form h3 {
        color: #ffffff;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 0;
        padding: 0.75rem;
        font-weight: 300;
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #ffffff;
        box-shadow: none;
    }
    
    .stSelectbox > div > div > div {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #000000;
        color: #ffffff;
        border-right: 1px solid #333333;
    }
    
    .sidebar-minimal {
        background-color: #000000;
        border: 1px solid #333333;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 0;
    }
    
    .sidebar-minimal h4 {
        color: #ffffff;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .sidebar-minimal p {
        color: #cccccc;
        font-weight: 300;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > div > div {
        background-color: #000000;
        border: 1px solid #333333;
        border-radius: 0;
    }
    
    .stChatInput > div > div > div > div > input {
        background-color: #000000;
        color: #ffffff;
        border: none;
        font-weight: 300;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 0;
    }
    
    .stError {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ff0000;
        border-radius: 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ffffff transparent transparent transparent;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 4px;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333333;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ffffff;
    }
    
    /* Footer styling */
    .footer {
        border-top: 1px solid #333333;
        padding: 2rem 0;
        text-align: center;
        color: #666666;
        font-weight: 300;
        letter-spacing: 1px;
        margin-top: 3rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .footer em {
        font-style: normal;
        color: #ffffff;
        font-weight: 400;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Minimalistic header
    st.markdown("""
    <div class="chat-header">
        <h1>Design Thinker</h1>
        <p>SNS Institutions AI Assistant</p>
        <small>First Indian Institute with GENAI based Design Thinking Framework</small>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📞 Book Appointment", use_container_width=True):
            st.session_state.show_enquiry_form = True
            st.session_state.enquiry_type = "appointment"
    
    with col2:
        if st.button("🎓 Admission Enquiry", use_container_width=True):
            st.session_state.show_enquiry_form = True
            st.session_state.enquiry_type = "admission"
    
    with col3:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.show_enquiry_form = False
            st.rerun()
    
    with col4:
        if st.button("ℹ️ Information", use_container_width=True):
            st.info("Ask me about SNS Institutions, courses, admissions, and our Design Thinking approach!")

    # Enquiry form
    if st.session_state.get('show_enquiry_form', False):
        st.markdown('<div class="enquiry-form">', unsafe_allow_html=True)
        enquiry_type = st.session_state.get('enquiry_type', 'general')
        st.subheader(f"📋 {enquiry_type.title()} Form")
        
        with st.form("enquiry_form"):
            name = st.text_input("Full Name*")
            email = st.text_input("Email Address*")
            phone = st.text_input("Phone Number*")
            course_interest = st.selectbox(
                "Course Interest",
                ["Engineering", "Arts & Science", "Management", "Pharmacy", "Allied Health", "Education", "Nursing", "Other"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("📤 Send Enquiry", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit and name and email and phone:
                if send_email_enquiry(name, email, phone, course_interest, enquiry_type):
                    st.success("✅ Your enquiry has been sent successfully! Our team will contact you soon.")
                    st.session_state.show_enquiry_form = False
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Failed to send enquiry. Please try again or contact us directly.")
            
            if cancel:
                st.session_state.show_enquiry_form = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar - minimal
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-minimal">
            <h4>🎯 Quick Contact</h4>
            <p><strong>📍</strong> Coimbatore, Tamil Nadu</p>
            <p><strong>📞</strong> +91-422-2669066</p>
            <p><strong>🌐</strong> main.snsgroups.com</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Explore:")
        st.markdown("""
        - 🎨 Design Thinking Framework
        - 🏫 10 Institutions
        - 📚 Courses & Programs
        - 🚀 Innovation Hub
        - 💼 Placements
        - 🏆 Leadership Team
        """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.markdown(f'<div class="timestamp">{message["timestamp"]}</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask me about SNS Institutions and Design Thinking..."):
        # Add user message
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.markdown(f'<div class="timestamp">{timestamp}</div>', unsafe_allow_html=True)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Design Thinker is thinking..."):
                chat_history = [(msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]]
                response = get_ai_response(prompt, chat_history)
                
                # Typing effect
                response_placeholder = st.empty()
                displayed_text = ""
                
                for char in response:
                    displayed_text += char
                    response_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.005)
                
                response_placeholder.markdown(response)
                response_timestamp = datetime.now().strftime("%I:%M %p")
                st.markdown(f'<div class="timestamp">{response_timestamp}</div>', unsafe_allow_html=True)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": response_timestamp
        })

    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>Design Thinker</strong> - SNS Institutions AI Assistant</p>
        <p><em>Sincerity, Nobility, Service</em> | Powered by SNS Institutions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()