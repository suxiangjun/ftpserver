#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socketserver
import hashlib
import socket,os,shelve,sys,time,logging
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_basedir=basedir+'/home/'
sys.path.append(basedir)
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.user_login()
        while True:
            try:
                self.data = self.request.recv(1024)
                while True:
                    if self.data.decode()=="1":
                        self.check_file()
                        break
                    elif self.data.decode()=="2":
                        self.data1=self.request.recv(1024)
                        print("{0}下载文件:".format(self.client_address[0]))
                        if not self.data1:
                            print("客户端已断开")
                            break
                        filename = self.data1.decode().split()[1]
                        self.log("{}用户下载{}文件".format(self.username,filename))
                        if os.path.isfile(user_basedir+self.username+'/'+filename):
                            m = hashlib.md5()  # 生成MD5的对象
                            self.request.send("y".encode())
                        else:
                            self.request.send("n".encode())
                            break
                        with open(user_basedir+self.username+'/'+filename, "rb") as f:
                            file_size = os.stat(user_basedir+self.username+'/'+filename).st_size
                            self.request.send(str(file_size).encode()) # send file size
                            self.request.recv(1024)
                            for line in f:
                                m.update(line)  # 计算md5值
                                self.request.send(line)
                            print("file md5", m.hexdigest())
                        self.request.recv(1024)  # 等待客户确认发送MD5值
                        self.request.send(m.hexdigest().encode())  # 生成MD5值并且发送给客户端
                        break
                    elif self.data.decode() == "3":
                        self.upload_file()
                        break
            except ConnectionResetError or IndexError as e:
                print("error:", e)
                break
    #用户登陆控制
    def user_login(self):
        self.username=self.request.recv(1024).decode()
        f=shelve.open(basedir+'/data/password')
        if self.username not in f:
            a="%s不存在，请注册"%self.username
            self.request.send(str([a,1]).encode())
            self.username_password=eval(self.request.recv(1024).decode())
            self.username=self.username_password[0]
            self.password=self.username_password[1]
            os.mkdir(basedir+"/home/"+self.username)
            self.dirhome=basedir+ "/home/"+self.username
            # self.username_password.append(self)  #[username,password,self]
            f[self.username_password[0]]=self.username_password
            f.close()
            self.request.send("恭喜你注册成功，请重新登陆。".encode())
            self.log("新注册%s用户"%self.username)
        else:
            self.request.send(str(["欢迎回来",f[self.username][1]]).encode())
            print("\33[32m{}\33[0m {}成功登陆".format(time.asctime(),self.username))
            self.log("%s用户成功登陆" % self.username)
            f.close()
    #查看家目录文件
    def check_file(self):
        self.dirhome=basedir+"/home/"+self.username
        self.filename=os.listdir(self.dirhome)
        self.request.send(str(self.filename).encode())
    #上传文件
    def upload_file(self):
        while True:
            self.request.send("ack".encode())
            filename = self.request.recv(1024).decode()
            self.request.send("ack".encode())
            file_total_size=int(self.request.recv(1024).decode())
            print(file_total_size)
            revived_size = 0
            self.request.send("ack".encode())
            with open(user_basedir +self.username+'/'+filename, "wb") as f:
                while revived_size < file_total_size:
                    data = self.request.recv(1024)
                    revived_size += len(data)
                    f.write(data)
                self.request.send("file upload done".encode())
                print("\33[32m{}\33[0m{}成功上传{}文件".format(time.asctime(),self.username,filename))
                self.log("{}成功上传{}文件".format(self.username,filename))
                break

    @staticmethod
    def log(info):
        logging.basicConfig(filename=basedir + "/log/" + "ftp.log",
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S %p')
        logging.info(info)
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)  # 采用ThreadingTCPServer多线程方式实例化
    server.serve_forever()
    server.server_close()