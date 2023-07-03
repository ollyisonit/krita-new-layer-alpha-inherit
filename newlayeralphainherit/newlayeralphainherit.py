# type: ignore
from krita import *
from PyQt5.QtWidgets import QWidget, QAction
from pprint import pprint
from functools import partial

TOGGLE_INHERITANCE_ACTION = "dninosores.new_layer_alpha_inheritance"

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
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def toggle_inheritance(self, isOn):
        msg = "with"
        if not isOn:
            msg = "without"

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
        toggle_inheritance_action.triggered.connect(self.toggle_inheritance)
        QTimer.singleShot(0, self.bind_events)

    def on_new_layer(self):
        print("NEW LAYER CREATED")
        if Application.action(TOGGLE_INHERITANCE_ACTION).isChecked():
            QTimer.singleShot(
                0, lambda: Application.action("toggle_layer_inherit_alpha").trigger()
            )

    def bind_events(self):
        for action in NEW_LAYER_ACTIONS:
            Application.action(action).triggered.connect(self.on_new_layer)
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
