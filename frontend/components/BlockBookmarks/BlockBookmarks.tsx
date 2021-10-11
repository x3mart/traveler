import styles from './BlockBookmarks.module.css';
import { BlockBookmarksProps } from './BlockBookmarks.props';
import cn from 'classnames';

export const BlockBookmarks = ({ block_style, children, className, ...props }: BlockBookmarksProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.bookmarks_block} {...props}>
                        <div className={styles.bookmarks_block_item} {...props}>Обзор</div>
                        <div className={styles.bookmarks_block_item} {...props}>Галерея</div>
                        <div className={styles.bookmarks_block_item} {...props}>Маршрут</div>
                        <div className={styles.bookmarks_block_item} {...props}>Проживание</div>
                        <div className={styles.bookmarks_block_item} {...props}>Что включено</div>
                        <div className={styles.bookmarks_block_item} {...props}>Тревел-Эксперт</div>
                        <div className={styles.bookmarks_block_item} {...props}>Отзывы</div> 
                    </div>                    
            </div> 
            
        </div>
    );
};