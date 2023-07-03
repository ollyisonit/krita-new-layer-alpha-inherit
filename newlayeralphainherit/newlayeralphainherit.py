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

    def createActions(self, window):
        toggle_inheritance_action = window.createAction(
            TOGGLE_INHERITANCE_ACTION,
            "New Layer Alpha Inheritance",
            "layer",
        )
        # export_region_action.triggered.connect(self.export_region)
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
