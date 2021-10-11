import styles from './BlockBreadCrumbs.module.css';
import { BlockBreadCrumbsProps } from './BlockBreadCrumbs.props';
import cn from 'classnames';
import Breadcrumbs from 'nextjs-breadcrumbs';

export const BlockBreadCrumbs = ({ block_style, children, margin, className, ...props }: BlockBreadCrumbsProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
                [styles.margin_first]: margin == 'margin_first',
                [styles.margin_second]: margin == 'margin_second',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    {/* <div className={styles.breadcrumb_main} {...props}>Главная </div>
                    <div>&nbsp;-&nbsp;Путешествия</div> */}
                    <Breadcrumbs useDefaultStyle rootLabel="Главная" replaceCharacterList="[{ from: '-', to: '-' }]" />

            </div> 
            
        </div>
    );
};