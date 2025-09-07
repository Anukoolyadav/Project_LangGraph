# **Multi-Agent Doctor Appointment System**

This project is an AI-powered chatbot designed to streamline the process of managing doctor appointments at a dental clinic. It uses a multi-agent system built with LangChain to handle user requests, from checking doctor availability to booking and canceling appointments, all through a conversational interface.

## **1\. Problem Statement**

### **The Problem**

For many clinics and hospitals, managing patient appointments is a manual, time-consuming process. Administrative staff spend a significant amount of time on the phone answering repetitive questions about doctor availability, booking new appointments, and handling cancellations or rescheduling requests. This process is inefficient, prone to human error, and doesn't provide the instant, 24/7 service that patients increasingly expect.

### **Why AI Agents?**

AI agents are perfectly suited to solve this problem. They can:

* **Automate Conversations:** Handle multiple user requests simultaneously without getting tired.  
* **Understand Natural Language:** Allow patients to ask questions and make requests in their own words.  
* **Perform Tasks:** Integrate with backend systems (in this case, a CSV file acting as a database) to perform actions like checking schedules and updating records.  
* **Provide 24/7 Availability:** Offer assistance to patients outside of normal business hours.

### **The Value of Multi-Agent Collaboration**

While a single AI agent could handle this task, it might struggle to differentiate between distinct goals like providing information and taking action. A multi-agent approach provides unique value:

* **Specialization:** We can create specialized agents that are experts at a single task (e.g., one for information, one for booking). This makes them more reliable and less prone to confusion.  
* **Robustness:** By separating concerns, the system is easier to manage, debug, and scale.  
* **Intelligent Routing:** A "supervisor" agent can analyze the user's intent and intelligently route the request to the correct specialist, creating a more efficient and logical workflow.

## **2\. Project Description**

This application is a conversational AI assistant for a dental clinic. Users can interact with a chatbot to manage their appointments.

The core of the application is a multi-agent system orchestrated by **LangGraph**. The system consists of:

1. **Supervisor Agent (The Router):** This is the central coordinator. It analyzes every user message to understand the primary intent. Based on its analysis, it decides which specialized agent is best suited to handle the request. After a specialist agent completes its task, the conversation returns to the supervisor to decide the next step (e.g., wait for the user, call another agent, or end the conversation).  
2. **Information Agent (The Inquirer):** This is a specialized agent whose only job is to answer questions. It is equipped with tools to:  
   * check\_availability\_by\_doctor  
   * check\_availability\_by\_specialization  
     It cannot book or cancel appointments. This separation ensures it doesn't accidentally perform actions when the user is just asking for information.  
3. **Booking Agent (The Doer):** This agent is a specialist in taking action. Its role is to modify the appointment schedule. It has tools to:  
   * set\_appointment  
   * cancel\_appointment  
     This agent is only activated by the supervisor when the user's intent is clearly to make a change to the schedule.

This collaborative workflow ensures that user requests are handled by the most qualified agent, leading to a more accurate and efficient system.

## **3\. Tools, Libraries, and Frameworks Used**

* **Agent Framework:** **LangChain** and **LangGraph** were used to create, define, and orchestrate the multi-agent system. LangGraph, in particular, was essential for building the cyclical graph that allows the conversation to flow between the supervisor and the specialized agents.  
* **LLM Integration:** langchain-google-genai to connect with Google's Gemini models.  
* **Backend:** **FastAPI** to create a robust API endpoint that serves the agent's logic.  
* **Frontend:** **Streamlit** to quickly build an interactive and user-friendly chat interface.  
* **Data Handling:** **Pandas** for managing the doctor\_availability.csv file, which acts as a simple, file-based database.  
* **Data Validation:** **Pydantic** to enforce strict data types and formats for the inputs to our agent's tools, preventing errors.

## **4\. LLM Selection**

### **Ideal LLM: Gemini 1.5 Pro**

For a production-level version of this application, **Gemini 1.5 Pro** would be the ideal choice. Its advanced reasoning and instruction-following capabilities would make the supervisor agent exceptionally accurate at routing tasks. Its large context window would allow it to handle very long and complex conversations without losing track of details, and its strong function-calling abilities are perfect for a tool-heavy, multi-agent system.

### **Free-Tier LLM Used: Gemini 1.5 Flash**

For development and demonstration, this project uses **Gemini 1.5 Flash**. This model was chosen because:

* **Excellent Free Tier:** It is one of the most capable models available for free, providing high-quality responses without incurring costs.  
* **Speed:** As its name suggests, "Flash" is optimized for fast response times, which is crucial for a good user experience in a real-time chatbot.  
* **Strong Capabilities:** Despite being a smaller model, it has excellent instruction-following and function-calling capabilities, which are the two most critical features needed for this multi-agent system to work correctly.

## **5\. Code and Deployment**

* **GitHub Repository:**YOURGITHUBREPOSITORYLINKHERE  
* **Deployed Demo:**YOURDEPLOYEDDEMOLINKHERE(e.g.,onStreamlitCommunityCloud)

### **How to Set Up and Run the Project**

Follow these steps to run the application on your local machine.

**1\. Clone the Repository**

git clone \[YOUR GITHUB REPOSITORY LINK HERE\]  
cd \[YOUR-REPOSITORY-NAME\]

**2\. Create and Activate a Virtual Environment**

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

\# For Windows  
python \-m venv venv  
.\\venv\\Scripts\\activate

**3\. Install Dependencies**

pip install \-r requirements.txt

**4\. Add Your API Key**

* Create a new file named .env in the root of the project directory.  
* Open the .env file and add your Gemini API key like this:  
  GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE"

5\. Run the Application  
You need to run two processes in two separate terminal windows.

* **Terminal 1: Start the Backend Server**  
  uvicorn main:app \--reload \--port 8003

  This will start the FastAPI server. Leave this terminal running.  
* **Terminal 2: Start the Frontend UI**  
  streamlit run streamlit\_ui.py

  This will open the Streamlit application in your web browser. You can now interact with the chatbot\!
