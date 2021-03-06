import unittest, word_stats


class UniTests(unittest.TestCase):
    naughty_words = []
    with open("word_lists/LDNOOBW_en.txt") as naughty_words_list:
        naughty_words = naughty_words_list.read().splitlines()

    word_list = ["five", "bed", "day", "read", "usually", "sexy", "Sexy", "12",
                 "need", "dead", "education", "educated", "five", "five", "day"]
    all_words = "1. The cat sat on the mat. Is he glad? Wait, it's actually a she!"
    expected_word_frequency = {"five": 3, "bed": 1, "day": 2, "usually": 1, "sexy": 1,
                "Sexy": 1, "12": 1, "need": 1, "dead": 1, "education": 1,
                "educated": 1, "read": 1}
    expected_sentence_importance = {"The cat sat on the mat.": 2, "Wait, it's actually a she!": 1}
    expected_sentences = ["The cat sat on the mat.", "Is he glad?",
                          "Wait, it's actually a she!"]

    def testWordsEndingInY(self):
        expected = ["day", "usually", "sexy", "Sexy"]
        actual = word_stats.words_ending_in(self.word_list, "y")
        self.assertEqual(expected, actual)

    def testWordsEndingInEd(self):
        expected = ["bed", "need", "educated"]
        actual = word_stats.words_ending_in(self.word_list, "ed")
        self.assertEqual(expected, actual)

    def testSentenceSplit(self):
        actual = word_stats.eng_sentence_splitter(self.all_words)
        self.assertEqual(self.expected_sentences, actual)

    def testWordFrequency(self):
        actual = word_stats.word_frequency(self.word_list)
        self.assertEqual(self.expected_word_frequency, actual)

    def testSentenceImportance(self):
        actual = word_stats.sentence_importance(self.expected_sentences, ["cat", "mat", "she!"])
        self.assertEqual(self.expected_sentence_importance, actual)

    def testTop3Words(self):
        expected = [("five", 3, "25.0%"), ("day", 2, "16.67%"), ("bed", 1, "8.33%")]
        actual = word_stats.top_x_words(self.expected_word_frequency, 3)
        self.assertEqual(expected, actual)

    def testTop3Sentences(self):
        expected = [('The cat sat on the mat.', 2, '66.67%'),
                    ("Wait, it's actually a she!", 1, '33.33%')]
        actual = word_stats.top_x_sentences(self.expected_sentence_importance, 3)
        self.assertEqual(expected, actual)

    def testAtMost3(self):
        expected = ["bed","day", "12", "day"]
        actual = word_stats.words_at_most(self.word_list, 3)
        self.assertEqual(expected, actual)

    def testAtLeast5(self):
        expected = ["usually", "education", "educated"]
        actual = word_stats.words_at_least(self.word_list, 5)
        self.assertEqual(expected, actual)

    def testNaughtyText(self):
        naughty_text = "My ass hurts because of the dingleberry."
        self.assertTrue(
            word_stats.text_is_naughty(self.naughty_words, naughty_text),
            "naughty words not found")
        naughty_text_2 = "Prefer blow jobs or handjobs"
        self.assertTrue(
            word_stats.text_is_naughty(self.naughty_words, naughty_text_2),
                        "naughty words not found")

    def testNotNaugtyText(self):
        not_naught_text = "I'll pass on the hand waving thanks. I like my job."
        not_naughty_text_2 = "The fan blows hot air."
        self.assertIs(word_stats.text_is_naughty(self.naughty_words, not_naught_text), False,
                         "false positive")
        self.assertIs(word_stats.text_is_naughty(self.naughty_words, not_naughty_text_2), False,
                         "faslse positive")