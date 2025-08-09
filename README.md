### **DEEP SEARCH AGENT**


### **First-Time Setup**

The following code is used to set up your project's virtual environment. This keeps all your project's dependencies separate from other Python projects.

#### Create a UV virtual environment

This command uses the **`uv`** tool to create a virtual environment in a folder named **`venv`** for your project.

```
uv venv project_name
```

#### Activate the virtual environment

To start using the virtual environment, you need to activate it. The command you use depends on your operating system.

**On macOS and Linux:**

```
source venv/bin/activate
```

**On Windows:**

```
.\venv\Scripts\activate
```

-----

### **Installation**

After activating your virtual environment, you'll need to set up your API keys and install the necessary libraries.

#### Set up a `.env` file

This code block shows the content you'll put into a file named **`.env`** to securely store your API keys.

```
GEMINI_API_KEY="your_gemini_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

#### Install the required libraries

This command uses the **`uv`** tool to install all the Python libraries the project needs to run.

```
uv pip install python-dotenv tavily-python openai agents-ai
```

-----

### **How to Run the Agent**

Once everything is set up and installed, this is the command you'll use to start the program.

#### Run the agent script

This command executes the Python script from your terminal. Be sure to replace **`your_script_name.py`** with the actual name of your file.
here mine file name is main.py
```

uv run main.py #run on terminal
```

-----


I hope this helps you get your deep search agent up and running\! Let me know if you have any other questions.
