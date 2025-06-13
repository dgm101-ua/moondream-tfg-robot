import re


# Script para calcular la media de las métricas en un fichero de log
def calcular_medias(path_log):
    det_re = re.compile(r"^Precisión detección:\s*([\d\.]+)%")
    col_re = re.compile(r"^Precisión colores:\s*([\d\.]+)%")

    det_vals = []
    col_vals = []

    with open(path_log, encoding="utf-8") as f:
        for line in f:
            m_det = det_re.match(line.strip())
            m_col = col_re.match(line.strip())
            if m_det:
                det_vals.append(float(m_det.group(1)))
            if m_col:
                col_vals.append(float(m_col.group(1)))

    media_det = sum(det_vals) / len(det_vals) if det_vals else 0
    media_col = sum(col_vals) / len(col_vals) if col_vals else 0

    print(f"Media Precisión detección: {media_det:.2f}%")
    print(f"Media Precisión colores:   {media_col:.2f}%")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python calcular_medias.py <ruta_fichero_log>")
    else:
        calcular_medias(sys.argv[1])
