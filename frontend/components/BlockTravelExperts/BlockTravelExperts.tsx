import styles from './BlockTravelExperts.module.css';
import { BlockTravelExpertsProps } from './BlockTravelExperts.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockTravelExperts = ({ block_style, children, className, ...props }: BlockTravelExpertsProps): JSX.Element => {    
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
                            Популярные тревел-эксперты
                        </Htag>
                        <Htag tag='h4'>
                            Лучшие из лучших
                        </Htag>
                    </InfoBlock>                     
            </div> 
            <CardCollection name_block='experts' children={undefined} />
            
        </div>
    );
};