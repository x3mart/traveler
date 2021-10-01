import styles from './BlockFeedback.module.css';
import { BlockFeedbackProps } from './BlockFeedback.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockFeedback = ({ block_style, children, className, ...props }: BlockFeedbackProps): JSX.Element => {    
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
                            Отзывы наших путешественников
                        </Htag>
                        <Htag tag='h4'>
                            Все самое интересное
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='feedback' children={undefined} />
            </div> 
            
        </div>
    );
};