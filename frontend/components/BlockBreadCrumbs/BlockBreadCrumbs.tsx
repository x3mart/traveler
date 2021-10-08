import styles from './BlockBreadCrumbs.module.css';
import { BlockBreadCrumbsProps } from './BlockBreadCrumbs.props';
import cn from 'classnames';


export const BlockBreadCrumbs = ({ block_style, children, className, ...props }: BlockBreadCrumbsProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.breadcrumb_main} {...props}>Главная </div>
                    <div>&nbsp;-&nbsp;Путешествия</div>
                    
            </div> 
            
        </div>
    );
};