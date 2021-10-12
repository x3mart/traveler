import React from 'react';
import { BlockFindTour, BlockFeedback, BlockViewed, BlockNewTour, BlockPresentation, BlockBreadCrumbs, BlockInfoDetail, BlockFiltersTypeTour,
        BlockDetailComfortLevel, BlockBookmarks, BlockImpression, BlockTourOverview, CardOnTop } from '../../../components';
import { withLayout } from '../../../layout/Layout';
import Head from 'next/head';

Home.title='Детализация'; 
function Home(): JSX.Element {   
  return ( 
    <>       
        <Head>
          <title>{Home.title}</title>
        </Head> 
        <BlockPresentation block_style='presentation_block_another' children={undefined} />
        
        <BlockBreadCrumbs block_style="viewed_block" margin="margin_second" children={undefined} />
        <BlockInfoDetail children={undefined} />
        <BlockFiltersTypeTour children={undefined} />
        <BlockDetailComfortLevel children={undefined} />
        <BlockBookmarks children={undefined} />
        <BlockImpression children={undefined} />
        <CardOnTop />
        <BlockTourOverview children={undefined} />

        <BlockFeedback children={undefined} />
        <BlockViewed children={undefined} />
        <BlockNewTour children={undefined} />  
        <BlockFindTour children={undefined} />
        
    </>
  );
}

export default withLayout(Home);  

