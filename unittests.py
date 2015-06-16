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
        self.assertEqual(len(self.ituneslib), 26, msg="Wrong # of songs in iTunes library, " +
                                                      "got {0!s}, expected 26.".format(len(self.ituneslib)))

    def test_gmusic_lib_structure(self):
        self.assertEqual(len(self.gmusiclib), 29, msg="Wrong # of songs in Google Play Music library, "
                                                      "got {0!s}, expected 29.".format(len(self.gmusiclib)))

    def test_exact_matches(self):
        matches = self.exact_match_results['match']
        self.assertNotEqual(len(matches), 0, msg="Found no exact matches, expected 24.")
        self.assertEqual(len(matches),
                         24, msg="Wrong # of exact matches, got {0!s}, "
                                 "expected 24".format(len(matches)))

    def test_exact_mismatches_itunes(self):
        imismatch = self.exact_match_results['imismatch']
        self.assertLessEqual(len(imismatch), 5, msg="Too many exact mismatches, got {0!s}, "
                                                    "expected 5.".format(len(imismatch)))
        self.assertNotIn(7400, imismatch, msg="Matched with same title/wrong artist")
        self.assertNotIn(6526, imismatch, msg="Matched with same title/wrong artist")

        self.assertEqual(imismatch, [10534, 16934], msg="Other matching errors, got {0!s}, "
                                                        "expected [10534, 16934]".format(len(imismatch)))

    def test_exact_mismatches_gmusic(self):
        known_mismatch_set = [u'95c66470-060f-30ec-b2b9-2965b5006f24', u'987130e2-f2e4-3cbc-887d-96835a1d9ada',
                              u'ccab029e-1899-35a6-99bf-554f34711daf', u'24ffedbb-4588-363e-a064-ebcdd2ae63eb',
                              u'7b362b61-8203-32b6-b97e-45bb4b4ff6e1']
        self.assertEqual(sorted(self.exact_match_results['gmismatch']), sorted(known_mismatch_set))

    def test_close_matches(self):
        pass

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()
