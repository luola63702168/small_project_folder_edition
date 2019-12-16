import socket
import re
import multiprocessing
import time
import sys


class WSGIServer(object):

    def __init__(self, port, app, static_path):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("192.168.233.1", port))
        self.tcp_socket.listen(128)
        self.application = app
        self.static_path = static_path

    def service_client(self, client_socket):
        client_request = client_socket.recv(1024).decode("utf-8")
        client_request_lines = client_request.splitlines()
        print(">>" * 20)
        print(client_request_lines)
        ret = re.match(r"[^/]+(/[^ ]*)", client_request_lines[0])
        file_name = ""
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"

        # 静动态处理
        if not file_name.endswith(".html"):
            try:
                f = open(self.static_path + file_name, "rb")
                html_content = f.read()
                f.close()
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # body
                client_socket.send(response.encode("gbk"))
                client_socket.send(html_content)
            except Exception as a:
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                response += "<h1>---没有你要的地址---</h1>"
                client_socket.send(response.encode("gbk"))
        else:

            env = dict()
            env["PATH_INFO"] = file_name
            body = self.application(env, self.set_response_header)

            header = "HTTP/1.1 %s\r\n" % self.status
            for temp in self.headers:
                header += "%s:%s\r\n" % (temp[0], temp[1])
            header += "\r\n"

            response = header + body
            client_socket.send(response.encode("utf-8"))

        client_socket.close()

    def set_response_header(self, status, headers):

        self.status = status
        self.headers = [("server", "mini_web v8.8")]
        self.headers += headers

    def run_forever(self):
        while True:
            client_socket, client_addr = self.tcp_socket.accept()
            p = multiprocessing.Process(target=self.service_client, args=(client_socket,))
            p.start()
            client_socket.close()


def main():
    '''调用run_forever方法运行'''
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            frame_app_name = sys.argv[2]
        except Exception as a:
            print("端口输入错误")
            return
    else:
        print("请按照以下方式运行")
        print("python xx.py '端口号'--例如：7890 框架名及调用的函数：例如： mini_frame:application")
        return
    ret = re.match(r"([^:]+):(.*)", frame_app_name)
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)
    else:
        print("请按照以下方式运行")
        print("python xx.py '端口号'--例如：7890 框架名及调用的函数：例如： mini_frame:application")
        return
    with open("./web_server.conf", encoding='utf-8') as f:
        conf_info = eval(f.read())
    sys.path.append(conf_info['dynamic_path'])
    frame = __import__(frame_name)
    app = getattr(frame, app_name)
    wsgi_server = WSGIServer(port, app, conf_info['static_path'])
    wsgi_server.run_forever()


if __name__ == '__main__':
    main()
