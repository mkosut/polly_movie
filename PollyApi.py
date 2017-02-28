#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author Julien Simon, https://github.com/juliensimon/aws/blob/master/rekognition/PollyApi.py

import os, boto3

defaultRegion = 'eu-west-1'
defaultUrl = 'https://polly.eu-west-1.amazonaws.com'

def connectToPolly(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('polly', region_name=regionName, endpoint_url=endpointUrl)

def speak(polly, text, voice='Brian', format='mp3' ):
    resp = polly.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)
    soundfile = open('/tmp/sound.mp3', 'wb')
    soundBytes = resp['AudioStream'].read()
    soundfile.write(soundBytes)
    soundfile.close()
    os.system('afplay /tmp/sound.mp3')  # Works only on Mac OS, sorry
    os.remove('/tmp/sound.mp3')
