#!/usr/bin/env python3
# author lfzyx date 2015.11.25
import requests
import json
import time
import sys
from urllib.parse import urljoin

if len(sys.argv) < 7:
    print("Usage:", sys.argv[0], "[address]", "[username]", "[passwd]", "[money]", "[managername]", "[managerpasswd]")
    sys.exit(1)


address = sys.argv[1]
username = sys.argv[2]
passwd = sys.argv[3]
money = sys.argv[4]
managername = sys.argv[5]
managerpasswd = sys.argv[6]


class Project:
    """a simple project"""
    def __init__(self, _address, _username, _passwd, _money, _managername, _managerpasswd):
        self.address = _address
        self.username = _username
        self.passwd = _passwd
        self.money = _money
        self.managername = _managername
        self.managerpasswd = _managerpasswd
        self.project_id = 0
        self.member_id = 0
        self.building_id = 0
        self.margin_fee = 0

    def __str__(self):
        return "server:" + self.address + "\nusername:" + self.username + "\npasswd:" + self.passwd + \
               "\nmoney:" + self.money + "\nmanagername:" + self.managername + "\nmanagerpasswd:" + self.managerpasswd

    def get_data(self, _url, _data, _headers):
        return loginsession.get(_url + str(_data), headers=_headers)

    def get_return(self, _returninfo):
        return ("code", returninfo.status_code, returninfo.json())

    def set_project_id(self, _project_id):
        self.project_id = _project_id
        return self.project_id

    def get_project_id(self):
        return self.project_id

    def set_member_id(self, _member_id):
        self.member_id = _member_id
        return self.member_id

    def get_member_id(self):
        return self.member_id

    def set_building_id(self, _building_id):
        self.building_id = _building_id
        return self.building_id

    def get_building_id(self):
        return self.building_id

    def set_margin_fee(self, _margin_fee):
        self.margin_fee = _margin_fee
        return self.margin_fee

    def get_margin_fee(self):
        return self.margin_fee

loginsession = requests.session()
headers = {'content-type': 'application/json'}
url =  address + port
adminurl =  address + port



oneProject = Project(address, username, passwd, money, managername, managerpasswd)


updatebuild_data = {
    'login_type': '02',
    'operate': '1',
    'project_id': oneProject.get_project_id(),
    'building': {
        'building_num': time.strftime('%Y-%m-%d.%H:%M:%S', time.localtime(time.time())),
        'community_name': time.strftime('%Y-%m-%d.%H:%M:%S', time.localtime(time.time())),
        'building_ban': '4',
        'building_floor': '4',
        'room_nbr': '4',
        'building_area': '400',
        'res_price': '4000000',
        'bought_date': '20150909',
        'pledge_state': '1',
        'obligee_name': '222',
        'pledge_type': '01',
        'property_type': '01',
        'estate_name_inner': '222',
        'member_id': oneProject.get_member_id(),
    }
}

returninfo = oneProject.get_data(urlupdatebuild, updatebuild_data, headers)
print(oneProject.get_return(returninfo))



