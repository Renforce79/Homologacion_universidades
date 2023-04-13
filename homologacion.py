import csv
import json

# Leer el archivo de universidades
with open('universidades.json', 'r') as f:
    universidades = json.load(f)

# Crear un diccionario de sinónimos
sinonimos = {}
for universidad in universidades:
    nombre = universidad['Nombre '].lower()
    siglas = universidad['Siglas '].lower()
    sinonimos[nombre] =  [nombre, siglas,nombre + "("+ siglas+ ")" ]
    if '(' in nombre and ')' in nombre:
        sinonimos[nombre].append(nombre[nombre.find('(')+1:nombre.find(')')])

# Leer el archivo de instituciones educativas
with open('instituciones_educativas.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

# Homologar las universidades
for row in rows:
    universidad = row['value'].lower()
    homologada = None
    for u in universidades:
        if u['Nombre '].lower() == universidad or u['Siglas '].lower() == universidad:
            homologada = 'HOMOLOGADA'
            break
    if not homologada:
        for s, sin in sinonimos.items():
            if universidad in sin:
                homologada = s
                break
    row['universidad_homologada'] = homologada if homologada else 'NO HOMOLOGADA'

# Escribir el archivo de instituciones educativas homologadas
with open('universidades_homologadas.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['candidateId', 'value', 'universidad_homologada']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Escribir el archivo de sinónimos
with open('sinonimo_universidades.json', 'w', encoding='utf-8') as f:
    json.dump([{'nombre_universidad': k, 'sinonimos': v} for k, v in sinonimos.items()], f, ensure_ascii=False, indent=2)

