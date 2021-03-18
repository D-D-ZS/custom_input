#!/usr/bin/env python
# !-*- coding:utf-8 -*-
# Create  : 2021/3/9 11:06 上午
import requests


class XY_API:
    def __init__(self, url):
        # todo 初始化连接
        self.token = "Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE2MTQyNDQ5NzgsImNsaWVudEtleSI6IlhpZXl1bl9Vc2VyX1NlcnZpY2VJSnVtWTJDYVI5RGpWakNnNDdRc0N2NWhLVHZFZFRMeHpTcUFpY3dOalhhQVkiLCJ0ZW5hbnRJZCI6IjEiLCJ0b2tlblR5cGUiOiJvcGVuQ2xpZW50IiwiZXhwIjoxNjE2ODM2OTc4fQ.Jc-L-yiYk1kFft2IKBwHaYhEDNjvNbfFom8r8fayWl0"
        self.url = url
        self.headers = {
            'Accept': '*/*',
            'SRC-No-Trace-Id': 'QN_CONNECT',
        }

    def get(self, path, **kwargs):
        if 'header' in kwargs.keys():
            self.headers = dict(self.headers, **kwargs['header'])
            kwargs.pop('header')
        return requests.get(url=f"{self.url}{path}", headers=self.headers, **kwargs)

    def post(self, path, data, **kwargs):
        if 'header' in kwargs.keys():
            self.headers = dict(self.headers, **kwargs['header'])
            kwargs.pop('header')
        return requests.post(url=f"{self.url}{path}", data=data, headers=self.headers, **kwargs)


