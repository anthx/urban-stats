import unittest, word_stats


class UniTests(unittest.TestCase):
    word_list = ["five", "bed", "day", "read", "usually", "sexy", "Sexy", "12",
                 "need", "dead", "education", "educated"]
    all_words = "1. The cat sat on the mat. Is he glad? Wait, it's actually a she!"

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