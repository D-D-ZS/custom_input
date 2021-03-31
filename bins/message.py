import logging
import sys
import os

# add library to python path , don't forget it
lib_name = 'libs'
sys.path.insert(0, os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), lib_name]))

from pdr_python_sdk.api.on_demand_api import OnDemandApi
from pdr_python_sdk.api.response import Response
from pdr_python_sdk.on_demand_action import run
from xy.message_api import MessageApi


class Message(OnDemandApi):

    def do_handle_init(self, packet):
        logging.info("start init")
        logging.info(packet.body().metadata())
        self.xy_conn = MessageApi()

    def do_handle_data(self, data):
        """
        TODO: Implement your own business logic

        :param data: http request
        :return:
        """
        if not data.contains_request():
            raise Exception('api data should contain request details')

        request = data.request()
        path = "/".join(request.path().split("/")[4:])
        params = request.param()
        if 'GET' != str.upper(request.method()):
            return Response(405, {"status": "method is not get"}).to_string()

        xy_path = {
            "message/templates": self.xy_conn.get_templates,
            "message/templates/id": self.xy_conn.get_template_by_id,
            "message/templates/sms": self.xy_conn.get_sms_templates,
            "message/templates/email": self.xy_conn.get_email_templates,
            "message/send/sms": self.xy_conn.send_sms,
            "message/send/email": self.xy_conn.send_mail_with_file
        }
        if path not in xy_path.keys():
            return Response(405, {"status": f"path: {path} not support"}).to_string()

        if params is None:
            res = xy_path[path]()
        else:
            res = xy_path[path](**params)
        if int(res["code"]) == 0:
            return Response(200, res).to_string()
        else:
            return Response(500, res).to_string()


if __name__ == '__main__':
    run(Message, sys.argv, sys.stdin.buffer, sys.stdout.buffer)
