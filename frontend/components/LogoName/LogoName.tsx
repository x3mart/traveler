import styles from './LogoName.module.css';
import { LogoNameProps } from './LogoName.props';
import LogoNameIcon from '/public/Logoname.svg';

import cn from 'classnames';

export const LogoName = ({ color, children, href, className, ...props }: LogoNameProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.logo, className, {
                [styles.logo_header]: color == 'logo_header',
                [styles.logo_footer]: color == 'logo_footer',
            })}
            {...props}
        >{
            href
                ? <a href={href}>{children}</a>
                : <>{children}</>
        }               
            <span>
                <LogoNameIcon />    
            </span> 
            
            
        </div>
    );
};