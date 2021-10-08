import React from 'react';
import { BlockFindTourWhite, BlockBreadCrumbs, BlockFilters, BlockTravels, BlockFindTour, BlockAboutUs } from '../../components';
import { withLayout } from '../../layout/Layout';
import axios from 'axios';


function Home(): JSX.Element {   
  return ( 
    <>       
        <BlockFindTourWhite children={undefined} />
        <BlockBreadCrumbs children={undefined} />
        <BlockFilters children={undefined} />
        <BlockTravels children={undefined} />
        <BlockFindTour children={undefined} />
        <BlockAboutUs children={undefined} />
        
    </>
  );
}

export default withLayout(Home); 

