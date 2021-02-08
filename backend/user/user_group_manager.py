# coding=utf-8
# author: Lan_zhijiang
# description: 用户组管理器
# date: 2020/11/1

import json
from backend.database.mongodb import MongoDBManipulator


class UserGroupManager:

    def __init__(self, log, setting):

        self.log = log
        self.setting = setting

        self.mongodb_manipulator = MongoDBManipulator(log, setting)

    def add_users_into_group(self, accounts, group_name):

        """
        添加用户到用户组中
        :param accounts: 要被添加的用户
        :param group_name: 目标用户组名称
        :type accounts: list
        :return: bool
        """
        self.log.add_log("UserGroupManager: try to add %s" % accounts + " into user_group-%s" % group_name, 1)
        err_add_users = []

        if type(accounts) != list:
            self.log.add_log("UserGroupManager: wrong type of the param-accounts, it should be a list", 3)
            return False, "param-accounts wrong type"

        if self.mongodb_manipulator.is_collection_exist("user_group", group_name) is False:
            self.log.add_log("UserGroupManager: user_group: " + group_name + " is not exist", 3)
            return False, "user_group-%s" % group_name + " is not exist, add user into group fail"
        else:
            for account in accounts:
                if self.mongodb_manipulator.is_collection_exist("user", account) is False:
                    err_add_users.append(account)
                    self.log.add_log("UserGroupManager: user-%s" % account + " not exist, skip")
                    continue

                self.mongodb_manipulator.update_many_documents("user", account, {"_id": 4}, {"userGroup": group_name})

                user_list = self.mongodb_manipulator.parse_document_result(
                    self.mongodb_manipulator.get_document("user_group", group_name, {"userList": 1}, 2),
                    ["userList"]
                )[0]["userList"]

                if account in user_list:
                    self.log.add_log("UserGroupManager: user-%s had already exists!" % account, 2)
                    err_add_users.append(account)

                user_list.append(account)
                if self.mongodb_manipulator.update_many_documents("user_group", group_name, {"_id": 1}, {"userList": user_list}) is False:
                    err_add_users.append(account)
                    self.log.add_log("UserGroupManager: add user-%s" % account + " into user_group-%s" % group_name + " fail, skip", 3)
                    continue
                else:
                    self.log.add_log("UserGroupManager: add user-%s" % account + " into user_group-%s" % group_name + " success", 1)

        if err_add_users is False:
            err = str(err_add_users) + " add fail"
        else:
            err = "success"

        return True, err

    def remove_users_from_group(self, accounts, group_name):

        """
        移除某个用户组的用户
        :param accounts: 用户名
        :param group_name: 用户组名
        :type accounts: list
        :return:
        """
        self.log.add_log("UserGroupManager: try to remove %s" % accounts + " from " + group_name, 1)

        if self.mongodb_manipulator.is_collection_exist("user_group", group_name) is False:
            self.log.add_log("UserGroupManager: user_group: " + group_name + " is not exists", 3)
            return False
        else:
            self.mongodb_manipulator.update_many_documents("user", account, {"_id": 4}, {"userGroup": None})

            try:
                user_list = self.mongodb_manipulator.parse_document_result(
                    self.mongodb_manipulator.get_document("user_group", group_name, {"userList": 1}, 2),
                    ["userList"]
                )[0]["userList"].remove(account)
            except ValueError:
                self.log.add_log("UserGroupManager: fail to delete " + "user-" + account + " from ser_group-" + group_name +
                                 "because it's not exist", 1)
                return False, "user-" + account + " not in the user_group-" + group_name
            if self.mongodb_manipulator.update_many_documents("user_group", group_name, {"_id": 1}, {"userList": user_list}) is False:
                self.log.add_log("UserGroupManager: remove " + account + " from " + group_name + " fail", 3)
            else:
                self.log.add_log("UserGroupManager: remove " + account + " from " + group_name + " success", 3)

    def move_user_to_another_group(self, account, from_group, to_group):

        """
        将某用户从一用户组移到另一用户组
        :param account: 用户名
        :param from_group: 原用户组
        :param to_group: 目标用户组
        :return: bool
        """
        self.log.add_log("UserGroupManager: try to move " + account + " from " + from_group + " to " + to_group, 1)

        if self.mongodb_manipulator.is_collection_exist("user_group", from_group) is False:
            self.log.add_log("UserGroupManager: move fail! from_group: " + from_group + " is not exists", 3)
            return False
        else:
            if self.mongodb_manipulator.is_collection_exist("user_group", to_group) is False:
                self.log.add_log("UserGroupManager: move fail! to_group: " + to_group + " is not exists", 3)
                return False
            else:
                from_group_user_list = self.mongodb_manipulator.parse_document_result(
                    self.mongodb_manipulator.get_document("user_group", from_group, {"userList": 1}, 2),
                    ["userList"]
                )[0]["userList"].remove(account)
                to_group_user_list = self.mongodb_manipulator.parse_document_result(
                    self.mongodb_manipulator.get_document("user_group", to_group, {"userList": 1}, 2),
                    ["userList"]
                )[0]["userList"].append(account)
                result_3 = self.mongodb_manipulator.update_many_documents("user_group", from_group, {"_id": 1}, {"userList": from_group_user_list})
                result_4 = self.mongodb_manipulator.update_many_documents("user_group", to_group, {"_id": 1}, {"userList": to_group_user_list})
                if result_3 is True or result_4 is True:
                    self.log.add_log("UserGroupManager: move user success", 1)
                    return True, "success"
                else:
                    self.log.add_log("UserGroupManager: move user fail", 3)
                    return False, "database error"

    def add_user_group(self, name, permissions_list=[]):

        """
        创建用户组
        :param name: 用户组名
        :param permissions_list: 初始化的权限组
        :return: bool
        """
        if permissions_list is None:
            permissions_list = []
        self.log.add_log("UserGroupManager: add user group: " + name, 1)

        if self.mongodb_manipulator.is_collection_exist("user_group", name) is True:
            self.log.add_log("UserGroupManager: user_group: " + name + " had already exists", 3)
            return False
        else:
            user_group_info = json.load(open("./backend/data/json/user_group_info_template.json", "r", encoding="utf-8"))
            user_group_info[0]["name"] = name
            user_group_info[2]["permissionsList"] = permissions_list

            self.mongodb_manipulator.add_collection("user_group", name)
            self.mongodb_manipulator.add_many_documents("user_group", name, user_group_info)

    def delete_user_group(self, name):

        """
        删除用户组
        :param name: 用户组名
        :return: bool
        """
        self.log.add_log("UserGroupManager: add user group: " + name, 1)

        if self.mongodb_manipulator.is_collection_exist("user_group", name) is False:
            self.log.add_log("UserGroupManager: user_group: " + name + " is not exists", 3)
            return False
        else:
            return self.mongodb_manipulator.delete_collection("user_group", name)

    def update_group_info(self, name, param):

        """
        更新用户组信息（全部）
        :param name: 用户组名
        :param param: 用户组信息
        :return:
        """

    def add_group_info(self, name, param):

        """
        设置用户组信息（个别）
        :type param: dict
        :param name: 用户组名
        :param param: key->value的dict
        :return: bool
        """
