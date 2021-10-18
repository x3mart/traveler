import React from 'react';
import { BlockFindTour, BlockFeedback, BlockViewed, BlockNewTour, BlockPresentation, BlockBreadCrumbs, BlockInfoDetail, BlockFiltersTypeTour,
        BlockDetailComfortLevel, BlockBookmarks, BlockImpression, BlockTourOverview, CardOnTop } from '../../../components';
import { withLayout } from '../../../layout/Layout';
// import { Sidebar } from '../../../layout/Sidebar/Sidebar';
import Head from 'next/head';
import { SectionFlex } from '../../../components/SectionFlex/SectionFlex';
import { SectionBlock } from '../../../components/SectionBlock/SectionBlock';


DetailTour.title='Детали тура'; 
function DetailTour(): JSX.Element {   
  return ( 
    <>       
        <Head>
          <title>{DetailTour.title}</title>
        </Head> 
        <BlockPresentation block_style='presentation_block_another' children={undefined} />
        <SectionBlock>
        <BlockBreadCrumbs block_style="viewed_block" margin="margin_second" children={undefined} />
        </SectionBlock>

        <SectionFlex>
        <main>
            <BlockInfoDetail children={undefined} />
            <BlockFiltersTypeTour children={undefined} />
            <BlockDetailComfortLevel children={undefined} />
            <BlockBookmarks children={undefined} />
            <BlockImpression children={undefined} />
            <BlockTourOverview children={undefined} />
          </main>     
          <aside>
            <CardOnTop />
          </aside>
        </SectionFlex>
        <SectionBlock>
        <BlockFeedback children={undefined} />
            <BlockViewed children={undefined} />
            <BlockNewTour children={undefined} />  
            <BlockFindTour children={undefined} />
        </SectionBlock>
    </>
  );
}

export default withLayout(DetailTour); 

