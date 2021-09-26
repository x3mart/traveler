import styles from './CardCollection.module.css';
import { CardCollectionProps } from './CardCollection.props';
import cn from 'classnames';
import { CardTour } from '../../components/';
import ArrowIconLeft from '/public/left_arrow.svg';
import ArrowIconRight from '/public/right_arrow.svg';

export const CardCollection = ({ block_style, children, className, ...props }: CardCollectionProps): JSX.Element => {    
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