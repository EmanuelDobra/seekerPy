# Prereqs
1. Python 3.11.9 version (others might work too)
2. Create .env file in project and store OPENAI_API_KEY
3. Have an active LLM (change endpoint if using something other than LM Studio)

# Setup
1. Create a new virtual environment `py -m venv venvName`
2. Start up the venv `.\venvName\Scripts\activate`
3. Install requirements `pip install -r .\requirements.txt`
4. In another terminal, activate app `uvicorn main:app --reload`
5. Launch LM studio with server port `1234` and any model of your choosing 

# Testing
1. Check http://127.0.0.1:8000/docs and try out endpoints you want to use