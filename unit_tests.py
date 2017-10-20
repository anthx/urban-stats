import unittest, word_stats


class UniTests(unittest.TestCase):
    word_list = ["five", "bed", "day", "read", "usually", "sexy", "Sexy", "12",
                 "need", "dead", "education", "educated"]

    def testWordsEndingInY(self):
        expected = ["day", "usually", "sexy", "Sexy"]
        actual = word_stats.words_ending_in(self.word_list, "y")
        self.assertEqual(expected, actual)

    def testWordsEndingInEd(self):
        expected = ["bed", "need", "educated"]
        actual = word_stats.words_ending_in(self.word_list, "ed")
        self.assertEqual(expected, actual)