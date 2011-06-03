#!/usr/bin/env python

import unittest
import os
import tempfile
import shutil

from ..git import Repository


class TestInRepo(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_in_repo_true_top(self):
        """test that in_repo() returns True when in a git repo"""
        os.chdir(self.tmpdir)
        repo = Repository(self.tmpdir)
        repo.shell("git", "init")

        self.assertTrue(repo.in_repo())

    def test_in_repo_true_subdir(self):
        """test that in_repo() returns True when in a git repo subdir"""
        os.chdir(self.tmpdir)
        repo = Repository(self.tmpdir)
        repo.shell("git", "init")

        subdir = os.path.join(self.tmpdir, "subdir")
        os.mkdir(subdir)
        os.chdir(subdir)

        self.assertTrue(repo.in_repo())

    def test_in_repo_false_another_repo(self):
        """
        test that in_repo() returns False when in a git repo that isnt
        ours
        """
        repo1_dir = os.path.join(self.tmpdir, "repo1")
        os.mkdir(repo1_dir)
        repo2_dir = os.path.join(self.tmpdir, "repo2")
        os.mkdir(repo2_dir)

        os.chdir(repo1_dir)
        repo1 = Repository(repo1_dir)
        repo1.shell("git", "init")

        os.chdir(repo2_dir)
        repo2 = Repository(repo2_dir)
        repo2.shell("git", "init")

        self.assertFalse(repo1.in_repo())

    def test_in_repo_false(self):
        """test that in_repo() returns False when not in a git repo"""
        self.assertFalse(Repository(self.tmpdir).in_repo())
