from flet import *
import database

class Card:

    def __init__(self, id):
            self.id_card = id

    def card_a_fazer(self, tipo, instrutor, mensagem):
        truco = ft.Card(
            surface_tint_color=ft.colors.TRANSPARENT,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(f"{tipo} - {instrutor}"),
                            subtitle=ft.Text(f'{mensagem}'),
                        ),
                        ft.Row(
                            [ft.TextButton("Estudei", on_click=lambda _: estudei(self.id_card)),
                             ft.TextButton("Abrir")],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ]
                ),
                width=1800,
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, '#9AB9FF'),
                border_radius=5,
                margin=ft.margin.only(0, 30, 0, 0)
            ),
        )
        return truco

    def card_concluido(self, tipo, instrutor, mensagem):
        truco = ft.Card(
            surface_tint_color=ft.colors.TRANSPARENT,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(f"{tipo} - {instrutor}"),
                            subtitle=ft.Text(f'{mensagem}'),
                        ),
                        ft.Row(
                            [ft.TextButton("Cancelar", on_click=lambda _: cancela_estudei(self.id_card))],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ]
                ),
                width=1800,
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, '#9AB9FF'),
                border_radius=5,
                margin=ft.margin.only(0, 30, 0, 0)
            ),
        )
        return truco

class ToDo(UserControl):

    cards = database.get_cards('João Marcelo')

    def __init__(self):
        super().__init__()

        self.appSpace = Column()

    def build(self):

        '''ESPAÇOS'''
        self.tasks = Column()

        '''ELMENTOS'''

        #Tabs
        self.filter = Tabs(
                scrollable=False,
                selected_index=0,
                # on_change=self.tabs_changed,
                tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
            )

        def a_fazer(self):
            cards_a_fazer = []
            for card in cards['aFazer']:
                task = Card(card['id'])
                cards_a_fazer.append(
                    task.card_a_fazer(card['tipo'], card['instrutor'], card['mensagem'])
                )
            return ft.ListView(controls=cards_a_fazer)

        return Column([
            Row([
                Text(
                    'Tarefa',
                    size=20,
                    weight=FontWeight.W_600,
                    color='#407BFF'
                ),

            ]),
            Column([
                self.filter,
                self.tasks,

            ])
        ])


def main(page:Page):

    page.theme_mode = ThemeMode.LIGHT
    page.title = "GEM Morrinho"

    myApp = ToDo()

    page.add(
        myApp
    )

app(target=main)
