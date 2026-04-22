import urllib.request
import json
import base64
import os

token = input("GitHub Personal Access Token: ")
username = "emirarda-hub"
repo = "mug-detection"
branch = "main"

headers = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json"
}

project_path = "/home/user/persistent/ai_project1/mug-cup-object-detection"

files_to_push = []
for root, dirs, files in os.walk(project_path):
    dirs[:] = [d for d in dirs if d not in ['data', 'sessions', '.venv', '.venv_backup', '__pycache__', '.idea', '.git']]
    for file in files:
        fullpath = os.path.join(root, file)
        relpath = os.path.relpath(fullpath, project_path)
        size = os.path.getsize(fullpath)
        if size < 5 * 1024 * 1024:  # 5MB altı
            files_to_push.append(relpath)
        else:
            print(f"⚠️ Çok büyük, atlanıyor ({size//1024}KB): {relpath}")

print(f"\nToplam {len(files_to_push)} dosya push edilecek")
confirm = input("Devam? (y/n): ")
if confirm != 'y':
    exit()

for filename in files_to_push:
    filepath = os.path.join(project_path, filename)
    print(f"📤 Push ediliyor: {filename}")
    with open(filepath, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{filename}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req)
        sha = json.loads(res.read())["sha"]
    except:
        sha = None
    
    data = {"message": f"Add {filename}", "content": content, "branch": branch}
    if sha:
        data["sha"] = sha
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="PUT")
    urllib.request.urlopen(req)
    print(f"✅ {filename}")

print("Tamamlandı!")
