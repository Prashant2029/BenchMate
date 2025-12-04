import requests
import json
from fpdf import FPDF

BASE_URL = "http://localhost:8000/api"

def create_dummy_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a dummy PDF content for testing.", ln=1, align="C")
    pdf.cell(200, 10, txt="It contains some text about Python and Django.", ln=2, align="C")
    pdf.output("dummy.pdf")

def run_verification():
    # 1. Register
    print("1. Registering user...")
    reg_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        resp = requests.post(f"{BASE_URL}/auth/register/", json=reg_data)
        if resp.status_code == 201:
            print("   Success!")
        elif resp.status_code == 400 and "username" in resp.json() and "already exists" in str(resp.json()):
             print("   User already exists, proceeding...")
        else:
            print(f"   Failed: {resp.status_code} {resp.text}")
            return
    except Exception as e:
        print(f"   Failed to connect: {e}")
        return

    # 2. Login
    print("2. Logging in...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    resp = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if resp.status_code != 200:
        print(f"   Failed: {resp.status_code} {resp.text}")
        return
    token = resp.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print("   Success! Token received.")

    # 3. Check Profile
    print("3. Checking Profile...")
    resp = requests.get(f"{BASE_URL}/gamification/profile/", headers=headers)
    if resp.status_code != 200:
        print(f"   Failed: {resp.status_code} {resp.text}")
        return
    profile = resp.json()
    print(f"   XP: {profile['xp']}, Rank: {profile['rank']}")
    initial_xp = profile['xp']

    # 4. Upload PDF
    print("4. Uploading PDF...")
    create_dummy_pdf()
    files = {'file': open('dummy.pdf', 'rb')}
    resp = requests.post(f"{BASE_URL}/core/upload/", headers=headers, files=files)
    if resp.status_code != 201:
        print(f"   Failed: {resp.status_code} {resp.text}")
        return
    pdf_id = resp.json()['pdf_id']
    print(f"   Success! PDF ID: {pdf_id}")

    # 5. Generate Quiz
    print("5. Generating Quiz...")
    quiz_data = {"pdf_id": pdf_id, "num_questions": 1}
    resp = requests.post(f"{BASE_URL}/core/generate/quiz/", headers=headers, json=quiz_data)
    if resp.status_code != 200:
        print(f"   Failed: {resp.status_code} {resp.text}")
        # Don't return, maybe API key issue, but let's try to submit quiz anyway
    else:
        print("   Success! Quiz generated.")

    # 6. Submit Quiz
    print("6. Submitting Quiz...")
    submit_data = {"score": 1, "total_questions": 1}
    resp = requests.post(f"{BASE_URL}/core/submit/quiz/", headers=headers, json=submit_data)
    if resp.status_code != 200:
        print(f"   Failed: {resp.status_code} {resp.text}")
        return
    print("   Success! Quiz submitted.")

    # 7. Check Profile Again
    print("7. Checking Profile Again...")
    resp = requests.get(f"{BASE_URL}/gamification/profile/", headers=headers)
    profile = resp.json()
    print(f"   XP: {profile['xp']}, Rank: {profile['rank']}")
    
    if profile['xp'] > initial_xp:
        print("   Verification SUCCESS: XP increased!")
    else:
        print("   Verification FAILED: XP did not increase.")

if __name__ == "__main__":
    run_verification()
