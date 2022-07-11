# This code is released under the Creative Commons zero license.  Go wild, but
# it would be nice to preserve the credit if you find it helpful.
#
# Tom Sgouros
# Center for Computation and Visualization
# Brown University
# March 2018.
import os, sys, logging, types, inspect, traceback, logging, re, json, base64
from time import time

# import RPC annotation
from wslink import register as exportRPC

# import paraview modules.
import paraview

from paraview import simple, servermanager, selection
from paraview.web import protocols as pv_protocols

# This class inherits from the standard ParaViewWeb protocols, and adds a
# few new ones with the @exportRPC decorator.  These become RPC calls that
# can be invoked from the web client.

class PVWSDTest(pv_protocols.ParaViewWebProtocol):

    def __init__(self):
        self.pickPointorCell = -1
        self.flagRunOnce = 0
        self.presetColorMap = {}
        super(PVWSDTest, self).__init__()

    @exportRPC("pvwsdprotocol.pick.point")
    def pickCone(self, positionx, positiony):
        # pre save the preset color into map
        self.renderview = simple.GetRenderView()
        if self.flagRunOnce == 0:
            self.flagRunOnce = 1
            for source in simple.GetSources().values():
                self.sourceDisplay = simple.GetDisplayProperties(source, self.renderview)
                self.presetColorMap[self.sourceDisplay.GetGlobalID()] = self.sourceDisplay.DiffuseColor.GetData()
        else:
            for source in simple.GetSources().values():
                self.sourceDisplay = simple.GetDisplayProperties(source, self.renderview)
                self.sourceDisplay.AmbientColor = self.presetColorMap[self.sourceDisplay.GetGlobalID()]
                self.sourceDisplay.DiffuseColor = self.presetColorMap[self.sourceDisplay.GetGlobalID()]
        positionx = int(positionx)
        positiony = int(positiony)

        # we get mouse position and pick a point or a cell
        # self.renderview = simple.GetRenderView()
        # a = self.renderview.Pick(positionx, positiony)
        # help(a)

        # pick point or cell
        # if self.pickPointorCell == -1:
        #     # select point
        #     selection.SelectSurfacePoints(Rectangle=[positionx, positiony, positionx, positiony])
        # else:
        #     # select cell
        #     selection.SelectSurfaceCells(Rectangle=[positionx, positiony, positionx, positiony])

        # 获取点或网格的信息
        # extractSelection = simple.ExtractSelection(Input=self.source)
        # selectionData = paraview.servermanager.Fetch(extractSelection)
        # print(selectionData)

        # pick object
        self.obj_picked = self.renderview.Pick(positionx, positiony) # GeometryRepresentation

        if self.obj_picked != None:
            id_objPicked = self.obj_picked.GetGlobalID()
            self.obj_picked.Specular = 100.0
            self.obj_picked.DiffuseColor = (1.0, 1.0, 0.0)
            self.obj_picked.AmbientColor = (1.0, 1.0, 1.0)
            # self.obj_picked.SetRepresentationType('Surface With Edges')
            # self.obj_picked.LineWidth = 5.0
            self.sources = simple.GetSources()
            for source in self.sources.values():
                representation = simple.GetDisplayProperties(source, self.renderview)
                id_sourse = representation.GetGlobalID()
                if (id_sourse == id_objPicked):
                    self.source = source # TrivialProducer
                    simple.SetActiveSource(source)
        self.getApplication().InvokeEvent('UpdateEvent')

    @exportRPC("pvwsdprotocol.pick.mode")
    def pickMode(self, r_pickPointorCell):
        self.pickPointorCell = r_pickPointorCell



    @exportRPC("pvwsdprotocol.wireframe.object")
    def wireFrame(self):
        # wireframe object
        simple.SetDisplayProperties(Representation="Wireframe")
        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Wireframe mode open")

    @exportRPC("pvwsdprotocol.opacity.object")
    def opacity(self):
        # wireframe object
        self.source = simple.GetActiveSource()
        self.view = simple.GetRenderView()
        self.sourceDisplay = simple.GetDisplayProperties(self.source,self.view)
        self.sourceDisplay.Opacity = 0.5
        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Opacity mode open")

    @exportRPC("pvwsdprotocol.clip.object")
    def clip(self):
        # clip a object
        self.source = simple.GetActiveSource()
        self.renderview = simple.GetRenderView()

        self.clip1 = simple.Clip(Input = self.source)

        self.clip1.ClipType = 'Plane' #type = plane box sphere cylinder scalar
        self.clip1.ClipType.Origin = [0.0, 0.0, 0.0]
        self.clip1.ClipType.Normal = [1.0, 0.0, 0.0]

        # self.clip1.ClipType = 'Sphere'
        # self.clip1.Scalars = ['POINTS', '']
        # self.clip1.ClipType.Center = [0.0, 0.0, 0.0]
        # self.clip1.ClipType.Radius = 0.2
        # self.clip1.Invert = 0
        # self.renderview.Update()

        self.clip1Display = simple.Show(self.clip1, self.renderview)

        simple.Hide(self.source,self.renderview)
        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Clip executed")

    @exportRPC("pvwsdprotocol.transform.object")
    def transform(self):
        self.source = simple.GetActiveSource()
        self.view = simple.GetRenderView()
        self.sourceDisplay = simple.GetDisplayProperties(self.source, self.view)
        self.sourceDisplay.Position = [0.2, 0.0, 0.0]
        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Transform executed")

    @exportRPC("pvwsdprotocol.recover.object")
    def recover(self):
        simple.SetDisplayProperties(Representation="Surface")
        self.source = simple.GetActiveSource()
        self.view = simple.GetRenderView()
        self.sourceDisplay = simple.GetDisplayProperties(self.source, self.view) # GeometryRepresentation
        self.sourceDisplay.Opacity = 1
        self.sourceDisplay.AmbientColor = self.presetColorMap[self.sourceDisplay.GetGlobalID()]
        self.sourceDisplay.DiffuseColor = self.presetColorMap[self.sourceDisplay.GetGlobalID()]
        # reset the flag for pick once
        # print(self.presetColorMap[self.sourceDisplay.GetGlobalID()])



        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Recover executed")

    @exportRPC("pvwsdprotocol.reset.object")
    def reset(self):
        simple.ResetCamera()
        self.getApplication().InvokeEvent('UpdateEvent')
        # print("Camera reset executed")


