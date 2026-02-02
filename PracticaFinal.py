from PySide6.QtWidgets import QMainWindow, QApplication, QTextEdit, QDockWidget, QToolBar, QMenu, QMenuBar, QStatusBar, QFileDialog, QMessageBox, QInputDialog, QFontDialog, QColorDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
import sys
from PySide6.QtGui import QAction, QKeySequence, QIcon, QTextCursor, QFont
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject
from contadorWidget import WordCounterWidget

try:
    import speech_recognition as sr
except ImportError:
    sr = None


class ReconocimientoVozWorker(QObject):
    recognized = Signal(str)
    error = Signal(str)
    status = Signal(str)
    finished = Signal()

    def __init__(self, language="es-ES"):
        super().__init__()
        self.language = language

    def start_listening(self):
        if sr is None:
            self.error.emit(
                "speech_recognition no está instalado (instala SpeechRecognition y PyAudio)."
            )
            self.finished.emit()
            return

        # Verificar que hay micrófonos disponibles antes de abrir uno
        mic_names = sr.Microphone.list_microphone_names()
        if not mic_names:
            self.error.emit("No se detectó ningún micrófono en el sistema.")
            self.finished.emit()
            return

        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                self.status.emit("Calibrando ruido ambiente...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                self.status.emit("Escuchando comando...")
                audio = recognizer.listen(
                    source, timeout=5, phrase_time_limit=6
                )

            texto = recognizer.recognize_google(
                audio, language=self.language
            )
            # Emitimos el texto tal cual para poder transcribirlo; se convierte a minúsculas en el procesado de comandos
            self.recognized.emit(texto)
        except sr.WaitTimeoutError:
            self.error.emit("No se detectó voz (tiempo agotado).")
        except sr.UnknownValueError:
            self.error.emit("No se entendió el audio.")
        except sr.RequestError as e:
            self.error.emit(f"Error con el servicio de reconocimiento: {e}")
        except Exception as e:
            self.error.emit(f"Error al escuchar: {e}")
        finally:
            self.finished.emit()


class DockWidgetBuscarReemplazar(QWidget):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Buscar y Reemplazar")
        titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titulo)

        # Crear botones con iconos
        fila_buscar = QHBoxLayout()
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setIcon(QIcon.fromTheme("edit-find"))
        self.buscar_btn.clicked.connect(self.ventana_principal.buscar_texto)
        fila_buscar.addWidget(self.buscar_btn)

        self.siguiente_btn = QPushButton("Siguiente")
        self.siguiente_btn.setIcon(QIcon.fromTheme("go-down"))
        self.siguiente_btn.clicked.connect(
            self.ventana_principal.buscar_siguiente)
        fila_buscar.addWidget(self.siguiente_btn)

        self.anterior_btn = QPushButton("Anterior")
        self.anterior_btn.setIcon(QIcon.fromTheme("go-up"))
        self.anterior_btn.clicked.connect(
            self.ventana_principal.buscar_anterior)
        fila_buscar.addWidget(self.anterior_btn)

        layout.addLayout(fila_buscar)

        self.reemplazar_btn = QPushButton("Reemplazar")
        self.reemplazar_btn.setIcon(QIcon.fromTheme("edit-find-replace"))
        self.reemplazar_btn.clicked.connect(
            self.ventana_principal.reemplazar_texto)
        layout.addWidget(self.reemplazar_btn)

        self.reemplazar_todo_btn = QPushButton("Reemplazar todo")
        self.reemplazar_todo_btn.setIcon(QIcon.fromTheme("edit-find-replace"))
        self.reemplazar_todo_btn.clicked.connect(
            self.ventana_principal.reemplazar_todo)
        layout.addWidget(self.reemplazar_todo_btn)

        # Botón de cerrar
        self.cerrar_btn = QPushButton("Cerrar")
        self.cerrar_btn.clicked.connect(self.cerrar_dock)
        layout.addWidget(self.cerrar_btn)

        self.setLayout(layout)

    def cerrar_dock(self):
        # Obtener el dock widget padre y cerrarlo
        dock_widget = self.parent().parent()
        dock_widget.close()


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word")
        self.setWindowIcon(QIcon("icons/favicon.ico"))
        self.setGeometry(200, 200, 600, 400)
        self.voice_thread = None

        # Inicializar componentes
        self.crear_edit_text()
        self.crear_acciones()
        self.configurar_shortcuts()
        self.crear_menu()
        self.crear_tool_bar()
        self.crear_iconos()
        self.crear_barra_de_estados()
        self.contar_palabras()
        self.crear_dock_buscar_reemplazar()
        # self.buscar_texto()

        # Timer para mensajes temporales en status bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.contar_palabras)

    # Crear StatusBar

    def crear_barra_de_estados(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Integrar el WordCounterWidget en la barra de estado
        self.contador_widget = WordCounterWidget(
            wpm=200,
            mostrarPalabras=True,
            mostrarCaracteres=True,
            mostrarTiempoLectura=True
        )
        self.status_bar.addPermanentWidget(self.contador_widget)

        # Conectar la señal textChanged para actualizar el contador
        self.crear_editText.textChanged.connect(self.actualizar_contador)

        # Conectar la señal conteoActualizado del widget para posibles usos futuros
        self.contador_widget.conteoActualizado.connect(self.on_conteo_actualizado)

    # CrearTextEdit
    def crear_edit_text(self):
        self.crear_editText = QTextEdit(self)
        self.setCentralWidget(self.crear_editText)
    # Crear acciones reutilizables

    def crear_acciones(self):
        self.nuevo_action = QAction("Nuevo", self)
        self.nuevo_action.triggered.connect(self.nuevo_archivo)

        self.abrir_action = QAction("Abrir", self)
        self.abrir_action.triggered.connect(self.abrir_archivo)

        self.guardar_action = QAction("Guardar", self)
        self.guardar_action.triggered.connect(self.guardar_archivo)

        self.salir_action = QAction("Salir", self)
        self.salir_action.triggered.connect(self.close)

        self.deshacer_action = QAction("Deshacer", self)
        self.deshacer_action.triggered.connect(self.deshacer_archivo)

        self.rehacer_action = QAction("Rehacer", self)
        self.rehacer_action.triggered.connect(self.rehacer_archivo)

        self.copiar_action = QAction("Copiar", self)
        self.copiar_action.triggered.connect(self.copiar_archivo)

        self.cortar_action = QAction("Cortar", self)
        self.cortar_action.triggered.connect(self.cortar_archivo)

        self.pegar_action = QAction("Pegar", self)
        self.pegar_action.triggered.connect(self.pegar_archivo)

        self.buscar_action = QAction("Buscar", self)
        self.buscar_action.triggered.connect(
            self.mostrar_dock_buscar_reemplazar)

        self.reemplazar_action = QAction("Reemplazar", self)
        self.reemplazar_action.triggered.connect(
            self.mostrar_dock_buscar_reemplazar)

        self.tipografia_action = QAction("Tipografia", self)
        self.tipografia_action.triggered.connect(self.cambiar_tipografia)

        self.color_fondo_action = QAction("Color de Fondo", self)
        self.color_fondo_action.triggered.connect(self.cambiar_color_fondo)

        self.resaltar_action = QAction("Resaltar Texto", self)
        self.resaltar_action.triggered.connect(self.resaltar_texto)

        self.negrita_action = QAction("Negrita", self)
        self.negrita_action.triggered.connect(self.aplicar_negrita)

        self.cursiva_action = QAction("Cursiva", self)
        self.cursiva_action.triggered.connect(self.aplicar_cursiva)

        self.subrayado_action = QAction("Subrayado", self)
        self.subrayado_action.triggered.connect(self.aplicar_subrayado)

        self.reconocimiento_voz_action = QAction(
            "Escuchar comando de voz", self
        )
        self.reconocimiento_voz_action.triggered.connect(
            self.iniciar_reconocimiento_voz
        )

    # Shortcuts para acciones

    def configurar_shortcuts(self):
        self.nuevo_action.setShortcut(QKeySequence.New)
        self.abrir_action.setShortcut(QKeySequence.Open)
        self.guardar_action.setShortcut(QKeySequence.Save)
        self.salir_action.setShortcut("Ctrl+Q")  # QKeySequence.Exit no existe

        self.deshacer_action.setShortcut(QKeySequence.Undo)
        self.rehacer_action.setShortcut(QKeySequence.Redo)
        self.copiar_action.setShortcut(QKeySequence.Copy)
        self.cortar_action.setShortcut(QKeySequence.Cut)
        self.pegar_action.setShortcut(QKeySequence.Paste)

        self.tipografia_action.setShortcut("Ctrl+T")
        self.color_fondo_action.setShortcut("Ctrl+Shift+C")
        self.resaltar_action.setShortcut("Ctrl+H")
        self.negrita_action.setShortcut("Ctrl+B")
        self.cursiva_action.setShortcut("Ctrl+I")
        self.subrayado_action.setShortcut("Ctrl+U")
        self.reconocimiento_voz_action.setShortcut("Ctrl+Shift+M")

    # Crear MenuBar con acciones

    def crear_menu(self):
        menu_bar = self.menuBar()

        # Menú Archivo
        archivo_menu = menu_bar.addMenu("Archivo")
        archivo_menu.addAction(self.nuevo_action)
        archivo_menu.addAction(self.abrir_action)
        archivo_menu.addAction(self.guardar_action)
        archivo_menu.addAction(self.salir_action)

        # Menú Editar
        editar_menu = menu_bar.addMenu("Editar")
        editar_menu.addAction(self.deshacer_action)
        editar_menu.addAction(self.rehacer_action)
        editar_menu.addSeparator()
        editar_menu.addAction(self.cortar_action)
        editar_menu.addAction(self.copiar_action)
        editar_menu.addAction(self.pegar_action)
        editar_menu.addAction(self.buscar_action)
        editar_menu.addAction(self.reemplazar_action)

        formato_menu = menu_bar.addMenu("Formato")
        formato_menu.addAction(self.tipografia_action)
        formato_menu.addAction(self.color_fondo_action)
        formato_menu.addAction(self.resaltar_action)
        formato_menu.addSeparator()
        formato_menu.addAction(self.negrita_action)
        formato_menu.addAction(self.cursiva_action)
        formato_menu.addAction(self.subrayado_action)

        voz_menu = menu_bar.addMenu("Voz")
        voz_menu.addAction(self.reconocimiento_voz_action)

    def crear_tool_bar(self):
        toolbar = QToolBar("Caja de herramientas")
        self.addToolBar(toolbar)

        # Añadir acciones con iconos a la toolbar
        toolbar.addAction(self.nuevo_action)
        toolbar.addAction(self.abrir_action)
        toolbar.addAction(self.guardar_action)
        toolbar.addSeparator()
        toolbar.addAction(self.deshacer_action)
        toolbar.addAction(self.rehacer_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cortar_action)
        toolbar.addAction(self.copiar_action)
        toolbar.addAction(self.pegar_action)
        toolbar.addSeparator()
        toolbar.addAction(self.buscar_action)
        toolbar.addAction(self.reemplazar_action)
        toolbar.addAction(self.tipografia_action)
        toolbar.addAction(self.color_fondo_action)
        toolbar.addAction(self.resaltar_action)
        toolbar.addAction(self.negrita_action)
        toolbar.addAction(self.cursiva_action)
        toolbar.addAction(self.subrayado_action)
        toolbar.addSeparator()
        toolbar.addAction(self.reconocimiento_voz_action)

    def crear_iconos(self):
        """Asigna iconos a todas las acciones usando iconos del sistema"""
        # Iconos para archivo
        self.nuevo_action.setIcon(QIcon.fromTheme("document-new"))
        self.abrir_action.setIcon(QIcon.fromTheme("document-open"))
        self.guardar_action.setIcon(QIcon.fromTheme("document-save"))
        self.salir_action.setIcon(QIcon.fromTheme("application-exit"))

        # Iconos para edición
        self.deshacer_action.setIcon(QIcon.fromTheme("edit-undo"))
        self.rehacer_action.setIcon(QIcon.fromTheme("edit-redo"))
        self.cortar_action.setIcon(QIcon.fromTheme("edit-cut"))
        self.copiar_action.setIcon(QIcon.fromTheme("edit-copy"))
        self.pegar_action.setIcon(QIcon.fromTheme("edit-paste"))

        # Icono para buscar
        self.buscar_action.setIcon(QIcon.fromTheme("edit-find"))

        # Icono para reemplazar
        self.reemplazar_action.setIcon(QIcon("icons/exchange.png"))

        # Icono para tipografía
        self.tipografia_action.setIcon(QIcon("icons/font.png"))

        # Icono para color de fondo
        self.color_fondo_action.setIcon(QIcon("icons/background.png"))

        # Icono para resaltar texto
        self.resaltar_action.setIcon(QIcon("icons/highlighter.png"))

        # Iconos para formato y voz
        self.negrita_action.setIcon(QIcon.fromTheme("format-text-bold"))
        self.cursiva_action.setIcon(QIcon.fromTheme("format-text-italic"))
        self.subrayado_action.setIcon(QIcon.fromTheme("format-text-underline"))
        self.reconocimiento_voz_action.setIcon(
            QIcon.fromTheme("audio-input-microphone")
        )

    def crear_dock_buscar_reemplazar(self):
        """Crear el dock widget para buscar y reemplazar"""
        self.dock_buscar_reemplazar = QDockWidget("Buscar y Reemplazar", self)

        # Crear el widget contenido del dock
        self.widget_buscar_reemplazar = DockWidgetBuscarReemplazar(self)
        self.dock_buscar_reemplazar.setWidget(self.widget_buscar_reemplazar)

        # Configurar el dock widget
        self.dock_buscar_reemplazar.setAllowedAreas(
            Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.dock_buscar_reemplazar.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)

        # Inicialmente oculto
        self.dock_buscar_reemplazar.hide()

        # Agregar el dock widget a la ventana principal
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_buscar_reemplazar)

    def mostrar_dock_buscar_reemplazar(self):
        """Mostrar u ocultar el dock widget de buscar y reemplazar"""
        if self.dock_buscar_reemplazar.isVisible():
            self.dock_buscar_reemplazar.hide()
        else:
            self.dock_buscar_reemplazar.show()
            # Enfocar el campo de búsqueda

    def actualizar_contador(self):
        """Actualiza el WordCounterWidget con el texto actual del editor."""
        texto = self.crear_editText.toPlainText()
        self.contador_widget.update_from_text(texto)

    def on_conteo_actualizado(self, palabras, caracteres):
        """Slot que recibe la señal conteoActualizado del WordCounterWidget.
        Puede usarse para lógica adicional basada en el conteo."""
        # Ejemplo: mostrar información en consola para debug
        # print(f"Conteo actualizado - Palabras: {palabras}, Caracteres: {caracteres}")
        pass

    def contar_palabras(self):
        """Método legacy - ahora delega al WordCounterWidget."""
        self.actualizar_contador()

    def mostrar_mensaje_temporal(self, mensaje, duracion=2000):
        """Muestra un mensaje temporal en la barra de estado y luego vuelve al contador de palabras"""
        self.status_bar.showMessage(mensaje)
        self.timer.stop()  # Detener timer anterior si existe
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.contar_palabras)
        self.timer.start(duracion)  # 2 segundos por defecto

    def nuevo_archivo(self):
        self.crear_editText.clear()
        self.mostrar_mensaje_temporal("Nuevo archivo creado")

    def abrir_archivo(self):
        ruta = QFileDialog.getOpenFileName(
            self, "Abrir archivo de texto",
            "",
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )

        if ruta:
            try:
                # Si no se le pasa el primer parametro de la ruta no funciona
                with open(ruta[0], "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                    self.crear_editText.setPlainText(contenido)
                    self.mostrar_mensaje_temporal(
                        f"Archivo cargado: {ruta[0]}")
            except Exception as e:
                self.status_bar.showMessage(f"Error al abrir el archivo: {e}")
                QMessageBox.warning(
                    self, "Error", f"No se pudo abrir el archivo: {e}")

    def guardar_archivo(self):
        ruta = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "Archivos de texto (*.txt)")
        if ruta:
            with open(ruta[0], "w", encoding="utf-8") as file:
                file.write(self.crear_editText.toPlainText())
            QMessageBox.information(
                self, "Guardado", "El archivo se ha guardado correctamente.")
            self.mostrar_mensaje_temporal("Archivo guardado correctamente")

    def buscar_texto(self):
        texto, ok = QInputDialog.getText(self, "Buscar", "Texto a buscar")
        if not ok or not texto:
            return
        self.texto_buscado = texto
        encontrado = self.mover_cursor_a_texto(
            self.texto_buscado, desde_inicio=True)
        if not encontrado:
            QMessageBox.information(
                self, "Buscar", f"No se encontró el texto '{texto}'")
            return
        self.mostrar_mensaje_temporal(
            "Selección posicionada en la primera coincidencia")

    def buscar_siguiente(self):
        # Usar último texto buscado o pedir uno
        if not hasattr(self, 'texto_buscado') or not self.texto_buscado:
            texto, ok = QInputDialog.getText(
                self, "Buscar siguiente", "Texto a buscar")
            if not ok or not texto:
                return
            self.texto_buscado = texto

        # Mover el cursor al final de la selección actual para evitar repetir
        c = self.crear_editText.textCursor()
        if c.hasSelection():
            c.setPosition(c.selectionEnd())
            self.crear_editText.setTextCursor(c)

        encontrado = self.mover_cursor_a_texto(
            self.texto_buscado, desde_inicio=False)
        if not encontrado:
            QMessageBox.information(self, "Buscar", "No hay más ocurrencias")
            return
        self.mostrar_mensaje_temporal("Ocurrencia siguiente encontrada")

    def buscar_anterior(self):
        # Usar último texto buscado o pedir uno si no tiene texto pedirle uno
        if not hasattr(self, 'texto_buscado') or not self.texto_buscado:
            texto, ok = QInputDialog.getText(
                self, "Buscar anterior", "Texto a buscar")
            if not ok or not texto:
                return
            self.texto_buscado = texto

        encontrado = self.mover_cursor_a_texto_anterior(self.texto_buscado)
        if not encontrado:
            QMessageBox.information(
                self, "Buscar", "No hay ocurrencias anteriores")
            return
        self.mostrar_mensaje_temporal("Ocurrencia anterior encontrada")

    def reemplazar_texto(self):
        buscar, ok = QInputDialog.getText(self, "Reemplazar", "Texto a buscar")
        if not ok or not buscar:
            return

        reemplazo, ok = QInputDialog.getText(
            self, "Reemplazar", f"Reemplazar {buscar} por")
        if not ok:
            return

        pos = self.crear_editText.toPlainText().find(buscar)
        if pos == -1:
            QMessageBox.information(
                self, "Buscar", f"No se encontró el texto {buscar}")
            return

        encontrado = self.mover_cursor_a_texto(buscar, desde_inicio=True)
        if not encontrado:
            QMessageBox.information(
                self, "Reemplazar", f"No se encontró '{buscar}'")
            return

        c = self.crear_editText.textCursor()
        c.insertText(reemplazo)
        self.mostrar_mensaje_temporal("Texto reemplazado correctamente")

    def reemplazar_todo(self):
        """Reemplaza todas las ocurrencias del texto buscado por el reemplazo dado."""
        buscar, ok = QInputDialog.getText(
            self, "Reemplazar todo", "Texto a buscar")
        if not ok or not buscar:
            return

        reemplazo, ok = QInputDialog.getText(
            self, "Reemplazar todo", f"Reemplazar '{buscar}' por")
        if not ok:
            return

        contenido = self.crear_editText.toPlainText()
        conteo = contenido.count(buscar)
        if conteo == 0:
            QMessageBox.information(
                self, "Reemplazar todo", f"No se encontró '{buscar}'")
            return

        contenido_nuevo = contenido.replace(buscar, reemplazo)
        self.crear_editText.setPlainText(contenido_nuevo)
        self.mostrar_mensaje_temporal(f"Reemplazadas {conteo} ocurrencias")

    def mover_cursor_a_texto(self, texto, desde_inicio=True):
        """
        Mueve el cursor a la siguiente ocurrencia de `texto`.
        Retorna True si se encontró, False si no.
        """
        c = self.crear_editText.textCursor()

        if desde_inicio:
            c.movePosition(QTextCursor.Start)

        documento = self.crear_editText.toPlainText()
        pos = documento.find(texto, c.position())

        if pos == -1:
            return False

        c.setPosition(pos)
        c.setPosition(pos + len(texto), QTextCursor.KeepAnchor)
        self.crear_editText.setTextCursor(c)
        return True

    def mover_cursor_a_texto_anterior(self, texto):
        """
        Mueve el cursor a la ocurrencia anterior de `texto` respecto a la posición actual.
        Retorna True si se encontró, False si no.
        """
        c = self.crear_editText.textCursor()
        inicio_busqueda = c.selectionStart() if c.hasSelection() else c.position()
        documento = self.crear_editText.toPlainText()
        # Buscar de manera inversa , cogiendo todo el texto del cocumento hasta la posicion actual del cursor
        pos = documento.rfind(texto, 0, inicio_busqueda)
        if pos == -1:
            return False
        c.setPosition(pos)
        c.setPosition(pos + len(texto), QTextCursor.KeepAnchor)
        self.crear_editText.setTextCursor(c)
        return True

    def cambiar_tipografia(self):
        fuente_actual = self.crear_editText.currentFont()
        ok, fuente = QFontDialog.getFont(
            fuente_actual, self, "Seleccionar Fuente")

        if ok:
            self.crear_editText.setFont(fuente)
            self.mostrar_mensaje_temporal("Tipografía cambiada")

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor(
            Qt.white, self, "Seleccionar color de fondo")
        if color.isValid():
            self.crear_editText.setStyleSheet(
                f"background-color: {color.name()};")
            self.mostrar_mensaje_temporal("Color de fondo cambiado")

    def resaltar_texto(self):
        cursor = self.crear_editText.textCursor()

        if not cursor.hasSelection():
            self.mostrar_mensaje_temporal("Selecciona texto para resaltar")
            return

        color = QColorDialog.getColor(
            Qt.yellow, self, "Seleccionar un color de fondo")

        if color.isValid():
            formato = cursor.charFormat()
            formato.setBackground(color)
            cursor.mergeCharFormat(formato)
            self.mostrar_mensaje_temporal("Texto resaltado")

    def _aplicar_formato_cursor(self, cursor, formato):
        """Aplica formato al cursor actual o a la palabra bajo el cursor."""
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(formato)
        self.crear_editText.mergeCurrentCharFormat(formato)
        self.crear_editText.setTextCursor(cursor)

    def aplicar_negrita(self):
        cursor = self.crear_editText.textCursor()
        formato = cursor.charFormat()
        activar = formato.fontWeight() != QFont.Bold
        formato.setFontWeight(QFont.Bold if activar else QFont.Normal)
        self._aplicar_formato_cursor(cursor, formato)
        mensaje = "Negrita activada" if activar else "Negrita desactivada"
        self.mostrar_mensaje_temporal(mensaje)

    def aplicar_cursiva(self):
        cursor = self.crear_editText.textCursor()
        formato = cursor.charFormat()
        activar = not formato.fontItalic()
        formato.setFontItalic(activar)
        self._aplicar_formato_cursor(cursor, formato)
        mensaje = "Cursiva activada" if activar else "Cursiva desactivada"
        self.mostrar_mensaje_temporal(mensaje)

    def aplicar_subrayado(self):
        cursor = self.crear_editText.textCursor()
        formato = cursor.charFormat()
        activar = not formato.fontUnderline()
        formato.setFontUnderline(activar)
        self._aplicar_formato_cursor(cursor, formato)
        mensaje = "Subrayado activado" if activar else "Subrayado desactivado"
        self.mostrar_mensaje_temporal(mensaje)

    def iniciar_reconocimiento_voz(self):
        if sr is None:
            QMessageBox.warning(
                self,
                "Reconocimiento de voz",
                "speech_recognition y PyAudio no están instalados.",
            )
            return

        if self.voice_thread and self.voice_thread.isRunning():
            self.mostrar_mensaje_temporal("Ya se está escuchando...")
            return

        self.voice_thread = QThread()
        self.voice_worker = ReconocimientoVozWorker()
        self.voice_worker.moveToThread(self.voice_thread)

        self.voice_thread.started.connect(self.voice_worker.start_listening)
        self.voice_worker.recognized.connect(self.procesar_comando_voz)
        self.voice_worker.status.connect(self.status_bar.showMessage)
        self.voice_worker.error.connect(self.mostrar_mensaje_temporal)
        self.voice_worker.finished.connect(self.voice_thread.quit)
        self.voice_worker.finished.connect(self.voice_worker.deleteLater)
        self.voice_worker.finished.connect(self.contar_palabras)
        self.voice_thread.finished.connect(
            lambda: setattr(self, "voice_thread", None)
        )
        self.voice_thread.finished.connect(self.voice_thread.deleteLater)

        self.status_bar.showMessage("Activando micrófono...")
        self.voice_thread.start()

    def procesar_comando_voz(self, comando_raw):
        comando = comando_raw.lower().strip()
        acciones_por_comando = [
            ("negrita", self.aplicar_negrita),
            ("cursiva", self.aplicar_cursiva),
            ("subrayado", self.aplicar_subrayado),
            ("guardar archivo", self.guardar_archivo),
            ("guardar", self.guardar_archivo),
            ("nuevo documento", self.nuevo_archivo),
            ("nuevo", self.nuevo_archivo),
        ]

        for texto_clave, accion in acciones_por_comando:
            if texto_clave in comando:
                accion()
                self.status_bar.showMessage(f"Comando por voz: {texto_clave}")
                return

        # Si no es comando, se transcribe el texto reconocido en el cursor actual
        texto_a_insertar = comando_raw.strip()
        if texto_a_insertar:
            cursor = self.crear_editText.textCursor()
            cursor.insertText(texto_a_insertar + " ")
            self.crear_editText.setTextCursor(cursor)
            self.mostrar_mensaje_temporal(f"Texto dictado: {texto_a_insertar}")
        else:
            self.mostrar_mensaje_temporal(
                "No se dictó texto o no se reconoció el comando"
            )

    def deshacer_archivo(self):
        self.crear_editText.undo()
        self.mostrar_mensaje_temporal("Acción deshecha")

    def rehacer_archivo(self):
        self.crear_editText.redo()
        self.mostrar_mensaje_temporal("Acción rehecha")

    def copiar_archivo(self):
        self.crear_editText.copy()
        self.mostrar_mensaje_temporal("Texto copiado")

    def cortar_archivo(self):
        self.crear_editText.cut()
        self.mostrar_mensaje_temporal("Texto cortado")

    def pegar_archivo(self):
        self.crear_editText.paste()
        self.mostrar_mensaje_temporal("Texto pegado")

    def salir_archivo(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())
