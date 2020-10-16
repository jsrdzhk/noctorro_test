import json
import threading

from wisbec.date.time import TimeUtil
from wisbec.logging.log import Log

from src.testdata.test_data_generator import SmsSendDataGenerator, SmsInfo
from src.util.post import PostUtil


class NoctorroTest:
    def __init__(self):
        self.m_send_sms_url: str = 'http://127.0.0.1:8089/modem_pool/send_sms'
        self.m_get_sms_url: str = 'http://127.0.0.1:8088/modem_pool/get_sms'
        self.m_is_phone_num_available_url: str = 'http://127.0.0.1:8088/modem_pool/apply_for_phone_number'
        self.m_lock: threading.Lock = threading.Lock()

    def apply_for_phone_number(self, sms_info: SmsInfo) -> bool:
        send_data = dict()
        send_data['phoneNum'] = sms_info.m_receive_phone_num
        r = PostUtil.post_form_data(self.m_is_phone_num_available_url, send_data)
        return 'success' in r.text

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
            Log.error('error response')
        else:
            sms = loaded['obj']
            if sms != sms_info.m_content:
                Log.error('error:{}', sms_info.m_content)
            else:
                Log.info('success')

    def thread_test_case(self, sms_info: SmsInfo):
        if self.apply_for_phone_number(sms_info):
            sms_info.m_send_time = TimeUtil.now('%Y-%m-%d %H:%M:%S')
            self.send_sms(sms_info)
            self.get_sms(sms_info)
        else:
            Log.info('{} is busy', sms_info.m_receive_phone_num)

    def test_main(self):
        sms_info_list = SmsSendDataGenerator.generate_sms_info_list(10)
        for sms_info in sms_info_list:
            threading.Thread(target=self.thread_test_case, args=[sms_info]).start()


def main():
    Log.init_logger(is_log_to_file=False)
    noctorro_test = NoctorroTest()
    noctorro_test.test_main()


if __name__ == '__main__':
    main()
