# MiniDock QT6 - Editor de Texto

Editor de texto desarrollado con **PySide6** que incluye funcionalidades avanzadas como reconocimiento de voz, búsqueda y reemplazo, formateo de texto y un widget contador de palabras reutilizable.

---

## 📦 Componentes

### WordCounterWidget (`contadorWidget.py`)

Widget reutilizable que muestra estadísticas del texto en tiempo real: palabras, caracteres y tiempo estimado de lectura.

---

## 📡 Documentación de Señales

### Señal: `conteoActualizado`

```python
conteoActualizado = Signal(int, int)
```

#### Descripción
Señal emitida cada vez que se actualiza el conteo de palabras y caracteres en el `WordCounterWidget`.

---

### 📚 ¿Qué significa `Signal(int, int)`?

En PySide6/Qt, las señales se definen con la clase `Signal` donde los **parámetros entre paréntesis indican los tipos de datos** que la señal transportará:

```python
Signal(int, int)  # Esta señal enviará DOS valores enteros
Signal(str)       # Esta señal enviaría UN string
Signal()          # Esta señal no envía datos (solo notifica)
```

En nuestro caso `Signal(int, int)` significa:
- **Primer `int`**: número de palabras
- **Segundo `int`**: número de caracteres

---

### 📤 ¿Cómo funciona `emit()`?

El método `emit()` es la forma de **disparar/emitir una señal** para notificar a todos los slots conectados:

```python
# Definición de la señal (en la clase)
conteoActualizado = Signal(int, int)

# Emisión de la señal (en algún método)
self.conteoActualizado.emit(palabras, caracteres)
#                           ↑          ↑
#                      primer int   segundo int
```

**Flujo completo:**
1. El texto cambia en el editor
2. Se llama a `update_from_text(texto)`
3. Se calculan palabras y caracteres
4. Se ejecuta `self.conteoActualizado.emit(palabras, caracteres)`
5. Todos los slots conectados reciben esos valores

```python
# Conexión: cuando se emita la señal, ejecutar on_conteo_actualizado
self.contador_widget.conteoActualizado.connect(self.on_conteo_actualizado)

# Slot que recibe los valores emitidos
def on_conteo_actualizado(self, palabras, caracteres):
    print(f"Recibido: {palabras} palabras, {caracteres} caracteres")
```

---

#### Parámetros de la señal

| Parámetro | Tipo  | Descripción                              |
|-----------|-------|------------------------------------------|
| `palabras`  | `int` | Número total de palabras en el texto     |
| `caracteres`| `int` | Número total de caracteres en el texto   |

#### ¿Cuándo se emite?
Se emite automáticamente al llamar al método `update_from_text(text)`.

#### Ejemplo de uso

```python
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from contadorWidget import WordCounterWidget

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.editor = QTextEdit()
        self.contador = WordCounterWidget(wpm=200)
        
        layout.addWidget(self.editor)
        layout.addWidget(self.contador)
        
        # Conectar el cambio de texto al contador
        self.editor.textChanged.connect(self.actualizar)
        
        # Conectar la señal conteoActualizado
        self.contador.conteoActualizado.connect(self.on_conteo_actualizado)
    
    def actualizar(self):
        self.contador.update_from_text(self.editor.toPlainText())
    
    def on_conteo_actualizado(self, palabras, caracteres):
        print(f"📊 Palabras: {palabras} | Caracteres: {caracteres}")

if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec()
```

---

## 🔧 API del WordCounterWidget

### Constructor

```python
WordCounterWidget(wpm=200, mostrarPalabras=True, mostrarCaracteres=True, mostrarTiempoLectura=True, parent=None)
```

| Parámetro           | Tipo   | Default | Descripción                                      |
|---------------------|--------|---------|--------------------------------------------------|
| `wpm`               | `int`  | `200`   | Palabras por minuto para calcular tiempo lectura |
| `mostrarPalabras`   | `bool` | `True`  | Mostrar/ocultar el label de palabras             |
| `mostrarCaracteres` | `bool` | `True`  | Mostrar/ocultar el label de caracteres           |
| `mostrarTiempoLectura`| `bool`| `True`  | Mostrar/ocultar el label de tiempo de lectura    |
| `parent`            | `QWidget`| `None`| Widget padre                                     |

### Métodos

#### `update_from_text(text: str)`
Actualiza los contadores con el texto proporcionado y emite la señal `conteoActualizado`.

```python
contador.update_from_text("Hola mundo, esto es un ejemplo.")
# Actualiza: Palabras: 6, Caracteres: 31
# Emite: conteoActualizado(6, 31)
```

---

## 🎤 Otras Señales en el Proyecto

### ReconocimientoVozWorker

| Señal       | Parámetros | Descripción                                        |
|-------------|------------|----------------------------------------------------|
| `recognized`| `str`      | Texto reconocido por el micrófono                  |
| `error`     | `str`      | Mensaje de error si falla el reconocimiento        |
| `status`    | `str`      | Estado actual del proceso (calibrando, escuchando) |
| `finished`  | —          | Indica que el proceso de escucha ha terminado      |

---

## 🚀 Ejecución

```bash
python PracticaFinal.py
```

### Dependencias
- `PySide6`
- `SpeechRecognition` (opcional, para reconocimiento de voz)
- `PyAudio` (opcional, para reconocimiento de voz)

```bash
pip install PySide6 SpeechRecognition PyAudio
```

---

## 📁 Estructura del Proyecto

```
MiniDockQT6/
├── PracticaFinal.py      # Aplicación principal
├── contadorWidget.py     # Widget contador de palabras
├── README.md             # Esta documentación
└── icons/                # Iconos de la aplicación
```
