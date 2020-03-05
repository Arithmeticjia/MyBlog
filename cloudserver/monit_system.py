import pymysql
import gevent
import time
import psutil


class MyPyMysql:
    def __init__(self, host, port, username, password, db, charset='utf8'):
        self.host = host  # mysql主机地址
        self.port = port  # mysql端口
        self.username = username  # mysql远程连接用户名
        self.password = password  # mysql远程连接密码
        self.db = db  # mysql使用的数据库名
        self.charset = charset  # mysql使用的字符编码,默认为utf8
        self.pymysql_connect()  # __init__初始化之后，执行的函数

    def pymysql_connect(self):
        # pymysql连接mysql数据库
        # 需要的参数host,port,user,password,db,charset
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset
                                    )
        # 连接mysql后执行的函数
        self.asynchronous()

    def getCPUstate(self,interval=1):
        cpu = psutil.cpu_percent(interval)
        return cpu

    def getMemorystate(self):
        phymem = psutil.virtual_memory()
        cur_mem = phymem.percent
        mem_rate = int(phymem.used / 1024 / 1024)
        mem_all = int(phymem.total / 1024 / 1024)

        line = {
            'cur_mem': cur_mem,
            'mem_rate': mem_rate,
            'mem_all': mem_all,
        }

        return line

    def run(self):
        # 创建游标
        self.cur = self.conn.cursor()
        # 定义sql语句
        sql = "insert into cloudserver_system_monit(cpu,cur_mem,mem_rate,mem_all,create_time,time_stamp) values (%s,%s,%s,%s,%s,%s)"
        print(sql)

        # 定义数据
        cpu = self.getCPUstate()  # cpu使用率
        mem = self.getMemorystate()  # 内存info信息
        mem_rate = mem['mem_rate']  # 内存使用率
        cur_mem = mem['cur_mem']  # 当前使用内存
        mem_all = mem['mem_all']  # 总内存
        struct_time = time.localtime()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 转换为标准时间
        t = time.time()  # 当前时间戳
        time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳

        print((cpu, cur_mem,mem_rate, mem_all,create_time,time_stamp))

        # 执行插入一行数据，如果插入多行，使用executemany(sql语句,数据(需一个元组类型))
        content = self.cur.execute(sql,(cpu,cur_mem,mem_rate,mem_all,create_time,time_stamp))
        if content:
            print('插入ok')

        # 提交数据,必须提交，不然数据不会保存
        self.conn.commit()

    def asynchronous(self):
        #执行30次协程任务
        for i in range(0,30):
            time.sleep(10)  # 等待10秒
            gevent.spawn(self.run())  # 执行方法

        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭pymysql连接

if __name__ == '__main__':
    start_time = time.time()  # 计算程序开始时间
    st = MyPyMysql('101.132.70.184', 3306, 'root', '980612ssj@%', 'MyBlog')  # 实例化类，传入必要参数
    print('程序耗时{:.2f}'.format(time.time() - start_time))  # 计算程序总耗时


