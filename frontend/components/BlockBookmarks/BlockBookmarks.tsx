import styles from './BlockBookmarks.module.css';
import { BlockBookmarksProps } from './BlockBookmarks.props';
import cn from 'classnames';

export const BlockBookmarks = ({ block_style, children, className }: BlockBookmarksProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            
        >
            
            <div className={styles.wrapper} >
                {children}
                    <div className={styles.bookmarks_block} >
                        <div className={ (styles.bookmarks_block_item, styles.bookmarks_block_item_active)} >Обзор</div>
                        <div className={styles.bookmarks_block_item} >Галерея</div>
                        <div className={styles.bookmarks_block_item} >Маршрут</div>
                        <div className={styles.bookmarks_block_item} >Проживание</div>
                        <div className={styles.bookmarks_block_item} >Что включено</div>
                        <div className={styles.bookmarks_block_item} >Тревел-Эксперт</div>
                        <div className={styles.bookmarks_block_item} >Отзывы</div> 
                    </div>                    
            </div> 
            
        </div>
    );
};