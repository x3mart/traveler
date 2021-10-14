import styles from './CardCollection.module.css';
import { CardCollectionProps } from './CardCollection.props';
import cn from 'classnames';
import { CardTour, CardCountryTour, CardTourLarge, CardTypeTour, CardExpert, Rating, Sale, CardFeedback, CardAboutExpert } from '../../components/';
import ArrowIconLeft from '/public/left_arrow.svg';
import ArrowIconRight from '/public/right_arrow.svg';
import Link from 'next/link';

export const CardCollection = ({name_block, children, className, ...props }: CardCollectionProps): JSX.Element => {    
    switch (name_block) {
        case 'viewed':
          return <div
                    className={ cn(styles.card_collection, className, {
                    })}
                    {...props}
                >
                    <div className={styles.card_tour_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_tour_arrow_right}><ArrowIconRight /></div>  
                    {children}
                    <CardTour />
                    <CardTour /> 
                    <CardTour />    
                </div>;
        case 'popular':
          return <div
                    className={ cn(styles.card_collection_popular, className, {
                    })}
                    {...props}
                > 
                    {children}
                    <CardCountryTour />
                    <CardCountryTour /> 
                    <CardCountryTour />
                    <CardCountryTour />
                    <CardCountryTour /> 
                    <CardCountryTour /> 
                    <CardCountryTour className={styles.none} />
                    <CardCountryTour className={styles.none} /> 
                    <CardCountryTour className={styles.none} /> 
                    <CardCountryTour className={styles.none} />
                    <CardCountryTour className={styles.none} /> 
                    <CardCountryTour className={styles.none} />     
                </div>;
        case 'personal':
          return <div
                    className={ cn(styles.card_collection, className, {
                    })}
                    {...props}
                >
                    {children}
                    <div className={styles.card_personal_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_personal_arrow_right}><ArrowIconRight /></div>                    
                    <CardTourLarge /> 
                    <CardTour />    
                </div>;
        case 'new':
          return <h4 className={styles.h4}>{children}</h4>;
        case 'type':
          return <div
                    className={ cn(styles.card_collection_type, className, {
                    })}
                    {...props}
                >                      
                    {children}
                    <CardTypeTour />  
                    <CardTypeTour /> 
                    <CardTypeTour /> 
                    <CardTypeTour /> 
                    <CardTypeTour /> 
                    <CardTypeTour />    
                </div>;
        case 'rating':
          return <div
                    className={ cn(styles.card_collection, className, {
                    })}
                    {...props}
                >
                    <div className={styles.card_tour_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_tour_arrow_right}><ArrowIconRight /></div>  
                    {children}
                    <CardTour block_style='card_tour_border'><Rating children={undefined} /></CardTour>
                    <CardTour block_style='card_tour_border'><Rating children={undefined} /></CardTour>
                    <CardTour block_style='card_tour_border'><Rating children={undefined} /></CardTour>    
                </div>;
        case 'experts':
          return <div
                      className={ cn(styles.card_collection_experts, className, {
                      })}
                      {...props}
                  >
                    <div className={styles.card_collection_experts_block}> 
                          <div className={styles.card_expert_arrow_left}><ArrowIconLeft /></div>
                          <div className={styles.card_expert_arrow_right}><ArrowIconRight /></div>  
                          {children}
                          <div className={styles.card_collection_expert_card_hidden_expert_left}></div>
                          <CardExpert className={styles.card_collection_expert_card_hidden} />
                          <CardExpert /> 
                          <CardExpert />
                          <CardExpert />
                          <CardExpert />
                          <CardExpert className={styles.card_collection_expert_card_hidden} />
                          <div className={styles.card_collection_expert_card_hidden_expert_right}></div>  
                    </div>   
                  </div>;
        case 'sales':
          return <div
                    className={ cn(styles.card_collection, className, {
                    })}
                    {...props}
                >
                    <div className={styles.card_tour_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_tour_arrow_right}><ArrowIconRight /></div>  
                    {children}
                    <CardTour block_style='card_tour_border'>
                      <Sale children={undefined} />
                      <div className={styles.sale_cost_block}>
                          <span className={styles.sale_cost}>89.000 <span className={styles.sale_cost_rub}>{'\u20bd'}</span></span>
                      </div>                      
                    </CardTour>
                    <CardTour block_style='card_tour_border'>
                      <Sale children={undefined} />
                      <div className={styles.sale_cost_block}>
                          <span className={styles.sale_cost}>89.000 <span className={styles.sale_cost_rub}>{'\u20bd'}</span></span>
                      </div>                      
                    </CardTour>
                    <CardTour block_style='card_tour_border'>
                      <Sale children={undefined} />
                      <div className={styles.sale_cost_block}>
                          <span className={styles.sale_cost}>89.000 <span className={styles.sale_cost_rub}>{'\u20bd'}</span></span>
                      </div>                      
                    </CardTour>    
                </div>; 
        case 'feedback':
          return <div
                    className={ cn(styles.card_feedback, className, {
                    })}
                    {...props}
                >
                    <div className={styles.card_feedback_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_feedback_arrow_right}><ArrowIconRight /></div>  
                    {children}
                    <CardFeedback />
                    <CardFeedback />                      
                </div>;
          case 'tour-page':
            return <div
                      className={ cn(styles.tour_page, className, {
                      })}
                      {...props}
                  >
                      <Link href='/tour/detail-tour/'>
                        <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} />
                      </Link>
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} />     
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} />
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} />
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="block_width_travel_page" block_style='card_tour_border' className={styles.tour_page_card} />
                      <CardTour block_width="display_none" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="display_none" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="display_none" block_style='card_tour_border' className={styles.tour_page_card} />
                      <CardTour block_width="display_none" block_style='card_tour_border' className={styles.tour_page_card} /> 
                      <CardTour block_width="display_none" block_style='card_tour_border' className={styles.tour_page_card} />                  
                  </div>;
          case 'about_expert':
            return <div
                      className={ cn(styles.about_expert_block, className, {
                      })}
                      {...props}
                  >
                      <div className={styles.card_about_expert_arrow_left}><ArrowIconLeft /></div>
                      <div className={styles.card_about_expert_arrow_right}><ArrowIconRight /></div>  
                      {children}
                      <div className={styles.card_collection_expert_card_hidden_left}></div>
                      <CardAboutExpert className={styles.card_collection_expert_card_hidden} />
                      <CardAboutExpert /> 
                      <CardAboutExpert />
                      <CardAboutExpert />
                      <CardAboutExpert />
                      <CardAboutExpert className={styles.card_collection_expert_card_hidden} />
                      <div className={styles.card_collection_expert_card_hidden_right}></div>   
                  </div>;
          default:
          return <></>;
      }     
};