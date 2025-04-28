# GIT_COMMIT_CONVENTIONS

Este proyecto utiliza convenciones de commits para mantener un historial de cambios limpio, estandarizado y fácil de automatizar.

## 🔖 Formato de Commit

Cada commit debe comenzar con un prefijo seguido de dos puntos y un breve resumen del cambio.

**Formato general:**

```plaintext
<tipo>: <descripción breve>
```

Ejemplo:

```plaintext
feat: agregar API para agendar citas médicas
```

## 🔹 Tipos de Prefix Permitidos

| Tipo         | Uso                                            | Ejemplo |
|--------------|------------------------------------------------|-------------------------------------------------------|
| feat         | Nueva funcionalidad                            | `feat: agregar exportación a XML`                     |
| fix          | Corrección de bug                              | `fix: corregir error de timezone en login`            |
| docs         | Cambios en documentación                       | `docs: actualizar README con pasos de deploy`         |
| style        | Cambios de formato (espaciado, indentaciones)  | `style: corregir indentaciones en views.py`           |
| refactor     | Refactorizar código sin cambiar funcionalidad  | `refactor: simplificar validación de login`           |
| test         | Agregar o corregir pruebas automáticas         | `test: agregar tests para logout y refresh token`     |
| chore        | Tareas menores (build, dependencias, configs)  | `chore: actualizar docker-compose con healthcheck`    |

## 🔍 Reglas generales

- Usa **presente imperativo** en la descripción ("agregar" en lugar de "agregado").
- Mantén la descripción **breve** (idealmente menos de 72 caracteres).
- Si necesitas una descripción extendida, agrégala después de una línea en blanco.

Ejemplo:

```plaintext
feat: agregar validación de emails en el registro

Se agrega expresión regular para verificar formato de correo.
Se evita duplicidad de registros.
```

## 🔄 Flujo recomendado de trabajo

1. Realizar cambios en una rama.
2. Commit siguiendo las convenciones.
3. Push a la rama remota.
4. Pull Request (PR) a `develop` o `main`.
5. GitHub Actions correrá tests automáticos.
6. Generación automática de changelog basada en commits.

## 📈 Beneficios de usar convenciones de commits

- Historial de cambios claro y profesional.
- Generación automática de CHANGELOG.md.
- Mejor revisión de Pull Requests.
- Facilitación de integración continua (CI/CD).
- Estándares de calidad en el repositorio.

## 🔹 Ejemplos correctos de commits

```plaintext
feat: agregar funcionalidad de reprogramación de citas
fix: corregir error de validación en registro de pacientes
docs: documentar nuevos endpoints de expedientes médicos
refactor: optimizar consultas a base de datos en logs
chore: actualizar versiones de librerías en requirements.txt
test: agregar pruebas unitarias para AccessLogExportView
```

## Fin del documento
