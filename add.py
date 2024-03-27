import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "GEM Morrinhos"


    page.add(
        ft.Row([
            ft.Container(
                content= ft.Icon(ft.icons.ARROW_BACK),
                margin=ft.margin.only(0,0,5,0)
            ),
            ft.Container(
                content=ft.Text(
                    'Nova Tarefa',
                    size=22
                )
            )
        ],),

        #Formulário
        ft.Column([
            ft.Container(
                ft.Dropdown(
                    label='Candidato',
                    hint_text='Candidato',
                    options=[
                        ft.dropdown.Option('João'),
                        ft.dropdown.Option('Marcos'),
                        ft.dropdown.Option('Thiago'),
                    ]
                ),
                margin=ft.margin.only(0,30,0,0)
            ),
            ft.Container(
                ft.Dropdown(
                    label='Assunto',
                    hint_text='Assunto',
                    options=[
                        ft.dropdown.Option('MSA'),
                        ft.dropdown.Option('MTS'),
                        ft.dropdown.Option('Método Instrumento'),
                        ft.dropdown.Option('Hinos'),
                    ]
                ),
            ),
            ft.Container(
                ft.TextField(label='Digite a tarefa...', multiline=True)
            ),
            ft.Container(
                ft.OutlinedButton(
                    text='ENVIAR',
                    width=1000,
                    style=ft.ButtonStyle(
                        shape= ft.RoundedRectangleBorder(radius=5),
                        bgcolor=ft.colors.BLUE_900,
                        color=ft.colors.WHITE,
                        padding=20
                    )
                )
            )
        ])
    )

ft.app(main)
