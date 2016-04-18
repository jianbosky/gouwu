#!/usr/bin/env python3.5
# -*-coding:utf8-*-
'''
-----------------
lock.txt:
alex
-----------------
user.txt:
jjb 123456
------------------
'''
import os
import sys
def deny_account(username):
    print('您的用户已被锁定！')
    with open('lock.txt', 'a') as deny_f:
        deny_f.write(username+'\n')
def main():
    i = 0
    while i < 3:
        # 输入用户名
        username = input('请输入用户名:')
        with open('lock.txt', 'r') as lock_f:
            # 匹配登陆用户是否在黑名单里
            for x_name in lock_f.readlines():
                if len(x_name) == 0:
                    continue
                if username == x_name.strip():
                    print("用户 %s 已经被锁定!" % username)
                    sys.exit()
        # 如果用户名为空重新输入
        if len(username) == 0:
            print('用户名不能为空，请重新输入')
            continue
        # 设置标志位
        flag = False
        # 打开用户名文件，将里面的用户名与输入的进行匹配，匹配成功，则进行密码匹配，否则提示用户名输入错误
        with open('user.txt', 'r') as account_f:
            for line in account_f.readlines():
                user_txt, pass_txt,money_txt = line.strip().split()
                if username == user_txt:
                    passward = input('请输入密码:').strip()
                    # 将用户名和对应密码分别赋给两个变量
                    if username == user_txt and passward == pass_txt:
                        # 登陆成功改变标志位
                        flag = True
                        money =money_txt
                        # 跳出for 循环
                        break

                    else:
                        if i < 2:
                            print('您输入的密码有误，请重新输入！')
                        i += 1
                        break
            else:
                print(' 您输入的用户名不存在！')
        if flag == True:
            # 登陆成功跳出登陆验证，转入购物商城主界面
            return sale(username,money)
            # 跳出while 循环
            break

    else:
        # 密码输入超过三次，将用户名锁定到黑名单
        deny_account(username)
# 修改用户金钱函数,参数username为需要修改的用户名，newmoney为新的金额
def modifmoney(username,newmoney):
    with open("user.txt", "r")as f:
        # 将数据赋值给列表
        fline = f.readlines()
        # 获取记录数
        lline = len(fline)
        for line in range(lline):
            # 定位修改金额的用户名
            if username ==fline[line].split()[0]:
                a = fline[line].split()[0]
                b = fline[line].split()[1]
                # 修改金额
                modi="%s %s %s\n"%(a,b,newmoney)
                # 将修改后的数据替换之前的数据
                fline[line] = modi
        # 将新数据写入文件中
        with open("user.txt", "w")as fd:
            fd.writelines(fline)
            fd.close()
def sale(username,money):
    print('欢迎用户%s进入购物商城,你当前可用金额为:%s元' % (username,money))
    print("以下是商品信息，请按键选择商品，进入购买界面！")
    item = {1:{"苹果":"4"},2:{"香焦":"2"},3:{"桔子":"3"},4:{"菠萝":"3"}}
    for k,v in item.items():
        for x,y in v.items():
            print("%s、%s：%s元/斤"%(k,x,y))

    num =int(input("请输入要购买商品的编号：").strip())
    if num in item:
        for k1 in item[num]:
            v1=(item[num][k1])
            shulian = int(input("你选择的是'%s'单价为:%s元/斤，请输入要购买的数量，单位（斤）:" %(k1,v1)).strip())
            # 调用购物车方法
            gouwuche(username, money, k1, shulian,num)
            xy=input("加入购物车成功，查看购车请按“1”结算请选择“2”还需购买请选择“3”").strip()
            if xy == "1":
                return show(username,money,item)
            elif xy == "2":
                return jieshan(username,money,item)
            elif xy == "3":
                return sale(username,money)
    else:
        print("输入错误,请重新输入\n\n")
        return sale(username,money)
def gouwuche (username, money, k1, shulian,num):
    xz = input("你选择了'%s',数量%s斤，是|否确认加入购物车:：是｜否" %(k1,shulian)).strip()
    if xz == "是":
        # 判断是否存在该用户的购物车文件
        gw = "%s %s\n" % (num, shulian)
        if os.path.isfile("%s.txt" % username)  == True:
            # 如果是购物车存在则修改
            with open("%s.txt" % username, "r")as xf:
                lines = xf.readlines()
                l = len(lines)
                for i in range(l):
                    # 如果购物车存在该条数据则进行修改
                    if num == int(lines[i].split()[0]):
                        old_ = int(lines[i].split()[1])
                        new_ = old_ + shulian
                        # 如果该记录是最后修改数据后面不换行
                        if i == l:
                            new = "%s %s" %(num,new_)
                        # 否则换行
                        else:
                            new = "%s %s\n" %(num,new_)
                        # 修改原数据
                        lines[i] = new
                        # 跳出for循环写入修改数据
                        break
                # 如果购物车不存在该条数据则在记录最后进行新增
                else:
                    lines.append(gw)
                # 将更改后的数据写入文件
                with open("%s.txt" % username, "w")as f:
                    f.writelines(lines)
                return 0
        else:
            with open("%s.txt" % username, "w") as f:
                f.writelines(gw)
            return 0
    elif xz == "否":
        return sale(username,money)
    else:
        return gouwuche(username,money, k1, shulian,num)
def show(username,money,item):
    with open("%s.txt"%username,"r") as f:
        data = f.readlines()
        total = 0
        for i in data:
            xnum,xdata = i.strip().split()
            ixnum = int(xnum)
            ixdata = int(xdata)
            for i in item[ixnum]:
                v2 = item[ixnum][i]
                total += (int(v2) * ixdata)
                print("""
                 －－－－－－－－－－－－－－－－－－－－－－
                 商品编号 商品名称   商品单价   商品数量   商品金额
                     %s        %s         %s        %s       %d """%(ixnum,i,v2,ixdata,(int(v2) * ixdata)))

    print("你的购物车总金额为:%s 元." % total)
    tell2=input("请选择：1、清空购物车，2、返回继续购物，3、商品结算 ：")
    if tell2 == "1":
        os.remove("%s.txt"%username)
        print("购物车已清空，请重新购物")
        sale(username,money)
    elif tell2 == "2":
        sale(username,money)
    elif tell2 == "3":
        jieshan(username,money,item)
    else:
        show(username,money,item)
def jieshan(username,money,item):
    imoney = int(money)
    with open("%s.txt"%username,"r") as f:
        data = f.readlines()
        total = 0
        for i in data:
            xnum,xdata = i.strip().split()
            ixnum = int(xnum)
            ixdata = int(xdata)
            for i in item[ixnum]:
                v2 = item[ixnum][i]
                total += (int(v2) * ixdata)
    if imoney < total:
        print("你购物车内的商品总价格为：%s元，已超过你的可用金额%s元,请返回购物车修改商品" %(total,money))
        show(username,money,item)
    else:
        # 商品价格扣款
        newmoney = imoney - total
        # 更改用户数据文件
        modifmoney(username,newmoney)
        # 清空购物车
        os.remove("%s.txt"%username)
        print("结算成功你当前可用余额为:%s" %newmoney)
        tell = input("感谢你的选购，请选择是否继续购买：是｜否")
        if tell == "是":
            sale(username,newmoney)
        else:
            print("谢谢光临，再见！")
            sys.exit()

# 程序执行入口
if __name__ == '__main__':
    main()





