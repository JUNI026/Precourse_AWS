def parse_line(line):
    line = line.strip()
    if line == "":
        return None

    parts = line.split()
    if len(parts) < 9:
        return None

    try:
        status = int(parts[8])
    except ValueError:
        return None

    return {
        "ip": parts[0],
        "time": parts[3].lstrip("[") + " " + parts[4].rstrip("]"),
        "method": parts[5].lstrip('"'),
        "url": parts[6],
        "status": status,
    }

entries = []
skipped = 0
total_lines = 0

with open("access.log", "r", encoding="utf-8") as f:
    for raw in f:
        total_lines += 1
        entry = parse_line(raw)

        if entry is None:
            skipped += 1
        else:
            entries.append(entry)

status_counts = {}
hourly_counts = {}
error_counts = {}
ip_counts = {}

for entry in entries:
    code = str(entry["status"])
    status_counts[code] = status_counts.get(code, 0) + 1

    hour = entry["time"].split(":")[1]
    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1

    ip = entry["ip"]
    ip_counts[ip] = ip_counts.get(ip, 0) + 1

    if entry["status"] >= 400:
        url = entry["url"]
        error_counts[url] = error_counts.get(url, 0) + 1

top_error_urls = [
    list(item)
    for item in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
]

top_ips = sorted(
    ip_counts.items(),
    key=lambda x: x[1],
    reverse=True
)[:5]


import json

results = {
    "status_counts": status_counts,
    "hourly_counts": hourly_counts,
    "top_error_urls": top_error_urls,
    "top_ips": top_ips
}

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("results.json 저장 완료")
