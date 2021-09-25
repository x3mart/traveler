import styles from './P.module.css';
import { PProps } from './P.props';
import cn from 'classnames';

export const P = ({ color, link, href, children, className, ...props }: PProps): JSX.Element => {    
    return (
        <p
            className={ cn(styles.p, className, {
                [styles.p_footer]: color == 'p_footer',
                [styles.p_footer_link]: link == 'p_footer_link',
                [styles.p_footer_link_col_2]: link == 'p_footer_link_col_2',
                [styles.p_footer_letter_spacing]: link == 'p_footer_letter_spacing',
                [styles.p_footer_letter_spacing_margin_top]: link == 'p_footer_letter_spacing_margin_top',
            })}
            {...props}
        >{
            href
                ? <a href={href}>{children}</a>
                : <>{children}</>
        }    
        </p>
    );
};