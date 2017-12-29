import redis
from app01 import models

POOL = redis.ConnectionPool(host='192.168.20.150',port=6379)
# host是服务端的，这个port是redis固定的，只要是连接redis的这个port就固定是6379，密码是服务端设置的。
CONN = redis.Redis(connection_pool=POOL)


class AutoSale(object):

    @classmethod
    def fetch_users(cls):
        # [obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),]
        sales = models.SaleRank.objects.all().order_by('-weight')
        print(sales)
        sale_id_list = []
        count = 0
        while True:
            flag = False
            for row in sales:
                if count < row.num:
                    sale_id_list.append(row.user_id)
                    flag = True
            count += 1
            if not flag:
                break
        print('sale_id_list===',sale_id_list)
        if sale_id_list:
            CONN.rpush('sale_id_list',*sale_id_list)        # 用来操作的数据
            CONN.rpush('sale_id_list_origin',*sale_id_list) # 保留一份源数据
            return True
        return False


    @classmethod
    def get_sale_id(cls):
        # 查看原来数据是否存在
        sale_id_origin_count = CONN.llen('sale_id_list_origin')
        if not sale_id_origin_count:
            # 取数据库中获取数据，并且赋值list_origin,pop数据
            status = cls.fetch_users()
            if not status:
                return None
            user_id = CONN.lpop('sale_id_list')
            if user_id:
                return user_id

            reset = CONN.get('sale_id_reset')
            if reset:
                CONN.delete('sale_id_list_origin')
                status = cls.fetch_users()
                if not status:
                    return None
                CONN.delete('sale_id_reset')
                return CONN.lpop('sale_id_list')
            else:
                ct = CONN.llen('sale_id_list_origin')
                for i in range(ct):
                    v = CONN.lindex('sale_id_list_origin',i)
                    CONN.rpush('sale_id_list',v)
                return CONN.lpop('sale_list_id')

        # if cls.rollback_list:
        #     """
        #     可能存在已经取到了销售,也分配了,可是在写进数据库的过程中出现了问题,
        #     在customer.py里面,我们使用了事务,虽然事务回滚了,可是因为我们使用的是生成器,所以自己写了rollback方法
        #     """
        #     return cls.rollback_list.pop()
        #
        # if not cls.users:
        #     cls.fetch_users()
        # # 如果没有课程顾问,就返回None
        # if not cls.users:
        #     return None
        #
        # if not cls.iter_users:
        #     cls.iter_users = iter(cls.users)
        # try:
        #     user_id = next(cls.iter_users)
        # except StopIteration as e:
        #     if cls.reset_status:
        #         cls.fetch_users()
        #         cls.reset_status = False
        #     cls.iter_users = iter(cls.users)
        #     user_id = cls.get_sale_id()
        # return user_id

    @classmethod
    def reset(cls):
        CONN.set('sale_id_reset',1)

    @classmethod
    def rollback(cls,nid):
        # cls.rollback_list.insert(0,nid)
        CONN.lpush('sale_id_list',nid)   # callback的id，往前面放
