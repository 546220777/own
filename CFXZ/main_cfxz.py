# Author: ss
# Date: 2021年9月5日
# Version: 1.1
# UpdateDate: 2021年9月5日
# UpdateLog: 1、感谢leeyiding(乌拉)大佬，本版本在上版本基础上修改
#            2、财富小镇更新做任务基本上所有任务都完成，除了老年那个活动其他如果有活动未完成请反馈，反正也不一定有时间改
#            3、 另外希望服务器提供者清空一下数据库~修改后本期可以继续使用！

import requests
import json
import os
import sys
import time
import re
import random
import urllib.parse
import logging

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
global msg
msg = ''


# 自行修改推送参数
def wxpush(msg, usr='@all', corpid='ww7305', corpsecret='aKVVk',
           agentid='1000002'):
    """
    企业微信推送
    """
    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    corpid = corpid
    corpsecret = corpsecret
    agentid = agentid

    if agentid == 0:
        agentid = 1000002

    def get_access_token(_base_url, _corpid, _corpsecret):
        """
        获取access_token，每次的access_token都不一样，所以需要运行一次请求一次
        """
        urls = _base_url + 'corpid=' + _corpid + '&corpsecret=' + _corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(_msg, _usr):
        """
        发送消息
        """
        data = get_message(_msg, _usr)
        req_urls = req_url + get_access_token(base_url, corpid, corpsecret)
        res = requests.post(url=req_urls, data=data)
        ret = res.json()
        if ret["errcode"] == 0:
            print(f"[{now}] 企业微信推送成功")
        else:
            print(f"[{now}] 推送失败：{ret['errcode']} 错误信息：{ret['errmsg']}")

    def get_message(_msg, _usr):
        """
        获取消息
        """
        data = {
            "touser": _usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": _msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

    msg = msg
    usr = usr
    if corpid == '':
        print("[注意] 未提供corpid，不进行企业微信推送！")
    elif corpsecret == '':
        print("[注意] 未提供corpsecret，不进行企业微信推送！")
    else:
        send_message(msg, usr)


class getCCB():
    def __init__(self, cookies, shareCode):
        self.cookies = cookies
        self.ua = 'Mozilla/5.0 (Linux; Android 11; Redmi K30 5G Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045613 Mobile Safari/537.36 MMWEBID/6824 micromessenger/8.0.1.1841(0x28000151) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
        shareCodeKeys = shareCode.keys()
        if (not 'common' in shareCodeKeys):
            shareCode['common'] = []
        if (not 'whcanswer' in shareCodeKeys):
            shareCode['whcanswer'] = []
        if (not 'xbanswer' in shareCodeKeys):
            shareCode['xbanswer'] = []
        if (not 'xbpickon' in shareCodeKeys):
            shareCode['xbpickon'] = []
        self.commonShareCode = shareCode['common']
        self.xbpickonShareCode = shareCode['xbpickon']
        self.whcanswerShareCode = shareCode['whcanswer']
        self.xbanswerShareCode = shareCode['xbanswer']
        # 题库地址
        self.whcanswerFilePath = rootDir + '/whcanswer.json'
        self.xbanswerFilePath = rootDir + '/xbanswer.json'
        self.xsrfToken = self.cookies['XSRF-TOKEN'].replace('%3D', '=')
        self.old = 0
        self.name = ''
        self.aut = ''
        self.csrf = ''
        self.msg = ''

    def getApi(self, functionId, aut, csrf,
               ref='https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index', activityId='73BDNYm4', params=()):
        '''
        通用GET请求接口
        '''
        url = 'https://jxjkhd7.kerlala.com/{}/91/{}'.format(functionId, activityId)
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer ' + aut,
            'X-CSRF-TOKEN': csrf,
            'X-XSRF-TOKEN': self.xsrfToken,
            'user-agent': self.ua,
            'referer': ref,
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/plain, */*'
        }
        for i in range(5):
            try:
                r = requests.get(url, headers=headers, params=params, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def getApieasy(self, functionId, activityId='73BDNYm4', params=()):
        '''
        通用GET请求接口
        '''
        url = 'https://jxjkhd7.kerlala.com/{}/91/{}'.format(functionId, activityId)
        headers = {
            'user-agent': self.ua,
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        for i in range(5):
            try:
                r = requests.get(url, headers=headers, params=params, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def getApilzf(self, functionId, activityId='73BDNYm4', params=()):
        '''
        通用GET请求接口
        '''
        url = 'https://jxjkhd7.kerlala.com/{}/91/{}'.format(functionId, activityId)
        headers = {
            'user-agent': self.ua,
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        for i in range(5):
            try:
                r = requests.get(url, headers=headers, params=params, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def get(self, url, params=()):
        '''
        GET请求接口
        '''
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'user-agent': self.ua,
            'Referer': 'https://jxjkhd7.kerlala.com/a/91/73BDNYm4?CCB_Chnl=1000202'
        }
        for i in range(2):
            try:
                r = requests.get(url, headers=headers, params=params, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def postApi(self, functionId, aut, csrf, data,
                ref='https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/task', activityId='73BDNYm4'):
        '''
        通用POST请求接口
        '''
        url = 'https://jxjkhd7.kerlala.com/{}/91/{}'.format(functionId, activityId)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer ' + aut,
            'X-CSRF-TOKEN': csrf,
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': self.xsrfToken,
            'user-agent': self.ua,
            'Accept-Encoding': 'gzip, deflate, br',
            'origin': 'https://jxjkhd7.kerlala.com',
            'referer': ref,
            'content-type': 'application/json;charset=UTF-8',
        }
        for i in range(5):
            try:
                r = requests.post(url, headers=headers, data=data, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        logger.error('Cookie已失效，请更新Cookie')
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def postApieasy(self, functionId, data, activityId):
        '''
        通用POST请求接口
        '''
        url = 'https://jxjkhd7.kerlala.com/{}/91/{}'.format(functionId, activityId)
        # logger.info(url)
        headers = {
            'x-xsrf-token': self.xsrfToken,
            'user-agent': self.ua,
            'origin': 'https://jxjkhd7.kerlala.com',
            'referer': 'https://jxjkhd7.kerlala.com/a/91/9ZaYbvZy/question',
            'content-type': 'application/json;charset=UTF-8'
        }
        for i in range(5):
            try:
                r = requests.post(url, headers=headers, data=data, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        logger.error('Cookie已失效，请更新Cookie')
                        return r.text
                    else:
                        # logger.info(r.json())
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def postApiT2(self, functionId, activityId, aut, csrf):
        '''
        通用POST请求接口
        '''
        url = 'https://fission-events2.ccbft.com/{}/91/{}'.format(functionId, activityId)
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer ' + aut,
            'X-CSRF-TOKEN': csrf,
            'x-xsrf-token': self.xsrfToken,
            'user-agent': self.ua,
            'origin': 'https://fission-events2.ccbft.com',
            'referer': ' https://fission-events2.ccbft.com/a/91/dmRVxrmD/index',
            'content-type': 'aapplication/json',
            'Accept': 'application/json, text/plain, */*'
        }
        for i in range(2):
            try:
                r = requests.post(url, headers=headers, cookies=self.cookies)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    if re.findall('DOCTYPE', r.text):
                        logger.error('Cookie已失效，请更新Cookie')
                        return r.text
                    else:
                        return r.json()
                else:
                    logger.error('调用接口失败，等待10秒重试')
                    time.sleep(10)
            except:
                logger.error('调用接口失败，等待10秒重试')
                time.sleep(10)

    def checkCookie(self):
        checkResult = self.getApi('Common/activity/getUserInfo', self.aut, self.csrf,
                                  'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/friendlist')
        if checkResult['status'] == 'success':
            return True
        else:
            logger.error('第{}个账号已失效'.format(i + 1))
            self.wxpush('第{}个账号已失效'.format(i + 1))
            return False

    def getUserInfo(self):
        '''
        获取账户信息
        '''
        html = self.get('https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index?CCB_Chnl=1000202')
        aut = re.findall(r'Authorization content=\"(\w+)\"', html)
        logger.info(aut[0])
        self.aut = aut[0]
        csrf = re.findall(r'csrf-token content=\"(\w+)\"', html)
        logger.info(csrf[0])
        self.csrf = csrf[0]
        userInfo = self.getApi('activity/cftopic/userInfo', self.aut, self.csrf)
        self.name = userInfo['data']['nickname']
        logger.info('用户{}信息获取成功'.format(userInfo['data']['nickname']))
        logger.info('当前建筑等级{}级，已获得建设值总量{},升级还需建设值{}'.format(userInfo['data']['grade'], userInfo['data']['build_score'],
                                                            userInfo['data']['need_build_score']))
        logger.info('您的助力码为：{}'.format(userInfo['data']['ident']))
        ccbInfo = self.getApi('Component/draw/getUserCCB', self.aut, self.csrf)
        logger.info('已获得CC币总量{}，剩余CC币总量{}'.format(ccbInfo['data']['total_money'], ccbInfo['data']['remain_money']))
        self.old = int(ccbInfo['data']['remain_money'])
        try:
            user_name = urllib.parse.quote(userInfo['data']['nickname'])
            addCodeResult = requests.get(
                'http://47.100.61.159:10080/add?user={}&code={}&type={}'.format(user_name, userInfo['data']['ident'],
                                                                                "ccbcommon"))
            if addCodeResult.status_code == 200:
                logger.info('提交云端助力池成功')
            else:
                logger.error('提交云端助力池失败')
        except Exception as e:
            logger.error(e)

    def getUserInfoend(self):
        '''
        获取账户信息 待修复
        '''
        ccbInfo = self.getApi('Component/draw/getUserCCB', self.aut, self.csrf)
        onece = int(ccbInfo['data']['remain_money'])
        result = onece - self.old
        logger.info('本次运行获得CC币数量{},剩余CC币数量{}'.format(result, ccbInfo['data']['remain_money']))
        global msg
        msg += '{}本次获得{}CC币,剩余{}CC币 \n'.format(self.name, result, ccbInfo['data']['remain_money'])

    def acceptCCB(self):
        '''
        领取每日CCB或建设值
        '''
        # 查询可领取的CC币
        time.sleep(5)
        ccbList = self.postApi('activity/cftopic/popList', self.aut, self.csrf,
                               {}, 'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index')
        logger.info(ccbList)
        for i in range(len(ccbList['data'])):
            data = '{"id":"' + str(ccbList['data'][i]['task_id']) + '","result_id": "' + str(
                ccbList['data'][i]['id']) + '"}'
            if ccbList['data'][i]['type'] == 'dailyCcb':
                acceptCcbResult = self.postApi('activity/cftopic/acceptCcb', self.aut, self.csrf, data)
                logger.info('领取{}个每日CCB成功'.format(ccbList['data'][i]['ccb_num']))
            elif ccbList['data'][i]['type'] == 'task':
                acceptCcbResult = self.postApi('Component/task/draw', self.aut, self.csrf, data)
                if acceptCcbResult['status'] == 'success':
                    logger.info('领取{}建设值成功'.format(ccbList['data'][i]['ccb_num']))
                else:
                    logger.info('领取建设值失败')
            elif ccbList['data'][i]['type'] == 'help':
                data = '{"id":"' + str(ccbList['data'][i]['id']) + '"}'
                acceptCcbResult = self.postApi('activity/cftopic/acceptHelp', self.aut, self.csrf, data)
                logger.info('领取{}建设值成功'.format(ccbList['data'][i]['ccb_num']))
            time.sleep(8)

    def doFdtopicTask(self):
        '''
        主会场完成任务
        '''
        logger.info('')
        logger.info('开始做日常任务')
        self.getUserInfo()
        # 获取任务列表
        taskList = self.getApi('Component/task/lists', self.aut, self.csrf)
        # logger.info(taskList)
        logger.info('共获取到{}个任务'.format(len(taskList['data']['task'])))
        for i in range(len(taskList['data']['task'])):
            logger.info('开始做任务{}【{}】'.format(i + 1, taskList['data']['task'][i]['show_set']['name']))
            if taskList['data']['task'][i]['id'] == 'daZkgzZ1':
                data = '{"id": "' + taskList['data']['task'][i]['id'] + '"}'
                doTaskResult = self.postApi('Component/task/do', self.aut, self.csrf, data)
                logger.info(doTaskResult['message'])
                time.sleep(6)
                self.getCJindex()
                time.sleep(7)
                num = self.getCJnum()
                time.sleep(5)
                logger.info(num)
                if num:
                    logger.info('今日剩余抽奖次数:{}'.format(num['data']['draw_remain_num']))
                    for o in range(int(num['data']['draw_remain_num'])):
                        time.sleep(10)
                        res = self.postApi('activity/cfjpet/drawPrize', self.aut, self.csrf, '',
                                           'https://jxjkhd7.kerlala.com/a/91/kmeREaZd/index', 'kmeREaZd')
                        # logger.info(res)
                        if res['status'] == 'success':
                            logger.info(
                                'No' + str(o + 1) + ':' + res['message'] + ' ' + res['data']['prizename'])
                        else:
                            logger.info(res)

                else:
                    logger.info('获取抽奖次数失败')
            if taskList['data']['userTask'][i]['finish'] == 1:
                logger.info('该任务已完成，无需重复执行')
                # 领取邀请任务奖励
                if taskList['data']['task'][i]['type'] == 'share':
                    data = '{"id":"' + taskList['data']['task'][i]['id'] + '"}'
                    acceptResult = self.postApi('Component/task/draw', self.aut, self.csrf, data)
                    logger.info(acceptResult['message'])
            elif taskList['data']['userTask'][i]['finish'] == -2:
                logger.info('无该任务，无需执行')
                continue
            else:
                # 判断任务类型
                if taskList['data']['task'][i]['type'] == 'visit' or taskList['data']['task'][i][
                    'type'] == 'other':
                    if taskList['data']['task'][i]['id'] == 'daZkgzZ1':
                        continue
                    # 浏览类型任务
                    data = '{"id": "' + taskList['data']['task'][i]['id'] + '"}'
                    doTaskResult = self.postApi('Component/task/do', self.aut, self.csrf, data)
                    logger.info(doTaskResult['message'])
                elif taskList['data']['task'][i]['type'] == 'share':
                    pass
                # 领取奖励
                if taskList['data']['task'][i]['draw_type'] == 'number':
                    # 气泡类型奖励
                    self.acceptCCB()
                elif taskList['data']['task'][i]['draw_type'] == 'accept':
                    # 按钮类型奖励
                    data = '{"id":"' + taskList['data']['task'][i]['id'] + '"}'
                    acceptResult = self.postApi('Component/task/draw', self.aut, self.csrf, data)
                    logger.info(acceptResult['message'])
                # 休息五秒，防止接口提示频繁
                time.sleep(random.randint(5, 10))
        # 签到
        self.qiandao()
        # 助力好友
        self.doHelp()
        # 助力好友userid
        self.doHelpu()
        # 升级建筑
        self.buildingUp()

    def getCJindex(self):
        logger.info('')
        logger.info('获取抽奖页面')
        # 获取openID
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent': self.ua,
            'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6',
            'referer': 'https://jxjkhd4.kerlala.com/a/91/73BDNYm4/cftopic_v1/index?CCB_Chnl=1025102',
        }
        oauthResult = requests.get('https://fission-events.ccbft.com/a/91/kmeREaZd', headers=headers,
                                   cookies=self.cookies, allow_redirects=False)
        if oauthResult.status_code == 302:
            self.location = oauthResult.headers['Location']
        else:
            return False
        html = self.get(self.location)
        logger.info(html)

    def getCJnum(self):
        return self.getApi('activity/cfjpet/getCurActivityUserInfo', self.aut, self.csrf,
                           'https://jxjkhd7.kerlala.com/a/91/kmeREaZd/index',
                           'kmeREaZd')

    def qiandao(self):
        '''
        每日签到
        '''
        info = self.getApi('activity/autographnew/info', self.aut, self.csrf,
                           'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/task', 'QPy6REmj')
        print(info)
        time.sleep(2)
        if info:
            if info['data']['today_is_register'] == True:
                logger.info('今日已签到')
            else:
                res = self.postApi('activity/autographnew/qdEvery', self.aut, self.csrf, '{}',
                                   'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/task', 'QPy6REmj')
                print(res)
                if res:
                    logger.info(res['data']['prize_name'])
                else:
                    logger.info('签到出错请检查')

    def getCommonCode(self):
        '''
        获取主会场互助码
        '''
        try:
            commonres = requests.get("http://47.100.61.159:10080/ccbcommon")
            if commonres.status_code == 200:
                commoncode = commonres.text.split('@')
                logger.info('从云端拉取到{}个互助码{}'.format(len(commoncode), commoncode))
            else:
                commoncode = []
        except:
            commoncode = []
        self.commonShareCode += commoncode

    def doHelp(self):
        '''
        助力任务
        '''
        logger.info('')
        logger.info('开始助力好友')
        # 拉取云端助力码
        self.getCommonCode()
        if len(self.commonShareCode) == 0:
            logger.info('未提供任何助力码')
        else:
            logger.info('您提供了{}个好友助力码'.format(len(self.commonShareCode)))
            for i in range(len(self.commonShareCode)):
                logger.info('开始助力好友{}'.format(i + 1))
                time.sleep(7)
                self.getApieasy('a', '73BDNYm4', (('u', self.commonShareCode[i]),))
                # print('助力结果：{}'.format(temp))
                time.sleep(6)
        self.commonShareCode = []

    def doHelpu(self):
        '''
        建设助力 采用user-id 助力好友列表
        '''
        logger.info('')
        logger.info('开始好友列表助力')
        rejson = self.getApi('Component/friend', self.aut, self.csrf,
                             'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/friendlist',
                             '73BDNYm4?page=1&pageSize=200')
        # logger.info(rejson)
        if rejson['status'] == 'success':
            for i in range(len(rejson['data']['data'])):
                if rejson['data']['data'][i]["is_help"]:
                    time.sleep(random.randint(5, 10))
                    logger.info('开始助力好友{}'.format(rejson['data']['data'][i]["user_id"]))
                    self.getApieasy('a', '73BDNYm4', (('u', '22c435a1-f4f3-4f40-9d14-27f858438535'),))
                    activeyid = '73BDNYm4?user_id=' + str(rejson['data']['data'][i]["user_id"])
                    refurl = 'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/friendvisit?id=' + str(
                        rejson['data']['data'][i]["user_id"])
                    usermesg = self.getApi('activity/cftopic/friendIndex', self.aut, self.csrf, refurl, activeyid)
                    # logger.info(usermesg)
                    if usermesg['data']['is_help'] == True:
                        data = '{"user_id": "' + str(rejson['data']['data'][i]["user_id"]) + '"}'
                        # logger.info(data)
                        outline = self.postApi('activity/cftopic/helpFriend', self.aut, self.csrf, data, refurl)
                        logger.info(outline)
                    elif usermesg['data']['is_max_help'] == False:
                        continue
                    else:
                        logger.info('已经好友助力上限，结束本次助力')
                        break
                else:
                    logger.info('跳过已经助力用户')
        else:
            logger.info('获取用户列表失败')

    def buildingUp(self):
        '''
        升级建筑
        '''
        logger.info('')
        logger.info('开始升级建筑')
        userInfo = self.getApilzf('activity/cftopic/userInfo')
        if userInfo['data']['remainder_build_score'] >= userInfo['data']['next_grade_build_score']:
            buildingUpResult = self.postApi('activity/cftopic/buildingUp', self.aut, self.csrf, {})
            if len(buildingUpResult['data']['up_awards']['up_awards']) > 0:
                upAwardsName = buildingUpResult['data']['up_awards']['up_awards'][0]['name']
                logger.info('升级{}成功，获得奖励{}'.format(buildingUpResult['data']['up_building']['name'], upAwardsName))
            else:
                logger.info('升级{}成功，无奖励'.format(buildingUpResult['data']['up_building']['name']))
            # 继续检查是否能升级
            time.sleep(6)
            self.buildingUp()
        else:
            logger.info('建设值不足,距下一等级还需{}建设值'.format(userInfo['data']['need_build_score']))

    def HitCall(self):
        '''
         #排行榜打CALL
        '''
        logger.info('')
        logger.info('开始做打CALL任务')
        # Calllist = self.getApiTY('activity/fbtopic/areaRank', 'lPYNjdmN', 'a/91/lPYNjdmN/fdtopic_v1/cityRanking')
        Calllist = self.getApi('activity/cftopic/areaRank', self.aut, self.csrf)
        logger.info(Calllist['data'][1]['is_cheer'])
        time.sleep(2)
        if Calllist['data'][1]['is_cheer'] == True:
            area_id = random.randint(1, 30)
            data = '{"area_id": "' + str(area_id) + '"}'
            logger.info(data)
            result = self.postApi('activity/cftopic/hitCall', self.aut, self.csrf, data,
                                  'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/friendRankingShare?areaId' + str(
                                      area_id), '73BDNYm4')
            logger.info(result)
        else:
            logger.info('今天已经打CALL')

    def choujiang(self):
        '''
        #每天十次抽奖
        '''
        logger.info('')
        logger.info('开始每日十次抽奖')
        winlist = self.getApi('Component/draw/getMyWinList', self.aut, self.csrf,
                              'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index?CCB_Chnl=1000202',
                              '5Z9BQV3K')
        # logger.info(winlist)
        time.sleep(3)
        if winlist['status'] == 'success':
            # 获取次数
            num = self.getApi('Component/draw/getUserCCB', self.aut, self.csrf,
                              'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index?CCB_Chnl=1000202',
                              '5Z9BQV3K')
            # userRemainDrawNum = int(num['data']['draw_day_max_num']) - int(num['data']['user_day_draw_num'])
            logger.info('今日剩余抽奖次数{}'.format(num['data']['user_day_draw_num']))
            if int(num['data']['user_day_draw_num']) > 0:
                logger.info('开始执行抽奖')
                for i in range(int(num['data']['user_day_draw_num'])):
                    # if userRemainDrawNum - i <= 4:
                    #     logger.info('今日已抽奖次数已经满6次，结束抽奖')
                    #     break
                    result = self.postApi('Component/draw/commonCcbDrawPrize', self.aut, self.csrf, {},
                                          'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index', '5Z9BQV3K')
                    if result['status'] == 'success':
                        logger.info('本次抽奖获得{}'.format(result['data']['prizename']))
                        time.sleep(random.randint(7, 13))
                    else:
                        logger.info('抽奖错误，请检查')
                        break
            else:
                logger.info('今日抽奖次数用完')
        else:
            logger.info('winlist获取失败')

    def doSubvenueTask(self):
        '''
        分会场 龙支付优惠集锦
        '''
        logger.info('')
        logger.info('开始做龙支付分会场任务')
        html = self.get('https://jxjkhd7.kerlala.com/a/91/dmRVxrmD/index?CCB_Chnl=6000112')
        aut = re.findall(r'Authorization content=\"(\w+)\"', html)
        # logger.info(aut[0])
        csrf = re.findall(r'csrf-token content=\"(\w+)\"', html)
        # logger.info(csrf[0])
        activityInfo = self.getApilzf('Common/activity/getActivityInfo', 'dmRVxrmD')
        if int(time.time()) < int(activityInfo['data']['end_time']):
            # 获取任务列表
            taskList = self.getApilzf('activity/lzfsubvenue/getIndicatorList', 'dmRVxrmD')
            # logger.info(taskList)
            logger.info('共获取到{}个大列表'.format(len(taskList['data']['task'])))
            isok = 0
            for i in range(len(taskList['data']['task'])):
                logger.info('开始做【{}】任务'.format(taskList['data']['task'][i]['task_subtitle_text']))
                for j in range(len(taskList['data']['task'][i]['items'])):
                    logger.info('开始做任务【{}】'.format(taskList['data']['task'][i]['items'][j]['indicator']['show_name']))
                    if taskList['data']['task'][i]['items'][j]['day_complete'] == '1':
                        logger.info('该任务今日已完成，无需重复执行')
                    elif taskList['data']['task'][i]['items'][j]['day_complete'] == 0:
                        data = '{"code": "' + taskList['data']['task'][i]['items'][j]['indicator']['code'] + '"}'
                        logger.info(data)
                        if isok == 1 and taskList['data']['task'][i]['items'][j]['ext']['qudao'] == 2:
                            logger.info('任务非法参数，跳过执行')
                            continue
                        doTaskResult = self.postApi('activity/lzfsubvenue/visit', aut[0], csrf[0], data,
                                                    'https://jxjkhd7.kerlala.com/a/91/dmRVxrmD/index?CCB_Chnl=6000112',
                                                    'dmRVxrmD')
                        logger.info(doTaskResult)
                        if doTaskResult['message'] == '参数非法':
                            isok = 1
                        if doTaskResult['message'] == 'ok':
                            logger.info('任务完成，获得2CC币')
                        time.sleep(8)
            self.openBox(aut[0], csrf[0])
        else:
            logger.info('抱歉，该活动已结束')

    def openBox(self, aut, crsf):
        '''
        每日开箱子
        '''
        pragram = {
            'activityUrl': 'https:%2F%2Fjxjkhd7.kerlala.com%2Fa%2F91%2FdmRVxrmD%2Findex%3FCCB_Chnl%3D6000112%23_spa_1'
        }
        inf = self.getApi('activity/lzfsubvenue/getActivityUserRemainNum', aut, crsf,
                          'https://jxjkhd7.kerlala.com/a/91/dmRVxrmD/index', 'dmRVxrmD', pragram)
        logger.info(inf)
        time.sleep(5)
        if inf:
            if inf['data']['remainNum'] == '0':
                logger.info('今日已开箱子')
            else:
                doTaskResult = self.postApi('activity/lzfsubvenue/draw', aut, crsf, '',
                                            'https://jxjkhd7.kerlala.com/a/91/dmRVxrmD/index', 'dmRVxrmD')
                logger.info(doTaskResult)
                if doTaskResult:
                    if doTaskResult['status'] != 'fail':
                        logger.info('箱子任务完成，获得{}'.format(doTaskResult['data']['prizename']))
                    else:
                        logger.info('箱子任务出错了')
                else:
                    logger.info('箱子未获取到返回值')
        else:
            logger.info('开箱子个人信息获取失败')

    def dayAnswer(self):
        '''
        每日一答
        无论对错，奖励均为10建设值
        '''
        logger.info('')
        logger.info('开始每日一答')
        # 获取用户答题信息
        userDataInfo = self.getApilzf('activity/dopanswer/getUserDataInfo', 'kZMNxg3W')
        print(userDataInfo)
        time.sleep(5)
        if int(userDataInfo['data']['remain_num']) == 1:
            # 获取题目
            question = self.getApi('activity/dopanswer/getQuestion', self.aut, self.csrf,
                                   'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index', 'kZMNxg3W')
            questionTitle = question['data']['all_question'][0]['question']['title']
            questionId = question['data']['all_question'][0]['question']['id']
            logger.info('问：{} id:{}'.format(questionTitle, questionId))
            for i in range(len(question['data']['all_question'][0]['option'])):
                logger.info('选项{}：{}'.format(i + 1, question['data']['all_question'][0]['option'][i]['title']))
            # 随机答题
            randomOption = random.randint(1, len(question['data']['all_question'][0]['option']))
            logger.info('随机选择选项{}'.format(randomOption))
            data = '{"answerId":"' + str(randomOption) + '","questionId":"' + str(questionId) + '"}'
            time.sleep(3)
            answerQuestionResult = self.postApi('activity/dopanswer/answerQuestion', self.aut, self.csrf, data,
                                                'https://jxjkhd7.kerlala.com/a/91/73BDNYm4/cftopic_v1/index?CCB_Chnl=1000202',
                                                'kZMNxg3W')
            logger.info('正确答案：选项{}'.format(answerQuestionResult['data']['right']))
            logger.info(answerQuestionResult['message'])
        else:
            logger.info('今日答题机会已用尽')

    def doCarTask(self):
        '''
        车主分会场做任务、抽奖
        '''
        logger.info('')
        logger.info('开始做车主分会场任务')
        activityInfo = self.getApilzf('Common/activity/getActivityInfo', '73BDNYm4')
        if int(time.time()) < int(activityInfo['data']['end_time']):
            # 访问首页，获得三次抽奖机会
            self.getApilzf('a', 'lPYrv1mN', (('CCB_Chnl', '6000111'),))
            time.sleep(3)
            # 获取任务列表
            taskList = self.getApilzf('activity/parallelsessions/getIndicatorList', 'lPYrv1mN')
            logger.info('共获取到{}个任务'.format(len(taskList['data']['task'])))
            for i in range(len(taskList['data']['task'])):
                logger.info('开始做任务【{}】'.format(taskList['data']['task'][i]['indicator']['show_name']))
                if taskList['data']['task'][i]['day_complete'] == 1:
                    logger.info('该任务今日已完成，无需重复执行')
                elif taskList['data']['task'][i]['day_complete'] == 0:
                    data = '{"code": "' + taskList['data']['task'][i]['indicator']['code'] + '"}'
                    doTaskResult = self.postApieasy('activity/parallelsessions/visit', data, 'lPYrv1mN')
                    logger.info(doTaskResult)
                    time.sleep(3)
            # 获取抽奖次数
            time.sleep(3)
            carIndexInfo = self.getApilzf('Component/draw/getUserExtInfo', 'lPYrv1mN')
            logger.info('车主分会场剩余抽奖次数{}'.format(carIndexInfo['data']['remain_num']))
            # 抽奖
            if int(carIndexInfo['data']['remain_num']) > 0:
                for i in range(int(carIndexInfo['data']['remain_num'])):
                    drawResult = self.postApieasy('activity/parallelsessions/draw', {}, 'lPYrv1mN')
                    if drawResult['status'] == 'success':
                        logger.info(drawResult['data']['prizename'])
                    else:
                        logger.info(drawResult['message'])
                    # 休息四秒，防止接口频繁
                    time.sleep(8)
        else:
            logger.info('抱歉，该活动已结束')

    def doWhcanswer(self):
        '''
        学外汇 得实惠活动答题、抽奖、助力
        '''
        logger.info('')
        logger.info('开始做 学外汇 得实惠 活动')
        # 读取题库
        if os.path.exists(self.whcanswerFilePath):
            with open(self.whcanswerFilePath, encoding='UTF-8') as fp:
                questionDict = json.load(fp)
        else:
            logger.info('题库不存在，请下载完整题库')
            return False
        # 读取活动信息
        activityInfo = self.getApilzf('Common/activity/getActivityInfo', 'dmRVOomD')
        if int(time.time()) < int(activityInfo['data']['end_time']):
            # 阅读任务
            self.xwhGetCcb()
            # 答题
            # 获取用户信息
            time.sleep(8)
            userInfo = self.getApilzf('Common/activity/getUserInfo', 'dmRev1PD')
            logger.info('您的活动助力码为：{}'.format(userInfo['data']['ident']))
            userDataInfo = self.getApilzf('activity/whcanswer/getUserDataInfo', 'dmRev1PD')
            if int(userDataInfo['data']['remain_num']) > 0:
                logger.info('今日剩余{}次答题机会'.format(userDataInfo['data']['remain_num']))
                for num in range(int(userDataInfo['data']['remain_num'])):
                    logger.info('开始第{}轮答题'.format(num + 1))
                    # 使用答题机会
                    self.getApilzf('activity/whcanswer/reduceNum', 'dmRev1PD')
                    # 获取题目
                    questionInfo = self.postApieasy('activity/whcanswer/getQuestion', '{levelId: 1}', 'dmRev1PD')
                    # 查询正确答案ID
                    rightOptionsId = []
                    for questionId in questionInfo['data']['question_id']:
                        rightOptionsId.append(questionDict[str(questionId)]['rightOptionId'])
                    logger.info(rightOptionsId)
                    # 获取正确答案位序
                    rightOptionsNum = []
                    for i in range(len(questionInfo['data']['all_question'])):
                        for j in range(len(questionInfo['data']['all_question'][i]['option'])):
                            if questionInfo['data']['all_question'][i]['option'][j]['id'] == rightOptionsId[i]:
                                rightOptionsNum.append(j + 1)
                                break
                    logger.info(rightOptionsNum)
                    # 开始答题
                    time.sleep(8)
                    for i in range(len(questionInfo['data']['all_question'])):
                        logger.info(
                            '问题{}：{}'.format(i + 1, questionInfo['data']['all_question'][i]['question']['title']))
                        for j in range(len(questionInfo['data']['all_question'][i]['option'])):
                            logger.info(
                                '选项{}：{}'.format(j + 1, questionInfo['data']['all_question'][i]['option'][j]['title']))
                        # 提交答案
                        logger.info('选择选项{}'.format(rightOptionsNum[i]))
                        data = '{"levelId": 1, "questionId": ' + str(i + 1) + ', "answerId":' + str(
                            rightOptionsNum[i]) + '}'
                        answerResult = self.postApieasy('activity/whcanswer/answerQuestion', data, 'dmRev1PD')
                        logger.info('当前得分{}'.format(answerResult['data']['curScore']))
                        # 休息3秒，防止接口频繁
                        time.sleep(8)
            else:
                logger.info('今日已无答题机会')
            # 抽奖
            # 获取剩余抽奖次数
            time.sleep(10)
            userDataInfo = self.getApilzf('activity/whcdraw/getUserDataInfo', 'lPYNEEmN')
            if int(userDataInfo['data']['drawUserExt']['remain_num']) > 0:
                self.getApilzf('a', 'dmRev1PD', (('u', '527aa529-db7e-4aea-afd1-f7a08eec9b28',)))
                logger.info('今日剩余抽奖次数{}'.format(userDataInfo['data']['drawUserExt']['remain_num']))
                for i in range(int(userDataInfo['data']['drawUserExt']['remain_num'])):
                    drawResult = self.getApilzf('activity/whcdraw/draw', 'lPYNEEmN')
                    logger.info(drawResult)
                    # 休息5秒，防止接口频繁
                    time.sleep(8)
            else:
                logger.info('今日已无抽奖机会')

            # 助力
            logger.info('开始助力好友')
            if len(self.whcanswerShareCode) == 0:
                logger.info('未提供任何助力码')
            else:
                logger.info('您提供了{}个好友助力码'.format(len(self.whcanswerShareCode)))
                for i in range(len(self.whcanswerShareCode)):
                    logger.info('开始助力好友{}'.format(i + 1))
                    self.getApilzf('a', 'dmRev1PD', (('u', self.whcanswerShareCode[i]),))
                    time.sleep(5)
        else:
            logger.info('抱歉，该活动已结束')

    def doXbanswer(self):
        '''
        消保分会场知识大考验答题、抽奖、助力
        '''
        logger.info('')
        logger.info('开始做 消保分会场知识大考验 活动')
        # 读取题库
        if os.path.exists(self.xbanswerFilePath):
            with open(self.xbanswerFilePath, encoding='UTF-8') as fp:
                questionDict = json.load(fp)
        else:
            logger.info('题库不存在，请下载完整题库')
            return False
        # 读取活动信息
        activityInfo = self.getApilzf('Common/activity/getActivityInfo', 'jmXrYb3d')
        if int(time.time()) < int(activityInfo['data']['end_time']):
            # 答题
            # 获取用户信息
            userInfo = self.getApilzf('Common/activity/getUserInfo', 'jmXrYb3d')
            logger.info('您的活动助力码为：{}'.format(userInfo['data']['ident']))
            userDataInfo = self.getApilzf('activity/xbanswer/getUserDataInfo', 'jmXrYb3d')
            if int(userDataInfo['data']['remain_num']) > 0:
                time.sleep(3)
                logger.info('今日剩余{}次答题机会'.format(userDataInfo['data']['remain_num']))
                for num in range(int(userDataInfo['data']['remain_num'])):
                    logger.info('开始第{}轮答题'.format(num + 1))
                    # 随机答题等级
                    # levelId = random.randint(1, 4)
                    levelId = 4
                    logger.info('随机选择等级{}题目'.format(levelId))
                    # 使用答题机会
                    self.getApilzf('activity/xbanswer/reduceNum', 'jmXrYb3d')
                    time.sleep(3)
                    # 获取题目
                    data = '{"levelId":"' + str(levelId) + '"}'
                    questionInfo = self.postApieasy('activity/xbanswer/getQuestion', data, 'jmXrYb3d')
                    # 查询正确答案ID
                    rightOptionsId = []
                    for questionId in questionInfo['data']['question_id']:
                        rightOptionsId.append(questionDict[str(questionId)]['rightOptionId'])
                    logger.info(rightOptionsId)
                    # 获取正确答案位序
                    rightOptionsNum = []
                    for i in range(len(questionInfo['data']['all_question'])):
                        for j in range(len(questionInfo['data']['all_question'][i]['option'])):
                            if questionInfo['data']['all_question'][i]['option'][j]['id'] == rightOptionsId[i]:
                                rightOptionsNum.append(j + 1)
                                break
                    logger.info(rightOptionsNum)
                    # 开始答题
                    for i in range(len(questionInfo['data']['all_question'])):
                        logger.info(
                            '问题{}：{}'.format(i + 1, questionInfo['data']['all_question'][i]['question']['title']))
                        for j in range(len(questionInfo['data']['all_question'][i]['option'])):
                            logger.info(
                                '选项{}：{}'.format(j + 1, questionInfo['data']['all_question'][i]['option'][j]['title']))
                        # 提交答案
                        logger.info('选择选项{}'.format(rightOptionsNum[i]))
                        data = '{"levelId": ' + str(levelId) + ', "questionId": ' + str(i + 1) + ', "answerId":' + str(
                            rightOptionsNum[i]) + '}'
                        time.sleep(3)
                        answerResult = self.postApieasy('activity/xbanswer/answerQuestion', data, 'jmXrYb3d')
                        logger.info('当前得分{}'.format(answerResult['data']['curScore']))
                        # 休息5秒，防止接口频繁
                        time.sleep(5)
            else:
                logger.info('今日已无答题机会')
            time.sleep(10)
            # 抽奖
            # 获取剩余抽奖次数
            userDataInfo = self.getApilzf('activity/xbdraw/getUserDataInfo', '5Z9Boa3K')
            if int(userDataInfo['data']['drawUserExt']['remain_num']) > 0:
                self.getApilzf('a', 'jmXrYb3d', (('u', 'ca777fd9-5737-4b3f-8e2d-6b3c19f489cd'),))
                logger.info('今日剩余抽奖次数{}'.format(userDataInfo['data']['drawUserExt']['remain_num']))
                for i in range(int(userDataInfo['data']['drawUserExt']['remain_num'])):
                    drawResult = self.getApilzf('activity/xbdraw/draw', '5Z9Boa3K')
                    logger.info(drawResult)
                    # 休息5秒，防止接口频繁
                    time.sleep(7)
            else:
                logger.info('今日已无抽奖机会')
            time.sleep(10)
            # 助力
            logger.info('开始助力好友')
            if len(self.xbanswerShareCode) == 0:
                logger.info('未提供任何助力码')
            else:
                logger.info('您提供了{}个好友助力码'.format(len(self.xbanswerShareCode)))
            for i in range(len(self.xbanswerShareCode)):
                logger.info('开始助力好友{}'.format(i + 1))
                self.getApilzf('a', 'jmXrYb3d', (('u', self.xbanswerShareCode[i]),))
                time.sleep(3)
        else:
            logger.info('抱歉，该活动已结束')

    def doXbpickon(self):
        '''
        消保分会场眼力大考验答题、抽奖、助力
        '''
        logger.info('')
        logger.info('开始做 消保分会场眼力大考验 活动')
        # 读取题库
        questionDict = {'嘉言善行': True, '教导有方': True, '循循善诱': True, '东风化雨': True, '春风中坐': True, '尊闻行知': True,
                        '敬如上宾': True,
                        '斯抬斯敬': True, '竭诚相待': True, '以礼相待': True, '依法赔偿': True, '多元化解': True, '及时处理': True,
                        '合理赔付': True,
                        '受理依据': True, '等价交换': True, '合法权益': True, '质价相符': True, '价格公开': True, '保护弱小': True, '公平': True,
                        '信用': True, '自由裁量': True, '公平交易': True, '账户安全': True, '合法使用': True, '风险防范': True, '信息真实': True,
                        '万无一失': True, '及时规避': True, '数据安全': True, '电子签名': True, '信息交换': True, '自愿选择': True,
                        '依法监督': True,
                        '明显': True, '真心实意': True, '敞开心扉': True, '如实相告': True, '货真价实': True, '求知若渴': True, '学而不厌': True,
                        '学无止境': True, '有教无类': True, '诲人不倦': True, '程门立雪': True, '彬彬有礼': True, '敬老怜贫': True,
                        '毕恭毕敬': True,
                        '扫径以待': True, ' 代位追偿': True, '友好协商': True, '首问负责': True, '有法可依': True, '有理有据': True,
                        '价格合理': True,
                        '准确计价': True, '买卖公平': True, '诚实守信': True, '透明公开': True, '公开': True, '自愿': True, '合适': True,
                        '密码安全': True, '安全保障': True, '鉴别能力': True, '风险警示': True, '稳若泰山': True, '保质保量': True,
                        '信息安全': True,
                        '指纹安全': True, '安全秘钥': True, '符合原则': True, ' 诚实': True, '开诚布公': True, '实话实说': True, '坦诚相对': True,
                        '去伪存真': True, '因材施教': True, '格物致知': True, '学以致用': True, '力学笃行': True, '博学多才': True,
                        '洗耳恭听': True,
                        '尊年尚齿': True, '敬老慈幼': True, '敬老尊贤': True, '弥补损害': True, '赔礼道歉': True, '合理申诉': True,
                        '证据确凿': True,
                        ' 民事调解': True, '严格准入': True, '自由谈判': True, ' 解释合理': True, '公平竞争': True, '公正': True, '自由': True,
                        '尊重': True, '授权使用': True, '杜绝侵害': True, '财产安全': True, '防微杜渐': True, '保障权益': True, '依法收集': True,
                        '虹膜技术': True, '数据准确': True, '严格保密': True, '依法查询': True, '一目了然': True, '学海无涯': True,
                        '勤学好问': True,
                        '满腹经纶': True, '鸿儒硕学': True, '尊师重道': True, '负弩前驱': True, '热情周到': True, '快速核查': True,
                        '公平公正': True,
                        '和解机制': True, '及时受理': True, '事实明显': True, '充分披露': True, '货值其价': True, '信息对等': True,
                        '平等自愿': True,
                        '真实': True, '自主': True, '推荐': True, '自主选择': True, '密钥安全': True, '信息透明': True, '合理收费': True,
                        '个人权益': True, '居安思危': True, '举证通报': True, '电子签约': True, '真实全面': True, '履行义务': True,
                        '承担责任': True,
                        ' 通俗易懂': True, '耳提面命': True, '心口如一': True, '仗气直书': True, '手不释卷': True, '笃实好学': True,
                        '学富五车': True,
                        '博古通今': True, '书通二酉': True, '安老怀少': True, '奉若神明': True, '举案齐眉': True, '倒履相迎': True,
                        '溯源整改 ': True,
                        '责任追究': True, '投诉畅通': True, '电话畅通': True, '受理有效': True, '规范文本': True, '风险提示': True,
                        '交易公平': True,
                        '交易自主': True, '准确': True, '平等': True, '尊重意愿': True, '自主决定': True, '抵制不当': True, '信息对称': True,
                        '防止纠纷': True, '金融素养': True, '稳健投资': True, '防范意识': True, '合理使用': True, '内容检查': True,
                        '正当合法': True,
                        '信息隐私': True, '防止损失': True, ' 开门见山': True, '实不相瞒': True, '直截了当': True, '公之于众': True,
                        '实事求是': True,
                        '敏而好学': True, '学贯中西': True, '力学不倦': True, '智周万物': True, '你敬我爱': True, '落落大方': True,
                        '将心比心': True,
                        '正大光明': True, '依法合规': True, '妥善处理': True, '合理维权': True, '机会平等': True, '格式合同': True,
                        '自愿行为': True,
                        '履职履责': True, '获利公平': True, '诚实': True, '自行判断': True, '充分尊重': True, '买卖自由': True, '请勿轻信': True,
                        '公平互惠': True, '诚实信用': True, '审慎对待': True, '分散风险': True, '资金安全': True, '数据字典': True,
                        '信息加密': True,
                        '流程标准': True, '网络安全': True, '维护权益': True, '知无不言': True, '倾囊相授': True, '千真万确': True,
                        '情真意切': True,
                        '屡教不改': False, '秀而不实': False, '不学无术': False, '不求甚解': False, '浅见寡识': False, '傲慢不逊': False,
                        '咄咄逼人': False,
                        '不可一世': False, '目空一切': False, '仗势欺人': False, '推诿扯皮': False, '敲诈勒索': False, '歪曲事实': False,
                        '捏造事实': False,
                        ' 恶意投诉': False, '诱导销售': False, '高额佣金': False, '强制交易': False, '转嫁成本': False, '虚假交易': False,
                        '非法侵害': False, '店大欺客': False, '胁迫': False, '犹豫不决': False, '非法集资': False, '高利诱惑': False,
                        '巧立名目': False,
                        '虚假宣传': False, '人财两空': False, '虚假网页': False, '非法收集': False, '信息泄露': False, '间谍软件': False,
                        '无效数据': False,
                        '追偿难': False, '掩人耳目': False, '混淆视听': False, '偏离 ': False, '模棱两可': False, '故弄玄虚': False,
                        '孤陋寡闻': False,
                        '蒙昧无知': False, '胸无点墨': False, '一知半解': False, '一窍不通': False, '欺贫爱富': False, '不理不睬': False,
                        '斯文扫地': False,
                        '盛世凌人': False, '诬告他人': False, '忍气吞声': False, '扰乱秩序': False, '投诉受阻': False, '纠缠不清': False,
                        '显失公平': False,
                        '单方变更': False, '欺诈合同': False, '伪造合同': False, '恃强凌弱': False, '欺骗': False, '引诱消费': False,
                        '口是心非': False,
                        '非法获利': False, '盲目跟从': False, '巧舌如簧': False, '伪基站': False, '网络攻击': False, '蠕虫病毒': False,
                        '侵犯安全': False,
                        '未经授权': False, '偷天换日': False, '瞒心昧己': False, '延迟 ': False, '断章取义': False, '瞒天过海': False,
                        '一无所知': False,
                        '井底之蛙': False, '不识之无': False, '束之高阁': False, '走马观花': False, '颐指气使': False, '倨傲无力': False,
                        '目无尊长': False,
                        '趾高气昂': False, '恶意投诉': False, '过度承诺 ': False, '逾期处理': False, '拒不受理': False, '拒不接受': False,
                        '捆绑销售': False, '代客操作': False, '不当得利': False, '过度营销': False, '擅自做主': False, '诱导': False,
                        '别有用心': False,
                        '恶意敛财': False, '账户盗刷': False, '亡羊补牢': False, '内幕消息': False, '盗取信息': False, '安全漏洞': False,
                        '网络破坏': False,
                        '信息丢失': False, '网络风险': False, '虚词诡说': False, '滞后': False, '欲盖弥彰': False, '欺上瞒下': False,
                        '一曝十寒': False,
                        '末学肤受': False, '不学无识': False, '累教不改': False, '鹘仑吞枣': False, '马耳东风': False, '蛮横无理': False,
                        '桀骜不驯': False,
                        '鄙夷不屑': False, '差强人意': False, '过度维权': False, '瞒报漏报': False, '纠缠投诉': False, '反复投诉': False,
                        '借贷搭售': False,
                        '披露不全': False, '以次充好': False, '夸大宣传': False, '霸王条款': False, '搭售商品': False, '过度消费': False,
                        '密码泄露': False,
                        '财产侵害': False, '不法侵害': False, '诈骗短信': False, '不明链接': False, '违规滥用': False, '弱口令': False,
                        '虚假数据': False,
                        '违规保管': False, '非法运营': False, '欺公罔法': False, '遮天蔽日': False, '以管窥天': False, '欺三瞒四': False,
                        '困而不学': False,
                        '囫囵吞枣': False, '自以为是': False, '独学寡闻': False, '款学寡闻': False, '尖酸刻薄': False, '恶语相向': False,
                        '拒不赔偿': False,
                        '逃避责任': False, '无故拒绝': False, '恶意中伤': False, '规避义务': False, '过度销售': False, '有失公平': False,
                        '无效合同': False,
                        '虚假标价': False, '强买强卖': False, '滥用权力': False, '有奖销售': False, '套利账户': False, '集资诈骗': False,
                        '消费争议': False,
                        '贪图便宜': False, '违禁销售': False, '网络诈骗': False, '非法盗取': False, '缓存溢出': False, '危害广泛': False,
                        '矫情饰诈': False,
                        '尺水丈波': False, '晦涩难懂': False, '一叶障目': False, '蒙混过关': False, '不懂装懂': False, '暗室求物': False,
                        '学非所用': False,
                        '记问之学': False, '三心二意': False, '鼻孔朝天': False, '数典忘祖': False, '狐假虎威': False, '扬威耀武': False,
                        '暴力维权': False,
                        '投诉无门': False, '投诉升级': False, '无故投诉': False, '限制交易': False, '乱收费': False, '虚假销售': False,
                        '信息短缺': False,
                        '虚构条款': False, '违备意愿': False, '处心积虑': False, '电信诈骗': False, '非法挪用': False, '缺乏保障': False,
                        '假冒伪略': False,
                        '盲目付款': False, '网络入侵': False, '木马病毒': False, '违规销毁': False, '信息缺失': False, '浮皮潦草': False,
                        '弄虚作假': False,
                        '偷梁换柱': False, '掩耳盗铃': False}
        # 读取活动信息
        activityInfo = self.getApilzf('Common/activity/getActivityInfo', 'kZMNz73W')
        if int(time.time()) < int(activityInfo['data']['end_time']):
            # 答题
            # 获取用户信息
            userInfo = self.getApilzf('Common/activity/getUserInfo', '9ZaYbvZy')
            logger.info('您的活动助力码为：{}'.format(userInfo['data']['ident']))
            userDataInfo = self.getApilzf('activity/xbpickon/getUserDataInfo', '9ZaYbvZy')
            if int(userDataInfo['data']['remain_num']) > 0:
                time.sleep(3)
                logger.info('今日剩余{}次答题机会'.format(userDataInfo['data']['remain_num']))
                for num in range(int(userDataInfo['data']['remain_num'])):
                    logger.info('开始第{}轮答题'.format(num + 1))
                    # 使用答题机会
                    self.getApilzf('activity/xbpickon/reduceNum', '9ZaYbvZy')
                    # 获取题目
                    time.sleep(3)
                    questionInfo = self.getApilzf('activity/xbpickon/getQuestion', '9ZaYbvZy')
                    logger.info(questionInfo)
                    questionWordList = []
                    rightIdList = []
                    rightWordList = []
                    for i in range(len(questionInfo['data'])):
                        questionWordList.append(questionInfo['data'][i]['word'])
                        if str(questionInfo['data'][i]['word']) in questionDict.keys():
                            if questionDict[str(questionInfo['data'][i]['word'])] == True:
                                rightIdList.append(str(questionInfo['data'][i]['id']))
                                rightWordList.append(questionInfo['data'][i]['word'])
                    strQuestionIds = ','.join(rightIdList)
                    logger.info('请在下列词汇中找出所有正面词汇{}'.format(questionWordList))
                    logger.info(rightIdList)
                    logger.info('选择{}'.format(rightWordList))
                    data = '{"answerId":"' + strQuestionIds + '"}'
                    time.sleep(5)
                    answerResult = self.postApieasy('activity/xbpickon/answerQuestion', data, '9ZaYbvZy')
                    # 休息5秒，防止接口频繁
                    time.sleep(5)
            else:
                logger.info('今日已无答题机会')

            # 抽奖
            # 获取剩余抽奖次数
            time.sleep(10)
            userDataInfo = self.getApilzf('activity/xbpickon/getUserDataInfo', '9ZaYbvZy')
            if int(userDataInfo['data']['draw_remain_num']) > 0:
                self.getApilzf('a', '9ZaYbvZy', (('u', '23d18701-d922-4ffb-aa3f-271ccfd13692'),))
                logger.info('今日剩余抽奖次数{}'.format(userDataInfo['data']['draw_remain_num']))
                for i in range(int(userDataInfo['data']['draw_remain_num'])):
                    drawResult = self.getApilzf('activity/xbpickon/draw', '9ZaYbvZy')
                    if drawResult['status'] == 'success':
                        logger.info('获得{}'.format(drawResult['data']['prizename']))
                    else:
                        logger.info(drawResult)
                    # 休息5秒，防止接口频繁
                    time.sleep(6)
            else:
                logger.info('今日已无抽奖机会')

            # 助力
            time.sleep(10)
            logger.info('开始助力好友')
            if len(self.xbpickonShareCode) == 0:
                logger.info('未提供任何助力码')
            else:
                logger.info('您提供了{}个好友助力码'.format(len(self.xbpickonShareCode)))
            for i in range(len(self.xbpickonShareCode)):
                logger.info('开始助力好友{}'.format(i + 1))
                self.getApilzf('a', '9ZaYbvZy', (('u', self.xbpickonShareCode[i]),))
                time.sleep(3)
        else:
            logger.info('抱歉，该活动已结束')

    def xwhGetCcb(self):
        '''
         外汇做任务得CCB
        '''
        logger.info('')
        logger.info('开始做外汇阅读任务')
        # 首页
        self.get('https://jxjkhd7.kerlala.com/a/91/dmRVOomD?CCB_Chnl=6000113')
        time.sleep(5)
        # 个人信息识别
        temp = self.getApilzf('activity/crossborder/getUserInfo', 'dmRVOomD')
        logger.info(temp)
        if temp['status'] != 'fail':
            # 获取任务列表
            time.sleep(3)
            taskList = self.getApilzf('activity/crossborder/getTaskList', 'dmRVOomD')
            logger.info('共获取到{}个任务'.format(len(taskList['data']['task'])))
            for i in range(len(taskList['data']['task'])):
                logger.info('开始做任务【{}】'.format(taskList['data']['task'][i]['indicator']['show_name']))
                if taskList['data']['task'][i]['day_complete'] == 1:
                    logger.info('该任务今日已完成，无需重复执行')
                elif taskList['data']['task'][i]['day_complete'] == 0:
                    # crossborder_foreign_exchange_add_ccb  crossborder_foreign_currency_add_ccb除外
                    if taskList['data']['task'][i]['indicator']['code'] == 'crossborder_foreign_exchange_add_ccb':
                        continue
                    if taskList['data']['task'][i]['indicator']['code'] == 'crossborder_foreign_currency_add_ccb':
                        continue
                    data = '{"code": "' + taskList['data']['task'][i]['indicator']['code'] + '"}'
                    doTaskResult = self.postApieasy('activity/crossborder/finishBrowseTask', data, 'dmRVOomD')
                    logger.info(doTaskResult)
                    time.sleep(10)
        else:
            logger.info('抱歉，此账号不能参加')

    def main(self):
        try:
            # 主会场活动
            self.doFdtopicTask()
            time.sleep(5)
            # 龙支付分会场活动
            self.doSubvenueTask()
            # 每日打CALl
            time.sleep(5)
            self.HitCall()
            # 每日抽奖
            time.sleep(5)
            self.choujiang()
            # 每日一答
            time.sleep(5)
            self.dayAnswer()
            # 车主分会场
            time.sleep(5)
            self.doCarTask()
            # 消保分会场
            time.sleep(5)
            self.doXbanswer()
            time.sleep(5)
            self.doXbpickon()
            # 学外汇
            time.sleep(5)
            self.doWhcanswer()
            # 发送信息
            self.getUserInfoend()
        except Exception as e:
            logger.error(e)


