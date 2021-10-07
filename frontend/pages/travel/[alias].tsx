// import { GetStaticProps } from 'next';
import React from 'react';
import { BlockViewed } from '../../components';
import { withLayout } from '../../layout/Layout';
// import axios from 'axios';


function Home(): JSX.Element {   
    return ( 
      <>       
          {/* <BlockPresentation block_style='presentation_block' children={undefined} /> */}
          <BlockViewed children={undefined} />
          {/* <BlockPopularCountry children={undefined} />
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
          <BlockAboutUs children={undefined} /> */}
          
      </>
    );
  }
  
  export default withLayout(Home); 

// export const getStaticProps: GetStaticProps<TravelProps> = async () => {
//   const firstCategory = 0;
//   const { data: page } = await axios.post<TravelProps[]>(process.env.NEXT_PUBLIC_DOMAIN + '/api/top-page/find', {
//     firstCategory
//   });
//   return {
//     props: {
//       page,
//       firstCategory
//     }
//   };
// };

// interface TravelProps extends Record<string, unknown> {
//     firstCategory: number;
// }