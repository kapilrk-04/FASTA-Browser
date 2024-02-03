import sys
sys.path.append('../..')
from send_email_module import send_mail_with_attachment

import unittest

class TestSendEmail(unittest.TestCase):
    def test_send_email(self):
        try:
            send_mail_with_attachment(
                to=['kkrk90792@gmail.com'],
                subject='Test',
                body='<p>Test</p>',
                attachment_data=b'',
                attachment_name='test.txt',
                to_mail='kkrk90792@gmail.com',
            )
        except Exception as e:
            print(e)
            self.fail()

    def test_send_mail_with_image(self):
        try:
            send_mail_with_attachment(
                to=['kkrk90792@gmail.com'],
                subject='Test with image',
                body='<p>Test</p>',
                attachment_data=b'',
                attachment_name='test.txt',
                to_mail='kkrk90792@gmail.com',
                imgpath='tests/unit_tests/msaout.png'
            )
        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
