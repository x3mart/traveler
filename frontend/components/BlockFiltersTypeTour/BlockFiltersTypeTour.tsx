import styles from './BlockFiltersTypeTour.module.css';
import { BlockFiltersTypeTourProps } from './BlockFiltersTypeTour.props';
import cn from 'classnames';


export const BlockFiltersTypeTour = ({ block_style, children, className, ...props }: BlockFiltersTypeTourProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.filter_item} {...props}>Тип в горы</div>
                    <div className={styles.filter_item} {...props}>Этнотур</div>
                    <div className={styles.filter_item} {...props}>Авто тур</div>
                    <div className={styles.filter_item} {...props}>Джип тур</div>
                    <div className={styles.filter_item} {...props}>Экскурсионный тур</div>
                    
                    
                    
                    
            </div> 
            
        </div>
    );
};