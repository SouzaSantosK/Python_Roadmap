class AdminView:
    @staticmethod
    def render_dashboard(articles):
        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()

        with open("templates/article_actions.html", "r", encoding="utf-8") as f:
            article_actions_template = f.read()

        with open("templates/dashboard.html", "r", encoding="utf-8") as f:
            dashboard_template = f.read()

        nav_content = '<a href="/admin">Dashboard</a> <a href="/logout" style="color:red;">Sair</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        rows = ""

        for article in articles:
            populated_article_action = article_actions_template.format(
                id=article.id, title=article.title, date=article.date
            )

            rows += populated_article_action

        populated_dashboard = dashboard_template.format(rows=rows)

        content = populated_dashboard

        return template.replace("{{ content }}", content)

    @staticmethod
    def render_edit_form(article):
        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()

        with open("templates/new_article.html", "r", encoding="utf-8") as f:
            form = f.read()

        nav_content = '<a href="/admin">Dashboard</a> <a href="/logout" style="color:red;">Sair</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        form = form.replace('action="/admin/new"', f'action="/admin/edit/{article.id}"')
        form = form.replace('name="title"', f'name="title" value="{article.title}"')
        form = form.replace('name="date"', f'name="date" value="{article.date}"')
        form = form.replace("</textarea>", f"{article.content}</textarea>")
        form = form.replace("Publicar Artigo</button>", f"Editar</button>")

        return template.replace("{{ content }}", f"<h2>Editar Artigo</h2>{form}")
