import lsst.afw.cameraGeom.cameraConfig
assert type(config) == lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (
    type(config).__module__, type(config).__name__)
# Plate scale of the camera in arcsec/mm
config.plateScale = 17.575

# Name of native coordinate system
config.transformDict.nativeSys = 'FocalPlane'

config.transformDict.transforms = {}
config.transformDict.transforms['Pupil'] = lsst.afw.geom.transformConfig.TransformConfig()
config.transformDict.transforms['Pupil'].transform['multi'].transformDict = None
# x, y translation vector
config.transformDict.transforms['Pupil'].transform['affine'].translation = [0.0, 0.0]

# 2x2 linear matrix in the usual numpy order;
#             to rotate a vector by theta use: cos(theta), sin(theta), -sin(theta), cos(theta)
config.transformDict.transforms['Pupil'].transform['affine'].linear = [1.0, 0.0, 0.0, 1.0]

# Coefficients for the radial polynomial; coeff[0] must be 0
config.transformDict.transforms['Pupil'].transform['radial'].coeffs = [
    0.0, 8.516497674138379e-05, 0.0, -4.501399132955917e-12]

config.transformDict.transforms['Pupil'].transform.name = 'radial'
config.detectorList = {}
config.detectorList[0] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[0].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[0].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[0].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[0].bbox_x0 = 0

# Name of detector slot
config.detectorList[0].name = 'S29'

# Pixel size in the x dimension in mm
config.detectorList[0].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys = 'Pixels'

config.detectorList[0].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[0].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x = -185.59199999999998

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y = -63.748000000000005

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[0].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[0].yawDeg = -0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[0].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[0].serial = '1'

# pitch (rotation about y) of the detector in degrees
config.detectorList[0].pitchDeg = 0.0

# ID of detector slot
config.detectorList[0].id = 1

config.detectorList[1] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[1].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[1].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[1].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[1].bbox_x0 = 0

# Name of detector slot
config.detectorList[1].name = 'S30'

# Pixel size in the x dimension in mm
config.detectorList[1].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[1].transformDict.nativeSys = 'Pixels'

config.detectorList[1].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[1].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[1].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_x = -185.54199999999997

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_y = -0.023999999999999133

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[1].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[1].yawDeg = -0.105

# roll (rotation about x) of the detector in degrees
config.detectorList[1].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[1].serial = '2'

# pitch (rotation about y) of the detector in degrees
config.detectorList[1].pitchDeg = 0.0

# ID of detector slot
config.detectorList[1].id = 2

config.detectorList[2] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[2].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[2].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[2].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[2].bbox_x0 = 0

# Name of detector slot
config.detectorList[2].name = 'S31'

# Pixel size in the x dimension in mm
config.detectorList[2].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[2].transformDict.nativeSys = 'Pixels'

config.detectorList[2].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[2].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[2].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_x = -185.618

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_y = 63.775999999999996

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[2].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[2].yawDeg = -0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[2].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[2].serial = '3'

# pitch (rotation about y) of the detector in degrees
config.detectorList[2].pitchDeg = 0.0

# ID of detector slot
config.detectorList[2].id = 3

config.detectorList[3] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[3].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[3].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[3].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[3].bbox_x0 = 0

# Name of detector slot
config.detectorList[3].name = 'S25'

# Pixel size in the x dimension in mm
config.detectorList[3].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[3].transformDict.nativeSys = 'Pixels'

config.detectorList[3].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[3].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[3].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_x = -151.832

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_y = -95.611

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[3].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[3].yawDeg = -0.004

# roll (rotation about x) of the detector in degrees
config.detectorList[3].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[3].serial = '4'

# pitch (rotation about y) of the detector in degrees
config.detectorList[3].pitchDeg = 0.0

# ID of detector slot
config.detectorList[3].id = 4

config.detectorList[4] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[4].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[4].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[4].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[4].bbox_x0 = 0

# Name of detector slot
config.detectorList[4].name = 'S26'

# Pixel size in the x dimension in mm
config.detectorList[4].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[4].transformDict.nativeSys = 'Pixels'

config.detectorList[4].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[4].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[4].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_x = -151.87

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_y = -31.869

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[4].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[4].yawDeg = 0.025

# roll (rotation about x) of the detector in degrees
config.detectorList[4].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[4].serial = '5'

# pitch (rotation about y) of the detector in degrees
config.detectorList[4].pitchDeg = 0.0

# ID of detector slot
config.detectorList[4].id = 5

config.detectorList[5] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[5].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[5].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[5].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[5].bbox_x0 = 0

# Name of detector slot
config.detectorList[5].name = 'S27'

# Pixel size in the x dimension in mm
config.detectorList[5].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[5].transformDict.nativeSys = 'Pixels'

config.detectorList[5].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[5].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[5].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_x = -151.904

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_y = 31.901

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[5].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[5].yawDeg = -0.025

# roll (rotation about x) of the detector in degrees
config.detectorList[5].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[5].serial = '6'

# pitch (rotation about y) of the detector in degrees
config.detectorList[5].pitchDeg = 0.0

# ID of detector slot
config.detectorList[5].id = 6

config.detectorList[6] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[6].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[6].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[6].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[6].bbox_x0 = 0

# Name of detector slot
config.detectorList[6].name = 'S28'

# Pixel size in the x dimension in mm
config.detectorList[6].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[6].transformDict.nativeSys = 'Pixels'

config.detectorList[6].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[6].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[6].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_x = -151.85199999999998

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_y = 95.595

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[6].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[6].yawDeg = 0.004

# roll (rotation about x) of the detector in degrees
config.detectorList[6].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[6].serial = '7'

# pitch (rotation about y) of the detector in degrees
config.detectorList[6].pitchDeg = 0.0

