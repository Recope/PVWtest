// This code is released under the Creative Commons zero license.  Go wild, but
// it would be nice to preserve the credit if you find it helpful.
//
// Tom Sgouros
// Center for Computation and Visualization
// Brown University
// March 2018.

import 'normalize.css';

import Workbench from 'paraviewweb/src/Component/Native/Workbench';
import ToggleControl from 'paraviewweb/src/Component/Native/ToggleControl';
import BGColor from 'paraviewweb/src/Component/Native/BackgroundColor';
import Spacer from 'paraviewweb/src/Component/Native/Spacer';
import Composite from 'paraviewweb/src/Component/Native/Composite';
import ReactAdapter from 'paraviewweb/src/Component/React/ReactAdapter';
import WorkbenchController from 'paraviewweb/src/Component/React/WorkbenchController';
import NumberSliderWidget from 'paraviewweb/src/React/Widgets/NumberSliderWidget';
import { debounce } from 'paraviewweb/src/Common/Misc/Debounce';


import SizeHelper from 'paraviewweb/src/Common/Misc/SizeHelper';
import ParaViewWebClient from 'paraviewweb/src/IO/WebSocket/ParaViewWebClient';
import VtkRenderer from 'paraviewweb/src/NativeUI/Renderers/VtkRenderer'

import React from 'react';
import ReactDOM from 'react-dom ';

import SmartConnect from 'wslink/src/SmartConnect';

// This URL and port number are determined when you invoke the server.
// See python/PVWSDServer.py for instructions.
const config = { sessionURL: 'ws://localhost:1234/ws' };//:9000

// We'll use that config object to create a connection to the
// pvpython-run server.
const smartConnect = SmartConnect.newInstance({ config });

// This is just a global object we can use to attach data to, in order to
// access it from other scopes.
var model = {};
var pickPointorCell = -1 // -1 point, 1 cell

// This is a hash of functions that return protocols.  For this example, we
// have only one, called 'pvwsdService'.  You could have more than one, though
// I'm not sure why you'd need that.
const pvwsdProtocols = {
  pvwsdService: (session) => {
     return {
      pickCone: (positionx, positiony) => {
         session.call('pvwsdprotocol.pick.point', [positionx, positiony]);
         // .then((result) => console.log('result: ' + result));
         console.log("******* pick a point or cell ********");
      },
      pickMode: () => {
        pickPointorCell = pickPointorCell * -1;
        var btnVal = document.getElementById("button_pickMode");
        console.log(pickPointorCell + btnVal.innerHTML)
        if(btnVal.innerHTML == "Pick Point")
            btnVal.innerHTML = "Pick Cell";
        else btnVal.innerHTML = "Pick Point";
         session.call('pvwsdprotocol.pick.mode', [pickPointorCell]);
         // .then((result) => console.log('result: ' + result));
         console.log("******* change pick mode ********");
      },
      wireFrame: () => {
         session.call('pvwsdprotocol.wireframe.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* wireframe ********");
      },
      opacity: () => {
         session.call('pvwsdprotocol.opacity.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* opacity ********");
      },
      clip: () => {
         session.call('pvwsdprotocol.clip.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* clip ********");
      },
      transform: () => {
         session.call('pvwsdprotocol.transform.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* transform ********");
      },
      recover: () => {
         session.call('pvwsdprotocol.recover.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* recover ********");
      },
      reset: () => {
         session.call('pvwsdprotocol.reset.object', []);
         // .then((result) => console.log('result: ' + result));
         console.log("******* reset ********");
      },

    };
  },
};

// Create a callback to be executed when the connection is made.
smartConnect.onConnectionReady((connection) => {
  // The createClient method takes a connection, a list of predefined protocols
  // to use, and a function that returns
  model.pvwClient =
    ParaViewWebClient.createClient(connection,
                                   [
                                     'MouseHandler',   // <--- These are pre-defined.
                                     'ViewPort',
                                     'ViewPortImageDelivery',
                                     'VtkImageDelivery',
                                   ],
                                   pvwsdProtocols);    // <-- These are yours.

  // Now build the HTML element that will display the goods.
  const renderer = VtkRenderer.newInstance({ client: model.pvwClient });

  renderer.setServerMaxFPS(60);
  renderer.setContainer(divRenderer);

  var canvas = renderer.getCanvas();
  canvas.addEventListener("click", function(event) {
    getMousePos(canvas, event);
  });

  function getMousePos(canvas, event) {

      var rect = canvas.getBoundingClientRect();
      var x= event.clientX - rect.left * (canvas.width / rect.width);
      var y= rect.bottom * (canvas.height / rect.height) - event.clientY;
      console.log("x:"+x+",y:"+y);
      model.pvwClient.pvwsdService.pickCone(x, y);
      
  }
  
  window.renderer = renderer;
  SizeHelper.onSizeChange(() => {
    renderer.resize();
  });
  SizeHelper.startListening();
});



const divRoot = document.createElement('div');
divRoot.id = "root";
document.body.appendChild(divRoot);

// Let's create the controls.
class PVWSDControlPanel extends React.Component {
  constructor(props) {
    super(props);
    // The state of the controls is really just the N on the slider.  There is
    // also a state for the visibility of the cone, but this is tracked on the
    // server.
    
  }

  render() {

    return (<center>
            <div style={{width: '100%', display: 'table'}}>
            <div style={{display: 'table-cell'}}>
            <button id="button_pickMode" onClick={() => model.pvwClient.pvwsdService.pickMode()}>Pick Point</button>
            <button onClick={() => model.pvwClient.pvwsdService.wireFrame()}>Wirframe mode</button>
            <button onClick={() => model.pvwClient.pvwsdService.opacity()}>Opacity</button>
            <button onClick={() => model.pvwClient.pvwsdService.transform()}>Transform</button>
            <button onClick={() => model.pvwClient.pvwsdService.recover()}>Recover</button>
            <button onClick={() => model.pvwClient.pvwsdService.reset()}>Reset Camera</button>
			      <button onClick={() => model.pvwClient.pvwsdService.clip()}>Plane Clip</button>
            <span style={{ marginLeft: 50}}>358,105 triangles / 8 parts</span>
            </div>
            <div style={{display: 'table-cell'}}>
            </div>
            </div>
            </center>
           );

  }
}

// Prepare the rest of the page to be shown.
const divRenderer = document.createElement('div');
document.body.appendChild(divRenderer);

divRenderer.style.position = 'relative';
divRenderer.style.width = '100vw';
divRenderer.style.height = '100vh';
divRenderer.style.overflow = 'hidden';

ReactDOM.render(<PVWSDControlPanel />,
                document.getElementById('root'));

// Let 'er rip.
smartConnect.connect();
