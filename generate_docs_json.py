import os
import json

def scan_directory(path):
    result = []
    for entry in os.scandir(path):
        if entry.is_dir():
            result.append({
                "type": "folder",
                "name": entry.name,
                "children": scan_directory(entry.path)
            })
        elif entry.name.endswith('.md'):
            result.append({
                "type": "file",
                "name": entry.name.replace('.md', ''),
                "path": entry.path.replace('\\', '/')
            })
    return result

docs = scan_directory('docs')
with open('docs.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, indent=2, ensure_ascii=False)