import React from 'react';
import { BlockPresentation, BlockViewed, BlockPopularCountry, BlockRecomendation, 
        BlockAdvantage, BlockNewTour, BlockChangeCountry, BlockTypeTours, BlockRaitingTours, 
        BlockTravelExperts, BlockSaleTours, BlockFeedback, BlockMoodTours, BlockFindTour, BlockAboutUs } from '../components';
import { withLayout } from '../layout/Layout';
import Head from 'next/head';

Home.title='Traveler Market - Маркетплейс авторских туров'; 
function Home(): JSX.Element {   
  return ( 
    <>       
        <Head>
          <title>{Home.title}</title>
        </Head>
        <BlockPresentation block_style='presentation_block' children={undefined} />
        <BlockViewed children={undefined} />
        <BlockPopularCountry children={undefined} />
        <BlockRecomendation children={undefined} />
        <BlockAdvantage children={undefined} />
        <BlockNewTour children={undefined} />
        <BlockChangeCountry children={undefined} />
        <BlockTypeTours children={undefined} />
        <BlockRaitingTours children={undefined} />
        <BlockTravelExperts children={undefined} />
        <BlockSaleTours children={undefined} />
        <BlockFeedback children={undefined} />
        <BlockMoodTours children={undefined} /> 
        <BlockFindTour children={undefined} />
        <BlockAboutUs children={undefined} />
        
    </>
  );
}

export default withLayout(Home); 

