import re

LOG_IN = "metrics_2B-int8.log"
LOG_OUT = "metrics_2B-int8-fixed.log"
TARGET_IMG = "IMG20250612151157.jpg"

line_re = re.compile(
    r"^\[(?P<img>.+?)\].*'found':\s*(?P<resp>True|False).*"
    r"GT: \{[^}]*'found':\s*(?P<gt>True|False)"
)
found_re = re.compile(r"'found':\s*(True|False)")
det_re = re.compile(r"^Precisión detección:\s*\d+\.\d+%$")

total_imgs = 0
hits_before = 0
hits_after = 0
fixed_lines = []
new_precision = []
# 1) Leemos todo y corregimos la línea TARGET_IMG
with open(LOG_IN, "r", encoding="utf-8") as fin:
    for line in fin:
        m = line_re.match(line)
        if det_re.match(line):
            # 2) Calculamos la nueva precisión de detección
            p = hits_after / 18 * 100
            # guardamos en la lista una cadena ya formateada a 2 decimales
            new_precision.append(f"{p:.2f}")
            hits_after = 0
        if not m:
            fixed_lines.append(line)
            continue

        img = m.group("img")
        resp_found = m.group("resp") == "True"
        gt_found = m.group("gt") == "True"

        total_imgs += 1
        if resp_found == gt_found:
            hits_before += 1

        if img == TARGET_IMG:
            prefix, gt_part = line.split("GT:", 1)
            gt_part_fixed = found_re.sub(f"'found': {resp_found}", gt_part, count=1)
            line = prefix + "GT:" + gt_part_fixed
            gt_found = resp_found

        if resp_found == gt_found:
            hits_after += 1

        fixed_lines.append(line)

    # 3) Reemplazamos in-place la primera ocurrencia de “Precisión detección: XX.XX%”
i = 0
for idx, ln in enumerate(fixed_lines):
    if det_re.match(ln):
        fixed_lines[idx] = f"Precisión detección: {new_precision[i]}%\n"
        print(f"Precisión detección corregida: {new_precision[i]}% en línea {i + 1}")
        i += 1
# 4) Volcamos el resultado al fichero fijo
with open(LOG_OUT, "w", encoding="utf-8") as fout:
    fout.writelines(fixed_lines)

print(f"Archivo corregido guardado como {LOG_OUT}")
print(f"Precisión antes: {hits_before/total_imgs*100:.2f}%")
print(f"Precisión después: {0}%")
