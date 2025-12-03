# MiniDockQT6 v1.1.0 – Control por voz y mejoras de edición

## Novedades destacadas
- **Control por voz**: comandos para negrita, cursiva, subrayado, guardar y nuevo documento, con inserción de texto dictado si no se reconoce un comando.
- **Escucha más robusta**: detección de micrófonos disponibles, calibrado de ruido ambiente, timeouts configurados y mensajes de estado/errores en la barra inferior.
- **Búsqueda y reemplazo en dock**: accesos rápidos para buscar, navegar coincidencias y reemplazar (incluye reemplazar todo).
- **Atajos e iconos**: toolbar y menús con iconos y shortcuts para formato, color de fondo, resaltado y acciones de archivo.
- **Indicador en vivo**: contador de palabras en la barra de estado con mensajes temporales contextualizados.

## Requisitos
- Python 3.8+ (Pipfile preparado para 3.13).
- Dependencias: PySide6, SpeechRecognition, PyAudio, PyInstaller.

Instalación rápida:
```bash
pip install -r requirements.txt
python PracticaFinal.py
```

Para voz en Windows, si PyAudio falla:
```bash
pip install pipwin
pipwin install pyaudio
```

## Uso del control por voz
- Toolbar o menú `Voz` → `Escuchar comando de voz` (Ctrl+Shift+M).
- Comandos soportados: "negrita", "cursiva", "subrayado", "guardar (archivo)", "nuevo (documento)".
- Si no se detecta un comando, el texto dictado se inserta en el cursor actual.

## Paquete listo para release
- Código principal: `PracticaFinal.py`.
- Recursos: iconos en `icons/` y `assets/`.
- Empaquetado sugerido: `pipenv install && pipenv run pyinstaller MiApp.spec`.
