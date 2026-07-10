from PyQt6.QtCore import pyqtSignal, QPoint
from PyQt6.QtWidgets import QMenu, QApplication
from PyQt6.QtGui import QAction, QKeySequence


class ContextMenu(QMenu):
    """Базовое контекстное меню для браузера."""

    new_tab_requested = pyqtSignal()
    copy_link_requested = pyqtSignal(str)
    inspect_requested = pyqtSignal()

    def __init__(self, tab: 'BrowserTab', parent=None):
        super().__init__(parent)
        self.tab = tab
        self.setStyleSheet("""
        QMenu {
            background-color: #1c1e22;
            border: 1px solid #3a3f4a;
            border-radius: 8px;
            padding: 4px 0px;
            margin: 0;
        }
        QMenu::item {
            padding: 6px 24px;
            color: #e6eef8;
        }
        QMenu::item:selected {
            background-color: #4b93ff;
            color: white;
            border-radius: 8px;
        }
        QMenu::separator {
            height: 1px;
            background: #3a3f4a;
            margin: 4px 8px;
        }""")
        self._build_menu()
    
    def _build_menu(self) -> None:
        self.back_action = QAction("Назад")
        self.back_action.setShortcut(QKeySequence.StandardKey.Back)
        self.forward_action = QAction("Вперёд")
        self.forward_action.setShortcut(QKeySequence.StandardKey.Forward)
        self.reload_action = QAction("Обновить")
        self.reload_action.setShortcut(QKeySequence.StandardKey.Refresh)

        self.copy_action = QAction("Копировать")
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.paste_action = QAction("Вставить")
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)

        self.select_all_action = QAction("Выделить всё")
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)

        #self.new_tab_action = QAction("Открыть в новой вкладке")
        #self.new_tab_action.setShortcut(QKeySequence.StandardKey.New)
        #self.new_tab_action.setEnabled(False)
        self.inspect_action = QAction("Проверить элемент")

        self.back_action.triggered.connect(self.handle_back)
        self.forward_action.triggered.connect(self.handle_forward)
        self.reload_action.triggered.connect(self.handle_reload)

        self.copy_action.triggered.connect(self.handle_copy)
        self.paste_action.triggered.connect(self.tab.pageAction(self.tab.page().WebAction.Paste).trigger)

        self.select_all_action.triggered.connect(self.handle_select_all)

        #self.new_tab_action.triggered.connect(self.new_tab_requested.emit)
        self.inspect_action.triggered.connect(self.handle_inspect)

        self.addAction(self.back_action)
        self.addAction(self.forward_action)
        self.addAction(self.reload_action)
        self.addSeparator()
        self.addAction(self.copy_action)
        #self.addAction(self.copy_link_action)
        self.addAction(self.paste_action)
        self.addSeparator()
        self.addAction(self.select_all_action)
        self.addSeparator()
        #self.addAction(self.new_tab_action)
        self.addAction(self.inspect_action)

        self.aboutToShow.connect(self._sync_actions)

    def _sync_actions(self) -> None:
        #? проверяем возможность перехода назад
        self.back_action.setVisible(True) if self.tab.page().history().canGoBack() else self.back_action.setVisible(False)
        #? проверяем возможность перехода вперед
        self.forward_action.setVisible(True) if self.tab.page().history().canGoForward() else self.forward_action.setVisible(False)
        self.reload_action.setEnabled(True)

        #? проверяем возможность копирования
        self.copy_action.setVisible(True) if self.tab.page().selectedText() else self.copy_action.setVisible(False)


        #self.new_tab_action.setEnabled(True)
        #self.select_all_action.setEnabled(True)
        #self.inspect_action.setEnabled(True)

    def handle_back(self) -> None:
        self.tab.history().back()

    def handle_forward(self) -> None:
        self.tab.history().forward()

    def handle_reload(self) -> None:
        self.tab.reload()

    def handle_new_tab(self) -> None:
        self.new_tab_requested.emit()

    def handle_copy_link(self) -> None:
        self.copy_link_requested.emit(self._link_url)

    def handle_copy(self) -> None:
        selected = self.tab.page().selectedText()
        if selected:
            QApplication.clipboard().setText(str(selected))

    def handle_select_all(self) -> None:
        self.tab.pageAction(self.tab.page().WebAction.SelectAll).trigger()

    def handle_inspect(self) -> None:
        self.tab.pageAction(self.tab.page().WebAction.InspectElement).trigger()

    def show_at(self, position: QPoint) -> None:
        """Показывает меню в глобальной позиции."""
        self.popup(position)