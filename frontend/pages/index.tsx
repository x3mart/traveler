
import React from 'react';
import { BlockPresentation, BlockViewed, BlockPopularCountry, BlockRecomendation, BlockAdvantage, BlockNewTour, BlockChangeCountry, BlockTypeTours, BlockRaitingTours } from '../components';
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
        <BlockChangeCountry />
        <BlockTypeTours />
        <BlockRaitingTours />
        
    </>
  );
}

export default withLayout(Home); 