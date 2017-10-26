#!python3
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : July 26, 2017
# Last update :
#
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import
from astropy.cosmology import FlatLambdaCDM
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np


def config_dict(config_path):
    """Create a dictionary of variables from input file."""

    # Parse config file and make a dictionary
    with open(config_path, 'r') as f:
        config = {}
        string_regex = re.compile('"(.*?)"')
        value_regex = re.compile('[^ |\t]*')

        for line in f:
            if not line.startswith("#"):
                temp = []
                temp = line.split("=")
                if temp[1].startswith("\""):
                    config[temp[0]] = string_regex.findall(temp[1])[0]
                else:
                    config[temp[0]] = value_regex.findall(temp[1])[0]
    return config

# Create config dictionary
def updated_config(config_path):
    config = config_dict(config_path)
    config_record = copy.deepcopy(config)
    prefix = config['output_folder'] + config['prefix']
    keys = ['catalog_file',         'dislist_file',
            'distortedlist_file',   'convolvedlist_file',
            'HST_image',            'HST_convolved_image',
            'rescaled_outfileb',    'rescaled_outfiled',
            'rescaled_outfilem',    'lsst_unnoised',
            'lsst',                 'lsst_mono' ]
    for key in keys:
        config[key] = prefix + config[key]

    # Add keys for 90 degree rotated case
    pre = '90_' + config_record['prefix']
    for key in keys:
        key90 = '90_' + key
        config[key90] = config['90_output_folder'] + pre + config_record[key]

    return config

def get_bulge_disk_weights(config_path):
    """Get bulge disk weights for jedicolor."""
    config = updated_config(config_path)
    infile = config['bd_weights'] # physics_settings/bd_weight_1.5.txt or so on.
    # print('bd_weights file is: ', infile)
    b,d = np.genfromtxt(infile,delimiter=None,usecols=(0,1),dtype=float,unpack=True)

    return b,d

def replace_outfolder(outfolder):
    """Replace given directory."""
    if os.path.exists(outfolder):
        print('Replacing folder: ', outfolder)
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
    else:
        print('Creating  folder: ', outfolder)
        os.makedirs(outfolder)

def run_process(name, args,):
    """Run a process.

    :Usage:

    run_process("example ", ["./python ", 'example.py', 'arg1' ])

    The first argument "example" is optional.

    Also note the whitespace after the command python.

    .. note::

      This function needs python3 print_funtion.

    """
    print("\n\n\n", "#" * 130)
    print("# Program  : %s\n# Commands :" % name, end=' ')
    for arg in args:
        print(arg, end=' ')

    print("\n", "#" * 130, end='\n\n')

    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
              Return code: %i." % (name, process.returncode))
        sys.exit(1)
    else:
        print("\n\n", "#" * 129, end='\n')
        print("# Success! : %s " % name)
        print("\b", "#" * 129, "\n\n\n")




def lookback_time(z):
    """Get lookback time.

    :Reference: http://www.astro.ufl.edu/~guzman/ast7939/projects/project01.html

    .. math::

      t_L = t_H \int_{0}^{z} \\frac{dz}{(1+z)E(z)} \\

      E(z) = \sqrt{\Omega_M(1+z)^3 + \Omega_K(1+z)^2 + \Omega_{\Lambda}} \\

      Hubble \ Time\ t_H = \\frac{1}{H_0}


    """
    from astropy.cosmology import FlatLambdaCDM
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    age0 = cosmo.age([0]).value
    age_z = cosmo.age([z]).value
    tL = age0 - age_z
    # print( 'Lookback time for z = {} is  {:.2f} Gyr.'.format(z, tL[0]))

    return tL[0]


def age(z):
    """Get age of the galaxy for FlatLambda CDM model."""
    from astropy.cosmology import FlatLambdaCDM
    z = float(z)
    # print("z = {}".format(z))
    # print("type(z) = {}".format(type(z)))
    
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    age_univ = cosmo.age([z]).value
    age_univ = age_univ[0]
    # print( 'Age of Universe for z = {} is  {:.2f} Gyr'.format(z, age_univ))
    # print( 'Age of Universe for z = {} is  {:.2f} Gyr'.format(0, cosmo.age([0]).value[0]))
    # print( 'Age of Universe for z = {} is  {:.2f} Gyr'.format(4, cosmo.age([4]).value[0]))
    # 
    return age_univ


def main():
    """Run main function."""
    age(1.5)

if __name__ == "__main__":
    main()
