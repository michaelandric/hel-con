# May 13 14:50 @andric
"""Getting aparc aseg."""

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


class GetAseg(object):
    """Making aparc aseg."""

    def __init__(self, fs_dir, asegname):
        self.fs_dir = fs_dir
        self.asegname = asegname
        os.environ['SUBJECTS_DIR'] = fs_dir

    def mri_convert(self, mgz_file):
        """Convert from mgz to nii."""
        stdf = open('stdout_files/stdout_from_mri_convert.txt', 'w')
        cmdargs = split('mri_convert -ot nii {}.mgz {}.nii'.format(
            self.asegname, self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()

    def align_centers(self, surfvol):
        """Doing alignment with SurfVol."""
        stdf = open('stdout_files/stdout_from_align_centers.txt', 'w')
        cmdargs = split('@Align_Centers -base {} -dset {}.nii -no_cp'.format(
            surfvol, self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()

    def merge(self):
        """getting rank file."""
        stdf = open('stdout_files/stdout_from_aseg_merge.txt', 'w')
        cmdargs = split('3dmerge -1rank -prefix {}_rank.nii {}.nii'.format(
            self.asegname, self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()

    def roi_label(self):
        """Make roi label file."""
        stdf = open('stdout_files/stdout_from_roi_label.txt', 'w')
        cmdargs = split('@FS_roi_label -name ALL -rankmap {}_rank.rankmap.1D \
                        -labeltable {}_rank > {}_rank.niml.lt.log'.format(
                            self.asegname, self.asegname, self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()

    def refit(self):
        """Do 3drefit to get rank in aparc aseg."""
        stdf = open('stdout_files/stdout_from_refit.txt', 'w')
        cmdargs = split('3drefit -labeltable {}_rank.niml.lt \
                        {}_rank.nii.gz'.format(self.asegname, self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()

    def make_label_table(self):
        """Make label table for reference later."""
        stdf = open('stdout_files/stdout_from_make_label_table.txt', 'w')
        cmdargs = split('@MakeLabelTable -atlasize_labeled_dset \
                        {}_rank.nii.gz'.format(self.asegname))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()


def main():
    """Running the aparc aseg maker."""
    freesurfdir = '/cnari/normal_language/HEL/freesurfdir'
    subject_list = ['hel{}'.format(i) for i in range(1, 12) if
                    i is not 9 and i is not 2]
    for subject in subject_list:
        if subject is 'hel1' or subject is 'hel3':
            year = '2005'
        else:
            year = '2009'
        aseg_name = os.path.join(freesurfdir, subject,
                                 'SUMA/aparc.a{}s+aseg'.format(year))
        asegmaker = GetAseg(freesurfdir, aseg_name)
        mgzfile = os.path.join(freesurfdir, subject,
                               'mri/aparc.a{}}s+aseg.mgz'.format(year))
        asegmaker.mri_convert()
        surf_vol = os.path.join(freesurfdir, subject,
                                'SUMA/{}_SurfVol+orig.BRIK.gz'.format(subject))
        asegmaker.align_centers(surf_vol)
        asegmaker.merge()
        asegmaker.roi_label()
        asegmaker.refit()
        asegmaker.make_label_table()

if __name__ == '__main__':
    main()
