#!/usr/bin/env python

import os
import sys
import commands
import time
import shutil
from optparse import OptionParser

class MaskOps:

    def get_opts(self):
        desc="""
        This is a program to make white matter and ventricle masks to then regress out some sources of nuisance noise. It uses AFNI functions, as well as FSL.  You will need an environment variable 'FSLDIR' pointing to the FSL directory. Note: Make sure to include '+orig' for all input AFNI data types specified here.
        """
        self.usage = "usage: %prog [options]"
        self.parser = OptionParser(description=desc, version="%prog 28.April.2010")
        self.parser.add_option("--identity", dest="id",
            help="subject and/or run identifier")
        self.parser.add_option("--volume", dest="vol",
            help="this is your volume data")
        self.parser.add_option("--automask", dest="amask",
            help="Specify the name of the automask")
        self.parser.add_option("--makeautobox", dest="doautobox",
            help="Do you want to use 3dAutobox to crop the volume image? Answer 'y' for yes and 'n' for no")
        self.parser.add_option("--location", dest="loc",
            help="Specify the working directory. this option is for the benefit of swift functionality.")

        (self.options, args) = self.parser.parse_args()
        if len(args) !=0:
            self.parser.error("your arguments == NO BUENO! maybe you put in a flag without giving the argument? maybe you're just messing with me??")

        

