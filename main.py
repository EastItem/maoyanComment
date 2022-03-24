import requests, json, time, datetime
import pandas as pd


# 请求评论api接口
def requestApi(url):
    headers = {
        'accept': '*/*',
        'cookie':'_lxsdk_cuid=17c98dcd4f8c8-0851bee51fa5f4-b7a1438-144000-17c98dcd4f8c8; uuid_n_v=v1; iuuid=91A3062030EF11ECAD67C15A730A616B2C87709EE65B4F3DA671AD34B7E7B5EB; ci=20%2C%E5%B9%BF%E5%B7%9E; ci=20%2C%E5%B9%BF%E5%B7%9E; ci=20%2C%E5%B9%BF%E5%B7%9E; _lxsdk=441FC6E030E511ECA37A37EAE64823DF58D4AA1CFEAD431685D0A377FDBA482B; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1634652182,1634821534; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=216251049.1634652182488.1634821538887.1634822077832.6' ,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        if "verify" in r.url :
            print('需要验证！建议自行访问上条URL，需要验证的url为',r.url)
            input('输入继续')
            raise Exception
        else:
            return r.text

    except requests.HTTPError as e:
        print(e)
    except requests.RequestException as e:
        print(e)
    except:
        print("出错了")
        raise Exception


# 解析接口返回数据
def getData(html):

    json_data = json.loads(html)['cmts']
    comments = []

    # 解析数据并存入数组
    try:
        for item in json_data:

            comment = []
            comment.append(item['nickName'])
            comment.append(item['cityName'] if 'cityName' in item else '')
            comment.append(item['content'].strip().replace('\n', ''))
            comment.append(item['score'])
            comment.append(item['startTime'])
            comment.append(item['approve'])
            comments.append(comment)

        return comments

    except Exception as e:
        print(comment)
        print(e)


# 保存数据，写入excel
def saveData(comments):
    filename = './newmovieComments2.csv'

    dataObject = pd.DataFrame(comments)
    dataObject.to_csv(filename, mode='a', index=False, sep=',', header=False)


# 爬虫主函数
def main():
    # 当前时间

    #访问上次中断的时间
    try:
        with open('save.txt', 'r') as fw:
            start_time=fw.read()
            print(start_time)
    except:
        start_time=datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')

    # 电影上映时间
    end_time = '2021-07-09  00:00:00'

    while start_time > end_time:
        url = 'https://m.maoyan.com/mmdb/comments/movie/1337700.json?_v_=yes&offset=0&startTime=' + start_time.replace(
            '  ', '%20')
        html = None
        print(url)
        try:
            html = requestApi(url)

        except Exception as e:  # 如果有异常,暂停一会再爬
            time.sleep(10)
            html = requestApi(url)

        # else: #开启慢速爬虫
        time.sleep(3)
        comments = getData(html)

        # print(url)=
        start_time = comments[len(comments)-1][4]  # 获取每页中最后一条评论时间,每页有15条评论
        # print(start_time)

        # 最后一条评论时间减一秒，避免爬取重复数据
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d  %H:%M:%S') + datetime.timedelta(seconds=-1)
        start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d  %H:%M:%S')
        print(start_time)

        with open('save.txt', 'w') as fw:
            fw.write(start_time)
        saveData(comments)


if __name__ == '__main__':
     main()

