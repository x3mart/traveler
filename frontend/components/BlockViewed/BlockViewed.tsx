import styles from './BlockViewed.module.css';
import { BlockViewedProps } from './BlockViewed.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '../../components/';

export const BlockViewed = ({ block_style, children, className, ...props }: BlockViewedProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
                [styles.white]: block_style == 'white',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <InfoBlock border_color='orange_left_border'>
                        <Htag tag='h2'>
                            Недавно просмотренные туры
                        </Htag>
                        <Htag tag='h4'>
                            Мы сохранили для вас недавно просмотренные вами туры, возможно вы захотите к ним вернуться и выбрать один из них
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='viewed' children={undefined} />
            </div> 
            
        </div>
    );
};