# type: ignore
from krita import *
from PyQt5.QtWidgets import QWidget, QAction
from pprint import pprint
from functools import partial

TOGGLE_INHERITANCE_ACTION = "dninosores.new_layer_alpha_inheritance"

WRAP_AROUND_TEXT = "Wrap Around Mode"

VERTICAL_MIRROR_TEXT = "Vertical Mirror Tool"

NEW_LAYER_ACTIONS = [
    "add_new_clone_layer",
    "add_new_file_layer",
    "add_new_fill_layer",
    "add_new_adjustment_layer",
    "add_new_group_layer",
    "add_new_paint_layer",
    "add_new_shape_layer",
]


class NewLayerAlphaInheritExtension(Extension):
    tool_button = None

    up_palette = None
    down_palette = None

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def toggle_inheritance(self, isOn):
        msg = "with"
        if not isOn:
            msg = "without"

        if self.tool_button:
            self.tool_button.setChecked(isOn)

        Application.activeWindow().activeView().showFloatingMessage(
            f"New layers will now be created {msg} alpha inheritance enabled.",
            Application.icon("transparency-enabled"),
            3000,
            1,
        )

    def createActions(self, window):
        toggle_inheritance_action = window.createAction(
            TOGGLE_INHERITANCE_ACTION,
            "New Layer Alpha Inheritance",
            "layer",
        )
        toggle_inheritance_action.setIcon(Krita.instance().icon("transparency-enabled"))
        toggle_inheritance_action.triggered.connect(self.toggle_inheritance)
        QTimer.singleShot(0, self.bind_events)

    def on_new_layer(self):
        if Application.action(TOGGLE_INHERITANCE_ACTION).isChecked():
            QTimer.singleShot(
                0, lambda: Application.action("toggle_layer_inherit_alpha").trigger()
            )

    def get_wraparound_button(self):
        for item, depth in IterHierarchy(Application.activeWindow().qwindow()):
            try:
                if item.text() == WRAP_AROUND_TEXT:
                    return item
            except:
                pass

    def get_mirror_button(self):
        for item, depth in IterHierarchy(Application.activeWindow().qwindow()):
            try:
                if item.text() == VERTICAL_MIRROR_TEXT:
                    return item
            except:
                pass

    def on_button_toggled(self, isOn):
        Application.action(TOGGLE_INHERITANCE_ACTION).setChecked(isOn)
        if not isOn:
            if self.up_palette:
                self.tool_button.setPalette(self.up_palette)
        else:
            if self.down_palette:
                self.tool_button.setPalette(self.down_palette)

    def bind_events(self):
        for action in NEW_LAYER_ACTIONS:
            Application.action(action).triggered.connect(self.on_new_layer)
        wraparound_button = self.get_wraparound_button()
        widget_group = wraparound_button.parent()
        self.tool_button = QToolButton(widget_group)
        layout = None
        for sibling in self.tool_button.parent().children():
            if "BoxLayout" in str(sibling):
                layout = sibling
        # self.tool_button.addAction(Application.action(TOGGLE_INHERITANCE_ACTION))
        self.tool_button.setCheckable(True)
        self.tool_button.toggled.connect(self.on_button_toggled)
        self.tool_button.setText("New layer alpha inheritance")
        self.tool_button.setToolTip("New layer alpha inheritance")
        self.tool_button.setBaseSize(wraparound_button.baseSize())
        self.tool_button.setAutoFillBackground(wraparound_button.autoFillBackground())
        self.tool_button.setBackgroundRole(wraparound_button.backgroundRole())
        self.tool_button.setForegroundRole(wraparound_button.foregroundRole())
        self.tool_button.setContentsMargins(wraparound_button.contentsMargins())
        self.tool_button.setContextMenuPolicy(wraparound_button.contextMenuPolicy())
        self.tool_button.setGeometry(wraparound_button.geometry())
        self.tool_button.setMaximumSize(wraparound_button.maximumSize())
        self.tool_button.setMinimumSize(wraparound_button.minimumSize())
        self.tool_button.setStyle(wraparound_button.style())
        self.tool_button.setSizePolicy(wraparound_button.sizePolicy())
        self.tool_button.setToolButtonStyle(wraparound_button.toolButtonStyle())
        self.tool_button.setPalette(wraparound_button.palette())
        self.tool_button.setGraphicsEffect(wraparound_button.graphicsEffect())
        self.tool_button.setAutoRaise(wraparound_button.autoRaise())

        mirror_button = self.get_mirror_button()
        mirror_button_checked = mirror_button.isChecked()
        mirror_button.setChecked(False)
        self.up_palette = mirror_button.palette()
        mirror_button.setChecked(True)
        self.down_palette = mirror_button.palette()
        mirror_button.setChecked(mirror_button_checked)

        # self.tool_button.setStyleSheet(wraparound_button.styleSheet())

        # self.tool_button.text = "New layer alpha inheritance"
        # self.tool_button.toolTip = self.tool_button.text
        # self.tool_button.baseSize = wraparound_button.baseSize
        # self.tool_button.focusPolicy = wraparound_button.focusPolicy
        # self.tool_button.font = wraparound_button.font
        # self.tool_button.frameGeometry = wraparound_button.frameGeometry
        # self.tool_button.frameSize = wraparound_button.frameSize
        # self.tool_button.geometry = wraparound_button.geometry
        # self.tool_button.height = wraparound_button.height
        # self.tool_button.iconSize = wraparound_button.iconSize
        # self.tool_button.width = wraparound_button.width

        self.tool_button.setIcon(Krita.instance().icon("transparency-enabled"))
        layout.addWidget(self.tool_button)
        # for item, depth in IterHierarchy(Application.activeWindow().qwindow()):
        #     # print_branch(item, depth)
        #     if "paintopbox" in item.objectName():
        #         print("Creating action")
        #         newaction = QWidgetAction(item)
        #         newaction.setIcon(Application.icon("transparency-enabled"))
        #         for child in item.children():
        #             print(child.objectName())
        # Application.action(TOGGLE_INHERITANCE_ACTION).setIcon(
        #     Application.icon("transparency-enabled")
        # )
        # item.addAction(Application.action(TOGGLE_INHERITANCE_ACTION))

        # print_branch(item, depth)
        # print_parents(item, depth)
        # print_children(item, depth)
        # if "QDockWidget" in str(item):
        #     print_branch(item, depth)
        # if "mirror" in item.dumpObjectInfo():
        #     print(item.dumpObjectInfo())
        # if item.objectName() == "mirror_actions":
        #     print_branch(item, 0)
        #     for item2, depth2 in IterHierarchy(item):
        #         print_branch(item2, depth2)
        # if "mirror" in item.objectName():
        #     testdepth = depth
        #     testitem = item
        #     while testitem:
        #         print(f"{'|   '*testdepth}{testitem.objectName()}-{testitem}")
        #         testitem = testitem.parent()
        #         testdepth -= 1
        #     print(f"{'|   '*depth}{item.objectName()}-{item}")
        #     for item2, depth2 in IterHierarchy(item):
        #         print(f"{'|   '*depth2}{item2.objectName()}-{item2}")


