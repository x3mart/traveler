import styles from './CardTypeTour.module.css';
import { CardTypeTourProps } from './CardTypeTour.props';
import cn from 'classnames';
import { Tag, Htag } from '..';
    


export const CardTypeTour = ({ block_style, children, className, ...props }: CardTypeTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
            })}
            {...props}
            
        >    
                  
            {children}
            <Tag size='m'>                
                <div className={styles.card_type_tour_content}>
                    
                    <Htag tag='h4'>Россия</Htag>
                    <Htag tag='h3'>325 туров</Htag>
                        
                </div>
            </Tag>     
             
        </div>
    );
};