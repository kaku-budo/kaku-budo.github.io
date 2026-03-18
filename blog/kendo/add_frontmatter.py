#!/usr/bin/env python3
"""
批次為 .md 檔加入 categories 和 series
使用方式：將此檔案放在 content 資料夾內，直接執行即可。
"""

import os

# 資料夾對應的分類設定
FOLDER_CONFIG = {
    "announcements":  {"categories": ["劍道"], "series": ["公告"]},
    
}

# 腳本所在資料夾（自動偵測）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def process_md_file(filepath, config):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"  [跳過] 無 front matter：{os.path.basename(filepath)}")
        return

    end = content.find("---", 3)
    if end == -1:
        print(f"  [跳過] front matter 格式錯誤：{os.path.basename(filepath)}")
        return

    front_matter = content[3:end]
    body = content[end:]

    has_categories = "categories:" in front_matter
    has_series = "series:" in front_matter

    if has_categories and has_series:
        print(f"  [已有] 略過：{os.path.basename(filepath)}")
        return

    addition = ""
    if not has_categories:
        cats = '", "'.join(config["categories"])
        addition += f'categories: ["{cats}"]\n'
    if not has_series:
        sers = '", "'.join(config["series"])
        addition += f'series: ["{sers}"]\n'

    new_content = "---" + front_matter.rstrip("\n") + "\n" + addition + body

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  [完成] {os.path.basename(filepath)}")

def main():
    print("=== 開始批次處理 ===\n")
    total = 0

    for folder_name, config in FOLDER_CONFIG.items():
        folder_path = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            print(f"[找不到] {folder_name}/ 資料夾，跳過。")
            continue

        print(f"\n📁 {folder_name}（{config['series'][0]}）")

        for sub in sorted(os.listdir(folder_path)):
            sub_path = os.path.join(folder_path, sub)
            if not os.path.isdir(sub_path) or not sub.startswith("part-"):
                continue
            print(f"  📂 {sub}")
            for filename in sorted(os.listdir(sub_path)):
                if not filename.endswith(".md"):
                    continue
                process_md_file(os.path.join(sub_path, filename), config)
                total += 1

    print(f"\n✅ 完成！共處理 {total} 個檔案。")
    input("\n按 Enter 關閉視窗...")  # 讓視窗不會立刻消失

if __name__ == "__main__":
    main()
