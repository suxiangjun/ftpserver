#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
import socket, hashlib,os,sys,time
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basedir1=os.path.dirname(os.path.abspath(__file__) )
sys.path.append(basedir)
class My_ftp(object):
    #登陆ftp
    def login(self):
        while True:
            self.client = socket.socket()
            self.client.connect(("localhost", 9999))
            self.username=input("FTP账号：")
            self.client.send(self.username.encode())
            received1=eval(self.client.recv(1024).decode())
            if received1[1]==1:
                print(received1[0])
                self.username=input("新账号名：")
                for i in range(3):
                    self.password1=input("密码：")
                    if not self.password1:continue
                    self.password2=input("请再输入一次：")
                    if not self.password2: continue
                    if self.password1==self.password2:
                        d=str([self.username,self.password1])
                        self.client.send(d.encode())   #发送用户名和密码到服务端
                        print(self.client.recv(1024).decode())
                        self.client.close()
                        break
                else:
                    print("输错3次，再见")
                    sys.exit()
            else:
                print(received1[0])
                for i in range(3):
                    password=input("密码：")
                    if not password:continue
                    if password==received1[1]:
                        self.run(self.client)
                        sys.exit()
                else:
                    print("输错3次，再见")
                    sys.exit()
    #下载文件
    def download(self,client):
        client.send("2".encode())
        time.sleep(0.1)
        while True:
            cmd = input("格式:get filename>>").strip()
            if len(cmd) == 0: continue
            if cmd.startswith("get"):
                client.send(cmd.encode())
                y_n=client.recv(1024).decode()
                if y_n=="y":
                    server_respose = client.recv(1024)
                    print("文件大小: %s bytes"%server_respose.decode() )
                    client.send("ready to recv file".encode())
                    file_total_size = int(server_respose.decode())
                    revived_size = 0
                    filename = cmd.split()[1]
                    m = hashlib.md5()  # 生成MD5对象
                    with open(filename + ".new", "wb") as f:
                        while revived_size < file_total_size:
                            data = client.recv(1024)
                            revived_size += len(data)
                            m.update(data)  # 计算数据接收的MD5值
                            f.write(data)
                        else:
                            print(file_total_size, revived_size)
                            client_md5_vaule = m.hexdigest()  # 生成接收数据的MD5值16进制形式
                            client.send("ready to recv file md5 value".encode())
                            server_md5_value = client.recv(1024)  # 接收客户端的MD5值
                            if client_md5_vaule == server_md5_value.decode():  # 客户端和服务端的MD5值做比较
                                print("file recv done")
                                break
                            else:
                                print(client_md5_vaule, server_md5_value.decode())
                else:
                    print("文件不存在")
                    break
            else:
                break

    #查看文件
    def check_file(self,client):
        client.send("1".encode())
        allfile=eval(client.recv(10240).decode())
        print("我的文件")
        for i in allfile:
             print("\33[31m%s\33[0m"%i)

    #上传文件
    def upload(self,client):
        client.send("3".encode())
        while True:
            up_file=input("格式:upload filename>>".strip())
            if not up_file:continue
            elif up_file=="q":break
            if up_file.startswith("upload"):
                file=up_file.split()[1]
                if os.path.isfile(basedir1+'/'+file):
                    file_size = os.stat(basedir1+'/'+file).st_size
                    print("文件大小为：%s bytes"% file_size)
                    client.recv(1024)
                    client.send(file.encode())
                    client.recv(1024)
                    client.send(str(file_size).encode())
                    client.recv(1024)
                    with open(basedir1+'/'+file, "rb") as f:
                        client.sendall(f.read())
                        print(client.recv(1024).decode())
                        break
            else:
                print("格式错误，请重新输入")
                break

    def run(self,client):
        while True:
            choice=input("1.查看文件\n2.下载文件\n3.上传文件\n>>")
            if choice=="1":
                self.check_file(client);continue
            elif choice=="2":
                self.download(client);continue
            elif choice=="3":
                self.upload(client);continue
            else:
                break
c=My_ftp()
c.login()

