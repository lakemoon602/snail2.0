# 表名: snail
# 字段 id domain type payload time
# 0 -- 未检测出异常
# 1 -- 备份文件
# 2 -- .git
# 3 -- .svn
# 4 -- .dsstore
# 5 -- idea
# 6 --apache
import sqlite3

class DB:
    # 创建数据表
    def __init__(self):
        conn = sqlite3.connect('result.db')
        c = conn.cursor()
        try:
            c.execute('''create table snail
                (id INTEGER PRIMARY KEY,
                domain text not null,
                type int not null,
                payload  text  not null,
                time datetime default(  datetime( 'now', 'localtime' )   )
                );''')
            conn.commit()
            c.close()
            conn.close()
        except:
            c.close()
            conn.close()
    
    # 插入数据
    def insert(self,domain,type,payload):
        conn = sqlite3.connect('result.db')
        c = conn.cursor()
        exist=c.execute("select * from snail where domain='"+domain+"'")
        if not len(list(exist)):
            c.execute("insert into snail(domain,type,payload) values('"+domain+"',"+str(type)+",'"+payload+"')")
            conn.commit()
            conn.close()
            return
        conn.close()
    
    # 检查域名存在
    def check(self,domain):
        conn = sqlite3.connect('result.db')
        c = conn.cursor()
        exist=c.execute("select * from snail where domain='"+domain+"'")
        if not len(list(exist)):
            c.close()
            conn.close()
            return False
        c.close()
        conn.close()
        return True

    # 删除数据
    def delete(self,id):
        conn = sqlite3.connect('result.db')
        c = conn.cursor()
        c.execute("delete from snail where id="+str(id))
        c.close()
        conn.commit()
        conn.close()

if __name__ == "__main__":
    db=DB()
    db.insert('www.edu.cn',0,'测试')
    db.delete(5)
    print(db.check('www.edu.cn'))



