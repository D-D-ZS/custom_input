import logging
import sys
import os

# add library to python path , don't forget it
lib_name = 'libs'
sys.path.insert(0, os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), lib_name]))

from pdr_python_sdk.api.on_demand_api import OnDemandApi
from pdr_python_sdk.api.response import Response
from pdr_python_sdk.tools.mock_tools import *
from xy.user_api import UserAPI


class Tenants(OnDemandApi):

    def do_handle_init(self, packet):
        logging.info("start init")
        logging.info(packet.body().metadata())
        self.xy_conn = UserAPI()

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
            "tenants": self.xy_conn.get_tenants,
            "tenants/users": self.xy_conn.get_users_by_tenantid,
            "tenants/users/info": self.xy_conn.get_user_info_by_id,
        }

        if path not in xy_path.keys():
            return Response(405, {"status": f"path: {path} not support"}).to_string()

        if params is None:
            res = xy_path[path]()
        else:
            res = xy_path[path](**params)
        logging.info(res)
        if int(res["code"]) == 0:
            return Response(200, res).to_string()
        else:
            return Response(500, res).to_string()


if __name__ == '__main__':
    run(Tenants, sys.argv, sys.stdin.buffer, sys.stdout.buffer)
