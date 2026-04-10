# 🤖 Auto-GPT Installation & Email Plugin Integration (Project_3)

## 📖 Overview
This project demonstrates the installation, configuration, and testing of **Auto-GPT**, along with the integration and evaluation of the **Email Plugin**. The objective was to explore autonomous AI agent capabilities, configure external API access, and validate real-world tasks such as content generation and email automation.

## 🎯 Objectives
- Install and configure Auto-GPT locally  
- Set up OpenAI API integration  
- Run and test autonomous AI task execution  
- Install and configure Auto-GPT Email Plugin  
- Validate email sending, receiving, and replying functionalities  

## 🧰 Tech Stack
- Python  
- Auto-GPT (v0.4.6)  
- OpenAI API  
- Git & GitHub  
- Gmail SMTP / IMAP  
- VS Code / Terminal  

## ⚙️ Task 1: Auto-GPT Installation

### Repository Setup
git clone https://github.com/Significant-Gravitas/AutoGPT  
cd AutoGPT  
git checkout v0.4.6  

### Dependency Installation
pip install -r requirements.txt  

### API Configuration
Create a `.env` file and add:
openai_secret_key=<YOUR_API_KEY>  

### Execution
python3 -m autogpt  

### Configured AI Agent
- Name: LinkedinGPT  
- Goal: Generate LinkedIn post for new .NET Core role  
- Budget: $1  

### Output
- AI successfully generated a LinkedIn post  
- Saved output as `.txt` file  
- Task completed autonomously  

### Challenges Faced
- Dependency version mismatches during installation  
- OpenAI API key required active credits  
- Initial configuration issues in `.env` setup  

## 📧 Task 2: Email Plugin Integration

### Plugin Setup
git clone https://github.com/Significant-Gravitas/Auto-GPT-Plugins  

### Allowlist Configuration
ALLOWLISTED_PLUGINS=AutoGPTEmailPlugin  

### Email Configuration
EMAIL_ADDRESS=<your_email>  
EMAIL_PASSWORD=<your_app_password>  
EMAIL_SMTP_HOST=smtp.gmail.com  
EMAIL_SMTP_PORT=587  
EMAIL_IMAP_SERVER=imap.gmail.com  
EMAIL_MARK_AS_SEEN=False  
EMAIL_SIGNATURE="This was sent by Auto-GPT"  

### Email Sending Test
- Created AI agent: Email-GPT  
- Task: Send invitation email  
- Result: Email successfully sent and verified  

### Email Receiving & Reply Test
- AI agent read latest email  
- Saved email content to `.txt` file  
- Generated automated reply  
- Reply successfully delivered  

## 📊 Results
- Auto-GPT successfully installed and executed  
- OpenAI API integration configured properly  
- Email plugin enabled autonomous email operations  
- Verified end-to-end AI automation workflow  

## 🚀 Key Learnings
- Setting up autonomous AI agents using Auto-GPT  
- Integrating OpenAI API with local systems  
- Working with plugin-based AI architecture  
- Automating real-world tasks using AI agents  
- Debugging dependency and environment issues  

## 🔮 Future Improvements
- Add more Auto-GPT plugins (calendar, web browsing, file system)  
- Deploy using Docker for portability  
- Add logging and monitoring for AI agents  
- Expand automation use-cases beyond email  

## ⭐ Conclusion
This project demonstrates the practical implementation of autonomous AI agents using Auto-GPT, including task automation and email integration through plugins.
