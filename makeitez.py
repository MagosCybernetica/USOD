import re
import csv
import io

data = """USOD10K_Base/TE/ (): 0.0203 mae || 0.9203 max-fm || 0.9044 mean-fm || 0.9653 max-Emeasure || 0.9600 mean-Emeasure || 0.9204 S-measure || 0.9123 AP || 0.9694 AUC.
USOD10K_Base/VAL/ (): 0.0235 mae || 0.9150 max-fm || 0.8988 mean-fm || 0.9601 max-Emeasure || 0.9547 mean-Emeasure || 0.9161 S-measure || 0.9095 AP || 0.9677 AUC.
USOD10K_DF/TE/ (): 0.0205 mae || 0.9192 max-fm || 0.9033 mean-fm || 0.9646 max-Emeasure || 0.9592 mean-Emeasure || 0.9200 S-measure || 0.9100 AP || 0.9689 AUC.
USOD10K_DF/VAL/ (): 0.0235 mae || 0.9150 max-fm || 0.8988 mean-fm || 0.9601 max-Emeasure || 0.9547 mean-Emeasure || 0.9161 S-measure || 0.9095 AP || 0.9677 AUC.
USOD10K_FFA/TE (): 0.0203 mae || 0.9203 max-fm || 0.9044 mean-fm || 0.9653 max-Emeasure || 0.9600 mean-Emeasure || 0.9204 S-measure || 0.9123 AP || 0.9694 AUC.
USOD10K_FFA/VAL/ (): 0.0234 mae || 0.9155 max-fm || 0.8994 mean-fm || 0.9604 max-Emeasure || 0.9551 mean-Emeasure || 0.9170 S-measure || 0.9106 AP || 0.9683 AUC.
USOD10K_U_Shape/TE/ (): 0.0240 mae || 0.9089 max-fm || 0.8883 mean-fm || 0.9573 max-Emeasure || 0.9511 mean-Emeasure || 0.9098 S-measure || 0.9016 AP || 0.9650 AUC.
USOD10K_U_Shape/VAL/ (): 0.0271 mae || 0.9047 max-fm || 0.8836 mean-fm || 0.9537 max-Emeasure || 0.9473 mean-Emeasure || 0.9080 S-measure || 0.9005 AP || 0.9654 AUC.
USOD10K_WWPF/TE (): 0.0259 mae || 0.9035 max-fm || 0.8841 mean-fm || 0.9556 max-Emeasure || 0.9499 mean-Emeasure || 0.9061 S-measure || 0.8918 AP || 0.9627 AUC.
USOD10K_WWPF/VAL/ (): 0.0267 mae || 0.9014 max-fm || 0.8824 mean-fm || 0.9516 max-Emeasure || 0.9461 mean-Emeasure || 0.9046 S-measure || 0.8913 AP || 0.9631 AUC."""

rows = []
for line in data.strip().splitlines():
    line = line.strip()
    if not line:
        continue

    name = line.split("()")[0].strip()
    metrics_str = re.sub(r"^.*?\(\)\s*:\s*", "", line)

    metrics = {}
    for part in metrics_str.split("||"):
        part = part.strip().rstrip(".")
        m = re.match(r"([0-9.]+)\s+(\S+)", part)
        if m:
            metrics[m.group(2)] = float(m.group(1))

    rows.append({"name": name, "metrics": metrics})

all_metrics = list(rows[0]["metrics"].keys())
all_names = [r["name"] for r in rows]

output = io.StringIO()
writer = csv.writer(output)
writer.writerow(["metric"] + all_names)
for metric in all_metrics:
    writer.writerow([metric] + [r["metrics"].get(metric, "") for r in rows])

csv_text = output.getvalue()
print(csv_text)

with open("metrics_transposed.csv", "w", newline="") as f:
    f.write(csv_text)

print("Saved to metrics_transposed.csv")
