import styles from './BlockNewTour.module.css';
import { BlockNewTourProps } from './BlockNewTour.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '../';

export const BlockNewTour = ({ block_style, children, className, ...props }: BlockNewTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <InfoBlock border_color='orange_left_border'>
                        <Htag tag='h2'>
                            Новинки
                        </Htag>
                        <Htag tag='h4'>
                            Все самое новое от наших тревел-экспертов
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='viewed' children={undefined} />
            </div> 
            
        </div>
    );
};