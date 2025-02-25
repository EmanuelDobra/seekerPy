# Prereqs
1. Python 3.11.9 version (others might work too)
2. Create .env file in project and store OPENAI_API_KEY (if using their embeddings)
3. Have an active LLM (change endpoint if using something other than LM Studio)

# Setup (Faster, but less flexible than miniconda)
1. Create a new virtual environment `py -m venv venvName`
2. Start up the venv `.\venvName\Scripts\activate`
3. Install requirements `pip install -r .\requirements.txt`
4. In another terminal, activate app `uvicorn main:app --reload`
5. Launch LM studio with server port `1234` and any model of your choosing 

# Setup (Better)
1. https://www.anaconda.com/download/success Install miniconda (and setup global paths)
2. `conda create -n nameIt python=3.11`
3. `conda activate nameIt`
4. `pip install -r .\requirements.txt`
5. C:\Users\{{user}}\miniconda3\envs

# LLMs
The basic models used are in `ragAI\Constants`, change them if you plan to use a different one

# Playground
1. http://127.0.0.1:8000/docs

# TODO:
- [ ] Store embeddings of text we want to use, generating embeddings each time is very slow. 