'use client'

import React, { createContext, useState } from 'react';

interface DataContextProps {
  dataContextValue: string | undefined;
  setDataContextValue: (value: string | undefined) => void;
}

export const DataContext = createContext<DataContextProps>({
  dataContextValue: undefined,
  setDataContextValue: () => {},
});

interface DataContextProviderProps {
  children: React.ReactNode;
}

export const DataContextProvider: React.FC<DataContextProviderProps> = ({
  children,
}) => {
  const [dataContextValue, setDataContextValue] = useState<string | undefined>(
    undefined
  );

  // Log the dataContextValue after it has been updated
  console.log('DataContextValue:', dataContextValue);

  return (
    <DataContext.Provider value={{ dataContextValue, setDataContextValue }}>
      {children}
    </DataContext.Provider>
  );
};