def print_parents(item, depth):
    depth2 = depth
    item2 = item
    while item2:
        print_branch(item2, depth2)
        item2 = item2.parent()
        depth2 -= 1


def print_children(item, depth):
    for item2, depth2 in IterHierarchy(item):
        print_branch(item2, depth + depth2)


def print_branch(item, depth):
    print(f"{'|   '*depth}{item.objectName()}-{item}")


class IterHierarchy:
    queue = []

    def __init__(self, root):
        self.root = root
        self.queue = []

    def __iter__(self):
        self.queue = self.walk_hierarchy(self.root)
        return self

    def walk_hierarchy(self, item, level=0, acc=[]):
        acc.append((item, level))
        for child in item.children():
            self.walk_hierarchy(child, level + 1, acc)
        return acc

    def __next__(self):
        if len(self.queue) > 0:
            cur_item = self.queue.pop(0)
            return cur_item[0], cur_item[1]
        else:
            raise StopIteration

    # # Take the existing export_region action and move it to be after file_export in the file menu
    # def moveAction(self, action, qwindow):
    #     menu_bar = qwindow.menuBar()
    #     file_menu_action = next(
    #         (a for a in menu_bar.actions() if a.objectName() == "file"), None
    #     )
    #     if file_menu_action:
    #         file_menu = file_menu_action.menu()
    #         for file_action in file_menu.actions():
    #             if file_action.objectName() == "file_export_advanced":
    #                 file_menu.removeAction(action)
    #                 file_menu.insertAction(file_action, action)


Krita.instance().addExtension(NewLayerAlphaInheritExtension(Krita.instance()))
