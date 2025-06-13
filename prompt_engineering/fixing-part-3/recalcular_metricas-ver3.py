import re
import ast

LOG_IN = "metrics_2B-int8-fixed2.log"
LOG_OUT = "metrics_2B-int8-fixed3.log"

# Regex para extraer listas de colores predichos y GT
col_pred_re = re.compile(r"'colours':\s*(\[[^\]]*\])")
col_gt_re = re.compile(r"GT:.*'colours':\s*(\[[^\]]*\])")

# Regex para detectar la línea de Precisión colores
col_prec_re = re.compile(r"^Precisión colores:\s*\d+\.\d+%$")

n_balloons = 18  # número de imágenes con globos (GT)
hits_colors = 0  # aciertos en color
fixed_lines = []
new_col_prec = []

# 1) Leemos y contamos aciertos de color
with open(LOG_IN, encoding="utf-8") as fin:
    for line in fin:
        # Contar aciertos de colores sólo para imágenes con colores en el GT
        m_pred = col_pred_re.search(line)
        m_gt = col_gt_re.search(line)
        if m_pred and m_gt:
            pred_list = ast.literal_eval(m_pred.group(1))
            gt_list = ast.literal_eval(m_gt.group(1))
            # sólo considerar si hay al menos un color en el GT
            if gt_list:
                # sólo dar acierto si predicción y GT coinciden exactamente
                if set(pred_list) == set(gt_list):
                    hits_colors += 1

                    print("Acierto de colores:", pred_list, "==", gt_list)
            if not gt_list and not pred_list:
                # Si ambos están vacíos, también es un acierto
                hits_colors += 1
                print("Acierto de colores vacío:", pred_list, "==", gt_list)
        # Preparar línea "Precisión colores" para reemplazo
        if col_prec_re.match(line):
            pct = round(hits_colors / n_balloons * 100, 2)
            new_col_prec.append(f"{pct:.2f}")
            fixed_lines.append(line)
            hits_colors = 0  # Reiniciar contador para la siguiente sección
            continue

        fixed_lines.append(line)

# 2) Reemplazamos cada "Precisión colores: XX.XX%" con el valor recalculado
idx = 0
for i, ln in enumerate(fixed_lines):
    if col_prec_re.match(ln):
        fixed_lines[i] = f"Precisión colores: {new_col_prec[idx]}%\n"
        print(f"Precisión colores corregida: {new_col_prec[idx]}% en línea {i+1}")
        idx += 1

# 3) Guardamos el fichero corregido
with open(LOG_OUT, "w", encoding="utf-8") as fout:
    fout.writelines(fixed_lines)

print(f"Fichero con precisión de colores corregido: {LOG_OUT}")
print(f"Aciertos de color: {hits_colors}/{n_balloons} ({new_col_prec[0]}%)")
