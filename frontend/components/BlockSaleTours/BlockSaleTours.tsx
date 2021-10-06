import styles from './BlockSaleTours.module.css';
import { BlockSaleToursProps } from './BlockSaleTours.props';
import cn from 'classnames';
import { InfoBlock, Htag, CardCollection } from '..';

export const BlockSaleTours = ({ block_style, children, className, ...props }: BlockSaleToursProps): JSX.Element => {    
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
                            Туры со скидками 
                        </Htag>
                        <Htag tag='h4'>
                            Только сегодня уникальные предложения по доступным ценам
                        </Htag>
                    </InfoBlock> 
                    <CardCollection name_block='sales' children={undefined} />
            </div> 
            
        </div>
    );
};