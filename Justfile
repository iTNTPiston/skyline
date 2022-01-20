# Version (1.5.0)
VERSION := 150

# Wrapper for scripts/genUkingHeader.py
header:
    python3 scripts/genUkingHeader.py

# Wrapper for scripts/genLinkerScript.py 
ldscript:
    python3 scripts/genLinkerScript.py

# Wrapper for scripts/patchNpdm.py
npdm:
    python3 scripts/patchNpdm.py main.npdm skyline{{VERSION}}.npdm

build:
    just skyline
    just patch

skyline:
    make skyline

# Wrapper for scripts/genPatch.py
patch:
    python3 scripts/genPatch.py {{VERSION}}

# Cleans the elf and ips
clean:
    make clean
    rm -f skyline{{VERSION}}.ips

# Clean the build output and all generated files
cleanall: clean
    rm -f include/uking/functions.hpp
    rm -f linkerscripts/syms{{VERSION}}.ld
    rm -f skyline{{VERSION}}.npdm

# Wrapper for scripts/deploy.py
deploy IP:
    python3 scripts/ftpDeploy.py {{IP}} {{VERSIOn}}