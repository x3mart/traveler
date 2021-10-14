import React from 'react';
import { BlockFindTourWhite, BlockBreadCrumbs, BlockFindTour, BlockAboutUs, BlockViewed, BlockExpertsFeedback, BlockExpertDetail, BlockTeam } from '../../components';
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
        <BlockTeam children={undefined} />        
        <BlockViewed block_style='white' children={undefined} />
        <BlockExpertsFeedback block_style="viewed_block" children={undefined} />
        <BlockFindTour children={undefined} />
        <BlockAboutUs children={undefined} />
        
    </>
  );
}

export default withLayout(Home); 

