import styles from './BlockFindTour.module.css';
import { BlockFindTourProps } from '../BlockFindTour/BlockFindTour.props';
import cn from 'classnames';
import { InfoBlock, Htag, FormGetTour } from '..';

export const BlockFindTour = ({ block_style, children, className, ...props }: BlockFindTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block', 
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                <div className={styles.findtour_block} {...props}>
                    <InfoBlock border_color='white_left_border'>
                        <Htag tag='h2'>
                            Подобрать тур 
                        </Htag>
                        <Htag tag='h4'>
                            Мы подберем только лучшее
                        </Htag>
                    </InfoBlock>
                    <FormGetTour form_style='second_form_get_tour' children={undefined} />  
                </div>
            </div> 
            
        </div>
    );
};