# ID of detector slot
config.detectorList[6].id = 7

config.detectorList[7] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[7].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[7].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[7].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[7].bbox_x0 = 0

# Name of detector slot
config.detectorList[7].name = 'S20'

# Pixel size in the x dimension in mm
config.detectorList[7].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[7].transformDict.nativeSys = 'Pixels'

config.detectorList[7].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[7].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[7].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_x = -118.018

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_y = -127.452

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[7].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[7].yawDeg = 0.03

# roll (rotation about x) of the detector in degrees
config.detectorList[7].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[7].serial = '8'

# pitch (rotation about y) of the detector in degrees
config.detectorList[7].pitchDeg = 0.0

# ID of detector slot
config.detectorList[7].id = 8

config.detectorList[8] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[8].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[8].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[8].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[8].bbox_x0 = 0

# Name of detector slot
config.detectorList[8].name = 'S21'

# Pixel size in the x dimension in mm
config.detectorList[8].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[8].transformDict.nativeSys = 'Pixels'

config.detectorList[8].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[8].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[8].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[8].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[8].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[8].offset_x = -118.166

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[8].offset_y = -63.738

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[8].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[8].yawDeg = -0.02

# roll (rotation about x) of the detector in degrees
config.detectorList[8].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[8].serial = '9'

# pitch (rotation about y) of the detector in degrees
config.detectorList[8].pitchDeg = 0.0

# ID of detector slot
config.detectorList[8].id = 9

config.detectorList[9] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[9].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[9].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[9].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[9].bbox_x0 = 0

# Name of detector slot
config.detectorList[9].name = 'S22'

# Pixel size in the x dimension in mm
config.detectorList[9].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[9].transformDict.nativeSys = 'Pixels'

config.detectorList[9].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[9].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[9].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[9].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[9].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[9].offset_x = -118.134

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[9].offset_y = 0.002000000000000668

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[9].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[9].yawDeg = 0.006

# roll (rotation about x) of the detector in degrees
config.detectorList[9].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[9].serial = '10'

# pitch (rotation about y) of the detector in degrees
config.detectorList[9].pitchDeg = 0.0

# ID of detector slot
config.detectorList[9].id = 10

config.detectorList[10] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[10].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[10].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[10].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[10].bbox_x0 = 0

# Name of detector slot
config.detectorList[10].name = 'S23'

# Pixel size in the x dimension in mm
config.detectorList[10].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[10].transformDict.nativeSys = 'Pixels'

config.detectorList[10].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[10].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[10].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[10].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[10].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[10].offset_x = -118.17399999999999

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[10].offset_y = 63.738

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[10].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[10].yawDeg = -0.03

# roll (rotation about x) of the detector in degrees
config.detectorList[10].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[10].serial = '11'

# pitch (rotation about y) of the detector in degrees
config.detectorList[10].pitchDeg = 0.0

# ID of detector slot
config.detectorList[10].id = 11

config.detectorList[11] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[11].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[11].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[11].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[11].bbox_x0 = 0

# Name of detector slot
config.detectorList[11].name = 'S24'

# Pixel size in the x dimension in mm
config.detectorList[11].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[11].transformDict.nativeSys = 'Pixels'

config.detectorList[11].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[11].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[11].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[11].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[11].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[11].offset_x = -118.086

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[11].offset_y = 127.48599999999999

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[11].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[11].yawDeg = -0.027

# roll (rotation about x) of the detector in degrees
config.detectorList[11].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[11].serial = '12'

# pitch (rotation about y) of the detector in degrees
config.detectorList[11].pitchDeg = 0.0

# ID of detector slot
config.detectorList[11].id = 12

config.detectorList[12] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[12].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[12].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[12].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[12].bbox_x0 = 0

# Name of detector slot
config.detectorList[12].name = 'S14'

# Pixel size in the x dimension in mm
config.detectorList[12].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[12].transformDict.nativeSys = 'Pixels'

config.detectorList[12].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[12].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[12].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[12].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[12].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[12].offset_x = -84.268

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[12].offset_y = -159.323

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[12].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[12].yawDeg = -0.004

# roll (rotation about x) of the detector in degrees
config.detectorList[12].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[12].serial = '13'

# pitch (rotation about y) of the detector in degrees
config.detectorList[12].pitchDeg = 0.0

# ID of detector slot
config.detectorList[12].id = 13

config.detectorList[13] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[13].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[13].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[13].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[13].bbox_x0 = 0

# Name of detector slot
config.detectorList[13].name = 'S15'

# Pixel size in the x dimension in mm
config.detectorList[13].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[13].transformDict.nativeSys = 'Pixels'

config.detectorList[13].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[13].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[13].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[13].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[13].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[13].offset_x = -84.38

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[13].offset_y = -95.689

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[13].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[13].yawDeg = 0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[13].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[13].serial = '14'

# pitch (rotation about y) of the detector in degrees
config.detectorList[13].pitchDeg = 0.0

# ID of detector slot
config.detectorList[13].id = 14

config.detectorList[14] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[14].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[14].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[14].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[14].bbox_x0 = 0

# Name of detector slot
config.detectorList[14].name = 'S16'

# Pixel size in the x dimension in mm
config.detectorList[14].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[14].transformDict.nativeSys = 'Pixels'

config.detectorList[14].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[14].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[14].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[14].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[14].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[14].offset_x = -84.466

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[14].offset_y = -31.907

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[14].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[14].yawDeg = 0.011

# roll (rotation about x) of the detector in degrees
config.detectorList[14].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[14].serial = '15'

# pitch (rotation about y) of the detector in degrees
config.detectorList[14].pitchDeg = 0.0

# ID of detector slot
config.detectorList[14].id = 15

