import styles from './BlockTravels.module.css';
import { BlockTravelsProps } from './BlockTravels.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

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
                    <InfoBlock border_color='blue_left_border'>
                        <Htag tag='h2'>
                            Путешествия
                        </Htag>
                        <Htag tag='h4'>
                            Найден 2381 тур
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='tour-page' children={undefined} />
            </div> 
            
        </div>
    );
};