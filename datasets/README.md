# Datasets de prueba — TRESDB

## Cómo cargar un dataset
```
LOAD pequeño.json
LOAD mediano.json
```

## pequeño.json
10 registros de personas con campos: nombre, edad, ciudad, activo.
Ideal para probar operaciones básicas.

## mediano.json  
100 registros generados aleatoriamente con campos: nombre, edad, ciudad, departamento, salario, activo.
Ideal para probar índices, rangos y rendimiento.

## Comandos sugeridos después de cargar
```
cargar
LOAD mediano.json
explorar
SELECT ciudad = Bogotá
RANGE edad 25 35
INDEX departamento
SELECT departamento = Sistemas
UPDATE ciudad = Cali SET ciudad:Medellín
DELETE activo = false
```