config.detectorList[15] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[15].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[15].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[15].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[15].bbox_x0 = 0

# Name of detector slot
config.detectorList[15].name = 'S17'

# Pixel size in the x dimension in mm
config.detectorList[15].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[15].transformDict.nativeSys = 'Pixels'

config.detectorList[15].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[15].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[15].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[15].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[15].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[15].offset_x = -84.384

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[15].offset_y = 31.891

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[15].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[15].yawDeg = 0.008

# roll (rotation about x) of the detector in degrees
config.detectorList[15].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[15].serial = '16'

# pitch (rotation about y) of the detector in degrees
config.detectorList[15].pitchDeg = 0.0

# ID of detector slot
config.detectorList[15].id = 16

config.detectorList[16] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[16].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[16].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[16].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[16].bbox_x0 = 0

# Name of detector slot
config.detectorList[16].name = 'S18'

# Pixel size in the x dimension in mm
config.detectorList[16].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[16].transformDict.nativeSys = 'Pixels'

config.detectorList[16].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[16].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[16].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[16].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[16].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[16].offset_x = -84.46

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[16].offset_y = 95.663

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[16].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[16].yawDeg = -0.04

# roll (rotation about x) of the detector in degrees
config.detectorList[16].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[16].serial = '17'

# pitch (rotation about y) of the detector in degrees
config.detectorList[16].pitchDeg = 0.0

# ID of detector slot
config.detectorList[16].id = 17

config.detectorList[17] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[17].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[17].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[17].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[17].bbox_x0 = 0

# Name of detector slot
config.detectorList[17].name = 'S19'

# Pixel size in the x dimension in mm
config.detectorList[17].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[17].transformDict.nativeSys = 'Pixels'

config.detectorList[17].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[17].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[17].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[17].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[17].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[17].offset_x = -84.316

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[17].offset_y = 159.413

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[17].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[17].yawDeg = 0.019

# roll (rotation about x) of the detector in degrees
config.detectorList[17].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[17].serial = '18'

# pitch (rotation about y) of the detector in degrees
config.detectorList[17].pitchDeg = 0.0

# ID of detector slot
config.detectorList[17].id = 18

config.detectorList[18] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[18].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[18].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[18].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[18].bbox_x0 = 0

# Name of detector slot
config.detectorList[18].name = 'S8'

# Pixel size in the x dimension in mm
config.detectorList[18].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[18].transformDict.nativeSys = 'Pixels'

config.detectorList[18].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[18].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[18].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[18].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[18].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[18].offset_x = -50.620000000000005

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[18].offset_y = -159.277

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[18].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[18].yawDeg = 0.016

# roll (rotation about x) of the detector in degrees
config.detectorList[18].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[18].serial = '19'

# pitch (rotation about y) of the detector in degrees
config.detectorList[18].pitchDeg = 0.0

# ID of detector slot
config.detectorList[18].id = 19

config.detectorList[19] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[19].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[19].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[19].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[19].bbox_x0 = 0

# Name of detector slot
config.detectorList[19].name = 'S9'

# Pixel size in the x dimension in mm
config.detectorList[19].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[19].transformDict.nativeSys = 'Pixels'

config.detectorList[19].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[19].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[19].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[19].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[19].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[19].offset_x = -50.596000000000004

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[19].offset_y = -95.689

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[19].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[19].yawDeg = -0.001

# roll (rotation about x) of the detector in degrees
config.detectorList[19].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[19].serial = '20'

# pitch (rotation about y) of the detector in degrees
config.detectorList[19].pitchDeg = 0.0

# ID of detector slot
config.detectorList[19].id = 20

config.detectorList[20] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[20].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[20].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[20].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[20].bbox_x0 = 0

# Name of detector slot
config.detectorList[20].name = 'S10'

# Pixel size in the x dimension in mm
config.detectorList[20].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[20].transformDict.nativeSys = 'Pixels'

config.detectorList[20].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[20].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[20].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[20].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[20].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[20].offset_x = -50.7

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[20].offset_y = -31.931

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[20].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[20].yawDeg = 0.007

# roll (rotation about x) of the detector in degrees
config.detectorList[20].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[20].serial = '21'

# pitch (rotation about y) of the detector in degrees
config.detectorList[20].pitchDeg = 0.0

# ID of detector slot
config.detectorList[20].id = 21

config.detectorList[21] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[21].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[21].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[21].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[21].bbox_x0 = 0

# Name of detector slot
config.detectorList[21].name = 'S11'

# Pixel size in the x dimension in mm
config.detectorList[21].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[21].transformDict.nativeSys = 'Pixels'

config.detectorList[21].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[21].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[21].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[21].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[21].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[21].offset_x = -50.757999999999996

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[21].offset_y = 31.915

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[21].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[21].yawDeg = -0.022

# roll (rotation about x) of the detector in degrees
config.detectorList[21].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[21].serial = '22'

# pitch (rotation about y) of the detector in degrees
config.detectorList[21].pitchDeg = 0.0

# ID of detector slot
config.detectorList[21].id = 22

config.detectorList[22] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[22].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[22].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[22].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[22].bbox_x0 = 0

# Name of detector slot
config.detectorList[22].name = 'S12'

# Pixel size in the x dimension in mm
config.detectorList[22].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[22].transformDict.nativeSys = 'Pixels'

config.detectorList[22].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[22].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[22].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[22].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[22].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[22].offset_x = -50.69800000000001

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[22].offset_y = 95.761

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[22].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[22].yawDeg = -0.022

# roll (rotation about x) of the detector in degrees
config.detectorList[22].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[22].serial = '23'

# pitch (rotation about y) of the detector in degrees
config.detectorList[22].pitchDeg = 0.0

