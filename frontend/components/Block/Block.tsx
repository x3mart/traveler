import styles from './Tag.module.css';
import { TagProps } from './Block.props';
import cn from 'classnames';

export const Tag = ({ size, children, href, className, ...props }: TagProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.tag, className, {
                [styles.s]: size == 's',
                [styles.m]: size == 'm',
                [styles.b]: size == 'b',
                [styles.l]: size == 'l',
            })}
            {...props}
        >{
            href
                ? <a href={href}>{children}</a>
                : <>{children}</>
        }   
            
        </div>
    );
};