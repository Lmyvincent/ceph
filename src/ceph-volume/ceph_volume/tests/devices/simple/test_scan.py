import os
import pytest
from ceph_volume.devices.simple import scan


class TestScan(object):

    def test_main_spits_help_with_no_arguments(self, capsys):
        scan.Scan([]).main()
        stdout, stderr = capsys.readouterr()
        assert 'Scan an OSD directory for files' in stdout


class TestGetContents(object):

    def test_multiple_lines_are_left_as_is(self, tmpfile):
        magic_file = tmpfile(contents='first\nsecond\n')
        scanner = scan.Scan([])
        assert scanner.get_contents(magic_file) == 'first\nsecond\n'

    def test_extra_whitespace_gets_removed(self, tmpfile):
        magic_file = tmpfile(contents='first   ')
        scanner = scan.Scan([])
        assert scanner.get_contents(magic_file) == 'first'

    def test_single_newline_values_are_trimmed(self, tmpfile):
        magic_file = tmpfile(contents='first\n')
        scanner = scan.Scan([])
        assert scanner.get_contents(magic_file) == 'first'


class TestEtcPath(object):

    def test_directory_is_valid(self, tmpdir):
        path = str(tmpdir)
        scanner = scan.Scan([])
        scanner._etc_path = path
        assert scanner.etc_path == path

    def test_directory_does_not_exist_gets_created(self, tmpdir):
        path = os.path.join(str(tmpdir), 'subdir')
        scanner = scan.Scan([])
        scanner._etc_path = path
        assert scanner.etc_path == path
        assert os.path.isdir(path)

    def test_complains_when_file(self, tmpfile):
        path = tmpfile()
        scanner = scan.Scan([])
        scanner._etc_path = path
        with pytest.raises(RuntimeError):
            scanner.etc_path
