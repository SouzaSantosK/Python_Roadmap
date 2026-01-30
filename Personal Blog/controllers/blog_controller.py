import os
from urllib.parse import parse_qs
from models.article import ArticleModel
from views.home_view import HomeView
from views.admin_view import AdminView
from views.article_view import ArticleView

from dotenv import load_dotenv  # Remova se não for usar o .env

from views.login_view import LoginView
from views.new_article_view import NewArticleView

load_dotenv()  # Remova se não for usar o .env


class BlogController:
    def __init__(self, request_handler):
        self.handler = request_handler
        self.path = request_handler.path
        self.model = ArticleModel()

    # --- Auth validation ---
    def is_authenticated(self):
        """Verifica manualmente se o header Cookie contém nossa sessão"""
        cookie_header = self.handler.headers.get("Cookie")
        if cookie_header and "session_id=admin_logado" in cookie_header:
            return True
        return False

    # --- GET ---
    def handle_request(self):
        if self.path == "/static/style.css":
            self.serve_static("static/style.css", "text/css")
            return

        if self.path.startswith("/admin"):
            if not self.is_authenticated():
                self.handler.send_response(303)
                self.handler.send_header("Location", "/login")
                self.handler.end_headers()
                return

        if self.path == "/":
            self.show_home()
        elif self.path == "/login":
            if self.is_authenticated():
                self.handler.send_response(303)
                self.handler.send_header("Location", "/admin")
                self.handler.end_headers()
                return
            self.show_login_form()
        elif self.path == "/admin":
            self.show_dashboard()
        elif self.path == "/admin/new":
            self.show_new_article_form()
        elif self.path.startswith("/article/"):
            self.show_article()
        elif self.path.startswith("/admin/edit"):
            self.show_edit_form()
        elif self.path == "/logout":
            self.logout()
        else:
            self.send_not_found()

    # --- POST ---
    def handle_post_request(self):
        if self.path.startswith("/admin"):
            if not self.is_authenticated():
                self.handler.send_response(303)
                self.handler.send_header("Location", "/login")
                self.handler.end_headers()
                return

        if self.path == "/login":
            self.login()
        elif self.path == "/admin/new":
            self.create_article()
        elif self.path == "/admin/delete":
            self.delete_article()
        elif self.path.startswith("/admin/edit"):
            self.update_article()

    def serve_static(self, file_path, mime_type):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.handler.send_response(200)
            self.handler.send_header("Content-type", mime_type)
            self.handler.end_headers()
            self.handler.wfile.write(content)
        except FileNotFoundError:
            self.send_not_found()

    # --- Response ---
    def send_response(self, content, status=200):
        self.handler.send_response(status)
        self.handler.send_header("Content-type", "text/html; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write(content.encode("utf-8"))

    # --- Views ---
    def show_home(self):
        articles = self.model.get_all()
        logged = self.is_authenticated()
        html_content = HomeView.render(articles, is_logged_in=logged)
        self.send_response(html_content)

    def show_login_form(self):
        html_content = LoginView.render()
        self.send_response(html_content)

    def show_article(self):
        try:
            article_id = int(self.path.split("/")[-1])
            article = self.model.get_by_id(article_id)

            if article:
                html_content = ArticleView.render(article)
                self.send_response(html_content)
            else:
                self.send_not_found()
        except ValueError:
            self.send_not_found()

    def login(self):
        content_length = int(self.handler.headers["Content-Length"])
        post_data = self.handler.rfile.read(content_length).decode("utf-8")
        fields = parse_qs(post_data)

        username = fields.get("username", [""])[0]
        password = fields.get("password", [""])[0]

        if username == "admin" and password == "admin":
            self.handler.send_response(303)
            self.handler.send_header(
                "Set-Cookie", "session_id=admin_logado; Path=/; HttpOnly"
            )
            self.handler.send_header("Location", "/admin")
            self.handler.end_headers()
        else:
            self.send_response(
                "<h1>Erro: Usuário ou senha inválidos</h1><a href='/login'>Voltar</a>"
            )

    def show_dashboard(self):
        articles = self.model.get_all()
        html_content = AdminView.render_dashboard(articles)
        self.send_response(html_content)

    def show_edit_form(self):
        article_id = int(self.path.split("/")[-1])
        article = self.model.get_by_id(article_id)
        if article:
            html_content = AdminView.render_edit_form(article)
            self.send_response(html_content)
        else:
            self.send_not_found()

    def show_new_article_form(self):
        html_content = NewArticleView.render()
        self.send_response(html_content)

    def create_article(self):
        content_length = int(self.handler.headers["Content-Length"])
        post_data = self.handler.rfile.read(content_length).decode("utf-8")
        fields = parse_qs(post_data)

        self.model.create(
            fields.get("title")[0], fields.get("content")[0], fields.get("date")[0]
        )
        self.handler.send_response(303)
        self.handler.send_header("Location", "/admin")
        self.handler.end_headers()

    def delete_article(self):
        content_length = int(self.handler.headers["Content-Length"])
        post_data = self.handler.rfile.read(content_length).decode("utf-8")
        fields = parse_qs(post_data)

        article_id = fields.get("id", [None])[0]

        if article_id:
            self.model.delete(article_id)

        self.handler.send_response(303)
        self.handler.send_header("Location", "/admin")
        self.handler.end_headers()

    def update_article(self):
        article_id = int(self.path.split("/")[-1])
        content_length = int(self.handler.headers["Content-Length"])
        post_data = self.handler.rfile.read(content_length).decode("utf-8")
        fields = parse_qs(post_data)

        self.model.update(
            article_id,
            fields.get("title")[0],
            fields.get("content")[0],
            fields.get("date")[0],
        )

        self.handler.send_response(303)
        self.handler.send_header("Location", "/admin")
        self.handler.end_headers()

    def logout(self):
        self.handler.send_response(303)
        self.handler.send_header(
            "Set-Cookie", "session_id=; Path=/; HttpOnly; Max-Age=0"
        )
        self.handler.send_header("Location", "/")
        self.handler.end_headers()

    def get_base_template(self):
        with open("templates/base.html", "r", encoding="utf-8") as f:
            content = f.read()

        auth_html = (
            '<a href="/logout">Sair</a>'
            if self.is_authenticated()
            else '<a href="/login">Entrar</a>'
        )
        return content.replace("{{ auth_links }}", auth_html)

    def send_not_found(self):
        self.send_response("<h1>404 - Página não encontrada</h1>", status=404)
