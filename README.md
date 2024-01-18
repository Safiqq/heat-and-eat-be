# Tim AADA

## Anggota Tim

- Hilmi Baskara Radanto (Hustler)
- Ceavin Rufus De Prayer Purba (Hacker)
- Syafiq Ziyadul Arifin (Hacker)
- Carissa Tabina Rianda (Hipster)

## How to Use
0. Place the **serviceaccount.json** file in the project directory. You can obtain this file from your GCP account under the IAM & Admin section.
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install required packages: `pip install -r requirements.txt`
4. Run the application: `python3 app/main.py`

#### Additional
1. Linting: `pylint app/*.py app/auth/*.py app/routes/*.py app/schemas/*.py`
2. Auto-formatting:`black app/*.py app/auth/*.py app/routes/*.py app/schemas/*.py`