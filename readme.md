                                                                  CleverQ - Multi-Model AI Q&A System
CleverQ is an AI-powered question-answering web application that solves the problem of students switching between multiple platforms to find accurate answers. 
It uses a multi-model fusion approach (Groq + Gemini) to deliver fast, reliable, and context-aware responses in one place.


1. Problem Students often:
   a.Search across multiple platforms (Google, ChatGPT, notes, etc.)
   b. Get incomplete or inconsistent answers
   c. Waste time verifying information

CleverQ solves this by combining multiple AI responses into a single refined answer

2. Solution:
  Groq → Fast responses
  Gimini → Accurate and detailed answers
  Fusion → Combines both for better results

Result: Faster, more accurate, and complete answers.

3.Features of CelverQ
  Multi-model AI (Groq + Gemini)
  Answer fusion system
  Fast and responsive UI (Streamlit)
  Chat-based interface
  Secure API handling
  Optional chat history

4.Tech used:

- Python
- Streamlit
- LangChain
- Google Gemini API
- Groq API
- python-dotenv


5.Project Structure

CleverQ/
│── app.py
│── requirements.txt
│── README.md
│── .env (not included)


6. Installation

a. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate

b. Install dependencies:
   pip install -r requirements.txt

c. Create .env file:
   GEMINI_API_KEY=your_key
   GROQ_API_KEY=your_key

d. Run app:
   streamlit run app.py



7. Deployment

a. Push project to GitHub
b. Go to https://share.streamlit.io
c. Deploy your repo
d. Add API keys in Secrets


8. Security

Do not upload .env file
Keep API keys private


9. Comparison

a. Groq:

- Very fast
- Less detailed

b. Gemini:

- More accurate
- Slower

c.Fusion:

- Combines both
- Better overall performance




10.Use Cases

- Students
- Developers
- Learning and research
- Assignment help

---

11.Future Improvements

- Answer ranking
- Confidence score
- Memory system
- Web search integration
- UI improvements


Author
Saloni Tiwari
Computer Science (AI) Student

---
