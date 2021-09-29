
import React from 'react';
import { BlockPresentation, BlockViewed, BlockPopularCountry, BlockRecomendation, BlockAdvantage, BlockNewTour } from '../components';
import { withLayout } from '../layout/Layout';


function Home(): JSX.Element {   
  return ( 
    <>       
        <BlockPresentation block_style='presentation_block'/>
        <BlockViewed />
        <BlockPopularCountry />
        <BlockRecomendation />
        <BlockAdvantage />
        <BlockNewTour />
        
    </>
  );
}

export default withLayout(Home); 