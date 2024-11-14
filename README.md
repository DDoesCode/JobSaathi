To set up this project and install the required dependencies, follow these steps:

1. Activate the Virtual Environment:

First, activate the virtual environment located in the .venv folder.
On Windows, open your terminal or command prompt and run:
bash
Copy code
.venv\Scripts\activate

2. Install Dependencies:

Once the virtual environment is activated, install the required packages by running:
bash
Copy code
pip install -r requirements.txt
Verify Installation:

After installation, you can check if all packages are installed by running:
bash
Copy code
pip freeze
This command should list all the packages specified in requirements.txt.

3. Run the Application:

With everything set up, you can start the application by running:

Copy code
python app.py
This should start your Flask (or similar framework) server if app.py is configured as the entry point.
