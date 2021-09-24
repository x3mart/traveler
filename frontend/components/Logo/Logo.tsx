import styles from './Logo.module.css';
import { LogoProps } from './Logo.props';
import LogoIcon from '/public/TM.svg';
import LogoNameIcon from '/public/Logoname.svg';
// import { LogoName } from '../../components';

import cn from 'classnames';

export const Logo = ({ children, href, className, ...props }: LogoProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.logo, className, {
                
            })}
            {...props}
        >{
            href
                ? <a href={href}>{children}</a>
                : <>{children}</>
        }   
            <LogoIcon />
            
        </div>
    );
};