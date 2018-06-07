#coding=utf-8

#处理基本信息

__all__=['tackle_null','test']
def tackle_null(arg):
    # return [x.strip() for x in arg if x.strip()!=''] #要加入到mappose 中，需要返回一个value，而不是容器类型
    if arg.strip()!='':
        return  arg.strip()



def test():
    pass



