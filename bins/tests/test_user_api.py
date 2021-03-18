#!/usr/bin/env python
# !-*- coding:utf-8 -*-
# Create  : 2021/3/9 11:12 上午

from xy.user_api import UserAPI

xy_conn = UserAPI()


def test_get_tenants():
    res = xy_conn.get_tenants()
    print(res)
    assert res["success"] == True


def test_get_users_by_tenantid():
    res = xy_conn.get_users_by_tenantid(1356436976027922433)
    print(res)
    assert res["success"] is True


def test_get_user_info_by_id():
    res = xy_conn.get_user_info_by_id("1356436881656082434,1367313166642790402,1")
    print(res)
    assert res["success"] is True


def test_get_platform_users():
    res = xy_conn.get_platform_users()
    print(res)
    assert res["success"] is True
