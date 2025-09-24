import json

# 读取原 JSON 文件
input_path = r"./cases/random.json"
output_path = r"./cases/random_format.json"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for idx, item in enumerate(data, start=1):
    item["id"] = f"random-{idx:03d}"  # 格式为 random-001, random-002 ...

json_lines = [json.dumps(item, ensure_ascii=False) for item in data]
json_str = "[\n" + ",\n".join(json_lines) + "\n]"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(json_str)

print(f"processed {len(data)} records, output file: {output_path}")
