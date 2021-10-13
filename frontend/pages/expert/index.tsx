import React from 'react';
import { BlockFindTourWhite, BlockBreadCrumbs, BlockFindTour, BlockAboutUs, BlockViewed, BlockExpertDetail } from '../../components';
import { withLayout } from '../../layout/Layout';
import Head from 'next/head';


Home.title='Выбери путешествие'; 
function Home(): JSX.Element {   
  return ( 
    <>       
        <Head>
          <title>{Home.title}</title>
        </Head>  
        <BlockFindTourWhite children={undefined} />
        <BlockBreadCrumbs block_style="viewed_block" margin="margin_first" children={undefined} />
        <BlockExpertDetail children={undefined} />        
        <BlockViewed children={undefined} />
        <BlockFindTour children={undefined} />
        <BlockAboutUs children={undefined} />
        
    </>
  );
}

export default withLayout(Home); 

