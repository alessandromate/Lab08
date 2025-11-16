import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()
    my_model.get_consumi()
    print(my_model._consumi)
    my_model.get_consumi_prima_settimana_mese(2)


ft.app(target=main)
