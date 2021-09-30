import styles from './BlockRecomendation.module.css';
import { BlockRecomendationProps } from './BlockRecomendation.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockRecomendation = ({ block_style, children, className, ...props }: BlockRecomendationProps): JSX.Element => {    
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
                            Персональные рекомендации
                        </Htag>
                        <Htag tag='h4'>
                            Мы подобрали туры именно для вас
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='personal' children={undefined} />
            </div> 
            
        </div>
    );
};