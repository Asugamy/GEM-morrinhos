import flet as ft
import database
import page_ficha as pf


def main(page: ft.Page):


    if not page.client_storage.contains_key("login_session"): page.client_storage.set('login_session', False)
    if not page.client_storage.contains_key("user"): page.client_storage.set('user', '')
    if not page.client_storage.contains_key("name_user"): page.client_storage.set('name_user', '')
    if not page.client_storage.contains_key("level"): page.client_storage.set('level', '')
    if not page.client_storage.contains_key("menu_index"): page.client_storage.set('menu_index', 0)

    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "GEM Morrinhos"            

    container_tasks = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    container_ficha = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    user = ft.TextField(label='Usuário', value='isaiasvitorslva@gmail.com')
    password = ft.TextField(label='Senha', value='12345', password=True, can_reveal_password=True)

    cards = []

    def login(e):
        attempt = database.authentication(user.value, password.value)
        if attempt:
            page.client_storage.set('login_session', True)
            page.client_storage.set('user', user.value)
            page.client_storage.set('name_user', attempt['nome'])
            page.client_storage.set('level', attempt['nivel'])
            cards = database.get_cards(user.value)
            return page.go("/app")
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
            ft.dropdown.Option('Vitor'),
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
        database.add_tasks(
            page.client_storage.get('name_user'), 
            form_task_mensagem.value, 
            form_task_tipo.value, 
            form_task_aluno.value
        )
        form_task_aluno.value = ''
        page.update()
        return page.go("/app")

    class Card:

        def __init__(self, id):
            self.id_card = id

        def card_a_fazer(self, tipo, instrutor, mensagem):
            card = ft.Card(
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
                ),
            )
            return card

        def card_concluido(self, tipo, instrutor, mensagem):
            card = ft.Card(
                surface_tint_color=ft.colors.TRANSPARENT,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(f"{tipo} - {instrutor}"),
                                subtitle=ft.Text(f'{mensagem}'),
                            ),
                            ft.Row(
                                [ft.TextButton("Cancelar", on_click=lambda _: cancela_estudei(self.id_card)),
                                 ft.TextButton('Corrigir', on_click=lambda _: corrigir(self.id_card))],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                        ]
                    ),
                    width=1800,
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, '#9AB9FF'),
                    border_radius=5,
                ),
            )
            return card

        def card_corrigido(self, tipo, instrutor, mensagem):
            card = ft.Card(
                surface_tint_color=ft.colors.TRANSPARENT,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(f"{tipo} - {instrutor}"),
                                subtitle=ft.Text(f'{mensagem}'),
                            ),
                            ft.Row(
                                [ft.TextButton("Cancelar", on_click=lambda _: cancela_corrigido(self.id_card))],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                        ]
                    ),
                    width=1800,
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, '#9AB9FF'),
                    border_radius=5,
                ),
            )
            return card

    def a_fazer():
        tasks = database.get_cards(user.value)['aFazer']
        cards_a_fazer = []
        for card in tasks:
            task = Card(card['id'])
            cards_a_fazer.append(
                task.card_a_fazer(card['tipo'], card['instrutor'], card['mensagem'])
            )
        return ft.ListView(controls=cards_a_fazer, auto_scroll=True, spacing=20)

    def estudei(id):
        tasks = database.get_cards(user.value)['aFazer']
        for card in tasks:
            if card['id'] == id:
                database.task_concluded(id, user.value)
                container_tasks.controls.clear()
                container_tasks.controls.append(a_fazer())
                page.update()

    def concluido():
        tasks = database.get_cards(user.value)['concluido']
        card_concluido = []
        for card in tasks:
            task = Card(card['id'])
            card_concluido.append(
                task.card_concluido(card['tipo'], card['instrutor'], card['mensagem'])
            )
        return ft.ListView(controls=card_concluido)

    def cancela_estudei(id):
        tasks = database.get_cards(user.value)['concluido']
        for card in tasks:
            if card['id'] == id:
                database.task_inconcluded(id, user.value)
                container_tasks.controls.clear()
                container_tasks.controls.append(concluido())
                page.update()

    def corrigido():
        tasks = database.get_cards(user.value)['corrigido']
        card_corrigido = []
        for card in tasks:
            task = Card(card['id'])
            card_corrigido.append(
                task.card_corrigido(card['tipo'], card['instrutor'], card['mensagem'])
            )
        return ft.ListView(controls=card_corrigido)
    
    def corrigir(id):
        tasks = database.get_cards(user.value)['concluido']
        for card in tasks:
            if card['id'] == id:
                database.task_corrected(id, user.value)
                container_tasks.controls.clear()
                container_tasks.controls.append(concluido())
                page.update()
    
    def cancela_corrigido(id):
        tasks = database.get_cards(user.value)['corrigido']
        for card in tasks:
            if card['id'] == id:
                database.task_incorrected(id, user.value)
                container_tasks.controls.clear()
                container_tasks.controls.append(corrigido())
                page.update()

    def update_cards(e):
        if tabs.selected_index == 0:
            container_tasks.controls.clear()
            container_tasks.controls.append(a_fazer())
        if tabs.selected_index == 1:
            container_tasks.controls.clear()
            container_tasks.controls.append(concluido())
        if tabs.selected_index == 2:
            container_tasks.controls.clear()
            container_tasks.controls.append(corrigido())           
        page.update()

    def update_content(i_destino):
        i_atual = page.client_storage.get('menu_index')
        page.client_storage.set('menu_index', i_destino)
        if i_atual == 0: menu_icon_todo.icon_color = ft.colors.GREY
        elif i_atual == 1: menu_icon_ficha.icon_color = ft.colors.GREY
        elif i_atual == 2: menu_icon_calendario.icon_color = ft.colors.GREY
        elif i_atual == 3: menu_icon_pessoal.icon_color = ft.colors.GREY
        if i_destino == 0: menu_icon_todo.icon_color = None
        if i_destino == 1: menu_icon_ficha.icon_color = None
        if i_destino == 2: menu_icon_calendario.icon_color = None
        if i_destino == 3: menu_icon_pessoal.icon_color = None
        page_content()
            


    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=update_cards,
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
    menu_icon_todo = ft.IconButton(
        ft.icons.CHECK_BOX, 
        icon_size=30, 
        on_click=lambda _:update_content(0)    
    )
    menu_icon_ficha = ft.IconButton(
        ft.icons.LIST_ALT, 
        icon_color=ft.colors.GREY, 
        icon_size=30, 
        on_click=lambda _:update_content(1)
    )
    menu_icon_calendario = ft.IconButton(
        ft.icons.CALENDAR_MONTH, 
        icon_color=ft.colors.GREY, 
        icon_size=30    
    )
    menu_icon_pessoal = ft.IconButton(
        ft.icons.PERSON, 
        icon_color=ft.colors.GREY, 
        icon_size=30
    )

    def page_add(e):
        return page.go("/add")
    
    navbar_top = ft.Container(
        ft.Row( 
            controls=[
                ft.Container(
                    ft.Image(
                        src="https://i.postimg.cc/Gpjj1sJY/img.png",
                        width=75,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                    ),
                ),
                ft.Container(
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_size=25,
                        on_click=page_add
                    ),
                ),
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )    
    )

    conteudo = ft.Container(expand=True)

    conteudo_todo = ft.Column(
        [
            ft.Container(
                tabs,
                alignment=ft.alignment.center  
            ),
            ft.Container(
                content = container_tasks, 
                expand=True,
                expand_loose=True,
                padding=ft.Padding(10,0,10,0),
                bgcolor=ft.colors.GREY_50,
            )
        ],
        horizontal_alignment=ft.MainAxisAlignment.CENTER, expand=True
    )

    conteudo_ficha = ft.Container(
        pf.main()
    )

    navbar_bottom = ft.Container(
        ft.Row(
            [
                menu_icon_todo,
                menu_icon_ficha,
                menu_icon_calendario,
                menu_icon_pessoal
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        border=ft.Border(top=ft.BorderSide(1,ft.colors.GREY_100)),
        padding=10,
        shadow=ft.BoxShadow(
            spread_radius=1,

            blur_radius=2,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        
    )

    view_app = ft.View(
        "/app",
        [
            navbar_top,
            conteudo,
            navbar_bottom
        ],
        padding=0,
        spacing=0
    )

    def page_content():
        aba_selecionada = page.client_storage.get('menu_index')
        print(aba_selecionada)
        if aba_selecionada == 0: conteudo.content = conteudo_todo
        if aba_selecionada == 1: conteudo.content = conteudo_ficha
        page.update()

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
        if page.route == "/app":
            #Atualiza Cards
            update_cards('a'),
            #Chama o conteudo
            update_content(0)
            page_content()
            page.views.append(
                view_app
            )
        if page.route == "/add":
            page.views.append(
                ft.View(
                    "/add",
                    [
                        ft.Container(
                            margin=ft.Margin(0, 25, 0, 0),
                            content = ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.icons.ARROW_BACK),
                                    margin=ft.margin.only(0, 0, 5, 0),
                                    on_click=lambda _: page.go("/app")
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        'Nova Tarefa',
                                        size=22
                                    )
                                )
                            ]), 
                        ),

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
