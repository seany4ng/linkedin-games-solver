import React from 'react';
import TangoBoard from './components/TangoBoard';
import QueensBoard from './components/QueensBoard';

const App: React.FC = () => {
  // TODO: this is the entrypoint for our app. we can start with Tango.
  // return <TangoBoard />;
  return <QueensBoard />;
};

export default App;
