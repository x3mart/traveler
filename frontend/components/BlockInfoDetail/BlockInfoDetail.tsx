import styles from './BlockInfoDetail.module.css';
import { BlockInfoDetailProps } from './BlockInfoDetail.props';
import cn from 'classnames';
import { Htag } from '..';
import StarIconBig from '/public/greenstarbig.svg';

export const BlockInfoDetail = ({ block_style, children, className, ...props }: BlockInfoDetailProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.detail_tour_block} {...props}>
                        <div className={styles.detail_tour_block_info} {...props}>
                            <Htag tag='h2'>
                                Сокровища Дагестана - 5 дней приключений на джипах! 
                            </Htag>
                            <Htag tag='h3'>
                                Россия  -  Дагестан 
                            </Htag>
                        </div>
                        <div className={styles.detail_tour_block_raiting} {...props}>
                            <div className={styles.detail_tour_block_raiting_num} {...props}>
                                <StarIconBig />
                                <span className={styles.raiting_star}>4.9</span>
                            </div>                            
                            <span className={styles.raiting_star_feedback}>185 отзывов</span>
                        </div>  
                    </div> 
                    
            </div> 
            
        </div>
    );
};