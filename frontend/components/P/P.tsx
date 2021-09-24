import styles from './P.module.css';
import { PProps } from './P.props';
import cn from 'classnames';

export const P = ({ color, children, className, ...props }: PProps): JSX.Element => {    
    return (
        <p
            className={ cn(styles.p, className, {
                [styles.p_footer]: color == 'p_footer',
            })}
            {...props}
        >
            {children} 
            
        </p>
    );
};