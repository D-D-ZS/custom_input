import sys
import os
import logging
import json
import subprocess
import os
import sys


# add library to python path , don't forget it

lib_name = 'libs'
sys.path.insert(0, os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), lib_name]))

from pdr_python_sdk.trigger_action.on_demand_trigger_action import OnDemandTriggerAction
from pdr_python_sdk.on_demand_action import run
from xy.message_api import MessageApi
from xy.user_api import UserAPI
from jsonpath import jsonpath


class SrcTrigger(OnDemandTriggerAction):
    def do_handle_init(self, packet):
        self.mess_conn = MessageApi()
        self.user_conn = UserAPI()

    def do_handle_events(self, events):
        length = len(events)
        logging.info(type(events[0]))
        values = events[0].__dict__
        event_name = values["eventName"]
        event_display_id = values["eventDisplayId"]
        params = {}
        logging.info("event length = {0}".format(length))
        if length > 0:
            # 前端传过来的字段在params中
            params = events[0].params
            logging.info(params)
            length = len(events[0].additionContents)
            if length > 0:
                logging.info(events[0].additionContents[0].__dict__)
            # 附加内容拆到 values 中，把
                additionContents = []
                for i in events[0].additionContents:
                    values[i.name] = i.contents
                    logging.info(f"name: {i.name}, contents: {i.contents}")
                    additionContents.append({i.name: i.contents})
                values["additionContents"] = json.dumps(additionContents)
            else:
                values["additionContents"] = ""
            user_ids = ",".join(params["userid"])
            self.notice_src(user_ids, params["methods"], **values)
        content= "from hello trigger: eventLength={0}, event_name={1}, " \
               "event_display_id={2}, params={3}".format(length, event_name, event_display_id, params)
        return content

    def notice_src(self, user_ids, methods, **kwargs):
        # todo 从前端传入的参数，得到发送类型，通过用户ID，获取用户的邮箱和手机号，通过模板ID，发送消息到对应地址
        user_info = self.user_conn.get_user_info_by_id(user_ids)
        email = ",".join(jsonpath(user_info, "data[*].email"))
        phone = ",".join(jsonpath(user_info, "data[*].phone"))
        logging.info(f"userids: {user_ids}")
        if methods["email"]["active"] is True:
            logging.info("send email")
            tem_id = methods["email"]["template"]
            logging.info(f"tem_id: {tem_id}")
            logging.info(f"email: {email}")
            values = self.replace_fields(tem_id, **kwargs)
            res = self.mess_conn.send_mail_with_file(tem_id, email, **values)
            logging.info(res)

        if methods["sms"]["active"] is True:
            logging.info("send sms")
            tem_id = methods["sms"]["template"]
            logging.info(f"tem_id: {tem_id}")
            logging.info(f"phone: {phone}")
            values = self.replace_fields(tem_id, **kwargs)
            res = self.mess_conn.send_sms(tem_id, phone, **values)
            logging.info(res)

    def replace_fields(self, tem_id, **kwargs):
        fields = self.mess_conn.get_replace_field_by_id(tem_id)
        logging.info(f"fields: {fields}")
        values = {}
        for field in fields:
            try:
                values[field] = kwargs[field]
            except Exception:
                return f"Not Found {field}"
        logging.info(f"values: {json.dumps(values)}")
        return values


if __name__ == '__main__':
    # p = subprocess.Popen(' list', stdout=subprocess.PIPE, shell=True)
    # p.stderr.readlines()
    run(SrcTrigger, sys.argv, sys.stdin.buffer, sys.stdout.buffer)

