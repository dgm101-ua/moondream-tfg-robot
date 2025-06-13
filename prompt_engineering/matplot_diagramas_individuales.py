import re
import matplotlib.pyplot as plt

# Regex para extraer las métricas
summary_re = re.compile(r"^Resumen para prompt '(.+)':")
lat_re = re.compile(r"Latencia media:\s*([\d\.]+)\s*s")
det_re = re.compile(r"Precisión detección:\s*([\d\.]+)%")
col_re = re.compile(r"Precisión colores:\s*([\d\.]+)%")


def load_metrics(path):
    prompts, det, col = [], [], []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        m = summary_re.match(lines[i].strip())
        if m and i + 3 < len(lines):
            p = m.group(1)
            m2 = det_re.match(lines[i + 2].strip())
            m3 = col_re.match(lines[i + 3].strip())
            if m2 and m3:
                prompts.append(p)
                det.append(float(m2.group(1)))
                col.append(float(m3.group(1)))
                i += 4
                continue
        i += 1
    return prompts, det, col


# Cargar métricas para cada modelo
prompts1, det1, col1 = load_metrics("metrics_0.5B-int8-fixed3.log")
prompts2, det2, col2 = load_metrics("metrics_2B-int8-fixed3.log")

# Crear diagrama para 0.5B-int8
plt.figure()
plt.plot(prompts1, det1, marker="o", label="Precisión detección")
plt.plot(prompts1, col1, marker="s", label="Precisión colores")
plt.title("0.5B-int8: Precisión por Prompt")
plt.xlabel("Prompt")
plt.ylabel("Precisión (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Crear diagrama para 2B-int8
plt.figure()
plt.plot(prompts2, det2, marker="o", label="Precisión detección")
plt.plot(prompts2, col2, marker="s", label="Precisión colores")
plt.title("2B-int8: Precisión por Prompt")
plt.xlabel("Prompt")
plt.ylabel("Precisión (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()
