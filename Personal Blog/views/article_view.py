class ArticleView:
    @staticmethod
    def render(article, is_logged_in=False):

        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()

        if is_logged_in:
            nav_content = '<a href="/admin">Dashboard</a> <a href="/logout" style="color:red;">Sair</a>'
        else:
            nav_content = '<a href="/login">Login</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        paragraphs = article.content.split("\n")

        paragraphs_html = "\n".join(f"<p>{p}</p>" for p in paragraphs if p.strip())

        article_html = f"""
            <div>
                <h2>{article.title}</h2>
                <span>{article.date}</span>
                {paragraphs_html}
            </div>
            """

        return template.replace("{{ content }}", article_html)
