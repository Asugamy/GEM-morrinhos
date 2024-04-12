import flet as ft
import database

# Cards
cards = database.get_cards('João Marcelo')


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "GEM Morrinho"
    page.scroll = ft.ScrollMode.ADAPTIVE

    teste = ft.Column(scroll=ft.ScrollMode.ALWAYS)

    user = ft.TextField(label='Usuário')
    password = ft.TextField(label='Senha', password=True, can_reveal_password=True)

    def login(e):
        attempt = database.authentication(user.value, password.value)
        if attempt:
            return page.go("/todo")
        else:

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Usuário/Senha inconreto(s)! Tente novamente",
                    text_align=ft.alignment.center,
                    weight=ft.FontWeight.W_600
                ),
                bgcolor=ft.colors.RED_ACCENT_400,

            )
            page.snack_bar.open = True
            page.update()

    form_task_aluno = ft.Dropdown(
        label='Candidato',
        hint_text='Candidato',
        options=[
            ft.dropdown.Option('João Marcelo'),
            ft.dropdown.Option('Marcos'),
            ft.dropdown.Option('Thiago'),
        ]
    )

    form_task_tipo = ft.Dropdown(
        label='Assunto',
        hint_text='Assunto',
        options=[
            ft.dropdown.Option('MS'),
            ft.dropdown.Option('MTS'),
            ft.dropdown.Option('Método Instrumento'),
            ft.dropdown.Option('Hino'),
        ]
    )

    form_task_mensagem = ft.TextField(label='Digite a tarefa', multiline=True)

    def adicionar_task(e):
        database.add_tasks('Vitor', form_task_mensagem.value, 'aFazer', form_task_tipo.value, form_task_aluno.value)
        page.update()
        return page.go("/todo")

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

    def a_fazer():
        tasks = database.get_cards('João Marcelo')['aFazer']
        cards_a_fazer = []
        for card in tasks:
            task = Card(card['id'])
            cards_a_fazer.append(
                task.card_a_fazer(card['tipo'], card['instrutor'], card['mensagem'])
            )
        return ft.ListView(controls=cards_a_fazer, auto_scroll=True)

    def estudei(id):
        tasks = database.get_cards('João Marcelo')['aFazer']
        for card in tasks:
            if card['id'] == id:
                database.task_concluded(id, 'João Marcelo')
                teste.controls.clear()
                teste.controls.append(a_fazer())
                page.update()

    def concluido():
        tasks = database.get_cards('João Marcelo')['concluido']
        card_concluido = []
        for card in tasks:
            task = Card(card['id'])
            card_concluido.append(
                task.card_concluido(card['tipo'], card['instrutor'], card['mensagem'])
            )
        return ft.ListView(controls=card_concluido)

    def cancela_estudei(id):
        # tasks = database.get_cards('João Marcelo')['concluido']
        for card in cards['concluido']:
            if card['id'] == id:
                database.task_inconcluded(id, 'João Marcelo')
                teste.controls.clear()
                teste.controls.append(concluido())
                page.update()

    def tabs_changed(e):
        if tabs.selected_index == 0:
            teste.controls.clear()
            teste.controls.append(a_fazer())
        if tabs.selected_index == 1:
            teste.controls.clear()
            teste.controls.append(concluido())
        if tabs.selected_index == 2:
            print('CCCCCCCCCCCCC')            
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=tabs_changed,
        scrollable=False,
        tabs=[
            ft.Tab(text="A FAZER"),
            ft.Tab(text='CONCLUÍDAS'),
            ft.Tab(text="CORRIGIDAS"),
        ],
        expand=True,
        tab_alignment=ft.MainAxisAlignment.CENTER,
        divider_color=ft.colors.WHITE,
    )

    def page_add(e):
        return page.go("/add")

    view_todo = ft.View(
        "/todo",
        [
            # Nav-bar
            ft.CupertinoAppBar(
                bgcolor=ft.colors.WHITE,
                middle=ft.Image(
                    src="img.png",
                    width=130,
                    fit=ft.ImageFit.CONTAIN,
                ),
                automatically_imply_leading=False,
            ),

            # Título
            ft.Container(
                ft.Text(
                    'Tarefas',
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color='#407BFF'
                ),
                bgcolor=ft.colors.WHITE,
                margin=ft.margin.only(0, 45, 0, 25),
            ),

            # Tabs
            ft.Column(
                [
                    ft.Container(
                        tabs,
                        alignment=ft.alignment.center  
                    ),
                    ft.Column([
                        teste
                    ], scroll=ft.ScrollMode.ADAPTIVE)
                ],
                horizontal_alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                on_click=page_add
            )
        ],
    )

    def route_change(route):
        page.update()
        page.views.clear()  
        page.views.append(
            ft.View(
                "/",

                [
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Container(
                                                ft.Text(
                                                    "Bem-vindo",
                                                    weight=ft.FontWeight.W_800,
                                                    size=30
                                                ),

                                                margin=ft.margin.only(0, 0, 0, 20),
                                                alignment=ft.alignment.center
                                            ),

                                            user,
                                            password,

                                            ft.Container(
                                                content=ft.OutlinedButton(
                                                    "ENTRAR",
                                                    expand=True,
                                                    width=1800,
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=5),
                                                        padding=20,
                                                    ),
                                                    on_click=login
                                                ),
                                                margin=ft.margin.only(0, 20, 0, 0),
                                            )
                                        ],
                                        alignment=ft.alignment.center,
                                    ),
                                    padding=15,
                                    border_radius=10,
                                    # border=ft.border.all(1, ft.colors.GREY_400),
                                    alignment=ft.alignment.center
                                ),
                                alignment=ft.alignment.center

                            )
                        ],
                    ),
                ],
                vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )
        if page.route == "/todo":
            #Atualiza Cards
            tabs_changed('a'),
            page.views.append(
                view_todo
            )
        if page.route == "/add":
            page.views.append(
                ft.View(
                    "/add",
                    [
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.icons.ARROW_BACK),
                                margin=ft.margin.only(0, 0, 5, 0),
                                on_click=lambda _: page.go("/todo")
                            ),
                            ft.Container(
                                content=ft.Text(
                                    'Nova Tarefa',
                                    size=22
                                )
                            )
                        ], ),

                        # Formulário
                        ft.Column([
                            ft.Container(
                                form_task_aluno,
                                margin=ft.margin.only(0, 30, 0, 0)
                            ),
                            ft.Container(
                                form_task_tipo,
                            ),
                            ft.Container(
                                form_task_mensagem,
                            ),
                            ft.Container(
                                ft.OutlinedButton(
                                    text='ENVIAR',
                                    width=1000,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                        bgcolor=ft.colors.BLUE_900,
                                        color=ft.colors.WHITE,
                                        padding=20
                                    ),
                                    on_click=adicionar_task
                                )
                            )
                        ])
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
