import styles from './BlockTravels.module.css';
import { BlockTravelsProps } from './BlockTravels.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection, Button } from '..';

export const BlockTravels = ({ block_style, children, className, ...props }: BlockTravelsProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <InfoBlock height_block='travel_page' border_color='blue_left_border'>
                        <div className={styles.info_content} {...props}>
                            <div className={styles.info_content_text} {...props}>
                                <Htag tag='h2'>
                                Путешествия
                                </Htag>
                                <Htag tag='h4'>
                                    Найден 2381 тур
                                </Htag>
                            </div>            
                            <Button className={styles.button_travel_filter_popular} appearance='header_button_travel' arrow='right'>Сначала популярные</Button>
                        </div>
                    </InfoBlock> 
                    <CardCollection name_block='tour-page' children={undefined} />  
            </div> 
            
        </div>
    );
};