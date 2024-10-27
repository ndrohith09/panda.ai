import React from 'react';
import logo from './logo.svg'; 
import Sidebar from './components/Sidebar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Pipeline from 'components/Pipeline';
import PipelineData from 'components/PipelineData';

function App() {
  return (
    <BrowserRouter>
    <div className="App">     
     <Sidebar />
     <Routes>
     <Route path="pipeline/" element={<Pipeline />} />    
     <Route path="pipeline/:id" element={<PipelineData />} />    
      </Routes> 
    </div>
    </BrowserRouter>
  );
}

export default App;
