import re

LOG_IN = "metrics_0.5B-int8-fixed.log"
LOG_OUT = "metrics_0.5-int8-fixed2.log"

# Expresiones regulares
line_re = re.compile(
    r"^\[(?P<img>.+?)\].*'answer':\s*'(?P<ans>[^']*)'.*'found':\s*(?P<resp>True|False).*"
    r"GT: \{[^}]*'found':\s*(?P<gt>True|False)"
)
found_re = re.compile(r"'found':\s*(True|False)")
det_re = re.compile(r"^Precisión detección:\s*\d+\.\d+%$")

total_imgs = 18
hits_before = 0
hits_after = 0
fixed_lines = []
new_precision = []

# 1) Leemos y procesamos línea a línea
with open(LOG_IN, "r", encoding="utf-8") as fin:
    for line in fin:
        # Si es la línea de “Precisión detección”…
        if det_re.match(line):
            # recalculamos usando hits_after
            p = hits_after / total_imgs * 100
            new_precision.append(f"{p:.2f}")
            hits_after = 0
            fixed_lines.append(line)
            continue

        m = line_re.match(line)
        if not m:
            fixed_lines.append(line)
            continue

        # Extraemos los campos
        ans_text = m.group("ans").strip().lower()
        resp_found = m.group("resp") == "True"
        gt_found = m.group("gt") == "True"

        # Si la respuesta empieza por “no”, forzamos found=False
        if ans_text.startswith("no"):
            resp_found = False

        # Conteo de aciertos antes de corregir GT
        if resp_found == gt_found:
            hits_before += 1

        # Reconstruimos la línea si queremos cambiar el GT (opcional)
        # Aquí no hacemos nada especial con imágenes target, así que lo omitimos

        # Conteo de aciertos después
        if resp_found == gt_found:
            hits_after += 1

        # Finalmente guardamos la línea original (o modificada si tocase)
        fixed_lines.append(line)

# 2) Sustituimos in-place cada “Precisión detección: XX.XX%” con los nuevos valores
idx_p = 0
for i, ln in enumerate(fixed_lines):
    if det_re.match(ln):
        fixed_lines[i] = f"Precisión detección: {new_precision[idx_p]}%\n"
        print(f"Reemplazado en línea {i+1}: {new_precision[idx_p]}%")
        idx_p += 1

# 3) Guardamos el fichero corregido
with open(LOG_OUT, "w", encoding="utf-8") as fout:
    fout.writelines(fixed_lines)

print(f"Fichero final guardado como {LOG_OUT}")
print(f"Precisión antes:  {hits_before/total_imgs*100:.2f}%")
print(f"Precisión después: {hits_after/total_imgs*100:.2f}%")