# ID of detector slot
config.detectorList[22].id = 23

config.detectorList[23] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[23].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[23].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[23].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[23].bbox_x0 = 0

# Name of detector slot
config.detectorList[23].name = 'S13'

# Pixel size in the x dimension in mm
config.detectorList[23].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[23].transformDict.nativeSys = 'Pixels'

config.detectorList[23].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[23].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[23].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[23].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[23].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[23].offset_x = -50.634

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[23].offset_y = 159.391

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[23].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[23].yawDeg = -0.016

# roll (rotation about x) of the detector in degrees
config.detectorList[23].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[23].serial = '24'

# pitch (rotation about y) of the detector in degrees
config.detectorList[23].pitchDeg = 0.0

# ID of detector slot
config.detectorList[23].id = 24

config.detectorList[24] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[24].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[24].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[24].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[24].bbox_x0 = 0

# Name of detector slot
config.detectorList[24].name = 'S1'

# Pixel size in the x dimension in mm
config.detectorList[24].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[24].transformDict.nativeSys = 'Pixels'

config.detectorList[24].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[24].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[24].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[24].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[24].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[24].offset_x = -16.798000000000002

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[24].offset_y = -191.216

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[24].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[24].yawDeg = 0.007

# roll (rotation about x) of the detector in degrees
config.detectorList[24].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[24].serial = '25'

# pitch (rotation about y) of the detector in degrees
config.detectorList[24].pitchDeg = 0.0

# ID of detector slot
config.detectorList[24].id = 25

config.detectorList[25] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[25].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[25].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[25].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[25].bbox_x0 = 0

# Name of detector slot
config.detectorList[25].name = 'S2'

# Pixel size in the x dimension in mm
config.detectorList[25].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[25].transformDict.nativeSys = 'Pixels'

config.detectorList[25].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[25].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[25].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[25].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[25].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[25].offset_x = -16.894

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[25].offset_y = -127.524

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[25].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[25].yawDeg = 0.003

# roll (rotation about x) of the detector in degrees
config.detectorList[25].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[25].serial = '26'

# pitch (rotation about y) of the detector in degrees
config.detectorList[25].pitchDeg = 0.0

# ID of detector slot
config.detectorList[25].id = 26

config.detectorList[26] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[26].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[26].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[26].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[26].bbox_x0 = 0

# Name of detector slot
config.detectorList[26].name = 'S3'

# Pixel size in the x dimension in mm
config.detectorList[26].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[26].transformDict.nativeSys = 'Pixels'

config.detectorList[26].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[26].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[26].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[26].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[26].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[26].offset_x = -16.85

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[26].offset_y = -63.792

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[26].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[26].yawDeg = -0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[26].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[26].serial = '27'

# pitch (rotation about y) of the detector in degrees
config.detectorList[26].pitchDeg = 0.0

# ID of detector slot
config.detectorList[26].id = 27

config.detectorList[27] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[27].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[27].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[27].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[27].bbox_x0 = 0

# Name of detector slot
config.detectorList[27].name = 'S4'

# Pixel size in the x dimension in mm
config.detectorList[27].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[27].transformDict.nativeSys = 'Pixels'

config.detectorList[27].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[27].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[27].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[27].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[27].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[27].offset_x = -16.892000000000003

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[27].offset_y = 0.09200000000000053

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[27].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[27].yawDeg = 0.019

# roll (rotation about x) of the detector in degrees
config.detectorList[27].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[27].serial = '28'

# pitch (rotation about y) of the detector in degrees
config.detectorList[27].pitchDeg = 0.0

# ID of detector slot
config.detectorList[27].id = 28

config.detectorList[28] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[28].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[28].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[28].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[28].bbox_x0 = 0

# Name of detector slot
config.detectorList[28].name = 'S5'

# Pixel size in the x dimension in mm
config.detectorList[28].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[28].transformDict.nativeSys = 'Pixels'

config.detectorList[28].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[28].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[28].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[28].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[28].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[28].offset_x = -16.836

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[28].offset_y = 63.824

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[28].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[28].yawDeg = 0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[28].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[28].serial = '29'

# pitch (rotation about y) of the detector in degrees
config.detectorList[28].pitchDeg = 0.0

# ID of detector slot
config.detectorList[28].id = 29

config.detectorList[29] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[29].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[29].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[29].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[29].bbox_x0 = 0

# Name of detector slot
config.detectorList[29].name = 'S6'

# Pixel size in the x dimension in mm
config.detectorList[29].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[29].transformDict.nativeSys = 'Pixels'

config.detectorList[29].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[29].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[29].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[29].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[29].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[29].offset_x = -16.85

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[29].offset_y = 127.636

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[29].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[29].yawDeg = 0.001

# roll (rotation about x) of the detector in degrees
config.detectorList[29].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[29].serial = '30'

# pitch (rotation about y) of the detector in degrees
config.detectorList[29].pitchDeg = 0.0

# ID of detector slot
config.detectorList[29].id = 30

config.detectorList[30] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[30].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[30].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[30].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[30].bbox_x0 = 0

# Name of detector slot
config.detectorList[30].name = 'S7'

# Pixel size in the x dimension in mm
config.detectorList[30].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[30].transformDict.nativeSys = 'Pixels'

config.detectorList[30].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[30].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[30].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[30].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[30].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[30].offset_x = -16.898

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[30].offset_y = 191.268

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[30].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[30].yawDeg = 0.023

# roll (rotation about x) of the detector in degrees
config.detectorList[30].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[30].serial = '31'

# pitch (rotation about y) of the detector in degrees
config.detectorList[30].pitchDeg = 0.0

# ID of detector slot
config.detectorList[30].id = 31

