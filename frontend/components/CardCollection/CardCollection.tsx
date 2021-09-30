import styles from './CardCollection.module.css';
import { CardCollectionProps } from './CardCollection.props';
import cn from 'classnames';
import { CardTour, CardCountryTour, CardTourLarge, CardTypeTour } from '../../components/';
import ArrowIconLeft from '/public/left_arrow.svg';
import ArrowIconRight from '/public/right_arrow.svg';

export const CardCollection = ({name_block, block_style, children, className, ...props }: CardCollectionProps): JSX.Element => {    
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
                    <div className={styles.card_tour_arrow_left}><ArrowIconLeft /></div>
                    <div className={styles.card_tour_arrow_right}><ArrowIconRight /></div>  
                    {children}
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
          return <h4 className={styles.h4}>{children}</h4>;
        case 'experts':
          return <h4 className={styles.h4}>{children}</h4>;
        case 'sales':
          return <h4 className={styles.h4}>{children}</h4>;
        case 'feedback':
          return <h4 className={styles.h4}>{children}</h4>;
          default:
          return <></>;
      }     
    return (
        <div
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
        </div>
    );
};