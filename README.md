# MiniDockQT6

# PracticaMiniDock - Editor de Texto (PySide6)

## Resumen

Aplicación de escritorio tipo editor de texto desarrollada con PySide6. Incluye funciones básicas de edición, búsqueda y reemplazo (con dock), formato de texto y gestión de archivos.

## Funcionalidades principales

- Editor central basado en QTextEdit.
- Crear, abrir y guardar archivos de texto (.txt).
- Deshacer / Rehacer.
- Cortar / Copiar / Pegar.
- Contador de palabras en la barra de estado (actualiza dinámicamente).
- Dock lateral "Buscar y Reemplazar" con:
  - Buscar (posiciona en la primera coincidencia).
  - Buscar siguiente / Buscar anterior.
  - Reemplazar (reemplaza la coincidencia actual).
  - Reemplazar todo (reemplaza todas las ocurrencias en el documento).
  - Cerrar el dock.
- Cambiar tipografía (QFontDialog).
- Cambiar color de fondo del área de texto (QColorDialog).
- Resaltar selección con color de fondo.
- Atajos de teclado para acciones comunes.
- Barra de herramientas (toolbar) con accesos rápidos e iconos.

## Instalación y requisitos

- Python 3.8+
- PySide6

Instalar PySide6:

```bash
pip install PySide6
```

## Ejecutar la aplicación

En la carpeta del proyecto:

```bash
python PracticaFinal.py
```

## Atajos de teclado

- Nuevo: Ctrl+N
- Abrir: Ctrl+O
- Guardar: Ctrl+S
- Salir: Ctrl+Q
- Deshacer: Ctrl+Z
- Rehacer: Ctrl+Y
- Copiar: Ctrl+C
- Cortar: Ctrl+X
- Pegar: Ctrl+V
- Tipografía: Ctrl+T
- Color de fondo: Ctrl+Shift+C
- Resaltar: Ctrl+H

## Detalles de uso

- Búsqueda y reemplazo:
  - "Buscar" solicita el texto y posiciona el cursor en la primera coincidencia.
  - "Buscar siguiente" y "Buscar anterior" usan el último término buscado (si no existe, piden uno).
  - "Reemplazar" solicita término y reemplazo, y sustituye la coincidencia actualmente seleccionada/posicionada.
  - "Reemplazar todo" reemplaza todas las ocurrencias en el documento (se realiza sobre texto plano).
- Resaltar conserva formato del documento usando charFormat y background.
- Contador de palabras cuenta palabras separadas por espacios y muestra el total en la barra de estado.

## Limitaciones conocidas y notas

- Reemplazar todo usa `setPlainText(...)` — esto elimina formato si el documento tuviera estilos ricos. Si es necesario preservar formato, usar QTextCursor para reemplazos.
- El dock usa QInputDialog para pedir términos; mejorar UX añadiendo QLineEdit dentro del dock es recomendado.
- `QIcon.fromTheme(...)` puede devolver iconos vacíos en sistemas sin esos temas; el proyecto incluye algunos iconos en `icons/` como fallback.
- El método de cierre del dock asume jerarquía de widgets; se puede robustecer buscando el ancestro QDockWidget.
- Mensajes temporales usados en barra de estado manejan un QTimer; evitar múltiples conexiones al timer (se recomienda usar `QTimer.singleShot`).

## Estructura de archivos

- PracticaFinal.py — código principal (VentanaPrincipal, DockWidgetBuscarReemplazar).
- icons/ — carpeta opcional con iconos locales usados como fallback.

## Contribuciones y mejoras sugeridas

- Añadir campos de búsqueda y reemplazo directamente en el dock para eliminar diálogos modales.
- Implementar búsqueda sensible a mayúsculas/minúsculas y soporte regex.
- Preservar formato al reemplazar (usar QTextCursor).
- Guardar/restaurar posición y estado del dock (QSettings).

## Licencia

Proyecto educativo — usar y modificar libremente para prácticas y aprendizaje.