config.detectorList[31] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[31].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[31].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[31].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[31].bbox_x0 = 0

# Name of detector slot
config.detectorList[31].name = 'N1'

# Pixel size in the x dimension in mm
config.detectorList[31].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[31].transformDict.nativeSys = 'Pixels'

config.detectorList[31].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[31].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[31].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[31].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[31].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[31].offset_x = 16.894

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[31].offset_y = -191.252

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[31].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[31].yawDeg = -0.024

# roll (rotation about x) of the detector in degrees
config.detectorList[31].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[31].serial = '32'

# pitch (rotation about y) of the detector in degrees
config.detectorList[31].pitchDeg = 0.0

# ID of detector slot
config.detectorList[31].id = 32

config.detectorList[32] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[32].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[32].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[32].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[32].bbox_x0 = 0

# Name of detector slot
config.detectorList[32].name = 'N2'

# Pixel size in the x dimension in mm
config.detectorList[32].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[32].transformDict.nativeSys = 'Pixels'

config.detectorList[32].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[32].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[32].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[32].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[32].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[32].offset_x = 16.884

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[32].offset_y = -127.54599999999999

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[32].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[32].yawDeg = -0.012

# roll (rotation about x) of the detector in degrees
config.detectorList[32].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[32].serial = '33'

# pitch (rotation about y) of the detector in degrees
config.detectorList[32].pitchDeg = 0.0

# ID of detector slot
config.detectorList[32].id = 33

config.detectorList[33] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[33].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[33].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[33].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[33].bbox_x0 = 0

# Name of detector slot
config.detectorList[33].name = 'N3'

# Pixel size in the x dimension in mm
config.detectorList[33].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[33].transformDict.nativeSys = 'Pixels'

config.detectorList[33].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[33].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[33].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[33].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[33].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[33].offset_x = 16.921999999999997

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[33].offset_y = -63.836

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[33].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[33].yawDeg = 0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[33].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[33].serial = '34'

# pitch (rotation about y) of the detector in degrees
config.detectorList[33].pitchDeg = 0.0

# ID of detector slot
config.detectorList[33].id = 34

config.detectorList[34] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[34].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[34].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[34].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[34].bbox_x0 = 0

# Name of detector slot
config.detectorList[34].name = 'N4'

# Pixel size in the x dimension in mm
config.detectorList[34].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[34].transformDict.nativeSys = 'Pixels'

config.detectorList[34].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[34].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[34].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[34].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[34].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[34].offset_x = 16.908

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[34].offset_y = -0.017999999999998906

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[34].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[34].yawDeg = 0.003

# roll (rotation about x) of the detector in degrees
config.detectorList[34].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[34].serial = '35'

# pitch (rotation about y) of the detector in degrees
config.detectorList[34].pitchDeg = 0.0

# ID of detector slot
config.detectorList[34].id = 35

config.detectorList[35] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[35].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[35].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[35].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[35].bbox_x0 = 0

# Name of detector slot
config.detectorList[35].name = 'N5'

# Pixel size in the x dimension in mm
config.detectorList[35].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[35].transformDict.nativeSys = 'Pixels'

config.detectorList[35].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[35].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[35].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[35].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[35].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[35].offset_x = 16.978

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[35].offset_y = 63.708

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[35].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[35].yawDeg = 0.05

# roll (rotation about x) of the detector in degrees
config.detectorList[35].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[35].serial = '36'

# pitch (rotation about y) of the detector in degrees
config.detectorList[35].pitchDeg = 0.0

# ID of detector slot
config.detectorList[35].id = 36

config.detectorList[36] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[36].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[36].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[36].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[36].bbox_x0 = 0

# Name of detector slot
config.detectorList[36].name = 'N6'

# Pixel size in the x dimension in mm
config.detectorList[36].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[36].transformDict.nativeSys = 'Pixels'

config.detectorList[36].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[36].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[36].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[36].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[36].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[36].offset_x = 16.872

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[36].offset_y = 127.47999999999999

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[36].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[36].yawDeg = 0.008

# roll (rotation about x) of the detector in degrees
config.detectorList[36].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[36].serial = '37'

# pitch (rotation about y) of the detector in degrees
config.detectorList[36].pitchDeg = 0.0

# ID of detector slot
config.detectorList[36].id = 37

config.detectorList[37] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[37].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[37].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[37].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[37].bbox_x0 = 0

# Name of detector slot
config.detectorList[37].name = 'N7'

# Pixel size in the x dimension in mm
config.detectorList[37].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[37].transformDict.nativeSys = 'Pixels'

config.detectorList[37].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[37].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[37].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[37].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[37].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[37].offset_x = 16.878

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[37].offset_y = 191.23

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[37].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[37].yawDeg = -0.014

# roll (rotation about x) of the detector in degrees
config.detectorList[37].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[37].serial = '38'

# pitch (rotation about y) of the detector in degrees
config.detectorList[37].pitchDeg = 0.0

# ID of detector slot
config.detectorList[37].id = 38

config.detectorList[38] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[38].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[38].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[38].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[38].bbox_x0 = 0

# Name of detector slot
config.detectorList[38].name = 'N8'

# Pixel size in the x dimension in mm
config.detectorList[38].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[38].transformDict.nativeSys = 'Pixels'

config.detectorList[38].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[38].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[38].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[38].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[38].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[38].offset_x = 50.662000000000006

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[38].offset_y = -159.379

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[38].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[38].yawDeg = 0.011

# roll (rotation about x) of the detector in degrees
config.detectorList[38].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[38].serial = '39'

# pitch (rotation about y) of the detector in degrees
config.detectorList[38].pitchDeg = 0.0

# ID of detector slot
config.detectorList[38].id = 39

