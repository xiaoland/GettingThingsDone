# coding=utf-8
# author: Lan_zhijiang
# description: 用户管理器
# date: 2020/10/2

import json
from backend.data.encryption import Encryption
from backend.database.mongodb import MongoDBManipulator
from backend.user.user_group_manager import UserGroupManager


class UserManager():

    def __init__(self, log, setting):

        self.log = log
        self.setting = setting

        self.encryption = Encryption(log, setting)
        self.mongodb_manipulator = MongoDBManipulator(log, setting)
        self.user_group_manager = UserGroupManager(log, setting)

    def sign_up(self, account, password, email, user_group="user"):

        """
        注册用户
        :param account: 账户名
        :param password: 密码(md5)
        :param email: 电子邮箱
        :param user_group: 用户组
        :return bool
        """
        if "/" in account or "." in account or "-" in account:
            self.log.add_log("UserManager: '/', '.' and '-' is banned in account name", 3)
            return False

        user_info = json.load(open("./backend/data/json/user_info_template.json", "r", encoding="utf-8"))
        user_info["_id"] = 0
        user_info["account"] = str(account)
        user_info["password"] = str(password)
        user_info["email"][0] = email
        user_info["userGroup"] = user_group

        self.user_group_manager.add_user_in(account, user_group)

        if self.mongodb_manipulator.add_collection("user", account) is False:
            self.log.add_log("UserManager: Sign up failed, this user had already exists. user: " + account, 3)
            return False
        else:
            self.log.add_log("UserManager: Account add to the collection: user successfully", 1)

        if self.mongodb_manipulator.add_one_document("user", account, user_info) is False:
            self.log.add_log("UserManager: Sign up failed, something went wrong while adding document. account: "
                             + account, 3)
            return False
        else:
            self.log.add_log("UserManager: Sign up success", 1)
            return True

    def delete_user(self, account):

        """
        删除某个用户
        :param account: 账户名
        :return:
        """
        self.log.add_log("UserManager: Delete user: " + account, 1)
        return self.mongodb_manipulator.delete_collection("user", account)

    def login(self, account, password):

        """
        登录
        :param account: 账户
        :param password: 密码
        :return: bool(fail) str(success)
        """
        self.log.add_log("UserManager: Try login " + account)

        user_info = self.mongodb_manipulator.get_document("user", account)
        if user_info is False:
            if password == user_info["password"]:
                token = self.encryption.md5(self.log.get_time_stamp() + account)

                self.mongodb_manipulator.update_many_documents("user", account, {"_id": 0}, {"token": token})
                self.setting["user"]["account"] = account
                self.setting["user"]["avatar"] = user_info["avatar"]

                # add user group manager to get permission

                self.log.add_log("UserManager: login success", 1)
                return token
            else:
                self.log.add_log("UserManager: Your password is wrong", 3)
                return False

        else:
            self.log.add_log("UserManager: login: Can't find your account or something wrong with the memcached.", 3)
            return False