class NewArticleView:
    @staticmethod
    def render():
        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()
        with open("templates/new_article.html", "r", encoding="utf-8") as f:
            form = f.read()

        nav_content = '<a href="/admin">Dashboard</a> <a href="/logout" style="color:red;">Sair</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        return template.replace("{{ content }}", f"<h2>Novo Artigo</h2>{form}")
