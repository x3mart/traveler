import styles from './BlockRaitingTours.module.css';
import { BlockRaitingToursProps } from './BlockRaitingTours.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockRaitingTours = ({ block_style, children, className, ...props }: BlockRaitingToursProps): JSX.Element => {    
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
                            Путешествия на основании оценок и отзывов 
                        </Htag>
                        <Htag tag='h4'>
                            Самое популярное среди наших клиентов
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='rating' children={undefined} />
            </div> 
            
        </div>
    );
};