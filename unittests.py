__author__ = 'roger'

import unittest
import main
import json


class LoadSampleLibraries(unittest.TestCase):
    def setUp(self):
        self.ituneslib = main.load_itunes("itunes test library.xml")
        with open("gmusic_sample.json", 'r') as gmusic_dump:
            self.gmusiclib = json.load(gmusic_dump)
        self.exact_match_results = main.exact_match_songs(self.ituneslib, self.gmusiclib)

    def test_itunes_lib_structure(self):
        self.assertIsInstance(self.ituneslib, list)
        self.assertIsInstance(self.ituneslib[0], dict)
        self.assertIsInstance(self.ituneslib[0]['Name'], str)
        self.assertEqual(len(self.ituneslib), 24)

    def test_gmusic_lib_structure(self):
        self.assertEqual(len(self.gmusiclib), 27)

    def test_exact_matches(self):
        self.assertEqual(len(self.exact_match_results['match']), 23)

    def test_exact_mismatches_itunes(self):
        self.assertEqual(self.exact_match_results['imismatch'], [16934])

    def text_exact_mismatches_gmusic(self):
        known_mismatch_set = [u'95c66470-060f-30ec-b2b9-2965b5006f24', u'987130e2-f2e4-3cbc-887d-96835a1d9ada',
                              u'ccab029e-1899-35a6-99bf-554f34711daf', u'24ffedbb-4588-363e-a064-ebcdd2ae63eb']
        self.assertEqual(self.exact_match_results['gmismatch'], known_mismatch_set)

if __name__ == '__main__':
    unittest.main()
