# coding=utf-8
# author: Lan_zhijiang
# description: http handler
# date: 2020/12/12

import json

from backend.database.mongodb import MongoDBManipulator
from backend.user.user_permission_mamanger import UserPermissionManager
from backend.api.http.command_finder import CommandFinder


class HttpHandler:

    def __init__(self, log, setting):

        self.log = log
        self.setting = setting

        self.mongodb_mainpulator = MongoDBManipulator(log, setting)
        self.permission_manager = UserPermissionManager(log, setting)
        self.command_finder = CommandFinder(log, setting)
        
        self.request_data = {}
        self.permission_list = []
        self.response_data = json.load(open("./backend/data/json/response_template.json", "r", encoding="utf-8"))

    def auth(self):

        """
        进行认证
        ATTENTION: the development of "root"
        :return bool
        """
        self.log.add_log("HttpHandler: start auth", 1)

        # is the user exists
        account = self.request_data["header"]["account"]
        if "@" in account or str(account) == account:  # ATTENTION: error might be here
            now_time_stamp = self.log.get_time_stamp()
            try:
                gave_time_stamp = self.request_data["header"]["timeStamp"]
            except KeyError:
                self.log.add_log("HttpHandler: param is not complete", 1)
                self.response_data["header"]["errorMsg"] = "param is not complete"
                return False

            time_loss = abs(int(now_time_stamp) - int(gave_time_stamp)) # might not safe here

            # is time stamp in law
            if 0 <= time_loss <= 600:

                if self.request_data["header"]["loginRequest"]:
                    return True
                elif self.request_data["header"]["signupRequest"]:
                    return True

                last_login_time_stamp = self.mongodb_mainpulator.parse_document_result(
                    self.mongodb_mainpulator.get_document("user", account, {"lastLoginTimeStamp": 1}, 2),
                    ["lastLoginTimeStamp"]
                )[0]["lastLoginTimeStamp"]
                print(last_login_time_stamp)

                login_time_loss = abs(int(gave_time_stamp) - int(last_login_time_stamp))
                if 0 <= login_time_loss <= 3600 * 24:
                    self.log.add_log("HttpHandler: time stamp is in law", 1)

                    # is token same
                    real_token = self.mongodb_mainpulator.parse_document_result(
                        self.mongodb_mainpulator.get_document("user", account, {"token": 1}, 2),
                        ["token"]
                    )[0]["token"]
                    need_verify_token = self.response_data["header"]["token"]
                    if real_token == need_verify_token:
                        # auth pass, load permission list
                        self.permission_list = self.permission_manager.get_user_permissions(account)
                        if self.permission_list is False:
                            self.log.add_log("HttpHandler: can't load permission list", 3)
                            self.response_data["header"][
                                "errorMsg"] = "database or something wrong with the backend"  # inside error
                            return False
                        return True
                else:
                    self.log.add_log("HttpHandler: login outdate", 1)
                    self.response_data["header"]["errorMsg"] = "login outdate, please login"  # login outdate error
            else:
                self.log.add_log("HttpHandler: time stamp not in law, time_loss > 600", 1)
                self.response_data["header"]["errorMsg"] = "time stamp is not in law, time_loss > 600"  # timestamp error
                return False
        else:
            self.log.add_log("HttpHandler: account not exists or format error", 1)
            self.response_data["header"]["errorMsg"] = "user does not exists or format error"  # user not exists error
            return False

    def handle_request(self, request_data):

        """
        处理请求
        :param request_data: 请求数据
        :return bool
        """
        # ATTENTION: 防压测任务！
        self.log.add_log("HttpHandler: recevied http request, start handle...", 1)
        self.request_data = request_data

        if self.auth():
            self.log.add_log("HttpHandler: auth completed", 1)
            special_pass = False

            # the handle of login command
            if self.request_data["header"]["loginRequest"]:
                try:
                    command_name = self.request_data["command"][0]["commandName"]
                except IndexError:
                    self.response_data["header"]["status"] = 1
                    self.response_data["header"]["errorMsg"] = "you lied to me! you are not here to login!"
                    self.log.add_log("HttpHandler: can't find commandName", 1)
                else:
                    if command_name != "user_login":
                        self.response_data["header"]["status"] = 1
                        self.response_data["header"]["errorMsg"] = "you lied to me! you are not here to login!"
                        self.log.add_log("HttpHandler: false request to login", 1)
                    else:
                        special_pass = True
            # the handle of signup request
            elif self.request_data["header"]["signupRequest"]:
                if self.setting["allowSignup"]:
                    try:
                        command_name = self.request_data["command"][0]["commandName"]
                    except IndexError:
                        self.response_data["header"]["status"] = 1
                        self.response_data["header"]["errorMsg"] = "you lied to me! you are not here to sign up!"
                        self.log.add_log("HttpHandler: can't find commandName", 1)
                    else:
                        if command_name != "user_sign_up":
                            self.response_data["header"]["status"] = 1
                            self.response_data["header"]["errorMsg"] = "you lied to me! you are not here to sign up!"
                            self.log.add_log("HttpHandler: false request to sign up", 1)
                        else:
                            special_pass = True
                else:
                    self.log.add_log("HttpHandler: not allow sign up free, please contact the admin", 1)

            # the handle of normal command
            try:
                request_commands = self.request_data["command"]
            except KeyError:
                self.log.add_log("HttpHandler: can't find 'command' in the request")
                self.response_data["header"]["errorMsg"] = "can't find command in your request"
                self.response_data["header"]["status"] = 1
            else:
                for command in request_commands:
                    command_response = {}
                    try:
                        command_name = command["commandName"]
                        command_param = command["param"]
                    except KeyError:
                        self.log.add_log("HttpHandler: the command info is wrong", 1)
                        command_response["status"] = 3
                        command_response["errorMsg"] = "command info wrong"
                        self.response_data["response"].append(command_response)
                        break

                    command_response["commandName"] = command_name

                    if command_name in self.permission_list or special_pass is True:
                        self.log.add_log("HttpHandler: " + command_name + " is allowed, start handle", 1)
                        try:
                            command_handle_function = self.command_finder.all_command_list[command_name]
                        except KeyError:
                            self.log.add_log("HttpHandler: can't find command: " + command_name + " in command finder, skip", 3)
                            command_response["status"] = 1
                            command_response["errorMsg"] = "can't find command in command_finder"
                            self.response_data["response"].append(command_response)
                            break
                        else:
                            function_response, err = command_handle_function(command_param)
                            if function_response is False:
                                command_response["status"] = 1
                                command_response["errorMsg"] = err
                            else:
                                command_response["status"] = 0
                                command_response["errorMsg"] = None
                                command_response["result"] = function_response
                            self.response_data["response"].append(command_response)
                    else:
                        command_response["status"] = 2
                        command_response["errorMsg"] = "you have no permission to request command-" + command_name
                        command_response["result"] = None
        else:
            self.log.add_log("HttpHandler: auth fail", 1)
            self.response_data["header"]["status"] = 1

        self.response_data["header"]["timeStamp"] = self.log.get_time_stamp()

        return self.response_data
