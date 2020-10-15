import random
import string
from typing import List


class SmsInfo:
    def __init__(self):
        self.m_send_phone_num: str = ''
        self.m_receive_phone_num: str = ''
        self.m_content: str = ''
        self.m_send_time: str = ''


class SmsSendDataGenerator:

    @staticmethod
    def generate_random_phone_number() -> str:
        res = '1'
        for i in range(10):
            res += str(random.randint(0, 9))
        return res

    @staticmethod
    def generate_random_sms_content() -> str:
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        return random_str

    @classmethod
    def generate_sms_info_list(cls, data_len: int) -> List[SmsInfo]:
        sms_info_list: List[SmsInfo] = list()
        for i in range(data_len):
            sms_info = SmsInfo()
            sms_info.m_send_phone_num = cls.generate_random_phone_number()
            sms_info.m_receive_phone_num = '18616739315'
            sms_info.m_content = cls.generate_random_sms_content()
            sms_info_list.append(sms_info)
        return sms_info_list
