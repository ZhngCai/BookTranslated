#!/usr/bin/env python3
"""合并翻译后的 Markdown 并生成中文 PDF（通过 headless Chrome）。"""
import os
import re
import shutil
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(BASE, "translated", "parts")
IMAGES = os.path.join(BASE, "extract", "images")
BUILD = os.path.join(BASE, "build")
os.makedirs(os.path.join(BUILD, "images"), exist_ok=True)

# 拷贝引用的图片
for fn in sorted(os.listdir(IMAGES)):
    if fn.endswith(".png") and fn != "p001_0.png":  # 封面原图不用
        shutil.copy(os.path.join(IMAGES, fn), os.path.join(BUILD, "images", fn))

order = [
    "00_front.md", "01_preface_1.md", "02_ch01_1.md", "03_ch02.md",
    "04_ch03.md", "05_ch04_1.md", "06_ch04_2.md", "07_ch04_3.md",
    "08_ch05.md", "09_ch06.md", "10_ch07.md", "11_ch08.md",
    "12_ch09.md", "13_ch10.md", "14_ch11.md", "15_ch12.md",
    "16_ch13.md", "17_ch14.md", "18_ch15.md", "19_epilogue.md",
    "20_glossary.md", "21_references.md",
]

full_md = []
for name in order:
    path = os.path.join(PARTS, name)
    with open(path, encoding="utf-8") as f:
        full_md.append(f.read())

md_text = "\n\n".join(full_md)

# 页标题拆分：使每个 part 从新页开始（在 markdown 层面标记）
md_text = md_text.replace("\n# 第 ", "\n<div class='page-break'></div>\n\n# 第 ")
md_text = md_text.replace("\n# 前言", "\n<div class='page-break'></div>\n\n# 前言")
md_text = md_text.replace("\n# 后记：展望未来", "\n<div class='page-break'></div>\n\n# 后记：展望未来")
md_text = md_text.replace("\n# 多智能体系统术语表", "\n<div class='page-break'></div>\n\n# 多智能体系统术语表")
md_text = md_text.replace("\n# 参考文献", "\n<div class='page-break'></div>\n\n# 参考文献")
md_text = md_text.replace("\n# 目录", "\n<div class='page-break'></div>\n\n# 目录")

html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
)

css = """
@page { size: A4; margin: 20mm 18mm; }
* { box-sizing: border-box; }
body {
  font-family: "PingFang SC", "Songti SC", "STSong", "Noto Sans CJK SC", sans-serif;
  font-size: 10.5pt; line-height: 1.75; color: #1a1a1a;
  max-width: 100%; margin: 0 auto; padding: 0;
}
h1 { font-size: 20pt; margin: 1.2em 0 0.6em; color: #111;
     border-bottom: 2px solid #333; padding-bottom: 6px; }
h2 { font-size: 15pt; margin: 1.1em 0 0.5em; color: #1a1a1a; }
h3 { font-size: 12.5pt; margin: 1em 0 0.4em; color: #222; }
h4 { font-size: 11pt; margin: 0.9em 0 0.3em; color: #333; }
p { margin: 0.5em 0; text-align: justify; }
ul, ol { margin: 0.4em 0 0.6em; padding-left: 1.6em; }
li { margin: 0.15em 0; }
code { font-family: "SF Mono", Menlo, Consolas, monospace;
       background: #f4f4f4; padding: 1px 4px; border-radius: 3px;
       font-size: 9pt; }
pre { background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px;
      padding: 10px 12px; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.5pt; line-height: 1.45; }
blockquote { margin: 0.6em 0; padding: 0.5em 1em;
             border-left: 4px solid #888; background: #fafafa; color: #444; }
blockquote p { margin: 0.3em 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0;
        font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #ccc; padding: 5px 8px; text-align: left;
         vertical-align: top; }
th { background: #efefef; font-weight: 600; }
img { max-width: 100%; height: auto; display: block;
      margin: 0.8em auto; page-break-inside: avoid; }
em { font-style: italic; }
.page-break { page-break-after: always; }
.figure { text-align: center; margin: 1em 0; }
.figure img { display: block; margin: 0 auto 0.4em; }
.figure .caption { font-size: 9pt; color: #555; text-align: center; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em 0; }
strong { font-weight: 600; }
"""

html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>多智能体系统设计：AI 智能体的原理、模式与实现（中文版）</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_path = os.path.join(BUILD, "book.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_doc)

print("HTML 生成完成:", html_path)
print("字符数:", len(html_doc))
