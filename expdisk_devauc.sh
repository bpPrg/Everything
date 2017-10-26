# Galfit Basics:
# Galfit Command to Create Model
# =====================================
# command: galfit INPUT_PARAMETER_FILE
# outputs: a) fit.log
#          b) galfit.01
#          c) imgbolock.fits
#
# a) fit.log       ==>  appended each time on the same fit.log
# b) galfit.XX     ==> created new each time e.g. galfit.01, galfit.02
# c) imgblock.fits ==> it has 4 frames.
#                      0 is empty, 1 is input, 2 is model , 3 is residual.
#
#  command: ds9 -multiframe imgblock.fits
#  output : we can see 4 frames. (we can also save frames from ds9)
#
# Galfit Command to Fit componets from the model just created
# =============================================================
# command: galfit -o3 galfit.01 && rm -r galfit.01
# output : a) subcomps.fits
#          The subcomps.fits has two or more frames.
#                     0 is subcomps.fits, 1 is expdisk, 2 is devauc etc.
#
# INPUT_PARAMETER_FILE for galfit has two components:
# =============================================================
# a) CONTROL PARAMETERS:  A-P   (these are compulsory)
# b) OBJECT PARAMETERS: 0-10 Z  (it should be at least one, e.g. devauc)
#
# a) CONTROL PARAMETERS
#        * These are fixed, not initial guesses.
#        * F: The row F is for masking
#            ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits  # in mask, image is 0 and rest is 1.
#            If the bad pixel input file is a FITS image, all non-zero valued
#            pixels would be ignored during the fit. The pixel numbers where
#            value is 0 is only fitted.
#         * E: psf fine sampling factor is 2
#         * K: in my case plate scale is 0.06
#
# b) OBJECT PARAMETERS:
#         * These are initial guesses.
#         * Second column 1 means value not-fixed.
#         * Z: 0 fits the model, do not choose 1 while fitting.
#         * Better initial guess makes the simulation faster.
#           e.g. for sect23_f814w_gal0.fits
#           NAXIS1  =  601
#           NAXIS2  =  601
#
#           MAG     =  20.282
#           RADIUS  =  14.514
#
#           PIXSCALE=  0.06 
#           MAG0    =  26.78212 for f814w (26.6611 for f606, f814)
#
#           Zoom and guess the center or brightest pixel of galaxy
#           x,y = 296.0 307.0
#
#   Main commands : ic '1 0 %1 0 == ?'  INPUT_GALAXY  > mask.fits
#                 rm -r imgblock.fits subcomps.fit ; galfit expdisk_devauc.sh
#                 galfit -o3 galfit.01 && rm -r galfit.01
#                 ds9 -cmap a -scale log -multiframe imgblock.fits subcomps.fits &
#
# rm -rf mask.fits; ic '1 0 %1 0 == ?'  /Users/poudel/Research/a1_data/original_data/stamps_new_0_200/sect23_f814w_gal0.fits  > mask.fits
# /Applications/ds9.app/Contents/MacOS/ds9 mask.fits /Users/poudel/Research/a1_data/original_data/stamps_new_0_200/sect23_f814w_gal39.fits &
# ds9 mask.fits /Users/poudel/Research/a1_data/original_data/stamps_new_0_200/sect23_f814w_gal39.fits &
#
# NOTE: x,y  mag, Rs changes for each galaxy
# for example for sect23_f814w_gal0.fits:
# x,y,mag,Rs = 296.0 307.0 20.282 14.514
#
#

# IMAGE and GALFIT CONTROL PARAMETERS
A) /Users/poudel/Research/a1_data/original_data/stamps_new_0_200/sect23_f814w_gal0.fits
B) imgblock.fits       # Output data image block
C) none                # Sigma image name (made from data if blank or "none")
D) f814w_psf.fits # Input PSF image and (optional) diffusion kernel
E) 2                   # PSF fine sampling factor relative to data
F) mask.fits           # Bad pixel mask (FITS image or ASCII coord list)
G) none                # File with parameter constraints (ASCII file)
H) 1 601 1 601         # Image region to fit (xmin xmax ymin ymax)
I) 200  200            # Size of the convolution box (x y)
J) 26.78212 # Magnitude photometric zeropoint
K) 0.06 0.06 # Plate scale (dx dy)    [arcsec per pixel]
O) regular             # Display type (regular, curses, both)
P) 0                   # Choose: 0=optimize, 1=model, 2=imgblock, 3=subcomps

# IMAGE and GALFIT OBJECT PARAMETERS
# Component number: 1
# Exponential function (concentration index n = 1)
# This gives disk profile.
0) expdisk            # Object type
1) 296.0 307.0 1 1         # position x, y        [pixel]
3) 20.282 1         # total magnitude
4) 14.514 1         #     Rs               [Pixels]
9) 0.5        1       # axis ratio (b/a)
10) 100.0      1      # position angle (PA)  [Degrees: Up=0, Left=90]
Z) 0                  #  Skip this model in output image?  (yes=1, no=0)


# Component number: 2
# deVaucouleur function (concentration index n = 4)
# This gives the bulge profile.
0) devauc             # Object type
1) 296.0 307.0 1 1         # position x, y        [pixel]
3) 20.282 1         # total magnitude
4) 14.514 1         #     R_e              [Pixels]
9) 0.5        1       # axis ratio (b/a)
10) 100.0       1     # position angle (PA)  [Degrees: Up=0, Left=90]
Z) 0                  #  Skip this model in output image?  (yes=1, no=0)
