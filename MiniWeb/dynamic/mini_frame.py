from pymysql import connect
import re
import urllib.parse
import logging

URL_FUNC_DICT = dict()


# 路由
def route(url):
    def set_func(func):
        URL_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        return call_func

    return set_func


# 连接
def coon_():
    coon = connect(host='localhost', port=3306, user='root', password='123456', database='stock_db',
                   charset='utf8')
    cs = coon.cursor()
    return cs, coon


# 关闭
def close_(cs, coon):
    cs.close()
    coon.close()


@route(r"/index.html")
def index(ret):
    with open("./templates/index.html", encoding='utf-8') as f:
        content = f.read()
    cs, coon = coon_()
    cs.execute("select * from info")
    stock_infos = cs.fetchall()
    close_(cs, coon)
    tr_template = """<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
            </tr>
        """
    html = ""
    for line_info in stock_infos:
        html += tr_template % (
            line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],
            line_info[7], line_info[1]
        )
    content = re.sub(r"\{%content%\}", html, content)
    return content


@route(r"/center.html")
def center(ret):
    with open("./templates/center.html", encoding='utf-8') as f:  # 1.py中如果使用了open(),路径都是以运行的那个程序为基准算的。
        content = f.read()
    cs, coon = coon_()
    cs.execute(
        "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id;")
    stock_infos = cs.fetchall()
    close_(cs, coon)
    tr_template = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                </td>
            </tr>
        """
    html = ""
    for line_info in stock_infos:
        html += tr_template % (
            line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],
            line_info[0], line_info[0]
        )
    content = re.sub(r"\{%content%\}", html, content)
    return content


@route(r"/add/(\d+)\.html")
def add_focus(ret):
    stock_code = ret.group(1)
    cs, coon = coon_()
    sql = """select * from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():
        close_(cs, coon)
        return "没有这只股票大哥放过我吧"
    sql = """ select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    if cs.fetchone():
        close_(cs, coon)
        return "已经关注过了，请勿重复关注..."
    sql = """insert into focus (info_id) select id from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    coon.commit()
    close_(cs, coon)

    return "关注成功...."


@route(r"/del/(\d+)\.html")
def del_focus(ret):
    stock_code = ret.group(1)
    cs, coon = coon_()
    sql = """select * from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():
        close_(cs, coon)
        return "没有这只股票大哥放过我吧"
    sql = """ select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():
        close_(cs, coon)
        return "之前没有关注过，请勿取消关注"

    # sql = """insert into focus (info_id) select id from info where code=%s;"""
    sql = """delete from focus where info_id=(select id from info where code=%s);"""
    # sql = """insert into focus (info_id) values(select id from info where code=%s);""" # 因为select可能插入多条数据，所以不能用values。
    cs.execute(sql, (stock_code,))
    coon.commit()
    close_(cs, coon)
    return "取消关注成功...."


'''URL_FUNC_DICT={
    "/index.py": index,  # 函数的引用
    "/center.py": center,
}'''


@route(r"/update/(\d+)\.html")
def show_update_page(ret):
    stock_code = ret.group(1)
    '''展示修改页面'''
    with open("./templates/update.html", encoding='utf-8') as f:
        content = f.read()
    cs, coon = coon_()
    sql = """select f.note_info from focus as f inner join info as i on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    stock_infos = cs.fetchone()
    note_info = stock_infos[0]
    close_(cs, coon)

    content = re.sub(r"\{%note_info%\}", note_info, content, )
    content = re.sub(r"\{%code%\}", stock_code, content, )
    return content


@route(r"/update/(\d+)/(.*)\.html")
def save_update_page(ret):
    """"保存修改的信息"""
    stock_code = ret.group(1)
    comment = ret.group(2)
    comment = urllib.parse.unquote(comment)
    cs, coon = coon_()

    sql = """update focus set note_info=%s where info_id = (select id from info where code=%s);"""
    cs.execute(sql, (comment, stock_code))
    coon.commit()
    close_(cs, coon)
    return "修改成功..."


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])

    file_name = env['PATH_INFO']

    logging.basicConfig(level=logging.INFO,
                        filename='./log.txt',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    logging.info("访问的是，%s" % file_name)
    try:
        for url, func in URL_FUNC_DICT.items():
            # {
            #   r"/index.html":index,
            #   r"/center.html":center,
            #   r"/add/\d+\.html":add_focus
            # }
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            logging.warning("没有对应的函数....")
            return "请求的url(%s)没有对应的函数...." % file_name

    except Exception as ret:
        return "产生了异常：%s" % str(ret)


