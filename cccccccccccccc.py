from app01 import models

class AutoSale(object):
    users = None # [1,2,1,2,3,1,...]
    iter_users = None # iter([1,2,1,2,3,1,...])
    reset_status = False
    rollback_list = []

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

        cls.users = sale_id_list

    @classmethod
    def get_sale_id(cls):
        if cls.rollback_list:
            """
            可能存在已经取到了销售,也分配了,可是在写进数据库的过程中出现了问题,
            在customer.py里面,我们使用了事务,虽然事务回滚了,可是因为我们使用的是生成器,所以自己写了rollback方法
            """
            return cls.rollback_list.pop()

        if not cls.users:
            cls.fetch_users()
        # 如果没有课程顾问,就返回None
        if not cls.users:
            return None

        if not cls.iter_users:
            cls.iter_users = iter(cls.users)
        try:
            user_id = next(cls.iter_users)
        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        return user_id

    @classmethod
    def reset(cls):
        cls.reset_status = True

    @classmethod
    def rollback(cls,nid):
        cls.rollback_list.insert(0,nid)