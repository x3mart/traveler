import styles from './Tag.module.css';
import { TagProps } from './Tag.props';
import cn from 'classnames';

export const Tag = ({ size, children, href, className, ...props }: TagProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.tag, className, {
                [styles.s]: size == 's',
                [styles.m]: size == 'm',
                [styles.b]: size == 'b',
                [styles.l]: size == 'l',
                [styles.t]: size == 't',
                [styles.feedback]: size == 'feedback',    
                [styles.about_expert]: size == 'about_expert',            
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