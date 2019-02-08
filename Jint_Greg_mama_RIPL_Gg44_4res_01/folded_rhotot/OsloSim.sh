#clean
#rm counting.eps counting.pdf counting.ps extendLH.cnt fermigas.cnt fgerr.rsg fg.rsg fgteo.rsg input.* resp.dat figegain.dat figegaout.dat rholev.cnt rhopaw.* rhosp.rsg rhotmopaw.cnt sigext.eps sigextpaw.cnt sigext.pdf sigext.ps sigpaw.cnt sigpaw.rsg sigsp.rsg spincut.cnt spincut.eps spincut.pdf spincut.ps spindis.rbn strength.eps strength.nrm strength.pdf strength.ps transext.* trans.nrm

# Running with oslo software git-commit:
#commit aa1425eab3df18bd5cfca32236ad546ca3c09b80 (HEAD -> Oscar2017Response, origin/Oscar2017Response)
#Author: Vetle W. Ingeberg <vetlewi@users.noreply.github.com>
#Date:   Wed Jun 13 13:53:54 2018 +0200
#
#    Counting can now smooth discrete level density with a certain FWHM


# declare for later
msg="Dont listen to the above fortran error. No gracious way to close mama with bash"

# takes ExEg.m from RAINIER and folds the NaI 2012 CACTUS det resp into ExEgFo.m
#mama < FoldExEg.mama
#echo $msg

# # takes ExEg.m from RAINIER and folds the NaI 2012 CACTUS det resp into ExEgFo.m
# # unfolds spectrum to ExEgUnFo.m with same det response: effectively smooths
mama < in_mama_foun.txt
echo $msg

# # Extracts first generation spectrum, fg.m
# this script (fg_cut) cuts away the gammas below ~1.3MeV
# (valley correction)
# + compression by factor of 4
mama < in_mama_fg_cut.txt
echo $msg

# first generation matrix in rhosigchi
rhosigchi < in_rsg_fg.txt

# counting
echo | counting
root.exe .x counting.cpp # oslo version
# need to close by hand to continue

# spin cut
# root.exe .x spincut.cpp
# sigext
# root.exe .x sigext.cpp

#normalization
echo | normalization

# strength
root.exe .x strength.cpp # oslo version

