# This code is released under the Creative Commons zero license.  Go wild, but
# it would be nice to preserve the credit if you find it helpful.
#
# Tom Sgouros
# Center for Computation and Visualization
# Brown University
# March 2018.
#
# This module is a ParaViewWeb server application.
#    Use it like this:
#     $ pvpython PVWSDServer.py -i localhost -p 1234
#
# There should be a README to explain how to start the client.

# import to process args
import os
import sys

# import paraview modules.
from paraview.web import pv_wslink
from paraview.web import protocols as pv_protocols

import PVWSDProtocols

# import RPC annotation
from wslink import register as exportRPC
import vtk
from paraview import simple
from paraview.simple import * # introduce clone
from wslink import server

import json
import argparse

# import jsonparse modules.
import jsonparse

# cout time
import time

# =============================================================================
# Create custom Pipeline Manager class to handle clients requests
# =============================================================================

class PVWSDServer(pv_wslink.PVServerProtocol):

    authKey = "wslink-secret"
    viewportScale=1.0
    viewportMaxWidth=2560
    viewportMaxHeight=1440

    @staticmethod
    def add_arguments(parser):
        # Not using this argument, but it's here to show how to do it.
        parser.add_argument("--data", default=os.getcwd(),
                            help="path to data directory to list", dest="data")

    @staticmethod
    def configure(args):
        # Same here. Not really using this, but this is how it should look.
        PVWSDServer.authKey   = args.authKey
        PVWSDServer.data      = args.data


    def initialize(self):
        # Register the built-in protocols: MouseHandler, ViewPort and
        # ViewPortImageDelivery.  (You can see these over on the client
        # in the createClient call)
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort(PVWSDServer.viewportScale, PVWSDServer.viewportMaxWidth, PVWSDServer.viewportMaxHeight))
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPortImageDelivery())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebPublishImageDelivery(decode=False))

        # Instantiate an object with the custom protocols...
        PVWSDTest = PVWSDProtocols.PVWSDTest()

        #                                      ... and register them, too.
        self.registerVtkWebProtocol(PVWSDTest)

        # Update authentication key to use
        self.updateSecret(PVWSDServer.authKey)
        self.getApplication().SetImageEncoding(0)
        # Disable interactor-based render calls
        simple.GetRenderView().EnableRenderOnInteraction = 0
        simple.GetRenderView().Background = [0,0,0]
        simple.GetRenderView().Background2 = [0,0,0]
        #######################################################
        # # 准备绘制对象 ########################################
        #######################################################
        testmode = 2
        # mode0 中等规模模型，car model PBR
        # mode1 大规模模型，齿轮矩阵
        # mode2 小规模多零件模型
        # explanation for testmode:
        if testmode == 0:
            # 性能测试：读取obj模型

            #车模型，材质，半透明
            reader01 = simple.OpenDataFile(
                r'D:\CarModel\CarBase.obj')
            reader02 = simple.OpenDataFile(
                r'D:\CarModel\CarBody.obj')
            reader03 = simple.OpenDataFile(
                r'D:\CarModel\CarBrick.obj')
            reader04 = simple.OpenDataFile(
                r'D:\CarModel\CarFace.obj')
            reader05 = simple.OpenDataFile(
                r'D:\CarModel\CarGlass.obj')
            reader06 = simple.OpenDataFile(
                r'D:\CarModel\CarGlassRim.obj')
            reader07 = simple.OpenDataFile(
                r'D:\CarModel\CarHandles.obj')
            reader08 = simple.OpenDataFile(
                r'D:\CarModel\CarInside.obj')
            reader09 = simple.OpenDataFile(
                r'D:\CarModel\CarLight.obj')
            reader10 = simple.OpenDataFile(
                r'D:\CarModel\CarLogo.obj')

            reader11 = simple.OpenDataFile(
                r'D:\CarModel\CarMirrorShell.obj')
            reader12 = simple.OpenDataFile(
                r'D:\CarModel\CarPipe.obj')
            reader13 = simple.OpenDataFile(
                r'D:\CarModel\CarPlate.obj')
            reader14 = simple.OpenDataFile(
                r'D:\CarModel\CarRim.obj')
            reader15 = simple.OpenDataFile(
                r'D:\CarModel\CarScrews.obj')
            reader16 = simple.OpenDataFile(
                r'D:\CarModel\CarSeats.obj')
            reader17 = simple.OpenDataFile(
                r'D:\CarModel\CarTop.obj')
            reader18 = simple.OpenDataFile(
                r'D:\CarModel\CarTyre.obj')
            reader19 = simple.OpenDataFile(
                r'D:\CarModel\CarWiper.obj')

            time_test01 = time.time()
            display = simple.Show(reader01)
            display1 = simple.Show(reader02)
            display2 = simple.Show(reader03)
            display3 = simple.Show(reader04)
            display4 = simple.Show(reader05)
            display5 = simple.Show(reader06)
            display6 = simple.Show(reader07)
            display7 = simple.Show(reader08)
            display8 = simple.Show(reader09)
            display9 = simple.Show(reader10)

            display10 = simple.Show(reader11)
            display11 = simple.Show(reader12)
            display12 = simple.Show(reader13)
            display13 = simple.Show(reader14)
            display14 = simple.Show(reader15)
            display15 = simple.Show(reader16)
            display16 = simple.Show(reader17)
            display17 = simple.Show(reader18)
            display18 = simple.Show(reader19)

            display.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]

            display1.AmbientColor = [0.9549019607843137, 0.0254901960784314, 0.0333333333333333]
            display1.DiffuseColor = [0.9549019607843137, 0.0254901960784314, 0.0333333333333333]
            display1.Interpolation = 'PBR'
            display1.Roughness = 0.2
            display1.Metallic = 0.4

            display2.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display2.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]

            display3.AmbientColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]
            display3.DiffuseColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]
            display3.Interpolation = 'PBR'
            display3.Roughness = 0.2
            display3.Metallic = 0.4

            display4.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display4.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display4.Interpolation = 'PBR'
            display4.Roughness = 0.2
            display4.Metallic = 0.02
            display4.Opacity = 0.5

            display5.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display5.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]


            display6.AmbientColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]
            display6.DiffuseColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]

            display7.AmbientColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]
            display7.DiffuseColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]
            display7.Interpolation = 'PBR'
            display7.Roughness = 0.2
            display7.Metallic = 0.4

            display8.AmbientColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]
            display8.DiffuseColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]

            display9.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display9.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display9.Interpolation = 'PBR'
            display9.Roughness = 0.2
            display9.Metallic = 0.4

            display10.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display10.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display11.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display11.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display12.AmbientColor = [0.4249019607843137, 0.7074901960784314, 0.9333333333333333]
            display12.DiffuseColor = [0.4249019607843137, 0.7074901960784314, 0.9333333333333333]
            display12.Interpolation = 'PBR'
            display12.Roughness = 0.3
            display12.Metallic = 0.4

            display13.AmbientColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]
            display13.DiffuseColor = [0.7549019607843137, 0.7554901960784314, 0.7533333333333333]
            display13.Interpolation = 'PBR'
            display13.Roughness = 0.3
            display13.Metallic = 0.4

            display14.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display14.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display15.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display15.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display15.Interpolation = 'PBR'
            display15.Roughness = 0.35
            display15.Metallic = 0.05

            display16.AmbientColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]
            display16.DiffuseColor = [0.8549019607843137, 0.0254901960784314, 0.0333333333333333]
            display16.Interpolation = 'PBR'
            display16.Roughness = 0.2
            display16.Metallic = 0.4

            display17.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display17.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]

            display18.AmbientColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]
            display18.DiffuseColor = [0.0549019607843137, 0.0254901960784314, 0.0333333333333333]

            time_test02 = time.time()
            print("paraview one object:" + str(time_test02 - time_test01))
        elif testmode == 1:
            reader01 = simple.OpenDataFile(
                r'D:\553_1.obj')
            reader02 = simple.OpenDataFile(
                r'D:\553_2.obj')
            reader03 = simple.OpenDataFile(
                r'D:\553_3.obj')
            reader04 = simple.OpenDataFile(
                r'D:\553_4.obj')
            time_test01 = time.time()
            display = simple.Show(reader01)
            display1 = simple.Show(reader02)
            display2 = simple.Show(reader03)
            display3 = simple.Show(reader04)

            display.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display1.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display1.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display2.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display2.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            display3.AmbientColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]
            display3.DiffuseColor = [0.8549019607843137, 0.9254901960784314, 0.9333333333333333]

            time_test02 = time.time()
            print("paraview one object:" + str(time_test02 - time_test01))
        elif testmode == 2:
            reader01 = simple.OpenDataFile(
                r'D:\Assembly\Part1.obj')
            reader02 = simple.OpenDataFile(
                r'D:\Assembly\Part2.obj')
            reader03 = simple.OpenDataFile(
                r'D:\Assembly\Part3.obj')
            reader04 = simple.OpenDataFile(
                r'D:\Assembly\Part4.obj')
            reader05 = simple.OpenDataFile(
                r'D:\Assembly\Part5.obj')
            reader06 = simple.OpenDataFile(
                r'D:\Assembly\Part6.obj')
            reader07 = simple.OpenDataFile(
                r'D:\Assembly\Part7.obj')
            reader08 = simple.OpenDataFile(
                r'D:\Assembly\Part8.obj')
            reader09 = simple.OpenDataFile(
                r'D:\Assembly\Part9.obj')
            reader10 = simple.OpenDataFile(
                r'D:\Assembly\Part10.obj')
            reader11 = simple.OpenDataFile(
                r'D:\Assembly\Part11.obj')

            time_test01 = time.time()
            display = simple.Show(reader01)
            display1 = simple.Show(reader02)
            display2 = simple.Show(reader03)
            display3 = simple.Show(reader04)
            display4 = simple.Show(reader05)
            display5 = simple.Show(reader06)
            display6 = simple.Show(reader07)
            display7 = simple.Show(reader08)
            display8 = simple.Show(reader09)
            display9 = simple.Show(reader10)
            display10 = simple.Show(reader11)

            #粉色
            display.AmbientColor = [0.9453125607843137, 0.6093751960784314, 0.6914062533333333]
            display.DiffuseColor = [0.9453125607843137, 0.6093751960784314, 0.6914062533333333]
            #天蓝色
            display1.AmbientColor = [0.4249019607843137, 0.7074901960784314, 0.9333333333333333]
            display1.DiffuseColor = [0.4249019607843137, 0.7074901960784314, 0.9333333333333333]
            #草绿色
            display2.AmbientColor = [0.2343759607843137, 0.6992187560784314, 0.4414062533333333]
            display2.DiffuseColor = [0.2343759607843137, 0.6992187560784314, 0.4414062533333333]
            #深橙色
            display3.AmbientColor = [0.9960937507843137, 0.5468751960784314, 0.0033333333333333]
            display3.DiffuseColor = [0.9960937507843137, 0.5468751960784314, 0.0033333333333333]
            #番茄红
            display4.AmbientColor = [0.9960937507843137, 0.3882352941176471, 0.2784313725490196]
            display4.DiffuseColor = [0.9960937507843137, 0.3882352941176471, 0.2784313725490196]
            #红
            display5.AmbientColor = [0.8803921568627451, 0.0004901960784314, 0.0274509803921569]
            display5.DiffuseColor = [0.8803921568627451, 0.0004901960784314, 0.0274509803921569]
            # 紫罗兰
            display6.AmbientColor = [0.5803921568627451, 0.0004901960784314, 0.8274509803921569]
            display6.DiffuseColor = [0.5803921568627451, 0.0004901960784314, 0.8274509803921569]
            #金色
            display7.AmbientColor = [0.9549019607843137, 0.8254901960784314, 0.0033333333333333]
            display7.DiffuseColor = [0.9549019607843137, 0.8254901960784314, 0.0033333333333333]
            #浅蓝色
            display8.AmbientColor = [0.6862745098039216, 0.9333333333333333, 0.9333333333333333]
            display8.DiffuseColor = [0.6862745098039216, 0.9333333333333333, 0.9333333333333333]
            #lavender
            display9.AmbientColor = [0.9019607843137255, 0.9019607843137255, 0.9803921568627451]
            display9.DiffuseColor = [0.9019607843137255, 0.9019607843137255, 0.9803921568627451]
            #Azure
            display10.AmbientColor = [0.9411764705882353, 1.0, 1.0]
            display10.DiffuseColor = [0.9411764705882353, 1.0, 1.0]

            # text1 = Text()
            # text1.Text = '358105 triangles / 1 parts.'
            # text2Display = simple.Show(text1)
            # text2Display.FontFamily = 'Times'
            # text2Display.FontSize = 13

            time_test02 = time.time()
            print("paraview one object:" + str(time_test02 - time_test01))

        simple.Render()

        # open ShowAnnotation
        pxm = simple.servermanager.ProxyManager()
        renderingSettings = pxm.GetProxy('settings', 'RenderViewSettings')
        renderingSettings.ShowAnnotation = 0

        pxm = simple.servermanager.ProxyManager()
        interactionProxy = pxm.GetProxy('settings',
                                      'RenderViewInteractionSettings')
        interactionProxy.Camera3DManipulators = ['Rotate',
                                               'Pan',
                                               'Zoom',
                                               'Pan',
                                               'Roll',
                                               'Pan',
                                               'Zoom',
                                               'Rotate',
                                               'Zoom']
        # Custom rendering settings
        renderingSettings = pxm.GetProxy('settings', 'RenderViewSettings')
        renderingSettings.LODThreshold = 102400

# =============================================================================
# Main: Parse args and start server
# =============================================================================

if __name__ == "__main__":
  # Create argument parser
  parser = argparse.ArgumentParser(description="PVWSD")

  # Add arguments with argparse.
  server.add_arguments(parser)
  PVWSDServer.add_arguments(parser)
  args = parser.parse_args()
  PVWSDServer.configure(args)

  # Start server
  server.start_webserver(options=args, protocol=PVWSDServer)