config.detectorList[39] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[39].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[39].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[39].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[39].bbox_x0 = 0

# Name of detector slot
config.detectorList[39].name = 'N9'

# Pixel size in the x dimension in mm
config.detectorList[39].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[39].transformDict.nativeSys = 'Pixels'

config.detectorList[39].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[39].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[39].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[39].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[39].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[39].offset_x = 50.682

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[39].offset_y = -95.727

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[39].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[39].yawDeg = 0.007

# roll (rotation about x) of the detector in degrees
config.detectorList[39].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[39].serial = '40'

# pitch (rotation about y) of the detector in degrees
config.detectorList[39].pitchDeg = 0.0

# ID of detector slot
config.detectorList[39].id = 40

config.detectorList[40] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[40].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[40].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[40].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[40].bbox_x0 = 0

# Name of detector slot
config.detectorList[40].name = 'N10'

# Pixel size in the x dimension in mm
config.detectorList[40].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[40].transformDict.nativeSys = 'Pixels'

config.detectorList[40].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[40].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[40].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[40].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[40].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[40].offset_x = 50.664

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[40].offset_y = -31.911

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[40].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[40].yawDeg = 0.016

# roll (rotation about x) of the detector in degrees
config.detectorList[40].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[40].serial = '41'

# pitch (rotation about y) of the detector in degrees
config.detectorList[40].pitchDeg = 0.0

# ID of detector slot
config.detectorList[40].id = 41

config.detectorList[41] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[41].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[41].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[41].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[41].bbox_x0 = 0

# Name of detector slot
config.detectorList[41].name = 'N11'

# Pixel size in the x dimension in mm
config.detectorList[41].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[41].transformDict.nativeSys = 'Pixels'

config.detectorList[41].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[41].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[41].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[41].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[41].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[41].offset_x = 50.714

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[41].offset_y = 31.933

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[41].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[41].yawDeg = 0.015

# roll (rotation about x) of the detector in degrees
config.detectorList[41].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[41].serial = '42'

# pitch (rotation about y) of the detector in degrees
config.detectorList[41].pitchDeg = 0.0

# ID of detector slot
config.detectorList[41].id = 42

config.detectorList[42] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[42].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[42].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[42].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[42].bbox_x0 = 0

# Name of detector slot
config.detectorList[42].name = 'N12'

# Pixel size in the x dimension in mm
config.detectorList[42].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[42].transformDict.nativeSys = 'Pixels'

config.detectorList[42].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[42].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[42].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[42].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[42].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[42].offset_x = 50.678

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[42].offset_y = 95.689

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[42].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[42].yawDeg = 0.017

# roll (rotation about x) of the detector in degrees
config.detectorList[42].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[42].serial = '43'

# pitch (rotation about y) of the detector in degrees
config.detectorList[42].pitchDeg = 0.0

# ID of detector slot
config.detectorList[42].id = 43

config.detectorList[43] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[43].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[43].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[43].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[43].bbox_x0 = 0

# Name of detector slot
config.detectorList[43].name = 'N13'

# Pixel size in the x dimension in mm
config.detectorList[43].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[43].transformDict.nativeSys = 'Pixels'

config.detectorList[43].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[43].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[43].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[43].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[43].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[43].offset_x = 50.646

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[43].offset_y = 159.333

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[43].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[43].yawDeg = 0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[43].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[43].serial = '44'

# pitch (rotation about y) of the detector in degrees
config.detectorList[43].pitchDeg = 0.0

# ID of detector slot
config.detectorList[43].id = 44

config.detectorList[44] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[44].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[44].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[44].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[44].bbox_x0 = 0

# Name of detector slot
config.detectorList[44].name = 'N14'

# Pixel size in the x dimension in mm
config.detectorList[44].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[44].transformDict.nativeSys = 'Pixels'

config.detectorList[44].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[44].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[44].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[44].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[44].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[44].offset_x = 84.352

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[44].offset_y = -159.393

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[44].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[44].yawDeg = 0.026

# roll (rotation about x) of the detector in degrees
config.detectorList[44].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[44].serial = '45'

# pitch (rotation about y) of the detector in degrees
config.detectorList[44].pitchDeg = 0.0

# ID of detector slot
config.detectorList[44].id = 45

config.detectorList[45] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[45].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[45].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[45].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[45].bbox_x0 = 0

# Name of detector slot
config.detectorList[45].name = 'N15'

# Pixel size in the x dimension in mm
config.detectorList[45].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[45].transformDict.nativeSys = 'Pixels'

config.detectorList[45].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[45].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[45].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[45].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[45].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[45].offset_x = 84.384

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[45].offset_y = -95.787

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[45].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[45].yawDeg = 0.005

# roll (rotation about x) of the detector in degrees
config.detectorList[45].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[45].serial = '46'

# pitch (rotation about y) of the detector in degrees
config.detectorList[45].pitchDeg = 0.0

# ID of detector slot
config.detectorList[45].id = 46

config.detectorList[46] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[46].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[46].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[46].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[46].bbox_x0 = 0

# Name of detector slot
config.detectorList[46].name = 'N16'

# Pixel size in the x dimension in mm
config.detectorList[46].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[46].transformDict.nativeSys = 'Pixels'

config.detectorList[46].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[46].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[46].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[46].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[46].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[46].offset_x = 84.412

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[46].offset_y = -31.899

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[46].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[46].yawDeg = -0.025

# roll (rotation about x) of the detector in degrees
config.detectorList[46].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[46].serial = '47'

# pitch (rotation about y) of the detector in degrees
config.detectorList[46].pitchDeg = 0.0

# ID of detector slot
config.detectorList[46].id = 47

config.detectorList[47] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[47].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[47].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[47].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[47].bbox_x0 = 0

