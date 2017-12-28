# from abc import ABCMeta
# from abc import abstractmethod
#
# 抽象方法:
# class BaseMessage(metaclass=ABCMeta):
#
#     @abstractmethod
#     def send(self,subject,body,to,name):
#         pass

# 抽象类
class BaseMessage(object):
    def send(self, subject, body, to, name):
        """
        必须满足该参数要求
        :param subject:  主题
        :param body:  发送内容
        :param to:  收件人
        :param name:  发件人
        :return:  要使用必须使用send方法
        """
        raise NotImplementedError('未实现send方法')



# 通过反射,可以实现解耦降低的功能,
# 只要我们修改配置文件,就自动全部都生效
# 这是参考django中间件的源码实现    #   动态导入模块 + 反射  这种模式叫做工厂模式

# 类的约束:   抽象方法抽象类
#           抽象方法 : @abstractmethod
#           抽象类 : 如上