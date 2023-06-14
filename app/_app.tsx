'use client'

import React from 'react';
import ReactDOM from 'react-dom';
import { DataContextProvider } from './components/dataContext';
import Page from './index';

ReactDOM.render(
  <DataContextProvider>
    <Page />
  </DataContextProvider>,
  document.getElementById('root')
);