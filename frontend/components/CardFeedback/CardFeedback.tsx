import styles from './CardFeedback.module.css';
import { CardFeedbackProps } from './CardFeedback.props';
import cn from 'classnames';
import { Tag, Htag } from '..';
import StarIcon from '/public/Star.svg';
import LikeIcon from '/public/Like.svg';
    


export const CardFeedback = ({ block_style, children, className, ...props }: CardFeedbackProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
            })}
            {...props}
            
        >    
                  
            {children}
            <Tag size='feedback'>
                
            </Tag>     
             
        </div>
    );
};