def readConfig(configPath):
    if os.path.exists(configPath):
        with open(configPath, encoding='UTF-8') as fp:
            try:
                config = json.load(fp)
                return config
            except:
                print('读取配置文件失败，请检查配置文件是否符合json语法')
                sys.exit(1)
    else:
        print('配置文件不存在，请复制模板文件config.sample.json为config.json')
        sys.exit(2)


def createLog(logDir):
    # 日志输出控制台
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    # 日志输入文件
    date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    logPath = '{}/{}.log'.format(logDir, date)
    if not os.path.exists(logDir):
        logger.warning("未检测到日志目录存在，开始创建logs目录")
        os.makedirs(logDir)
    fh = logging.FileHandler(logPath, mode='a', encoding='utf-8')
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)
    return logger


def cleanLog(logDir):
    logger.info("开始清理日志")
    cleanNum = 0
    files = os.listdir(logDir)
    for file in files:
        today = time.mktime(time.strptime(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()), "%Y-%m-%d-%H-%M-%S"))
        logDate = time.mktime(time.strptime(file.split(".")[0], "%Y-%m-%d-%H-%M-%S"))
        dayNum = int((int(today) - int(logDate)) / (24 * 60 * 60))
        if dayNum > 7:
            os.remove("{}/{}".format(logDir, file))
            cleanNum += 1
            logger.info("已删除{}天前日志{}".format(dayNum, file))
    if cleanNum == 0:
        logger.info("未检测到过期日志，无需清理！")


if __name__ == '__main__':
    global rootDir
    rootDir = os.path.dirname(os.path.abspath(__file__))
    configPath = rootDir + "/config.json"
    config = readConfig(configPath)
    logDir = rootDir + "/logs/main/"
    if 'logDir' in config:
        if config['logDir'] != '':
            logDir = config['logDir'] + "/ccb_main/"
    global logger
    logger = createLog(logDir)
    for i in range(len(config['cookie'])):
        user = getCCB(config['cookie'][i], config['shareCode'])
        print(user)
        if user.checkCookie():
            user.main()
        else:
            logger.error('账号{}已失效，请及时更新Cookie'.format(i + 1))
            wxpush('账号{}已失效，请及时更新Cookie'.format(i + 1))
        logger.info('')
        logger.info('')
        logger.info('')
    wxpush(msg)
    cleanLog(logDir)
