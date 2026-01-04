# 📊 Generación de Datos y Clustering K-Means (Implementación Manual)

Este proyecto es una herramienta en Python diseñada para generar datos demográficos sintéticos, normalizarlos y agruparlos utilizando una implementación propia del algoritmo **K-Means**, sin depender de librerías de Machine Learning externas para el cálculo de distancias o agrupación.

## 🚀 Características

* **Generación de Datos Pseudoaleatorios:** Crea perfiles ficticios con atributos como Peso, Estatura, Salario, Edad, Género y Estado Civil.
* **Manejo de Variables Categóricas:** Convierte automáticamente variables categóricas (Género, Estado Civil) en variables numéricas (*dummy/one-hot*) para poder procesarlas matemáticamente.
* **Normalización Manual:** Implementa la fórmula Min-Max desde cero para escalar los datos.
* **Algoritmo K-Means Propio:** Implementación de la lógica de centroides, distancias y reasignación iterativa.

## 📋 Requisitos

El código utiliza **Pandas** para la manipulación de estructuras de datos y librerías estándar de Python.

* Python 3.x
* Pandas

Instalación de dependencias:

```bash
pip install pandas
```