# Name of detector slot
config.detectorList[47].name = 'N17'

# Pixel size in the x dimension in mm
config.detectorList[47].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[47].transformDict.nativeSys = 'Pixels'

config.detectorList[47].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[47].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[47].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[47].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[47].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[47].offset_x = 84.482

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[47].offset_y = 31.787

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[47].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[47].yawDeg = 0.032

# roll (rotation about x) of the detector in degrees
config.detectorList[47].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[47].serial = '48'

# pitch (rotation about y) of the detector in degrees
config.detectorList[47].pitchDeg = 0.0

# ID of detector slot
config.detectorList[47].id = 48

config.detectorList[48] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[48].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[48].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[48].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[48].bbox_x0 = 0

# Name of detector slot
config.detectorList[48].name = 'N18'

# Pixel size in the x dimension in mm
config.detectorList[48].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[48].transformDict.nativeSys = 'Pixels'

config.detectorList[48].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[48].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[48].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[48].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[48].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[48].offset_x = 84.388

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[48].offset_y = 95.663

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[48].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[48].yawDeg = 0.012

# roll (rotation about x) of the detector in degrees
config.detectorList[48].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[48].serial = '49'

# pitch (rotation about y) of the detector in degrees
config.detectorList[48].pitchDeg = 0.0

# ID of detector slot
config.detectorList[48].id = 49

config.detectorList[49] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[49].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[49].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[49].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[49].bbox_x0 = 0

# Name of detector slot
config.detectorList[49].name = 'N19'

# Pixel size in the x dimension in mm
config.detectorList[49].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[49].transformDict.nativeSys = 'Pixels'

config.detectorList[49].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[49].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[49].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[49].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[49].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[49].offset_x = 84.30799999999999

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[49].offset_y = 159.357

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[49].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[49].yawDeg = 0.006

# roll (rotation about x) of the detector in degrees
config.detectorList[49].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[49].serial = '50'

# pitch (rotation about y) of the detector in degrees
config.detectorList[49].pitchDeg = 0.0

# ID of detector slot
config.detectorList[49].id = 50

config.detectorList[50] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[50].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[50].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[50].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[50].bbox_x0 = 0

# Name of detector slot
config.detectorList[50].name = 'N20'

# Pixel size in the x dimension in mm
config.detectorList[50].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[50].transformDict.nativeSys = 'Pixels'

config.detectorList[50].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[50].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[50].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[50].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[50].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[50].offset_x = 118.086

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[50].offset_y = -127.458

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[50].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[50].yawDeg = -0.018

# roll (rotation about x) of the detector in degrees
config.detectorList[50].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[50].serial = '51'

# pitch (rotation about y) of the detector in degrees
config.detectorList[50].pitchDeg = 0.0

# ID of detector slot
config.detectorList[50].id = 51

config.detectorList[51] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[51].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[51].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[51].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[51].bbox_x0 = 0

# Name of detector slot
config.detectorList[51].name = 'N21'

# Pixel size in the x dimension in mm
config.detectorList[51].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[51].transformDict.nativeSys = 'Pixels'

config.detectorList[51].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[51].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[51].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[51].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[51].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[51].offset_x = 118.086

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[51].offset_y = -63.762

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[51].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[51].yawDeg = -0.007

# roll (rotation about x) of the detector in degrees
config.detectorList[51].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[51].serial = '52'

# pitch (rotation about y) of the detector in degrees
config.detectorList[51].pitchDeg = 0.0

# ID of detector slot
config.detectorList[51].id = 52

config.detectorList[52] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[52].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[52].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[52].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[52].bbox_x0 = 0

# Name of detector slot
config.detectorList[52].name = 'N22'

# Pixel size in the x dimension in mm
config.detectorList[52].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[52].transformDict.nativeSys = 'Pixels'

config.detectorList[52].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[52].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[52].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[52].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[52].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[52].offset_x = 118.09

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[52].offset_y = 0.049999999999998934

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[52].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[52].yawDeg = -0.008

# roll (rotation about x) of the detector in degrees
config.detectorList[52].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[52].serial = '53'

# pitch (rotation about y) of the detector in degrees
config.detectorList[52].pitchDeg = 0.0

# ID of detector slot
config.detectorList[52].id = 53

config.detectorList[53] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[53].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[53].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[53].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[53].bbox_x0 = 0

# Name of detector slot
config.detectorList[53].name = 'N23'

# Pixel size in the x dimension in mm
config.detectorList[53].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[53].transformDict.nativeSys = 'Pixels'

config.detectorList[53].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[53].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[53].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[53].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[53].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[53].offset_x = 118.166

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[53].offset_y = 63.754000000000005

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[53].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[53].yawDeg = 0.006

# roll (rotation about x) of the detector in degrees
config.detectorList[53].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[53].serial = '54'

# pitch (rotation about y) of the detector in degrees
config.detectorList[53].pitchDeg = 0.0

# ID of detector slot
config.detectorList[53].id = 54

config.detectorList[54] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[54].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[54].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[54].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[54].bbox_x0 = 0

# Name of detector slot
config.detectorList[54].name = 'N24'

# Pixel size in the x dimension in mm
config.detectorList[54].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[54].transformDict.nativeSys = 'Pixels'

config.detectorList[54].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[54].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[54].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[54].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[54].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[54].offset_x = 118.074

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[54].offset_y = 127.464

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[54].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[54].yawDeg = 0.01

# roll (rotation about x) of the detector in degrees
config.detectorList[54].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[54].serial = '55'

# pitch (rotation about y) of the detector in degrees
config.detectorList[54].pitchDeg = 0.0

# ID of detector slot
config.detectorList[54].id = 55

