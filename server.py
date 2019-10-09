from http.server import HTTPServer, CGIHTTPRequestHandler


class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]


PORT = 3000
httpd = HTTPServer(("", PORT), Handler)
httpd.serve_forever()
