import styles from './BlockTypeTours.module.css';
import { BlockTypeToursProps } from './BlockTypeTours.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockTypeTours = ({ block_style, children, className, ...props }: BlockTypeToursProps): JSX.Element => {    
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
                            Туры по типам
                        </Htag>
                        <Htag tag='h4'>
                        Мы разделили туры на типы чтобы вам было удобнее выбрать нужный
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='type' children={undefined} />
            </div> 
            
        </div>
    );
};