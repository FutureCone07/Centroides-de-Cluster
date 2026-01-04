import pandas as pd
import random
import math

# ============================================================
# 1. GENERACIÓN DE DATOS ALEATORIOS
# ============================================================
print("=================INICIO DEL PROGRAMA=================\n")
try:
    cantidad_datos = int(input("¿Cuántos registros deseas generar?: "))
except ValueError:
    print("Por favor, ingresa un número entero válido.")
    exit()

# Diccionario con las columnas
datos = {
    'Peso': [], 'Estatura': [], 'Salario': [], 'Edad': [],
    'H': [], 'M': [], 'Soltero': [], 'Casado': [], 'Divorciado': [], 'Paga': []
}

# Generación de registros pseudoaleatorios
for _ in range(cantidad_datos):
    peso = round(random.uniform(60, 100), 2)
    estatura = round(random.uniform(1.50, 2.10), 2)
    salario = random.randrange(3000, 30000, 500)
    edad = random.randint(17, 68)

    # Género
    es_hombre = random.choice([0, 1])
    h, m = es_hombre, 1 - es_hombre

    # Estado civil
    sol, cas, div = 0, 0, 0
    estado_civil = random.randint(1, 3)
    if estado_civil == 1:
        sol = 1
    elif estado_civil == 2:
        cas = 1
    elif estado_civil == 3:
        div = 1

    paga = random.choice(["si", "no"])

    # Agregar a listas
    datos['Peso'].append(peso)
    datos['Estatura'].append(estatura)
    datos['Salario'].append(salario)
    datos['Edad'].append(edad)
    datos['H'].append(h)
    datos['M'].append(m)
    datos['Soltero'].append(sol)
    datos['Casado'].append(cas)
    datos['Divorciado'].append(div)
    datos['Paga'].append(paga)

# Crear DataFrame
df = pd.DataFrame(datos)
print("\n=========================== TABLA GENERADA ===========================")
print(df)

# ============================================================
# 2. NORMALIZACIÓN DE DATOS
# ============================================================

def formula_normalizar(arreglo):
    valor_maximo = max(arreglo)
    valor_minimo = min(arreglo)
    rango = valor_maximo - valor_minimo

    if rango == 0:
        return [0.0] * len(arreglo)
    resultado = []
    for valor in arreglo:
        valor_normalizado = (valor - valor_minimo) / rango
        resultado.append(round(valor_normalizado, 2))
    return resultado


columnas_a_normalizar = ['Peso', 'Estatura', 'Salario', 'Edad', 'H', 'M', 'Soltero', 'Casado', 'Divorciado']

df_normalizado = pd.DataFrame()
for col in columnas_a_normalizar:
    df_normalizado[col] = formula_normalizar(df[col])
df_normalizado['Paga'] = df['Paga']

print("\n=========================== TABLA NORMALIZADA ===========================")
print(df_normalizado)

# ============================================================
# 3.                     CLUSTERING
# ============================================================

try:
    cantidad_grupos = int(input("\n¿Cuántos grupos deseas hacer?: "))
    if cantidad_grupos < 1 or cantidad_grupos > cantidad_datos:
        print("Valor inválido. Usando K=2.")
        cantidad_grupos = 2
except ValueError:
    print("Por favor, ingresa un número entero válido para K. Usando K=2.")
    cantidad_grupos = 2

# Índices disponibles para elegir centroides iniciales
indices_disponibles = df_normalizado.index.tolist()
if cantidad_datos < cantidad_grupos:
    cantidad_grupos = cantidad_datos


# Selección aleatoria de centroides iniciales
grupos_arreglo = random.sample(indices_disponibles, cantidad_grupos)
df_grupos = df_normalizado.loc[grupos_arreglo]
grupos_iniciales = {f'Grupo_{i+1}': df_grupos.loc[idx].tolist() for i, idx in enumerate(df_grupos.index)}


print("\n========== GRUPOS INICIALES ==========")
for nombre, grupo in grupos_iniciales.items():
    print(f"{nombre}: {grupo}")

# ============================================================
# 4. FUNCIONES AUXILIARES
# ============================================================

def formula_distancia_n_dim(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

columnas_X = ['Peso', 'Estatura', 'Salario', 'Edad', 'H', 'M', 'Soltero', 'Casado', 'Divorciado']

# ============================================================
# 5.                    ITERACIONES
# ============================================================

max_iteraciones = 10
for iteracion in range(max_iteraciones):
    print(f"\n--- Iteración {iteracion + 1} ---")

    # Asignar cada registro al centroide más cercano
    asignaciones = []
    for _, fila in df_normalizado.iterrows():
        punto = fila[columnas_X].tolist()
        distancias = [(nombre, formula_distancia_n_dim(punto, centroide)) for nombre, centroide in grupos_iniciales.items()]
        grupo_mas_cercano = min(distancias, key=lambda x: x[1])[0]
        asignaciones.append(grupo_mas_cercano)

    df_normalizado['Grupo'] = asignaciones

    # Calcular nuevos centroides
    nuevos_centroides = {}
    cambio = False

    for nombre in grupos_iniciales.keys():
        miembros = df_normalizado[df_normalizado['Grupo'] == nombre]
        if len(miembros) > 0:
            nuevo_centroide = miembros[columnas_X].mean().tolist()
        else:
            # Si el grupo queda vacío, se reasigna aleatoriamente
            nuevo_centroide = df_normalizado.sample(1)[columnas_X].iloc[0].tolist()

        nuevos_centroides[nombre] = nuevo_centroide

        # Verificar si el centroide cambió
        if grupos_iniciales[nombre] != nuevo_centroide:
            cambio = True

    grupos_iniciales = nuevos_centroides

    # Mostrar centroides actuales
    for nombre, centroide in grupos_iniciales.items():
        print(f"{nombre}: {centroide}")

    # Si no hay cambios, detener
    if not cambio:
        print("\nLos centroides ya no cambiaron. Proceso detenido.")
        break

# ============================================================
# 6. RESULTADOS FINALES
# ============================================================

# Añadir la columna "Grupo" del df_normalizado al df original
df['Grupo'] = df_normalizado['Grupo']

# Ordenar por grupo para mostrar los datos originales organizados
df_ordenado = df.sort_values(by='Grupo').reset_index(drop=True)

print("\n========== DATOS ORIGINALES ORGANIZADOS POR GRUPOS ==========")
print(df_ordenado.to_string(index=False))

print("\n========== CENTROIDES FINALES ==========")
for nombre, centroide in grupos_iniciales.items():
    print(f"{nombre}:{centroide}")
