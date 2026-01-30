class LoginView:
    @staticmethod
    def render():

        with open("templates/base.html", "r", encoding="utf-8") as f:
            template = f.read()
        with open("templates/login.html", "r", encoding="utf-8") as f:
            login_form = f.read()

        nav_content = '<a href="/login">Login</a>'

        template = template.replace("{{ auth_links }}", nav_content)

        return template.replace("{{ content }}", f"<h2>User Login</h2>{login_form}")
