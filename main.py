import requests
import csv
from datetime import datetime
from pathlib import Path

def fetch_quote():
    response = requests.get("https://zenquotes.io/api/today")
    data = response.json()[0]
    return data["q"], data["a"]  # 명언, 저자

def update_readme(quote, author):
    readme = Path("README.md")
    content = readme.read_text(encoding="utf-8")

    new_section = f"## 🌅 오늘의 명언\n> {quote}\n>\n> — {author}\n"

    # 기존 명언 섹션이 있으면 교체, 없으면 맨 앞에 추가
    if "## 🌅 오늘의 명언" in content:
        start = content.index("## 🌅 오늘의 명언")
        end = content.find("\n## ", start + 1)
        content = content[:start] + new_section + (content[end:] if end != -1 else "")
    else:
        content = new_section + "\n" + content

    readme.write_text(content, encoding="utf-8")

def save_to_csv(quote, author):
    file = Path("quotes.csv")
    is_new = not file.exists()

    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["date", "quote", "author"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), quote, author])

if __name__ == "__main__":
    quote, author = fetch_quote()
    update_readme(quote, author)
    save_to_csv(quote, author)
    print(f"✅ 업데이트 완료: {author} — {quote}")
