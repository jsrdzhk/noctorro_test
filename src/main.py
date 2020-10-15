import json

from wisbec.date.time import TimeUtil

from src.testdata.test_data_generator import SmsSendDataGenerator, SmsInfo
from src.util.post import PostUtil


class NoctorroTest:
    def __init__(self):
        self.m_send_sms_url: str = 'http://127.0.0.1:8089/modem_pool/send_sms'
        self.m_get_sms_url: str = 'http://127.0.0.1:8088/modem_pool/get_sms'

    def send_sms(self, sms_info: SmsInfo) -> bool:
        send_data = dict()
        send_data['phoneNum'] = sms_info.m_send_phone_num
        send_data['content'] = sms_info.m_content
        r = PostUtil.post_form_data(self.m_send_sms_url, send_data)
        return 'success' in r.text

    def get_sms(self, sms_info: SmsInfo):
        send_data = dict()
        send_data['phoneNumber'] = sms_info.m_receive_phone_num
        send_data['sendTime'] = sms_info.m_send_time
        response_body = PostUtil.post_form_data(self.m_get_sms_url, send_data).text
        loaded = json.loads(response_body)
        if 'obj' not in loaded:
            print('error')
        else:
            sms = loaded['obj']
            if sms != sms_info.m_content:
                print('error:', sms_info)
            else:
                print('success')


def main():
    sms_info_list = SmsSendDataGenerator.generate_sms_info_list(10)
    noctorro_test = NoctorroTest()
    for sms_info in sms_info_list:
        sms_info.m_send_time = TimeUtil.now('%Y-%m-%d %H:%M:%S')
        noctorro_test.send_sms(sms_info)
        noctorro_test.get_sms(sms_info)


if __name__ == '__main__':
    main()
