import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_AROUND
    page.title = "GEM Morrinhos"

    ft.Container(
        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        ft.Text(
                                            "Bem-vindo",
                                            weight= ft.FontWeight.W_800,
                                            size=30
                                        ),

                                        margin=ft.margin.only(0,0,0,20),
                                        alignment=ft.alignment.center
                                    ),

                                    ft.TextField(
                                        label='Usuário',
                                        # border_color=ft.colors.GREY_400,
                                    ),

                                    ft.TextField(
                                        label='Senha',
                                        # border_color=ft.colors.GREY_400,
                                    ),

                                    ft.Container(
                                        content=ft.OutlinedButton(
                                            "ENTRAR",
                                            expand=True,
                                            width=1800,
                                            style= ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=5),
                                                padding=20,
                                            )
                                        ),
                                        margin=ft.margin.only(0,20,0,0)
                                    )
                                ],
                                alignment= ft.alignment.center,
                            ),
                            padding=15,
                            border_radius= 10,
                            # border=ft.border.all(1, ft.colors.GREY_400),
                            alignment=ft.alignment.center
                        ),
                        alignment=ft.alignment.center

                    )


ft.app(target=main)
