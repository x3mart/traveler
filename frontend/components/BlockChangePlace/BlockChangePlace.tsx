import styles from './BlockChangePlace.module.css';
import { BlockChangePlaceProps } from './BlockChangePlace.props';
import { BlockFiltersTypeTour } from '../../components/';
import cn from 'classnames';


    


export const BlockChangePlace = ({ children, className, ...props }: BlockChangePlaceProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.calendar, className, {
                
            })}
            {...props}
            
        >    
            {children}
            
            <div className={styles.place_block} {...props}>

                <BlockFiltersTypeTour children={undefined} />

                <div className={styles.change_contry} {...props}>
                    <div className={styles.change_contry_item} {...props}>Вся Россия</div>
                    <div className={styles.change_contry_item} {...props}>Адыгея</div>
                    <div className={styles.change_contry_item} {...props}>Алтай</div>
                    <div className={styles.change_contry_item} {...props}>Анапа</div>
                    <div className={styles.change_contry_item} {...props}>Архангельск и Архангельская область</div>
                    <div className={styles.change_contry_item} {...props}>Архыз</div>
                    <div className={styles.change_contry_item} {...props}>Байкал</div>
                    <div className={styles.change_contry_item} {...props}>Башкирия</div>
                    <div className={styles.change_contry_item} {...props}>Бурятия</div>

                    <div className={styles.change_contry_item} {...props}>Вся Россия</div>
                    <div className={styles.change_contry_item} {...props}>Адыгея</div>
                    <div className={styles.change_contry_item} {...props}>Алтай</div>
                    <div className={styles.change_contry_item} {...props}>Анапа</div>
                    <div className={styles.change_contry_item} {...props}>Архангельск и Архангельская область</div>
                    <div className={styles.change_contry_item} {...props}>Архыз</div>
                    <div className={styles.change_contry_item} {...props}>Байкал</div>
                    <div className={styles.change_contry_item} {...props}>Башкирия</div>
                    <div className={styles.change_contry_item} {...props}>Бурятия</div>

                    <div className={styles.change_contry_item} {...props}>Вся Россия</div>
                    <div className={styles.change_contry_item} {...props}>Адыгея</div>
                    <div className={styles.change_contry_item} {...props}>Алтай</div>
                    <div className={styles.change_contry_item} {...props}>Анапа</div>
                    <div className={styles.change_contry_item} {...props}>Архангельск и Архангельская область</div>
                    <div className={styles.change_contry_item} {...props}>Архыз</div>
                    <div className={styles.change_contry_item} {...props}>Байкал</div>
                    <div className={styles.change_contry_item} {...props}>Башкирия</div>
                    <div className={styles.change_contry_item} {...props}>Бурятия</div>
                </div>

                <div className={styles.change_contry_accept} {...props}>Применить</div>
                <div className={styles.change_contry_cancel} {...props}>Сбросить выбор</div>
            </div>
        </div>
    );
};


















