#!/usr/bin/env python
# 
# Found this script parser from this forum post:
# http://ask.metafilter.com/274007/Parsing-movie-TV-scripts
# added polly capabiltiies from Julien Simon's module

from fileinput import input
from re import match
import PollyApi

characters = ["BEVERLY", "WESLEY", "DATA", "GEORDI", "PICARD", "RIKER"]
prefix_speaker = True

actors = {}
actors["BEVERLY"] = "Justin"
actors["WESLEY"] = "Mathieu"
actors["DATA"] = "Hans"
actors["GEORDI"] = "Russell"
actors["GEORDI/MARKHAM"] = "Justin"
actors["PICARD"] = "Kendra"
actors["RIKER"] = "Brian"
actors["RIKER'S VOICE"] = "Brian"

out = speaker = ""

polly = PollyApi.connectToPolly()

for line in input():
    # parse all lines beginning with at least one tab
    result = match(r"^(\t+)(\S.*?)\s*$", line)
    if not result:
        continue
    tabs = len(result.group(1))
    text = result.group(2)
    if tabs == 5:
        # dialogue header
        if speaker != text:
            # speaker changed, print what we've got and start over
            if len(out) > 0:
                if prefix_speaker:
                    voice = actors[speaker]
                    print("%s: %s" % (speaker, out))
                    PollyApi.speak(polly, out, voice)
            out = ""
            speaker = text
    elif tabs == 3 and any(c in speaker for c in characters):
        # spoken line
        # append this line to the dialogue, with a space
        if len(out) > 0:
            out += " "
        out += text
    else:
        # ignore all other lines
        pass

# just in case the input ends in the middle of dialogue
if len(out) > 0:
    print(out)
