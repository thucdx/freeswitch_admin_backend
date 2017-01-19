import unittest

from fsadmin.conference import Conference


class ConferenceTest(unittest.TestCase):
    @staticmethod
    def getcontent(file_name):
        content = ''
        with open(file_name) as f:
            for line in f:
                content += line
        return content

    def test_parse(self):
        str = ConferenceTest.getcontent('../sample/conference_list_02.txt')
        conference_list = Conference.from_string(str)
        self.assertEqual(len(conference_list), 2)
        self.assertEquals(len(conference_list[0].users), 3)
        self.assertEquals(conference_list[0].name, '3000-172.31.6.132')

        self.assertEquals(len(conference_list[1].users), 1)
        self.assertEquals(conference_list[1].name, '3002-172.31.6.132')

    def testParseHeader01(self):
        conference_header = 'Conference 3000-172.31.6.132 (1 member rate: 8000 flags: ' \
                            'running|answered|enforce_min|dynamic|exit_sound|enter_sound|json_status) '

        conf = Conference.from_header(conference_header)
        self.assertEquals(conf.name, '3000-172.31.6.132')
        self.assertEquals(conf.total, 1)
        self.assertEquals(conf.rate, 8000)
        self.assertEquals(conf.flags, 'running|answered|enforce_min|dynamic|exit_sound|enter_sound|json_status')

    def testParseHeader02(self):
        conference_header = 'Conference 3000-172.31.6.132 (3 members rate: 8000 flags: ' \
                            'running|answered|enforce_min|dynamic|exit_sound|enter_sound|json_status) '

        conf = Conference.from_header(conference_header)
        self.assertEquals(conf.name, '3000-172.31.6.132')
        self.assertEquals(conf.total, 3)
        self.assertEquals(conf.rate, 8000)
        self.assertEquals(conf.flags, 'running|answered|enforce_min|dynamic|exit_sound|enter_sound|json_status')


