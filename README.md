# wristband-python

## Setup Instructions

1. **Create a Virtual Environment**

   To keep your project's dependencies isolated, it's recommended to use a virtual environment. You can create one using the following command:
   ```bash
   python -m venv .venv
   ```

2.  **Activate the Virtual Environment**

Activate the virtual environment to ensure that any packages you install are confined to this environment.

   - On Windows:
   ```bash
   .venv\Scripts\activate
   ```

   - On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

3.	**Install the Dependencies**

With the virtual environment activated, install all required Python packages using:
```bash
pip install -r requirements.txt
```


4.  **Configure Environment Variables**

Copy the example environment file and fill in your specific details:
```bash
cp .env.example .env
```

Open the .env file in a text editor and replace the placeholder values with your actual Wristband credentials

Example .env file:
```ini

```