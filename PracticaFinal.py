from PySide6.QtWidgets import QMainWindow, QApplication, QTextEdit, QDockWidget, QToolBar, QMenu, QMenuBar, QStatusBar, QFileDialog, QMessageBox, QInputDialog, QFontDialog, QColorDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
import sys
from PySide6.QtGui import QAction, QKeySequence, QIcon, QTextCursor, QFont
from PySide6.QtCore import Qt, QTimer


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
        self.setGeometry(200, 200, 600, 400)

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
        self.status_bar.showMessage("Palabras:0")
        self.crear_editText.textChanged.connect(self.contar_palabras)

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
        editar_menu.addAction(self.tipografia_action)
        editar_menu.addAction(self.color_fondo_action)
        editar_menu.addAction(self.resaltar_action)

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

    def contar_palabras(self):
        lista_palabras = self.crear_editText.toPlainText().strip().split()
        cantidad = len(lista_palabras)
        self.status_bar.showMessage(f"Palabras: {cantidad}")

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
        # Primero pedir la palabra a buscar y si n existe que se retorne la funcion
        buscar, ok = QInputDialog.getText(self, "Reemplazar", "Texto a buscar")

        if not ok or not buscar:
            return

        reemplazo, ok = QInputDialog.getText(
            self, "Reemplazar", f"Reeemplazar  {buscar} por")

        if not ok:
            return

        pos = self.crear_editText.toPlainText().find(buscar)
        if pos == -1:
            QMessageBox.information(
                self, "Buscar", f"No se encontro el texto {buscar}")
            return

        encontrado = self.mover_cursor_a_texto(buscar, desde_inicio=True)

        if not encontrado:
            QMessageBox.information(
                self, "Reemplazar", f"No se encontró '{buscar}'")
            return

        while encontrado:
            c = self.crear_editText.textCursor()
            # Inserta el reemplazo y mantiene cursor actualizado
            c.insertText(reemplazo)
            encontrado = self.mover_cursor_a_texto(buscar, desde_inicio=False)
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
