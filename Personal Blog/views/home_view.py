class HomeView:
    @staticmethod
    def render(articles, is_logged_in=False):

        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()

        with open("templates/article.html", "r", encoding="utf-8") as f:
            article_template = f.read()

        if is_logged_in:
            nav_content = '<a href="/admin">Dashboard</a> <a href="/logout" style="color:red;">Sair</a>'
        else:
            nav_content = '<a href="/login">Login</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        articles_html = ""

        for article in articles:
            populated_article = article_template.format(
                id=article.id, title=article.title, date=article.date
            )

            articles_html += populated_article

        return template.replace(
            "{{ content }}", f"<h2>Artigos Recentes</h2>{articles_html}"
        )
