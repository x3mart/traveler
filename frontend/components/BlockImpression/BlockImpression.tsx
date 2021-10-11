import styles from './BlockImpression.module.css';
import { BlockImpressionProps } from './BlockImpression.props';
import cn from 'classnames';
import DoneIcon from '../../public/done.svg';
import { Htag } from '..';

export const BlockImpression = ({ block_style, children, className, ...props }: BlockImpressionProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                        <Htag tag='h2'>
                            Главные впечатления
                        </Htag>
                    <div className={styles.impression_block} {...props}>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Бархан Сарыкум</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Сулакский каньон</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Чиркейская ГЭС</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Водопад Тобот</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Карадахская теснина</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Селение-призрак Гамсутль</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Верхний Гуниб</div> 

                        <div className={styles.impression_block_item} {...props}><DoneIcon />Гунибская крепость</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Ворота Шамиля</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Салтинский водопад</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Аул Чох</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Селение златокузнецов Кубачи</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Каспийское море</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Экраноплан Лунь</div> 
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Древнейший город Дербент</div>
                        <div className={styles.impression_block_item} {...props}><DoneIcon />Крепость Нарын-Кала</div> 
                    </div>                    
            </div> 
            
        </div>
    );
};