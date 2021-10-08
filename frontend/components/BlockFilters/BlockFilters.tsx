import styles from './BlockFilters.module.css';
import { BlockFiltersProps } from './BlockFilters.props';
import cn from 'classnames';


export const BlockFilters = ({ block_style, children, className, ...props }: BlockFiltersProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.filter_item} {...props}>Тип тура</div>
                    <div className={styles.filter_item} {...props}>Язык группы</div>
                    <div className={styles.filter_item} {...props}>Цена</div>
                    <div className={styles.filter_item} {...props}>Туры с кешбеком</div>
                    <div className={styles.filter_item} {...props}>Средний возраст группы</div>
                    <div className={styles.filter_item} {...props}>Длительность (дни)</div>
                    <div className={styles.filter_item} {...props}>Осталось мест</div>
                    <div className={styles.filter_item} {...props}>Проживание</div>
                    <div className={styles.filter_item} {...props}>Активность</div>
                    <div className={styles.filter_item} {...props}>Рейтинг</div>
                    <div className={styles.filter_item} {...props}>Гарантированные даты</div>
                    
                    
                    
            </div> 
            
        </div>
    );
};