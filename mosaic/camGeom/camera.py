import lsst.afw.cameraGeom.cameraConfig
assert type(config)==lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (type(config).__module__, type(config).__name__)
# Plate scale of the camera in arcsec/mm
config.plateScale=17.575

# Name of native coordinate system
config.transformDict.nativeSys='FocalPlane'

config.transformDict.transforms={}
config.transformDict.transforms['Pupil']=lsst.afw.geom.transformConfig.TransformConfig()
config.transformDict.transforms['Pupil'].transform['multi'].transformDict=None
# x, y translation vector
config.transformDict.transforms['Pupil'].transform['affine'].translation=[0.0, 0.0]

# 2x2 linear matrix in the usual numpy order;
#             to rotate a vector by theta use: cos(theta), sin(theta), -sin(theta), cos(theta)
config.transformDict.transforms['Pupil'].transform['affine'].linear=[1.0, 0.0, 0.0, 1.0]

# Coefficients for the radial polynomial; coeff[0] must be 0
config.transformDict.transforms['Pupil'].transform['radial'].coeffs=[0.0, 8.516497674138379e-05, 0.0, -4.501399132955917e-12]

config.transformDict.transforms['Pupil'].transform.name='radial'
config.detectorList={}
config.detectorList[0]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[0].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[0].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[0].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[0].bbox_x0=0

# Name of detector slot
config.detectorList[0].name='E1'

# Pixel size in the x dimension in mm
config.detectorList[0].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys='Pixels'

config.detectorList[0].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[0].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x=-48.81

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y=-30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[0].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[0].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[0].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[0].serial='1'

# pitch (rotation about y) of the detector in degrees
config.detectorList[0].pitchDeg=0.0

# ID of detector slot
config.detectorList[0].id=1

config.detectorList[1]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[1].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[1].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[1].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[1].bbox_x0=0

# Name of detector slot
config.detectorList[1].name='E2'

# Pixel size in the x dimension in mm
config.detectorList[1].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[1].transformDict.nativeSys='Pixels'

config.detectorList[1].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[1].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[1].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_x=-16.07

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_y=-30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[1].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[1].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[1].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[1].serial='2'

# pitch (rotation about y) of the detector in degrees
config.detectorList[1].pitchDeg=0.0

# ID of detector slot
config.detectorList[1].id=2

config.detectorList[2]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[2].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[2].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[2].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[2].bbox_x0=0

# Name of detector slot
config.detectorList[2].name='E3'

# Pixel size in the x dimension in mm
config.detectorList[2].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[2].transformDict.nativeSys='Pixels'

config.detectorList[2].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[2].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[2].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_x=16.67

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_y=-30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[2].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[2].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[2].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[2].serial='3'

# pitch (rotation about y) of the detector in degrees
config.detectorList[2].pitchDeg=0.0

# ID of detector slot
config.detectorList[2].id=3

config.detectorList[3]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[3].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[3].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[3].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[3].bbox_x0=0

# Name of detector slot
config.detectorList[3].name='E4'

# Pixel size in the x dimension in mm
config.detectorList[3].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[3].transformDict.nativeSys='Pixels'

config.detectorList[3].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[3].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[3].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_x=49.41

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_y=-30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[3].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[3].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[3].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[3].serial='4'

# pitch (rotation about y) of the detector in degrees
config.detectorList[3].pitchDeg=0.0

# ID of detector slot
config.detectorList[3].id=4

config.detectorList[4]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[4].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[4].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[4].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[4].bbox_x0=0

# Name of detector slot
config.detectorList[4].name='W5'

# Pixel size in the x dimension in mm
config.detectorList[4].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[4].transformDict.nativeSys='Pixels'

config.detectorList[4].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[4].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[4].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_x=-49.41

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_y=30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[4].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[4].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[4].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[4].serial='5'

# pitch (rotation about y) of the detector in degrees
config.detectorList[4].pitchDeg=0.0

# ID of detector slot
config.detectorList[4].id=5

config.detectorList[5]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[5].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[5].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[5].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[5].bbox_x0=0

# Name of detector slot
config.detectorList[5].name='W6'

# Pixel size in the x dimension in mm
config.detectorList[5].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[5].transformDict.nativeSys='Pixels'

config.detectorList[5].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[5].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[5].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_x=-16.67

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_y=30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[5].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[5].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[5].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[5].serial='6'

# pitch (rotation about y) of the detector in degrees
config.detectorList[5].pitchDeg=0.0

# ID of detector slot
config.detectorList[5].id=6

config.detectorList[6]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[6].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[6].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[6].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[6].bbox_x0=0

# Name of detector slot
config.detectorList[6].name='W7'

# Pixel size in the x dimension in mm
config.detectorList[6].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[6].transformDict.nativeSys='Pixels'

config.detectorList[6].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[6].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[6].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_x=16.07

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_y=30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[6].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[6].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[6].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[6].serial='7'

# pitch (rotation about y) of the detector in degrees
config.detectorList[6].pitchDeg=0.0

# ID of detector slot
config.detectorList[6].id=7

config.detectorList[7]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[7].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[7].bbox_y1=4095

# x1 of pixel bounding box
config.detectorList[7].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[7].bbox_x0=0

# Name of detector slot
config.detectorList[7].name='W8'

# Pixel size in the x dimension in mm
config.detectorList[7].pixelSize_x=0.015

# Name of native coordinate system
config.detectorList[7].transformDict.nativeSys='Pixels'

config.detectorList[7].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_y=2047.5

# Pixel size in the y dimension in mm
config.detectorList[7].pixelSize_y=0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[7].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_x=48.81

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_y=30.97

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[7].transposeDetector=False

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[7].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[7].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[7].serial='8'

# pitch (rotation about y) of the detector in degrees
config.detectorList[7].pitchDeg=0.0

# ID of detector slot
config.detectorList[7].id=8

# Coefficients for radial distortion
config.radialCoeffs=None

# Name of this camera
config.name='MOSAIC1'

