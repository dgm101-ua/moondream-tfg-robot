import re
import matplotlib.pyplot as plt

# Regex para extraer las métricas
summary_re = re.compile(r"^Resumen para prompt '(.+)':")
lat_re = re.compile(r"Latencia media:\s*([\d\.]+)\s*s")
det_re = re.compile(r"Precisión detección:\s*([\d\.]+)%")
col_re = re.compile(r"Precisión colores:\s*([\d\.]+)%")
n_total = 18  # total original
n_balloons = 11  # sólo las imágenes con globos


def load_metrics(path):
    prompts, lat, det, col = [], [], [], []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        m = summary_re.match(lines[i].strip())
        if m and i + 3 < len(lines):
            p = m.group(1)
            m1 = lat_re.match(lines[i + 1].strip())
            m2 = det_re.match(lines[i + 2].strip())
            m3 = col_re.match(lines[i + 3].strip())
            if m1 and m2 and m3:
                # Extraemos directamente el porcentaje de colores
                lat_val = float(m1.group(1))
                det_val = float(m2.group(1))
                col_val = float(m3.group(1))  # sin transformación

                prompts.append(p)
                lat.append(lat_val)
                det.append(det_val)
                col.append(col_val)

                i += 4
                continue
        i += 1
    return prompts, lat, det, col


# Carga de los dos ficheros
p1, lat1, det1, col1 = load_metrics("metrics_0.5B-int8-fixed3.log")
p2, lat2, det2, col2 = load_metrics("metrics_2B-int8-fixed3.log")

# Asegurar mismo orden de prompts
assert p1 == p2, "Los prompts no coinciden entre ficheros"

# 1) Gráfica de Latencias
plt.figure()
plt.plot(p1, lat1, marker="o", label="0.5B-int8")
plt.plot(p2, lat2, marker="s", label="2B-int8")
plt.title("Latencia media por Prompt")
plt.xlabel("Prompt")
plt.ylabel("Latencia (s)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# 2) Gráfica de Precisión de Detección
plt.figure()
plt.plot(p1, det1, marker="o", label="0.5B-int8")
plt.plot(p2, det2, marker="s", label="2B-int8")
plt.title("Precisión de Detección por Prompt")
plt.xlabel("Prompt")
plt.ylabel("Precisión detección (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# 3) Gráfica de Precisión de Colores
plt.figure()
plt.plot(p1, col1, marker="o", label="0.5B-int8")
plt.plot(p2, col2, marker="s", label="2B-int8")
plt.title("Precisión de Colores por Prompt")
plt.xlabel("Prompt")
plt.ylabel("Precisión colores (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()
