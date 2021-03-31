#!/usr/bin/env python
# !-*- coding:utf-8 -*-
# Create  : 2021/3/8 4:40 下午
import logging

from xy.xy_api import XY_API


class UserAPI(XY_API):
    def __init__(self):
        self.url = "http://127.0.0.1:8080/src-user-svc"
        super().__init__(self.url)

    def get_tenants(self):
        # todo 获取租户列表
        res = self.get("/tenants/allTenant").json()
        # 添加平台
        res["data"].insert(0,

                           {
                               "id": "0",
                               "name": "平台",
                               "tenantAdminList": "",
                               "code": "",
                               "deptSecurityOwner": "",
                               "compSecurityOwner": "",
                               "parentOrgId": "",
                               "parentOrg": "",
                               "orgId": "",
                               "description": "",
                               "status": ""
                           }
                           )
        return res

    def get_users_by_tenantid(self, tenantid):
        # todo 根据租户ID获取，租户下用户
        logging.info(tenantid)
        if int(tenantid) == 0:
            logging.info("平台用户获取")
            return self.get_platform_users()
        return self.get(f"/tenants/{tenantid}/users").json()

    def get_user_info_by_id(self, userid):
        return self.get(f"/users/selectByIds?ids={userid}").json()

    def get_platform_users(self):
        # todo 返回平台用户列表
        res = self.get(f"/users?queryStr=&current=1&size=10000&type=2").json()
        if int(res["code"]) != 0:
            logging.info("请求异常")
            return res["msg"]
        data = []
        for record in res["data"]["records"]:
            data.append(record)
        res["data"] = data
        return res
