import unittest, word_stats


class UniTests(unittest.TestCase):
    word_list = ["five", "bed", "day", "read", "usually", "sexy", "Sexy", "12",
                 "need", "dead", "education", "educated", "five", "five", "day"]
    all_words = "1. The cat sat on the mat. Is he glad? Wait, it's actually a she!"
    expected_word_frequency = {"five": 3, "bed": 1, "day": 2, "usually": 1, "sexy": 1,
                "Sexy": 1, "12": 1, "need": 1, "dead": 1, "education": 1,
                "educated": 1, "read": 1}
    def testWordsEndingInY(self):
        expected = ["day", "usually", "sexy", "Sexy"]
        actual = word_stats.words_ending_in(self.word_list, "y")
        self.assertEqual(expected, actual)

    def testWordsEndingInEd(self):
        expected = ["bed", "need", "educated"]
        actual = word_stats.words_ending_in(self.word_list, "ed")
        self.assertEqual(expected, actual)

    def testSentenceSplit(self):
        expected = ["The cat sat on the mat.", "Is he glad?", "Wait, it's actually a she!"]
        actual = word_stats.eng_sentence_splitter(self.all_words)
        self.assertEqual(expected, actual)

    def testWordFrequency(self):
        actual = word_stats.word_frequency(self.word_list)
        self.assertEqual(self.expected_word_frequency, actual)

    def testTop3Words(self):
        expected = [("five", 3, "25.0%"), ("day", 2, "16.67%"), ("bed", 1, "8.33%")]
        actual = word_stats.top_x_words(self.expected_word_frequency, 3)
        self.assertEqual(expected, actual)