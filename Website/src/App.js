import './App.css';
import React from 'react';
import { BrowserRouter, Route, Link, Routes, Navigate } from 'react-router-dom';

import Homepg from './homepage/Homepg';
import BlastSearch from './blastsearch/BlastSearch';
import Compare from './compare/Compare';
import Multiple_Align from './multiple_align/Multiple_Align';
import Generate_Tree from './generate_tree/GenerateTree';
import VariationAnalyzer from './variationanalyzer/VariationAnalyzer';
import ViewQueues from './viewqueues/ViewQueues';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<Homepg />} />
        <Route path="/blast_search" element={<BlastSearch />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/multiple_align" element={<Multiple_Align />} />
        <Route path="/generate_tree" element={<Generate_Tree />} />
        <Route path="/variation_analyzer" element={<VariationAnalyzer />} />
        <Route path="/view_queues" element={<ViewQueues />} />
        <Route path="*" element={<h1>Page Not Found</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
