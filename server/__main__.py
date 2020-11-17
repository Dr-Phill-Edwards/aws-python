import signal
import sys
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from server.FileHandler import FileHandler
from server.messages import message

class MessageHandler(RequestHandler):
    def post(self):
        event = {"message": self.get_argument('message'), "headers": self.request.headers}
        context = {}
        self.write(message(event, context))


define("port", default=8080, help="Listener port")
options.parse_command_line()
application = Application([
    ('/api/messages', MessageHandler),
    ('/()$', FileHandler, {'path': "client/index.html"}),
    ('/(.*)', FileHandler, {'path': "client"}),
])
http_server = HTTPServer(application)
http_server.listen(options.port)
print("Listening on port", options.port)
try:
    IOLoop.current().start()
except KeyboardInterrupt:
   print("Exiting")
   IOLoop.current().stop()
