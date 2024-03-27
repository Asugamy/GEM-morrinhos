import flet as ft
import database

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "GEM Morrinhos"

    # Menu Lateral
    def login(e):
        attempt = database.authentication(user.value, password.value)
        if attempt:
            return page.go("/todo")
        else:

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Usuário/Senha inconreto(s)! Tente novamente.",
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
            ft.dropdown.Option('MSA'),
            ft.dropdown.Option('MTS'),
            ft.dropdown.Option('Método Instrumento'),
            ft.dropdown.Option('Hinos'),
        ]
    )

    form_task_mensagem = ft.TextField(label='Digite a tarefa', multiline=True)

    # def adicionar_task(e):
    #     database.add_tasks('Vitor', form_task_mensagem.value, 'aFazer', form_task_tipo.value, form_task_aluno.value)

    # Cards
    # cards = database.get_cards('João Marcelo')

    # def a_fazer():
    #     cards_a_fazer = []
    #     for card in cards['aFazer']:
    #         cards_a_fazer.append(
    #             ft.Card(
    #                 surface_tint_color=ft.colors.TRANSPARENT,
    #                 content=ft.Container(
    #                     content=ft.Column(
    #                         [
    #                             ft.ListTile(
    #                                 title=ft.Text(f"{card['tipo']} - {card['instrutor']}"),
    #                                 subtitle=ft.Text(f'{card["mensagem"]}'),
    #                             ),
    #                             ft.Row(
    #                                 [ft.TextButton("Estudei", on_click=lambda: estudei(card['id'])),
    #                                  ft.TextButton("Abrir")],
    #                                 alignment=ft.MainAxisAlignment.SPACE_AROUND,
    #                             ),
    #                             ft.TextField(value=card['id'], visible=False),
    #                         ]
    #                     ),
    #                     width=1800,
    #                     padding=10,
    #                     bgcolor=ft.colors.WHITE,
    #                     border=ft.border.all(1, '#9AB9FF'),
    #                     border_radius=5,
    #                     margin=ft.margin.only(0, 30, 0, 0)
    #                 ),
    #             )
    #         )
    #     return ft.ListView(controls=cards_a_fazer)

    # def estudei(id):
    #     for card in cards['aFazer']:
    #         if card['id'] == id :
    #             card['status'] = 'concluido'
    #             page.update()

    def page_add(e):
        return page.go("/add")

    page.add(
        #Título
        ft.Container(
            ft.Text(
                'Tarefas',
                size=20,
                weight=ft.FontWeight.W_600,
                color='#407BFF'
            ),
            bgcolor=ft.colors.WHITE,
            margin=ft.margin.only(0,45,0,25),
        ),

        #Tabs
        ft.Row(
            [
                ft.Tabs(
                    selected_index=1,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="A FAZER",
                            content=ft.Column(
                                [
                                    ft.Card(
                                        surface_tint_color=ft.colors.WHITE,
                                        content=ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.ListTile(
                                                        title=ft.Text("Método - Almir"),
                                                        subtitle=ft.Text(
                                                            "Estudar novamente a lição 16 da página 14, lembrando de pontuar"
                                                        ),
                                                    ),
                                                    ft.Row(
                                                        [ft.TextButton("Estudei"), ft.TextButton("Abrir")],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),
                                                ]
                                            ),
                                            width=1800,
                                            padding=10,
                                            bgcolor=ft.colors.WHITE,
                                            border=ft.border.all(1, '#9AB9FF'),
                                            border_radius=5,
                                            margin=ft.margin.only(0,30,0,0)
                                        ),
                                    ),
                                    ft.Card(
                                        surface_tint_color=ft.colors.WHITE,
                                        content=ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.ListTile(
                                                        title=ft.Text("Método - Almir"),
                                                        subtitle=ft.Text(
                                                            "Estudar novamente a lição 16 da página 14, lembrando de pontuar"
                                                        ),
                                                    ),
                                                    ft.Row(
                                                        [ft.TextButton("Estudei"), ft.TextButton("Abrir")],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),
                                                ]
                                            ),
                                            width=1800,
                                            padding=10,
                                            bgcolor=ft.colors.WHITE,
                                            border=ft.border.all(1, '#9AB9FF'),
                                            border_radius=5,
                                            margin=ft.margin.only(0,15,0,0)
                                        ),
                                    ),
                                    ft.Card(
                                        surface_tint_color=ft.colors.WHITE,
                                        content=ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.ListTile(
                                                        title=ft.Text("Método - Almir"),
                                                        subtitle=ft.Text(
                                                            "Estudar novamente a lição 16 da página 14, lembrando de pontuar"
                                                        ),
                                                    ),
                                                    ft.Row(
                                                        [ft.TextButton("Estudei"), ft.TextButton("Abrir")],
                                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    ),
                                                ]
                                            ),
                                            width=1800,
                                            padding=10,
                                            bgcolor=ft.colors.WHITE,
                                            border=ft.border.all(1, '#9AB9FF'),
                                            border_radius=5,
                                            margin=ft.margin.only(0,15,0,0),
                                        ),
                                    ),
                                ],
                                scroll=ft.ScrollMode.ALWAYS
                            )
                        ),
                        ft.Tab(
                            text='CONCLUÍDAS',
                            content=ft.Text("This is Tab 2"),
                        ),
                        ft.Tab(
                            text="CORRIGIDAS",
                            content=ft.Text("This is Tab 3"),
                        ),
                    ],
                    expand=1,
                    tab_alignment=ft.MainAxisAlignment.CENTER,
                    divider_color=ft.colors.WHITE
                )
            ],
            expand=True,

        ),

        ft.FloatingActionButton(icon=ft.icons.ADD)
    )

ft.app(main)
