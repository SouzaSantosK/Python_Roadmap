from http.server import HTTPServer, BaseHTTPRequestHandler
from controllers.blog_controller import BlogController


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        controller = BlogController(self)
        controller.handle_request()

    def do_POST(self):
        controller = BlogController(self)
        controller.handle_post_request()


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor iniciado em http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
