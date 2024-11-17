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

5. **Distribute to PyPi**
# Increment the version number
- PATCH for bug fixes (e.g., 0.1.1)
   - MINOR for new features (e.g., 0.2.0)
   - MAJOR for incompatible API changes (e.g., 1.0.0)

# Clean previous builds (optional but recommended)
```bash
rm -rf build dist *.egg-info 
```
# Upgrade setuptools and wheel (optional but good practice)
```bash
pip install --upgrade setuptools wheel
```
# Build the distribution packages
```bash
python setup.py sdist bdist_wheel
```
# Upload the New Version to PyPI
```bash
pip install --upgrade twine
```
# Upload the package to PyPI
```bash
twine upload dist/*
```
# Verify the Upload
```bash
pip install wristband
```



python3 get_token \
   --application_vanity_domain "invoexp-donato.us.wristband.dev" \
   --client_id "ploopscbu5cmzi4hndvcsyepi4" \
   --client_secret "dc0a4ba0a4e10cb670c1c95a66d11698"