config.detectorList[55] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[55].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[55].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[55].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[55].bbox_x0 = 0

# Name of detector slot
config.detectorList[55].name = 'N25'

# Pixel size in the x dimension in mm
config.detectorList[55].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[55].transformDict.nativeSys = 'Pixels'

config.detectorList[55].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[55].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[55].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[55].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[55].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[55].offset_x = 151.808

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[55].offset_y = -95.587

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[55].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[55].yawDeg = -0.008

# roll (rotation about x) of the detector in degrees
config.detectorList[55].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[55].serial = '56'

# pitch (rotation about y) of the detector in degrees
config.detectorList[55].pitchDeg = 0.0

# ID of detector slot
config.detectorList[55].id = 56

config.detectorList[56] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[56].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[56].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[56].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[56].bbox_x0 = 0

# Name of detector slot
config.detectorList[56].name = 'N26'

# Pixel size in the x dimension in mm
config.detectorList[56].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[56].transformDict.nativeSys = 'Pixels'

config.detectorList[56].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[56].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[56].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[56].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[56].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[56].offset_x = 151.8

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[56].offset_y = -31.935000000000002

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[56].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[56].yawDeg = 0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[56].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[56].serial = '57'

# pitch (rotation about y) of the detector in degrees
config.detectorList[56].pitchDeg = 0.0

# ID of detector slot
config.detectorList[56].id = 57

config.detectorList[57] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[57].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[57].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[57].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[57].bbox_x0 = 0

# Name of detector slot
config.detectorList[57].name = 'N27'

# Pixel size in the x dimension in mm
config.detectorList[57].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[57].transformDict.nativeSys = 'Pixels'

config.detectorList[57].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[57].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[57].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[57].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[57].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[57].offset_x = 151.86

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[57].offset_y = 31.847

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[57].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[57].yawDeg = 0.039

# roll (rotation about x) of the detector in degrees
config.detectorList[57].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[57].serial = '58'

# pitch (rotation about y) of the detector in degrees
config.detectorList[57].pitchDeg = 0.0

# ID of detector slot
config.detectorList[57].id = 58

config.detectorList[58] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[58].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[58].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[58].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[58].bbox_x0 = 0

# Name of detector slot
config.detectorList[58].name = 'N28'

# Pixel size in the x dimension in mm
config.detectorList[58].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[58].transformDict.nativeSys = 'Pixels'

config.detectorList[58].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[58].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[58].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[58].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[58].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[58].offset_x = 151.79399999999998

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[58].offset_y = 95.557

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[58].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[58].yawDeg = 0.021

# roll (rotation about x) of the detector in degrees
config.detectorList[58].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[58].serial = '59'

# pitch (rotation about y) of the detector in degrees
config.detectorList[58].pitchDeg = 0.0

# ID of detector slot
config.detectorList[58].id = 59

config.detectorList[59] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[59].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[59].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[59].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[59].bbox_x0 = 0

# Name of detector slot
config.detectorList[59].name = 'N29'

# Pixel size in the x dimension in mm
config.detectorList[59].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[59].transformDict.nativeSys = 'Pixels'

config.detectorList[59].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[59].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[59].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[59].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[59].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[59].offset_x = 185.558

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[59].offset_y = -63.732

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[59].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[59].yawDeg = -0.012

# roll (rotation about x) of the detector in degrees
config.detectorList[59].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[59].serial = '60'

# pitch (rotation about y) of the detector in degrees
config.detectorList[59].pitchDeg = 0.0

# ID of detector slot
config.detectorList[59].id = 60

config.detectorList[60] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[60].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[60].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[60].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[60].bbox_x0 = 0

# Name of detector slot
config.detectorList[60].name = 'N30'

# Pixel size in the x dimension in mm
config.detectorList[60].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[60].transformDict.nativeSys = 'Pixels'

config.detectorList[60].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[60].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[60].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[60].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[60].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[60].offset_x = 185.50400000000002

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[60].offset_y = 0.016000000000000014

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[60].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[60].yawDeg = 0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[60].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[60].serial = '61'

# pitch (rotation about y) of the detector in degrees
config.detectorList[60].pitchDeg = 0.0

# ID of detector slot
config.detectorList[60].id = 61

config.detectorList[61] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[61].bbox_y0 = 0

# y1 of pixel bounding box
config.detectorList[61].bbox_y1 = 4095

# x1 of pixel bounding box
config.detectorList[61].bbox_x1 = 2047

# x0 of pixel bounding box
config.detectorList[61].bbox_x0 = 0

# Name of detector slot
config.detectorList[61].name = 'N31'

# Pixel size in the x dimension in mm
config.detectorList[61].pixelSize_x = 0.015

# Name of native coordinate system
config.detectorList[61].transformDict.nativeSys = 'Pixels'

config.detectorList[61].transformDict.transforms = None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[61].refpos_x = 1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[61].refpos_y = 2047.5

# Pixel size in the y dimension in mm
config.detectorList[61].pixelSize_y = 0.015

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[61].detectorType = 0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[61].offset_x = 185.55

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[61].offset_y = 63.794

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[61].transposeDetector = False

# yaw (rotation about z) of the detector in degrees. This includes any
# necessary rotation to go from detector coordinates to camera coordinates
# after optional transposition.
config.detectorList[61].yawDeg = -0.026

# roll (rotation about x) of the detector in degrees
config.detectorList[61].rollDeg = 0.0

# Serial string associated with this specific detector
config.detectorList[61].serial = '62'

# pitch (rotation about y) of the detector in degrees
config.detectorList[61].pitchDeg = 0.0

# ID of detector slot
config.detectorList[61].id = 62

# Coefficients for radial distortion
config.radialCoeffs = None

# Name of this camera
config.name = 'DECAM'
