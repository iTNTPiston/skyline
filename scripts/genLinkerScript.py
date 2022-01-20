# Generates syms600.ld based on LinkerHints in comments in the headers
# Hints must be defined as /* LinkerHints <address> <mangledName> <comment> */
# Included paths (file or directory) need to be added below
import os, csv

# consts
CUSTOM_HEADER = """
/*
 *  This file is generated from LinkerHints in headers
 *  DO NOT EDIT THIS FILE DIRECTLY
 *  Generate with genLinkerScript.py instead
 */

"""
# The paths to search for LinkerHints
INCLUDE = [
    "include/ukr150.hpp",
    "include/sead",
    "include/agl"
]

# LinkerHints
DISABLED = "Disabled"
LINKER_HINTS = "LinkerHints"
# Offset for functions in main (beginning of skyline - beginning of main)
MAIN_OFFSET = "0x2d91000"

LD_OUTPUT = "linkerscripts/syms150.ld"

def addLinkerScriptLine(ldLines, addrStr, mangledName, comment):
    commentStr = ""
    if comment != "":
        commentStr = f"/* {comment} */"

    line = f"{mangledName} = {addrStr} - {MAIN_OFFSET}; {commentStr}"

    ldLines.append(line)

def scanFileForLinkerHints(ldLines, pathStr, headerFile):
    headerLines = headerFile.readlines()
    foundLinkerHintsCount = 0
    disabledCount = 0
    for line in headerLines:
        parts = line.split()
        if len(parts) >= 5 and parts[0] == "/*" and parts[1] == LINKER_HINTS:
            addrStr = parts[2]
            mangledName = parts[3]
            comment = parts[4]
            if comment == "*/":
                comment = ""
            if foundLinkerHintsCount == 0:
                ldLines.append(f"/* {pathStr} Start */")
            addLinkerScriptLine(ldLines, addrStr, mangledName, comment)
            foundLinkerHintsCount+=1
        elif len(parts) >= 3 and parts[0] == "/*" and parts[1] == DISABLED and parts[2] == LINKER_HINTS:
            disabledCount+=1

    if foundLinkerHintsCount != 0:
        print(f"Found {foundLinkerHintsCount} Hints in {pathStr}")
        ldLines.append(f"/* {pathStr} End */")
    if disabledCount != 0:
        print(f"Found {disabledCount} Disabled Hints in {pathStr}")

    return foundLinkerHintsCount


def scanPathForLinkerHints(ldLines, pathStr):
    if os.path.isfile(pathStr):
        with open(pathStr) as headerFile:
            return scanFileForLinkerHints(ldLines, pathStr, headerFile)
    elif os.path.isdir(pathStr):
        dirContent = os.listdir(pathStr)
        dirCount = 0
        for subPathName in dirContent:
            dirCount += scanPathForLinkerHints(ldLines, os.path.join(pathStr, subPathName))
        return dirCount

ldLines = []
count = 0
for pathStr in INCLUDE:
    count += scanPathForLinkerHints(ldLines, pathStr)

print(f"Found {count} LinkerHints Total")

# Write ld
with open(LD_OUTPUT, "w") as ldFile:
    ldFile.write(f"/* {LD_OUTPUT} */\n")
    ldFile.write(CUSTOM_HEADER)

    ldFile.write(f"blank = 0;\n")
    for line in ldLines:
        ldFile.write(line)
        ldFile.write("\n")

print("Done")