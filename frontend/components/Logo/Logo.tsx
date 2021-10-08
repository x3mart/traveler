import styles from './Logo.module.css';
import { LogoProps } from './Logo.props';
import LogoIcon from '/public/TM.svg';
import cn from 'classnames';
import Link from 'next/link';

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
        <Link href='/'>
            <LogoIcon />
        </Link>
        </div>
    );
};