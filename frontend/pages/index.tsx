
import React from 'react';
import { P, BlockPresentation, BlockViewed } from '../components';
import { withLayout } from '../layout/Layout';


function Home(): JSX.Element {   
  return ( 
    <>       
        <BlockPresentation block_style='presentation_block'/>
        <BlockViewed />
        
    </>
  );
}

export default withLayout(Home);