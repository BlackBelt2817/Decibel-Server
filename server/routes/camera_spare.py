from flask import Blueprint, render_template, jsonify, request, Response, send_file
from flask_socketio import emit
import os
import subprocess
#from werkzeug.utils import secure_filename
#from camera import Camera
import io
import threading
from time import sleep
import picamera
from datetime import date
import time

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
LED_PIN = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
motor_channel = (29,31,33,35)
for pin in motor_channel:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

motor_half_step_seq_clockwise = [
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0],
    [1,0,0,1]
]

motor_half_step_seq_counter_clockwise = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

class ControlFunctions():
    
    current_rotation_val = 16
    hold_cw = False
    hold_ccw = False
    
    #Rotating 1/32 of a rotation
    @staticmethod
    def rotate_clockwise():
        for i in range(16):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(motor_channel[pin], motor_half_step_seq_clockwise[halfstep][pin])
#                time.sleep(0.001)
                time.sleep(0.003)

    #Rotating 1/32 of a rotation
    @staticmethod
    def rotate_counter_clockwise():
        for i in range(16):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(motor_channel[pin], motor_half_step_seq_counter_clockwise[halfstep][pin])
#                time.sleep(0.001)
                time.sleep(0.003)
            
    @staticmethod
    def hold_ccw_rotate():
        while ControlFunctions.hold_ccw == True and ControlFunctions.current_rotation_val > 0:
            ControlFunctions.current_rotation_val -= 1
            ControlFunctions.rotate_counter_clockwise()
        
    @staticmethod
    def hold_cw_rotate():
        while ControlFunctions.hold_cw == True and ControlFunctions.current_rotation_val < 32:
            ControlFunctions.current_rotation_val += 1
            ControlFunctions.rotate_clockwise()

curPath = os.path.dirname(__file__)
recordingsPath = curPath + '/../recordings'

routes_camera_spare = Blueprint('routes_camera_spare', __name__)

camera_resolution = '1920x1080'
camera_framerate = 30

cameraSpareStream = picamera.PiCamera(resolution=camera_resolution, framerate=camera_framerate)

class StreamingOutputCameraSpare(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = threading.Condition()
        self.isRecording = False
        self.currentRecordingFolder = ''
        self.currentFileName = ''
        self.currentFileIndex = 1

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
                
            if self.isRecording == True:
                with open(os.path.join(self.currentRecordingFolder, self.currentFileName + '_' + str(self.currentFileIndex) + '.jpeg'), 'wb') as file_to_save:
                    file_to_save.write(self.frame)
                    self.currentFileIndex += 1
                    
            self.buffer.seek(0)
        return self.buffer.write(buf)

outputCameraSpareStream = StreamingOutputCameraSpare()
    
def socket_init_camera_spare(socketio):
    @socketio.on('startRecordingSpare')
    def startRecordingSpare(data):
        outputCameraSpareStream.isRecording = True
        outputCameraSpareStream.currentFileName = data['timestampFilename']
        cameraSpareRecordingDir = os.path.join(recordingsPath, data['timestampFilename'])
        if not os.path.exists(cameraSpareRecordingDir):
            os.makedirs(cameraSpareRecordingDir)
        outputCameraSpareStream.currentRecordingFolder = cameraSpareRecordingDir
        emit('sendRecordingStatusSpare', True, broadcast=True)

    @socketio.on('stopRecordingSpare')
    def stopRecordingSpare():
        outputCameraSpareStream.isRecording = False
        outputCameraSpareStream.currentFileIndex = 1
#        emit('sendData', os.path.join(outputCameraSpareStream.currentRecordingFolder, outputCameraSpareStream.currentFileName + '_' + str(outputCameraSpareStream.currentFileIndex) + '.jpeg'), broadcast=True)
        emit('sendRecordingStatusSpare', False, broadcast=True)
        emit('receiveRecordingFiles', os.listdir(outputCameraSpareStream.currentRecordingFolder), broadcast=True)
#        os.chdir(outputCameraSpareStream.currentRecordingFolder)
#        subprocess.call(['ffmpeg', '-framerate', camera_framerate, '-i', outputCameraSpareStream.currentFileName + '%d.jpeg', outputCameraSpareStream.currentFileName + '.mp4'])

    @socketio.on('getVideoFrameSpare')
    def getVideoFrame():
        emit('receiveVideoFrameSpare', outputCameraSpareStream.frame, broadcast=True)
        
    @socketio.on('getOutputIsRecording')
    def getOutputIsRecording():
        emit('sendOutputIsRecording', outputCameraSpareStream.isRecording, broadcast=True)
        
    
    @socketio.on('cameraSpareRotateCW')
    def rotateCW():
        ControlFunctions.rotate_clockwise()
        
    @socketio.on('cameraSpareRotateCCW')
    def rotateCCW():
        ControlFunctions.rotate_counter_clockwise()
    
        
@routes_camera_spare.route('/cameraSpare/recordings/file/get/<fileName>', methods=['GET'])
def getRecordingFile(fileName):
    try:
        return send_file(os.path.join(outputCameraSpareStream.currentRecordingFolder, fileName))
#        return jsonify({'data': os.path.join(outputCameraSpareStream.currentRecordingFolder, fileName), 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
    


